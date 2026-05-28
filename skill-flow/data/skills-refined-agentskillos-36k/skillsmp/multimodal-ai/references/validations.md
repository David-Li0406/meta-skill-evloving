# Multimodal Ai - Validations

## No Image Format Validation

### **Id**
no-image-format-check
### **Severity**
error
### **Description**
Validate image format before sending to API
### **Pattern**
  image_url.*url(?!.*format.*check|valid|jpg|png|webp)
  
### **Message**
Validate image format (JPEG, PNG, WebP, GIF) before API call.
### **Autofix**


## No Image Token Estimation

### **Id**
no-token-estimation
### **Severity**
warning
### **Description**
Estimate image tokens for cost management
### **Pattern**
  image_url.*detail.*high(?!.*token|estimate|cost)
  
### **Message**
Estimate image tokens before sending high-detail images.
### **Autofix**


## High Detail for Simple Tasks

### **Id**
high-detail-unnecessary
### **Severity**
info
### **Description**
Low detail often sufficient for descriptions
### **Pattern**
  detail.*high.*describe|summarize.*detail.*high
  
### **Message**
Consider 'low' detail for simple descriptions to save tokens.
### **Autofix**


## No Audio Format Validation

### **Id**
no-audio-format-check
### **Severity**
error
### **Description**
Check audio format before transcription
### **Pattern**
  transcriptions\.create(?!.*format|check|mp3|wav)
  
### **Message**
Validate audio format before sending to Whisper.
### **Autofix**


## No Audio Preprocessing

### **Id**
no-audio-normalization
### **Severity**
warning
### **Description**
Normalize audio for better transcription
### **Pattern**
  transcriptions\.create(?!.*normalize|process|ffmpeg)
  
### **Message**
Consider normalizing audio for better transcription quality.
### **Autofix**


## Large Audio File

### **Id**
large-audio-file
### **Severity**
warning
### **Description**
Audio files over 25MB need splitting
### **Pattern**
  transcriptions\.create(?!.*size.*check|split|chunk)
  
### **Message**
Check audio file size (max 25MB) and split if needed.
### **Autofix**


## No Multimodal Context Tracking

### **Id**
no-context-tracking
### **Severity**
warning
### **Description**
Track token usage across modalities
### **Pattern**
  image_url.*image_url(?!.*context|token.*track)
  
### **Message**
Track cumulative token usage when using multiple images.
### **Autofix**


## Too Many Images in Context

### **Id**
images-fill-context
### **Severity**
error
### **Description**
Multiple high-res images can fill context
### **Pattern**
  images\.map.*image_url(?!.*limit|max|budget)
  
### **Message**
Limit number of images to prevent context overflow.
### **Autofix**


## No Vision Error Handling

### **Id**
no-vision-error-handling
### **Severity**
error
### **Description**
Handle vision API errors gracefully
### **Pattern**
  image_url(?!.*catch|try|error)
  
### **Message**
Handle vision API errors (invalid images, rate limits).
### **Autofix**


## No Transcription Fallback

### **Id**
no-transcription-fallback
### **Severity**
warning
### **Description**
Have fallback for transcription failures
### **Pattern**
  transcriptions\.create(?!.*catch|fallback|retry)
  
### **Message**
Add fallback handling for transcription failures.
### **Autofix**


## Sequential Multimodal Processing

### **Id**
sequential-multimodal
### **Severity**
info
### **Description**
Process modalities in parallel when possible
### **Pattern**
  await.*image.*await.*audio(?!.*Promise\.all|parallel)
  
### **Message**
Process images and audio in parallel to reduce latency.
### **Autofix**


## No Image Description Caching

### **Id**
no-image-caching
### **Severity**
info
### **Description**
Cache repeated image analyses
### **Pattern**
  image_url.*same.*image(?!.*cache|memo)
  
### **Message**
Cache image descriptions to avoid reprocessing.
### **Autofix**
