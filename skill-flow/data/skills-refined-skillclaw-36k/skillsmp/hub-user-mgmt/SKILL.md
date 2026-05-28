---
name: hub-user-mgmt
description: Manage MCP Hub users (Götterboten). Use when creating new users, updating permissions, or checking user status.
---

# Hub User Management

Manage MCP Hub multi-user endpoints.

## Workflows

### 1. List Users

```bash
ls -la clients/*/config.json
```

Or read the config files to see user details.

### 2. Create New User

**Steps:**
1. Copy template: `cp -r clients/_template clients/{username}`
2. Edit `clients/{username}/config.json`
3. Generate JWT: `docker compose exec hub node scripts/generate-token.js {username}`
4. Add to user documentation
5. Restart hub if needed

**Quick Template:**

```json
{
  "name": "{username}",
  "endpoint": "/mcp/{username}-sse",
  "tools": {
    "mode": "whitelist",
    "allowed": [
      "ping",
      "list_tools",
      "invoke_notion_tool"
    ]
  }
}
```

### 3. Update Permissions

Edit `clients/{username}/config.json`:

```json
{
  "tools": {
    "mode": "whitelist",
    "allowed": ["tool_pattern_*"]
  }
}
```

**Or for blacklist mode:**

```json
{
  "tools": {
    "mode": "blacklist",
    "denied": ["admin_*"]
  }
}
```

**Or for full access:**

```json
{
  "tools": {
    "mode": "all"
  }
}
```

### 4. Generate JWT Token

```bash
# Using docker
docker compose exec hub node scripts/generate-token.js {username}

# Or locally
node services/hub/scripts/generate-token.js {username}
```

### 5. Disable User

Set `"enabled": false` in config and restart hub.

```json
{
  "name": "{username}",
  "enabled": false
}
```

## File Locations

| File | Purpose |
|------|---------|
| `clients/_template/` | Template for new users |
| `clients/{username}/` | User-specific configs |
| `clients/{username}/config.json` | User permissions |
| `services/hub/scripts/generate-token.js` | JWT generation |

## Götterboten Pool

Pre-configured mythological messenger names:

| Name | Description |
|------|-------------|
| hermes | Greek messenger (admin) |
| iris | Greek rainbow messenger |
| mercury | Roman messenger |
| thoth | Egyptian god of writing |
| gabriel | Abrahamic messenger |
| angelos | Greek for messenger |
| arke | Greek messenger of Titans |
| jibril | Arabic for Gabriel |

## Tool Permission Modes

| Mode | Behavior |
|------|----------|
| `all` | All tools accessible |
| `whitelist` | Only `allowed` tools accessible |
| `blacklist` | All except `denied` tools |

## Common Permission Sets

### Admin
```json
{
  "tools": { "mode": "all" }
}
```

### Developer
```json
{
  "tools": {
    "mode": "whitelist",
    "allowed": [
      "ping",
      "list_tools",
      "invoke_notion_tool",
      "list_notion_tools"
    ]
  }
}
```

### Read-Only
```json
{
  "tools": {
    "mode": "whitelist",
    "allowed": [
      "ping",
      "list_tools"
    ]
  }
}
```

## Deployment

After user changes, restart the hub:

```bash
docker compose restart hub
```
