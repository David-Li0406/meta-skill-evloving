---
name: dojo-world
description: Use this skill when managing world permissions, namespaces, resource registration, and access control in your Dojo environment.
---

# Dojo World Management

Manage your Dojo world's permissions, namespaces, resource registration, and access control policies.

## When to Use This Skill

- "Configure world permissions"
- "Set up namespace access"
- "Grant writer permissions"
- "Manage resource ownership"

## What This Skill Does

Handles world management:
- Namespace configuration
- Resource registration
- Writer permissions (can write data)
- Owner permissions (can write data + manage permissions)
- Permission hierarchy management

## Quick Start

**Configure permissions:**
```
"Grant writer permission to my system"
```

**Check permissions:**
```
"List permissions for my world"
```

## Permission Concepts

### Permission Types

**Owner Permission:**
- Write data to the resource
- Grant and revoke permissions to others
- Upgrade the resource
- Set resource metadata

**Writer Permission:**
- Write data to the resource
- Cannot grant permissions to others
- Cannot upgrade the resource

**Reading is always permissionless.**

### Permission Hierarchy

```
World Owner (highest)
    └── Namespace Owner
        └── Resource Owner / Writer (lowest)
```

- **World Owner**: Can do anything in the world
- **Namespace Owner**: Can manage all resources in their namespace
- **Resource Owner**: Can manage a specific resource (model/contract/event)
- **Writer**: Can only write data to a resource

## CLI Permission Management

### Granting Permissions

```bash
# Grant writer permission
sozo auth grant writer MODEL_NAME,SYSTEM_ADDRESS --world WORLD_ADDRESS

# Grant owner permission
sozo auth grant owner RESOURCE_NAME,NEW_OWNER_ADDRESS --world WORLD_ADDRESS
```

### Revoking Permissions

```bash
# Revoke writer permission
sozo auth revoke writer MODEL_NAME,SYSTEM_ADDRESS --world WORLD_ADDRESS

# Revoke owner permission
sozo auth revoke owner RESOURCE_NAME,NEW_OWNER_ADDRESS --world WORLD_ADDRESS
```

### Listing Permissions

```bash
# List all permissions for the world
sozo auth list permissions --world WORLD_ADDRESS
```

## Namespace Management

### Creating Namespace

```bash
sozo auth create-namespace my_namespace --world WORLD_ADDRESS
```

### Registering Resources

```bash
# Register model to namespace
sozo auth register model Position --namespace my_namespace --world WORLD_ADDRESS

# Register system to namespace
sozo auth register contract actions --namespace my_namespace --world WORLD_ADDRESS
```