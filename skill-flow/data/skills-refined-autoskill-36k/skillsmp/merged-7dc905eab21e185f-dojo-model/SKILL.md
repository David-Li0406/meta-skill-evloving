---
name: dojo-model
description: Use this skill to create Dojo models for storing game state with proper key definitions, trait derivations, and ECS patterns when defining game entities, components, or state structures.
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
struct Position {
    #[key]
    player: ContractAddress,
    vec: Vec2,
}

#[derive(Copy, Drop, Serde, Introspect)]
struct Vec2 {
    x: u32,
    y: u32,
}
```

### Composite Keys
Multiple keys for relationships:
```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
struct GameResource {
    #[key]
    player: ContractAddress,
    #[key]
    location: ContractAddress,
    balance: u8,
}
```

### Global Singleton
Constant key for global settings:
```cairo
const RESPAWN_DELAY: u128 = 9999999999999;

#[derive(Copy, Drop, Serde)]
#[dojo::model]
struct GameSetting {
    #[key]
    setting_id: u128,
    setting_value: felt252,
}
```

### ECS Composition
Small, focused models that can be combined on entities:
```cairo
#[derive(Copy, Drop, Serde)]
#[dojo::model]
struct Health {
    #[key]
    id: u32,
    health: u8,
}
```

## Key Rules

1. **At least one key required** - Every model needs a `#[key]` field.
2. **Keys must come first** - All key fields before data fields.
3. **Keys are not stored** - Used only for indexing/lookup.
4. **All keys required for read** - Composite keys must all be provided.

## Model API

### Write a Model
```cairo
world.write_model(@Position { player, vec: Vec2 { x: 0, y: 0 } });
```

### Read a Model
```cairo
let position: Position = world.read_model(player);
```

### Read with Composite Key
```cairo
let resource: GameResource = world.read_model((player, location));
```

### Generate Unique ID
```cairo
let entity_id = world.uuid();
world.write_model(@Health { id: entity_id, health: 100 });
```

## Field Types

- `u8`, `u16`, `u32`, `u64`, `u128`, `u256` - Unsigned integers
- `felt252` - Field elements
- `bool` - Booleans
- `ContractAddress` - Starknet addresses
- Custom structs - Must derive `Introspect`
- Custom enums - Must derive `Introspect`

## Best Practices

- Keep models small and focused (one concern per model).
- Use appropriate key patterns (single, composite, constant).
- Choose smallest sufficient type (u8 vs u32 vs u128).
- Name fields clearly.
- Add doc comments for complex models.

## Next Steps

After creating models:
1. Use `dojo-system` skill to create systems that use your models.
2. Use `dojo-test` skill to test model read/write operations.
3. Use `dojo-config` skill to configure permissions.

## Related Skills

- **dojo-system**: Create systems that use these models.
- **dojo-test**: Test your models.
- **dojo-init**: Initialize project first.
- **dojo-review**: Review model design.