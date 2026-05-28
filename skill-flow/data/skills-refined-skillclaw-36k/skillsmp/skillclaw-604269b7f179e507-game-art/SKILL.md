---
name: game-art
description: Use this skill when you need to understand game art principles, including visual style selection, asset pipeline management, and animation workflows.
---

# Game Art Principles

> Visual design thinking for games - style selection, asset pipelines, and art direction.

## 1. Art Style Selection

### Decision Tree

```
What feeling should the game evoke?
│
├── Nostalgic / Retro
│   ├── Limited palette? → Pixel Art
│   └── Hand-drawn feel? → Vector / Flash style
│
├── Realistic / Immersive
│   ├── High budget? → PBR 3D
│   └── Stylized realism? → Hand-painted textures
│
├── Approachable / Casual
│   ├── Clean shapes? → Flat / Minimalist
│   └── Soft feel? → Gradient / Soft shadows
│
└── Unique / Experimental
    └── Define custom style guide
```

### Style Comparison Matrix

| Style            | Production Speed | Skill Floor | Scalability  | Best For          |
| ---------------- | ---------------- | ----------- | ------------ | ----------------- |
| **Pixel Art**    | Medium           | Medium      | Hard to hire | Indie, retro      |
| **Vector/Flat**  | Fast             | Low         | Easy         | Mobile, casual    |
| **Hand-painted** | Slow             | High        | Medium       | Fantasy, stylized |
| **PBR 3D**       | Slow             | High        | AAA pipeline | Realistic games   |
| **Low-poly**     | Fast             | Medium      | Easy         | Indie 3D          |
| **Cel-shaded**   | Medium           | Medium      | Medium       | Anime, cartoon    |

## 2. Asset Pipeline Decisions

### 2D Pipeline

| Phase           | Tool Options                       | Output             |
| --------------- | ---------------------------------- | ------------------ |
| **Concept**     | Paper, Procreate, Photoshop        | Reference sheet    |
| **Creation**    | Aseprite, Photoshop, Krita         | Individual sprites |
| **Atlas**       | TexturePacker, Aseprite            | Spritesheet        |
| **Animation**   | Spine, DragonBones, Frame-by-frame | Animation data     |
| **Integration** | Engine import                      | Game-ready assets  |

### 3D Pipeline

| Phase            | Tool Options               | Output          |
| ---------------- | -------------------------- | --------------- |
| **Concept**      | 2D art, Blockout           | Reference       |
| **Modeling**     | Blender, Maya, 3ds Max     | High-poly mesh  |
| **Retopology**   | Blender, ZBrush            | Game-ready mesh |
| **UV/Texturing** | Substance Painter, Blender  | Texture maps    |
| **Rigging**      | Blender, Maya              | Skeletal rig    |
| **Animation**    | Blender, Maya, Mixamo      | Animation clips  |
| **Export**       | FBX, glTF                  | Engine-ready    |

## 3. Color Theory Decisions

### Palette Selection

| Goal      | Strategy                       | Example          |
|-----------|--------------------------------|------------------|
| **Harmony** | Complementary or analogous    | Nature games     |
| **Contrast** | High saturation differences    | Action games     |
| **Mood**    | Warm/cool temperature         | Horror, cozy     |
| **Readability** | Value contrast for clarity | UI elements      |