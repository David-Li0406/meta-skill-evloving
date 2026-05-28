---
name: generate-game-asset
description: Use when you need to generate game art - sprites, textures, 3D model concepts. Uses FREE HuggingFace AI models.
---

# Game Asset Generation

## Overview

This skill triggers the **game-asset-generator** MCP server for AI-powered art generation using HuggingFace models.

## When to Use

- "Create a sprite for [monster name]"
- "Generate a UI icon for [element]"
- "Make a texture for [surface]"
- "Design concept art for [character]"

## VeilBreakers Art Style

**ALWAYS include this in prompts:**

```
dark fantasy horror, [subject], dark atmospheric,
glowing [color] eyes/core, dramatic lighting, deep shadows,
high detail, painterly quality, ominous mood
```

## Brand Color Reference

| Brand | Glow Color | Theme |
|-------|------------|-------|
| IRON | Steel blue | Armored, angular |
| SAVAGE | Blood red | Feral, claws |
| SURGE | Electric blue | Crackling, fast |
| VENOM | Toxic green | Dripping, sickly |
| DREAD | Purple/void | Shadowy, terror |
| LEECH | Dark red | Parasitic, tendrils |
| GRACE | White/gold | Ethereal, light |
| MEND | Soft green | Protective, shields |
| RUIN | Orange/red | Explosive, cracked |
| VOID | Deep purple | Chaotic, reality-bending |

## DO NOT Use

- "Battle Chasers" or "Joe Madureira"
- "thick linework" or "comic book"
- anime/cel-shaded style
- checker pattern backgrounds

## Output Specs

| Parameter | Value |
|-----------|-------|
| Resolution | 1024-2048px |
| Format | PNG with transparency |
| Save to | Assets/Art/[category]/ |

## MCP Server

**Server**: game-asset-generator
**Package**: game-asset-mcp
**Requires**: HF_TOKEN environment variable set

## Workflow

1. Define what asset is needed
2. Craft prompt using VeilBreakers style template
3. Generate via MCP
4. Review output quality
5. Save to correct Assets/ folder
6. Verify import settings in Unity
