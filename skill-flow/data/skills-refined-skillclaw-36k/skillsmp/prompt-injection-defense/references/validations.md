# Prompt Injection Defense - Validations

## Missing Input Sanitization

### **Id**
no-input-sanitization
### **Severity**
critical
### **Type**
regex
### **Pattern**
messages\.create\s*\(\{[^}]*content:\s*(?:req|user|input|body)\.
### **Negative Pattern**
sanitize|validate|filter|escape|detect
### **Message**
User input passed directly to LLM without sanitization.
### **Fix Action**
Add input validation: await detector.detect(userInput)
### **Applies To**
  - *.ts
  - *.js
  - *.py

## RAG Content Without Sanitization

### **Id**
rag-no-sanitization
### **Severity**
critical
### **Type**
regex
### **Pattern**
retrieve|search\s*\([^)]+\)[^;]*(?:content|text|messages)
### **Negative Pattern**
sanitize|filter|isolate|validate
### **Message**
Retrieved content passed to LLM without sanitization.
### **Fix Action**
Sanitize retrieved documents before including in context
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Verbose Injection Detection Error

### **Id**
verbose-injection-error
### **Severity**
medium
### **Type**
regex
### **Pattern**
(?:throw|return|send)\s*[^;]*(?:injection|blocked|detected)[^;]*pattern|reason|details
### **Message**
Error messages reveal injection detection details to attacker.
### **Fix Action**
Return generic error: 'Request could not be processed'
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Single Layer Injection Defense

### **Id**
single-layer-defense
### **Severity**
medium
### **Type**
regex
### **Pattern**
if\s*\([^)]*(?:includes|match|test)\s*\([^)]*ignore.*instruction
### **Negative Pattern**
semantic|behavioral|monitor|layer|multi
### **Message**
Single pattern-based injection check. Easily bypassed.
### **Fix Action**
Implement multi-layer defense with semantic analysis and output monitoring
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Missing Output Behavior Monitoring

### **Id**
no-output-monitoring
### **Severity**
medium
### **Type**
regex
### **Pattern**
response\.content|message\.content|completion\.text
### **Negative Pattern**
monitor|analyze|check|validate.*output|suspicious
### **Message**
LLM output used without behavior monitoring.
### **Fix Action**
Monitor output for signs of successful injection
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Tool Calls Without Validation

### **Id**
tool-no-validation
### **Severity**
critical
### **Type**
regex
### **Pattern**
tool_calls|function_call|toolCalls
### **Negative Pattern**
validate|allow|check|verify|permission
### **Message**
Tool calls executed without validation.
### **Fix Action**
Validate tool calls against allowed list and check arguments
### **Applies To**
  - *.ts
  - *.js
  - *.py

## System Prompt Exposure Risk

### **Id**
system-prompt-in-output
### **Severity**
high
### **Type**
regex
### **Pattern**
system.*prompt|SYSTEM_PROMPT|systemPrompt
### **Negative Pattern**
private|secret|hidden|redact|mask
### **Message**
System prompt may be extractable via prompt injection.
### **Fix Action**
Mark system prompt as sensitive, monitor for leakage
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Multi-Turn Context Analysis

### **Id**
no-conversation-context-check
### **Severity**
medium
### **Type**
regex
### **Pattern**
messages\.push|addMessage|appendMessage
### **Negative Pattern**
analyze.*conversation|multi.*turn|session.*check|cumulative
### **Message**
Messages added without multi-turn injection analysis.
### **Fix Action**
Analyze full conversation context, not just latest message
### **Applies To**
  - *.ts
  - *.js
  - *.py

## External Content Without Isolation

### **Id**
external-content-no-isolation
### **Severity**
high
### **Type**
regex
### **Pattern**
(?:fetch|axios|request|http)\s*\([^)]+\)[^;]*(?:content|text|body)[^;]*messages
### **Negative Pattern**
isolate|boundary|external.*content|untrusted
### **Message**
External content added to context without isolation markers.
### **Fix Action**
Wrap external content with clear boundaries and untrusted labels
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Encoded Injection Detection

### **Id**
no-encoding-check
### **Severity**
medium
### **Type**
regex
### **Pattern**
detect.*injection|injection.*detect
### **Negative Pattern**
base64|encode|decode|unicode|homoglyph
### **Message**
Injection detection doesn't check for encoded payloads.
### **Fix Action**
Add checks for Base64, URL encoding, Unicode homoglyphs
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Unlimited Tool Access

### **Id**
unlimited-tool-access
### **Severity**
critical
### **Type**
regex
### **Pattern**
tools:\s*(?:ALL_TOOLS|allTools|tools)
### **Negative Pattern**
filter|allow|limit|restrict|subset
### **Message**
LLM has access to all tools without restriction.
### **Fix Action**
Limit tools to minimum required for task
### **Applies To**
  - *.ts
  - *.js
  - *.py