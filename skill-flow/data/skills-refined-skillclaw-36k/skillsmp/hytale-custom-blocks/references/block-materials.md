# Block Materials Reference

Complete reference for Hytale block material types and their properties.

## Material Types

| Material | Hardness | Tool | Blast Resist | Description |
|----------|----------|------|--------------|-------------|
| `Air` | 0 | - | 0 | Empty space |
| `Stone` | 4 | Pickaxe | 30 | Hard rock materials |
| `Dirt` | 1 | Shovel | 2.5 | Soft earth |
| `Sand` | 0.5 | Shovel | 2.5 | Loose granular |
| `Gravel` | 0.6 | Shovel | 3 | Rocky loose |
| `Wood` | 2 | Axe | 10 | Organic wood |
| `Leaves` | 0.2 | Shears | 1 | Plant foliage |
| `Grass` | 0.6 | Shovel | 3 | Grass-covered dirt |
| `Clay` | 0.6 | Shovel | 3 | Wet clay |
| `Metal` | 5 | Pickaxe | 50 | Metallic blocks |
| `Glass` | 0.3 | - | 1.5 | Fragile glass |
| `Ice` | 0.5 | Pickaxe | 2.5 | Frozen water |
| `Snow` | 0.2 | Shovel | 1 | Soft snow |
| `Wool` | 0.8 | Shears | 4 | Fabric blocks |
| `Slime` | 0 | - | 0 | Bouncy gel |
| `Coral` | 1.5 | Pickaxe | 15 | Underwater coral |
| `Crystal` | 3 | Pickaxe | 25 | Crystal formations |
| `Bone` | 2 | Pickaxe | 10 | Skeletal material |
| `Flesh` | 0.5 | Sword | 2 | Organic tissue |
| `Plant` | 0 | Hoe | 0 | Crops and plants |
| `Web` | 4 | Sword | 2 | Spider webs |
| `Obsidian` | 50 | Pickaxe | 6000 | Extremely hard |
| `Bedrock` | -1 | - | 18000000 | Unbreakable |

## Material Properties

### Hardness

Determines break time:

```
BreakTime = Hardness * 1.5 / ToolSpeed
```

- `0` = Instant break
- `1-3` = Soft blocks
- `4-10` = Medium blocks
- `10+` = Hard blocks
- `-1` = Unbreakable

### Blast Resistance

Explosion damage resistance:

```
DamageReduction = BlastResistance / ExplosionPower
```

- `0-5` = Destroyed by any explosion
- `5-30` = Survives weak explosions
- `30-100` = Survives medium explosions
- `100+` = Survives strong explosions
- `18000000` = Explosion proof

### Preferred Tool

| Tool | Materials |
|------|-----------|
| Pickaxe | Stone, Metal, Ice, Crystal, Bone, Coral, Obsidian |
| Axe | Wood |
| Shovel | Dirt, Sand, Gravel, Grass, Clay, Snow |
| Shears | Leaves, Wool, Web |
| Hoe | Plant |
| Sword | Flesh, Web |
| None | Air, Glass, Slime |

## Tool Power Levels

Tools have power levels that determine what they can mine:

| Tool Level | Quality | Example | Can Mine |
|------------|---------|---------|----------|
| 0 | Hand | Bare hands | Dirt, Sand, Wood |
| 1 | Wood | Wooden Pickaxe | Stone, Coal |
| 2 | Stone | Stone Pickaxe | Iron, Copper |
| 3 | Iron | Iron Pickaxe | Gold, Redstone |
| 4 | Diamond | Diamond Pickaxe | Diamond, Obsidian |
| 5 | Mythril | Mythril Pickaxe | All blocks |

## Custom Material Definition

Define custom materials in your plugin:

```json
{
  "Material": "MyPlugin:CustomMaterial",
  "CustomMaterialProperties": {
    "Hardness": 3.5,
    "BlastResistance": 20,
    "PreferredTool": "Pickaxe",
    "RequiredToolLevel": 2,
    "SoundType": "Stone",
    "MapColor": "#4a4a4a"
  }
}
```

## Sound Types by Material

| Material | Step | Break | Place | Hit |
|----------|------|-------|-------|-----|
| Stone | Hard click | Crumble | Thud | Click |
| Wood | Hollow thud | Crack | Knock | Tap |
| Dirt | Soft thud | Crumble | Pat | Thump |
| Sand | Shuffle | Swoosh | Pat | Scrape |
| Metal | Clang | Clatter | Clang | Ring |
| Glass | Clink | Shatter | Clink | Ting |
| Grass | Rustle | Tear | Pat | Rustle |
| Snow | Crunch | Poof | Poof | Crunch |
| Wool | Soft thud | Tear | Flump | Thud |

## Particle Effects by Material

| Material | Break Particles | Step Particles |
|----------|-----------------|----------------|
| Stone | Gray dust | None |
| Dirt | Brown dust | None |
| Sand | Tan particles | Puff on land |
| Wood | Wood chips | None |
| Glass | Glass shards | None |
| Leaves | Leaf bits | None |
| Snow | Snow puff | Snow puff |
| Grass | Green particles | None |

## Block State Interactions with Materials

Some materials have special state behaviors:

### Gravity Materials

```
Sand, Gravel, Concrete Powder
- Fall when unsupported
- Can suffocate entities
```

### Fluid-Reactive Materials

```
Sand + Water = Wet Sand
Lava + Water = Obsidian/Cobblestone
Ice + Heat = Water
```

### Light-Reactive Materials

```
Grass - Requires light to spread
Crops - Require light to grow
Ice - Melts in high light
Snow - Melts in high light
```

## Material Flags

Additional boolean properties:

| Flag | Description |
|------|-------------|
| `IsTransparent` | Light passes through |
| `IsFlammable` | Can catch fire |
| `IsLiquid` | Flows like fluid |
| `IsReplaceable` | Can be overwritten |
| `IsClimbable` | Can be climbed |
| `IsBouncy` | Bounces entities |
| `IsSlippery` | Ice-like movement |
| `IsSuffocating` | Damages in block |
