import org.moqui.context.ExecutionContext

ExecutionContext ec = context.ec

if (!jsonSchemaId && !filename && !schemaFileName) {
    ec.message.addError("Schema ID or filename is required")
    return
}

def schema = null
if (jsonSchemaId) {
    schema = ec.entity.find("darpan.reconciliation.JsonSchema")
            .condition("jsonSchemaId", jsonSchemaId)
            .one()
} else {
    String fName = filename ?: schemaFileName
    if (fName) {
         schema = ec.entity.find("darpan.reconciliation.JsonSchema")
            .condition("schemaName", fName)
            .one()
    }
}

if (!schema) {
    // If we only had a file-based schema, we can't delete it from DB.
    // Legacy support: Try to delete file? 
    // No, deleteJsonSchema service implies DB deletion.
    ec.message.addError("Schema not found in database to delete")
    return
}

try {
    schema.delete()
    ec.message.addMessage("Deleted schema: ${schema.schemaName}")
} catch (Exception e) {
    ec.message.addError("Error deleting schema: ${e.message}")
}

