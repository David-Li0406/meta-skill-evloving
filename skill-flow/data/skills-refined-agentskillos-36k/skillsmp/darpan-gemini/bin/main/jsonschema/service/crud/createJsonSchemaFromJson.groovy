import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.ObjectMapper

import org.slf4j.LoggerFactory
// --------------------------------------------------------------------------------
// Unique naming logic inlined
// --------------------------------------------------------------------------------
def generateUniqueSchemaName = { String baseName, boolean overwrite ->
    if (!baseName) return null
    if (overwrite) return baseName

    String name = baseName
    def existing = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("schemaName", name)
        .one()
    
    if (existing) {
        String nameRoot = baseName
        int suffix = 1
        while (existing != null) {
            name = "${nameRoot} (${suffix})"
            existing = ec.entity.find("darpan.reconciliation.JsonSchema")
                .condition("schemaName", name)
                .one()
            suffix++
        }
    }
    return name
}



def logger = LoggerFactory.getLogger("darpan.jsonschema.CreateFromJson")

def normalizeBool = { Object val, boolean defaultValue ->
    if (val == null) return defaultValue
    return val.toString().trim().equalsIgnoreCase("true")
}

def normalizeString = { Object val ->
    def text = val?.toString()?.trim()
    return text ?: null
}

def normalizeBaseName = { Object rawName ->
    def name = normalizeString(rawName)
    if (!name) return null
    name = name.replaceAll("[^A-Za-z0-9._-]", "_")
    name = name.replaceAll("(?i)\\.schema\\.json\$", "")
    name = name.replaceAll("(?i)\\.json\$", "")
    name = name.replaceAll("^\\.+", "")
    return name ?: null
}

def schemaTypeList = { Map schema ->
    if (!(schema instanceof Map)) return []
    def typeVal = schema.type
    def types = []
    if (typeVal instanceof Collection) {
        types = typeVal.collect { it?.toString() }.findAll { it }
    } else if (typeVal != null) {
        types = [typeVal.toString()]
    }
    if (!types) {
        if (schema.properties instanceof Map) types = ["object"]
        else if (schema.items != null) types = ["array"]
    }
    return types
}

def mergeTypeLists = { List types ->
    def normalized = types.collect { it?.toString() }.findAll { it }
    def ordered = new LinkedHashSet(normalized)
    if (ordered.contains("number") && ordered.contains("integer")) {
        ordered.remove("integer")
    }
    return ordered as List
}

def primitiveTypes = ["string", "integer", "number", "boolean", "null"]
def isObjectOnly = { Map schema ->
    def types = schemaTypeList(schema)
    if (types) {
        def allowed = ["object", "null"]
        return types.every { allowed.contains(it) }
    }
    return schema?.properties instanceof Map
}
def isArrayOnly = { Map schema ->
    def types = schemaTypeList(schema)
    if (types) {
        def allowed = ["array", "null"]
        return types.every { allowed.contains(it) }
    }
    return schema?.items != null
}
def isPrimitiveOnly = { Map schema ->
    def types = schemaTypeList(schema)
    if (!types) return false
    return types.every { primitiveTypes.contains(it) }
}

def mergeSchemaList
mergeSchemaList = { List schemas ->
    def flattened = []
    schemas.findAll { it != null }.each { schema ->
        if (schema instanceof Map && schema.anyOf instanceof List) {
            flattened.addAll(schema.anyOf)
        } else {
            flattened.add(schema)
        }
    }
    if (!flattened) return null

    if (flattened.every { it instanceof Map && isObjectOnly(it) }) {
        Map mergedProps = [:]
        flattened.each { schema ->
            def props = schema.properties instanceof Map ? schema.properties : [:]
            props.each { k, v ->
                if (k == null || v == null) return
                def key = k.toString()
                def merged = mergeSchemaList([mergedProps[key], v].findAll { it != null })
                mergedProps[key] = merged ?: v
            }
        }
        def mergedTypes = mergeTypeLists(flattened.collectMany { schemaTypeList(it) } + ["object"])
        def typeVal = mergedTypes.size() == 1 ? mergedTypes[0] : mergedTypes
        return [type: typeVal, properties: mergedProps]
    }

    if (flattened.every { it instanceof Map && isArrayOnly(it) }) {
        def itemSchemas = flattened.collect { it.items }.findAll { it != null }
        def mergedItems = mergeSchemaList(itemSchemas)
        def mergedTypes = mergeTypeLists(flattened.collectMany { schemaTypeList(it) } + ["array"])
        def typeVal = mergedTypes.size() == 1 ? mergedTypes[0] : mergedTypes
        return [type: typeVal, items: mergedItems ?: [:]]
    }

    if (flattened.every { it instanceof Map && isPrimitiveOnly(it) }) {
        def mergedTypes = mergeTypeLists(flattened.collectMany { schemaTypeList(it) })
        def typeVal = mergedTypes.size() == 1 ? mergedTypes[0] : mergedTypes
        return [type: typeVal]
    }

    def uniqueSchemas = flattened.unique()
    if (uniqueSchemas.size() == 1) return uniqueSchemas[0]
    return [anyOf: uniqueSchemas]
}

// -----------------------------------------------------
// Helper to recursively build schema
// -----------------------------------------------------
final int MAX_DEPTH = 50

def buildSchema
buildSchema = { JsonNode node, boolean strictMode, int depth = 0 ->
    if (depth > MAX_DEPTH) {
        // Return a generic fallback or null when max depth is reached to prevent stack overflow
        return [type: "object", description: "Max depth of ${MAX_DEPTH} reached, schema truncated"] 
        // Or strictly: return [type: "string", description: "Depth limit reached"]
    }

    if (node == null || node.isNull()) return [type: "null"]
    if (node.isObject()) {
        Map properties = [:]
        def fields = node.fields()
        while (fields.hasNext()) {
            def entry = fields.next()
            properties[entry.getKey()] = buildSchema(entry.getValue(), strictMode, depth + 1)
        }
        Map schema = [type: "object", properties: properties]
        if (strictMode && properties) {
            schema.required = properties.keySet().toList()
            schema.additionalProperties = false
        }
        return schema
    }
    if (node.isArray()) {
        List itemSchemas = []
        def elements = node.elements()
        while (elements.hasNext()) {
            itemSchemas << buildSchema(elements.next(), strictMode, depth + 1)
        }
        itemSchemas = itemSchemas.findAll { it != null }
        if (itemSchemas.isEmpty()) {
            return [type: "array", items: [:]]
        }
        if (!strictMode) {
            def mergedItemsSchema = mergeSchemaList(itemSchemas)
            if (mergedItemsSchema != null) {
                return [type: "array", items: mergedItemsSchema]
            }
        }
        List uniqueSchemas = itemSchemas.unique()
        Map itemsSchema = uniqueSchemas.size() == 1 ? uniqueSchemas[0] : [anyOf: uniqueSchemas]
        return [type: "array", items: itemsSchema]
    }
    if (node.isBoolean()) return [type: "boolean"]
    if (node.isIntegralNumber()) return [type: "integer"]
    if (node.isNumber()) return [type: "number"]
    return [type: "string"]
}

if (!jsonFile) {
    logger.error("createJsonSchemaFromJson: jsonFile is missing!")
    throw new IllegalArgumentException("jsonFile is required")
}
logger.info("createJsonSchemaFromJson called. File: ${jsonFile.getName()}, Size: ${jsonFile.getSize()}")

boolean overwriteMode = normalizeBool(overwrite, false)
boolean strictMode = normalizeBool(strict, false)

def mapper = new ObjectMapper()
mapper.configure(DeserializationFeature.USE_BIG_DECIMAL_FOR_FLOATS, true)
def jsonData = jsonFile.getInputStream().withCloseable { stream ->
    mapper.readTree(stream)
}
if (jsonData == null) {
    throw new IllegalArgumentException("jsonFile is empty")
}

Map schemaMap = buildSchema(jsonData, strictMode, 0)
schemaMap["\$schema"] = "http://json-schema.org/draft-07/schema#"
def schemaTitle = normalizeString(schemaName)
// Serialize map to JSON string
import groovy.json.JsonOutput
String schemaJson = JsonOutput.toJson(schemaMap)

if (schemaTitle) schemaMap.title = schemaTitle

// Use provided schemaName directly, fallback to json filename
String nameToSave = schemaTitle ?: jsonFile.getName()

// --------------------------------------------------------------------------------
// Unique naming logic centralized in JsonSchemaUtil
// --------------------------------------------------------------------------------
String finalName = generateUniqueSchemaName(nameToSave, overwriteMode)

// Re-fetch to confirm if we are updating or creating
existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
    .condition("schemaName", finalName)
    .one()
    
nameToSave = finalName

if (existingSchema) {
    // Update existing
    existingSchema.schemaText = schemaJson
    if (description) existingSchema.description = description
    existingSchema.lastUpdatedStamp = ec.user.nowTimestamp
    existingSchema.update()
    
    jsonSchemaId = existingSchema.jsonSchemaId
} else {
    // Create new
    def newSchema = ec.entity.makeValue("darpan.reconciliation.JsonSchema")
    newSchema.schemaName = nameToSave
    newSchema.schemaText = schemaJson
    newSchema.description = description
    newSchema.statusId = "Active"
    
    // Create will handle ID generation
    newSchema.setSequencedIdPrimary()
    newSchema.create()
    
    jsonSchemaId = newSchema.jsonSchemaId
}

filename = nameToSave // Set output params
schemaName = nameToSave


logger.info("Saved generated JSON schema ${filename} to DB with ID ${jsonSchemaId}")

