---
name: game-performance-optimization
description: Use this skill when optimizing game performance across rendering, scripting, memory, and physics to ensure smooth gameplay on all devices.
---

# Skill body

When optimizing games, follow these patterns for better performance across all platforms.

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
            # Generate occluder from mesh
            occluder.occluder = mesh.mesh.create_convex_shape()
            occluder.global_transform = mesh.global_transform
            add_child(occluder)
            occluders.append(occluder)
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
        -- Set individual transforms for each instance
```

### Streaming Enabled
```lua
-- Enable instance streaming for large worlds
workspace.StreamingEnabled = true
```