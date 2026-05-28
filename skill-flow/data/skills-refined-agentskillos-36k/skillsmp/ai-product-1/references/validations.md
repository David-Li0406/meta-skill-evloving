# Ai Product - Validations

## LLM output used without validation

### **Id**
unvalidated-llm-output
### **Description**
LLM responses should be validated against a schema
### **Severity**
warning
### **Pattern**
JSON\.parse\s*\(.*completion|JSON\.parse\s*\(.*message\.content
### **Negative Pattern**
schema|Schema|validate|Validate|parse.*z\.|zod
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
LLM output parsed as JSON without schema validation. Use Zod or similar to validate.
### **Fix Hint**
Wrap in ResponseSchema.parse() to validate structure

## Unsanitized user input in prompt

### **Id**
user-input-in-prompt
### **Description**
User input in prompts risks injection attacks
### **Severity**
warning
### **Pattern**
content\s*:\s*`[^`]*\$\{.*input|content\s*:\s*`[^`]*\$\{.*req\.
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
User input interpolated directly in prompt content. Sanitize or use separate message.
### **Fix Hint**
Put user input in separate 'user' role message, not template literal

## LLM response without streaming

### **Id**
no-streaming
### **Description**
Long LLM responses should be streamed for better UX
### **Severity**
info
### **Pattern**
completions\.create\s*\(|chat\.completions\.create\s*\(
### **Negative Pattern**
stream\s*:\s*true
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
LLM call without streaming. Consider stream: true for better user experience.
### **Fix Hint**
Add stream: true and use streaming response handler

## LLM call without error handling

### **Id**
missing-error-handling-llm
### **Description**
LLM API calls can fail and should be handled
### **Severity**
warning
### **Pattern**
await.*openai\.|await.*anthropic\.
### **Negative Pattern**
try|catch|\.catch
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
LLM API call without apparent error handling. Add try-catch for failures.
### **Fix Hint**
Wrap in try-catch and handle rate limits, timeouts, etc.

## LLM API key in code

### **Id**
hardcoded-api-key
### **Description**
API keys should come from environment variables
### **Severity**
error
### **Pattern**
sk-[A-Za-z0-9]{32,}|anthropic-[A-Za-z0-9]{32,}
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Exclude Patterns**
  - **/*.test.*
  - **/*.spec.*
### **Message**
LLM API key appears hardcoded. Use environment variable.
### **Fix Hint**
Use process.env.OPENAI_API_KEY or similar

## LLM usage without token tracking

### **Id**
no-token-tracking
### **Description**
Track token usage for cost monitoring
### **Severity**
info
### **Pattern**
completions\.create|chat\.create
### **Negative Pattern**
usage|tokens|cost|billing|track
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
LLM call without apparent usage tracking. Log token usage for cost monitoring.
### **Fix Hint**
Access response.usage.total_tokens and log/store it

## LLM call without timeout

### **Id**
missing-timeout
### **Description**
LLM calls should have timeout to prevent hanging
### **Severity**
warning
### **Pattern**
openai\.|anthropic\.
### **Negative Pattern**
timeout|AbortController|signal
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
LLM call without apparent timeout. Add timeout to prevent hanging requests.
### **Fix Hint**
Use AbortController with timeout or library timeout option

## User-facing LLM without rate limiting

### **Id**
no-rate-limiting-llm
### **Description**
LLM endpoints should be rate limited per user
### **Severity**
warning
### **Pattern**
POST.*chat|POST.*completion|POST.*generate
### **Negative Pattern**
rateLimit|limit|throttle|Ratelimit
### **File Patterns**
  - **/api/**/*.ts
  - **/routes/**/*.ts
### **Message**
LLM API endpoint without apparent rate limiting. Add per-user limits.
### **Fix Hint**
Add rate limiter middleware (e.g., Upstash Ratelimit)

## Sequential embedding generation

### **Id**
sync-embedding-loop
### **Description**
Bulk embeddings should be batched, not sequential
### **Severity**
info
### **Pattern**
for.*await.*embedding|forEach.*await.*embedding
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Message**
Embeddings generated sequentially. Batch requests for better performance.
### **Fix Hint**
Use bulk embedding API or Promise.all with batching

## Single LLM provider with no fallback

### **Id**
no-fallback-provider
### **Description**
Consider fallback provider for reliability
### **Severity**
info
### **Pattern**
openai|anthropic
### **Negative Pattern**
fallback|alternative|backup|retry.*different
### **File Patterns**
  - **/ai/**/*.ts
  - **/llm/**/*.ts
### **Message**
Single LLM provider without fallback. Consider backup provider for outages.
### **Fix Hint**
Add fallback to alternative provider on failure

## Long prompts hardcoded in source

### **Id**
prompt-in-code
### **Description**
Complex prompts should be externalized for versioning
### **Severity**
info
### **Pattern**
content\s*:\s*`[^`]{500,}`|content\s*:\s*"[^"]{500,}"
### **File Patterns**
  - **/*.ts
  - **/*.js
### **Exclude Patterns**
  - **/prompts/**
  - **/templates/**
### **Message**
Long prompt hardcoded in source. Consider externalizing for easier versioning.
### **Fix Hint**
Move prompts to /prompts directory or prompt management system

## LLM output without content filtering

### **Id**
no-content-filtering
### **Description**
User-facing LLM output should be filtered for safety
### **Severity**
warning
### **Pattern**
message\.content|completion\.text
### **Negative Pattern**
filter|moderate|safety|sanitize|check
### **File Patterns**
  - **/api/**/*.ts
  - **/chat/**/*.ts
### **Message**
LLM output returned without apparent content filtering. Add safety checks.
### **Fix Hint**
Add content moderation before displaying to users