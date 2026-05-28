
import org.moqui.context.ExecutionContext

ExecutionContext ec = context.ec

ec.logger.info("saveRefinedSchema transition triggered.")
ec.logger.info("Raw Context Keys: " + context.keySet())
ec.logger.info("Web Parameters (Full Dump): " + ec.web.parameters)

def fields = []
Map params = ec.web.parameters

ec.logger.info("Checking for schemaName and jsonSchemaId in parameters...")
// Fix: Resolve schemaName/ID from first row if missing or if it's a list (form-list multi=true)
if (params.schemaName instanceof List) ec.context.put("schemaName", params.schemaName[0])
if (params.jsonSchemaId instanceof List) ec.context.put("jsonSchemaId", params.jsonSchemaId[0])

if (!context.schemaName && params.schemaName_0) ec.context.put("schemaName", params.schemaName_0)
if (!context.jsonSchemaId && params.jsonSchemaId_0) ec.context.put("jsonSchemaId", params.jsonSchemaId_0)

ec.logger.info("Resolved Context - schemaName: ${context.schemaName}, jsonSchemaId: ${context.jsonSchemaId}")

def maxIndex = 1000 // Safety limit
ec.logger.info("Starting loop to extract fields (limit ${maxIndex})...")
for (int i=0; i < maxIndex; i++) {
     String pKey = "fieldPath_" + i
     if (!params.containsKey(pKey)) {
        ec.logger.info("Loop break at index ${i}. Key ${pKey} not found.")
        break
     }
     
     def fieldData = [
         fieldPath: params[pKey],
         type: params["type_" + i],
         required: params["required_" + i]
     ]
     // ec.logger.info("Found field at index ${i}: ${fieldData}")
     fields.add(fieldData)
}

// Fallback: If no suffixed fields found, check for list/array parameters (fieldPath, type, required)
if (fields.isEmpty() && params.fieldPath) {
     ec.logger.info("No suffixed fields found, trying array parameters.")
     def fPaths = params.fieldPath instanceof List ? params.fieldPath : [params.fieldPath]
     def types = params.type instanceof List ? params.type : [params.type]
     def reqs = params.required instanceof List ? params.required : [params.required]
     
     ec.logger.info("Array parameter details - fieldPath size: ${fPaths.size()}")
     
     for (int i=0; i < fPaths.size(); i++) {
         fields.add([
             fieldPath: fPaths[i],
             type: (i < types.size() ? types[i] : 'string'),
             required: (i < reqs.size() ? reqs[i] : 'false')
         ])
     }
}

// Final Fallback: Use wizardResultList from session if available
// This protects against cases where form parameters aren't submitted but the session state is valid (e.g. after Add/Remove)
if (fields.isEmpty()) {
    def sessionList = ec.web.session.getAttribute("wizardResultList")
    if (sessionList) {
        ec.logger.warn("Form fields empty. Falling back to 'wizardResultList' from session (Size: ${sessionList.size()}). Edits to text fields may be lost if not submitted.")
        fields = sessionList
    }
}

ec.logger.info("Final Field List Size: " + fields.size())
if (fields.size() > 0) {
    ec.logger.info("First field sample: " + fields[0])
} else {
    ec.logger.warn("WARNING: Field list is empty! Service call will likely fail.")
}

ec.context.put("fieldList", fields)
