# Hytale Texture Specifications Reference

Detailed specifications for textures in the Hytale asset system.

## Texture File Format

- **Format**: PNG (Portable Network Graphics)
- **Color Depth**: 8-bit RGBA
- **Compression**: Standard PNG compression
- **Alpha**: Full alpha channel support

---

## Block Textures

### Directory

```
BlockTextures/
├── Stone.png
├── Dirt.png
├── Grass_Top.png
├── Grass_Side.png
├── Unknown.png
└── _Debug/
    ├── Up.png
    ├── Down.png
    ├── North.png
    ├── South.png
    ├── East.png
    └── West.png
```

### Per-Face Assignment

Blocks can have different textures per face:

```json
{
  "Textures": {
    "up": "BlockTextures/Grass_Top.png",
    "down": "BlockTextures/Dirt.png",
    "north": "BlockTextures/Grass_Side.png",
    "south": "BlockTextures/Grass_Side.png",
    "east": "BlockTextures/Grass_Side.png",
    "west": "BlockTextures/Grass_Side.png"
  }
}
```

### Shorthand Properties

```json
// All faces same texture
{ "All": "BlockTextures/Stone.png" }

// Top/bottom different from sides
{
  "UpDown": "BlockTextures/Log_End.png",
  "Sides": "BlockTextures/Log_Side.png"
}
```

### Texture Variants

Multiple textures with weights for random selection:

```json
{
  "TextureVariants": [
    { "All": "BlockTextures/Stone_1.png", "weight": 3 },
    { "All": "BlockTextures/Stone_2.png", "weight": 2 },
    { "All": "BlockTextures/Stone_3.png", "weight": 1 }
  ]
}
```

---

## Model Textures

### Directory Structure

```
Items/
├── Weapons/
│   ├── Sword.blockymodel
│   └── Sword.png           # Auto-matched texture
Characters/
├── Player/
│   ├── Player.blockymodel
│   └── Player.png
NPC/
├── Goblin/
│   ├── Goblin.blockymodel
│   └── Goblin.png
```

### Texture Auto-Detection

If no texture specified, uses model path with `.png`:

```java
// Model: Items/Sword.blockymodel
// Auto texture: Items/Sword.png
texture = model.replace(".blockymodel", ".png");
```

### Explicit Texture Override

```json
{
  "Model": "Items/Sword.blockymodel",
  "Texture": "Items/Weapons/Custom_Sword_Texture.png"
}
```

---

## Gradient System

Textures can use gradient sets for color variations.

### Gradient Set

```json
{
  "GradientSet": "Metal_Iron",
  "GradientId": "rusty"
}
```

### How Gradients Work

1. Base texture uses grayscale values
2. Gradient maps grayscale to color ramp
3. Different gradient IDs = different color schemes

---

## Particle Textures

### Directory

```
Particles/
├── Fire.png
├── Smoke.png
├── Spark.png
└── Magic/
    └── Sparkle.png
```

### Sprite Sheet Format

Particle textures can be sprite sheets:

```json
{
  "texture": "Particles/Fire.png",
  "frameSize": { "width": 64, "height": 64 }
}
```

### Frame Layout

```
+--------+--------+--------+--------+
| Frame0 | Frame1 | Frame2 | Frame3 |
+--------+--------+--------+--------+
| Frame4 | Frame5 | Frame6 | Frame7 |
+--------+--------+--------+--------+
```

Frames read left-to-right, top-to-bottom.

---

## Trail Textures

### Directory

```
Trails/
├── Sword.png
├── Magic.png
└── Fire.png
```

### Trail Sprite Animation

```json
{
  "texture": "Trails/Magic.png",
  "animation": {
    "frameSize": [64, 64],
    "frameRange": { "min": 0, "max": 8 },
    "frameLifeSpan": 50
  }
}
```

---

## UI Textures

### Directories

```
UI/
├── Reticles/
│   ├── Crosshair.png
│   └── Crosshair@2x.png     # High-DPI version
├── ItemQualities/
│   ├── Common.png
│   ├── Uncommon.png
│   ├── Rare.png
│   └── Legendary.png
└── Buttons/
    └── ...
```

### High-DPI Support

UI textures support `@2x` suffix:

```
UI/Button.png       # 1x resolution (100x50)
UI/Button@2x.png    # 2x resolution (200x100)
```

---

## Icon Textures

### Auto-Generated Icons

Icons generated from 3D models:

```
Icons/ItemsGenerated/{AssetId}.png
Icons/ModelsGenerated/{AssetId}.png
```

### Manual Icons

Hand-crafted icons:

```
Icons/Items/{ItemId}.png
Icons/Models/{ModelId}.png
Icons/ResourceTypes/{ResourceId}.png
```

---

## Screen Effects

### Directory

```
ScreenEffects/
├── Vignette.png
├── Damage.png
└── Underwater.png
```

Used for fullscreen post-processing effects.

---

## Sky Textures

### Directory

```
Sky/
├── Skybox_Day.png
├── Skybox_Night.png
├── Clouds.png
└── Sun.png
```

---

## Crafting Diagrams

### Format

SVG files for vector crafting layouts:

```
CraftingDiagrams/
├── Workbench.svg
├── Furnace.svg
└── Anvil.svg
```

---

## Texture Validation

### Required Path Roots

Textures validated by category:

| Category | Valid Roots |
|----------|-------------|
| Item/Block | `Blocks/`, `BlockTextures/`, `Items/`, `NPC/`, `Resources/`, `VFX/` |
| Character | `Characters/`, `NPC/`, `Items/`, `VFX/` |
| Trail | `Trails/` |
| Particle | `Particles/` |
| Sky | `Sky/` |
| UI | `UI/` |
| Icons | `Icons/` |

### Validation Rules

1. Path must start with valid root
2. File extension must be `.png`
3. File must exist in asset registry
4. Dimensions should be power-of-2 for 3D textures

---

## Power-of-2 Sizes

Recommended texture dimensions:

| Size | Usage |
|------|-------|
| 16x16 | Block textures, small icons |
| 32x32 | Item icons |
| 64x64 | Particle frames, trails |
| 128x128 | Character textures |
| 256x256 | Large character textures |
| 512x512 | High-detail textures |
| 1024x1024 | Environment textures |
| 2048x2048 | Very high-detail |

Non-power-of-2 supported but may reduce performance.

---

## Texture Naming Conventions

### Block Textures

```
{Material}_{Variant}.png
{Material}_{Face}.png

Examples:
Stone.png
Stone_Mossy.png
Wood_Oak_Side.png
Grass_Top.png
```

### Item Textures

```
{ItemType}_{Material}_{Variant}.png

Examples:
Sword_Iron.png
Armor_Steel_Chest.png
Potion_Health.png
```

### NPC Textures

```
{NPCType}_{Variant}.png

Examples:
Goblin.png
Goblin_Armored.png
Skeleton_Warrior.png
```

---

## Color Spaces

- **sRGB**: Standard for all textures
- **Linear**: Used internally after loading
- **Normal Maps**: Tangent-space, blue-ish appearance

---

## Alpha Channel Usage

| Alpha Value | Meaning |
|-------------|---------|
| 255 | Fully opaque |
| 1-254 | Semi-transparent |
| 0 | Fully transparent |

### Block Texture Alpha

- **Opaque blocks**: Alpha = 255 everywhere
- **Transparent blocks**: Use alpha for see-through areas
- **Cutout blocks**: Use alpha 0 or 255 only (no gradients)

---

## Source Files

- `com/hypixel/hytale/server/core/asset/type/blocktype/config/BlockTypeTextures.java`
- `com/hypixel/hytale/server/core/asset/type/model/config/Model.java`
- `com/hypixel/hytale/server/core/asset/type/particle/config/Particle.java`
- `com/hypixel/hytale/server/core/asset/type/trail/config/Trail.java`
- `com/hypixel/hytale/server/core/asset/common/CommonAssetValidator.java`
