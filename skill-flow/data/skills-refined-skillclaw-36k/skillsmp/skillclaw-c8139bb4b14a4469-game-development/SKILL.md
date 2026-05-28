---
name: game-development
description: Use this skill when you are working on a game development project and need guidance on core principles and routing to specialized sub-skills based on your project's context.
---

# Game Development

> **Orchestrator skill** that provides core principles and routes to specialized sub-skills.

## When to Use This Skill

You are working on a game development project. This skill teaches the PRINCIPLES of game development and directs you to the right sub-skill based on context.

## Sub-Skill Routing

### Platform Selection

| If the game targets...      | Use Sub-Skill                   |
| --------------------------- | ------------------------------- |
| Web browsers (HTML5, WebGL) | `game-development/web-games`    |
| Mobile (iOS, Android)       | `game-development/mobile-games` |
| PC (Steam, Desktop)         | `game-development/pc-games`     |
| VR/AR headsets              | `game-development/vr-ar`        |

### Dimension Selection

| If the game is...      | Use Sub-Skill               |
| ---------------------- | --------------------------- |
| 2D (sprites, tilemaps) | `game-development/2d-games` |
| 3D (meshes, shaders)   | `game-development/3d-games` |

### Specialty Areas

| If you need...                          | Use Sub-Skill                  |
| --------------------------------------- | ------------------------------ |
| GDD, balancing, player psychology       | `game-development/game-design` |
| Multiplayer, networking                 | `game-development/multiplayer` |
| Visual style, asset pipeline, animation | `game-development/game-art`    |
| Sound design, music, adaptive audio     | `game-development/game-audio`  |

## Core Principles (All Platforms)

### 1. The Game Loop

Every game, regardless of platform, follows this pattern:

```
INPUT  → Read player actions
UPDATE → Process game logic (fixed timestep)
RENDER → Draw the frame (interpolated)
```

**Fixed Timestep Rule:**

- Physics/logic: Fixed rate (e.g., 50Hz)
- Rendering: As fast as possible
- Interpolate between states for smooth visuals

### 2. Pattern Selection Matrix

| Pattern             | Use When                      | Example                |
| ------------------- | ----------------------------- | ---------------------- |
| **State Machine**   | 3-5 discrete states           | Player: Idle→Walk→Jump |
| **Object Pooling**  | Frequent spawn/destroy        | Bullets, particles     |
| **Observer/Events** | Cross-system communication    | Health→UI updates      |
| **ECS**             | Thousands of similar entities  | RTS units, particles   |
| **Command**         | Undo, replay, networking      | Input recording        |
| **Behavior Tree**   | Complex AI decisions          | Enemy AI              |

**Decision Rule:** Start with State Machine. Add ECS only when performance demands.

### 3. Input Abstraction

Abstract input into ACTIONS, not raw keys:

```
"jump" → ACTION
```