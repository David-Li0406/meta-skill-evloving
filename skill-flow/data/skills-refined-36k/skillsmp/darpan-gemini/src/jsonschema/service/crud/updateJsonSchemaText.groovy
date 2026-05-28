import org.slf4j.LoggerFactory
import com.fasterxml.jackson.databind.ObjectMapper

def logger = LoggerFactory.getLogger("darpan.jsonschema.UpdateText")

// jsonSchemaId is preferred, fallback to filename logic if needed (but service defines both)
// schemaName input from service parameter map might be null if called with jsonSchemaId only, but older calls use schemaName.

if (!jsonSchemaId && !filename) {
     throw new IllegalArgumentException("jsonSchemaId or filename is required")
}
if (!jsonText) {
    throw new IllegalArgumentException("jsonText is required")
}

// Validate JSON
def mapper = new ObjectMapper()
try {
    mapper.readTree(jsonText)
} catch (Exception e) {
    throw new IllegalArgumentException("Invalid JSON content: ${e.message}")
}

def existingSchema = null

if (jsonSchemaId) {
    existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("jsonSchemaId", jsonSchemaId)
        .one()
} else if (filename) {
    existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("schemaName", filename)
        .one()
}

if (!existingSchema) {
    throw new IllegalArgumentException("Schema not found for ID ${jsonSchemaId} or Name ${filename}")
}

existingSchema.schemaText = jsonText
existingSchema.lastUpdatedStamp = ec.user.nowTimestamp
existingSchema.update()

jsonSchemaId = existingSchema.jsonSchemaId

logger.info("Updated JSON schema '${existingSchema.schemaName}' (ID: ${jsonSchemaId}) from text editor")

