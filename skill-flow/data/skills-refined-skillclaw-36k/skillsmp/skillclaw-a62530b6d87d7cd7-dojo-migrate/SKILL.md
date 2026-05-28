---
name: dojo-migrate
description: Use this skill when managing world migrations, handling breaking changes, or upgrading Dojo versions in deployed worlds.
---

# Dojo Migration Management

Handle world migrations, upgrades, and breaking changes when updating deployed Dojo worlds.

## When to Use This Skill

- "Migrate my world changes"
- "Upgrade to new Dojo version"
- "Handle breaking changes"
- "Update deployed models"

## What This Skill Does

Manages migration workflows:
- Analyze migration diffs
- Plan migration strategies
- Execute migrations
- Handle breaking changes
- Upgrade Dojo versions

## Quick Start

**Update existing world:**
```
"Migrate my changes to the deployed world"
```

**Version upgrade:**
```
"Upgrade my project to Dojo v1.8.0"
```

## Migration Workflow

### 1. Inspect Changes

**Check diff:**
```bash
sozo inspect
```

Shows:
- New models
- Modified models
- New systems/contracts
- Modified systems
- Status of all resources

### 2. Plan Migration

**Review changes:**
- Breaking: Model key changes, field removals
- Safe: New models, new systems, field additions
- Risky: Field type changes, system logic changes

**Strategy:**
- Safe changes: Direct migration
- Breaking changes: Data migration needed
- Major changes: Consider new world

### 3. Execute Migration

**Apply changes:**
```bash
sozo migrate --world WORLD_ADDRESS
```

**With specific profile:**
```bash
sozo migrate --profile sepolia
```

## Migration Types

### Additive Migrations (Safe)

**Adding new model:**
```cairo
// New model - safe to add
#[derive(Copy, Drop, Serde)]
#[dojo::model]
pub struct NewFeature {
    #[key]
    pub player: ContractAddress,
    pub data: u32,
}
```

**Adding new system:**
```cairo
// New system - safe to add
#[dojo::contract]
pub mod new_system {
    // Implementation
}
```

**Adding model field:**
```cairo
// Adding field - existing data will have default (zero) value
struct Position {
    #[key] player: ContractAddress,
    x: u32,
    y: u32,
    z: u32,  // New field
}
```

### Breaking Migrations (Dangerous)

**Changing key fields:**
```cairo
// Old
struct Position {
    #[key] player: ContractAddress,
    x: u32, y: u32,
}

// New - BREAKING! Different key structure
struct Position {
    #[key] entity_id: u32,  // Changed key
    x: u32, y: u32,
}
```

**Removing fields:**
```cairo
// Old
struct Stats {
    #[key] player: ContractAddress,
    health: u8,
    mana: u8,
}

// New - BREAKING! Data loss
struct Stats {
    #[key] player: ContractAddress,
    health: u8,
    // mana removed
}
```

**Changing field types:**
```cairo
// Old
struct Position {
    #[key] player: ContractAddress,
    x: u32,
    y: u32,
}

// New - BREAKING! Type change
struct Position {
    #[key] player: ContractAddress,
    x: f32,  // Changed type
    y: u32,
}
```