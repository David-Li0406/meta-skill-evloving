# Microservices Patterns - Validations

## Service Call Without Timeout

### **Id**
microservices-no-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - axios\.(get|post|put|delete)\([^)]+\)(?![\s\S]{0,100}timeout)
  - fetch\([^)]+\)(?![\s\S]{0,100}signal|AbortController)
  - http\.request(?![\s\S]{0,200}timeout)
### **Message**
Service calls without timeout can hang forever and cause cascade failures.
### **Fix Action**
Add timeout option: axios.get(url, { timeout: 5000 })
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/services/**

## External Call Without Circuit Breaker

### **Id**
microservices-no-circuit-breaker
### **Severity**
error
### **Type**
regex
### **Pattern**
  - axios\.(get|post).*Service(?![\s\S]{0,500}circuit|breaker|opossum)
  - fetch.*api(?![\s\S]{0,500}circuit)
### **Message**
External service calls should use circuit breaker to prevent cascade failures.
### **Fix Action**
Wrap calls with opossum circuit breaker
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/services/**

## Multiple Services Accessing Same Table

### **Id**
microservices-shared-db
### **Severity**
error
### **Type**
regex
### **Pattern**
  - from.*orders.*from.*products.*from.*users
  - JOIN.*orders.*JOIN.*inventory
### **Message**
Services should own their data. Shared tables create coupling.
### **Fix Action**
Each service should have its own database with denormalized data
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.sql

## Synchronous Service Call Chain

### **Id**
microservices-sync-chain
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await.*Service.*await.*Service.*await.*Service
  - await.*client\.[a-z]+.*await.*client\.[a-z]+.*await.*client
### **Message**
Chain of sync calls multiplies latency and failure probability. Consider async.
### **Fix Action**
Use events for non-blocking operations, parallelize independent calls
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing Correlation ID

### **Id**
microservices-no-correlation-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - axios\.(get|post)(?![\s\S]{0,300}correlation|x-request-id|traceId)
  - fetch(?![\s\S]{0,300}correlation|requestId)
### **Message**
Service calls should include correlation ID for distributed tracing.
### **Fix Action**
Add x-correlation-id header to all service calls
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/services/**

## Service Call Without Retry Logic

### **Id**
microservices-no-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - axios\.(get|post)(?![\s\S]{0,500}retry|attempt|backoff)
  - try.*await.*Service(?![\s\S]{0,300}retry)
### **Message**
Transient failures need retry with backoff.
### **Fix Action**
Add retry logic with exponential backoff for transient errors
### **Applies To**
  - **/*.ts
  - **/*.js

## Chatty Service Communication

### **Id**
microservices-chatty
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*of.*await.*Service
  - map.*async.*await.*Service
  - Promise\.all.*\.map.*Service
### **Message**
Multiple sequential service calls cause high latency. Batch or denormalize.
### **Fix Action**
Use batch endpoints, denormalize data, or aggregate at source
### **Applies To**
  - **/*.ts
  - **/*.js

## Event Handler Without Idempotency

### **Id**
microservices-no-idempotency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - eventBus\.subscribe(?![\s\S]{0,500}idempotency|dedupe|already)
  - on\(['"].*created['"](?![\s\S]{0,300}idempotent)
### **Message**
Event handlers must be idempotent - events can be redelivered.
### **Fix Action**
Check for duplicate processing using event ID or idempotency key
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/handlers/**
  - **/events/**

## No Fallback for Service Failure

### **Id**
microservices-no-fallback
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - circuitBreaker(?![\s\S]{0,300}fallback)
  - try.*await.*Service(?![\s\S]{0,200}catch.*fallback|catch.*default)
### **Message**
Service calls should have fallback for graceful degradation.
### **Fix Action**
Add fallback behavior when dependency is unavailable
### **Applies To**
  - **/*.ts
  - **/*.js

## Hardcoded Service URL

### **Id**
microservices-hardcoded-url
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - http://localhost:[0-9]+/api
  - https://[a-z]+-service\.[a-z]+\.com
  - baseURL.*=.*['"]http
### **Message**
Service URLs should come from environment/config, not hardcoded.
### **Fix Action**
Use process.env.SERVICE_URL or service discovery
### **Applies To**
  - **/*.ts
  - **/*.js

## Service Without Health Check

### **Id**
microservices-no-health-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - express\(\)(?![\s\S]{0,1000}/health|/ready|/live)
  - createServer(?![\s\S]{0,1000}health)
### **Message**
Services need health check endpoints for orchestration.
### **Fix Action**
Add /health and /ready endpoints
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/server.*
  - **/app.*

## Missing Graceful Shutdown

### **Id**
microservices-no-graceful-shutdown
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - listen\([0-9]+(?![\s\S]{0,1000}SIGTERM|graceful)
  - createServer(?![\s\S]{0,1000}SIGTERM)
### **Message**
Services need graceful shutdown for zero-downtime deploys.
### **Fix Action**
Handle SIGTERM to stop accepting requests and drain connections
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/server.*

## API Without Versioning

### **Id**
microservices-no-api-version
### **Severity**
info
### **Type**
regex
### **Pattern**
  - app\.(get|post)\(['"]/((?!v[0-9]).)*['"]
  - router\.(get|post)\(['"]/((?!v[0-9]).)*['"]
### **Message**
API endpoints should be versioned for backward compatibility.
### **Fix Action**
Add version prefix: /v1/orders instead of /orders
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/routes/**

## Service Without Metrics

### **Id**
microservices-no-metrics
### **Severity**
info
### **Type**
regex
### **Pattern**
  - express\(\)(?![\s\S]{0,2000}prometheus|metrics|prom-client)
### **Message**
Services should expose metrics for monitoring.
### **Fix Action**
Add Prometheus metrics endpoint with prom-client
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/server.*

## Unstructured Logging

### **Id**
microservices-no-structured-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.log\([^{]
  - console\.error\(['"]
### **Message**
Use structured JSON logging for log aggregation.
### **Fix Action**
Use logger.info({ message, correlationId, ...data })
### **Applies To**
  - **/*.ts
  - **/*.js

## Direct Database Access Across Boundaries

### **Id**
microservices-direct-db-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - import.*from.*other-service.*db
  - require.*other-service.*prisma
### **Message**
Services should not directly access another service's database.
### **Fix Action**
Use service API calls instead of direct database access
### **Applies To**
  - **/*.ts
  - **/*.js