# Api Design - Validations

## Verb in URL path

### **Id**
verb-in-url
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\\.(get|post)\\(["'].*/(get|create|update|delete|fetch)
  - router\\.(get|post)\\(["'].*/(get|create|update|delete|fetch)
### **Message**
URLs should use nouns, not verbs
### **Fix Action**
Use HTTP method + noun: POST /users instead of POST /createUser
### **Applies To**
  - *.js
  - *.ts

## Always returning 200 status

### **Id**
always-200
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - res\\.json\\(\\{[^}]*error
  - res\\.send\\(\\{[^}]*success.*false
### **Message**
Use proper HTTP status codes for errors
### **Fix Action**
Return 4xx/5xx status codes for errors
### **Applies To**
  - *.js
  - *.ts

## Wrong success status code

### **Id**
wrong-success-code
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.status\\(200\\)\\.json.*create
  - \\.status\\(204\\).*return.*json
### **Message**
Use 201 for creation, 204 should have no body
### **Fix Action**
POST creating resource: 201; DELETE: 204 with no body
### **Applies To**
  - *.js
  - *.ts

## Raw error object in response

### **Id**
raw-error-response
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - res\\.json\\(err\\)
  - res\\.json\\(error\\)
  - res\\.send\\(err\\.message\\)
### **Message**
Don't expose raw error objects
### **Fix Action**
Return sanitized error format
### **Applies To**
  - *.js
  - *.ts

## Stack trace in response

### **Id**
stack-trace-response
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - res\\..*err\\.stack
  - res\\..*error\\.stack
  - stack.*res\\.json
### **Message**
Never expose stack traces to clients
### **Fix Action**
Log stack trace, return generic error
### **Applies To**
  - *.js
  - *.ts

## Sequential ID in route

### **Id**
sequential-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - params\\.id.*parseInt
  - params\\.userId.*parseInt
### **Message**
Consider using UUIDs instead of sequential IDs
### **Fix Action**
Use UUIDs to prevent enumeration attacks
### **Applies To**
  - *.js
  - *.ts

## Route without rate limiting

### **Id**
no-rate-limit
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\.post\(["']/(auth|login|register)
### **Message**
Sensitive endpoints should have rate limiting
### **Fix Action**
Add rate limiter middleware
### **Applies To**
  - *.js
  - *.ts

## Handler without input validation

### **Id**
no-validation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - req\\.body\\.\\w+(?!.*parse|.*validate|.*schema)
### **Message**
Validate input before using
### **Fix Action**
Use Zod or similar to validate req.body
### **Applies To**
  - *.js
  - *.ts