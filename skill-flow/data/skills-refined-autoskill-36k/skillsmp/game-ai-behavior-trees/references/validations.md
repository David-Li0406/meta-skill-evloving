# Game Ai Behavior Trees - Validations

## Synchronous LLM in Behavior Tree

### **Id**
bt-sync-llm
### **Severity**
critical
### **Type**
regex
### **Pattern**
tick\\([^)]*\\)[^}]*llm\\.complete(?!_async)|tick\\([^)]*\\)[^}]*await.*llm
### **Message**
Synchronous LLM call in tick(). Will block behavior tree execution.
### **Fix Action**
Use async LLM with RUNNING state, or read cached decision from blackboard
### **Applies To**
  - *.ts
  - *.js
  - *.gd
  - *.cs

## BT Node Without Cleanup

### **Id**
bt-no-exit-cleanup
### **Severity**
high
### **Type**
regex
### **Pattern**
on_enter|OnEnter|Enter
### **Negative Pattern**
on_exit|OnExit|Exit|cleanup|Cleanup
### **Message**
BT node has on_enter but no on_exit. State may not be cleaned up.
### **Fix Action**
Add on_exit to reset any state set in on_enter
### **Applies To**
  - *.ts
  - *.js
  - *.gd
  - *.cs

## String-Based Blackboard Keys

### **Id**
bt-string-blackboard
### **Severity**
warning
### **Type**
regex
### **Pattern**
blackboard\.set\s*\(\s*["']|GetValue\s*\(\s*["']|SetValue\s*\(\s*["']
### **Message**
String-based blackboard access. Typos cause silent failures.
### **Fix Action**
Use typed blackboard properties or constants for keys
### **Applies To**
  - *.ts
  - *.js
  - *.gd
  - *.cs

## Selector Without Fallback

### **Id**
bt-no-fallback
### **Severity**
warning
### **Type**
regex
### **Pattern**
Selector|selector
### **Negative Pattern**
fallback|Fallback|default|Default|always.*succeed
### **Message**
Selector may have no fallback if all children fail.
### **Fix Action**
Add a fallback leaf node that always succeeds with default behavior
### **Applies To**
  - *.ts
  - *.js
  - *.gd
  - *.yaml

## LLM Query Every Tick

### **Id**
bt-llm-every-tick
### **Severity**
warning
### **Type**
regex
### **Pattern**
tick\\([^}]*llm|update\\([^}]*llm
### **Negative Pattern**
cooldown|Cooldown|cache|Cache|throttle|timer
### **Message**
LLM may be queried every tick. Add cooldown/caching.
### **Fix Action**
Add cooldown timer, only query LLM every 5-30 seconds
### **Applies To**
  - *.ts
  - *.js
  - *.gd
  - *.cs

## Deep Tree Nesting

### **Id**
bt-deep-nesting
### **Severity**
info
### **Type**
regex
### **Pattern**
\\s{16,}[\\[\\-]|\\t{4,}[\\[\\-]
### **Message**
Deep nesting detected. Consider using subtrees for modularity.
### **Fix Action**
Extract deeply nested sections into reusable subtrees
### **Applies To**
  - *.yaml
  - *.json