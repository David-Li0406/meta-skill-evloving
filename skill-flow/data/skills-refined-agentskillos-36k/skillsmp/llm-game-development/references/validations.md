# Llm Game Development - Validations

## AI Prompt Without Version Context

### **Id**
llm-no-version-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
//\s*(?:AI|Claude|GPT|Copilot|LLM).*(?:generated|created|wrote)
### **Negative Pattern**
Unity\s*\d|Godot\s*\d|UE\s*\d|version|Version
### **Message**
AI-generated code marker without version context. Helps future debugging.
### **Fix Action**
Add version info to AI generation comments: // AI-generated for Unity 2023.2
### **Applies To**
  - *.cs
  - *.gd
  - *.cpp
  - *.ts
  - *.js

## Deprecated Unity API

### **Id**
llm-deprecated-unity-api
### **Severity**
warning
### **Type**
regex
### **Pattern**
FindObjectOfType|SendMessage|BroadcastMessage|InvokeRepeating
### **Message**
Using deprecated or slow Unity API. LLMs often generate these.
### **Fix Action**
Use FindFirstObjectByType, Events/UnityEvents, or Coroutines/Invoke
### **Applies To**
  - *.cs

## Stringly-Typed Godot Code

### **Id**
llm-string-comparison-godot
### **Severity**
warning
### **Type**
regex
### **Pattern**
get_node\(\s*["']|has_node\(\s*["']
### **Negative Pattern**
@onready|$|%
### **Message**
String-based node access. LLMs often miss Godot 4's $ and % syntax.
### **Fix Action**
Use $NodeName or %UniqueNode for type-safe node access
### **Applies To**
  - *.gd

## Public Fields Without SerializeField

### **Id**
llm-unity-public-field
### **Severity**
info
### **Type**
regex
### **Pattern**
public\s+(?:int|float|string|bool|GameObject|Transform)\s+\w+\s*;
### **Negative Pattern**
\[SerializeField\]|\[HideInInspector\]
### **Message**
Public field - prefer [SerializeField] private for encapsulation.
### **Fix Action**
Use [SerializeField] private field; for inspector-visible private fields
### **Applies To**
  - *.cs

## Potential Null Reference

### **Id**
llm-missing-null-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
GetComponent.*\(\)\.|\bFind.*\(\)\.|\bInstantiate.*as\s+\w+\)\.
### **Negative Pattern**
\?\.|if\s*\(|null|!=
### **Message**
Direct method call on potentially null result. LLMs often skip null checks.
### **Fix Action**
Add null check or use ?. operator: GetComponent<T>()?.Method()
### **Applies To**
  - *.cs

## Find/GetComponent in Update Loop

### **Id**
llm-update-find
### **Severity**
high
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)\s*\{[^}]*(?:Find|GetComponent)
### **Message**
Expensive operation in Update(). Cache references in Start/Awake.
### **Fix Action**
Move Find/GetComponent to Start() or Awake() and cache in field
### **Applies To**
  - *.cs

## Find in _process Loop

### **Id**
llm-process-find
### **Severity**
high
### **Type**
regex
### **Pattern**
func\s+_process\s*\([^)]*\):[^:]*(?:get_node|find_child|get_tree)
### **Message**
Node lookup in _process(). Cache with @onready.
### **Fix Action**
Use @onready var node = $NodePath and reference cached variable
### **Applies To**
  - *.gd

## Hardcoded String Identifiers

### **Id**
llm-hardcoded-strings
### **Severity**
info
### **Type**
regex
### **Pattern**
Animator\.SetBool\(\s*"|GetInput\(\s*"|LoadScene\(\s*"
### **Message**
Hardcoded string identifiers. Use constants to prevent typos.
### **Fix Action**
Define const string ANIM_JUMPING = "isJumping"; and use constant
### **Applies To**
  - *.cs

## Physics in Update Instead of FixedUpdate

### **Id**
llm-physics-in-update
### **Severity**
warning
### **Type**
regex
### **Pattern**
void\s+Update\s*\([^)]*\)\s*\{[^}]*(?:AddForce|velocity|MovePosition)
### **Message**
Physics operations should be in FixedUpdate(), not Update().
### **Fix Action**
Move physics code to FixedUpdate() for consistent behavior
### **Applies To**
  - *.cs

## Async Without Error Handling

### **Id**
llm-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
async\s+|await\s+|\.then\(|Promise\.
### **Negative Pattern**
catch|try|error|Error|except|Exception
### **Message**
Async code without error handling. LLMs often skip try/catch.
### **Fix Action**
Wrap async operations in try/catch with appropriate error handling
### **Applies To**
  - *.cs
  - *.ts
  - *.js
  - *.gd

## Magic Numbers in Game Logic

### **Id**
llm-magic-numbers
### **Severity**
info
### **Type**
regex
### **Pattern**
\b(?:if|while|for).*[<>=]+\s*\d{2,}|\w+\s*=\s*\d{3,}
### **Negative Pattern**
const|readonly|CONST|MAX_|MIN_|DEFAULT_
### **Message**
Magic number in logic. Use named constants for clarity.
### **Fix Action**
Define constant: const int MAX_HEALTH = 100;
### **Applies To**
  - *.cs
  - *.gd
  - *.ts
  - *.js

## User Input Without Validation

### **Id**
llm-missing-input-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
PlayerPrefs\.GetString|Input\.inputString|GetComponent.*TMP_InputField.*\.text
### **Negative Pattern**
string\.IsNullOrEmpty|TryParse|Validate|sanitize|escape
### **Message**
User input without validation. Validate before using.
### **Fix Action**
Validate and sanitize user input before processing
### **Applies To**
  - *.cs

## Coroutine Not Stopped

### **Id**
llm-coroutine-leak
### **Severity**
warning
### **Type**
regex
### **Pattern**
StartCoroutine\s*\(
### **Negative Pattern**
StopCoroutine|StopAllCoroutines|OnDisable|OnDestroy
### **Message**
Coroutine started but might not be stopped. Can cause issues on scene change.
### **Fix Action**
Store coroutine reference and stop in OnDisable/OnDestroy
### **Applies To**
  - *.cs