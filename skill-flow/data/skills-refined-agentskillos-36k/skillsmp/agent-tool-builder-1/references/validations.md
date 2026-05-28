# Agent Tool Builder - Validations

## Tool Description Must Be Comprehensive

### **Id**
tool-description-length
### **Severity**
warning
### **Description**
Tool descriptions should be at least 100 characters
### **Pattern**
  "description":\s*"[^"]{1,99}"
  
### **Message**
Tool description is too short. Add details about when to use it, parameters, and return values.
### **Autofix**


## Parameter Descriptions Required

### **Id**
parameter-description-missing
### **Severity**
warning
### **Description**
Every parameter should have a description
### **Pattern**
  "properties":\s*\{[^}]*"type":\s*"[^"]+"\s*[,}]
  
### **Anti Pattern**
  "description"
  
### **Message**
Parameter missing description. Describe what it is and the expected format.
### **Autofix**


## Schema Should Specify Required Fields

### **Id**
missing-required-array
### **Severity**
info
### **Description**
Explicitly define which fields are required
### **Pattern**
  "input_schema":\s*\{[^}]*"properties"
  
### **Anti Pattern**
  "required"
  
### **Message**
Schema doesn't specify required fields. Add 'required' array.
### **Autofix**


## Tool Implementation Needs Error Handling

### **Id**
tool-no-try-catch
### **Severity**
error
### **Description**
Tool functions should handle exceptions
### **Pattern**
  def\s+\w+.*->.*str:|async\s+def\s+\w+.*->.*str:
  
### **Anti Pattern**
  try:|except
  
### **Message**
Tool function without try/except block. Add error handling.
### **Autofix**


## Error Results Need is_error Flag

### **Id**
missing-is-error-flag
### **Severity**
warning
### **Description**
When returning errors, set is_error to true
### **Pattern**
  "content":\s*"[Ee]rror
  
### **Anti Pattern**
  "is_error":\s*true
  
### **Message**
Error result without is_error flag. Add 'is_error': true.
### **Autofix**


## Tools Should Return Strings

### **Id**
returning-dict-not-string
### **Severity**
warning
### **Description**
Return JSON string, not dict/object
### **Pattern**
  return\s*\{[^}]+\}$
  
### **Message**
Returning dict instead of string. Use json.dumps() or JSON.stringify().
### **Autofix**


## Tools Should Validate Inputs

### **Id**
tool-no-input-validation
### **Severity**
warning
### **Description**
Validate LLM-provided inputs before execution
### **Pattern**
  def\s+\w+\([^)]+\)\s*->|async\s+def\s+\w+\([^)]+\)\s*->
  
### **Anti Pattern**
  isinstance|len\(|\.strip\(\)|validate|sanitize
  
### **Message**
Tool function without visible input validation. Validate before execution.
### **Autofix**


## SQL Queries Must Use Parameterization

### **Id**
sql-without-parameterization
### **Severity**
error
### **Description**
Never concatenate user input into SQL
### **Pattern**
  execute\([^)]*\+|execute\([^)]*f"|execute\([^)]*%
  
### **Message**
SQL query appears to use string concatenation. Use parameterized queries.
### **Autofix**


## External Calls Need Timeouts

### **Id**
external-call-no-timeout
### **Severity**
warning
### **Description**
HTTP requests and external calls should have timeouts
### **Pattern**
  requests\.(get|post|put|delete)\(|fetch\(|axios\.|http\.
  
### **Anti Pattern**
  timeout
  
### **Message**
External API call without timeout. Add timeout parameter.
### **Autofix**


## MCP Tools Must Have Input Schema

### **Id**
mcp-tool-missing-inputschema
### **Severity**
error
### **Description**
All MCP tools require inputSchema
### **Pattern**
  name:\s*["'][^"']+["']
  
### **Anti Pattern**
  inputSchema
  
### **Message**
MCP tool definition missing inputSchema.
### **Autofix**


## Parallel Results Must Be Single Message

### **Id**
parallel-results-separate-messages
### **Severity**
error
### **Description**
All parallel tool results go in one user message
### **Pattern**
  append.*tool_result.*\n.*append.*tool_result
  
### **Message**
Parallel tool results in separate messages. Combine into single message.
### **Autofix**
