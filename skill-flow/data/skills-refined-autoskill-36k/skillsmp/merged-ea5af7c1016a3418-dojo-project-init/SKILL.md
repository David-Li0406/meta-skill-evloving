---
name: dojo-project-init
description: Use this skill to initialize new Dojo projects with the proper directory structure, configuration files, and dependencies when starting a new Dojo game project.
---

# Dojo Project Initialization

Initialize new Dojo projects with a complete directory structure, configuration files, and dependencies.

## When to Use This Skill

- "Create a new Dojo project"
- "Initialize a Dojo game called [name]"
- "Set up a new Dojo application"
- "Start a new provable game project"

## What This Skill Does

Creates a complete Dojo project with:
- `Scarb.toml` for package configuration and dependencies
- `dojo_dev.toml` for local development settings
- `dojo_release.toml` for production deployment settings
- Source directory structure: `src/models/`, `src/systems/`, `src/tests/`
- Example models and systems
- Test files
- `.gitignore` configured for Dojo projects

## Quick Start

**Using sozo init:**
```bash
sozo init <project_name>
```
This creates a new Dojo project from the starter template.

**Interactive mode:**
```
"Create a new Dojo project called <project_name>"
```

## Project Structure

After initialization:

```
<project_name>/
├── Scarb.toml              # Package manifest and dependencies
├── dojo_dev.toml           # Local development profile
├── dojo_release.toml       # Production deployment profile
└── src/
    ├── lib.cairo           # Module exports
    ├── models.cairo        # Game state models
    ├── systems/
    │   └── actions.cairo   # Game logic systems
    └── tests/
        └── test_world.cairo # Integration tests
```

## Configuration Files

### Scarb.toml

Package manifest with Dojo dependencies:
```toml
[package]
cairo-version = "2.12.2"
name = "<project_name>"
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
name = "<project_name>"
seed = "<project_name>"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."

[namespace]
default = "<project_name>"

[writers]
"<project_name>" = ["<project_name>-actions"]
```

### dojo_release.toml

Production deployment configuration:
- Testnet/Mainnet RPC URLs
- Account configuration
- Deployment settings

## Development Workflow

1. **Initialize project:**
   ```bash
   sozo init <project_name>
   cd <project_name>
   ```

2. **Start Katana:**
   ```bash
   katana --dev --dev.no-fee
   ```

3. **Build and deploy:**
   ```bash
   sozo build && sozo migrate
   ```

4. **Test your system:**
   ```bash
   sozo execute <project_name>-actions spawn
   ```

5. **Run tests:**
   ```bash
   sozo test
   ```

## Customization

After initialization, customize your project:
1. **Add models:** Create new model structs in `src/models.cairo` or separate files.
2. **Add systems:** Create new contract modules in `src/systems/`.
3. **Update permissions:** Edit `[writers]` in `dojo_dev.toml`.
4. **Add dependencies:** Edit `[dependencies]` in `Scarb.toml`.

## Next Steps

After initialization:
1. Use `dojo-model` skill to add game state models.
2. Use `dojo-system` skill to implement game logic.
3. Use `dojo-test` skill to write tests.
4. Use `dojo-deploy` skill to deploy your world.

## Related Skills

- **dojo-model**: Add models to your project.
- **dojo-system**: Add systems to your project.
- **dojo-config**: Modify configuration.
- **dojo-deploy**: Deploy your project.