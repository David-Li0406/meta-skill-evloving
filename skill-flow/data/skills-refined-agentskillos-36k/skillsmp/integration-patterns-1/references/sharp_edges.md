# Integration Patterns - Sharp Edges

## Synchronous Call Chain Causes Cascade Failure

### **Id**
sync-chain-cascade
### **Severity**
critical
### **Summary**
One slow service brings down entire request path
### **Symptoms**
  - Request timeouts cascade
  - One service issue affects all callers
  - Thread pool exhaustion
### **Why**
  When Service A calls B calls C synchronously, a problem in C
  causes B to block, which causes A to block. Threads pile up,
  timeouts cascade, and your entire system becomes unavailable.
  
### **Gotcha**
  "The payment service is slow"
  "And now the order service is down"
  "And the checkout page times out"
  "But we only changed the inventory service!"
  
  # Synchronous chain: checkout → order → payment → inventory
  
### **Solution**
  1. Break synchronous chains:
     - Use async events where possible
     - Add circuit breakers
     - Set aggressive timeouts
  
  2. Bulkhead pattern:
     - Separate thread pools per integration
     - Rate limit downstream calls
     - Fail fast when pool exhausted
  
  3. Fallback strategies:
     - Return cached data
     - Degrade gracefully
     - Queue for later retry
  

## Non-Idempotent Operations Cause Duplicates

### **Id**
no-idempotency
### **Severity**
critical
### **Summary**
Retry logic processes same request multiple times
### **Symptoms**
  - Duplicate orders
  - Double charges
  - Duplicate notifications
### **Why**
  Networks are unreliable. Requests will be retried. If your
  operations aren't idempotent, retries cause duplicates.
  This is especially dangerous for financial operations.
  
### **Gotcha**
  "Customer was charged twice"
  "The first request timed out, so we retried"
  "But the first one actually went through"
  "We just didn't get the response"
  
  # Network timeout doesn't mean the operation failed
  
### **Solution**
  1. Idempotency keys:
     - Client generates unique key
     - Server stores key → result
     - Return cached result on retry
  
  2. Natural idempotency:
     - PUT over POST where possible
     - Include timestamp/version in request
     - Check for existing before insert
  
  3. Deduplication:
     - Message deduplication in queues
     - Track processed message IDs
     - Time-based dedup windows
  

## No Dead Letter Queue for Failed Messages

### **Id**
missing-dlq
### **Severity**
high
### **Summary**
Failed messages disappear or block the queue
### **Symptoms**
  - Messages silently dropped
  - Queue blocked by poison messages
  - No visibility into failures
### **Why**
  Some messages will fail processing - bad data, temporary issues,
  bugs. Without a DLQ, these either disappear forever or block
  your queue. You need a place to park failures for investigation.
  
### **Gotcha**
  "Where did those orders go?"
  "They were in the queue..."
  "The consumer crashed processing them"
  "And then?"
  "They were lost"
  
  # No DLQ = lost data
  
### **Solution**
  1. Configure DLQ for every queue:
     - Set max retry attempts
     - Route to DLQ after exhaustion
     - Alert on DLQ depth
  
  2. DLQ processing:
     - Monitor DLQ continuously
     - Investigate root causes
     - Replay after fixes
  
  3. Poison message handling:
     - Catch and log exceptions
     - Don't block healthy messages
     - Track failure patterns
  

## Schema Change Breaks Consumers

### **Id**
schema-breaking-change
### **Severity**
high
### **Summary**
Producer schema update breaks existing consumers
### **Symptoms**
  - Consumers crash after producer deploy
  - Deserialization failures
  - Data loss from unknown fields
### **Why**
  Producers and consumers deploy independently. If you change
  a schema without backward compatibility, old consumers break.
  This is especially painful with many consumers.
  
### **Gotcha**
  "We renamed the 'user_id' field to 'customer_id'"
  "All consumers are crashing"
  "They expect 'user_id'"
  "We need to update 15 services"
  
  # Breaking change requires synchronized deploy of everything
  
### **Solution**
  1. Schema evolution rules:
     - Add fields as optional
     - Never remove required fields
     - Never change field types
     - Deprecate before removing
  
  2. Schema registry:
     - Version all schemas
     - Compatibility checks on publish
     - Block breaking changes
  
  3. Consumer tolerance:
     - Ignore unknown fields
     - Handle missing optional fields
     - Multiple schema version support
  

## No Circuit Breaker on External Calls

### **Id**
no-circuit-breaker
### **Severity**
high
### **Summary**
Failing external service consumes all resources
### **Symptoms**
  - Thread pool exhaustion
  - Cascading timeouts
  - Slow degradation then crash
### **Why**
  When an external service fails, continuing to call it wastes
  resources (threads, connections) and adds latency. A circuit
  breaker fails fast, protecting your system from cascade failure.
  
### **Gotcha**
  "The API is timing out"
  "We're retrying..."
  "All threads are blocked waiting for responses"
  "Now our API is timing out too"
  
  # Failing service consumed all available threads
  
### **Solution**
  1. Circuit breaker per external dependency:
     - Track failure rate
     - Open circuit on threshold
     - Fail fast when open
  
  2. Configure properly:
     - Failure threshold (e.g., 5 failures)
     - Recovery timeout (e.g., 30 seconds)
     - Half-open test requests
  
  3. Combine with bulkhead:
     - Dedicated thread pool
     - Limited connections
     - Independent failure domains
  