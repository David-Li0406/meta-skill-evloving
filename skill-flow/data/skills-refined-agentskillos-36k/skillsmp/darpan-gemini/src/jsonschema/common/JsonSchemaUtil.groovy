package jsonschema.common

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.JsonNode
import org.moqui.context.ExecutionContext
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import groovy.json.JsonSlurper

class JsonSchemaUtil {
    private static final Logger logger = LoggerFactory.getLogger(JsonSchemaUtil.class)
    private static final ObjectMapper mapper = new ObjectMapper()

    /**
     * Sanitizes a filename to prevent path traversal/injection.
     */
    static String cleanFileName(String rawName) {
        if (!rawName) return null
        def name = rawName.toString().trim()
        if (!name) return null
        if (name.contains("..") || name.contains("/") || name.contains("\\")) {
            throw new IllegalArgumentException("Invalid schema file name: ${name}")
        }
        return name
    }

    /**
     * Loads schema text from Database (primary).
     * @param ec ExecutionContext
     * @param id Optional jsonSchemaId
     * @param name Optional schemaName (or filename)
     * @return Schema JSON String or null if not found
     */
    static String loadSchemaText(ExecutionContext ec, Object id, Object name) {
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
        
        // Removed Legacy File System Fallback
        return null
    }

    /**
     * Resolves a location string to an absolute file path.
     */
    static String resolveFilePath(ExecutionContext ec, String location) {
        if (!location) return null
        def rr = ec.resource.getLocationReference(location)
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

    static JsonNode loadSchemaNode(ExecutionContext ec, Object id, Object name) {
        String text = loadSchemaText(ec, id, name)
        if (!text) return null
        return mapper.readTree(text)
    }

    /**
     * Generates a unique schema name by appending (1), (2), etc. if the name already exists.
     * @param ec ExecutionContext
     * @param baseName The desired name
     * @param overwrite If true, returns baseName as is (assuming caller handles overwrite)
     * @return Unique schema name
     */
    static String generateUniqueSchemaName(ExecutionContext ec, String baseName, boolean overwrite) {
        if (!baseName) return null
        if (overwrite) return baseName

        String nameToSave = baseName
        def existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
            .condition("schemaName", nameToSave)
            .one()
        
        if (existingSchema) {
            String nameRoot = baseName
            int suffix = 1
            while (existingSchema != null) {
                nameToSave = "${nameRoot} (${suffix})"
                existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
                    .condition("schemaName", nameToSave)
                    .one()
                suffix++
            }
        }
        return nameToSave
    }
}
