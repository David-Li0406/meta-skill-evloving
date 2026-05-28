# Email Systems - Validations

## Missing plain text email part

### **Id**
missing-text-part
### **Description**
Emails should always include a plain text alternative
### **Severity**
warning
### **Pattern**
send\s*\(\s*\{[^}]*html\s*:[^}]*\}\s*\)
### **Negative Pattern**
text\s*:
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Email being sent with HTML but no plain text part. Add 'text:' property for accessibility and deliverability.
### **Fix Hint**
Add text: 'Plain text version' alongside html property

## Hardcoded from email address

### **Id**
hardcoded-from-email
### **Description**
From addresses should come from environment variables
### **Severity**
warning
### **Pattern**
from\s*:\s*['"][^'"]+@[^'"]+['"]
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Exclude Patterns**
  - **/*.test.*
  - **/*.spec.*
### **Message**
From email appears hardcoded. Use environment variable for flexibility.
### **Fix Hint**
Use process.env.FROM_EMAIL or similar

## Missing bounce webhook handler

### **Id**
no-bounce-handler
### **Description**
Email bounces should be handled to maintain list hygiene
### **Severity**
warning
### **Pattern**
resend|sendgrid|postmark|mailgun
### **Negative Pattern**
bounce|Bounce|BOUNCE
### **File Patterns**
  - **/webhook*.ts
  - **/api/**/*.ts
### **Message**
Email provider used but no bounce handling detected. Implement webhook handler for bounces.
### **Fix Hint**
Add webhook endpoint to handle bounce events and mark emails as invalid

## Missing List-Unsubscribe header

### **Id**
missing-unsubscribe-header
### **Description**
Marketing emails should include List-Unsubscribe header
### **Severity**
info
### **Pattern**
newsletter|marketing|campaign|broadcast
### **Negative Pattern**
List-Unsubscribe|listUnsubscribe|unsubscribe.*header
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Marketing email detected without List-Unsubscribe header. Add header for better deliverability.
### **Fix Hint**
Add headers: { 'List-Unsubscribe': '<mailto:...>, <https://...>' }

## Synchronous email send in request handler

### **Id**
sync-email-send
### **Description**
Email sends should be queued, not blocking
### **Severity**
warning
### **Pattern**
await.*send.*email|await.*resend.*send|await.*sendgrid.*send
### **File Patterns**
  - **/api/**/*.ts
  - **/routes/**/*.ts
### **Message**
Email sent synchronously in request handler. Consider queuing for better reliability.
### **Fix Hint**
Queue email send job instead of awaiting directly in request

## Email send without retry logic

### **Id**
no-email-retry
### **Description**
Email sends should have retry mechanism for failures
### **Severity**
info
### **Pattern**
send\s*\(\s*\{
### **Negative Pattern**
retry|attempts|backoff
### **File Patterns**
  - **/email*.ts
  - **/mail*.ts
### **Message**
Email send without apparent retry logic. Add retry for transient failures.
### **Fix Hint**
Wrap send in retry logic or use queue with built-in retries

## Email API key in code

### **Id**
exposed-api-key
### **Description**
API keys should come from environment variables
### **Severity**
error
### **Pattern**
api[_-]?key\s*[=:]\s*['"][A-Za-z0-9]{20,}['"]
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Exclude Patterns**
  - **/*.example.*
  - **/*.test.*
### **Message**
Email API key appears hardcoded in source code. Use environment variable.
### **Fix Hint**
Use process.env.RESEND_API_KEY or similar

## Bulk email without rate limiting

### **Id**
no-rate-limiting
### **Description**
Bulk sends should respect provider rate limits
### **Severity**
warning
### **Pattern**
forEach.*send|map.*send|Promise\.all.*send
### **Negative Pattern**
limit|throttle|batch|delay|sleep
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Bulk email sending without apparent rate limiting. Add throttling to avoid hitting limits.
### **Fix Hint**
Add delay between sends or use batching

## Email without preview text

### **Id**
missing-preview-text
### **Description**
Emails should include preview/preheader text
### **Severity**
info
### **Pattern**
html\s*:[^}]*<body
### **Negative Pattern**
preview|preheader|Preview
### **File Patterns**
  - **/*.ts
  - **/*.tsx
### **Message**
Email template without preview text. Add hidden preheader for inbox preview.
### **Fix Hint**
Add <Preview>Your preview text</Preview> at start of email

## Email send without logging

### **Id**
missing-email-logging
### **Description**
Email sends should be logged for debugging and auditing
### **Severity**
warning
### **Pattern**
await.*send.*\{
### **Negative Pattern**
log|Log|track|audit|db\.|prisma\.|supabase\.
### **File Patterns**
  - **/email*.ts
  - **/mail*.ts
  - **/send*.ts
### **Message**
Email being sent without apparent logging. Log sends for debugging and compliance.
### **Fix Hint**
Log email sent event with recipient, subject, and message ID

## Unsafe template interpolation in email

### **Id**
template-interpolation-xss
### **Description**
User input in emails should be escaped
### **Severity**
error
### **Pattern**
\$\{.*user.*\}|\$\{.*input.*\}|\$\{.*req\.
### **File Patterns**
  - **/email*.ts
  - **/template*.ts
### **Message**
User input interpolated in email template. Ensure proper escaping to prevent HTML injection.
### **Fix Hint**
Use email library's built-in escaping or sanitize input

## Email send without error handling

### **Id**
missing-error-handling
### **Description**
Email sends can fail and should be handled
### **Severity**
warning
### **Pattern**
await.*send\(
### **Negative Pattern**
try|catch|\.catch|error
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Email send without apparent error handling. Wrap in try-catch or handle promise rejection.
### **Fix Hint**
Add try-catch block and log/handle failures appropriately