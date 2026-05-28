import groovy.json.JsonSlurper
import groovy.json.JsonOutput
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.core.JsonToken
import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.types.StructType
import org.slf4j.LoggerFactory
import java.io.File
import static org.apache.spark.sql.functions.*

def logger = LoggerFactory.getLogger("darpan.reconciliation.view.MissingJsonList")

// --------------------------------------------------------------------------------
// Inputs
// --------------------------------------------------------------------------------
// outputFile (String): Path to the output file or directory
// pageIndex (String/Int): Page number (0-based)
// pageSize (String/Int): Page size
// missingType (String): Filter type (e.g., "missing_in_json1")
// recordId (String): Optional filter applied to record id/compare_id/record_id fields

long viewMaxInMemoryBytes = 5 * 1024 * 1024 // 5MB limit for in-memory loading (legacy check)

// Helper: Parse safe int
def parseIntSafe = { val, defVal ->
    if (val == null) return defVal
    if (val instanceof Integer) return val
    try { return Integer.parseInt(val.toString()) } catch (Exception e) { return defVal }
}

def trimToNull = { str ->
    def s = str?.toString()?.trim()
    return (s && s.length() > 0) ? s : null
}

def resolveParamValue = { String name ->
    def rawValue = ec.web?.parameters?.get(name)
    if (rawValue == null) rawValue = ec.web?.requestParameters?.get(name)
    def lastNonBlank = { Iterable items ->
        def resolved = null
        items?.each { item ->
            def candidate = item?.toString()
            if (candidate != null && candidate.trim()) {
                resolved = candidate
            }
        }
        return resolved
    }
    if (rawValue instanceof Collection) return lastNonBlank(rawValue)
    if (rawValue != null && rawValue.getClass().isArray()) return lastNonBlank(rawValue as List)
    return rawValue
}

def requestUri = ec.web?.request?.getRequestURI() ?: ''
if (requestUri.contains('/menuData')) return
if (ec.context?.viewError) return

if (!outputFile) outputFile = ec.context?.outputFile

int index = parseIntSafe(resolveParamValue('pageIndex'), 0)
int size = parseIntSafe(resolveParamValue('pageSize'), 20)
if (size <= 0) size = 20
if (index < 0) index = 0
String filterType = trimToNull((resolveParamValue('missingType') ?: ec.context?.get('missingType'))?.toString())
String filterMissingLabel = trimToNull(ec.context?.viewMissingLabel)
String recordIdSearch = trimToNull(resolveParamValue('recordId') ?: resolveParamValue('record_id'))
String recordIdSearchLower = recordIdSearch?.toLowerCase()

// Normalize for comparison
if (filterType) filterType = filterType.trim()
if (filterMissingLabel) filterMissingLabel = filterMissingLabel.trim()

// Validate inputs
if (!outputFile) {
    ec.message.addError("No output file specified")
    logger.warn("MissingJsonList missing outputFile pageIndex=${index} pageSize=${size} filterType=${filterType}")
    return
}

File targetFile = new File(outputFile)
if (!targetFile.exists()) {
    // try relative to runtime
    String rt = ec.factory.getRuntimePath()
    targetFile = new File(rt, outputFile)
    if (!targetFile.exists()) {
         ec.message.addError("Output file not found: ${outputFile}")
         logger.warn("MissingJsonList outputFile not found path=${outputFile} runtime=${rt} pageIndex=${index} pageSize=${size} filterType=${filterType}")
         return
    }
}
logger.info("MissingJsonList start file=${targetFile.absolutePath} isDirectory=${targetFile.isDirectory()} pageIndex=${index} pageSize=${size} filterType=${filterType} recordIdSearch=${recordIdSearch}")

// --------------------------------------------------------------------------------
// Logic
// --------------------------------------------------------------------------------

def extractIds = { row ->
    def ids = []
    def addVal = { val ->
        def txt = val?.toString()?.trim()
        if (txt) ids.add(txt)
    }
    addVal(row?.id)
    addVal(row?.record_id ?: row?.recordId)
    addVal(row?.compare_id ?: row?.compareId)
    if (row?.data instanceof Map) {
        addVal(row.data?.id)
        addVal(row.data?.record_id ?: row.data?.recordId)
        addVal(row.data?.compare_id ?: row.data?.compareId)
    }
    return ids
}

def matchesRecordId = { row ->
    if (!recordIdSearchLower) return true
    def ids = extractIds(row)
    return ids.any { idVal -> idVal?.toLowerCase()?.contains(recordIdSearchLower) }
}

def rowToMap
rowToMap = { Row r ->
    if (r == null) return null
    def m = [:]
    r.schema().fieldNames().each { fname ->
        def val = r.getAs(fname)
        if (val instanceof Row) {
            m[fname] = rowToMap(val)
        } else if (val instanceof Iterable && !(val instanceof CharSequence)) {
            def list = []
            val.each { item ->
                list.add(item instanceof Row ? rowToMap(item) : item)
            }
            m[fname] = list
        } else {
            m[fname] = val
        }
    }
    return m
}

def hasFieldPath = { StructType schema, String path ->
    if (schema == null || !path) return false
    def current = schema
    for (String part : path.split("\\.")) {
        def field = current?.fields()?.find { it.name() == part }
        if (field == null) return false
        current = (field.dataType() instanceof StructType) ? (StructType) field.dataType() : null
    }
    return true
}

def messagesList = []
long listCount = 0

// Metadata defaults
Map metadata = [:]
Map summary = [:]

// Detect mode: Directory (Spark) vs Single File (Legacy/Small)
boolean isDirectory = targetFile.isDirectory()
List<File> dataFiles = []

if (isDirectory) {
    // Spark Output: Directory of JSONL files
    // Metadata usually missing or in a specific file. 
    // We assume the caller knows the context or we try to find a metadata.json if we wrote one?
    // Our new Mixed service creates a directory but doesn't strictly separate metadata yet unless we check for it.
    // Actually, Mixed service writes ONE file or directory. 
    // Spark 'write.json' creates a directory of part-*.json files. 
    // Any metadata we wrote manually might be lost if we used Spark write directly.
    // Legacy mixed reconciliation wrote a single JSON file for metadata wrapping; Spark writes directories of JSONL.
    // We keep support for both single-file outputs and Spark directory outputs.
    
    // Let's support both.
    
    targetFile.eachFile { f ->
        if ((f.name.startsWith("part-") || f.name.endsWith(".json")) && !f.name.endsWith(".crc") && !f.name.startsWith("_")) {
            dataFiles.add(f)
        }
    }
} else {
    dataFiles.add(targetFile)
}

// Check format. If single file, is it wrapped (metadata/differences array) or JSONL?
// Heuristic: Read first char. '{' = Wrapped Object (likely). 
// If it's a directory, assume JSONL.

boolean isWrappedFormat = !isDirectory
if (isWrappedFormat) {
    // It might still be JSONL if it's a single part file renamed.
    // Check start (ignore whitespace)
    // Check start (ignore whitespace) and verify structure
    try {
        def mapper = new ObjectMapper()
        targetFile.withInputStream { is ->
            def parser = mapper.getFactory().createParser(is)
            try {
                if (parser.nextToken() == JsonToken.START_OBJECT) {
                    // Peek at first few fields to determine type
                    boolean hasMetadata = false
                    boolean hasDifferences = false
                    int fieldsChecked = 0
                    
                    while (parser.nextToken() != JsonToken.END_OBJECT && fieldsChecked < 5) {
                        def name = parser.getCurrentName()
                        parser.nextToken() // move to value
                        if ("metadata".equals(name)) hasMetadata = true
                        if ("differences".equals(name)) hasDifferences = true
                        parser.skipChildren()
                        fieldsChecked++
                    }
                    
                    // If it has metadata or differences, it's likely a wrapped file.
                    if (!hasMetadata && !hasDifferences) {
                        isWrappedFormat = false
                    }
                } else {
                   isWrappedFormat = false
                }
            } finally {
                try { parser.close() } catch (Exception ignored) {}
            }
        }
    } catch (Throwable t) {
        // Catch Throwable to prevent transaction rollback on linkage/runtime errors
        logger.warn("MissingJsonList format detection failed (defaulting to JSONL/Spark): ${t.toString()}")
        isWrappedFormat = false 
    }
}

logger.info("MissingJsonList detected format: ${isWrappedFormat ? 'Wrapped (Legacy/Single)' : 'JSONL (Spark/Directory)'} for file ${targetFile.name}")

def trySparkSearch = {
    if (!recordIdSearchLower) return false
    SparkSession spark = null
    boolean stopSpark = false
    try {
        String sparkMasterCfg = ec.resource?.properties?.get('spark.master') ?: "local[*]"
        try {
            spark = SparkSession.getActiveSession()?.orElse(null)
        } catch (Throwable ignored) { }
        if (spark == null) {
            spark = SparkSession.builder()
                    .appName("GenericReconciliationViewSearch")
                    .master(sparkMasterCfg)
                    .config("spark.sql.shuffle.partitions", "8")
                    .config("spark.sql.files.maxPartitionBytes", "134217728")
                    .getOrCreate()
            stopSpark = true
        }

        def reader = spark.read().option("multiLine", "true")
        def baseDf = reader.json(targetFile.absolutePath)
        def cols = (baseDf?.columns() ?: []) as List

        if (metadata.isEmpty() && cols.contains("metadata")) {
            try {
                def metaRow = baseDf.select("metadata").limit(1).collectAsList()
                if (metaRow && metaRow[0]?.get(0) instanceof Row) {
                    metadata = rowToMap(metaRow[0].getAs("metadata")) ?: [:]
                }
            } catch (Exception ignored) { }
        }

        def diffDf
        if (cols.contains("differences")) {
            diffDf = baseDf.select(posexplode(col("differences")).alias("pos", "diff"))
                    .select(col("pos"), col("diff.*"))
        } else {
            diffDf = baseDf
            if (!((diffDf?.columns() ?: []) as List).contains("pos")) {
                diffDf = diffDf.withColumn("pos", monotonically_increasing_id())
            }
        }

        String likePattern = (recordIdSearchLower.contains("%") || recordIdSearchLower.contains("_")) ?
                recordIdSearchLower : "%${recordIdSearchLower}%"
        List<String> idPaths = [
                "id", "record_id", "recordId", "compare_id", "compareId",
                "data.id", "data.record_id", "data.recordId", "data.compare_id", "data.compareId",
                "data.legacyResourceId", "data.node.legacyResourceId", "data.node.id"
        ]
        def idCond = null
        def schema = diffDf.schema() as StructType
        for (String path : idPaths) {
            try {
                if (!hasFieldPath(schema, path)) continue
                def cond = lower(col(path)).like(lit(likePattern))
                idCond = idCond ? idCond.or(cond) : cond
            } catch (Exception ignored) { }
        }
        if (idCond == null) idCond = lit(true)

        String filterTypeLower = filterType ? filterType.toLowerCase() : null
        String filterMissingLower = filterMissingLabel ? filterMissingLabel.toLowerCase() : null
        def typeCond = filterTypeLower ? lower(col("type")).equalTo(lit(filterTypeLower)) : lit(true)
        def missingCond = filterMissingLower ? lower(col("missingIn")).equalTo(lit(filterMissingLower)) : lit(false)
        def finalCond = idCond.and(typeCond.or(missingCond))

        def filtered = diffDf.filter(finalCond)
        def windowSpec = Window.orderBy(col("pos"))
        def numbered = filtered.withColumn("_rn", row_number().over(windowSpec))
        long total = numbered.count()
        listCount = total

        int effectiveIndex = index < 0 ? 0 : index
        if (total > 0 && ((long) effectiveIndex * (long) size) >= total) {
            effectiveIndex = 0
        }
        long startRow = (long) effectiveIndex * (long) size
        long endRow = startRow + (long) size
        def pageDf = numbered.filter(col("_rn").gt(startRow).and(col("_rn").lte(endRow))).drop("_rn")
        def rows = pageDf.collectAsList()
        messagesList = rows.collect { Row r -> rowToMap(r) ?: [:] }
        index = effectiveIndex

        logger.info("MissingJsonList Spark search handled matches=${total} recordIdSearch=${recordIdSearch} pageIndex=${index} pageSize=${size}")
        return true
    } catch (Throwable t) {
        logger.warn("MissingJsonList Spark search failed; falling back to file scan: ${t.toString()}", t)
        return false
    } finally {
        if (stopSpark && spark != null) {
            try { spark.stop() } catch (Exception ignored) { }
        }
    }
}

def parseJsonLines = { List<File> files, int pageIdx ->
    messagesList = []
    def objectMapper = new ObjectMapper()
    long totalMatched = 0
    int added = 0
    long skip = (long)pageIdx * (long)size
    files.each { File f ->
        f.withReader("UTF-8") { reader ->
            reader.eachLine { line ->
                if (!line?.trim()) return
                try {
                    def row = objectMapper.readValue(line, Map.class)
                    def typeStr = row?.type?.toString()?.trim()
                    def missingStr = row?.missingIn?.toString()?.trim()
                    boolean typeMatch = !filterType || (typeStr && typeStr.equalsIgnoreCase(filterType))
                    boolean labelMatch = filterMissingLabel && missingStr && missingStr.equalsIgnoreCase(filterMissingLabel)
                    boolean idMatch = matchesRecordId(row)
                    if ((typeMatch || labelMatch) && idMatch) {
                        totalMatched++
                        if (totalMatched > skip && added < size) {
                            messagesList.add(row)
                            added++
                        }
                    }
                } catch (Exception ignored) { }
            }
        }
    }
    listCount = totalMatched
}

def loadPageForIndex = { int pageIdx ->
    messagesList = []
    listCount = 0
    int effectiveIndex = pageIdx

    if (isWrappedFormat) {
        if (isDirectory) {
            // Unified/Spark output written as JSONL part files
            parseJsonLines(dataFiles, effectiveIndex)
        } else {
            // Legacy wrapped file (also covers unified single-file JSON output)
            try {
                def objectMapper = new ObjectMapper()
                if (targetFile.length() < viewMaxInMemoryBytes) {
                    def root = objectMapper.readTree(targetFile)
                    if (root.has("metadata")) metadata = objectMapper.convertValue(root.get("metadata"), Map.class)
                    def diffs = root.get("differences")
                    if (diffs && diffs.isArray()) {
                        logger.info("MissingJsonList processing 'differences' array. Size: ${diffs.size()}")
                        List<Map> all = []
                        int debugCount = 0
                        diffs.each { n ->
                            Map r = objectMapper.convertValue(n, Map.class)
                            def typeStr = r?.type?.toString()?.trim()
                            def missingStr = r?.missingIn?.toString()?.trim()
                            if (debugCount < 3) {
                                 logger.info("MissingJsonList Row[${debugCount}]: type=${typeStr} missingIn=${missingStr} id=${r.id}")
                                 boolean tMatch = !filterType || (typeStr && typeStr.equalsIgnoreCase(filterType))
                                 boolean lMatch = filterMissingLabel && (missingStr && missingStr.equalsIgnoreCase(filterMissingLabel))
                                 boolean idMatchDebug = matchesRecordId(r)
                                 logger.info("MissingJsonList Match Check: filterType='${filterType}' vs '${typeStr}' -> ${tMatch}. filterMissingLabel='${filterMissingLabel}' vs '${missingStr}' -> ${lMatch}. recordId='${recordIdSearch}' -> ${idMatchDebug}. Final: ${(tMatch || lMatch) && idMatchDebug}")
                                 debugCount++
                            }
                            boolean typeMatch = !filterType || (typeStr && typeStr.equalsIgnoreCase(filterType))
                            boolean labelMatch = filterMissingLabel && (missingStr && missingStr.equalsIgnoreCase(filterMissingLabel))
                            boolean idMatch = matchesRecordId(r)
                            if ((typeMatch || labelMatch) && idMatch) {
                                all.add(r)
                            }
                        }
                        listCount = all.size()
                        int start = effectiveIndex * size
                        if (start >= listCount && listCount > 0) {
                            effectiveIndex = 0
                            start = 0
                        }
                        int end = Math.min(start + size, (int)listCount)
                        if (start < listCount) messagesList = all.subList(start, end)
                    }
                } else {
                    long skip = (long) effectiveIndex * (long) size
                    long totalMatched = 0
                    int added = 0
                    logger.info("MissingJsonList streaming wrapped file size=${targetFile.length()} skip=${skip} pageSize=${size} filterType=${filterType}")
                    targetFile.withInputStream { is ->
                        def parser = objectMapper.getFactory().createParser(is)
                        try {
                            if (parser.nextToken() != JsonToken.START_OBJECT) {
                                throw new IllegalArgumentException("Invalid diff JSON format (expected object)")
                            }
                            while (parser.nextToken() != JsonToken.END_OBJECT) {
                                def fieldName = parser.getCurrentName()
                                parser.nextToken()
                                if ("metadata".equals(fieldName)) {
                                    try {
                                        metadata = objectMapper.readValue(parser, Map.class)
                                    } catch (Exception ignored) {
                                        parser.skipChildren()
                                    }
                                } else if ("differences".equals(fieldName)) {
                                    if (parser.getCurrentToken() != JsonToken.START_ARRAY) {
                                        parser.skipChildren()
                                        continue
                                    }
                                    while (parser.nextToken() != JsonToken.END_ARRAY) {
                                        if (parser.getCurrentToken() != JsonToken.START_OBJECT && parser.getCurrentToken() != JsonToken.START_ARRAY) {
                                            parser.skipChildren()
                                            continue
                                        }
                                        Map row = null
                                        try {
                                            row = objectMapper.readValue(parser, Map.class)
                                        } catch (Exception ignored) {
                                            parser.skipChildren()
                                        }
                                        if (row == null) continue
                                        def typeStr = row?.type?.toString()?.trim()
                                        def missingStr = row?.missingIn?.toString()?.trim()
                                        boolean typeMatch = !filterType || (typeStr && typeStr.equalsIgnoreCase(filterType))
                                        boolean labelMatch = filterMissingLabel && (missingStr && missingStr.equalsIgnoreCase(filterMissingLabel))
                                        boolean idMatch = matchesRecordId(row)
                                        
                                        if ((typeMatch || labelMatch) && idMatch) {
                                            totalMatched++
                                            if (totalMatched > skip && added < size) {
                                                messagesList.add(row)
                                                added++
                                            }
                                        }
                                        if (added >= size) {
                                            while (parser.nextToken() != JsonToken.END_ARRAY) {
                                                if (parser.getCurrentToken() == JsonToken.START_OBJECT || parser.getCurrentToken() == JsonToken.START_ARRAY) {
                                                        try {
                                                            def rowSkip = objectMapper.readValue(parser, Map.class)
                                                            def skipType = rowSkip?.type?.toString()
                                                            def skipMissing = rowSkip?.missingIn?.toString()
                                                            boolean skipIdMatch = matchesRecordId(rowSkip)
                                                            if (skipIdMatch && (!filterType || (skipType && skipType.equalsIgnoreCase(filterType)) ||
                                                                    (filterMissingLabel && skipMissing && skipMissing.equalsIgnoreCase(filterMissingLabel)))) {
                                                                totalMatched++
                                                            }
                                                        } catch (Exception ignored) {
                                                            parser.skipChildren()
                                                        }
                                                } else {
                                                    parser.skipChildren()
                                                }
                                            }
                                            break
                                        }
                                    }
                                } else {
                                    parser.skipChildren()
                                }
                            }
                        } finally {
                            parser.close()
                        }
                    }
                    listCount = totalMatched
                }
            } catch (Exception e) {
                 logger.error("Failed to read legacy file", e)
            }

            if (listCount == 0 && messagesList.isEmpty()) {
                parseJsonLines([targetFile], effectiveIndex)
            }
        }

    } else {
        parseJsonLines(dataFiles, effectiveIndex)
    }

    return effectiveIndex
}

boolean sparkHandled = recordIdSearchLower ? trySparkSearch() : false

int resolvedPageIndex = index
if (!sparkHandled) {
    resolvedPageIndex = loadPageForIndex(index)
    if (recordIdSearchLower && listCount > 0 && messagesList.isEmpty() && resolvedPageIndex > 0) {
        logger.info("MissingJsonList recordIdSearch=${recordIdSearch} has ${listCount} matches but pageIndex=${resolvedPageIndex} exceeds range; resetting to first page")
        resolvedPageIndex = loadPageForIndex(0)
    }
    index = resolvedPageIndex
}

// --------------------------------------------------------------------------------
// Output to Context
// --------------------------------------------------------------------------------

ec.context.put("list", messagesList)
ec.context.put("listCount", listCount)
ec.context.put("listPageIndex", index)
ec.context.put("listPageSize", size)
ec.context.put("metadata", metadata)

def missingRecords = []
messagesList.each { row ->
    def idCandidates = extractIds(row)
    def idVal = idCandidates ? idCandidates[0] : null
    def jsonPayload = row?.data ?: row
    if (jsonPayload instanceof String) {
        def txt = jsonPayload.trim()
        if (txt.startsWith("{") || txt.startsWith("[")) {
            try {
                jsonPayload = new JsonSlurper().parseText(txt)
            } catch (Exception ignored) {
                // leave as-is
            }
        }
    }
    def jsonString
    try {
        jsonString = JsonOutput.prettyPrint(JsonOutput.toJson(jsonPayload))
    } catch (Exception ignored) {
        jsonString = JsonOutput.toJson(jsonPayload)
    }
    missingRecords.add([id: idVal, json: jsonString])
}
ec.context.put("missingRecords", missingRecords)
ec.context.put("missingRecordsCount", listCount)

// Provide pagination variables expected by form-list macros
int pageIndexInt = index < 0 ? 0 : index
int pageSizeInt = size <= 0 ? 20 : size
int pageMaxIndex = listCount > 0 ? (int) ((listCount - 1) / pageSizeInt) : 0
int pageRangeLow = listCount > 0 ? (pageIndexInt * pageSizeInt) + 1 : 0
int pageRangeHigh = listCount > 0 ? Math.min((pageIndexInt + 1) * pageSizeInt, (int) listCount) : 0
ec.context.put("missingRecordsPageIndex", pageIndexInt)
ec.context.put("missingRecordsPageSize", pageSizeInt)
ec.context.put("missingRecordsPageMaxIndex", pageMaxIndex)
ec.context.put("missingRecordsPageRangeLow", pageRangeLow)
ec.context.put("missingRecordsPageRangeHigh", pageRangeHigh)

def label1 = metadata?.json1Label ?: "File 1"
def label2 = metadata?.json2Label ?: "File 2"

if (filterType && filterType.contains("json1")) { // heuristic
    ec.context.put("missingListTitle", "Missing in ${label1}")
} else if (filterType && filterType.contains("json2")) {
    ec.context.put("missingListTitle", "Missing in ${label2}")
} else {
    ec.context.put("missingListTitle", "Differences")
}

ec.context.put("file1Label", label1)
ec.context.put("file2Label", label2)
ec.context.put("recordIdSearch", recordIdSearch)

logger.info("MissingJsonList completed listCount=${listCount} returned=${messagesList?.size()} filterType=${filterType} recordIdSearch=${recordIdSearch} pageIndex=${index} pageSize=${size}")
