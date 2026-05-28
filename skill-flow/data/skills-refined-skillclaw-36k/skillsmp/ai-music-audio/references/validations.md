# Ai Music Audio - Validations

## Audio API Key in Client Code

### **Id**
audio-api-key-exposed
### **Severity**
error
### **Description**
Audio generation API keys must be server-side only
### **Pattern**
  (NEXT_PUBLIC|REACT_APP|VITE).*(ELEVENLABS|REPLICATE|FAL|OPENAI).*KEY
  
### **Message**
Audio API key exposed to client. Use server-side routes only.
### **Autofix**


## Hardcoded Audio API Key

### **Id**
hardcoded-audio-api-key
### **Severity**
error
### **Description**
API keys should use environment variables
### **Pattern**
  (xi-|sk-|r8_|fal_)[A-Za-z0-9]{20,}
  
### **Message**
Hardcoded API key detected. Use environment variables.
### **Autofix**


## Missing TTS Content Moderation

### **Id**
no-tts-moderation
### **Severity**
error
### **Description**
Text must be moderated before speech synthesis
### **Pattern**
  textToSpeech\(.*(?:req|request|user)\.(?:body|query)(?!.*moderat)
  
### **Message**
User text passed to TTS without moderation. Add content check.
### **Autofix**


## Voice Cloning Without Consent Check

### **Id**
voice-clone-no-consent
### **Severity**
error
### **Description**
Voice cloning requires verified consent
### **Pattern**
  createVoiceClone|add.*voice|clone.*voice(?!.*consent|verify|permission)
  
### **Message**
Voice cloning without consent verification. Implement consent flow.
### **Autofix**


## Missing Deepfake Prevention

### **Id**
no-deepfake-prevention
### **Severity**
warning
### **Description**
Check for impersonation attempts in TTS requests
### **Pattern**
  textToSpeech.*(?:as|voice.*of|impersonate).*(?:president|ceo|celebrity)
  
### **Message**
Potential impersonation content. Add impersonation detection.
### **Autofix**


## TTS Without Rate Limiting

### **Id**
no-tts-rate-limiting
### **Severity**
warning
### **Description**
TTS endpoints should be rate limited
### **Pattern**
  async.*textToSpeech.*request(?!.*rateLimit|limit)
  
### **Message**
TTS endpoint without rate limiting.
### **Autofix**


## TTS Without Character Limit

### **Id**
no-character-limit
### **Severity**
warning
### **Description**
Text length should be limited to prevent cost abuse
### **Pattern**
  textToSpeech\(.*text(?!.*length.*<|slice|substring|limit)
  
### **Message**
TTS without text length limit. Add maximum character check.
### **Autofix**


## Missing Audio Cost Tracking

### **Id**
no-audio-cost-tracking
### **Severity**
warning
### **Description**
Audio generation costs should be tracked per user
### **Pattern**
  (textToSpeech|generateMusic)\((?!.*cost|credits|budget)
  
### **Message**
No cost tracking for audio generation. Add usage tracking.
### **Autofix**


## Unbounded Music Duration

### **Id**
unbounded-music-duration
### **Severity**
warning
### **Description**
Music duration should be capped
### **Pattern**
  duration.*request\.(body|query)(?!.*Math\.min|clamp|max)
  
### **Message**
User-controlled duration without limit. Cap at maximum allowed.
### **Autofix**


## Missing Sample Rate Normalization

### **Id**
no-sample-rate-normalization
### **Severity**
warning
### **Description**
Audio should be normalized before mixing/concatenation
### **Pattern**
  concat.*audio|merge.*audio(?!.*resample|normalize|rate)
  
### **Message**
Audio concatenation without sample rate normalization.
### **Autofix**


## Missing Audio Format Validation

### **Id**
no-audio-format-validation
### **Severity**
warning
### **Description**
Uploaded audio should be validated
### **Pattern**
  upload.*audio|audio.*file(?!.*validate|check|format)
  
### **Message**
Audio upload without format validation.
### **Autofix**


## Audio Stream Not Properly Closed

### **Id**
stream-not-closed
### **Severity**
warning
### **Description**
Audio streams should be properly closed
### **Pattern**
  convertAsStream\((?!.*finally|close|destroy)
  
### **Message**
Audio stream without proper cleanup. Add finally block.
### **Autofix**


## Streaming Without Timeout

### **Id**
no-stream-timeout
### **Severity**
warning
### **Description**
Audio streams should have timeouts
### **Pattern**
  Stream.*audio(?!.*timeout|AbortController)
  
### **Message**
Audio streaming without timeout. Add timeout handling.
### **Autofix**


## Missing Audio Watermark

### **Id**
no-audio-watermark
### **Severity**
warning
### **Description**
AI-generated audio should be watermarked
### **Pattern**
  generate.*audio.*return(?!.*watermark|seal|c2pa)
  
### **Message**
AI audio returned without watermark. Add AudioSeal or similar.
### **Autofix**
