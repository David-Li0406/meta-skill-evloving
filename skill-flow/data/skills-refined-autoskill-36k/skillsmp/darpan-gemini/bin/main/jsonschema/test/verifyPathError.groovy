
import java.nio.file.Paths
import groovy.json.JsonGenerator

try {
    println "Creating a Path object..."
    def p = Paths.get("tmp", "foo")
    println "Path created: ${p} (Class: ${p.getClass().getName()})"
    println "Is Iterable? ${p instanceof Iterable}"
    
    println "Attempting serialization with Groovy JsonGenerator..."
    def generator = new groovy.json.JsonGenerator.Options().build()
    
    // Wrap in map simulates context
    def ctx = [somePath: p]
    
    String json = generator.toJson(ctx)
    println "Serialization successful (unexpected): ${json}"
    
} catch (StackOverflowError e) {
    println "SUCCESS: Caught expected StackOverflowError!"
    e.printStackTrace(System.out)
} catch (Exception e) {
    println "CAUGHT OTHER EXCEPTION: ${e}"
    e.printStackTrace(System.out)
}
