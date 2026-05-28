# Inngest - Validations

## Inngest serve handler present

### **Id**
inngest-serve-handler
### **Severity**
critical
### **Type**
regex
### **Pattern**
export const \{ GET, POST, PUT \} = serve
### **Message**
Inngest requires a serve handler to receive events
### **Fix Action**
Create app/api/inngest/route.ts with serve() export
### **Applies To**
  - **/api/inngest/*.ts
  - **/api/inngest/*.js
### **Inverse**


## Functions registered with serve

### **Id**
inngest-function-registered
### **Severity**
error
### **Type**
regex
### **Pattern**
serve\(\{[^}]*functions:\s*\[[^\]]+\]
### **Message**
Ensure all Inngest functions are registered in the serve() call
### **Fix Action**
Add function to the functions array in serve()
### **Applies To**
  - **/api/inngest/*.ts
  - **/api/inngest/*.js

## Step.run has descriptive name

### **Id**
inngest-step-run-naming
### **Severity**
warning
### **Type**
regex
### **Pattern**
step\.run\(['"][a-z0-9-]+['"]
### **Message**
Step names should be kebab-case and descriptive
### **Fix Action**
Use descriptive step names like 'fetch-user' or 'send-email'
### **Applies To**
  - **/*.ts
  - **/*.js

## waitForEvent has timeout

### **Id**
inngest-waitForEvent-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
step\.waitForEvent\([^)]+\)(?!.*timeout)
### **Message**
waitForEvent should have a timeout to prevent infinite waits
### **Fix Action**
Add timeout option: { timeout: '24h' }
### **Applies To**
  - **/*.ts
  - **/*.js

## Function has concurrency limit

### **Id**
inngest-concurrency-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
createFunction\([^)]+\)(?!.*concurrency)
### **Message**
Consider adding concurrency limits to protect downstream services
### **Fix Action**
Add concurrency: { limit: 10 } to function config
### **Applies To**
  - **/*.ts
  - **/*.js

## Event types defined

### **Id**
inngest-event-id-typed
### **Severity**
warning
### **Type**
regex
### **Pattern**
new Inngest\(\{[^}]*id:
### **Message**
Inngest client should define event schemas for type safety
### **Fix Action**
Add schemas: new EventSchemas().fromRecord<Events>()
### **Applies To**
  - **/inngest/client.ts
  - **/inngest/index.ts

## Function has unique ID

### **Id**
inngest-function-id
### **Severity**
critical
### **Type**
regex
### **Pattern**
createFunction\(\{\s*id:\s*['"][a-z0-9-]+['"]
### **Message**
Every Inngest function must have a unique ID
### **Fix Action**
Add id: 'my-function-name' to function config
### **Applies To**
  - **/*.ts
  - **/*.js
### **Inverse**


## Sleep uses duration string

### **Id**
inngest-sleep-duration-string
### **Severity**
warning
### **Type**
regex
### **Pattern**
step\.sleep\([^,]+,\s*[0-9]+\)
### **Message**
step.sleep should use duration strings like '1h' or '30m', not milliseconds
### **Fix Action**
Use duration string: step.sleep('wait', '1h')
### **Applies To**
  - **/*.ts
  - **/*.js

## Retry policy configured

### **Id**
inngest-retries-configured
### **Severity**
warning
### **Type**
regex
### **Pattern**
createFunction\([^)]+retries:
### **Message**
Consider configuring retry policy for failure handling
### **Fix Action**
Add retries: 3 or retries: { attempts: 3, backoff: { ... } }
### **Applies To**
  - **/*.ts
  - **/*.js

## Idempotency key for payment functions

### **Id**
inngest-idempotency-for-payments
### **Severity**
error
### **Type**
regex
### **Pattern**
event:\s*['"](?:payment|order|charge|subscription)[/\.][^'"]+['"].*(?!.*idempotency)
### **Message**
Payment-related functions should use idempotency keys
### **Fix Action**
Add idempotency: 'event.data.orderId' to function config
### **Applies To**
  - **/*.ts
  - **/*.js

## Step has error handling

### **Id**
inngest-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
step\.run\([^)]+\)(?![^;]*\.catch)
### **Message**
Consider error handling for steps that may fail
### **Fix Action**
Wrap in try/catch or use onFailure handler
### **Applies To**
  - **/*.ts
  - **/*.js

## Inngest keys not hardcoded

### **Id**
inngest-env-key-exposed
### **Severity**
critical
### **Type**
regex
### **Pattern**
signKey:\s*['"][a-zA-Z0-9]+
### **Message**
Inngest signing keys must not be hardcoded
### **Fix Action**
Use process.env.INNGEST_SIGNING_KEY
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Cron schedule has timezone

### **Id**
inngest-cron-timezone
### **Severity**
warning
### **Type**
regex
### **Pattern**
cron:\s*['"][^'"]+['"](?![^}]*tz)
### **Message**
Cron schedules should specify timezone to avoid ambiguity
### **Fix Action**
Add tz: 'America/New_York' to cron config
### **Applies To**
  - **/*.ts
  - **/*.js

## Large data in event payload

### **Id**
inngest-large-payload-in-send
### **Severity**
warning
### **Type**
regex
### **Pattern**
inngest\.send\([^)]*(?:content|body|document|file|data\.(?:content|body))
### **Message**
Event payloads should be small - send IDs, not data
### **Fix Action**
Store large data externally and send only references/IDs
### **Applies To**
  - **/*.ts
  - **/*.js

## Steps in tight loops

### **Id**
inngest-step-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for\s*\([^)]+\)\s*\{[^}]*step\.(run|sleep)
### **Message**
Steps in loops create many checkpoints - consider batching
### **Fix Action**
Batch operations or use fan-out pattern with sendEvent
### **Applies To**
  - **/*.ts
  - **/*.js