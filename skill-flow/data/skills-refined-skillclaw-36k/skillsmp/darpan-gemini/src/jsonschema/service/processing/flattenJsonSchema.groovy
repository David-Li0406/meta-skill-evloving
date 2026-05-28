import org.moqui.context.ExecutionContext
import org.moqui.resource.ResourceReference
import groovy.json.JsonSlurper

ExecutionContext ec = context.ec
ec.logger.info("flattenJsonSchema called with: ${schemaFileName}")

fieldList = []
jsonSchemaString = ""

// 1. Resolve and read schema content
if (schemaFile != null && schemaFile.getSize() > 0) {
    jsonSchemaString = schemaFile.getString("UTF-8")
} else if (jsonSchemaId) {
    def schema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("jsonSchemaId", jsonSchemaId)
        .one()
    if (!schema) {
         ec.message.addError("Schema not found for ID: ${jsonSchemaId}")
         return
    }
    jsonSchemaString = schema.schemaText
} else if (filename || schemaFileName || schemaName) {
    String fName = schemaName ?: (filename ?: schemaFileName)
    def schema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("schemaName", fName)
        .one()
    if (!schema) {
         ec.message.addError("Schema not found for Name: ${fName}")
         return
    }
    jsonSchemaString = schema.schemaText
    ec.logger.info("Found schema by Name '${fName}': valid? ${schema != null}, text length: ${jsonSchemaString?.length()}")
} else {
    ec.logger.warn("No jsonSchemaId, schemaName, filename, or schemaFile provided")
    return
}

if (!jsonSchemaString || jsonSchemaString.trim().isEmpty()) {
    ec.logger.error("jsonSchemaString is empty or null for inputs: ID=${jsonSchemaId}, Name=${schemaName}, File=${filename}")
    ec.message.addError("Schema content is empty")
    return
}
// --------------------------------------------------------------------------------
// Schema Flattener Logic Inlined
// --------------------------------------------------------------------------------
def flattenRecursive
flattenRecursive = { List result, String name, String path, Map node, int depth, boolean isRequired, Map definitions ->
    int MAX_DEPTH = 50
    if (depth > MAX_DEPTH) {
        ec.logger.warn("Max depth reached at ${path}.${name}")
        return
    }

    // Handle $ref
    if (node.'$ref') {
        String ref = node.'$ref'
        if (ref.startsWith("#/definitions/")) {
            String defName = ref.substring("#/definitions/".length())
            Map defNode = definitions[defName] as Map
            if (defNode) {
                flattenRecursive(result, name, path, defNode, depth, isRequired, definitions)
                return
            }
        }
    }

    String displayPath = path ? "${path}.${name}" : name
    if (name == "#ROOT") displayPath = ""

    if (name != "#ROOT") {
        String type = node.type
        if (type == null && node.anyOf) {
            type = "any" 
        }
        
        result.add([
            fieldPath: displayPath,
            fieldName: name,
            type: type ?: "string",
            required: isRequired,
            depth: depth,
            indentLevel: depth
        ])
    }

    // Logic to find properties in various structures
    Map propertiesToParse = null
    if (node.properties instanceof Map) {
        propertiesToParse = node.properties
    } else {
        // Check Combinators (anyOf, oneOf, allOf)
        def combinator = ['anyOf', 'oneOf', 'allOf'].find { node[it] instanceof List }
        if (combinator) {
            List options = node[combinator]
            def validOption = options.find { it instanceof Map && it.properties instanceof Map }
            if (validOption) {
                propertiesToParse = validOption.properties
            }
        }
    }

    if (propertiesToParse) {
        propertiesToParse.each { k, v ->
            boolean childRequired = node.required instanceof List && node.required.contains(k)
            flattenRecursive(result, k as String, displayPath, (Map)v, depth + 1, childRequired, definitions)
        }
    } 
    
    // Items handling
    if (node.items) {
        if (node.items instanceof Map) {
            flattenRecursive(result, "[0]", displayPath, (Map)node.items, depth + 1, false, definitions)
        } else if (node.items instanceof List && !node.items.isEmpty()) {
            def firstItem = node.items[0]
            if (firstItem instanceof Map) {
                    flattenRecursive(result, "[0]", displayPath, (Map)firstItem, depth + 1, false, definitions)
            }
        }
    }
}

def flattenSchema = { Map schemaMap ->
    List result = []
    Map definitions = (schemaMap.definitions instanceof Map) ? (Map) schemaMap.definitions : [:]
    
    flattenRecursive(result, "#ROOT", "", schemaMap, 0, true, definitions)
    
    // Post-process to ensure primitive types for serialization safety if needed
    result.each { row ->
        row.each { k, v ->
            if (v != null && !(v instanceof String || v instanceof Number || v instanceof Boolean)) {
                row.put(k, v.toString())
            }
        }
    }
    return result
}

try {
    def schemaMap = new JsonSlurper().parseText(jsonSchemaString)
    ec.logger.info("Schema parsed, keys: ${schemaMap.keySet()}")
    
    // 2. Flatten logic using local closure
    fieldList = flattenSchema(schemaMap)

    ec.logger.info("Flattened fieldList size: ${fieldList.size()}")

} catch (Exception e) {
    ec.message.addError("Error parsing schema: ${e.message}")
    ec.logger.error("Error parsing schema", e)
}
