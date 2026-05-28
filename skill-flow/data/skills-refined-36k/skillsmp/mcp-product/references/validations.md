# Mcp Product - Validations

## Required ID Parameter on Entry Tool

### **Id**
required-id-params
### **Severity**
critical
### **Type**
regex
### **Pattern**
required.*\[.*"(project_id|user_id|session_id)"
### **Message**
  This tool requires an ID parameter that new users won't have.
  
  Vibe coders calling for the first time will immediately fail.
  Make IDs optional and generate them if not provided.
  
### **Applies To**
  - **/tools/*.ts
  - **/tools/*.js

## Raw Error Messages

### **Id**
raw-error-throw
### **Severity**
critical
### **Type**
regex
### **Pattern**
throw new Error\([^)]*\b(Zod|schema|validation|parse|JSON)\b
### **Message**
  Error uses technical jargon that vibe coders won't understand.
  
  Wrap this error with a human-readable explanation and suggested action.
  
### **Applies To**
  - **/tools/*.ts
  - **/*.ts

## Minimal Success Response

### **Id**
minimal-success-response
### **Severity**
error
### **Type**
regex
### **Pattern**
return\s*\{\s*(success|ok|status)\s*:\s*(true|"ok"|"success")\s*\}
### **Message**
  This success response doesn't tell users what happened or what to do next.
  
  Add: what_happened, context, and next_steps to every success response.
  
### **Applies To**
  - **/tools/*.ts

## CRUD-style Tool Naming

### **Id**
crud-tool-naming
### **Severity**
error
### **Type**
regex
### **Pattern**
name:\s*["\'']spawner_(create|read|update|delete|get|set|fetch|query)_
### **Message**
  Tool name uses database operation style (CRUD).
  
  Users think in goals, not operations. Rename to reflect what users
  are trying to accomplish:
  - spawner_create_project → spawner_plan
  - spawner_get_skills → spawner_skills
  - spawner_update_memory → spawner_remember
  
### **Applies To**
  - **/tools/*.ts
  - **/index.ts

## Too Many Required Parameters

### **Id**
too-many-required-params
### **Severity**
error
### **Type**
regex
### **Pattern**
required:\s*\[[^\]]{100,}\]
### **Message**
  Tool has too many required parameters (detected long required array).
  
  This creates friction for first-time users. Reduce to 1-3 required
  params max, with smart defaults for everything else.
  
### **Applies To**
  - **/tools/*.ts

## Parameter Without Description

### **Id**
no-description-in-schema
### **Severity**
warning
### **Type**
regex
### **Pattern**
"[a-z_]+"\s*:\s*\{\s*type:\s*"
### **Message**
  Schema parameter has no description.
  
  Claude uses descriptions to understand what to pass. Vibe coders
  see descriptions when exploring tools. Always include helpful descriptions.
  
### **Applies To**
  - **/tools/*.ts

## Inconsistent Response Envelope

### **Id**
inconsistent-response-shape
### **Severity**
warning
### **Type**
regex
### **Pattern**
return\s*\{\s*(result|data|output|response|payload)\s*:
### **Message**
  Response uses a non-standard envelope.
  
  For consistency, prefer a standard shape across all tools:
  { success, data?, error?, meta? }
  
### **Applies To**
  - **/tools/*.ts

## Error Without Suggestion

### **Id**
missing-error-suggestion
### **Severity**
warning
### **Type**
regex
### **Pattern**
error:\s*\{\s*message:[^}]+\}(?!\s*,\s*(suggestion|what_to_do|try))
### **Message**
  Error response has no suggestion for what to try next.
  
  Vibe coders need guidance. Add a "suggestion" or "what_to_do" field.
  
### **Applies To**
  - **/tools/*.ts