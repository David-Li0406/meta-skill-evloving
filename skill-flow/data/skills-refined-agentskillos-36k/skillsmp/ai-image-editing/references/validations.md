# Ai Image Editing - Validations

## API Key in Client Code

### **Id**
api-key-exposed
### **Severity**
error
### **Description**
Image generation API keys should only be server-side
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*(REPLICATE|STABILITY|FAL|OPENAI).*KEY
  
### **Message**
API key exposed to client. Use server-side only.
### **Autofix**


## Hardcoded API Key

### **Id**
hardcoded-api-key
### **Severity**
error
### **Description**
API keys should use environment variables
### **Pattern**
  (r8_|sk-|fal-)[A-Za-z0-9]{20,}
  
### **Message**
Hardcoded API key. Use environment variables.
### **Autofix**


## Missing Prompt Moderation

### **Id**
no-prompt-moderation
### **Severity**
error
### **Description**
User prompts should be checked before generation
### **Pattern**
  request\.(body|query)\.prompt.*generate(?!.*moderat)
  
### **Message**
User prompt passed to generation without moderation check.
### **Autofix**


## Missing Output Moderation

### **Id**
no-output-moderation
### **Severity**
warning
### **Description**
Generated images should be checked before serving
### **Pattern**
  generate\(.*\).*return.*url(?!.*check)
  
### **Message**
Generated image returned without content check.
### **Autofix**


## Safety Checker Explicitly Disabled

### **Id**
safety-checker-disabled
### **Severity**
warning
### **Description**
Model safety checkers should remain enabled
### **Pattern**
  safety_checker.*false|enable_safety_checker.*false
  
### **Message**
Safety checker disabled. Enable for production.
### **Autofix**


## Generation Without Rate Limiting

### **Id**
no-rate-limiting
### **Severity**
warning
### **Description**
API calls should be rate limited to prevent abuse
### **Pattern**
  async.*generate.*request(?!.*rateLimit|limit)
  
### **Message**
Generation endpoint without rate limiting.
### **Autofix**


## Unbounded Generation Loop

### **Id**
unbounded-generation-loop
### **Severity**
error
### **Description**
Loops generating images should have limits
### **Pattern**
  while.*True.*generate|for.*range\(.*\).*generate(?!.*limit)
  
### **Message**
Unbounded generation loop. Add limits and rate control.
### **Autofix**


## Missing Cost Tracking

### **Id**
no-cost-tracking
### **Severity**
warning
### **Description**
Image generation costs should be tracked
### **Pattern**
  generate\((?!.*cost|budget)
  
### **Message**
No cost tracking for generation. Add budget controls.
### **Autofix**


## Missing Resolution Validation

### **Id**
no-resolution-validation
### **Severity**
warning
### **Description**
Image dimensions should be validated for model compatibility
### **Pattern**
  generate\(.*image.*(?!.*resize|divisible|resolution)
  
### **Message**
Image passed without resolution validation. Ensure dimensions divisible by 8.
### **Autofix**


## Mask Not Validated

### **Id**
mask-not-validated
### **Severity**
warning
### **Description**
Inpainting masks should be validated before use
### **Pattern**
  inpaint\(.*mask(?!.*validate|check)
  
### **Message**
Mask used without validation. Check dimensions and values.
### **Autofix**


## Missing Error Handling for Generation

### **Id**
no-generation-error-handling
### **Severity**
warning
### **Description**
API calls should handle failures gracefully
### **Pattern**
  await.*generate\((?!.*try|catch|\.catch)
  
### **Message**
Generation call without error handling.
### **Autofix**


## Missing Timeout for Long Generation

### **Id**
no-timeout-handling
### **Severity**
warning
### **Description**
Long-running generations should have timeouts
### **Pattern**
  generate\((?!.*timeout).*resolution.*2048
  
### **Message**
High-resolution generation without timeout.
### **Autofix**
