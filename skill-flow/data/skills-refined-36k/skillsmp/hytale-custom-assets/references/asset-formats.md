# Hytale Asset Formats Reference

Complete reference for asset file formats in the Hytale server.

## File Types Overview

| Extension | Type | Description |
|-----------|------|-------------|
| `.blockymodel` | Model | 3D model format for entities, items, blocks |
| `.blockyanim` | Animation | Animation data for blocky models |
| `.png` | Texture | Image textures (primary format) |
| `.svg` | Vector | SVG format for UI elements |
| `.ogg` | Audio | Ogg Vorbis audio format |
| `.json` | Data | JSON configuration files |

---

## Model Format (.blockymodel)

JSON-based 3D model files with hierarchical structure.

### Model Properties

| Property | Type | Description |
|----------|------|-------------|
| `path` | String | Path to .blockymodel file |
| `texture` | String | Path to texture file (.png) |
| `gradientSet` | String | Gradient set reference |
| `gradientId` | String | Specific gradient ID |
| `scale` | Float | Scale multiplier (default: 1.0) |
| `eyeHeight` | Float | Eye point height for entities |
| `crouchOffset` | Float | Vertical offset when crouching |
| `animationSets` | Map | Animation set mappings |
| `attachments` | Array | Model attachments |
| `hitbox` | Box | Bounding box for collision |
| `light` | ColorLight | Light emission properties |
| `particles` | Array | Attached particle systems |
| `trails` | Array | Trail effects |
| `camera` | CameraSettings | First-person camera config |
| `detailBoxes` | Map | Detail collision boxes |
| `phobia` | Enum | Phobia classification |
| `phobiaModel` | Model | Alternative for phobia mode |

### Model Path Requirements

| Category | Required Roots |
|----------|----------------|
| Item Models | `Blocks/`, `Items/`, `Resources/`, `NPC/`, `VFX/`, `Consumable/` |
| Character Models | `Characters/`, `NPC/`, `Items/`, `VFX/` |
| Attachment Models | `Characters/`, `NPC/`, `Items/`, `Cosmetics/`, `Resources/` |

### Model Attachment

```json
{
  "model": "Items/Weapons/Sword.blockymodel",
  "texture": "Items/Weapons/Sword.png",
  "gradientSet": "Metal_Iron",
  "gradientId": "default",
  "weight": 1.0
}
```

---

## Animation Format (.blockyanim)

JSON files with keyframe-based animation data.

### Animation Properties

| Property | Type | Description |
|----------|------|-------------|
| `duration` | Integer | Duration in frames (60 FPS) |

### Frame Rate

```java
FRAMES_PER_SECOND = 60.0

// Duration calculations
durationMillis = duration * 1000.0 / 60.0
durationSeconds = duration / 60.0
```

### Animation Path Requirements

| Category | Required Roots |
|----------|----------------|
| Item/Character | `Characters/`, `NPC/` |
| Block | `Blocks/`, `Items/`, `Resources/`, `NPC/`, `VFX/`, `Consumable/` |
| Equipment | `Characters/`, `NPC/`, `Equipment/`, `VFX/`, `Items/` |

---

## Sound Format (.ogg)

Ogg Vorbis audio files.

### Audio Requirements

| Type | Channels | Usage |
|------|----------|-------|
| Mono | 1 | 3D positional audio (required) |
| Stereo | 2 | Music, ambient sounds |

### SoundEvent Structure

```json
{
  "id": "Blocks/Wood_Break",
  "volume": 0.0,
  "pitch": 0.0,
  "musicDuckingVolume": -6.0,
  "ambientDuckingVolume": 0.0,
  "startAttenuationDistance": 2.0,
  "maxDistance": 16.0,
  "maxInstance": 10,
  "preventSoundInterruption": false,
  "layers": [...],
  "audioCategoryId": "SFX"
}
```

### SoundEventLayer

```json
{
  "volume": 0.0,
  "startDelay": 0.0,
  "looping": false,
  "probability": 100,
  "probabilityRerollDelay": 0.0,
  "files": ["Sounds/Blocks/Wood_Break_1.ogg", "Sounds/Blocks/Wood_Break_2.ogg"],
  "roundRobinHistorySize": 2,
  "randomSettings": {
    "minVolume": -2.0,
    "maxVolume": 2.0,
    "minPitch": -1.0,
    "maxPitch": 1.0,
    "maxStartOffset": 0.0
  }
}
```

### Volume/Pitch Ranges

| Property | Range | Unit |
|----------|-------|------|
| Volume | -100 to +10 | Decibels |
| Pitch | -12 to +12 | Semitones |
| Ducking | -100 to 0 | Decibels |

---

## Particle System Format

### ParticleSystem Structure

```json
{
  "id": "Effects/Fire",
  "lifeSpan": 2.0,
  "spawners": [...],
  "cullDistance": 50.0,
  "boundingRadius": 5.0,
  "isImportant": false
}
```

### ParticleSpawner

```json
{
  "id": "main",
  "shape": "Sphere",
  "emitOffset": { "min": [0,0,0], "max": [0.5,0.5,0.5] },
  "useEmitDirection": false,
  "totalParticles": { "min": 10, "max": 20 },
  "lifeSpan": 2.0,
  "maxConcurrentParticles": 100,
  "particleLifeSpan": { "min": 0.5, "max": 1.0 },
  "spawnRate": { "min": 10, "max": 20 },
  "spawnBurst": false,
  "waveDelay": { "min": 0, "max": 0 },
  "renderMode": "BlendLinear",
  "lightInfluence": 0.5,
  "linearFiltering": true,
  "cameraOffset": 0.0,
  "isLowRes": false,
  "particle": {...}
}
```

### Particle Properties

```json
{
  "texture": "Particles/Fire.png",
  "frameSize": { "width": 64, "height": 64 },
  "uvOption": "Random",
  "scaleRatioConstraint": "None",
  "softParticle": "Enable",
  "softParticlesFadeFactor": 1.0,
  "useSpriteBlending": true,
  "animation": {
    "0": { "scale": [1,1], "rotation": [0,0,0], "opacity": 1.0 },
    "50": { "scale": [1.5,1.5], "opacity": 0.8 },
    "100": { "scale": [2,2], "opacity": 0.0 }
  }
}
```

---

## Trail Format

### Trail Structure

```json
{
  "id": "Weapons/Sword_Trail",
  "texture": "Trails/Sword.png",
  "lifeSpan": 200,
  "roll": 0.0,
  "lightInfluence": 0.5,
  "renderMode": "BlendLinear",
  "smooth": true,
  "start": { "width": 0.1, "color": [255,255,255,255] },
  "end": { "width": 0.0, "color": [255,255,255,0] },
  "animation": {
    "frameSize": [64, 64],
    "frameRange": { "min": 0, "max": 4 },
    "frameLifeSpan": 50
  }
}
```

---

## Block Textures

### BlockTypeTextures Structure

```json
{
  "up": "BlockTextures/Grass_Top.png",
  "down": "BlockTextures/Dirt.png",
  "north": "BlockTextures/Grass_Side.png",
  "south": "BlockTextures/Grass_Side.png",
  "east": "BlockTextures/Grass_Side.png",
  "west": "BlockTextures/Grass_Side.png",
  "weight": 1
}
```

### Shorthand Properties

| Property | Sets Faces |
|----------|------------|
| `All` | All six faces |
| `Sides` | north, south, east, west |
| `UpDown` | up, down |

### Default Textures

```
Unknown: BlockTextures/Unknown.png
Debug: BlockTextures/_Debug/{Up,Down,North,South,East,West}.png
```

---

## Texture Specifications

### Texture Path Requirements

| Category | Required Roots |
|----------|----------------|
| Item/Block | `Blocks/`, `BlockTextures/`, `Items/`, `NPC/`, `Resources/`, `VFX/` |
| Character | `Characters/`, `NPC/`, `Items/`, `VFX/` |
| Trail | `Trails/` |
| Sky | `Sky/` |
| Particle | `Particles/` |
| UI Quality | `UI/ItemQualities/` |
| Resource Icons | `Icons/ResourceTypes/` |
| Item Icons | `Icons/ItemsGenerated/`, `Icons/Items/` |
| Model Icons | `Icons/ModelsGenerated/`, `Icons/Models/` |
| Reticles | `UI/Reticles/` |
| Screen Effects | `ScreenEffects/` |
| Crafting | `CraftingDiagrams/` |

### High-Resolution Support

UI textures support `@2x` suffix for high-DPI:

```
UI/Button.png      -> Standard resolution
UI/Button@2x.png   -> 2x resolution
```

---

## Asset Validation

### Path Validators

```java
CommonAssetValidator(String extension, String... requiredRoots)

// Example: Validates model files
new CommonAssetValidator(".blockymodel", "Blocks/", "Items/", "NPC/")
```

### Sound Validators

| Validator | Description |
|-----------|-------------|
| `ONESHOT` | No layers may be looping |
| `LOOPING` | At least one layer must loop |
| `MONO` | All files must be mono |
| `STEREO` | Validates stereo audio |

### Numeric Validators

```java
Validators.range(min, max)
Validators.nonNull()
Validators.nonEmptyArray()
Validators.nonEmptyMap()
Validators.greaterThan(value)
```

---

## Asset Pack Structure

```
AssetPack/
├── manifest.json
├── Blocks/
│   └── *.blockymodel
├── BlockTextures/
│   └── *.png
├── Items/
│   ├── *.blockymodel
│   └── *.png
├── Characters/
│   ├── *.blockymodel
│   └── *.blockyanim
├── NPC/
│   └── ...
├── Sounds/
│   └── *.ogg
├── Particles/
│   └── *.png
├── Trails/
│   └── *.png
└── Icons/
    └── *.png
```

---

## Source Files

- `com/hypixel/hytale/server/core/asset/common/HytaleFileTypes.java`
- `com/hypixel/hytale/server/core/asset/common/CommonAssetValidator.java`
- `com/hypixel/hytale/server/core/asset/type/model/config/Model.java`
- `com/hypixel/hytale/server/core/asset/common/BlockyAnimationCache.java`
- `com/hypixel/hytale/server/core/asset/type/soundevent/config/SoundEvent.java`
- `com/hypixel/hytale/server/core/asset/type/particle/config/ParticleSystem.java`
- `com/hypixel/hytale/server/core/asset/type/trail/config/Trail.java`
- `com/hypixel/hytale/server/core/asset/type/blocktype/config/BlockTypeTextures.java`
- `com/hypixel/hytale/assetstore/AssetPack.java`
