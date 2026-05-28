package jsonschema.common

import com.fasterxml.jackson.core.JsonFactory
import com.fasterxml.jackson.core.JsonParser
import com.fasterxml.jackson.core.JsonToken
import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.ObjectMapper
import com.networknt.schema.JsonSchema
import com.networknt.schema.JsonSchemaFactory
import com.networknt.schema.SpecVersion
import com.networknt.schema.ValidationMessage
import org.slf4j.Logger
import org.slf4j.LoggerFactory

class SchemaValidator {
    private static final Logger logger = LoggerFactory.getLogger(SchemaValidator.class)
    private static final ObjectMapper mapper = new ObjectMapper()
    
    /**
     * Validates a JSON input stream against a loaded JsonSchema.
     * Supports streaming for Arrays to handle large files.
     */
    static Map validateStream(InputStream inputStream, JsonNode schemaNode, long maxErrors) {
        JsonSchemaFactory factory = JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V7)
        JsonSchema rootSchema = factory.getSchema(schemaNode)
        
        List<String> errors = []
        boolean isValid = true
        
        try {
            JsonFactory jsonFactory = mapper.getFactory()
            JsonParser parser = jsonFactory.createParser(inputStream)
            
            JsonToken token = parser.nextToken()
            if (token == null) {
                return [valid: false, errors: ["Empty JSON content"]]
            }
            
            if (token == JsonToken.START_ARRAY && isSchemaArray(schemaNode)) {
                logger.info("Validating array stream...")
                // Extract item schema
                // Note: This only handles simple "items" definition. 
                // Tuple validation (array of schemas) is not supported in this simplified stream.
                JsonNode itemsNode = schemaNode.get("items")
                JsonSchema itemSchema = null
                
                if (itemsNode != null && itemsNode.isObject()) {
                    itemSchema = factory.getSchema(itemsNode)
                } else {
                    logger.warn("Schema is array but 'items' is complex or missing. Falling back to validating items against root (loose validation).")
                    // In some cases (like ANY), we might just validate against root? No, that fails.
                    // If no item schema, maybe we skip validation? 
                    // Better to fallback to root schema if "items" is not present, effectively assuming the user meant to validate the objects?
                    // Or if items is missing, it accepts anything.
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
    
    private static boolean isSchemaArray(JsonNode schemaNode) {
        JsonNode typeNode = schemaNode.get("type")
        if (typeNode != null) {
            if (typeNode.isTextual() && typeNode.asText() == "array") return true
            if (typeNode.isArray()) {
                 for (JsonNode t : typeNode) {
                     if (t.asText() == "array") return true
                 }
            }
        }
        // Implicit array if "items" keyword exists
        return schemaNode.has("items")
    }
}
