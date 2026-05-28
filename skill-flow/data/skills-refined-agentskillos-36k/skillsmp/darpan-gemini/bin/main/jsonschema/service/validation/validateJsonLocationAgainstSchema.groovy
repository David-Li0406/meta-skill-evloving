import com.fasterxml.jackson.core.JsonFactory
import com.fasterxml.jackson.core.JsonParser
import com.fasterxml.jackson.core.JsonToken
import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.ObjectMapper
import com.networknt.schema.JsonSchema
import com.networknt.schema.JsonSchemaFactory
import com.networknt.schema.SpecVersion
import com.networknt.schema.ValidationMessage
import org.slf4j.LoggerFactory
import org.moqui.context.ExecutionContext

def logger = LoggerFactory.getLogger("darpan.jsonschema.ValidateLocation")

if (!jsonLocation) throw new IllegalArgumentException("jsonLocation is required")
if (!schemaFileName) throw new IllegalArgumentException("schemaFileName is required")

// --------------------------------------------------------------------------------
// Helper: Resolve File Path (Inlined from JsonSchemaUtil)
// --------------------------------------------------------------------------------
def resolveFilePath = { ExecutionContext context, String location ->
    if (!location) return null
    def rr = context.resource.getLocationReference(location)
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

// --------------------------------------------------------------------------------
// Helper: Validation Logic (Inlined from SchemaValidator)
// --------------------------------------------------------------------------------
ObjectMapper mapper = new ObjectMapper()

def isSchemaArray = { JsonNode sNode ->
    JsonNode typeNode = sNode.get("type")
    if (typeNode != null) {
        if (typeNode.isTextual() && typeNode.asText() == "array") return true
        if (typeNode.isArray()) {
                for (JsonNode t : typeNode) {
                    if (t.asText() == "array") return true
                }
        }
    }
    // Implicit array if "items" keyword exists
    return sNode.has("items")
}

def validateStream = { InputStream inputStream, JsonNode sNode, long maxErrors ->
    JsonSchemaFactory factory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V7)
    JsonSchema rootSchema = factory.getSchema(sNode)
    
    List<String> errors = []
    boolean isValid = true
    
    try {
        JsonFactory jsonFactory = mapper.getFactory()
        JsonParser parser = jsonFactory.createParser(inputStream)
        
        JsonToken token = parser.nextToken()
        if (token == null) {
            return [valid: false, errors: ["Empty JSON content"]]
        }
        
        if (token == JsonToken.START_ARRAY && isSchemaArray(sNode)) {
            logger.info("Validating array stream...")
            JsonNode itemsNode = sNode.get("items")
            JsonSchema itemSchema = null
            
            if (itemsNode != null && itemsNode.isObject()) {
                itemSchema = factory.getSchema(itemsNode)
            } else {
                logger.warn("Schema is array but 'items' is complex or missing.")
            }
            
            int index = 0
            while (parser.nextToken() != JsonToken.END_ARRAY && errors.size() < maxErrors) {
                JsonNode itemNode = mapper.readTree(parser)
                if (itemSchema) {
                    Set<ValidationMessage> messages = itemSchema.validate(itemNode)
                    messages.each { msg ->
                        errors.add("Item ${index}: ${msg.getMessage()}")
                    }
                    if (!messages.isEmpty()) isValid = false
                }
                index++
            }
        } else {
            // Object or non-array root
            logger.info("Validating full object...")
            JsonNode node = mapper.readTree(parser)
            Set<ValidationMessage> messages = rootSchema.validate(node)
            messages.each { msg ->
                errors.add(msg.getMessage())
            }
            if (!messages.isEmpty()) isValid = false
        }
        
        parser.close()
        
    } catch (Exception e) {
        logger.error("Validation error", e)
        errors.add("System Error: ${e.message}")
        isValid = false
    }
    
    return [valid: isValid, errors: errors, count: errors.size()]
}

// --------------------------------------------------------------------------------
// Main Execution Flow
// --------------------------------------------------------------------------------

// 1. Resolve JSON File
String jsonPath = resolveFilePath(ec, jsonLocation)
File jsonFile = new File(jsonPath)
if (!jsonFile.exists()) {
    throw new IllegalArgumentException("JSON file not found: ${jsonPath}")
}

// 2. Load Schema Node
String schemaText = loadSchemaText(null, schemaFileName)
if (!schemaText) {
     throw new IllegalArgumentException("Schema not found: ${schemaFileName}")
}
JsonNode schemaNode = mapper.readTree(schemaText)

// 3. Validate
logger.info("Starting validation for ${jsonPath} against ${schemaFileName}")
Map result = [:]

jsonFile.withInputStream { stream ->
    result = validateStream(stream, schemaNode, 100)
}

// 4. Return results
valid = result.valid
errorCount = result.count
errorMessages = result.errors

logger.info("Validation complete: valid=${valid}, errors=${errorCount}")

