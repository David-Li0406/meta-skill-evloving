# Voice Agents - Validations

## Missing Latency Measurement

### **Id**
no-latency-tracking
### **Severity**
error
### **Description**
Voice agents must track latency at each stage
### **Pattern**
  (deepgram|whisper|elevenlabs|realtime)
  
### **Anti Pattern**
  (timestamp|latency|duration|timing|metrics)
  
### **Message**
Voice pipeline without latency tracking. Add timestamps at each stage to measure performance.
### **Autofix**


## Using Batch STT Instead of Streaming

### **Id**
no-streaming-stt
### **Severity**
warning
### **Description**
Streaming STT reduces latency significantly
### **Pattern**
  (transcribe|createTranscription).*audio.*file|whisper.*transcribe
  
### **Anti Pattern**
  stream|live|realtime
  
### **Message**
Using batch transcription. Consider streaming for lower latency in voice agents.
### **Autofix**


## TTS Without Streaming Output

### **Id**
no-streaming-tts
### **Severity**
warning
### **Description**
Streaming TTS reduces time to first audio
### **Pattern**
  textToSpeech|speech\.create|generateSpeech
  
### **Anti Pattern**
  stream|chunk|buffer
  
### **Message**
TTS without streaming. Stream audio to reduce time to first audio.
### **Autofix**


## Hardcoded VAD Silence Threshold

### **Id**
fixed-vad-threshold
### **Severity**
warning
### **Description**
Fixed silence thresholds don't adapt to conversation
### **Pattern**
  silence_duration.*=.*\d+|timeout.*=.*\d+.*ms
  
### **Message**
Fixed silence threshold. Consider semantic VAD or adaptive thresholds for better turn-taking.
### **Autofix**


## Missing Barge-In Handling

### **Id**
no-barge-in
### **Severity**
warning
### **Description**
Voice agents should stop when user interrupts
### **Pattern**
  (vad|speech_start)
  
### **Anti Pattern**
  (stop|abort|interrupt|barge|cancel.*playing)
  
### **Message**
VAD without barge-in handling. Stop TTS when user starts speaking.
### **Autofix**


## Voice Prompt Without Length Constraints

### **Id**
no-voice-prompt-constraints
### **Severity**
warning
### **Description**
Voice prompts should constrain response length
### **Pattern**
  (system|prompt).*voice|voice.*(system|prompt)
  
### **Anti Pattern**
  (concise|short|brief|under.*words|max.*words)
  
### **Message**
Voice prompt without length constraints. Add 'Keep responses under 30 words' to system prompt.
### **Autofix**


## Markdown Formatting Sent to TTS

### **Id**
markdown-in-tts
### **Severity**
warning
### **Description**
Markdown will be read literally by TTS
### **Pattern**
  textToSpeech|speech\.create
  
### **Anti Pattern**
  (replace|sanitize|clean|strip).*markdown
  
### **Message**
Check for markdown in TTS input. Strip formatting before sending to TTS.
### **Autofix**


## STT Without Error Handling

### **Id**
no-stt-error-handling
### **Severity**
warning
### **Description**
STT can fail or return low confidence
### **Pattern**
  (transcript|transcription)
  
### **Anti Pattern**
  (confidence|error|try|catch|fallback)
  
### **Message**
STT without error handling. Check confidence scores and handle failures.
### **Autofix**


## WebSocket Without Reconnection

### **Id**
no-reconnection-logic
### **Severity**
warning
### **Description**
Realtime APIs need reconnection handling
### **Pattern**
  (WebSocket|realtime|RealtimeClient)
  
### **Anti Pattern**
  (reconnect|retry|onclose|onerror)
  
### **Message**
Realtime connection without reconnection logic. Handle disconnects gracefully.
### **Autofix**


## Missing Noise Handling

### **Id**
no-noise-handling
### **Severity**
info
### **Description**
Real-world audio includes background noise
### **Pattern**
  (vad|transcription|stt)
  
### **Anti Pattern**
  (noise|ambient|threshold|filter)
  
### **Message**
Consider adding noise handling for real-world audio quality.
### **Autofix**


## Missing Echo Cancellation

### **Id**
no-echo-cancellation
### **Severity**
info
### **Description**
Agent's voice may be captured by user's mic
### **Pattern**
  (tts.*stt|stt.*tts|voice.*agent)
  
### **Anti Pattern**
  (echo|aec|cancell)
  
### **Message**
Consider echo cancellation to prevent agent voice from triggering STT.
### **Autofix**
