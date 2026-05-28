# Observability - Validations

## Console.log in production code

### **Id**
console-log-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - console\.(log|debug|info|warn|error)\(
### **Message**
Use structured logger instead of console
### **Fix Action**
Replace with pino/winston logger
### **Applies To**
  - *.js
  - *.ts
### **Exclude**
  - *.test.*
  - *.spec.*

## Log without request context

### **Id**
log-without-context
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\.(info|error|warn)\([^{]*\)$
  - log\.(info|error|warn)\([^{]*\)$
### **Message**
Include context object in log calls
### **Fix Action**
Add context: logger.info({ request_id }, 'message')
### **Applies To**
  - *.js
  - *.ts

## Logging sensitive data

### **Id**
logging-password
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - log.*password
  - log.*token
  - log.*secret
  - log.*apiKey
  - log.*req\.body
  - console\.log.*password
### **Message**
Never log sensitive data
### **Fix Action**
Use redaction or log specific safe fields only
### **Applies To**
  - *.js
  - *.ts

## Logging error without stack

### **Id**
error-without-stack
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\.error\([^)]*error\.message[^)]*\)(?!.*stack)
  - log\.error\([^)]*err\.message[^)]*\)(?!.*stack)
### **Message**
Include stack trace when logging errors
### **Fix Action**
Log the full error object or include stack
### **Applies To**
  - *.js
  - *.ts

## High cardinality metric label

### **Id**
high-cardinality-label
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - labels:.*user_id
  - labels:.*userId
  - labels:.*email
  - labels:.*request_id
  - labels:.*requestId
  - labelNames.*user_id
  - labelNames.*userId
### **Message**
Avoid high-cardinality labels in metrics
### **Fix Action**
Use logs for user_id, metrics for aggregates only
### **Applies To**
  - *.js
  - *.ts

## Counter/Histogram without useful labels

### **Id**
metric-without-labels
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Counter\(\{[^}]*labelNames:\s*\[\s*\]
  - new Histogram\(\{[^}]*labelNames:\s*\[\s*\]
### **Message**
Add labels like method, path, status for filtering
### **Fix Action**
Add low-cardinality labels for useful breakdowns
### **Applies To**
  - *.js
  - *.ts

## Using raw path as metric label

### **Id**
unbounded-path-label
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - req\.url|req\.originalUrl|req\.path(?!.*route)
### **Message**
Use route pattern, not actual URL path
### **Fix Action**
Use req.route?.path which gives /users/:id not /users/123
### **Applies To**
  - *.js
  - *.ts

## HTTP call without trace propagation

### **Id**
fetch-without-trace
### **Severity**
info
### **Type**
regex
### **Pattern**
  - fetch\([^)]+\)(?!.*traceparent|.*propagat)
  - axios\.[^(]+\([^)]+\)(?!.*traceparent|.*propagat)
### **Message**
Propagate trace context to downstream services
### **Fix Action**
Use OpenTelemetry instrumentation or manual propagation
### **Applies To**
  - *.js
  - *.ts

## Span created but not ended

### **Id**
span-not-ended
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - startSpan\([^)]+\)(?!.*\.end\(\))
  - tracer\.startSpan(?!.*finally.*end)
### **Message**
Always end spans, preferably in finally block
### **Fix Action**
Use startActiveSpan with callback or end in finally
### **Applies To**
  - *.js
  - *.ts

## Sentry capture without context

### **Id**
sentry-without-context
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Sentry\.captureException\(\w+\)$
  - Sentry\.captureMessage\([^,]+\)$
### **Message**
Add context to Sentry captures
### **Fix Action**
Add tags, extra, or user context
### **Applies To**
  - *.js
  - *.ts

## Catch block without error reporting

### **Id**
catch-no-report
### **Severity**
info
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]+\)\s*\{[^}]*\}(?!.*Sentry|.*logger|.*log)
### **Message**
Caught errors should be logged or reported
### **Fix Action**
Add logger.error or Sentry.captureException
### **Applies To**
  - *.js
  - *.ts