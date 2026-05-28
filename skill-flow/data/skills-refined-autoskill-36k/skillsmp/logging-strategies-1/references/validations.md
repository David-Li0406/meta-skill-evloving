# Logging Strategies - Validations

## Console.log in Production Code

### **Id**
log-console-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\\.log\\(
  - console\\.debug\\(
  - console\\.info\\(
  - console\\.warn\\(
  - console\\.error\\(
### **Message**
console.log detected. Use structured logger instead for production code.
### **Fix Action**
Replace with structured logger (pino, winston): logger.info({ data }, 'message')
### **Applies To**
  - src/**/*.ts
  - src/**/*.js
  - lib/**/*.ts
  - lib/**/*.js
### **Excludes**
  - **/*.test.*
  - **/*.spec.*
  - **/scripts/**

## Potential Sensitive Data in Log

### **Id**
log-sensitive-data
### **Severity**
error
### **Type**
regex
### **Pattern**
  - logger\\.[a-z]+.*password
  - logger\\.[a-z]+.*token
  - logger\\.[a-z]+.*secret
  - logger\\.[a-z]+.*apiKey
  - logger\\.[a-z]+.*authorization
  - console\\.log.*password
  - console\\.log.*token
### **Message**
Potentially logging sensitive data. Ensure proper redaction.
### **Fix Action**
Configure logger redaction or remove sensitive field from log
### **Applies To**
  - **/*.ts
  - **/*.js

## Logging Full Request Body

### **Id**
log-req-body-full
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - logger\\.[a-z]+.*req\\.body[^.]
  - logger\\.[a-z]+.*request\\.body[^.]
  - console\\.log.*req\\.body
  - JSON\\.stringify.*req\\.body
### **Message**
Logging full request body may expose sensitive data.
### **Fix Action**
Log specific safe fields only or configure redaction
### **Applies To**
  - **/*.ts
  - **/*.js

## Unstructured String Log

### **Id**
log-string-concatenation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\\.[a-z]+\\(`[^`]*\\$\\{
  - logger\.[a-z]+\(["'][^{]+["']\s*\)
  - console\\.log\\(`[^`]*\\$\\{
### **Message**
String concatenation in log. Use structured logging for searchability.
### **Fix Action**
Replace with: logger.info({ field: value }, 'message')
### **Applies To**
  - **/*.ts
  - **/*.js

## Error Logged Without Stack Trace

### **Id**
log-no-error-stack
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - logger\\.error\\([^)]*\\.message[^)]*\\)
  - logger\.error\(['"][^'"]+['"]\)
  - catch.*logger\\.error.*(?!.*stack)
### **Message**
Error logged without stack trace. Include full error object.
### **Fix Action**
Log complete error: logger.error({ err: error }, 'message')
### **Applies To**
  - **/*.ts
  - **/*.js

## Synchronous Log File Write

### **Id**
log-sync-file-write
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fs\\.appendFileSync.*log
  - fs\\.writeFileSync.*log
  - writeFileSync.*\\.log
### **Message**
Synchronous file write blocks event loop. Use async logging.
### **Fix Action**
Use pino with async destination or log aggregation service
### **Applies To**
  - **/*.ts
  - **/*.js

## Expensive Operation Without Level Check

### **Id**
log-no-level-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\\.debug.*JSON\\.stringify
  - logger\\.trace.*JSON\\.stringify
  - logger\\.debug.*\\bawait\\b
### **Message**
Expensive operation in debug log runs even when disabled.
### **Fix Action**
Check level first: if (logger.isLevelEnabled('debug')) { ... }
### **Applies To**
  - **/*.ts
  - **/*.js

## Request Handler Without Correlation ID

### **Id**
log-missing-correlation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\\.(get|post|put|delete).*logger\\.[a-z]+(?!.*correlationId|requestId|traceId)
### **Message**
Request handler logs without correlation ID. Hard to trace requests.
### **Fix Action**
Add correlation ID middleware and include in all logs
### **Applies To**
  - **/*.ts
  - **/*.js

## Error Logged at INFO Level

### **Id**
log-error-as-info
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - logger\\.info.*error
  - logger\\.info.*Error
  - logger\\.info.*exception
  - logger\\.info.*failed
### **Message**
Error condition logged at INFO level. Use appropriate level.
### **Fix Action**
Use logger.error() or logger.warn() for error conditions
### **Applies To**
  - **/*.ts
  - **/*.js

## 404 Logged as Error

### **Id**
log-404-as-error
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\\.error.*not found
  - logger\\.error.*404
  - logger\\.error.*NotFound
### **Message**
404 Not Found logged as error. This is normal operation, use info or warn.
### **Fix Action**
Use logger.info() for expected conditions like 404s
### **Applies To**
  - **/*.ts
  - **/*.js

## Caught Error Not Logged

### **Id**
log-catch-swallow
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch\\s*\\([^)]+\\)\\s*\\{\\s*\\}
  - catch\\s*\\([^)]+\\)\\s*\\{\\s*//[^}]*\\}
  - catch\\s*\\{\\s*\\}
### **Message**
Exception caught but not logged. Silent failures are hard to debug.
### **Fix Action**
Log the error before handling or rethrowing
### **Applies To**
  - **/*.ts
  - **/*.js

## Debug Level as Default

### **Id**
log-debug-default
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - level.*\|\|.*['"]debug['"]
  - LOG_LEVEL.*\|\|.*debug
  - level:\s*['"]debug['"]
### **Message**
Debug level as default. Should default to 'info' for production.
### **Fix Action**
Default to 'info': process.env.LOG_LEVEL || 'info'
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.json

## Logger Without Timestamp

### **Id**
log-no-timestamp
### **Severity**
info
### **Type**
regex
### **Pattern**
  - createLogger\\(\\{(?![^}]*timestamp)
  - winston\.format\.(?!.*timestamp)
### **Message**
Logger may be missing timestamp. Essential for debugging.
### **Fix Action**
Add timestamp to logger format
### **Applies To**
  - **/*.ts
  - **/*.js

## Logging Full Request Headers

### **Id**
log-headers-full
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - logger\\.[a-z]+.*req\\.headers[^.]
  - logger\\.[a-z]+.*request\\.headers[^.]
  - JSON\\.stringify.*headers
### **Message**
Logging full headers may expose authorization tokens and cookies.
### **Fix Action**
Log specific safe headers only or configure redaction
### **Applies To**
  - **/*.ts
  - **/*.js

## Log Then Throw Pattern

### **Id**
log-throw-after-log
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\\.error.*\\n\\s*throw
  - console\\.error.*\\n\\s*throw
### **Message**
Logging then throwing may cause duplicate log entries in error handler.
### **Fix Action**
Either log at throw site OR in error handler, not both
### **Applies To**
  - **/*.ts
  - **/*.js