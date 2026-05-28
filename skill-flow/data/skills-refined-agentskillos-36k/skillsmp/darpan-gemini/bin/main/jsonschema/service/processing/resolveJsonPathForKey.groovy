import groovy.json.JsonSlurper
import org.slf4j.LoggerFactory

def logger = LoggerFactory.getLogger("darpan.jsonschema.ResolveJsonPath")

if (!key) {
    throw new IllegalArgumentException("key is required")
}

def keyName = key.toString().trim()
if (!keyName) {
    throw new IllegalArgumentException("key is required")
}

if (keyName.startsWith('$')) {
    resolvedJsonPath = keyName
    matchingPaths = [keyName]
    found = true
    return
}

// --------------------------------------------------------------------------------
// Helper: Load Schema Logic (Inlined from JsonSchemaUtil)
// --------------------------------------------------------------------------------
def loadSchemaText = { Object id, Object name ->
    // 1. Try DB by ID
    if (id) {
        def schema = ec.entity.find("darpan.reconciliation.JsonSchema")
            .condition("jsonSchemaId", id).useCache(true).one()
        if (schema?.schemaText) return schema.schemaText
    }
    
    // 2. Try DB by Name
    def nameKey = (name ?: id)?.toString()
    if (!nameKey) return null
    
    def schema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("schemaName", nameKey).useCache(true).one()
    if (schema?.schemaText) return schema.schemaText
    
    return null
}

// Resolve schema text using local closure
String schemaJsonString = loadSchemaText(jsonSchemaId, (filename ?: schemaFileName))

if (!schemaJsonString) {
    throw new IllegalArgumentException("Schema not found for provided ID or Name")
}

def rootSchema = new JsonSlurper().parseText(schemaJsonString)

def resolveRef = { Object root, String ref ->
    if (!ref || !ref.startsWith("#/")) return null
    def parts = ref.substring(2).split("/")
    def current = root
    for (String part : parts) {
        part = part.replace("~1", "/").replace("~0", "~")
        if (!(current instanceof Map)) return null
        current = current[part]
    }
    return current
}

def appendProperty = { String basePath, String prop ->
    basePath == "\$" ? "\$.${prop}" : "${basePath}.${prop}"
}

def matching = []
def visited = new HashSet<Integer>()

def collectPaths
collectPaths = { Object node, String currentPath ->
    if (node == null) return
    def actualNode = node
    if (node instanceof Map && node['$ref']) {
        def resolved = resolveRef(rootSchema, node['$ref']?.toString())
        if (resolved != null) actualNode = resolved
    }

    int nodeId = System.identityHashCode(actualNode)
    if (visited.contains(nodeId)) return
    visited.add(nodeId)

    if (actualNode instanceof Map) {
        def props = actualNode.properties instanceof Map ? actualNode.properties : null
        if (props) {
            props.each { propName, propSchema ->
                def propPath = appendProperty(currentPath, propName.toString())
                if (propName?.toString() == keyName) {
                    if (!matching.contains(propPath)) matching.add(propPath)
                }
                collectPaths(propSchema, propPath)
            }
        }

        def itemsNode = actualNode.items
        if (itemsNode != null) {
            def arrayPath = "${currentPath}[*]"
            collectPaths(itemsNode, arrayPath)
        }

        ['allOf', 'anyOf', 'oneOf'].each { altKey ->
            def altList = actualNode[altKey]
            if (altList instanceof List) {
                altList.each { altNode -> collectPaths(altNode, currentPath) }
            }
        }
    } else if (actualNode instanceof List) {
        actualNode.each { altNode -> collectPaths(altNode, currentPath) }
    }
}

collectPaths(rootSchema, "\$")

matchingPaths = matching
found = !matching.isEmpty()
if (matching.size() == 1) resolvedJsonPath = matching[0]

logger.info("Resolved JSONPath for key ${keyName} in schema ${schemaFileSafeName}: ${matching}")
