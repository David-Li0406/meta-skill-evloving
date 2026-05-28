---
name: optimization
description: Implements optimization techniques for rendering, scripting, memory, physics, and networking performance. Use when improving game performance across various platforms.
---

# Game Performance Optimization

When optimizing games, follow these patterns for better performance across all devices.

## Rendering Optimization

### Part Count Reduction
```lua
-- Combine multiple parts into unions or meshes
local function combineStaticParts(model)
    local parts = {}
    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") and part.Anchored then
            table.insert(parts, part)
        end
    end

    if #parts > 1 then
        local union = parts[1]:UnionAsync(parts, Enum.CollisionFidelity.Box)
        union.Name = model.Name .. "_Combined"
        union.Parent = model.Parent

        for _, part in ipairs(parts) do
            part:Destroy()
        end

        return union
    end
end
```

### Level of Detail (LOD)
```lua
local LODManager = {}
local LOD_DISTANCES = {50, 100, 200}  -- Distance thresholds

function LODManager.setup(model)
    local lodLevels = {
        model:FindFirstChild("LOD0"),  -- Highest detail
        model:FindFirstChild("LOD1"),
        model:FindFirstChild("LOD2"),
        model:FindFirstChild("LOD3")   -- Lowest detail
    }

    local function updateLOD()
        local camera = workspace.CurrentCamera
        local distance = (model.PrimaryPart.Position - camera.CFrame.Position).Magnitude

        local activeLOD = 1
        for i, threshold in ipairs(LOD_DISTANCES) do
            if distance > threshold then
                activeLOD = i + 1
            end
        end

        for i, lod in ipairs(lodLevels) do
            if lod then
                lod.Visible = (i == activeLOD)
            end
        end
    end

    RunService.RenderStepped:Connect(updateLOD)
end
```

### Occlusion Culling
```gdscript
extends Node3D

# Manual occlusion for complex scenes
var occluders: Array[OccluderInstance3D] = []

func setup_occluders() -> void:
    for mesh in get_tree().get_nodes_in_group("static_geometry"):
        if mesh is MeshInstance3D and mesh.mesh:
            var occluder := OccluderInstance3D.new()
            occluder.occluder = mesh.mesh.create_convex_shape()
            occluder.global_transform = mesh.global_transform
            add_child(occluder)
            occluders.append(occluder)
```

### Texture Optimization
```lua
-- Use appropriate texture sizes
-- Mobile: 256x256 or 512x512
-- Desktop: 512x512 or 1024x1024 max

-- Reduce unique materials
local function consolidateMaterials(model)
    local materials = {}
    for _, part in ipairs(model:GetDescendants()) do
        if part:IsA("BasePart") then
            local key = tostring(part.Material) .. "_" .. tostring(part.Color)
            materials[key] = (materials[key] or 0) + 1
        end
    end
    -- Identify and consolidate similar materials
end
```

## Script Optimization

### Avoid wait() and Use task Library
```lua
-- BAD: Uses deprecated wait()
wait(1)
spawn(function() ... end)
delay(1, function() ... end)

-- GOOD: Use task library
task.wait(1)
task.spawn(function() ... end)
task.delay(1, function() ... end)
```

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
```

### Caching and Avoiding Repeated Lookups
```lua
-- BAD: Repeated FindFirstChild every frame
RunService.Heartbeat:Connect(function()
    local hrp = player.Character:FindFirstChild("HumanoidRootPart")
    local humanoid = player.Character:FindFirstChildOfClass("Humanoid")
    -- ...
end)

-- GOOD: Cache references
local character, hrp, humanoid

local function cacheCharacter()
    character = player.Character
    if character then
        hrp = character:WaitForChild("HumanoidRootPart")
        humanoid = character:WaitForChild("Humanoid")
    end
end

player.CharacterAdded:Connect(cacheCharacter)
cacheCharacter()

RunService.Heartbeat:Connect(function()
    if hrp then
        -- Use cached reference
    end
end)
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

## Memory Optimization

### Instance Destruction
```lua
-- Properly destroy instances to free memory
local function cleanup(instance)
    -- Disconnect all connections first
    for _, connection in ipairs(instance:GetConnections()) do
        connection:Disconnect()
    end

    -- Clear attributes
    for _, attr in ipairs(instance:GetAttributes()) do
        instance:SetAttribute(attr, nil)
    end

    instance:Destroy()
end
```

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

## Physics Optimization

### Collision Groups
```lua
local PhysicsService = game:GetService("PhysicsService")

-- Create collision groups
PhysicsService:RegisterCollisionGroup("Players")
PhysicsService:RegisterCollisionGroup("Enemies")
PhysicsService:RegisterCollisionGroup("Projectiles")
PhysicsService:RegisterCollisionGroup("Debris")

-- Disable unnecessary collisions
PhysicsService:CollisionGroupSetCollidable("Players", "Players", false)
PhysicsService:CollisionGroupSetCollidable("Projectiles", "Projectiles", false)
PhysicsService:CollisionGroupSetCollidable("Debris", "Debris", false)
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
```

## Network Optimization

### Minimize RemoteEvent Traffic
```lua
-- BAD: Fire every frame
RunService.Heartbeat:Connect(function()
    PositionRemote:FireServer(hrp.Position)
end)

-- GOOD: Throttle updates
local lastUpdate = 0
local UPDATE_RATE = 1/20  -- 20 updates per second

RunService.Heartbeat:Connect(function()
    local now = os.clock()
    if now - lastUpdate >= UPDATE_RATE then
        lastUpdate = now
        PositionRemote:FireServer(hrp.Position)
    end
end)
```

### Data Compression
```lua
-- Quantize positions to reduce data size
local function quantizeVector3(v, precision)
    precision = precision or 0.1
    return Vector3.new(
        math.floor(v.X / precision) * precision,
        math.floor(v.Y / precision) * precision,
        math.floor(v.Z / precision) * precision
    )
end
```

## Profiling Tools

### MicroProfiler
```lua
-- Use debug.profilebegin/end for custom profiling
debug.profilebegin("MyExpensiveFunction")
-- ... expensive code ...
debug.profileend()
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
```