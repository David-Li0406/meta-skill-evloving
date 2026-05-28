import org.moqui.context.ExecutionContext
import org.moqui.entity.EntityValue
import org.slf4j.LoggerFactory


ExecutionContext ec = context.ec
def logger = LoggerFactory.getLogger("VerifyJsonSchemaMigration")

logger.info("Starting JSON Schema Migration Verification...")

String testSchemaName = "TestSchema_${System.currentTimeMillis()}"
// String testFileName = "${testSchemaName}.schema.json" // Removed
String testDescription = "Automated verification schema"

// ---------------------------------------------------------
// 1. Test Generate/Create (Create JSON Schema from JSON)
// ---------------------------------------------------------
logger.info("1. Testing Create Schema from JSON...")

def sampleJson = '{"id": 1, "name": "Test Item"}'
def jsonFileStub = new org.apache.commons.fileupload.disk.DiskFileItem(
    "jsonFile", "application/json", false, "sample.json", 1024, new File(System.getProperty("java.io.tmpdir"))
)
jsonFileStub.getOutputStream().withCloseable { it.write(sampleJson.getBytes("UTF-8")) }

Map createResult = ec.service.sync().name("JsonSchemaServices.create#JsonSchemaFromJson")
    .parameters([jsonFile: jsonFileStub, schemaName: testSchemaName, description: testDescription, overwrite: true])
    .call()

String jsonSchemaId = createResult.jsonSchemaId
String schemaNameResult = createResult.schemaName

if (!jsonSchemaId) {
    logger.error("FAILURE: Create service did not return jsonSchemaId")
    return
}
logger.info("   -> Created schema ID: ${jsonSchemaId}, SchemaName: ${schemaNameResult}")

// Verify DB
EntityValue schemaEntity = ec.entity.find("darpan.reconciliation.JsonSchema")
    .condition("jsonSchemaId", jsonSchemaId)
    .one()

if (!schemaEntity) {
    logger.error("FAILURE: Entity not found in DB for ID ${jsonSchemaId}")
    return
}
if (schemaEntity.schemaName != schemaNameResult) {
    logger.error("FAILURE: Schema Name mismatch. Expected ${schemaNameResult}, got ${schemaEntity.schemaName}")
    return
}
if (schemaEntity.schemaName != testSchemaName) {
    logger.warn("WARNING: Schema Name modified? Expected ${testSchemaName}, got ${schemaEntity.schemaName}")
}
logger.info("   -> DB Verification PASSED")


// ---------------------------------------------------------
// 2. Test Flatten (Read Schema)
// ---------------------------------------------------------
logger.info("2. Testing Flatten Schema (Read)...")
Map flattenResult = ec.service.sync().name("JsonSchemaServices.flatten#JsonSchema")
    .parameters([jsonSchemaId: jsonSchemaId])
    .call()

List fields = flattenResult.fieldList
if (!fields || fields.isEmpty()) {
    logger.error("FAILURE: Flatten returned empty fields")
    return
}
logger.info("   -> Flatten returned ${fields.size()} fields. PASSED")


// ---------------------------------------------------------
// 3. Test Update Text (Editor Save)
// ---------------------------------------------------------
logger.info("3. Testing Update Schema Text...")
String newSchemaText = '''{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "updatedField": { "type": "string" }
  }
}'''

ec.service.sync().name("JsonSchemaServices.update#JsonSchemaText")
    .parameters([jsonSchemaId: jsonSchemaId, jsonText: newSchemaText])
    .call()

// Verify Update
schemaEntity = ec.entity.find("darpan.reconciliation.JsonSchema")
    .condition("jsonSchemaId", jsonSchemaId)
    .one()

if (!schemaEntity.schemaText.contains("updatedField")) {
    logger.error("FAILURE: Schema text not updated in DB")
    return
}
logger.info("   -> Update Text PASSED")


// ---------------------------------------------------------
// 4. Test Validation
// ---------------------------------------------------------
logger.info("4. Testing Validation...")
def validJson = '{"updatedField": "value"}'
def validJsonFileStub = new org.apache.commons.fileupload.disk.DiskFileItem(
    "jsonFile", "application/json", false, "valid.json", 1024, new File(System.getProperty("java.io.tmpdir"))
)
validJsonFileStub.getOutputStream().withCloseable { it.write(validJson.getBytes("UTF-8")) }

Map validateResult = ec.service.sync().name("JsonSchemaServices.validate#JsonFileAgainstSchema")
    .parameters([jsonSchemaId: jsonSchemaId, jsonFile: validJsonFileStub])
    .call()

if (!validateResult.valid) {
    logger.error("FAILURE: Validation failed with errors: ${validateResult.errorMessages}")
    return
}
logger.info("   -> Validation PASSED")


// ---------------------------------------------------------
// 5. Test Delete
// ---------------------------------------------------------
logger.info("5. Testing Delete...")
ec.service.sync().name("JsonSchemaServices.delete#JsonSchema")
    .parameters([jsonSchemaId: jsonSchemaId])
    .call()

schemaEntity = ec.entity.find("darpan.reconciliation.JsonSchema")
    .condition("jsonSchemaId", jsonSchemaId)
    .one()

if (schemaEntity) {
    logger.error("FAILURE: Entity still exists after delete")
    return
}
logger.info("   -> Delete PASSED")

logger.info("--------------------------------------------------")
logger.info("ALL VERIFICATION CHECKS PASSED")
logger.info("--------------------------------------------------")
