---
name: dojo-model
description: Use this skill when defining game entities, components, or state structures to create Dojo models with proper key definitions and trait derivations.
---

# Dojo Model Generation

Create Dojo models that define your game's state using Entity Component System (ECS) patterns.

## When to Use This Skill

- "Add a Position model"
- "Create a Player entity with health and level"
- "Generate an Inventory model"
- "Define a model for [game concept]"

## What This Skill Does

Generates Cairo model structs with:
- `#[dojo::model]` attribute
- Required trait derivations (`Drop`, `Serde`)
- Key field configuration (`#[key]`)
- Field types appropriate to your data
- Optional: Model tests

## Quick Start

**Interactive mode:**
```
"Add a model for player positions"
```
I'll ask about:
- Model name
- Key fields (what makes it unique)
- Data fields and their types
- Whether to generate tests

**Direct mode:**
```
"Create a Position model with player as key and x, y coordinates"
```

## Model Patterns

### Player-Owned Model
Models keyed by player address:
```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct Position {
    #[key]
    pub player: ContractAddress,
    pub vec: Vec2,
}

#[derive(Copy, Drop, Serde, Introspect)]
pub struct Vec2 {
    pub x: u32,
    pub y: u32,
}
```

### Composite Keys
Multiple keys for relationships:
```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct GameResource {
    #[key]
    pub player: ContractAddress,
    #[key]
    pub location: ContractAddress,
    pub balance: u8,
}
```

### Global Singleton
Constant key for global settings:
```cairo
const RESPAWN_DELAY: u128 = 9999999999999;

#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct GameSetting {
    #[key]
    pub setting_id: u128,
    pub setting_value: felt252,
}
```

## Key Concepts

**#[key] Attribute:**
- Defines how models are indexed
- At least one key required
- Keys must come before data fields
- Keys not stored, used for lookup only

**Required Traits:**
- `Drop` - Cairo ownership
- `Serde` - Serialization

**Optional Traits:**
- `Copy` - For copyable types (optional)

**Field Types:**
- `u8`, `u32`, `u128` - Unsigned integers
- `felt252` - Field elements
- `bool` - Booleans
- `ContractAddress` - Addresses
- Custom enums (with Introspect)

## Model API

### Write a Model
```cairo
world.write_model(@Position { player, vec });
```