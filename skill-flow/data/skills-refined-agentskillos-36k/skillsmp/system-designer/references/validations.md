# System Designer - Validations

## Hardcoded Service URL

### **Id**
hardcoded-url
### **Severity**
error
### **Type**
regex
### **Pattern**
  - https?://(?:localhost|127\.0\.0\.1|\d+\.\d+\.\d+\.\d+):\d+
  - https?://[a-z-]+\.(?:internal|local|corp)\.[a-z]+/
### **Message**
Hardcoded service URL. This breaks when services move or scale.
### **Fix Action**
Use environment variables or service discovery for URLs.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Network Call Without Timeout

### **Id**
missing-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\([^)]*\)(?![^;]*timeout)
  - axios\.(?:get|post|put|delete)\([^)]*\)(?![^;]*timeout)
  - http\.(?:get|post)\([^)]*\)(?![^;]*timeout)
### **Message**
Network call without explicit timeout. Will hang forever if remote is slow.
### **Fix Action**
Add timeout: fetch(url, { signal: AbortSignal.timeout(5000) })
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Query Without Limit

### **Id**
unbounded-query
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.findMany\(\s*\{(?![^}]*take:)
  - \.find\(\s*\{\}\s*\)
  - SELECT\s+\*\s+FROM\s+\w+(?!.*LIMIT)
### **Message**
Query without limit. Will cause memory issues as data grows.
### **Fix Action**
Add pagination: .findMany({ take: 50, skip: offset })
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Sequential Awaits That Could Be Parallel

### **Id**
sequential-await
### **Severity**
info
### **Type**
regex
### **Pattern**
  - await\s+\w+\([^)]*\);\s*await\s+\w+\(
### **Message**
Sequential awaits may be parallelizable with Promise.all().
### **Fix Action**
If independent, use: const [a, b] = await Promise.all([fn1(), fn2()])
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Slow Sync Operation in Request Handler

### **Id**
sync-in-request
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await\s+sendEmail
  - await\s+sendNotification
  - await\s+generatePDF
  - await\s+generateReport
### **Message**
Slow operation blocking request. Consider async processing with queue.
### **Fix Action**
Queue for background processing: queue.add({ type: 'email', data })
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Mutable Operation Without Idempotency

### **Id**
missing-idempotency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \+\+|\+=|-=|--
  - \.increment\(
  - \.push\(
### **Message**
Mutable operation may cause duplicates on retry. Consider idempotency.
### **Fix Action**
Use idempotency keys or idempotent operations (SET instead of INCREMENT).
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## External Call Without Retry

### **Id**
no-retry-logic
### **Severity**
info
### **Type**
regex
### **Pattern**
  - await\s+stripe\.
  - await\s+twilio\.
  - await\s+sendgrid\.
  - await\s+s3Client\.
### **Message**
External service call without retry logic. Transient failures will fail permanently.
### **Fix Action**
Wrap in retry with exponential backoff for transient errors.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Money Stored or Calculated as Float

### **Id**
money-as-float
### **Severity**
error
### **Type**
regex
### **Pattern**
  - price:\s*number
  - amount:\s*number
  - price\s*=\s*\d+\.\d+
  - amount\s*\*\s*\d+\.\d+
### **Message**
Money handled as float can cause rounding errors. Use cents (integer).
### **Fix Action**
Store money as cents (integer): price_cents: 1999 for $19.99
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Multiple Services Without Circuit Breaker

### **Id**
no-circuit-breaker
### **Severity**
info
### **Type**
regex
### **Pattern**
  - services\s*=\s*\[
  - Promise\.all\(\[.*http
### **Message**
Multiple service calls without circuit breaker. Slow service can cascade.
### **Fix Action**
Implement circuit breaker pattern to fail fast when downstream is unhealthy.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## HTTP Instead of HTTPS

### **Id**
http-not-https
### **Severity**
error
### **Type**
regex
### **Pattern**
  - http://(?!localhost|127\.0\.0\.1)
  - protocol:\s*['"]http['"]
### **Message**
HTTP used instead of HTTPS. Data in transit is not encrypted.
### **Fix Action**
Use HTTPS for all non-localhost connections.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Shared State in Stateless Server

### **Id**
shared-state-web
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - let\s+\w+\s*=\s*\{\}
  - const\s+cache\s*=\s*new\s+Map
  - global\.\w+\s*=
### **Message**
Module-level mutable state in web server. Won't work with multiple instances.
### **Fix Action**
Use external state store (Redis, database) for shared state.
### **Applies To**
  - **/api/**/*.ts
  - **/routes/**/*.ts
  - **/handlers/**/*.ts

## Delete Without Cascade Consideration

### **Id**
cascade-delete-missing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.delete\(\{\s*where:
  - DELETE\s+FROM\s+\w+\s+WHERE
### **Message**
Delete operation may leave orphaned related records.
### **Fix Action**
Consider cascade delete or check for dependent records first.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Service Without Health Check Endpoint

### **Id**
no-health-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\.listen|server\.listen|createServer
### **Message**
Server created but no health check endpoint found.
### **Fix Action**
Add /health endpoint for load balancer and monitoring.
### **Applies To**
  - **/server.ts
  - **/index.ts
  - **/app.ts

## Environment-Specific Logic in Code

### **Id**
env-in-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - if.*process\.env\.NODE_ENV.*===.*production
  - if.*development.*\{.*else.*production
### **Message**
Environment-specific branching in code. Prefer environment variables.
### **Fix Action**
Use environment variables for config, not conditionals in code.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx