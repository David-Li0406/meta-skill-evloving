---
name: optimization
description: Implements optimization techniques for rendering, scripting, memory, and physics performance. Use when improving game performance for release.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Performance Optimization

When optimizing games, follow these patterns for better performance across all platforms.

## Rendering Optimization

### Occlusion Culling
```gdscript
extends Node3D

# Manual occlusion for complex scenes
var occluders: Array[OccluderInstance3D] = []

func setup_occluders() -> void:
    for mesh in get_tree().get_nodes_in_group("static_geometry"):
        if mesh is MeshInstance3D and mesh.mesh:
            var occluder := OccluderInstance3D.new()
            # Generate occluder from mesh
            occluder.occluder = mesh.mesh.create_convex_shape()
            occluder.global_transform = mesh.global_transform
            add_child(occluder)
            occluders.append(occluder)
```

### LOD (Level of Detail)
```gdscript
extends MeshInstance3D

@export var lod_meshes: Array[Mesh]
@export var lod_distances: Array[float] = [20.0, 50.0, 100.0]

var camera: Camera3D

func _ready() -> void:
    camera = get_viewport().get_camera_3d()

func _process(_delta: float) -> void:
    if not camera:
        return

    var distance := global_position.distance_to(camera.global_position)
    update_lod(distance)

func update_lod(distance: float) -> void:
    for i in range(lod_distances.size()):
        if distance < lod_distances[i]:
            if i < lod_meshes.size():
                mesh = lod_meshes[i]
            return

    # Furthest LOD
    if lod_meshes.size() > 0:
        mesh = lod_meshes[-1]

# Using GeometryInstance3D built-in LOD
func setup_builtin_lod() -> void:
    # Set LOD bias (lower = more aggressive LOD)
    lod_bias = 1.0

    # Visibility range (hide at distance)
    visibility_range_begin = 0.0
    visibility_range_end = 100.0
    visibility_range_fade_mode = GeometryInstance3D.VISIBILITY_RANGE_FADE_SELF
```

### Instancing for Repeated Objects
```gdscript
extends Node3D

@export var instance_mesh: Mesh
@export var instance_count := 1000

var multimesh_instance: MultiMeshInstance3D

func _ready() -> void:
    setup_multimesh()

func setup_multimesh() -> void:
    var multimesh := MultiMesh.new()
    multimesh.mesh = instance_mesh
    multimesh.transform_format = MultiMesh.TRANSFORM_3D
    multimesh.instance_count = instance_count

    # Set transforms
    for i in range(instance_count):
        var transform := Transform3D()
        transform.origin = Vector3(
            randf_range(-100, 100),
            0,
            randf_range(-100, 100)
        )
        multimesh.set_instance_transform(i, transform)

    multimesh_instance = MultiMeshInstance3D.new()
    multimesh_instance.multimesh = multimesh
    add_child(multimesh_instance)

# Animating multimesh instances
func _process(_delta: float) -> void:
    var mm := multimesh_instance.multimesh
    for i in range(mm.instance_count):
        var transform := mm.get_instance_transform(i)
        transform = transform.rotated(Vector3.UP, 0.01)
        mm.set_instance_transform(i, transform)
```

### Shader Optimization
```gdshader
shader_type spatial;

// GOOD: Use uniforms for values that change rarely
uniform vec4 base_color : source_color;

// GOOD: Use constants for fixed values
const float PI = 3.14159;

// AVOID: Complex calculations in fragment shader
// Move to vertex shader when possible

void vertex() {
    // Pre-calculate values here
}

void fragment() {
    // GOOD: Use built-in functions
    vec3 normalized = normalize(NORMAL);

    // AVOID: Multiple texture samples when possible
    vec4 tex = texture(TEXTURE, UV);
    // Reuse tex instead of sampling again

    // GOOD: Use step/smoothstep instead of if statements
    float factor = step(0.5, UV.x);

    // AVOID: pow() with non-constant exponents
    // Use approximations when possible

    ALBEDO = base_color.rgb * tex.rgb;
}
```

## Script Optimization

### Object Pooling
```gdscript
class_name ObjectPool
extends Node

var pool: Array[Node] = []
var scene: PackedScene
var pool_size: int
var active_count := 0

func _init(packed_scene: PackedScene, size: int) -> void:
    scene = packed_scene
    pool_size = size

func _ready() -> void:
    # Pre-instantiate objects
    for i in range(pool_size):
        var obj := scene.instantiate()
        obj.process_mode = Node.PROCESS_MODE_DISABLED
        obj.hide()
        add_child(obj)
        pool.append(obj)

func get_object() -> Node:
    for obj in pool:
        if obj.process_mode == Node.PROCESS_MODE_DISABLED:
            obj.process_mode = Node.PROCESS_MODE_INHERIT
            obj.show()
            active_count += 1
            return obj

    # Pool exhausted, create new (or return null)
    var obj := scene.instantiate()
    add_child(obj)
    pool.append(obj)
    active_count += 1
    return obj

func return_object(obj: Node) -> void:
    obj.process_mode = Node.PROCESS_MODE_DISABLED
    obj.hide()
    active_count -= 1
    # Reset object state here

func get_active_count() -> int:
    return active_count
```

### Avoiding Unnecessary Processing
```gdscript
extends Node2D

var is_on_screen := true

func _ready() -> void:
    # Use visibility notifier
    var notifier := VisibleOnScreenNotifier2D.new()
    notifier.screen_entered.connect(_on_screen_entered)
    notifier.screen_exited.connect(_on_screen_exited)
    add_child(notifier)

func _on_screen_entered() -> void:
    is_on_screen = true
    set_process(true)
    set_physics_process(true)

func _on_screen_exited() -> void:
    is_on_screen = false
    set_process(false)
    set_physics_process(false)

func _process(delta: float) -> void:
    # Only runs when on screen
    update_visuals(delta)
```

### Caching References
```gdscript
extends CharacterBody2D

# BAD: Finding nodes every frame
func _process(_delta: float) -> void:
    var player := get_tree().get_first_node_in_group("player")  # Slow!
    var health := get_node("UI/HealthBar")  # Repeated lookup

# GOOD: Cache references
@onready var player: Node2D = get_tree().get_first_node_in_group("player")
@onready var health_bar: ProgressBar = $UI/HealthBar

func _process(_delta: float) -> void:
    if player:
        # Use cached reference
        pass
```

### Efficient Loops
```gdscript
# BAD: Creating arrays in loops
func _process(_delta: float) -> void:
    var nearby := []  # Created every frame
    for enemy in enemies:
        if enemy.position.distance_to(position) < 100:
            nearby.append(enemy)

# GOOD: Reuse arrays
var nearby: Array[Node2D] = []

func _process(_delta: float) -> void:
    nearby.clear()
    for enemy in enemies:
        if enemy.global_position.distance_squared_to(global_position) < 10000:  # squared is faster
            nearby.append(enemy)

# GOOD: Use built-in methods when available
func get_closest_enemy() -> Node2D:
    var closest: Node2D
    var closest_dist := INF

    for enemy in enemies:
        var dist := global_position.distance_squared_to(enemy.global_position)
        if dist < closest_dist:
            closest_dist = dist
            closest = enemy

    return closest
```

### Signal vs Direct Calls
```gdscript
# Signals are great for decoupling but have overhead
# For hot paths, consider direct calls

# BAD for hot path:
signal position_changed(pos: Vector2)

func _physics_process(_delta: float) -> void:
    move_and_slide()
    position_changed.emit(global_position)  # Signal overhead each frame

# GOOD for hot path:
var position_listener: Node

func _physics_process(_delta: float) -> void:
    move_and_slide()
    if position_listener:
        position_listener.on_position_updated(global_position)  # Direct call
```

## Physics Optimization

### Collision Layers
```gdscript
# Optimize by using appropriate collision layers
# Only check collisions that matter

# Example layer setup:
# Layer 1: World geometry
# Layer 2: Player
# Layer 3: Enemies
# Layer 4: Projectiles
# Layer 5: Pickups

func setup_projectile(projectile: Area2D) -> void:
    projectile.collision_layer = 4  # Is on projectile layer
    projectile.collision_mask = 1 | 3  # Collides with world and enemies only
    # Doesn't check player, other projectiles, or pickups
```

### Physics Process Optimization
```gdscript
extends CharacterBody2D

# Reduce physics checks when not needed
var is_active := true

func _physics_process(delta: float) -> void:
    if not is_active:
        return

    # Only process when necessary
    if not is_on_screen:
        return

    move_and_slide()

# Use Area2D instead of constant raycasting
@onready var detection_area: Area2D = $DetectionArea

func _ready() -> void:
    detection_area.body_entered.connect(_on_body_entered)
    # Much more efficient than raycasting every frame
```

### Spatial Partitioning
```gdscript
class_name SpatialGrid
extends RefCounted

var cell_size: float
var cells: Dictionary = {}  # Vector2i -> Array[Node2D]

func _init(size: float) -> void:
    cell_size = size

func get_cell(position: Vector2) -> Vector2i:
    return Vector2i(
        int(position.x / cell_size),
        int(position.y / cell_size)
    )

func add_object(obj: Node2D) -> void:
    var cell := get_cell(obj.global_position)
    if not cells.has(cell):
        cells[cell] = []
    cells[cell].append(obj)

func remove_object(obj: Node2D) -> void:
    var cell := get_cell(obj.global_position)
    if cells.has(cell):
        cells[cell].erase(obj)

func get_nearby(position: Vector2, radius: float) -> Array[Node2D]:
    var result: Array[Node2D] = []
    var cell := get_cell(position)
    var cell_radius := int(ceil(radius / cell_size))

    for x in range(-cell_radius, cell_radius + 1):
        for y in range(-cell_radius, cell_radius + 1):
            var check_cell := cell + Vector2i(x, y)
            if cells.has(check_cell):
                for obj in cells[check_cell]:
                    if obj.global_position.distance_to(position) <= radius:
                        result.append(obj)

    return result
```

## Memory Management

### Resource Preloading vs Loading
```gdscript
# Preload for small, frequently used resources
const BULLET_SCENE := preload("res://bullet.tscn")
const EXPLOSION_SOUND := preload("res://sfx/explosion.ogg")

# Load dynamically for large or rarely used resources
var boss_scene: PackedScene

func load_boss_async() -> void:
    ResourceLoader.load_threaded_request("res://boss.tscn")

func _process(_delta: float) -> void:
    var status := ResourceLoader.load_threaded_get_status("res://boss.tscn")
    if status == ResourceLoader.THREAD_LOAD_LOADED:
        boss_scene = ResourceLoader.load_threaded_get("res://boss.tscn")
```

### Freeing Resources
```gdscript
extends Node

func cleanup() -> void:
    # Explicitly free large resources
    for child in get_children():
        child.queue_free()

    # Clear references
    large_texture = null
    cached_data.clear()

# Use weak references when appropriate
var weak_ref: WeakRef

func set_target(target: Node) -> void:
    weak_ref = weakref(target)

func get_target() -> Node:
    if weak_ref:
        return weak_ref.get_ref()
    return null
```

## Profiling

### Built-in Profiler Usage
```gdscript
extends Node

func expensive_operation() -> void:
    # Add profiling markers
    var start := Time.get_ticks_usec()

    # ... expensive code ...

    var elapsed := Time.get_ticks_usec() - start
    print("Operation took: %d microseconds" % elapsed)

# Use _physics_process for consistent timing
var frame_times: Array[float] = []

func _physics_process(delta: float) -> void:
    frame_times.append(delta)
    if frame_times.size() > 60:
        frame_times.pop_front()

func get_average_frame_time() -> float:
    if frame_times.is_empty():
        return 0
    var total := 0.0
    for t in frame_times:
        total += t
    return total / frame_times.size()

func get_fps() -> float:
    var avg := get_average_frame_time()
    return 1.0 / avg if avg > 0 else 0
```

### Debug Display
```gdscript
extends CanvasLayer

@onready var label: Label = $DebugLabel

func _process(_delta: float) -> void:
    if not OS.is_debug_build():
        return

    var fps := Engine.get_frames_per_second()
    var memory := OS.get_static_memory_usage() / 1048576.0  # MB

    label.text = "FPS: %d\nMemory: %.1f MB\nObjects: %d" % [
        fps,
        memory,
        Performance.get_monitor(Performance.OBJECT_COUNT)
    ]
```

## Platform-Specific Optimization

### Mobile Optimization
```gdscript
extends Node

func _ready() -> void:
    if OS.has_feature("mobile"):
        apply_mobile_settings()

func apply_mobile_settings() -> void:
    # Reduce quality
    get_viewport().msaa_2d = Viewport.MSAA_DISABLED
    get_viewport().msaa_3d = Viewport.MSAA_DISABLED

    # Reduce shadow quality
    RenderingServer.directional_shadow_atlas_set_size(1024, true)

    # Lower physics tick rate if acceptable
    Engine.physics_ticks_per_second = 30

    # Disable expensive effects
    $PostProcessing.visible = false
```

### Web Optimization
```gdscript
extends Node

func _ready() -> void:
    if OS.has_feature("web"):
        apply_web_settings()

func apply_web_settings() -> void:
    # Reduce initial load
    # Use smaller textures
    # Compress audio

    # Handle browser focus
    get_tree().auto_accept_quit = false

func _notification(what: int) -> void:
    if what == NOTIFICATION_WM_WINDOW_FOCUS_OUT:
        # Pause when browser tab loses focus
        get_tree().paused = true
    elif what == NOTIFICATION_WM_WINDOW_FOCUS_IN:
        get_tree().paused = false
```
