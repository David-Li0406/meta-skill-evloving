---
name: dojo-configuration-management
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
- `dojo_<profile>.toml` - Environment-specific profiles (e.g., `dojo_dev.toml`, `dojo_mainnet.toml`)
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
```

### `dojo_<profile>.toml` - Profile Configuration

Profile-specific deployment settings. Dojo looks for `dojo_dev.toml` by default.

```toml
[world]
name = "My Game"
description = "An awesome on-chain game"
seed = "my-unique-seed"

[env]
rpc_url = "http://localhost:5050/"
account_address = "0x127fd..."
private_key = "0xc5b2f..."
```

## Profile System

Dojo uses profiles to manage different environments:

```bash
# Use default 'dev' profile (dojo_dev.toml)
sozo build
sozo migrate

# Use specific profile (dojo_mainnet.toml)
sozo build --profile mainnet
sozo migrate --profile mainnet
```

## World Configuration

```toml
[world]
name = "My Game"
description = "A provable game"
seed = "my-unique-seed"
```

## Namespace Configuration

Namespaces organize your resources:

```toml
[namespace]
default = "my_game"
```

## Dependencies

### Add Dojo Dependencies

```toml
[dependencies]
starknet = "2.12.2"
dojo = "1.7.1"
```

### Add External Libraries

**Origami (game utilities):**
```toml
[dependencies]
origami_token = { git = "https://github.com/dojoengine/origami", tag = "v1.0.0" }
```

## Security

### Protecting Secrets

**Never commit private keys.** Use `.gitignore`:

```
# Ignore sensitive configs
dojo_mainnet.toml
dojo_*_secrets.toml

# Keep development config
!dojo_dev.toml
```

## Troubleshooting

**"Profile not found":**
- Ensure `dojo_<profile>.toml` exists in project root

**"World not found":**
- Set `world_address` in `[env]` after first deployment

## Next Steps

After configuration:
1. Use `dojo-deploy` skill to deploy with your config
2. Use `dojo-migrate` skill when updating deployments
3. Use `dojo-world` skill to manage runtime permissions

## Related Skills

- **dojo-init**: Initialize new project with config
- **dojo-deploy**: Deploy using configuration
- **dojo-migrate**: Update deployed worlds
- **dojo-world**: Manage world permissions