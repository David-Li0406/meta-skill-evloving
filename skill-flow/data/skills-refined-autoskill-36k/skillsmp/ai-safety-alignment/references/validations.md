# Ai Safety Alignment - Validations

## LLM Call Without Input Validation

### **Id**
no-input-validation
### **Severity**
error
### **Description**
User input must be validated before passing to LLM
### **Pattern**
  chat\.completions\.create\((?!.*validate|sanitize|check)
  
### **Message**
LLM call without input validation. Add safety checks before sending to model.
### **Autofix**


## Raw User Input to System Prompt

### **Id**
raw-user-input
### **Severity**
error
### **Description**
User input interpolated directly into system prompt enables injection
### **Pattern**
  system.*`\$\{.*user|input|query
  
### **Message**
User input in system prompt enables injection. Use separate user message.
### **Autofix**


## No Moderation API Call

### **Id**
no-moderation
### **Severity**
warning
### **Description**
Use moderation API for content safety
### **Pattern**
  chat\.completions\.create(?!.*moderation|moderate)
  
### **Message**
Consider adding OpenAI Moderation API for content safety.
### **Autofix**


## No Output Filtering

### **Id**
no-output-filtering
### **Severity**
warning
### **Description**
LLM output should be checked before returning to user
### **Pattern**
  return.*response\.choices\[0\](?!.*filter|sanitize|validate)
  
### **Message**
LLM output returned without filtering. Add output safety checks.
### **Autofix**


## Unescaped LLM Output in HTML

### **Id**
unescaped-output
### **Severity**
error
### **Description**
LLM output may contain XSS if rendered as HTML
### **Pattern**
  dangerouslySetInnerHTML.*response|innerHTML.*completion
  
### **Message**
LLM output rendered as HTML without escaping. Sanitize with DOMPurify.
### **Autofix**


## No Prompt Injection Detection

### **Id**
no-injection-detection
### **Severity**
warning
### **Description**
Implement prompt injection detection for user-facing LLM apps
### **Pattern**
  messages\.push\(\{.*role.*user.*content.*\$\{(?!.*detectInjection|validatePrompt)
  
### **Message**
User messages need prompt injection detection before LLM call.
### **Autofix**


## Unsanitized RAG Context

### **Id**
unsanitized-context
### **Severity**
warning
### **Description**
Retrieved context may contain injection attacks
### **Pattern**
  retrieve.*chunks.*messages\.push(?!.*sanitize|validate)
  
### **Message**
Retrieved context should be sanitized before adding to messages.
### **Autofix**


## No PII Detection

### **Id**
no-pii-detection
### **Severity**
warning
### **Description**
User input may contain PII that should be redacted
### **Pattern**
  trace.*input|log.*prompt(?!.*sanitize|redact|pii)
  
### **Message**
PII may be logged or traced. Add PII detection and redaction.
### **Autofix**


## PII Sent to LLM Without Redaction

### **Id**
pii-in-llm-call
### **Severity**
warning
### **Description**
Consider redacting PII before sending to third-party LLM
### **Pattern**
  create\(.*messages.*user(?!.*redact|anonymize)
  
### **Message**
Consider PII redaction before sending to external LLM providers.
### **Autofix**


## Safety Check Without Rate Limiting

### **Id**
no-safety-rate-limit
### **Severity**
warning
### **Description**
Rate limit safety checks to prevent abuse
### **Pattern**
  validateInput|detectInjection(?!.*rateLimit|throttle)
  
### **Message**
Safety checks should be rate-limited to prevent probe attacks.
### **Autofix**


## No Violation Tracking

### **Id**
no-violation-tracking
### **Severity**
info
### **Description**
Track safety violations per user for escalation
### **Pattern**
  blocked.*true(?!.*violation|track|increment)
  
### **Message**
Track violations per user for escalating blocks.
### **Autofix**


## Safety Error Exposes Details

### **Id**
safety-error-exposes
### **Severity**
warning
### **Description**
Safety check errors should not expose detection logic
### **Pattern**
  catch.*error.*reason|message.*injection.*detected
  
### **Message**
Safety errors should be generic to not help attackers.
### **Autofix**


## Safety Check Fails Open

### **Id**
safety-fail-open
### **Severity**
error
### **Description**
Safety checks must fail closed (block on error)
### **Pattern**
  catch.*return.*true|catch.*allowed.*true
  
### **Message**
Safety check fails open. Should block on error (fail closed).
### **Autofix**


## Hardcoded Blocklist

### **Id**
hardcoded-blocklist
### **Severity**
info
### **Description**
Safety patterns should be configurable
### **Pattern**
  const.*BLOCKED_WORDS.*=.*\[
  
### **Message**
Safety blocklists should be configurable for updates.
### **Autofix**


## No Guardrail Action Logging

### **Id**
no-guardrail-logging
### **Severity**
warning
### **Description**
Log safety actions for audit and improvement
### **Pattern**
  blocked.*true(?!.*log|audit|track)
  
### **Message**
Log safety blocks for audit trail and model improvement.
### **Autofix**
