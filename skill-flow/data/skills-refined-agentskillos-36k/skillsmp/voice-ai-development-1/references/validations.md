# Voice Ai Development - Validations

## Non-Streaming TTS

### **Id**
no-streaming-tts
### **Severity**
high
### **Type**
regex
### **Pattern**
await.*tts\.(synthesize|convert)\([^)]*\)
### **Negative Pattern**
stream|async for
### **Message**
Non-streaming TTS adds significant latency.
### **Fix Action**
Use tts.synthesize_stream() or tts.convert_as_stream()
### **Applies To**
  - *.py

## Hardcoded Sample Rate

### **Id**
hardcoded-sample-rate
### **Severity**
medium
### **Type**
regex
### **Pattern**
sample_rate\s*=\s*\d{4,5}
### **Message**
Hardcoded sample rate may cause format mismatches.
### **Fix Action**
Define sample rates as constants, document expected formats
### **Applies To**
  - *.py

## WebSocket Without Reconnection

### **Id**
no-reconnection-logic
### **Severity**
high
### **Type**
regex
### **Pattern**
websockets\.connect\(
### **Negative Pattern**
while.*True|reconnect|retry
### **Message**
WebSocket connections need reconnection logic.
### **Fix Action**
Add retry loop with exponential backoff
### **Applies To**
  - *.py

## Missing VAD Configuration

### **Id**
no-vad-configuration
### **Severity**
medium
### **Type**
regex
### **Pattern**
turn_detection
### **Negative Pattern**
threshold|silence_duration
### **Message**
VAD needs tuning for good user experience.
### **Fix Action**
Configure threshold and silence_duration_ms
### **Applies To**
  - *.py

## Blocking Audio Processing

### **Id**
blocking-audio-processing
### **Severity**
high
### **Type**
regex
### **Pattern**
def process_audio|def transcribe
### **Negative Pattern**
async def
### **Message**
Audio processing should be async to avoid blocking.
### **Fix Action**
Use async def and await for audio operations
### **Applies To**
  - *.py

## Missing Interruption Handling

### **Id**
no-interruption-handling
### **Severity**
medium
### **Type**
regex
### **Pattern**
is_speaking|speaking
### **Negative Pattern**
interrupt|cancel|stop_speaking
### **Message**
Voice agents should handle user interruptions.
### **Fix Action**
Add barge-in detection and cancel current response
### **Applies To**
  - *.py

## Audio Queue Without Clear

### **Id**
audio-queue-no-clear
### **Severity**
low
### **Type**
regex
### **Pattern**
audio_queue|Queue\(\)
### **Negative Pattern**
clear|empty|get_nowait
### **Message**
Audio queues should be clearable for interruptions.
### **Fix Action**
Add method to clear queue on interruption
### **Applies To**
  - *.py

## WebSocket Without Error Handling

### **Id**
no-error-handling-websocket
### **Severity**
high
### **Type**
regex
### **Pattern**
await ws\.(send|recv)
### **Negative Pattern**
try:|except|ConnectionClosed
### **Message**
WebSocket operations need error handling.
### **Fix Action**
Wrap in try/except for ConnectionClosed
### **Applies To**
  - *.py