# Godot 4 Development

## Patterns

### **Scene Composition**
  #### **Name**
Scene Composition Over Inheritance
  #### **Description**
    Build complex behaviors by combining simple, focused scenes rather than
    deep inheritance hierarchies. Each scene should do one thing well.
    
  #### **Example**
    # HealthComponent.gd - Reusable across any entity
    class_name HealthComponent
    extends Node
    
    signal health_changed(new_health: int, max_health: int)
    signal died
    
    @export var max_health: int = 100
    var current_health: int
    
    func _ready() -> void:
        current_health = max_health
    
    func take_damage(amount: int) -> void:
        current_health = maxi(0, current_health - amount)
        health_changed.emit(current_health, max_health)
        if current_health == 0:
            died.emit()
    
    func heal(amount: int) -> void:
        current_health = mini(max_health, current_health + amount)
        health_changed.emit(current_health, max_health)
    
  #### **When To Use**
    - Health systems, damage, status effects
    - Movement controllers
    - AI behavior modules
    - Inventory systems
    - Any reusable game logic
### **Signal Architecture**
  #### **Name**
Signal-Based Communication
  #### **Description**
    Use signals for upward/sideways communication between nodes. The emitter
    doesn't need to know who's listening. Connect in _ready or via editor.
    
  #### **Example**
    # Player.gd - Emits signals, doesn't know about UI
    extends CharacterBody2D
    
    signal coin_collected(total: int)
    signal health_changed(current: int, max: int)
    
    var coins: int = 0
    
    func collect_coin() -> void:
        coins += 1
        coin_collected.emit(coins)
    
    # ---
    
    # HUD.gd - Connects to player signals
    extends CanvasLayer
    
    @onready var coin_label: Label = $CoinLabel
    
    func _ready() -> void:
        # Get reference and connect
        var player = get_tree().get_first_node_in_group("player")
        if player:
            player.coin_collected.connect(_on_coin_collected)
    
    func _on_coin_collected(total: int) -> void:
        coin_label.text = "Coins: %d" % total
    
  #### **Principles**
    - Signals go UP, calls go DOWN
    - Parent knows children, children don't know parent
    - Use groups for cross-tree communication
### **Custom Resources**
  #### **Name**
Data-Driven Design with Resources
  #### **Description**
    Use custom Resource classes for game data. Resources are saved to disk,
    shared across instances, and inspectable in the editor.
    
  #### **Example**
    # weapon_data.gd
    class_name WeaponData
    extends Resource
    
    @export var name: String = "Sword"
    @export var damage: int = 10
    @export var attack_speed: float = 1.0
    @export var range: float = 50.0
    @export var icon: Texture2D
    @export var swing_animation: SpriteFrames
    
    func get_dps() -> float:
        return damage * attack_speed
    
    # ---
    
    # weapon.gd - Uses the resource
    extends Node2D
    
    @export var data: WeaponData
    
    func attack(target: Node2D) -> void:
        if target.has_method("take_damage"):
            target.take_damage(data.damage)
    
  #### **Benefits**
    - Edit data in inspector without code changes
    - Share data across multiple instances
    - Version control friendly (.tres files)
    - Runtime swappable (change weapon by changing resource)
### **State Machine**
  #### **Name**
Finite State Machine Pattern
  #### **Description**
    Implement state machines for complex entity behavior. States are nodes,
    the machine manages transitions. Clean, debuggable, extensible.
    
  #### **Example**
    # state_machine.gd
    class_name StateMachine
    extends Node
    
    @export var initial_state: State
    var current_state: State
    var states: Dictionary = {}
    
    func _ready() -> void:
        for child in get_children():
            if child is State:
                states[child.name.to_lower()] = child
                child.state_machine = self
    
        if initial_state:
            current_state = initial_state
            current_state.enter()
    
    func _process(delta: float) -> void:
        if current_state:
            current_state.update(delta)
    
    func _physics_process(delta: float) -> void:
        if current_state:
            current_state.physics_update(delta)
    
    func transition_to(state_name: String) -> void:
        var new_state = states.get(state_name.to_lower())
        if new_state and new_state != current_state:
            current_state.exit()
            current_state = new_state
            current_state.enter()
    
    # ---
    
    # state.gd
    class_name State
    extends Node
    
    var state_machine: StateMachine
    
    func enter() -> void:
        pass
    
    func exit() -> void:
        pass
    
    func update(_delta: float) -> void:
        pass
    
    func physics_update(_delta: float) -> void:
        pass
    
### **Typed Gdscript**
  #### **Name**
Static Typing Best Practices
  #### **Description**
    Use static typing everywhere in GDScript. Catches errors at parse time,
    enables autocompletion, and documents intent.
    
  #### **Example**
    extends CharacterBody2D
    
    # Typed exports with defaults
    @export var speed: float = 200.0
    @export var jump_force: float = -400.0
    @export_range(0, 1) var friction: float = 0.1
    
    # Typed constants
    const GRAVITY: float = 980.0
    
    # Typed variables
    var coins_collected: int = 0
    var is_jumping: bool = false
    
    # Typed function with return type
    func calculate_damage(base: int, multiplier: float) -> int:
        return int(base * multiplier)
    
    # Typed arrays
    var inventory: Array[String] = []
    var waypoints: Array[Vector2] = []
    
    # Typed dictionaries (Godot 4.x)
    var stats: Dictionary = {
        "health": 100,
        "mana": 50
    }
    
    # Inferred typing with :=
    var player := get_node("Player") as CharacterBody2D
    
### **Autoload Architecture**
  #### **Name**
Autoload (Singleton) Management
  #### **Description**
    Use autoloads sparingly for truly global systems. Prefer dependency
    injection and signals over autoload access for testability.
    
  #### **Example**
    # Good autoload candidates:
    # - GameManager (game state, pause, quit)
    # - AudioManager (music, SFX bus control)
    # - SaveManager (save/load game data)
    # - EventBus (global signals)
    
    # event_bus.gd (Autoload)
    extends Node
    
    # Global signals any node can emit/connect to
    signal game_paused
    signal game_resumed
    signal level_completed(level_id: int)
    signal achievement_unlocked(achievement_id: String)
    
    # ---
    
    # Usage in any script:
    func _ready() -> void:
        EventBus.level_completed.connect(_on_level_completed)
    
    func complete_level() -> void:
        EventBus.level_completed.emit(current_level_id)
    
  #### **Guidelines**
    - Maximum 5-7 autoloads in a project
    - Each autoload should have a single responsibility
    - Avoid storing game state in autoloads when possible
    - Use for coordination, not for storing data
### **Physics Patterns**
  #### **Name**
Physics Best Practices
  #### **Description**
    Understand when to use CharacterBody2D/3D vs RigidBody vs Area.
    Process physics in _physics_process, never _process.
    
  #### **Example**
    # CharacterBody2D - Player/NPC movement (you control physics)
    extends CharacterBody2D
    
    @export var speed: float = 200.0
    @export var gravity: float = 980.0
    
    func _physics_process(delta: float) -> void:
        # Apply gravity
        if not is_on_floor():
            velocity.y += gravity * delta
    
        # Get input
        var direction := Input.get_axis("move_left", "move_right")
        velocity.x = direction * speed
    
        # Move and handle collisions
        move_and_slide()
    
        # Check for collisions
        for i in get_slide_collision_count():
            var collision := get_slide_collision(i)
            var collider := collision.get_collider()
            if collider.is_in_group("enemies"):
                take_damage(10)
    
    # ---
    
    # Area2D - Triggers, pickups, hit detection
    extends Area2D
    
    signal picked_up
    
    func _ready() -> void:
        body_entered.connect(_on_body_entered)
    
    func _on_body_entered(body: Node2D) -> void:
        if body.is_in_group("player"):
            picked_up.emit()
            queue_free()
    

## Anti-Patterns

### **Get Node In Process**
  #### **Name**
Calling get_node() in _process
  #### **Description**
    Never call get_node() or $ in _process/_physics_process. Cache node
    references in _ready using @onready.
    
  #### **Bad Example**
    func _process(delta: float) -> void:
        # BAD: Searches tree every frame
        var player = get_node("../Player")
        var label = $UI/HealthLabel
        label.text = str(player.health)
    
  #### **Good Example**
    # GOOD: Cache references once
    @onready var player: CharacterBody2D = get_node("../Player")
    @onready var label: Label = $UI/HealthLabel
    
    func _process(delta: float) -> void:
        label.text = str(player.health)
    
### **Signal Memory Leaks**
  #### **Name**
Not Disconnecting Signals
  #### **Description**
    When connecting signals in code to objects that outlive the listener,
    disconnect in _exit_tree or use one-shot connections.
    
  #### **Bad Example**
    func _ready() -> void:
        # BAD: If this node is freed, signal still references it
        GameManager.level_changed.connect(_on_level_changed)
    
  #### **Good Example**
    func _ready() -> void:
        # GOOD: Disconnect when node exits tree
        GameManager.level_changed.connect(_on_level_changed)
    
    func _exit_tree() -> void:
        if GameManager.level_changed.is_connected(_on_level_changed):
            GameManager.level_changed.disconnect(_on_level_changed)
    
    # OR use CONNECT_ONE_SHOT for single-use:
    signal_source.my_signal.connect(_handler, CONNECT_ONE_SHOT)
    
### **Inheritance Overuse**
  #### **Name**
Deep Inheritance Hierarchies
  #### **Description**
    Avoid deep inheritance trees. Godot favors composition via scenes and
    nodes over inheritance.
    
  #### **Bad Example**
    # BAD: Deep inheritance
    # Entity -> Character -> Enemy -> FlyingEnemy -> Dragon
    
    class_name Dragon
    extends FlyingEnemy  # Inherits from Enemy -> Character -> Entity
    
    # Changes to any parent class ripple down
    # Hard to understand what Dragon actually does
    
  #### **Good Example**
    # GOOD: Composition
    # Dragon scene contains:
    # - CharacterBody3D (root)
    #   - HealthComponent
    #   - MovementComponent (flying behavior)
    #   - AIComponent
    #   - AttackComponent (fire breath)
    
    # Each component is a separate, reusable scene
    # Easy to mix and match behaviors
    
### **Autoload Abuse**
  #### **Name**
Putting Everything in Autoloads
  #### **Description**
    Don't use autoloads as a dumping ground. They create tight coupling
    and make testing difficult.
    
  #### **Bad Example**
    # BAD: Global.gd autoload with everything
    extends Node
    
    var player_health: int = 100
    var player_mana: int = 50
    var inventory: Array = []
    var current_level: int = 1
    var settings: Dictionary = {}
    var highscores: Array = []
    # ... 500 more lines
    
  #### **Good Example**
    # GOOD: Separate autoloads with single responsibility
    # GameState - current run state
    # SaveManager - persistence
    # AudioManager - sound
    # EventBus - global signals
    
    # Better: Store state on actual game objects
    # Player has health, inventory
    # Level has enemies, items
    # Use Resources for shared data
    
### **String Node Paths**
  #### **Name**
Hardcoded String Node Paths
  #### **Description**
    Avoid hardcoded node paths that break when scene structure changes.
    Use groups, exports, or unique names (%NodeName).
    
  #### **Bad Example**
    # BAD: Breaks if hierarchy changes
    var enemy = get_node("../../Enemies/Spawner/Enemy1")
    
  #### **Good Example**
    # GOOD: Use groups
    var enemies = get_tree().get_nodes_in_group("enemies")
    
    # GOOD: Use unique names (set % in editor)
    @onready var spawner: Node = %EnemySpawner
    
    # GOOD: Export and assign in editor
    @export var enemy_spawner: Node
    
### **Mixing Physics Frames**
  #### **Name**
Physics in _process
  #### **Description**
    Physics operations must be in _physics_process for deterministic behavior.
    _process runs at variable framerate.
    
  #### **Bad Example**
    # BAD: Physics in _process - framerate dependent
    func _process(delta: float) -> void:
        velocity += Vector2(0, gravity) * delta
        move_and_slide()
    
  #### **Good Example**
    # GOOD: Physics in _physics_process - fixed timestep
    func _physics_process(delta: float) -> void:
        velocity += Vector2(0, gravity) * delta
        move_and_slide()
    
    # Use _process for:
    # - Visual updates (animations, UI)
    # - Non-physics input handling
    # - Timers that don't affect gameplay
    