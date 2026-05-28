# Agent Communication - Validations

## Untyped Message Passing

### **Id**
untyped-message
### **Severity**
medium
### **Type**
regex
### **Pattern**
send\s*\([^)]*\{[^}]*\}|emit\s*\([^)]*\{[^}]*\}
### **Negative Pattern**
Schema|schema|z\.|zod|type:
### **Message**
Sending untyped message. Use schema validation for type safety.
### **Fix Action**
Define message schema with Zod and validate before sending
### **Applies To**
  - *.ts
  - *.js

## Message Without Unique ID

### **Id**
no-message-id
### **Severity**
medium
### **Type**
regex
### **Pattern**
(?:send|emit|publish)\s*\(\s*\{(?![^}]*(?:id|messageId|eventId))
### **Message**
Message without unique identifier. Debugging and deduplication will fail.
### **Fix Action**
Add messageId: crypto.randomUUID() to all messages
### **Applies To**
  - *.ts
  - *.js

## Missing Correlation ID for Request-Response

### **Id**
no-correlation-id
### **Severity**
medium
### **Type**
regex
### **Pattern**
request|response|reply
### **Negative Pattern**
correlationId|correlation_id|requestId|request_id
### **Message**
Request-response pattern without correlation ID.
### **Fix Action**
Include correlationId to match responses to requests
### **Applies To**
  - *.ts
  - *.js

## Critical Message Without Acknowledgment

### **Id**
fire-and-forget-critical
### **Severity**
high
### **Type**
regex
### **Pattern**
(?:send|emit)\s*\([^)]*(?:critical|important|required)
### **Negative Pattern**
ack|acknowledge|confirm|waitFor
### **Message**
Critical message sent without acknowledgment mechanism.
### **Fix Action**
Use reliable messaging with acknowledgments for critical messages
### **Applies To**
  - *.ts
  - *.js

## Waiting for Message Without Timeout

### **Id**
no-message-timeout
### **Severity**
high
### **Type**
regex
### **Pattern**
await\s+(?:waitFor|receive|getMessage)
### **Negative Pattern**
timeout|Promise\.race|AbortController
### **Message**
Waiting for message without timeout. Could hang indefinitely.
### **Fix Action**
Add timeout: Promise.race([waitFor(), timeout(5000)])
### **Applies To**
  - *.ts
  - *.js

## Event Handler Without Error Handling

### **Id**
event-handler-no-error-handling
### **Severity**
high
### **Type**
regex
### **Pattern**
\.on\s*\([^)]+,\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{
### **Negative Pattern**
try|catch|\.catch|error
### **Message**
Event handler without error handling. Errors will propagate.
### **Fix Action**
Wrap handler in try-catch to prevent cascade failures
### **Applies To**
  - *.ts
  - *.js

## Message Passing Without Logging

### **Id**
no-message-logging
### **Severity**
medium
### **Type**
regex
### **Pattern**
(?:send|emit|publish|receive)\s*\(
### **Negative Pattern**
log|trace|record|audit
### **Message**
Message passing without logging. Debugging will be difficult.
### **Fix Action**
Log all messages with timestamps for debugging
### **Applies To**
  - *.ts
  - *.js

## Event Handler Emitting Same Event Type

### **Id**
circular-event-risk
### **Severity**
critical
### **Type**
regex
### **Pattern**
\.on\s*\(["'](\w+)["'][^}]+emit\s*\(["'](\1)["']
### **Message**
Event handler emits same event type it listens to. Risk of infinite loop.
### **Fix Action**
Break the cycle or add deduplication/rate limiting
### **Applies To**
  - *.ts
  - *.js

## Blocking Operation in Event Handler

### **Id**
blocking-in-event-handler
### **Severity**
medium
### **Type**
regex
### **Pattern**
\.on\s*\([^)]+,\s*\([^)]*\)\s*=>\s*\{[^}]*(?:sleep|setTimeout.*await|while)
### **Message**
Blocking operation in event handler. May slow down event processing.
### **Fix Action**
Use non-blocking patterns or spawn separate task
### **Applies To**
  - *.ts
  - *.js

## Event Publishing Without Rate Limiting

### **Id**
no-rate-limiting-events
### **Severity**
medium
### **Type**
regex
### **Pattern**
while.*emit|for.*emit|map.*emit
### **Negative Pattern**
rateLimit|throttle|debounce|limit
### **Message**
Publishing events in loop without rate limiting.
### **Fix Action**
Add rate limiting to prevent broadcast storms
### **Applies To**
  - *.ts
  - *.js