# Godot Llm Integration - Validations

## Separate Model Nodes Per NPC

### **Id**
godot-separate-model-nodes
### **Severity**
critical
### **Type**
regex
### **Pattern**
NobodyWhoModel|model_file.*=.*\.gguf
### **Message**
Each NobodyWhoModel loads model separately. Use shared model in autoload.
### **Fix Action**
Create one model in Global autoload, reference via chat.model_node = Global.model
### **Applies To**
  - *.gd
  - *.tscn

## Blocking Await in Process

### **Id**
godot-blocking-await
### **Severity**
critical
### **Type**
regex
### **Pattern**
func _process\([^)]*\):[^}]*await|func _physics_process\([^)]*\):[^}]*await.*chat
### **Message**
Awaiting LLM in _process blocks the game loop. Use signals instead.
### **Fix Action**
Connect to message_received signal, handle response in callback
### **Applies To**
  - *.gd

## Absolute Model Path

### **Id**
godot-absolute-model-path
### **Severity**
high
### **Type**
regex
### **Pattern**
model_file\s*=\s*["'][A-Za-z]:|model_path\s*=\s*["']/
### **Message**
Absolute path for model won't work in exports. Use res:// path.
### **Fix Action**
Place model in res://ai/models/ and use res:// path
### **Applies To**
  - *.gd

## No Signal Connection for Response

### **Id**
godot-no-signal-connection
### **Severity**
high
### **Type**
regex
### **Pattern**
\.say\(
### **Negative Pattern**
message_received\\.connect|completed\\.connect
### **Message**
Calling say() without connecting to response signal. Response will be lost.
### **Fix Action**
Connect to chat.message_received signal before calling say()
### **Applies To**
  - *.gd

## Model Loading in _ready Without Feedback

### **Id**
godot-model-in-ready
### **Severity**
high
### **Type**
regex
### **Pattern**
func _ready\(\):[^}]*NobodyWhoModel\.new\(\)
### **Negative Pattern**
loading|Loading|progress|Progress
### **Message**
Model loading in _ready freezes game without feedback.
### **Fix Action**
Load model during loading screen with progress indication
### **Applies To**
  - *.gd

## No Grammar Constraint for Structured Output

### **Id**
godot-no-grammar-for-actions
### **Severity**
warning
### **Type**
regex
### **Pattern**
JSON\.parse_string
### **Negative Pattern**
grammar|Grammar|GRAMMAR
### **Message**
Parsing JSON without grammar constraint. LLM may output invalid JSON.
### **Fix Action**
Use chat.grammar to guarantee valid JSON output
### **Applies To**
  - *.gd

## No Context Window Management

### **Id**
godot-no-context-management
### **Severity**
warning
### **Type**
regex
### **Pattern**
NobodyWhoChat|system_prompt
### **Negative Pattern**
context_shifting|context_size|get_context_length
### **Message**
No context management. Long conversations may lose early context.
### **Fix Action**
Enable context shifting or manually manage conversation history
### **Applies To**
  - *.gd

## LLM Code Without Platform Check

### **Id**
godot-mobile-without-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
NobodyWho|\.say\(|\.model_node
### **Negative Pattern**
OS\\.has_feature|mobile|Mobile|platform|Platform
### **Message**
LLM code without platform check. Mobile support is experimental.
### **Fix Action**
Add OS.has_feature() check and cloud API fallback for mobile
### **Applies To**
  - *.gd

## No Error Handling for LLM

### **Id**
godot-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
\.say\(
### **Negative Pattern**
error|Error|failed|Failed|catch
### **Message**
No error handling for LLM calls. What if model fails to load?
### **Fix Action**
Add error signal handling and fallback responses
### **Applies To**
  - *.gd

## No Visual Feedback During Generation

### **Id**
godot-no-thinking-indicator
### **Severity**
info
### **Type**
regex
### **Pattern**
\.say\(
### **Negative Pattern**
thinking|Thinking|loading|Loading|indicator|Indicator|bubble|Bubble
### **Message**
No thinking indicator while LLM generates. Players won't know NPC is processing.
### **Fix Action**
Show thinking bubble or typing indicator while awaiting response
### **Applies To**
  - *.gd

## Conversation Not Persisted

### **Id**
godot-conversation-not-persisted
### **Severity**
info
### **Type**
regex
### **Pattern**
NobodyWhoChat
### **Negative Pattern**
save|Save|persist|Persist|store|Store|conversation.*manager|ConversationManager
### **Message**
Conversation state may be lost on scene change. Consider persisting.
### **Fix Action**
Save conversation in autoload, restore when NPC scene loads
### **Applies To**
  - *.gd