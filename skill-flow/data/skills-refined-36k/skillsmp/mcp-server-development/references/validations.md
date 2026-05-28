# Mcp Server Development - Validations

## Tool Without Input Schema

### **Id**
mcp-no-input-schema
### **Severity**
critical
### **Type**
regex
### **Pattern**
name:\s*["'][^"']+["']
### **Negative Pattern**
inputSchema|input_schema
### **Message**
Tool defined without inputSchema. AI can't know what parameters to send.
### **Fix Action**
Add inputSchema with properties, types, and required fields
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Tool With Vague Description

### **Id**
mcp-vague-description
### **Severity**
warning
### **Type**
regex
### **Pattern**
description:\s*["'](?:This tool|Handles|Manages|Does)[^"']{0,30}["']
### **Message**
Tool description is vague. Include WHEN to use it and WHAT it returns.
### **Fix Action**
Expand description: what it does, when to use, what it returns
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Tool Handler Without Error Handling

### **Id**
mcp-no-error-handling
### **Severity**
high
### **Type**
regex
### **Pattern**
setRequestHandler.*CallTool
### **Negative Pattern**
try|catch|isError|error
### **Message**
Tool handler without error handling. Failures will crash or hang.
### **Fix Action**
Wrap handler in try/catch, return isError: true on failure
### **Applies To**
  - *.ts
  - *.js

## No Input Validation

### **Id**
mcp-no-validation
### **Severity**
high
### **Type**
regex
### **Pattern**
request\.params\.arguments
### **Negative Pattern**
z\.|zod|Zod|ajv|Ajv|validate|safeParse|parse\(
### **Message**
Using request arguments without validation. Unsafe input from AI.
### **Fix Action**
Validate with Zod or Ajv before using arguments
### **Applies To**
  - *.ts
  - *.js

## Synchronous Long Operation

### **Id**
mcp-sync-long-operation
### **Severity**
warning
### **Type**
regex
### **Pattern**
await.*(?:fetch|request|query|exec|spawn)
### **Negative Pattern**
timeout|AbortController|signal|jobId|background
### **Message**
Long operation without timeout. May cause transport timeout.
### **Fix Action**
Add timeout, or return job ID and implement polling
### **Applies To**
  - *.ts
  - *.js

## Hardcoded Credentials

### **Id**
mcp-hardcoded-creds
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:api_key|apiKey|secret|password|token)\s*[=:]\s*["'][^"']{8,}["']
### **Message**
Hardcoded credentials in MCP server. Security vulnerability.
### **Fix Action**
Use environment variables: process.env.API_KEY
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Request Logging

### **Id**
mcp-no-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
setRequestHandler
### **Negative Pattern**
console\.log|logger|log\(|logging
### **Message**
No logging in request handler. Debugging will be difficult.
### **Fix Action**
Add logging for requests and responses with correlation IDs
### **Applies To**
  - *.ts
  - *.js

## Global Mutable State

### **Id**
mcp-global-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
let\s+\w+\s*=|var\s+\w+\s*=
### **Negative Pattern**
const|readonly|server\.
### **Message**
Global mutable state may not persist between requests.
### **Fix Action**
Use external storage (Redis, DB) or stateless design
### **Applies To**
  - *.ts
  - *.js

## No Rate Limiting

### **Id**
mcp-no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
setRequestHandler.*CallTool
### **Negative Pattern**
rateLimit|rate_limit|throttle|limit
### **Message**
No rate limiting. Server vulnerable to abuse.
### **Fix Action**
Implement per-user or global rate limiting
### **Applies To**
  - *.ts
  - *.js
  - *.py