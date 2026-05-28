# Godot Development - Sharp Edges

## _ready vs _enter_tree Timing

### **Id**
ready-vs-enter-tree
### **Severity**
high
### **Category**
lifecycle
### **Description**
  _enter_tree is called when a node enters the scene tree, BEFORE its
  children are ready. _ready is called AFTER all children are ready.
  Using @onready or accessing children in _enter_tree will fail.
  
### **Symptom**
  - Null reference errors when accessing child nodes
  - @onready variables are null
  - Signals connected in _enter_tree don't fire as expected
  
### **Solution**
  ```gdscript
  # WRONG: Children not ready yet
  func _enter_tree() -> void:
      $HealthBar.max_value = max_health  # Error: null
  
  # CORRECT: Use _ready for child access
  func _ready() -> void:
      $HealthBar.max_value = max_health  # Works
  
  # Use _enter_tree only for:
  # - Connecting to parent/tree signals
  # - Setting up before children initialize
  # - Adding to groups early
  ```
  
### **Tags**
  - lifecycle
  - initialization
  - null-reference

## Signal Connections Cause Memory Leaks

### **Id**
signal-memory-leaks
### **Severity**
critical
### **Category**
memory
### **Description**
  When object A connects to object B's signal, B holds a reference to A.
  If A is freed while B still exists, B has a dangling reference.
  If B is an autoload (never freed), A is never garbage collected.
  
### **Symptom**
  - Memory usage grows over time
  - Errors about "freed object" when signals emit
  - Game slows down after many scene changes
  
### **Solution**
  ```gdscript
  # Option 1: Disconnect in _exit_tree
  func _ready() -> void:
      EventBus.game_event.connect(_on_game_event)
  
  func _exit_tree() -> void:
      if EventBus.game_event.is_connected(_on_game_event):
          EventBus.game_event.disconnect(_on_game_event)
  
  # Option 2: Use one-shot for single-use signals
  enemy.died.connect(_on_enemy_died, CONNECT_ONE_SHOT)
  
  # Option 3: Use Callable with CONNECT_DEFERRED (auto-cleanup)
  # Godot 4.2+ handles some cases automatically
  
  # Option 4: Weak references for optional listeners
  # (advanced - use with caution)
  ```
  
### **Tags**
  - memory
  - signals
  - leaks

## Calling get_node() Every Frame

### **Id**
get-node-in-process
### **Severity**
high
### **Category**
performance
### **Description**
  get_node(), $, and get_tree().get_nodes_in_group() traverse the scene
  tree. Calling them every frame in _process or _physics_process wastes
  CPU cycles. Cache references in _ready.
  
### **Symptom**
  - Poor frame rate with many nodes
  - Profiler shows high "Idle" time in scripts
  - Game stutters during complex scenes
  
### **Solution**
  ```gdscript
  # WRONG: Tree traversal every frame
  func _process(delta: float) -> void:
      var player = $"../Player"
      var enemies = get_tree().get_nodes_in_group("enemies")
  
  # CORRECT: Cache in _ready
  @onready var player: CharacterBody2D = $"../Player"
  var enemies: Array[Node]
  
  func _ready() -> void:
      enemies = get_tree().get_nodes_in_group("enemies")
      # Update cache when enemies change
      get_tree().node_added.connect(_on_node_added)
  
  func _process(delta: float) -> void:
      # Use cached references
      player.take_damage(1)
  ```
  
### **Tags**
  - performance
  - caching
  - optimization

## Storing Game State in Autoloads

### **Id**
autoload-state-abuse
### **Severity**
medium
### **Category**
architecture
### **Description**
  Using autoloads as global state containers creates tight coupling,
  makes testing difficult, and causes issues with scene reloading.
  Player health in an autoload persists across game restarts.
  
### **Symptom**
  - Restarting game doesn't reset state
  - Difficult to write unit tests
  - Changing one autoload breaks many scripts
  - Circular dependencies between autoloads
  
### **Solution**
  ```gdscript
  # BAD: Global state autoload
  # Global.gd
  var player_health = 100
  var player_coins = 0
  
  # GOOD: State on actual objects
  # Player.gd
  extends CharacterBody2D
  var health: int = 100
  var coins: int = 0
  
  # Use autoloads for:
  # - EventBus (signals only, no state)
  # - SaveManager (load/save, transient)
  # - AudioManager (plays sounds, no game state)
  # - SceneManager (transitions, no game state)
  ```
  
### **Tags**
  - architecture
  - state-management
  - testing

## Using _process for Physics

### **Id**
physics-process-vs-process
### **Severity**
high
### **Category**
physics
### **Description**
  _process runs every visual frame (variable rate). _physics_process runs
  at fixed intervals (default 60 Hz). Physics calculations in _process
  cause jitter, tunneling, and non-deterministic behavior.
  
### **Symptom**
  - Movement speed varies with frame rate
  - Objects pass through walls at low FPS
  - Multiplayer desync
  - Physics behave differently on different machines
  
### **Solution**
  ```gdscript
  # WRONG: Physics in _process
  func _process(delta: float) -> void:
      velocity += gravity * delta
      move_and_slide()
  
  # CORRECT: Physics in _physics_process
  func _physics_process(delta: float) -> void:
      velocity += gravity * delta
      move_and_slide()
  
  # _process is for:
  # - Visual updates (sprite animation)
  # - UI updates
  # - Audio triggers
  # - Non-gameplay timers
  ```
  
### **Tags**
  - physics
  - determinism
  - framerate

## @export Variable Pitfalls

### **Id**
export-variable-gotchas
### **Severity**
medium
### **Category**
gdscript
### **Description**
  Exported variables have subtle behaviors: default values in code can be
  overridden by scene values, resources are shared by default, and some
  types don't export well.
  
### **Symptom**
  - Changing default in code doesn't affect existing scenes
  - All instances share the same resource/array
  - Exported dictionaries don't save properly
  
### **Solution**
  ```gdscript
  # Issue 1: Default override
  @export var speed: float = 100.0  # Changed to 200.0 in code
  # Existing scenes still have 100.0 saved!
  # Fix: Reset in inspector or delete .tscn and recreate
  
  # Issue 2: Shared resources
  @export var inventory: Array = []  # Shared across instances!
  # Fix: Initialize in _ready
  var inventory: Array
  func _ready() -> void:
      inventory = []
  
  # Issue 3: Resource sharing
  @export var stats: Resource  # Same instance if not unique
  # Fix: Make unique in inspector OR:
  func _ready() -> void:
      stats = stats.duplicate()
  
  # Issue 4: Complex types
  @export var data: Dictionary  # Limited editor support
  # Fix: Use custom Resource class instead
  ```
  
### **Tags**
  - export
  - inspector
  - resources

## GDScript vs C# Tradeoffs

### **Id**
gdscript-vs-csharp
### **Severity**
medium
### **Category**
language-choice
### **Description**
  GDScript is tightly integrated with Godot but slower than C#.
  C# has better performance and tooling but requires more setup and
  has some engine integration quirks.
  
### **Considerations**
  #### **Gdscript Pros**
    - Native integration, hot reload works perfectly
    - Simpler syntax, faster prototyping
    - Smaller build sizes
    - Better documentation and community examples
    - No external dependencies
  #### **Gdscript Cons**
    - Slower execution (10-100x vs C#)
    - Limited static analysis
    - No shared code with other platforms
  #### **Csharp Pros**
    - Better performance for heavy computation
    - Excellent IDE support (VS, Rider)
    - Share code with server/other projects
    - Strong typing, better refactoring
  #### **Csharp Cons**
    - Hot reload issues in Godot 4
    - Larger export sizes (.NET runtime)
    - Some API differences from GDScript
    - Fewer community examples
### **Recommendation**
  Use GDScript for most game code. Use C# for:
  - Complex AI calculations
  - Procedural generation algorithms
  - Server-shared game logic
  - Large team projects needing strict typing
  

## TileMap Performance Issues

### **Id**
tilemap-performance
### **Severity**
medium
### **Category**
performance
### **Description**
  Large TileMaps with many layers or complex tile data can cause
  performance issues. Runtime tile modification is expensive.
  
### **Symptom**
  - Low FPS with large maps
  - Stuttering when modifying tiles
  - Long load times for tile-heavy scenes
  
### **Solution**
  ```gdscript
  # 1. Use multiple TileMapLayers instead of one TileMap with layers
  # (Godot 4.3+ TileMapLayer is faster)
  
  # 2. Chunk large maps
  # Only load visible chunks
  
  # 3. Batch tile operations
  # BAD: Set tiles one by one
  for x in 1000:
      for y in 1000:
          tilemap.set_cell(0, Vector2i(x, y), source, atlas)
  
  # BETTER: Use set_cells_terrain_connect for terrain
  # Or queue changes and apply in batches
  
  # 4. Disable navigation/physics on decorative layers
  # In TileSet, only enable collision on necessary layers
  ```
  
### **Tags**
  - performance
  - tilemap
  - optimization

## Scene Tree Processing Order

### **Id**
scene-tree-order
### **Severity**
medium
### **Category**
lifecycle
### **Description**
  Nodes process in tree order (top to bottom). If node A depends on
  node B's state and B is below A, A sees stale data.
  
### **Symptom**
  - One-frame delays in reactions
  - Inconsistent behavior depending on scene structure
  - "Teleporting" objects
  
### **Solution**
  ```gdscript
  # The tree processes top-to-bottom:
  # Player (processes first)
  # Enemy (processes second, sees Player's NEW position)
  # UI (processes last, sees current state)
  
  # If order matters:
  # 1. Rearrange nodes in tree
  # 2. Use process_priority (lower = earlier)
  func _ready() -> void:
      process_priority = -1  # Process before default (0)
  
  # 3. Use signals for guaranteed timing
  # 4. Use call_deferred for next-frame operations
  call_deferred("late_update")
  ```
  
### **Tags**
  - lifecycle
  - ordering
  - timing

## Input Handling Anti-patterns

### **Id**
input-handling-mistakes
### **Severity**
medium
### **Category**
input
### **Description**
  Common mistakes with Godot's input system: not using Input Map,
  checking input in wrong callbacks, and missing _unhandled_input.
  
### **Symptom**
  - Input "eaten" by UI
  - Actions fire multiple times
  - Input doesn't work in certain scenes
  
### **Solution**
  ```gdscript
  # 1. Use Input Map (Project Settings > Input Map)
  # DON'T hardcode keys
  if Input.is_key_pressed(KEY_SPACE):  # Bad
  if Input.is_action_pressed("jump"):   # Good
  
  # 2. Choose correct callback
  # _input: ALL input, including handled
  # _unhandled_input: Input not consumed by UI
  # _physics_process: Poll-based input for movement
  
  func _unhandled_input(event: InputEvent) -> void:
      if event.is_action_pressed("interact"):
          interact()
          get_viewport().set_input_as_handled()
  
  func _physics_process(delta: float) -> void:
      # Movement input (continuous)
      var direction = Input.get_vector("left", "right", "up", "down")
  
  # 3. UI blocking input
  # Control nodes consume input by default
  # Use mouse_filter = MOUSE_FILTER_IGNORE on overlays
  ```
  
### **Tags**
  - input
  - ui
  - events

## Shader Performance Gotchas

### **Id**
shader-performance
### **Severity**
medium
### **Category**
rendering
### **Description**
  Shaders can tank performance if not careful. Texture reads in
  loops, complex math per pixel, and too many uniforms hurt FPS.
  
### **Symptom**
  - GPU-bound performance (profiler shows high GPU time)
  - Frame rate drops with shader effects
  - Mobile devices struggle with effects
  
### **Solution**
  ```glsl
  // 1. Minimize texture reads
  // BAD: Sample in loop
  for (int i = 0; i < 10; i++) {
      color += texture(tex, uv + offset * float(i));
  }
  
  // GOOD: Precompute, use texture LOD
  color = textureLod(tex, uv, 2.0);  // Lower LOD = faster
  
  // 2. Avoid branching
  // BAD: if/else per pixel
  if (condition) { ... }
  
  // GOOD: Use mix/step
  color = mix(color1, color2, step(0.5, value));
  
  // 3. Reduce overdraw
  // Use DEPTH_TEST when possible
  // Sort transparent objects back-to-front
  
  // 4. Use simpler shaders on mobile
  // Check: if ANDROID or if IOS
  ```
  
### **Tags**
  - shaders
  - performance
  - gpu

## Resource Loading Stalls

### **Id**
resource-preloading
### **Severity**
high
### **Category**
performance
### **Description**
  load() and preload() block the main thread. Loading large resources
  during gameplay causes stuttering. Use background loading.
  
### **Symptom**
  - Game freezes when entering new areas
  - Stuttering when spawning enemies
  - Long transitions between scenes
  
### **Solution**
  ```gdscript
  # preload() - Loads at script parse time (good for small, always-used)
  const BulletScene = preload("res://bullet.tscn")
  
  # load() - Loads when called (blocks!)
  var resource = load("res://big_texture.png")  # Stalls!
  
  # Background loading (non-blocking)
  func load_level_async(path: String) -> void:
      ResourceLoader.load_threaded_request(path)
  
  func _process(delta: float) -> void:
      var status = ResourceLoader.load_threaded_get_status(path)
      if status == ResourceLoader.THREAD_LOAD_LOADED:
          var level = ResourceLoader.load_threaded_get(path)
          get_tree().change_scene_to_packed(level)
  
  # Preload during loading screen
  # Use ResourceLoader.load_threaded_request for each asset
  # Show progress with load_threaded_get_status
  ```
  
### **Tags**
  - loading
  - performance
  - threading