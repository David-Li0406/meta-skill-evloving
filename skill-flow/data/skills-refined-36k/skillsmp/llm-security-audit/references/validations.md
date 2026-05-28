# Llm Security Audit - Validations

## Missing Security Event Logging

### **Id**
no-security-logging
### **Severity**
high
### **Type**
regex
### **Pattern**
(?:messages\.create|completion|chat)\s*\(
### **Negative Pattern**
log|audit|monitor|track|record
### **Message**
LLM API calls without security event logging.
### **Fix Action**
Log all LLM interactions with timestamps, user IDs, and request hashes
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Rate Limiting on LLM Endpoints

### **Id**
no-rate-limiting
### **Severity**
high
### **Type**
regex
### **Pattern**
app\.(?:get|post)\s*\([^)]*(?:chat|completion|generate|ask)
### **Negative Pattern**
rateLimit|rateLimiter|throttle|limiter
### **Message**
LLM endpoint without rate limiting. Vulnerable to DoS and cost attacks.
### **Fix Action**
Add rate limiting: app.use('/api/chat', rateLimiter({ max: 10, window: 60000 }))
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Cost Monitoring

### **Id**
no-cost-monitoring
### **Severity**
medium
### **Type**
regex
### **Pattern**
messages\.create|completion\.create|chat\.completions
### **Negative Pattern**
cost|usage|tokens|billing|budget
### **Message**
LLM calls without cost/usage tracking. Risk of unexpected bills.
### **Fix Action**
Track token usage and implement budget alerts
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Hardcoded LLM API Key

### **Id**
hardcoded-api-key
### **Severity**
critical
### **Type**
regex
### **Pattern**
(?:ANTHROPIC_API_KEY|OPENAI_API_KEY|api[_-]?key)\s*[:=]\s*["'][a-zA-Z0-9_-]{20,}["']
### **Message**
Hardcoded API key detected. Use environment variables.
### **Fix Action**
Use process.env.ANTHROPIC_API_KEY or secrets manager
### **Applies To**
  - *.ts
  - *.js
  - *.py
  - *.env

## LLM Call Without Timeout

### **Id**
no-timeout
### **Severity**
medium
### **Type**
regex
### **Pattern**
messages\.create|completion\.create|chat\.completions\.create
### **Negative Pattern**
timeout|signal|AbortController
### **Message**
LLM API call without timeout. Could hang indefinitely.
### **Fix Action**
Add timeout: new AbortController() with setTimeout
### **Applies To**
  - *.ts
  - *.js

## LLM Call Without Error Handling

### **Id**
no-error-handling
### **Severity**
medium
### **Type**
regex
### **Pattern**
await\s+(?:client|anthropic|openai)\.(?:messages|chat|completions)
### **Negative Pattern**
try|catch|\.catch|error|except
### **Message**
LLM API call without error handling.
### **Fix Action**
Wrap in try-catch and handle API errors gracefully
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Potential PII in LLM Logs

### **Id**
pii-in-logs
### **Severity**
high
### **Type**
regex
### **Pattern**
console\.log|logger\.(?:info|debug|log)\s*\([^)]*(?:message|content|prompt|input)
### **Negative Pattern**
redact|mask|sanitize|scrub
### **Message**
Logging LLM content that may contain PII.
### **Fix Action**
Redact PII before logging: log(redactPII(content))
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Model Selection Without Validation

### **Id**
no-model-validation
### **Severity**
medium
### **Type**
regex
### **Pattern**
model:\s*(?:req|user|input|body)\.
### **Message**
Model parameter from user input. Could be manipulated.
### **Fix Action**
Validate model against allowed list before use
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Content Policy Enforcement

### **Id**
no-content-policy
### **Severity**
medium
### **Type**
regex
### **Pattern**
messages\.create|completion\.create
### **Negative Pattern**
content.?policy|moderat|filter|safe|block
### **Message**
LLM without content policy enforcement.
### **Fix Action**
Implement content moderation for inputs and outputs
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing User Context Isolation

### **Id**
no-user-isolation
### **Severity**
high
### **Type**
regex
### **Pattern**
messages\.push|conversation|history
### **Negative Pattern**
user.?id|session.?id|isolat|tenant
### **Message**
Conversation context without user isolation. Risk of data leakage.
### **Fix Action**
Isolate conversation contexts by user/session ID
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Audit Trail

### **Id**
no-audit-trail
### **Severity**
high
### **Type**
regex
### **Pattern**
tool.?call|function.?call|execute
### **Negative Pattern**
audit|log|record|trace
### **Message**
Tool/function execution without audit trail.
### **Fix Action**
Log all tool executions with user, timestamp, and parameters
### **Applies To**
  - *.ts
  - *.js
  - *.py

## AI Dependencies Without Vulnerability Scanning

### **Id**
no-dependency-scanning
### **Severity**
medium
### **Type**
regex
### **Pattern**
"@anthropic-ai/sdk"|"openai"|"langchain"|"llama-index"
### **Negative Pattern**
audit|snyk|trivy|dependabot
### **Message**
AI SDK dependency without vulnerability scanning configured.
### **Fix Action**
Add npm audit, Snyk, or Dependabot for dependency scanning
### **Applies To**
  - package.json
  - requirements.txt
  - pyproject.toml