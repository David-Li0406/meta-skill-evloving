# Incident Responder - Validations

## Missing Error Context in Logging

### **Id**
no-error-logging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.error\(['"][^'"]+['"]\)
  - logger\.error\(['"][^'"]+['"]\)
  - log\.error\(['"][^'"]+['"]\)
### **Message**
Error logged without context. Include error object and relevant state.
### **Fix Action**
Add context: logger.error('Payment failed', { orderId, error, userId })
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - \{|error:|err:|e:|ex:|exception

## Error Caught and Ignored

### **Id**
silent-failure
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{\s*\}
  - \.catch\(\(\)\s*=>\s*\{\}\)
  - \.catch\(\s*\(\)\s*=>\s*null\)
### **Message**
Silent error handling hides failures. At minimum, log the error.
### **Fix Action**
Log errors: catch(e) { logger.error('Operation failed', { error: e }); }
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Generic Error Message

### **Id**
generic-error-message
### **Severity**
info
### **Type**
regex
### **Pattern**
  - throw new Error\(['"]Error['"]\)
  - throw new Error\(['"]Something went wrong['"]\)
  - throw new Error\(['"]An error occurred['"]\)
### **Message**
Generic error message provides no debugging context.
### **Fix Action**
Include specific context: throw new Error(`Failed to process order ${orderId}: ${reason}`)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## HTTP Response Without Request ID

### **Id**
no-request-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - res\.status\(\d{3}\)\.json\(\{(?!.*requestId)
  - res\.send\(\{(?!.*requestId)
### **Message**
Response without request ID makes incident correlation difficult.
### **Fix Action**
Include request ID in error responses for easy log correlation
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## No Health Check Endpoint

### **Id**
missing-health-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\.listen\(
  - createServer\(
### **Message**
Server without health check. Add /health endpoint for monitoring.
### **Fix Action**
Add health check: app.get('/health', (req, res) => res.json({ status: 'ok' }))
### **Applies To**
  - **/server.ts
  - **/server.js
  - **/app.ts
  - **/app.js
  - **/index.ts
### **Exceptions**
  - /health|/healthz|/ready|/ping

## External Call Without Timeout

### **Id**
no-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\([^)]+\)(?!.*timeout)
  - axios\.get\([^)]+\)(?!.*timeout)
  - axios\.post\([^)]+\)(?!.*timeout)
### **Message**
External call without timeout can hang indefinitely during incidents.
### **Fix Action**
Add timeout: fetch(url, { signal: AbortSignal.timeout(5000) })
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - timeout|signal|AbortController

## External Dependency Without Circuit Breaker

### **Id**
no-circuit-breaker
### **Severity**
info
### **Type**
regex
### **Pattern**
  - fetch\(['"]https?://(?!localhost)
  - axios\.[a-z]+\(['"]https?://(?!localhost)
### **Message**
External API call without circuit breaker. Failure can cascade.
### **Fix Action**
Consider circuit breaker pattern for critical external dependencies
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Hardcoded Retry Count

### **Id**
hardcoded-retry-count
### **Severity**
info
### **Type**
regex
### **Pattern**
  - retry.*[35]\s*times
  - maxRetries.*=.*[35]
  - for\s*\(.*<\s*[35].*retry
### **Message**
Hardcoded retry count. Consider configurable retry with backoff.
### **Fix Action**
Make retry configurable and add exponential backoff
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Alert Without Clear Threshold

### **Id**
missing-alert-threshold
### **Severity**
info
### **Type**
regex
### **Pattern**
  - alert\s*\{
  - createAlert\(
### **Message**
Alert configuration found. Verify thresholds are appropriate.
### **Fix Action**
Ensure thresholds prevent alert fatigue while catching real issues
### **Applies To**
  - **/*.yaml
  - **/*.yml
  - **/alerts/**
  - **/monitoring/**

## Missing Graceful Shutdown Handler

### **Id**
no-graceful-shutdown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.listen\(
  - server\.listen\(
### **Message**
Server without graceful shutdown handling. Active requests may fail on deploy.
### **Fix Action**
Add SIGTERM handler to complete in-flight requests before shutdown
### **Applies To**
  - **/server.ts
  - **/server.js
  - **/app.ts
  - **/app.js
### **Exceptions**
  - SIGTERM|gracefulShutdown|closeServer

## Synchronous Logging in Hot Path

### **Id**
sync-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - writeFileSync.*log
  - appendFileSync.*log
### **Message**
Sync file logging can block during incidents. Use async logging.
### **Fix Action**
Use async logging or buffered logging library
### **Applies To**
  - **/*.ts
  - **/*.js

## API Endpoint Without Rate Limiting

### **Id**
no-rate-limiting
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\.post\(['"]/
  - router\.post\(['"]/
### **Message**
POST endpoint may need rate limiting to prevent abuse during incidents.
### **Fix Action**
Consider rate limiting on public endpoints
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
### **Exceptions**
  - rateLimit|throttle|limit

## Async Operation Without Correlation

### **Id**
missing-correlation-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - queue\.publish\((?!.*correlationId)
  - emit\(['"]\w+['"],(?!.*traceId)
### **Message**
Async operation without correlation ID. Hard to trace during incidents.
### **Fix Action**
Pass correlation/trace ID through async boundaries
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Catch-All Error Handler Too Generic

### **Id**
catch-all-error
### **Severity**
info
### **Type**
regex
### **Pattern**
  - catch\s*\(\s*\w+\s*\)\s*\{[^}]*res\.status\(500\)
### **Message**
Generic 500 response hides specific error types. Consider error classification.
### **Fix Action**
Classify errors: 400 for validation, 503 for downstream, 500 for unknown
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx