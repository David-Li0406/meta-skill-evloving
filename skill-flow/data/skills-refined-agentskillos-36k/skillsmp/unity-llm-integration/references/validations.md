# Unity Llm Integration - Validations

## Synchronous LLM Call in Unity

### **Id**
unity-sync-llm-call
### **Severity**
critical
### **Type**
regex
### **Pattern**
\.Chat\([^)]*\)\.Result|\.Complete\([^)]*\)\.Result|GetAwaiter\(\)\.GetResult\(\)
### **Message**
Synchronous LLM call detected. This will freeze Unity's main thread.
### **Fix Action**
Use async/await, coroutines with callbacks, or UniTask
### **Applies To**
  - *.cs

## LLM Call in Update Loop

### **Id**
unity-llm-in-update
### **Severity**
critical
### **Type**
regex
### **Pattern**
void Update\(\)[^}]*\.Chat\(|void FixedUpdate\(\)[^}]*\.Chat\(
### **Message**
LLM call in Update loop. Will flood LLM with requests and freeze game.
### **Fix Action**
Move LLM calls to event handlers or throttled methods
### **Applies To**
  - *.cs

## Absolute Model Path

### **Id**
unity-model-absolute-path
### **Severity**
high
### **Type**
regex
### **Pattern**
SetModel\s*\(\s*["'][A-Za-z]:\\|SetModel\s*\(\s*["']/
### **Message**
Absolute path for model. Won't work in builds - use StreamingAssets.
### **Fix Action**
Place model in StreamingAssets and use Application.streamingAssetsPath
### **Applies To**
  - *.cs

## Blocking LLM Load in Start

### **Id**
unity-llm-in-start-sync
### **Severity**
high
### **Type**
regex
### **Pattern**
void Start\(\)[^}]*llm\.Load\(\)|void Awake\(\)[^}]*llm\.Load\(\)
### **Message**
LLM loading in Start/Awake without async. Game will freeze during load.
### **Fix Action**
Use IEnumerator Start() with yield return llm.Load() and loading UI
### **Applies To**
  - *.cs

## No Platform-Specific Configuration

### **Id**
unity-no-platform-check
### **Severity**
high
### **Type**
regex
### **Pattern**
SetModel\s*\(
### **Negative Pattern**
#if UNITY_|UNITY_ANDROID|UNITY_IOS|UNITY_STANDALONE|platform|Platform
### **Message**
Model configuration without platform checks. Different platforms need different models.
### **Fix Action**
Add #if UNITY_ANDROID, UNITY_IOS, etc. for platform-specific model selection
### **Applies To**
  - *.cs

## No Fallback for LLM Failure

### **Id**
unity-no-llm-fallback
### **Severity**
high
### **Type**
regex
### **Pattern**
await.*\.Chat\(
### **Negative Pattern**
try|catch|fallback|Fallback|timeout|Timeout
### **Message**
LLM call without error handling. What happens when LLM fails?
### **Fix Action**
Add try/catch with fallback dialogue for LLM failures
### **Applies To**
  - *.cs

## Multiple LLM Instances

### **Id**
unity-multiple-llm-instances
### **Severity**
warning
### **Type**
regex
### **Pattern**
public LLM llm|\[SerializeField\].*LLM llm|new LLM\(\)
### **Message**
Each LLM instance loads model separately. Use singleton pattern for shared LLM.
### **Fix Action**
Create LLMManager singleton and share one LLM across NPCs
### **Applies To**
  - *.cs

## Missing Loading UI for LLM

### **Id**
unity-no-loading-ui
### **Severity**
warning
### **Type**
regex
### **Pattern**
llm\.Load\(
### **Negative Pattern**
loading|Loading|progress|Progress|indicator|Indicator|screen|Screen
### **Message**
LLM loading without visible feedback. Users will think app is frozen.
### **Fix Action**
Add loading screen or progress indicator during model load
### **Applies To**
  - *.cs

## Large Model on Mobile Platform

### **Id**
unity-large-model-mobile
### **Severity**
warning
### **Type**
regex
### **Pattern**
(?:7[bB]|8[bB]|13[bB]|14[bB]).*\.gguf
### **Message**
Large model (7B+) detected. May be too large for mobile deployment.
### **Fix Action**
Use 1-3B models for mobile. Add platform-specific model selection.
### **Applies To**
  - *.cs

## Local LLM in WebGL Build

### **Id**
unity-webgl-local-llm
### **Severity**
warning
### **Type**
regex
### **Pattern**
UNITY_WEBGL.*LLM|LLM.*UNITY_WEBGL
### **Negative Pattern**
disabled|Disabled|fallback|Fallback|cloud|Cloud|API
### **Message**
LLM reference in WebGL code. Local LLM doesn't work in WebGL.
### **Fix Action**
Disable local LLM and use cloud API fallback for WebGL
### **Applies To**
  - *.cs

## No LLM Cleanup on Destroy

### **Id**
unity-no-destroy-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
LLM llm|LLMCharacter character
### **Negative Pattern**
OnDestroy|OnDisable|Unload|Dispose|cleanup|Cleanup
### **Message**
LLM components without cleanup. May cause memory leaks between scenes.
### **Fix Action**
Add OnDestroy to unload models and cancel pending operations
### **Applies To**
  - *.cs

## Not Using Streaming Response

### **Id**
unity-streaming-not-used
### **Severity**
info
### **Type**
regex
### **Pattern**
await.*\.Chat\([^,)]*\)
### **Negative Pattern**
callback|Callback|stream|Stream|partial|Partial
### **Message**
Chat without streaming. Consider streaming for better UX in dialogue.
### **Fix Action**
Use Chat(input, callback) to show text as it generates
### **Applies To**
  - *.cs

## Hard-coded Context Size

### **Id**
unity-hard-coded-context-size
### **Severity**
info
### **Type**
regex
### **Pattern**
contextSize\s*=\s*\d{4}
### **Message**
Hard-coded context size. Consider platform-specific values.
### **Fix Action**
Use smaller context (1024-2048) on mobile, larger (4096) on desktop
### **Applies To**
  - *.cs