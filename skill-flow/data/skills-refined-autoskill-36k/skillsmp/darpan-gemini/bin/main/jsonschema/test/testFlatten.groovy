import org.moqui.context.ExecutionContext
import org.moqui.service.ServiceCallSync

ExecutionContext ec = context.ec
String filename = "omsData.schema.json" // Using an existing file

try {
    Map result = ec.service.sync().name("JsonSchemaServices.flatten#JsonSchema")
        .parameter("schemaFileName", filename)
        .call()
    
    println "Service Result keys: ${result.keys}"
    if (result.fieldList) {
        println "Field List size: ${result.fieldList.size()}"
        println "First 5 fields: ${result.fieldList.take(5)}"
    } else {
        println "Field List is null or empty"
    }
} catch (Exception e) {
    println "Error calling service: ${e.message}"
    e.printStackTrace()
}
