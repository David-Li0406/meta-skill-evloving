import groovy.json.JsonOutput
import jsonschema.common.JsonSchemaUtil
import org.slf4j.LoggerFactory
import org.moqui.resource.ResourceReference

def logger = LoggerFactory.getLogger("darpan.jsonschema.SaveSchema")

def normalizeBool = { val, boolean defaultValue ->
    if (val == null) return defaultValue
    return val.toString().equalsIgnoreCase("true")
}

// Use schemaName input or fallback to file name (without enforcing strict filename chars)
String nameToSave = schemaName ? schemaName.trim() : schemaFile.getName()

String schemaJson = null
if (schemaFile != null && schemaFile.getSize() > 0) {
    schemaJson = schemaFile.getString("UTF-8")
}

if (!schemaJson) {
   ec.message.addError("Uploaded schema file is empty")
   return
}

// --------------------------------------------------------------------------------
// Unique naming logic centralized in JsonSchemaUtil
// --------------------------------------------------------------------------------
String finalName = JsonSchemaUtil.generateUniqueSchemaName(ec, nameToSave, doOverwrite)

// Re-fetch to confirm if we are updating or creating
existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
    .condition("schemaName", finalName)
    .one()
    
// Update nameToSave to the resolved unique name
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
    newSchema.statusId = "Active" // Default status
    
    // Create will handle ID generation
    newSchema.setSequencedIdPrimary()
    newSchema.create()
    
    jsonSchemaId = newSchema.jsonSchemaId
}

filename = nameToSave // Maintain output param name for now, but value is schemaName
schemaName = nameToSave // Return corrected name

logger.info("Saved JSON schema '${schemaName}' to DB with ID ${jsonSchemaId}")
