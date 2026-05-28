# Godot Development - Validations

## get_node() called in _process

### **Id**
get-node-in-process
### **Description**
Calling get_node() every frame is expensive. Cache the reference in @onready.
### **Severity**
warning
### **Category**
performance
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_(?:physics_)?process\s*\([^)]*\)\s*(?:->\s*\w+)?\s*:[^}]*get_node\s*\(
### **Multiline**

### **Fix Hint**
  Replace with @onready:
  ```gdscript
  @onready var my_node: Node = get_node("path/to/node")
  
  func _process(delta: float) -> void:
      my_node.do_something()
  ```
  

## $ operator in _process

### **Id**
dollar-in-process
### **Description**
Using $ in _process traverses the tree every frame. Cache with @onready.
### **Severity**
warning
### **Category**
performance
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_(?:physics_)?process\s*\([^)]*\)\s*(?:->\s*\w+)?\s*:[^}]*\$\w+
### **Multiline**

### **Fix Hint**
Cache node reference with @onready var node_name: Type = $NodePath

## get_nodes_in_group() in _process

### **Id**
get-nodes-in-group-process
### **Description**
Getting nodes in group every frame is expensive. Cache the array.
### **Severity**
warning
### **Category**
performance
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_(?:physics_)?process\s*\([^)]*\)[^}]*get_nodes_in_group\s*\(
### **Multiline**

### **Fix Hint**
  Cache the array and update when nodes change:
  ```gdscript
  var enemies: Array[Node]
  
  func _ready() -> void:
      enemies = get_tree().get_nodes_in_group("enemies")
  ```
  

## load() called in _process

### **Id**
load-in-process
### **Description**
load() blocks the main thread. Use preload() or ResourceLoader.load_threaded_request().
### **Severity**
error
### **Category**
performance
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_(?:physics_)?process\s*\([^)]*\)[^}]*[^pre]load\s*\(
### **Multiline**

### **Fix Hint**
Use preload() for static resources or ResourceLoader.load_threaded_request() for dynamic loading.

## Physics operations in _process

### **Id**
physics-in-process
### **Description**
move_and_slide() and velocity changes should be in _physics_process for deterministic behavior.
### **Severity**
error
### **Category**
physics
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_process\s*\([^)]*\)[^}]*move_and_slide\s*\(
### **Multiline**

### **Fix Hint**
Move physics code to _physics_process(delta: float) -> void

## Velocity modified in _process

### **Id**
velocity-in-process
### **Description**
Velocity should be modified in _physics_process for consistent physics.
### **Severity**
warning
### **Category**
physics
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_process\s*\([^)]*\)[^}]*velocity\s*[+\-*/]?=
### **Multiline**

### **Fix Hint**
Move velocity calculations to _physics_process

## Accessing children in _enter_tree

### **Id**
child-access-enter-tree
### **Description**
_enter_tree runs before children are ready. Use _ready for child access.
### **Severity**
error
### **Category**
lifecycle
### **File Patterns**
  - *.gd
### **Pattern**
func\s+_enter_tree\s*\([^)]*\)[^}]*(?:get_node|get_child|\$)
### **Multiline**

### **Fix Hint**
Move child access to _ready() where children are guaranteed to exist.

## Signal connected without disconnect

### **Id**
signal-no-disconnect
### **Description**
Signals to autoloads or persistent nodes should be disconnected in _exit_tree.
### **Severity**
info
### **Category**
memory
### **File Patterns**
  - *.gd
### **Pattern**
\.connect\s*\([^)]+\)(?!.*\.disconnect)
### **Fix Hint**
  Add disconnect in _exit_tree:
  ```gdscript
  func _exit_tree() -> void:
      if signal_source.my_signal.is_connected(_my_handler):
          signal_source.my_signal.disconnect(_my_handler)
  ```
  

## Exported array with empty default

### **Id**
exported-empty-array
### **Description**
Exported arrays with [] default are shared across instances. Initialize in _ready.
### **Severity**
warning
### **Category**
gdscript
### **File Patterns**
  - *.gd
### **Pattern**
@export\s+var\s+\w+\s*:\s*Array\s*=\s*\[\]
### **Fix Hint**
  Initialize in _ready instead:
  ```gdscript
  @export var items: Array  # No default
  func _ready() -> void:
      items = []
  ```
  

## Exported dictionary with empty default

### **Id**
exported-empty-dict
### **Description**
Exported dictionaries with {} default are shared across instances.
### **Severity**
warning
### **Category**
gdscript
### **File Patterns**
  - *.gd
### **Pattern**
@export\s+var\s+\w+\s*:\s*Dictionary\s*=\s*\{\}
### **Fix Hint**
Initialize dictionaries in _ready() or use a custom Resource.

## Hardcoded key constants

### **Id**
hardcoded-keys
### **Description**
Use Input Map actions instead of hardcoded keys for remappable controls.
### **Severity**
warning
### **Category**
input
### **File Patterns**
  - *.gd
### **Pattern**
is_key_pressed\s*\(\s*KEY_
### **Fix Hint**
  Use Input Map:
  ```gdscript
  # In Project Settings > Input Map, add action "jump" with KEY_SPACE
  if Input.is_action_pressed("jump"):
  ```
  

## Hardcoded mouse button check

### **Id**
hardcoded-mouse-buttons
### **Description**
Use Input Map actions for mouse buttons for consistency and remapping.
### **Severity**
info
### **Category**
input
### **File Patterns**
  - *.gd
### **Pattern**
is_mouse_button_pressed\s*\(\s*MOUSE_BUTTON_
### **Fix Hint**
Add mouse actions to Input Map (e.g., 'shoot' -> MOUSE_BUTTON_LEFT)

## Untyped function parameters

### **Id**
untyped-function-params
### **Description**
Add type hints to function parameters for better error detection and autocompletion.
### **Severity**
info
### **Category**
gdscript
### **File Patterns**
  - *.gd
### **Pattern**
func\s+\w+\s*\(\s*\w+(?:\s*,\s*\w+)*\s*\)\s*(?:->|:)
### **Negative Pattern**
func\s+\w+\s*\(\s*\w+\s*:\s*\w+
### **Fix Hint**
  Add type hints:
  ```gdscript
  func take_damage(amount: int, source: Node) -> void:
  ```
  

## Function missing return type

### **Id**
untyped-return
### **Description**
Add return type hints to functions for clarity and error detection.
### **Severity**
info
### **Category**
gdscript
### **File Patterns**
  - *.gd
### **Pattern**
func\s+\w+\s*\([^)]*\)\s*:
### **Negative Pattern**
func\s+\w+\s*\([^)]*\)\s*->\s*\w+
### **Fix Hint**
  Add return type:
  ```gdscript
  func get_health() -> int:
      return current_health
  ```
  

## Hardcoded relative node path

### **Id**
hardcoded-node-path
### **Description**
Deep relative paths break easily. Use groups, unique names (%), or exports.
### **Severity**
info
### **Category**
architecture
### **File Patterns**
  - *.gd
### **Pattern**
get_node\s*\(\s*["']\.\./
### **Fix Hint**
  Use alternatives:
  ```gdscript
  # Groups
  var player = get_tree().get_first_node_in_group("player")
  
  # Unique names (set % in editor)
  @onready var hud = %HUD
  
  # Exports
  @export var target: Node
  ```
  

## await in loop without check

### **Id**
await-in-loop
### **Description**
Awaiting in loops can cause issues if the object is freed during wait.
### **Severity**
warning
### **Category**
async
### **File Patterns**
  - *.gd
### **Pattern**
(?:for|while)[^:]*:[^}]*await
### **Multiline**

### **Fix Hint**
  Check validity after await:
  ```gdscript
  for item in items:
      await some_signal
      if not is_instance_valid(self):
          return
      # Continue processing
  ```
  

## Disabling process incorrectly

### **Id**
set-process-false
### **Description**
set_process(false) only affects _process, not _physics_process.
### **Severity**
info
### **Category**
lifecycle
### **File Patterns**
  - *.gd
### **Pattern**
set_process\s*\(\s*false\s*\)
### **Fix Hint**
  To disable all processing:
  ```gdscript
  set_process(false)
  set_physics_process(false)
  # Or use process_mode = PROCESS_MODE_DISABLED
  ```
  

## Code after queue_free()

### **Id**
queue-free-continue
### **Description**
queue_free() doesn't immediately free the node. Add return after queue_free().
### **Severity**
warning
### **Category**
lifecycle
### **File Patterns**
  - *.gd
### **Pattern**
queue_free\s*\(\s*\)[^\n]*\n[^\n]*[^\s\n]
### **Fix Hint**
  Add return after queue_free:
  ```gdscript
  func die() -> void:
      play_death_effect()
      queue_free()
      return  # Prevent further execution
  ```
  

## Instantiating scene without type check

### **Id**
direct-instance-scene
### **Description**
Use typed instantiate for better safety and autocompletion.
### **Severity**
info
### **Category**
gdscript
### **File Patterns**
  - *.gd
### **Pattern**
\.instantiate\s*\(\s*\)(?!\s+as\s+)
### **Fix Hint**
  Use typed instantiate:
  ```gdscript
  var enemy := enemy_scene.instantiate() as Enemy
  ```
  

## Discarding pixels in shader

### **Id**
shader-discard-alpha
### **Description**
discard breaks GPU optimizations. Consider alpha testing instead.
### **Severity**
info
### **Category**
rendering
### **File Patterns**
  - *.gdshader
### **Pattern**
discard\s*;
### **Fix Hint**
  For simple alpha cutoff, use:
  ```glsl
  ALPHA = step(0.5, texture_color.a);
  // Or configure material for alpha scissor
  ```
  