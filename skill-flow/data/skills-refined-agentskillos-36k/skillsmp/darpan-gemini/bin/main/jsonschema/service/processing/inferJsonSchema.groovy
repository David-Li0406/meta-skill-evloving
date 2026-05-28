/*
 * Service to infer a draft JSON Schema from a JSON file and return it as a flattened list of fields
 * for the UI Wizard "Refine" step.
 */

import groovy.json.JsonSlurper
import groovy.json.JsonOutput
import org.slf4j.LoggerFactory
import com.saasquatch.jsonschemainferrer.JsonSchemaInferrer
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.core.JsonFactory
import com.fasterxml.jackson.core.JsonParser
import com.fasterxml.jackson.core.JsonToken
import com.fasterxml.jackson.databind.JsonNode
import com.fasterxml.jackson.databind.node.ArrayNode
import jsonschema.common.SchemaFlattener

def logger = LoggerFactory.getLogger("darpan.jsonschema.Infer")

// -----------------------------------------------------
// 1. HELPER FUNCTIONS
// -----------------------------------------------------
// Flattening logic moved to SchemaFlattener.groovy
final int SAMPLE_SIZE_LIMIT = 1000

// -----------------------------------------------------
// 3. MAIN EXECUTION
// -----------------------------------------------------

if (!jsonFile) {
    ec.message.addError("No JSON file uploaded")
    return
}

try {
    def mapper = new ObjectMapper()
    def inferrer = JsonSchemaInferrer.newBuilder()
                        .setSpecVersion(com.saasquatch.jsonschemainferrer.SpecVersion.DRAFT_07)
                        .build()
    
    // Using streaming parser to consume only a sample of the data
    JsonNode sampleJson = null
    
    jsonFile.getInputStream().withStream { stream ->
        JsonFactory factory = mapper.getFactory()
        JsonParser parser = factory.createParser(stream)
        
        try {
            JsonToken token = parser.nextToken()
            if (token == null) {
                throw new IllegalArgumentException("Empty JSON file")
            }
            
            if (token == JsonToken.START_ARRAY) {
                // If it's an array, read first SAMPLE_SIZE_LIMIT items
                logger.info("JSON root is Array. Sampling up to ${SAMPLE_SIZE_LIMIT} items...")
                ArrayNode arrayNode = mapper.createArrayNode()
                int count = 0
                while (parser.nextToken() != JsonToken.END_ARRAY && count < SAMPLE_SIZE_LIMIT) {
                    JsonNode node = mapper.readTree(parser)
                    arrayNode.add(node)
                    count++
                }
                sampleJson = arrayNode
                logger.info("Sampled ${count} items from array.")
            } else {
                logger.info("JSON root is Object. Reading full object (single record)...")
                sampleJson = mapper.readTree(parser)
            }
        } finally {
            parser.close()
        }
    }
    
    if (sampleJson == null) {
        ec.message.addError("Could not read valid JSON data from file")
        return
    }

    def jsonSchemaNode = inferrer.inferForSample(sampleJson)
    
    // Convert Jackson JsonNode back to Map for easy Groovy handling/flattening
    Map schemaMap = mapper.convertValue(jsonSchemaNode, Map.class)

    logger.info("Generated schema map using library. Flattening...")
    
    // 2. Flatten for UI using Helper
    List<Map> flattenedFields = SchemaFlattener.flatten(schemaMap)
    
    // Schema String for editor
    String schemaString = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(jsonSchemaNode)

    logger.info("Flattened fields count: ${flattenedFields.size()}")
    
    // Return to context
    resultList = flattenedFields
    jsonSchemaString = schemaString
    
} catch (Exception e) {
    ec.message.addError("Error inferring schema: ${e.message}")
    logger.error("Error inferring schema", e)
}
