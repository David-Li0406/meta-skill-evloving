---
name: dojo-init
description: Use this skill when starting a new Dojo game project to initialize the project with the proper directory structure, configuration files, and dependencies.
---

# Dojo Project Initialization

Initialize new Dojo projects with the complete directory structure, configuration files, and dependencies.

## When to Use This Skill

- "Create a new Dojo project"
- "Initialize a Dojo game called [name]"
- "Set up a new Dojo application"
- "Start a new provable game project"

## What This Skill Does

Creates a complete Dojo project with:
- `Scarb.toml` with Dojo dependencies
- `dojo_dev.toml` for local development
- `dojo_release.toml` for deployment
- Source directory structure: `src/models/`, `src/systems/`, `src/tests/`
- `src/lib.cairo` with module exports
- Example models and systems
- `.gitignore` configured for Dojo projects

## Quick Start

**Using sozo init:**
```bash
sozo init my-game
```
This creates a new Dojo project from the [dojo-starter template](https://github.com/dojoengine/dojo-starter).

**Interactive mode:**
```
"Create a new Dojo project called my-game"
```

## Project Structure

```
my-game/
├── Scarb.toml              # Package manifest and dependencies
├── dojo_dev.toml           # Local development profile
├── dojo_release.toml       # Production deployment profile
└── src/
    ├── lib.cairo           # Module exports
    ├── models.cairo        # Game state models
    ├── systems/            # Game logic systems
    │   └── actions.cairo   # Example game logic
    └── tests/              # Test files
        └── test_world.cairo # Integration tests
```

## Configuration Files

### Scarb.toml

Package manifest with Dojo dependencies:
```toml
[package]
cairo-version = "2.12.2"
name = "my_game"
version = "1.0.0"
edition = "2024_07"

[[target.starknet-contract]]
sierra = true
build-external-contracts = ["dojo::world::world_contract::world"]

[dependencies]
starknet = "2.12.2"
dojo = "1.7.1"

[dev-dependencies]
cairo_test = "2.12.2"
dojo_cairo_test = "1.7.1"

[tool.scarb]
allow-prebuilt-plugins = ["dojo_cairo_macros"]
```

### dojo_dev.toml

Local development configuration:
```toml
[world]
name = "My Game"
seed = "my_game"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."

[namespace]
default = "my_game"

[writers]
"my_game" = ["my_game-actions"]
```

## Next Steps

After initialization:
1. Use `dojo-model` skill to add game state models.
2. Use `dojo-system` skill to implement game logic.
3. Use `dojo-test` skill to write tests.
4. Use `dojo-deploy` skill to deploy your world.

## Related Skills

- **dojo-model**: Add models to your project.
- **dojo-system**: Add systems to your project.
- **dojo-config**: Modify configuration later.
- **dojo-deploy**: Deploy your project.