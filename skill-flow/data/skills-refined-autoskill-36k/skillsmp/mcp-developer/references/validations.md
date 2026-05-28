# Mcp Developer - Validations

## Generic Tool Name Without Namespace

### **Id**
generic-tool-name
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - name:\s*['"](?:search|query|get|list|create|update|delete|read|write)['"]
### **Message**
Generic tool name without namespace. May collide with other MCP servers.
### **Fix Action**
Prefix tool name with server namespace (e.g., 'docs_search' instead of 'search')
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Tool Without Input Schema

### **Id**
missing-input-schema
### **Severity**
error
### **Type**
regex
### **Pattern**
  - name:\s*['"][^'"]+['"](?!.*inputSchema)
### **Message**
Tool defined without inputSchema. LLM cannot know what parameters to pass.
### **Fix Action**
Add inputSchema with JSON Schema or Zod-to-JSON-Schema conversion
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Zod Schema Passed Directly as inputSchema

### **Id**
zod-as-input-schema
### **Severity**
error
### **Type**
regex
### **Pattern**
  - inputSchema:\s*z\.
  - inputSchema:\s*[a-zA-Z]+Schema(?!.*zodToJsonSchema)
### **Message**
Zod schema passed directly. MCP expects JSON Schema format.
### **Fix Action**
Use zodToJsonSchema() to convert Zod schema to JSON Schema
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Console.log in MCP Server

### **Id**
console-log-in-server
### **Severity**
error
### **Type**
regex
### **Pattern**
  - console\.log\(
### **Message**
console.log writes to stdout, corrupting MCP protocol messages.
### **Fix Action**
Use process.stderr.write() for debugging or remove logging
### **Applies To**
  - **/mcp/**/*.ts
  - **/mcp/**/*.js
  - **/*-mcp-server*.ts
  - **/*-mcp-server*.js

## Async Handler Without Try/Catch

### **Id**
unhandled-async-in-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setRequestHandler.*async.*=>\s*\{
### **Message**
Async handler without visible error handling. Unhandled errors crash server.
### **Fix Action**
Wrap handler body in try/catch and return error response
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Tool Without Description

### **Id**
missing-tool-description
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - name:\s*['"][^'"]+['"](?!.*description)
### **Message**
Tool without description. LLM uses descriptions to understand when to use tools.
### **Fix Action**
Add clear description explaining what the tool does and when to use it
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Schema Parameters Without Descriptions

### **Id**
missing-parameter-descriptions
### **Severity**
info
### **Type**
regex
### **Pattern**
  - properties:\s*\{[^}]+\}(?!.*description)
### **Message**
Schema parameters without descriptions. Descriptions help LLM use tools correctly.
### **Fix Action**
Add .describe() in Zod or 'description' field in JSON Schema for each parameter
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Hardcoded URI Without Encoding

### **Id**
hardcoded-uri-scheme
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - uri.*`[^`]*\$\{[^}]+\}[^`]*`(?!.*encode|URI)
### **Message**
URI with interpolated values may need encoding for special characters.
### **Fix Action**
Use encodeURIComponent() for path segments in URIs
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Potential Secrets in Tool Response

### **Id**
secrets-in-response
### **Severity**
error
### **Type**
regex
### **Pattern**
  - content.*text.*(?:key|secret|token|password|apiKey|api_key)
### **Message**
Potential secrets in tool response. Secrets may leak to LLM output.
### **Fix Action**
Never include secrets in tool responses. Store server-side.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Tool With Mode/Action Enum

### **Id**
mega-tool-enum
### **Severity**
info
### **Type**
regex
### **Pattern**
  - action.*enum.*create.*update.*delete
  - mode.*enum.*list.*get.*create
  - operation.*enum.*read.*write
### **Message**
Tool with mode/action enum detected. Consider splitting into atomic tools.
### **Fix Action**
Create separate tools for each action for better LLM comprehension
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Error Response Without isError Flag

### **Id**
missing-error-flag
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - content.*type.*text.*[Ee]rror(?!.*isError)
### **Message**
Error message returned without isError flag. Client may not recognize as error.
### **Fix Action**
Add 'isError: true' to error responses
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Blocking Sync Operation in Handler

### **Id**
blocking-sync-operation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - readFileSync|writeFileSync|execSync
### **Message**
Synchronous blocking operation in handler. May timeout clients.
### **Fix Action**
Use async versions (readFile, writeFile, exec) with await
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Transport Without Close Handler

### **Id**
missing-transport-close
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new.*Transport(?!.*on.*close|onclose)
### **Message**
Transport created without close handler. Resources may leak.
### **Fix Action**
Add transport.on('close', ...) to clean up session state
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Resource Without MIME Type

### **Id**
resource-without-mimetype
### **Severity**
info
### **Type**
regex
### **Pattern**
  - uri:.*(?!.*mimeType)
### **Message**
Resource defined without mimeType. Client may not render correctly.
### **Fix Action**
Add mimeType field to resource definition
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx