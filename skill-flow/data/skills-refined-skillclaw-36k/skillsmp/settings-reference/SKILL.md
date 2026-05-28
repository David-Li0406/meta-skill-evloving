---
name: settings-reference
description: Claude Code settings configuration reference. Use when configuring Claude Code behavior, understanding settings hierarchy, or customizing project/user settings.
---

# Claude Code Settings Reference

Configure Claude Code behavior through settings files at different scopes.

## Settings Hierarchy (Priority Order)

| Priority | Location | Purpose |
|----------|----------|---------|
| 1 (highest) | Enterprise managed | Organization policies |
| 2 | `.claude/settings.local.json` | Project personal (gitignored) |
| 3 | `.claude/settings.json` | Project team (shared) |
| 4 | `~/.claude/settings.json` | User global |

Higher priority settings override lower.

## Settings File Locations

```
/Library/Application Support/ClaudeCode/settings.json  # Enterprise (macOS)
~/.claude/settings.json                                 # User global
.claude/settings.json                                   # Project team
.claude/settings.local.json                             # Project personal
```

## Common Settings

### Tool Permissions
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build)",
      "Bash(npm test)",
      "Read",
      "Write"
    ],
    "deny": [
      "Bash(rm -rf /)"
    ]
  }
}
```

### Model Selection
```json
{
  "model": "claude-sonnet-4-20250514",
  "preferredModels": {
    "default": "claude-sonnet-4-20250514",
    "agents": "claude-haiku-3-5-20240307"
  }
}
```

### MCP Servers
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Hooks
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "echo 'Bash tool used'"
      }]
    }]
  }
}
```

## Permission Patterns

### Exact Match
```json
"allow": ["Bash(npm test)"]
```

### Wildcard
```json
"allow": ["Bash(npm *)"]
```

### Tool Only
```json
"allow": ["Read", "Write"]
```

### Regex (in matcher)
```json
"allow": ["Bash(npm (test|build))"]
```

## Settings Merging

Settings merge across files:
- Arrays: concatenated
- Objects: deep merged
- Primitives: higher priority wins

## Environment Variables

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "true"
  }
}
```

These are set when Claude runs Bash commands.

## Plugin Settings

### Enable Plugins
```json
{
  "enabledPlugins": {
    "formatter@marketplace": true,
    "linter@marketplace": true
  }
}
```

### Add Marketplace
```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "org/claude-plugins"
      }
    }
  }
}
```

### Restrict Marketplaces
```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "approved/plugins"
    }
  ]
}
```

## Trust Settings

```json
{
  "trust": {
    "autoTrustDirectories": [
      "~/projects"
    ]
  }
}
```

## Editor Integration

```json
{
  "editor": {
    "command": "code",
    "args": ["--wait", "$FILE"]
  }
}
```

## Debugging Settings

View effective settings:
```bash
/settings
```

Check specific scope:
```bash
/settings user
/settings project
```

## Settings Commands

| Command | Description |
|---------|-------------|
| `/settings` | View/edit settings |
| `/config` | Configuration wizard |
| `/permissions` | Tool permission management |

## Common Configuration Patterns

### Development Project
```json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(git *)",
      "Read",
      "Write",
      "Edit"
    ]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write"
      }]
    }]
  }
}
```

### Restricted Production
```json
{
  "permissions": {
    "deny": [
      "Bash(rm *)",
      "Bash(git push *)"
    ]
  }
}
```

---

For complete documentation, see:
- [settings-full.md](settings-full.md) - Complete settings reference
