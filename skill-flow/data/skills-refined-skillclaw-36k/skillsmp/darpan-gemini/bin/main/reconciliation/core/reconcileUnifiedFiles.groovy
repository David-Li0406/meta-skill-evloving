import groovy.json.JsonOutput
import org.apache.spark.sql.Dataset
import org.apache.spark.sql.Row
import org.apache.spark.sql.SparkSession
import org.apache.spark.storage.StorageLevel
import org.slf4j.LoggerFactory
import static org.apache.spark.sql.functions.*

def logger = LoggerFactory.getLogger("darpan.reconciliation.core.UnifiedReconciliation")

def normalize = { it?.toString()?.trim() }
def normalizeSlug = { String val ->
    def normalized = normalize(val)
    if (!normalized) return null
    def slug = normalized.replaceAll(/[^A-Za-z0-9_-]/, "-")
    slug = slug.replaceAll(/-+/, "-")
    slug = slug.replaceAll(/^[-_]+|[-_]+$/, "")
    return slug ?: null
}
def normalizeJsonIdExpr = { String expr ->
    def raw = normalize(expr)
    if (!raw) return "\$.id"
    if (raw.startsWith("\$")) return raw
    if (raw.contains("[") || raw.contains(".")) return raw.startsWith("\$.") ? raw : "\$." + raw
    return "\$[*].${raw}"
}
def normalizeCsvId = { String expr ->
    def raw = normalize(expr)
    if (!raw) return "id"
    if (raw.startsWith("\$")) {
        def parts = raw.tokenize(".")
        return parts ? parts[-1].replaceAll(/\[.*\]/, "") : "id"
    }
    return raw
}
def resolvePath = { String location ->
    def rr = ec.resource.getLocationReference(location)
    if (rr != null && rr.supportsUrl()) {
        def url = rr.getUrl()
        if (url != null) {
            if ("file".equalsIgnoreCase(url.protocol)) {
                try {
                    return new File(url.toURI()).getAbsolutePath()
                } catch (Exception e) {
                    return url.getPath()
                }
            }
            return url.toString()
        }
    }
    return location
}
def normalizeSparkPath = { String jsonPath ->
    if (!jsonPath) return jsonPath
    def path = jsonPath.toString().trim()
    path = path.replaceFirst(/^\$\[\*\]/, "")
    path = path.replaceFirst(/^\$\./, "")
    if (path.startsWith(".")) path = path.substring(1)
    return path
}
def convertJsonPathToSpark = { String jsonPath ->
    def path = normalizeSparkPath(jsonPath)
    if (!path) {
        throw new IllegalArgumentException("JSONPath ${jsonPath} resolves to an empty field path.")
    }
    if (path.contains("[*]")) {
        def parts = path.split(/\[\*\]/)
        if (parts.length == 2) {
            def arrayPath = parts[0]
            def afterArray = parts[1].replaceFirst(/^\./, "")
            return [needsExplode: true, arrayPath: arrayPath, fieldPath: afterArray]
        }
    }
    return [needsExplode: false, path: path]
}
def assertRootFieldExists = { Dataset df, String rootField, String pathLabel ->
    def rootFields = (df.columns() ?: []) as List
    if (!rootFields.contains(rootField)) {
        throw new IllegalArgumentException("JSONPath ${pathLabel} does not match root fields. Available root fields: ${rootFields.join(', ')}")
    }
}
def buildJsonIdDf = { Dataset rawDf, Map pathInfo, String pathLabel ->
    if (pathInfo.needsExplode) {
        def arrayPath = normalizeSparkPath(pathInfo.arrayPath)
        def fieldPath = normalizeSparkPath(pathInfo.fieldPath)
        def rootField = arrayPath?.split(/\./)[0]
        if (rootField) assertRootFieldExists(rawDf, rootField, pathLabel)

        return rawDf
                .selectExpr("explode(${arrayPath}) as exploded_item")
                .selectExpr("exploded_item.${fieldPath} as compare_id")
                .filter("compare_id IS NOT NULL AND length(trim(cast(compare_id as string))) > 0")
                .withColumn("compare_id", col("compare_id").cast("string"))
                .distinct()
    }
    def safePath = normalizeSparkPath(pathInfo.path)
    def rootField = safePath?.split(/\./)[0]
    if (rootField) assertRootFieldExists(rawDf, rootField, pathLabel)

    return rawDf
            .selectExpr("${safePath} as compare_id")
            .filter("compare_id IS NOT NULL AND length(trim(cast(compare_id as string))) > 0")
            .withColumn("compare_id", col("compare_id").cast("string"))
            .distinct()
}
def buildJsonDataDf = { Dataset rawDf, Map pathInfo, String pathLabel ->
    if (pathInfo.needsExplode) {
        def arrayPath = normalizeSparkPath(pathInfo.arrayPath)
        def fieldPath = normalizeSparkPath(pathInfo.fieldPath)
        return rawDf
                .selectExpr("explode(${arrayPath}) as exploded_item")
                .selectExpr("exploded_item.${fieldPath} as compare_id", "exploded_item as data")
                .filter("compare_id IS NOT NULL AND length(trim(cast(compare_id as string))) > 0")
                .withColumn("compare_id", col("compare_id").cast("string"))
    }
    def safePath = normalizeSparkPath(pathInfo.path)
    return rawDf
            .selectExpr("${safePath} as compare_id", "struct(*) as data")
            .filter("compare_id IS NOT NULL AND length(trim(cast(compare_id as string))) > 0")
            .withColumn("compare_id", col("compare_id").cast("string"))
}
def buildCsvIdDf = { Dataset rawDf, String fieldName ->
    def fieldExpr = fieldName?.replace("`", "``")
    if (!fieldExpr) throw new IllegalArgumentException("CSV id field is required")
    fieldExpr = "`" + fieldExpr + "`"
    return rawDf
            .selectExpr("${fieldExpr} as compare_id")
            .filter("compare_id IS NOT NULL AND length(trim(compare_id)) > 0")
            .withColumn("compare_id", col("compare_id").cast("string"))
            .distinct()
}
def buildCsvDataDf = { Dataset rawDf, String fieldName ->
    def fieldExpr = fieldName?.replace("`", "``")
    fieldExpr = "`" + fieldExpr + "`"
    return rawDf
            .selectExpr("${fieldExpr} as compare_id", "struct(*) as data")
            .filter("compare_id IS NOT NULL AND length(trim(compare_id)) > 0")
            .withColumn("compare_id", col("compare_id").cast("string"))
}

// Validate inputs
if (!file1Location || !file2Location) throw new IllegalArgumentException("file1Location and file2Location are required")
if (!file1Type || !file2Type) throw new IllegalArgumentException("file1Type and file2Type are required")

List<String> processingWarnings = (processingWarnings ?: []) as List<String>
List<String> validationErrors = (validationErrors ?: []) as List<String>

String type1 = normalize(file1Type)?.toUpperCase()
String type2 = normalize(file2Type)?.toUpperCase()
if (!type1 || !type2) throw new IllegalArgumentException("file types are required")

def reconType = "${type1}_${type2}"
reconciliationType = (reconType == "CSV_CSV") ? "CSV" : (reconType == "JSON_JSON" ? "JSON" : "MIXED")

String id1Expr = (type1 == "CSV") ? normalizeCsvId(file1IdExpression ?: file1IdField) : normalizeJsonIdExpr(file1IdExpression ?: file1IdField)
String id2Expr = (type2 == "CSV") ? normalizeCsvId(file2IdExpression ?: file2IdField) : normalizeJsonIdExpr(file2IdExpression ?: file2IdField)

String json1Schema = (type1 == "JSON") ? normalize(file1SchemaFileName) : null
String json2Schema = (type2 == "JSON") ? normalize(file2SchemaFileName) : null

if (type1 == "JSON" && !json1Schema) throw new IllegalArgumentException("JSON source 1 requires schemaFileName")
if (type2 == "JSON" && !json2Schema) throw new IllegalArgumentException("JSON source 2 requires schemaFileName")

String label1 = normalize(file1Label) ?: "File 1"
String label2 = normalize(file2Label) ?: "File 2"
String mappingSlug = normalizeSlug(reconciliationMappingName) ?: normalizeSlug(reconciliationMappingId)

String outputBaseLocation = outputLocation ?: "runtime://tmp/reconciliation/unified/output"
String sparkMasterToUse = sparkMaster ?: (ec.resource.properties['spark.master'] ?: "local[*]")
String sparkAppNameToUse = sparkAppName ?: "UnifiedReconciliation"

// Optional validation for JSON inputs
def validateJsonIfNeeded = { String loc, String schema, String label ->
    if (!schema) return
    try {
        def result = ec.service.sync()
                .name("jsonschema.JsonSchemaServices.validate#JsonLocationAgainstSchema")
                .parameters([jsonLocation: loc, schemaFileName: schema])
                .call()
        if (!result.valid) {
            result.errorMessages.each { msg ->
                validationErrors.add("${label}: ${msg}")
            }
        }
    } catch (Exception e) {
        validationErrors.add("${label}: ${e.message}")
    }
}
if (type1 == "JSON") validateJsonIfNeeded(file1Location, json1Schema, label1)
if (type2 == "JSON") validateJsonIfNeeded(file2Location, json2Schema, label2)

SparkSession spark = SparkSession.builder()
        .appName(sparkAppNameToUse)
        .master(sparkMasterToUse)
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .config("spark.sql.files.maxPartitionBytes", "134217728")
        .getOrCreate()

Dataset dfJson1 = null
Dataset dfJson2 = null
Dataset dfCsv1 = null
Dataset dfCsv2 = null
Dataset idDf1 = null
Dataset idDf2 = null
Dataset dataDf1 = null
Dataset dataDf2 = null

try {
    def path1 = resolvePath(file1Location)
    def path2 = resolvePath(file2Location)
    def csvReader = spark.read().option("header", (hasHeader != null ? hasHeader : true).toString()).option("multiLine", "true")

    if (type1 == "JSON") {
        dfJson1 = spark.read().option("multiLine", "true").json(path1)
        def pathInfo1 = convertJsonPathToSpark(id1Expr)
        idDf1 = buildJsonIdDf(dfJson1, pathInfo1, id1Expr)
        dataDf1 = buildJsonDataDf(dfJson1, pathInfo1, id1Expr)
    } else {
        dfCsv1 = csvReader.csv(path1)
        idDf1 = buildCsvIdDf(dfCsv1, id1Expr)
        dataDf1 = buildCsvDataDf(dfCsv1, id1Expr)
    }

    if (type2 == "JSON") {
        dfJson2 = spark.read().option("multiLine", "true").json(path2)
        def pathInfo2 = convertJsonPathToSpark(id2Expr)
        idDf2 = buildJsonIdDf(dfJson2, pathInfo2, id2Expr)
        dataDf2 = buildJsonDataDf(dfJson2, pathInfo2, id2Expr)
    } else {
        dfCsv2 = csvReader.csv(path2)
        idDf2 = buildCsvIdDf(dfCsv2, id2Expr)
        dataDf2 = buildCsvDataDf(dfCsv2, id2Expr)
    }

    idDf1 = idDf1.persist(StorageLevel.DISK_ONLY())
    idDf2 = idDf2.persist(StorageLevel.DISK_ONLY())

    def onlyIn1Df = idDf1.join(idDf2, "compare_id", "left_anti").persist(StorageLevel.DISK_ONLY())
    def onlyIn2Df = idDf2.join(idDf1, "compare_id", "left_anti").persist(StorageLevel.DISK_ONLY())

    long count1 = onlyIn1Df.count()
    long count2 = onlyIn2Df.count()
    differenceCount = count1 + count2
    onlyInFile1Count = count1
    onlyInFile2Count = count2

    def normLabel = { String str ->
        def normalized = str?.replaceAll(/[^A-Za-z0-9_]/, "")
        return normalized ?: "file"
    }

    String label1Norm = normLabel(label1)
    String label2Norm = normLabel(label2)
    String missingInTypeForFile1 = "missing_in_${label2Norm}"
    String missingInTypeForFile2 = "missing_in_${label1Norm}"
    String noteForFile1 = "Present in ${label1}, missing in ${label2}".toString()
    String noteForFile2 = "Present in ${label2}, missing in ${label1}".toString()

    Dataset diffDf = null
    if (differenceCount > 0) {
        Dataset diffs1 = null
        if (count1 > 0) {
            Dataset joined1 = dataDf1.join(onlyIn1Df, "compare_id", "inner")
            diffs1 = joined1.select(
                    lit(missingInTypeForFile1).alias("type"),
                    col("compare_id").alias("id"),
                    lit(label1).alias("presentIn"),
                    lit(label2).alias("missingIn"),
                    to_json(col("data")).alias("data"),
                    lit(noteForFile1).alias("note")
            )
        }

        Dataset diffs2 = null
        if (count2 > 0) {
            Dataset joined2 = dataDf2.join(onlyIn2Df, "compare_id", "inner")
            diffs2 = joined2.select(
                    lit(missingInTypeForFile2).alias("type"),
                    col("compare_id").alias("id"),
                    lit(label2).alias("presentIn"),
                    lit(label1).alias("missingIn"),
                    to_json(col("data")).alias("data"),
                    lit(noteForFile2).alias("note")
            )
        }

        if (diffs1 != null && diffs2 != null) {
            diffDf = diffs1.union(diffs2)
        } else if (diffs1 != null) {
            diffDf = diffs1
        } else {
            diffDf = diffs2
        }
    }

    def outputRef = ec.resource.getLocationReference(outputBaseLocation)
    File outputDir = outputRef?.getFile()
    if (outputDir == null) {
        outputDir = outputBaseLocation.startsWith("/") ?
                new File(outputBaseLocation) :
                new File((String) ec.factory.getRuntimePath(), outputBaseLocation)
    }
    if (!outputDir.exists()) outputDir.mkdirs()

    String timestampIso = null
    try {
        timestampIso = ec.user.nowTimestamp?.toInstant()?.toString()
    } catch (Exception e) {
        timestampIso = ec.user.nowTimestamp?.toString()
    }

    String timestamp = ec.l10n.format(ec.user.nowTimestamp, "yyyyMMdd-HHmmss")
    String basePrefix = (reconciliationType == "CSV") ? "csv" : (reconciliationType == "JSON" ? "json" : "mixed")
    String defaultBase = mappingSlug ? "${mappingSlug}-diff-${timestamp}.json" : "${basePrefix}-diff-${timestamp}.json"
    String baseFileName = outputFileName ?: defaultBase
    if (!baseFileName.toLowerCase().endsWith(".json")) baseFileName = baseFileName + ".json"
    String nameRoot = baseFileName[0..-6]
    File outputFile = new File(outputDir, baseFileName)
    int suffix = 1
    while (outputFile.exists()) {
        baseFileName = "${nameRoot}-${suffix}.json"
        outputFile = new File(outputDir, baseFileName)
        suffix++
    }

    def outputLocationBase = outputBaseLocation.endsWith("/") ? outputBaseLocation[0..-2] : outputBaseLocation
    diffLocation = "${outputLocationBase}/${baseFileName}"
    diffFileName = baseFileName

    Map outputMetadata = [
            timestamp      : timestampIso,
            file1Label     : label1,
            file2Label     : label2,
            file1Type      : type1,
            file2Type      : type2,
            reconciliation : reconciliationType,
            file1Id        : id1Expr,
            file2Id        : id2Expr
    ]
    if (json1Schema) outputMetadata.file1Schema = json1Schema
    if (json2Schema) outputMetadata.file2Schema = json2Schema

    Map outputSummary = [
            totalDifferences: differenceCount,
            onlyInFile1Count: count1,
            onlyInFile2Count: count2
    ]

    outputFile.withWriter("UTF-8") { writer ->
        writer << "{\n"
        writer << "\"metadata\":" + JsonOutput.toJson(outputMetadata) + ",\n"
        writer << "\"summary\":" + JsonOutput.toJson(outputSummary) + ",\n"
        writer << "\"validationErrors\":" + JsonOutput.toJson(validationErrors) + ",\n"
        writer << "\"differences\":["
        boolean first = true
        if (differenceCount > 0 && diffDf != null) {
            def iter = diffDf.toJSON().toLocalIterator()
            while (iter.hasNext()) {
                def rowJson = iter.next()
                if (!first) writer << ","
                writer << "\n" << rowJson
                first = false
            }
        }
        if (!first) writer << "\n"
        writer << "]\n}"
    }

    context.processingWarnings = processingWarnings
    context.validationErrors = validationErrors

    logger.info("Unified reconciliation complete type=${reconciliationType} diff=${diffFileName} differences=${differenceCount}")

    // Unpersist
    onlyIn1Df.unpersist()
    onlyIn2Df.unpersist()
    idDf1.unpersist()
    idDf2.unpersist()
} catch (Exception e) {
    logger.error("Unified reconciliation failed", e)
    throw e
}
