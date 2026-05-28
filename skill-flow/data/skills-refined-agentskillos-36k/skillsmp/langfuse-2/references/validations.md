# Langfuse - Validations

## Missing Langfuse Flush

### **Id**
no-flush
### **Severity**
high
### **Type**
regex
### **Pattern**
langfuse\.trace\(
### **Negative Pattern**
langfuse\.flush\(\)|@observe
### **Message**
Langfuse traces may be lost without flush() call.
### **Fix Action**
Add langfuse.flush() before script/function exit
### **Applies To**
  - *.py

## Trace Without User ID

### **Id**
no-user-id
### **Severity**
medium
### **Type**
regex
### **Pattern**
langfuse\.trace\([^)]*\)
### **Negative Pattern**
user_id=
### **Message**
Traces should include user_id for better analytics.
### **Fix Action**
Add user_id parameter to trace()
### **Applies To**
  - *.py

## Dynamic Trace Name

### **Id**
dynamic-trace-name
### **Severity**
medium
### **Type**
regex
### **Pattern**
name=f"[^"]*\{[^"]*\}"
### **Message**
Dynamic trace names create high cardinality. Use metadata instead.
### **Fix Action**
Use static name and move variables to metadata parameter
### **Applies To**
  - *.py

## Generation Without Usage

### **Id**
no-usage-tracking
### **Severity**
medium
### **Type**
regex
### **Pattern**
generation\([^)]*\)
### **Negative Pattern**
usage=|from langfuse\.openai
### **Message**
Generation without usage data won't show costs.
### **Fix Action**
Add usage={input: X, output: Y} or use langfuse.openai wrapper
### **Applies To**
  - *.py

## Generation Without Model

### **Id**
no-generation-model
### **Severity**
low
### **Type**
regex
### **Pattern**
\.generation\([^)]*\)
### **Negative Pattern**
model=
### **Message**
Generation should specify model for proper cost calculation.
### **Fix Action**
Add model parameter to generation()
### **Applies To**
  - *.py

## Span Without End

### **Id**
no-end-call
### **Severity**
high
### **Type**
regex
### **Pattern**
\.generation\(|\.span\(
### **Negative Pattern**
\.end\(\)|@observe
### **Message**
Spans should be ended to record duration.
### **Fix Action**
Call span.end() or generation.end() when complete
### **Applies To**
  - *.py

## Hardcoded Langfuse Keys

### **Id**
hardcoded-keys
### **Severity**
high
### **Type**
regex
### **Pattern**
(public_key|secret_key)=["']pk-|sk-
### **Message**
API keys should not be hardcoded. Use environment variables.
### **Fix Action**
Use LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY env vars
### **Applies To**
  - *.py

## No Auth Check

### **Id**
no-auth-check
### **Severity**
low
### **Type**
regex
### **Pattern**
Langfuse\(\)
### **Negative Pattern**
auth_check
### **Message**
Consider checking Langfuse auth on startup.
### **Fix Action**
Add langfuse.auth_check() to verify connection
### **Applies To**
  - *.py