# Structured Output - Validations

## JSON Mode Without Prompt Mention

### **Id**
json-mode-no-prompt
### **Severity**
high
### **Type**
regex
### **Pattern**
response_format.*json_object
### **Negative Pattern**
[Jj][Ss][Oo][Nn].*[Rr]espond|[Rr]espond.*[Jj][Ss][Oo][Nn]|format.*[Jj][Ss][Oo][Nn]
### **Message**
OpenAI JSON mode requires mentioning JSON in the prompt.
### **Fix Action**
Add 'Respond in JSON format' to system or user message
### **Applies To**
  - *.py

## JSON Parse Without Validation

### **Id**
no-response-validation
### **Severity**
medium
### **Type**
regex
### **Pattern**
json\.loads\([^)]*\.content
### **Negative Pattern**
model_validate|try:|except
### **Message**
Parsing JSON without Pydantic validation is risky.
### **Fix Action**
Use MyModel.model_validate_json() instead of json.loads()
### **Applies To**
  - *.py

## Instructor Without Retries

### **Id**
missing-max-retries
### **Severity**
medium
### **Type**
regex
### **Pattern**
response_model=\w+
### **Negative Pattern**
max_retries
### **Message**
Instructor extraction without max_retries may fail silently.
### **Fix Action**
Add max_retries=3 for production reliability
### **Applies To**
  - *.py

## Many Optional Fields

### **Id**
complex-optional-schema
### **Severity**
low
### **Type**
regex
### **Pattern**
Optional\[.*\]\s*=\s*None.*Optional\[.*\]\s*=\s*None.*Optional\[
### **Message**
Multiple optional fields increase extraction failure rate.
### **Fix Action**
Split into required and optional models, or use defaults
### **Applies To**
  - *.py

## Extraction Without Error Handling

### **Id**
no-error-handling-extraction
### **Severity**
high
### **Type**
regex
### **Pattern**
response_model=\w+[^}]*messages=
### **Negative Pattern**
try:|except|max_retries
### **Message**
Structured extraction can fail. Add error handling.
### **Fix Action**
Wrap in try/except or use max_retries parameter
### **Applies To**
  - *.py

## Direct Content Access on Anthropic Response

### **Id**
anthropic-direct-content-access
### **Severity**
high
### **Type**
regex
### **Pattern**
response\.content\[0\]\.input
### **Message**
Anthropic response may have TextBlock before ToolUseBlock.
### **Fix Action**
Iterate content blocks to find tool_use type
### **Applies To**
  - *.py

## Outlines Model Load in Function

### **Id**
outlines-model-in-function
### **Severity**
medium
### **Type**
regex
### **Pattern**
def \w+\([^)]*\):[^}]*outlines\.models\.
### **Message**
Loading Outlines model inside function causes slow calls.
### **Fix Action**
Load model at module level or in __init__
### **Applies To**
  - *.py

## Streaming With Strict Validation

### **Id**
streaming-with-validation
### **Severity**
medium
### **Type**
regex
### **Pattern**
stream=True.*@validator|@model_validator.*stream=True
### **Message**
Validators may fail on partial streaming data.
### **Fix Action**
Use instructor.Partial[] wrapper or skip validation during stream
### **Applies To**
  - *.py

## Hardcoded JSON Schema

### **Id**
hardcoded-schema-json
### **Severity**
low
### **Type**
regex
### **Pattern**
"type":\s*"object".*"properties":\s*\{
### **Message**
Hardcoded JSON schemas are hard to maintain.
### **Fix Action**
Use Pydantic model.model_json_schema() to generate
### **Applies To**
  - *.py