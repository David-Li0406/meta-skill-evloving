---
name: phaser-gamedev
description: Use this skill when you want to build 2D games with the Phaser 3 framework, covering essential aspects like scene lifecycle, sprites, physics, and game architecture.
---

# Skill body

## Overview

Build 2D browser games using the Phaser 3 framework, which utilizes a scene-based architecture and various physics systems.

## Key Concepts

- **Scene Lifecycle**: Understand how to manage different game states and transitions.
- **Sprites**: Learn to create and manipulate sprites for characters and objects.
- **Physics**: Choose between Arcade and Matter physics systems based on game requirements.
- **Tilemaps**: Implement tile-based maps for level design.
- **Animations**: Create smooth animations for sprites.
- **Input Handling**: Manage user input for interactive gameplay.
- **Game Architecture**: Structure your game for maintainability and scalability.

## Quick Start

1. **Set Up Your Project**: Initialize a new Phaser project.
2. **Create Your First Scene**: Define a basic scene with a preload, create, and update function.
3. **Load Assets**: Use the asset loading system to manage images and spritesheets.
4. **Implement Physics**: Choose a physics system and set up collision detection.
5. **Add Input Handling**: Capture keyboard and mouse events for player interaction.

## Important Considerations

### STOP: Before Loading Any Spritesheet

**Read the spritesheet loading guidelines carefully.** Spritesheet loading is fragile; incorrect dimensions can lead to visual issues. Follow these quick rules:

1. **Measure the asset** before writing loader code—never guess frame dimensions.
2. **Character sprites use SQUARE frames**: If you calculate frameWidth=56, try 56 for height first.
3. **Different animations have different frame sizes**: Measure each spritesheet independently.
4. **Check for spacing**: Gaps between frames require `spacing: N` in loader config.
5. **Verify the math**: Ensure `imageWidth = (frameWidth × cols) + (spacing × (cols - 1))`.

### Architecture Decisions (Make Early)

#### Physics System Choice

| System | Use When |
|--------|----------|
| **Arcade** | Platformers, shooters, most 2D games. Fast AABB collisions. |
| **Matter** | Physics puzzles, ragdolls, realistic collisions. Slower, more accurate. |
| **None** | Menu scenes, visual novels, card games. |

#### Scene Structure

```
scenes/
├── BootScene.ts      # Asset loading, progress bar
├── MenuScene.ts      # Title screen, options
├── GameScene.ts      # Main gameplay
├── UIScene.ts        # HUD overlay (launched parallel)
└── GameOverScene.ts  # End screen
```