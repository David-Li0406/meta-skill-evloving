import org.apache.commons.csv.CSVFormat
import org.apache.commons.csv.CSVParser
import org.apache.commons.csv.CSVPrinter
import org.apache.commons.fileupload.FileItem
import org.slf4j.LoggerFactory

import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Paths

def logger = LoggerFactory.getLogger("darpan.bom.BomCycleCheck")

def normalize = { val ->
    def str = val?.toString()?.trim()
    return str ? str : null
}
def sanitizeFileName = { String name ->
    return (name ?: "bom").replaceAll("[^A-Za-z0-9._-]", "_")
}
def toBoolean = { val, boolean defaultVal ->
    if (val == null) return defaultVal
    return val.toString().equalsIgnoreCase("true")
}
def resolvePath = { String location ->
    if (!location) return null
    def ref = ec.resource.getLocationReference(location)
    if (ref != null) {
        def file = ref.getFile()
        if (file != null) return file.getAbsolutePath()
        def url = ref.getUrl()
        if (url != null) return url.toString()
    }
    return location
}
def ensureDir = { String location ->
    def dirRef = ec.resource.getLocationReference(location)
    if (dirRef == null) {
        throw new IllegalArgumentException("Unable to resolve location: ${location}")
    }
    File dirFile = dirRef.getFile()
    if (dirFile != null && !dirFile.exists()) dirFile.mkdirs()
    return dirRef
}
def saveFileItem = { FileItem fileItem, String dirLocation ->
    def dirRef = ensureDir(dirLocation)
    String safeName = sanitizeFileName(fileItem.getName())
    String timestamp = ec.l10n.format(ec.user.nowTimestamp, "yyyyMMdd-HHmmssSSS")
    def fileRef = dirRef.makeFile("${timestamp}-${safeName}")
    File targetFile = fileRef.getFile()
    if (targetFile != null) {
        try {
            fileItem.write(targetFile)
            return fileRef
        } catch (Exception e) {
            logger.warn("Direct FileItem write failed, falling back to stream: ${e.message}")
        }
    }
    fileRef.putStream(fileItem.getInputStream())
    return fileRef
}
def uniqueFile = { File dir, String baseName ->
    String cleanName = sanitizeFileName(baseName)
    int dotIdx = cleanName.lastIndexOf(".")
    String prefix = dotIdx > 0 ? cleanName.substring(0, dotIdx) : cleanName
    String suffix = dotIdx > 0 ? cleanName.substring(dotIdx) : ""

    File target = new File(dir, cleanName)
    int counter = 1
    while (target.exists()) {
        target = new File(dir, "${prefix}-${counter}${suffix}")
        counter++
    }
    return target
}

if (!bomFile && !bomLocation) {
    throw new IllegalArgumentException("bomFile or bomLocation is required")
}

boolean includeHeader = toBoolean(hasHeader, true)
char delimiterChar = delimiter ? delimiter.toString().charAt(0) : ','
String parentField = normalize(parentFieldName) ?: "product-sku"
String componentField = normalize(componentFieldName) ?: "product-sku-to"
int parentIdx = (parentColumnIndex ?: 1) as int
int componentIdx = (componentColumnIndex ?: 2) as int
if (parentIdx < 1 || componentIdx < 1) {
    throw new IllegalArgumentException("parentColumnIndex and componentColumnIndex must be 1 or greater")
}
String assocTypeField = normalize(assocTypeFieldName) ?: "product-assoc-type-id"
String assocTypeFilterVal = normalize(assocTypeFilter)

String baseTempLoc = tempLocation ?: "runtime://tmp/bom/cycle-check"
String inputDirLoc = baseTempLoc.endsWith("/") ? (baseTempLoc + "input") : (baseTempLoc + "/input")
String outputDirLoc = outputLocation ?: (baseTempLoc.endsWith("/") ? (baseTempLoc + "output") : (baseTempLoc + "/output"))

String inputPath
String inputLabel
if (bomFile) {
    def savedRef = saveFileItem((FileItem) bomFile, inputDirLoc)
    inputPath = savedRef.getFile()?.getAbsolutePath() ?: savedRef.getLocation()
    inputLabel = bomFile.getName()
    logger.info("Saved BOM upload to ${inputPath}")
} else {
    inputPath = resolvePath(bomLocation.toString())
    inputLabel = bomLocation.toString()
}

if (!inputPath) {
    throw new IllegalArgumentException("Unable to resolve BOM input path from bomLocation")
}

def format = CSVFormat.DEFAULT
        .withIgnoreSurroundingSpaces()
        .withIgnoreEmptyLines()
        .withTrim()
        .withDelimiter(delimiterChar)
if (includeHeader) format = format.withFirstRecordAsHeader()

List<String> headerNames = []
Map<String, Integer> headerIndexByLower = [:]
List<Map> rows = []
Map<String, Set<String>> graph = [:].withDefault { new LinkedHashSet<String>() }
Set<String> selfLoopNodes = new LinkedHashSet<>()
Set<String> nodes = new LinkedHashSet<>()
long skippedMissing = 0
long skippedAssoc = 0

CSVParser parser = null
def reader = Files.newBufferedReader(Paths.get(inputPath), StandardCharsets.UTF_8)
try {
    parser = new CSVParser(reader, format)
    if (includeHeader && parser.getHeaderMap()) {
        headerNames.addAll(parser.getHeaderMap().keySet())
        headerNames.eachWithIndex { String name, int idx ->
            headerIndexByLower[name?.toLowerCase()] = idx
        }
    }

    def getField = { record, String headerLower, int fallbackIndex ->
        Integer headerIdx = includeHeader ? headerIndexByLower[headerLower] : null
        int idxToUse = headerIdx != null ? headerIdx.intValue() : fallbackIndex
        if (idxToUse < 0 || idxToUse >= record.size()) return null
        return record.get(idxToUse)
    }

    parser.each { record ->
        def values = []
        record.iterator().each { values.add(it) }

        def parentVal = normalize(getField(record, parentField.toLowerCase(), parentIdx - 1))
        def childVal = normalize(getField(record, componentField.toLowerCase(), componentIdx - 1))
        def assocTypeVal = assocTypeField ? normalize(getField(record, assocTypeField.toLowerCase(), 2)) : null

        if (assocTypeFilterVal && !assocTypeVal?.equalsIgnoreCase(assocTypeFilterVal)) {
            skippedAssoc++
            return
        }
        if (!parentVal || !childVal) {
            skippedMissing++
            return
        }

        nodes.add(parentVal)
        nodes.add(childVal)
        graph[parentVal].add(childVal)
        if (parentVal == childVal) selfLoopNodes.add(parentVal)

        rows.add([
                parent      : parentVal,
                child       : childVal,
                values      : values,
                recordNumber: record.recordNumber
        ])
    }
} finally {
    if (parser != null) parser.close()
    reader.close()
}

def indexMap = [:]
def lowLink = [:]
def onStack = [:].withDefault { false }
List<String> stack = []
int indexCounter = 0
List<List<String>> sccList = []

def strongConnect
// Tarjan strongly connected components to isolate cyclic nodes
strongConnect = { String node ->
    indexMap[node] = indexCounter
    lowLink[node] = indexCounter
    indexCounter++
    stack.add(node)
    onStack[node] = true

    for (String neighbor : graph[node]) {
        if (!indexMap.containsKey(neighbor)) {
            strongConnect(neighbor)
            lowLink[node] = Math.min(lowLink[node], lowLink[neighbor])
        } else if (onStack[neighbor]) {
            lowLink[node] = Math.min(lowLink[node], indexMap[neighbor])
        }
    }

    if (lowLink[node] == indexMap[node]) {
        List<String> component = []
        while (!stack.isEmpty()) {
            String w = stack.remove(stack.size() - 1)
            onStack[w] = false
            component.add(w)
            if (w == node) break
        }
        sccList.add(component)
    }
}

nodes.each { if (!indexMap.containsKey(it)) strongConnect(it) }

Map<String, Integer> sccIdByNode = [:]
List<Map> cyclicComponents = []
sccList.eachWithIndex { List<String> component, int idx ->
    boolean hasSelfLoop = component.size() == 1 && selfLoopNodes.contains(component[0])
    boolean hasCycle = component.size() > 1 || hasSelfLoop
    component.each { sccIdByNode[it] = idx }
    if (hasCycle) {
        cyclicComponents.add([id: idx, nodes: component])
    }
}
Set<Integer> cyclicIds = cyclicComponents.collect { it.id } as Set

List<Map> importableRows = []
List<Map> problemRows = []
rows.each { row ->
    Integer parentSccId = sccIdByNode[row.parent]
    Integer childSccId = sccIdByNode[row.child]
    boolean inCycle = row.parent == row.child
    if (!inCycle && parentSccId != null && parentSccId == childSccId && cyclicIds.contains(parentSccId)) {
        inCycle = true
    }
    if (inCycle) {
        def cycleNodes = cyclicComponents.find { it.id == parentSccId }?.nodes ?: [row.parent, row.child]
        problemRows.add(row + [cycleNodes: cycleNodes, errorReason: "Reciprocal relationship detected"])
    } else {
        importableRows.add(row)
    }
}

def outputDirRef = ensureDir(outputDirLoc)
File outputDirFile = outputDirRef.getFile()
if (outputDirFile == null) {
    throw new IllegalArgumentException("Output location must resolve to a filesystem directory: ${outputDirLoc}")
}
if (!outputDirFile.exists()) outputDirFile.mkdirs()

String timestamp = ec.l10n.format(ec.user.nowTimestamp, "yyyyMMdd-HHmmss")
String baseName = sanitizeFileName(inputLabel ?: "bom")
File importableFile = uniqueFile(outputDirFile, "${baseName}-importable-${timestamp}.csv")
File problemFile = uniqueFile(outputDirFile, "${baseName}-errors-${timestamp}.csv")

def importFormat = CSVFormat.DEFAULT.withDelimiter(delimiterChar)
if (includeHeader && headerNames) importFormat = importFormat.withHeader((String[]) headerNames.toArray(new String[0]))

List<String> errorHeader = headerNames ? new ArrayList<>(headerNames) : []
if (includeHeader) errorHeader.addAll(["error_reason", "cycle_description"])
def problemFormat = CSVFormat.DEFAULT.withDelimiter(delimiterChar)
if (includeHeader && errorHeader) problemFormat = problemFormat.withHeader((String[]) errorHeader.toArray(new String[0]))

CSVPrinter importPrinter = null
CSVPrinter problemPrinter = null
try {
    importPrinter = new CSVPrinter(new OutputStreamWriter(new FileOutputStream(importableFile), StandardCharsets.UTF_8), importFormat)
    problemPrinter = new CSVPrinter(new OutputStreamWriter(new FileOutputStream(problemFile), StandardCharsets.UTF_8), problemFormat)

    importableRows.each { row -> importPrinter.printRecord(row.values) }

    problemRows.each { row ->
        def rowValues = []
        rowValues.addAll((Collection) row.values)
        def cycleNodesList = row.cycleNodes ?: []
        String description
        if (!cycleNodesList || cycleNodesList.size() == 0) {
            description = ""
        } else if (cycleNodesList.size() == 1) {
            description = "Self relationship on ${cycleNodesList[0]}"
        } else {
            // Close the loop for readability: A -> B -> C -> A
            def loop = new ArrayList(cycleNodesList)
            loop.add(cycleNodesList[0])
            description = "Cycle among ${cycleNodesList.join(', ')} (path: ${loop.join(' -> ')})"
        }
        rowValues.add(row.errorReason ?: "Cyclic relationship detected")
        rowValues.add(description)
        problemPrinter.printRecord(rowValues)
    }
} finally {
    if (importPrinter != null) importPrinter.close()
    if (problemPrinter != null) problemPrinter.close()
}

importableFileName = importableFile.getName()
problemFileName = problemFile.getName()
importableLocation = (outputDirLoc.endsWith("/") ? outputDirLoc[0..-2] : outputDirLoc) + "/" + importableFileName
problemLocation = (outputDirLoc.endsWith("/") ? outputDirLoc[0..-2] : outputDirLoc) + "/" + problemFileName
importableRowCount = importableRows.size()
problemRowCount = problemRows.size()
totalRowCount = rows.size()
cycleCount = cyclicComponents.size()
skippedRowCount = skippedMissing + skippedAssoc
cycleGroups = cyclicComponents.collect { [size: it.nodes?.size() ?: 0, nodes: it.nodes] }

logger.info("BOM cycle check complete: totalRows=${totalRowCount} importable=${importableRowCount} problems=${problemRowCount} cycles=${cycleCount} skippedMissing=${skippedMissing} skippedAssoc=${skippedAssoc}")
