# Mcp Security - Validations

## Missing Authentication Check

### **Id**
mcp-no-auth-check
### **Severity**
critical
### **Type**
regex
### **Pattern**
setRequestHandler.*CallTool
### **Negative Pattern**
authToken|authorization|verifyToken|authenticate|isAuthenticated
### **Message**
Tool handler without authentication check. Server may accept unauthenticated requests.
### **Fix Action**
Add authentication check at start of handler
### **Applies To**
  - *.ts
  - *.js

## Hardcoded Secrets

### **Id**
mcp-hardcoded-secrets
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:api_key|apiKey|secret|password|token|auth)\s*[=:]\s*["'][A-Za-z0-9+/=_-]{20,}["']
### **Message**
Hardcoded secret detected. Security vulnerability.
### **Fix Action**
Use environment variables: process.env.SECRET_NAME
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Rate Limiting

### **Id**
mcp-no-rate-limit
### **Severity**
high
### **Type**
regex
### **Pattern**
setRequestHandler.*CallTool
### **Negative Pattern**
rateLimit|rate_limit|throttle|RateLimiter
### **Message**
No rate limiting detected. Server vulnerable to abuse.
### **Fix Action**
Implement per-user rate limiting with rate-limiter-flexible or similar
### **Applies To**
  - *.ts
  - *.js

## Potential Path Traversal

### **Id**
mcp-path-traversal
### **Severity**
critical
### **Type**
regex
### **Pattern**
readFile|writeFile|fs\.|path\.join
### **Negative Pattern**
sanitize|validate|\.\.|startsWith|isAbsolute
### **Message**
File operations without path traversal protection.
### **Fix Action**
Validate paths don't contain '..' and are within allowed directories
### **Applies To**
  - *.ts
  - *.js

## Potential SQL Injection

### **Id**
mcp-sql-injection
### **Severity**
critical
### **Type**
regex
### **Pattern**
query\s*\(\s*[`"'].*\$\{|execute\s*\(\s*[`"'].*\+
### **Message**
String interpolation in SQL query. SQL injection risk.
### **Fix Action**
Use parameterized queries: query('SELECT * FROM users WHERE id = ?', [id])
### **Applies To**
  - *.ts
  - *.js

## Potential Command Injection

### **Id**
mcp-command-injection
### **Severity**
critical
### **Type**
regex
### **Pattern**
exec\s*\(\s*[`"'].*\$\{|spawn\s*\(\s*[`"'].*\+
### **Message**
String interpolation in shell command. Command injection risk.
### **Fix Action**
Use array form: spawn('cmd', ['arg1', arg2]) or whitelist commands
### **Applies To**
  - *.ts
  - *.js

## Logging Sensitive Data

### **Id**
mcp-sensitive-logging
### **Severity**
high
### **Type**
regex
### **Pattern**
console\.log.*(?:password|token|secret|key|auth)
### **Message**
Potentially logging sensitive data. Security risk.
### **Fix Action**
Sanitize logs to remove sensitive fields
### **Applies To**
  - *.ts
  - *.js

## User Data Without Sanitization

### **Id**
mcp-no-input-sanitization
### **Severity**
warning
### **Type**
regex
### **Pattern**
content.*text.*\$\{|text:.*\+.*arguments
### **Negative Pattern**
sanitize|escape|encode|filter
### **Message**
User data in response without sanitization. Prompt injection risk.
### **Fix Action**
Sanitize user data and wrap clearly in tool responses
### **Applies To**
  - *.ts
  - *.js