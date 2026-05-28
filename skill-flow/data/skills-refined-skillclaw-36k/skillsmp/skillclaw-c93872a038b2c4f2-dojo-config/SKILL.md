---
name: dojo-config
description: Use this skill when setting up project configuration, managing dependencies, or configuring deployment environments for Dojo projects.
---

# Dojo Configuration Management

Manage Dojo project configuration including Scarb.toml, deployment profiles, and world settings.

## When to Use This Skill

- "Configure Dojo for my project"
- "Update Scarb.toml dependencies"
- "Set up deployment profiles"
- "Configure world settings"

## What This Skill Does

Manages configuration files:
- `Scarb.toml` - Package manifest and dependencies
- `dojo_dev.toml` - Local development profile
- `dojo_<profile>.toml` - Other environment profiles
- World configuration, namespaces, and permissions

## Quick Start

**Interactive mode:**
```
"Update my Dojo configuration"
```

I'll ask about:
- What to configure (dependencies, profiles, world)
- Environment (dev, testnet, mainnet)
- Specific settings

**Direct mode:**
```
"Add the Origami library to my dependencies"
"Configure production deployment for Sepolia"
```

## Configuration Files

### `Scarb.toml` - Project Manifest

Defines project dependencies and build settings:

```toml
[package]
name = "my_game"
version = "0.1.0"
edition = "2024_07"

[dependencies]
dojo = { git = "https://github.com/dojoengine/dojo", tag = "v1.0.0" }

[[target.dojo]]

[tool.dojo]
initializer_class_hash = "0x..."

[tool.dojo.env]
rpc_url = "http://localhost:5050/"
account_address = "0x..."
private_key = "0x..."
world_address = "0x..."
```

### `dojo_dev.toml` - Local Development Configuration

```toml
[env]
rpc_url = "http://localhost:5050/"
account_address = "0xb3ff441a68610b30fd5e2abbf3a1548eb6ba6f3559f2862bf2dc757e5828ca"
private_key = "0x2bbf4f9fd0bbb2e60b0316c1fe0b76cf7a4d0198bd493ced9b8df2a3a24d68a"
world_address = ""

[world]
name = "my_game"
seed = "my_game"
```

### `dojo_<profile>.toml` - Profile Configuration

Profile-specific deployment settings. Dojo looks for `dojo_dev.toml` by default.

```toml
[world]
name = "My Game"
description = "An awesome on-chain game"
seed = "my-unique-seed"
cover_uri = "file://assets/cover.png"
icon_uri = "file://assets/icon.png"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."
```

## Common Configuration Tasks

### Add Dependencies

To add a new dependency, update the `[dependencies]` section in `Scarb.toml`:

```toml
[dependencies]
origami_token = "latest_version"
```