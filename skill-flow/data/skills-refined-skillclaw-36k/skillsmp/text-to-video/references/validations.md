# Text To Video - Validations

## Video API Key in Client Code

### **Id**
video-api-key-exposed
### **Severity**
error
### **Description**
Video generation API keys must be server-side only
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*(RUNWAY|LUMA|KLING|REPLICATE|PIKA).*KEY
  
### **Message**
Video API key exposed to client. Use server-side routes only.
### **Autofix**


## Hardcoded Video API Key

### **Id**
hardcoded-video-api-key
### **Severity**
error
### **Description**
API keys should use environment variables
### **Pattern**
  (runway_|luma_|r8_|kling_)[A-Za-z0-9]{20,}
  
### **Message**
Hardcoded API key detected. Use environment variables.
### **Autofix**


## Missing Video Prompt Moderation

### **Id**
no-video-prompt-moderation
### **Severity**
error
### **Description**
Video prompts must be moderated before generation
### **Pattern**
  request\.(body|query)\.prompt.*generateVideo(?!.*moderat)
  
### **Message**
Video prompt passed without moderation. Check for policy violations.
### **Autofix**


## Missing Video Output Moderation

### **Id**
no-video-output-moderation
### **Severity**
warning
### **Description**
Generated videos should be checked before serving
### **Pattern**
  generateVideo\(.*\).*return.*url(?!.*check|scan)
  
### **Message**
Generated video returned without content moderation.
### **Autofix**


## Video Safety Checker Disabled

### **Id**
video-safety-disabled
### **Severity**
warning
### **Description**
Model safety checkers should remain enabled
### **Pattern**
  safety_checker.*false|nsfw_filter.*false|content_filter.*disabled
  
### **Message**
Video safety checker disabled. Enable for production.
### **Autofix**


## Video Generation Without Rate Limiting

### **Id**
no-video-rate-limiting
### **Severity**
warning
### **Description**
Video generation is expensive - rate limiting required
### **Pattern**
  async.*generateVideo.*request(?!.*rateLimit|limit)
  
### **Message**
Video generation endpoint without rate limiting.
### **Autofix**


## Missing Timeout for Video Generation

### **Id**
no-video-timeout
### **Severity**
error
### **Description**
Video generation can take minutes - timeout required
### **Pattern**
  await.*generate.*video(?!.*timeout)
  
### **Message**
Video generation without timeout. Add 5-10 minute timeout.
### **Autofix**


## Blocking Video Generation

### **Id**
synchronous-video-generation
### **Severity**
error
### **Description**
Video generation should be async with status polling
### **Pattern**
  await.*generateVideo\((?!.*queue|poll|async|webhook)
  
### **Message**
Synchronous video generation blocks requests. Use async pattern.
### **Autofix**


## Missing Video Cost Tracking

### **Id**
no-video-cost-tracking
### **Severity**
warning
### **Description**
Video generation costs should be tracked
### **Pattern**
  generateVideo\((?!.*cost|budget|credits)
  
### **Message**
No cost tracking for video generation. Add budget controls.
### **Autofix**


## Unbounded Video Duration

### **Id**
unbounded-video-duration
### **Severity**
warning
### **Description**
Video duration should be capped to control costs
### **Pattern**
  duration.*request\.(body|query)(?!.*Math\.min|clamp|max)
  
### **Message**
User-controlled duration without limit. Cap at maximum allowed.
### **Autofix**


## Invalid Video Resolution

### **Id**
invalid-video-resolution
### **Severity**
warning
### **Description**
Video dimensions must match model requirements
### **Pattern**
  generateVideo\(.*width.*(?!.*512|576|640|704|768|832|896|960|1024|1280)
  
### **Message**
Check resolution compatibility with model requirements.
### **Autofix**


## Invalid Aspect Ratio

### **Id**
invalid-aspect-ratio
### **Severity**
warning
### **Description**
Aspect ratio must match model capabilities
### **Pattern**
  aspect_ratio.*[0-9]+:[0-9]+(?!.*16:9|9:16|1:1|4:3|3:4)
  
### **Message**
Non-standard aspect ratio may cause issues. Use 16:9, 9:16, or 1:1.
### **Autofix**


## Missing Input Image Validation

### **Id**
no-input-image-validation
### **Severity**
warning
### **Description**
Image-to-video inputs should be validated
### **Pattern**
  imageToVideo\(.*image(?!.*validate|check|resize)
  
### **Message**
Input image not validated. Check format, size, and dimensions.
### **Autofix**


## Missing Retry Logic

### **Id**
no-generation-retry
### **Severity**
warning
### **Description**
Video generation should retry on transient failures
### **Pattern**
  await.*generateVideo\((?!.*retry|attempts)
  
### **Message**
No retry logic for video generation failures.
### **Autofix**


## Missing Queue Failure Handling

### **Id**
no-queue-failure-handling
### **Severity**
warning
### **Description**
Video generation queues should handle failures
### **Pattern**
  queue\.add\(.*video(?!.*onFail|deadLetter)
  
### **Message**
Video queue without failure handling. Add dead letter queue.
### **Autofix**
