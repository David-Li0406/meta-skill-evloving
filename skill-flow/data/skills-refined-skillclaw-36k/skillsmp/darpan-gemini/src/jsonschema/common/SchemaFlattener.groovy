package jsonschema.common

import org.slf4j.LoggerFactory

/**
 * flattens a JSON Schema structure into a list of fields suitable for tabular UI display.
 */
class SchemaFlattener {
    private static final org.slf4j.Logger logger = LoggerFactory.getLogger(SchemaFlattener.class)
    private static final int MAX_DEPTH = 50

    /**
     * Flattens a JSON Schema Map (Jackson converted or native) into a list of Map representations.
     * @param schemaMap The root schema map.
     * @return List of Maps representing fields.
     */
    static List<Map<String, Object>> flatten(Map<String, Object> schemaMap) {
        List<Map<String, Object>> result = []
        Map<String, Object> definitions = (schemaMap.definitions instanceof Map) ? (Map) schemaMap.definitions : [:]
        
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

    private static void flattenRecursive(List<Map> result, String name, String path, Map node, int depth, boolean isRequired, Map definitions) {
        if (depth > MAX_DEPTH) {
            logger.warn("Max depth reached at ${path}.${name}")
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
                // Strategy: Find first option that has properties. 
                // Using 'allOf' to merge is complex; taking first valid structure is a safe best-effort for flattening.
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
                // Tuple validation: just process the first item definition as representative for the list
                def firstItem = node.items[0]
                if (firstItem instanceof Map) {
                     flattenRecursive(result, "[0]", displayPath, (Map)firstItem, depth + 1, false, definitions)
                }
            }
        }
    }
}
