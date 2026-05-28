/*
 * Service to reconstruct a JSON Schema from a flattened list of fields (from Wizard UI) 
 * and save it to a file.
 */

import groovy.json.JsonOutput
import org.slf4j.LoggerFactory

def logger = LoggerFactory.getLogger("darpan.jsonschema.SaveRefined")

if (!schemaName) {
    ec.message.addError("Schema Name is required")
    return
}
if (!fieldList) {
    ec.message.addError("No fields provided")
    return
}

// fieldList is List<Map> from the form-list. 
// Keys: fieldPath, type, required (boolean or "true" string)

// -----------------------------------------------------
// 1. RECONSTRUCT LOGIC
// -----------------------------------------------------

Map rootSchema = [type: 'object', properties: [:], required: []]

// Helper to find or create node at path
def getNode
getNode = { Map current, List<String> pathParts ->
    if (pathParts.isEmpty()) return current
    
    String key = pathParts[0]
    
    // Handle Array Items "[0]"
    if (key == "[0]") {
        if (!current.items) current.items = [type: 'object', properties: [:], required: []]
        return getNode(current.items, pathParts.drop(1))
    }
    
    if (!current.properties) current.properties = [:]
    
    if (!current.properties[key]) {
        // Default placeholder, will be filled when we hit the leaf entry
        current.properties[key] = [type: 'object', properties: [:], required: []]
    }
    
    return getNode(current.properties[key], pathParts.drop(1))
}

// Sort by path length to ensure parents exist? 
// DFS traversal order from input is usually safe, but let's be robust.
// Actually, simple path splitting works if we process carefully.

fieldList.each { field ->
    String path = field.fieldPath
    String type = field.type
    boolean req = field.required == "true" || field.required == true
    
    // cleanup path
    if (path.startsWith(".")) path = path.substring(1)
    
    List<String> parts = path.split(/\./).toList()
    String name = parts.last()
    
    // Parent node
    List<String> parentPath = parts.dropRight(1)
    Map parentNode = getNode(rootSchema, parentPath)
    
    // If name is "[0]", we are defining the array Item itself
    if (name == "[0]") {
        // The node IS 'items'
        // If the array itself was defined as type 'array', parentNode is that array node.
        // Wait, getNode returns the container. 
        // If parent is array, it has 'items'.
        if (parentNode.type == 'array') {
             if (!parentNode.items) parentNode.items = [:]
             parentNode.items.type = type
             // If object, prep props
             if (type == 'object' && !parentNode.items.properties) {
                 parentNode.items.properties = [:]
                 parentNode.items.required = []
             }
        }
    } else {
        // Regular property on Object
        // define property
        if (!parentNode.properties) parentNode.properties = [:]
        
        // Check if existing (created by child traversal)
        if (!parentNode.properties[name]) {
            parentNode.properties[name] = [:]
        }
        
        parentNode.properties[name].type = type
        if (type == 'object' && !parentNode.properties[name].properties) {
             parentNode.properties[name].properties = [:]
             parentNode.properties[name].required = []
        }
         if (type == 'array' && !parentNode.properties[name].items) {
             parentNode.properties[name].items = [:]
        }
        
        // Handle Required
        if (req) {
            if (parentNode.required == null) parentNode.required = []
            if (!parentNode.required.contains(name)) parentNode.required.add(name)
        }
    }
}

// Cleanup: Remove empty 'properties' and 'required' from leaf nodes or non-objects
// Valid JSON Schema shouldn't have empty 'properties' map if strict? No, it's allowed but useless.
// Let's do a recursive cleanup
def cleanup
cleanup = { Map node ->
    if (node.type != 'object') {
        node.remove('properties')
        node.remove('required')
    } else {
        if (node.properties && node.properties.isEmpty()) node.remove('properties')
        if (node.required && node.required.isEmpty()) node.remove('required')
    }
    
    if (node.type != 'array') {
        node.remove('items')
    }
    
    // Recurse
    if (node.properties) node.properties.each { k, v -> cleanup(v) }
    if (node.items) cleanup(node.items)
}

cleanup(rootSchema)

// -----------------------------------------------------
// 2. SAVE LOGIC
// -----------------------------------------------------

// -----------------------------------------------------
// 2. SAVE LOGIC
// -----------------------------------------------------

String schemaJson = JsonOutput.toJson(rootSchema)

// Determine name
String nameToSave = schemaName.trim()

// Check for existing by ID or Schema Name
def existingSchema = null

if (jsonSchemaId) {
    existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("jsonSchemaId", jsonSchemaId)
        .one()
} 

if (!existingSchema && nameToSave) {
    existingSchema = ec.entity.find("darpan.reconciliation.JsonSchema")
        .condition("schemaName", nameToSave)
        .one()
}

if (existingSchema) {
    // Expire existing
    String oldName = existingSchema.schemaName
    // Use format with underscore to keep it readable but unique
    String archivedName = "${oldName}_${ec.user.nowTimestamp.time}"
    
    // Ensure uniqueness just in case (though timestamp is usually enough)
    // We could check if archivedName exists, but it's highly unlikely.
    
    existingSchema.schemaName = archivedName
    existingSchema.statusId = "Disabled"
    existingSchema.update()
    
    // Create NEW with original name
    def newSchema = ec.entity.makeValue("darpan.reconciliation.JsonSchema")
    newSchema.schemaName = oldName
    newSchema.schemaText = schemaJson
    newSchema.description = description ?: existingSchema.description
    newSchema.statusId = "Active"
    
    newSchema.setSequencedIdPrimary()
    newSchema.create()
    
    jsonSchemaId = newSchema.jsonSchemaId
    nameToSave = newSchema.schemaName
} else {
    // Create
    def newSchema = ec.entity.makeValue("darpan.reconciliation.JsonSchema")
    newSchema.schemaName = nameToSave
    newSchema.schemaText = schemaJson
    newSchema.description = description
    newSchema.statusId = "Active"
    
    newSchema.setSequencedIdPrimary()
    newSchema.create()
    
    jsonSchemaId = newSchema.jsonSchemaId
}

schemaFileName = nameToSave // keep for backward compat but matches schemaName
schemaName = nameToSave


