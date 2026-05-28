# Integration Patterns - Validations

## Missing Circuit Breaker

### **Id**
no-circuit-breaker
### **Severity**
error
### **Type**
regex
### **Pattern**
  - requests\.get\((?!.*circuit)
  - http\.request\((?!.*breaker)
  - fetch\((?!.*circuitBreaker)
### **Message**
External HTTP call may lack circuit breaker protection.
### **Fix Action**
Add circuit breaker for external service calls
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Missing Request Timeout

### **Id**
no-timeout-set
### **Severity**
error
### **Type**
regex
### **Pattern**
  - requests\.(?!.*timeout)
  - aiohttp.*(?!.*timeout)
  - axios\((?!.*timeout)
### **Message**
HTTP request may not have timeout configured.
### **Fix Action**
Set explicit timeout for all external calls
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Missing Idempotency Key

### **Id**
no-idempotency-key
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - POST.*payment(?!.*idempotency)
  - create_order\((?!.*idempotency_key)
  - process_charge\((?!.*dedup)
### **Message**
Financial operation may lack idempotency key.
### **Fix Action**
Add idempotency key for financial operations
### **Applies To**
  - **/*.py
  - **/*.ts

## Missing Dead Letter Queue

### **Id**
no-dead-letter-queue
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - SQS.*Queue(?!.*DeadLetterQueue)
  - create_queue\((?!.*dlq)
  - subscribe\((?!.*dead_letter)
### **Message**
Message queue may lack dead letter queue configuration.
### **Fix Action**
Configure DLQ for message queue
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.yaml

## Synchronous Call in Event Handler

### **Id**
sync-in-event-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - on_event.*requests\.get
  - handle_message.*http\.post
  - consume.*await.*fetch
### **Message**
Synchronous HTTP call in event handler - consider async.
### **Fix Action**
Use async patterns or emit events instead of sync calls
### **Applies To**
  - **/*.py
  - **/*.ts

## Missing Retry Configuration

### **Id**
no-retry-config
### **Severity**
info
### **Type**
regex
### **Pattern**
  - publish_event\((?!.*retry)
  - send_message\((?!.*attempts)
### **Message**
Event publishing may lack retry configuration.
### **Fix Action**
Configure retries with exponential backoff
### **Applies To**
  - **/*.py
  - **/*.ts

## Hardcoded Service Endpoint

### **Id**
hardcoded-endpoint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - http://localhost:[0-9]+
  - https://api\.production\.
  - service_url\s*=\s*['"]http
### **Message**
Service endpoint may be hardcoded - use service discovery.
### **Fix Action**
Use environment variables or service discovery
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js