---
name: procedural-generation
description: Use this skill when creating procedurally generated content such as terrain, dungeons, or cities using various noise functions and generation techniques.
---

# Skill body

## Noise-Based Generation

### Using FastNoiseLite (Godot)
```gdscript
extends Node2D

var noise := FastNoiseLite.new()

func _ready() -> void:
    noise.noise_type = FastNoiseLite.TYPE_PERLIN
    noise.seed = randi()
    noise.frequency = 0.02

func get_height_at(x: float, y: float) -> float:
    return noise.get_noise_2d(x, y)

func get_normalized_height(x: float, y: float) -> float:
    return (noise.get_noise_2d(x, y) + 1.0) / 2.0
```

### Multi-Octave Perlin Noise (Roblox)
```lua
local function octaveNoise(x, y, octaves, persistence, scale, lacunarity)
    octaves = octaves or 4
    persistence = persistence or 0.5
    scale = scale or 1
    lacunarity = lacunarity or 2

    local total = 0
    local frequency = scale
    local amplitude = 1
    local maxValue = 0

    for i = 1, octaves do
        total = total + math.noise(x * frequency, y * frequency) * amplitude
        maxValue = maxValue + amplitude
        amplitude = amplitude * persistence
        frequency = frequency * lacunarity
    end

    return total / maxValue  -- Normalize to [-1, 1]
end
```

## Terrain Generation

### Terrain Generation with Multiple Noise Layers (Godot)
```gdscript
extends Node3D

var base_noise := FastNoiseLite.new()
var detail_noise := FastNoiseLite.new()
var moisture_noise := FastNoiseLite.new()

@export var terrain_size := Vector2i(100, 100)
@export var height_scale := 20.0

func _ready() -> void:
    setup_noise()
    generate_terrain()

func setup_noise() -> void:
    var seed_value := randi()
    base_noise.seed = seed_value
    base_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    base_noise.frequency = 0.005
    base_noise.fractal_type = FastNoiseLite.FRACTAL_FBM
    base_noise.fractal_octaves = 5

    detail_noise.seed = seed_value + 1
    detail_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    detail_noise.frequency = 0.05
    detail_noise.fractal_octaves = 3

    moisture_noise.seed = seed_value + 2
    moisture_noise.noise_type = FastNoiseLite.TYPE_PERLIN
    moisture_noise.frequency = 0.01

func get_terrain_height(x: float, z: float) -> float:
    var base := base_noise.get_noise_2d(x, z)
    var detail := detail_noise.get_noise_2d(x, z) * 0.3
    return (base + detail) * height_scale
```

### Usage for Terrain (Roblox)
```lua
local function getTerrainHeight(x, z)
    local baseHeight = octaveNoise(x, z, 4, 0.5, 0.01) * 50
    local detail = octaveNoise(x, z, 2, 0.5, 0.1) * 5
    return baseHeight + detail + 10
end
```

## Additional Techniques

### Domain Warping (Roblox)
```lua
local function warpedNoise(x, y, scale, warpStrength)
    local warpX = math.noise(x * scale, y * scale, 0) * warpStrength
    local warpY = math.noise(x * scale, y * scale, 100) * warpStrength
    return math.noise((x + warpX) * scale, (y + warpY) * scale)
end
```

### Ridged Noise (Roblox)
```lua
local function ridgedNoise(x, y, octaves, scale)
    local total = 0
    local frequency = scale
    local amplitude = 1
    local weight = 1

    for i = 1, octaves do
        local noise = math.noise(x * frequency, y * frequency)
        noise = 1 - math.abs(noise)
        noise = noise * noise
        noise = noise * weight
        weight = math.clamp(noise * 2, 0, 1)

        total = total + noise * amplitude
    end
    return total
end
```