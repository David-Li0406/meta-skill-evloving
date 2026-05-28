# Upstash Qstash - Validations

## Webhook signature verification

### **Id**
qstash-signature-verification
### **Severity**
critical
### **Type**
regex
### **Pattern**
Receiver|receiver\.verify
### **Message**
QStash webhook handlers must verify signatures using Receiver
### **Fix Action**
Add signature verification: const receiver = new Receiver({ currentSigningKey, nextSigningKey }); await receiver.verify({ signature, body, url })
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js
  - **/qstash*.ts
  - **/qstash*.js
  - **/api/**/route.ts
  - **/api/**/route.js
### **Inverse**


## Both signing keys configured

### **Id**
qstash-signing-keys-present
### **Severity**
critical
### **Type**
regex
### **Pattern**
currentSigningKey.*nextSigningKey|nextSigningKey.*currentSigningKey
### **Message**
QStash Receiver must have both currentSigningKey and nextSigningKey for key rotation
### **Fix Action**
Configure both keys: new Receiver({ currentSigningKey: process.env.QSTASH_CURRENT_SIGNING_KEY, nextSigningKey: process.env.QSTASH_NEXT_SIGNING_KEY })
### **Applies To**
  - **/*.ts
  - **/*.js
### **Inverse**


## QStash token hardcoded

### **Id**
qstash-token-hardcoded
### **Severity**
critical
### **Type**
regex
### **Pattern**
token:\s*['"]qstash_[a-zA-Z0-9]+
### **Message**
QStash token must not be hardcoded - use environment variables
### **Fix Action**
Use process.env.QSTASH_TOKEN
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## QStash signing keys hardcoded

### **Id**
qstash-signing-key-hardcoded
### **Severity**
critical
### **Type**
regex
### **Pattern**
(currentSigningKey|nextSigningKey):\s*['"]sig_[a-zA-Z0-9]+
### **Message**
QStash signing keys must not be hardcoded
### **Fix Action**
Use process.env.QSTASH_CURRENT_SIGNING_KEY and process.env.QSTASH_NEXT_SIGNING_KEY
### **Applies To**
  - **/*.ts
  - **/*.js

## Localhost URL in QStash publish

### **Id**
qstash-localhost-url
### **Severity**
critical
### **Type**
regex
### **Pattern**
url:\s*['"]https?://localhost|url:\s*['"]https?://127\.0\.0\.1
### **Message**
QStash cannot reach localhost - endpoints must be publicly accessible
### **Fix Action**
Use a public URL (e.g., your deployed domain or ngrok for testing)
### **Applies To**
  - **/*.ts
  - **/*.js

## HTTP URL instead of HTTPS

### **Id**
qstash-http-url
### **Severity**
error
### **Type**
regex
### **Pattern**
url:\s*['"]http://(?!localhost|127\.0\.0\.1)
### **Message**
QStash requires HTTPS URLs for security
### **Fix Action**
Change http:// to https://
### **Applies To**
  - **/*.ts
  - **/*.js

## QStash publish without error handling

### **Id**
qstash-missing-error-handling
### **Severity**
error
### **Type**
regex
### **Pattern**
await qstash\.publish(?:JSON)?\([^)]+\)(?![^;]*catch)
### **Message**
QStash publish calls should have error handling for rate limits and failures
### **Fix Action**
Wrap in try/catch and handle errors appropriately
### **Applies To**
  - **/*.ts
  - **/*.js

## Using parsed JSON for signature verification

### **Id**
qstash-raw-body-required
### **Severity**
critical
### **Type**
regex
### **Pattern**
req\.json\(\).*receiver\.verify|receiver\.verify.*req\.json\(\)
### **Message**
Signature verification requires raw body (req.text()), not parsed JSON
### **Fix Action**
Use await req.text() to get raw body for verification
### **Applies To**
  - **/*.ts
  - **/*.js

## Callback endpoint without signature verification

### **Id**
qstash-callback-missing-verification
### **Severity**
critical
### **Type**
regex
### **Pattern**
callback|failureCallback
### **Message**
Callback endpoints must also verify signatures - they receive QStash requests too
### **Fix Action**
Add Receiver signature verification to callback handlers
### **Applies To**
  - **/callback*.ts
  - **/callback*.js
### **Inverse**


## Schedule without destination URL

### **Id**
qstash-schedule-missing-destination
### **Severity**
error
### **Type**
regex
### **Pattern**
schedules\.create\([^)]*\)(?!.*destination)
### **Message**
QStash schedules require a destination URL
### **Fix Action**
Add destination: 'https://your-app.com/api/endpoint' to schedule options
### **Applies To**
  - **/*.ts
  - **/*.js

## Critical operation without deduplication

### **Id**
qstash-deduplication-critical-ops
### **Severity**
warning
### **Type**
regex
### **Pattern**
(charge|payment|subscription|order).*publishJSON(?![^;]*deduplicationId)
### **Message**
Critical operations (payments, orders) should use deduplicationId to prevent duplicates
### **Fix Action**
Add deduplicationId: 'unique-operation-id' to prevent duplicate processing
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing retry configuration

### **Id**
qstash-missing-retries-config
### **Severity**
warning
### **Type**
regex
### **Pattern**
publishJSON\([^)]*\)(?!.*retries)
### **Message**
Consider configuring retries for your specific use case
### **Fix Action**
Add retries option if default (3) doesn't match your needs
### **Applies To**
  - **/*.ts
  - **/*.js

## Potentially large message body

### **Id**
qstash-large-body-warning
### **Severity**
warning
### **Type**
regex
### **Pattern**
body:\s*\{[^}]{500,}\}
### **Message**
Large message bodies may hit size limits - consider sending references instead
### **Fix Action**
Send IDs/references and fetch full data in the handler
### **Applies To**
  - **/*.ts
  - **/*.js

## URL group operations without name

### **Id**
qstash-url-group-without-name
### **Severity**
error
### **Type**
regex
### **Pattern**
urlGroups\.(add|remove)Endpoints\([^)]*\)(?!.*name)
### **Message**
URL group operations require a group name
### **Fix Action**
Add name: 'your-group-name' to URL group options
### **Applies To**
  - **/*.ts
  - **/*.js

## Environment variables accessed in client code

### **Id**
qstash-env-vars-in-client
### **Severity**
critical
### **Type**
regex
### **Pattern**
process\.env\.QSTASH
### **Message**
QStash tokens and signing keys must only be used server-side
### **Fix Action**
Ensure QStash operations are only in server components or API routes
### **Applies To**
  - **/*.tsx
  - **/*.jsx
  - **/components/**/*.ts
  - **/components/**/*.js