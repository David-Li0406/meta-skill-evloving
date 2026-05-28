---
name: plugins-reference
description: Claude Code plugins configuration reference. Use when creating plugins, bundling commands/agents/hooks/skills/MCP servers, setting up marketplaces, or distributing extensions.
---

# Claude Code Plugins Reference

Plugins bundle commands, agents, skills, hooks, and MCP servers into distributable packages.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Slash commands
│   └── deploy.md
├── agents/                   # Subagent definitions
│   └── reviewer.md
├── skills/                   # Agent skills
│   └── api-patterns/
│       └── SKILL.md
├── hooks/
│   └── hooks.json           # Hook configurations
├── .mcp.json                # MCP server configs
└── .lsp.json                # LSP server configs
```

## plugin.json Manifest

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

## Required vs Optional Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `version` | No | Semantic version |
| `description` | No | Brief description |
| `author` | No | Author info |
| `commands` | No | Custom command paths |
| `agents` | No | Custom agent paths |
| `skills` | No | Custom skill paths |
| `hooks` | No | Hook config path/object |
| `mcpServers` | No | MCP config path/object |
| `lspServers` | No | LSP config path/object |

## Installation Scopes

| Scope | Location | Use Case |
|-------|----------|----------|
| `user` | `~/.claude/settings.json` | Personal (default) |
| `project` | `.claude/settings.json` | Team shared |
| `local` | `.claude/settings.local.json` | Project, gitignored |

## Plugin Commands

**Install plugin**:
```bash
/plugin install plugin-name@marketplace
claude plugin install plugin-name@marketplace --scope project
```

**Uninstall plugin**:
```bash
/plugin uninstall plugin-name
```

**Enable/Disable**:
```bash
/plugin enable plugin-name
/plugin disable plugin-name
```

**Update plugin**:
```bash
/plugin update plugin-name
```

**Validate plugin**:
```bash
/plugin validate ./path/to/plugin
claude plugin validate ./path/to/plugin
```

## Marketplace Setup

### marketplace.json

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Team Name"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description"
    }
  ]
}
```

### Marketplace Commands

```bash
# Add marketplace
/plugin marketplace add owner/repo
/plugin marketplace add https://gitlab.com/org/plugins.git

# Update marketplaces
/plugin marketplace update

# List marketplaces
/plugin marketplace list
```

## Plugin Sources

### Relative Path
```json
{ "source": "./plugins/my-plugin" }
```

### GitHub
```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo"
  }
}
```

### Git URL
```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/org/plugin.git"
  }
}
```

## Environment Variable

Use `${CLAUDE_PLUGIN_ROOT}` in hooks and MCP configs:

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
      }]
    }]
  }
}
```

## Project-Required Plugins

Add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "formatter@company-tools": true
  }
}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Plugin not loading | Check `plugin.json` syntax |
| Commands missing | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing | Check script permissions (`chmod +x`) |
| MCP fails | Use `${CLAUDE_PLUGIN_ROOT}` for paths |

## Debugging

```bash
# Debug mode shows plugin loading
claude --debug

# Check for errors
/plugin  # Navigate to Errors tab
```

---

For complete documentation, see:
- [plugins-full.md](plugins-full.md) - Plugin creation guide
- [plugins-tech-reference.md](plugins-tech-reference.md) - Complete technical reference
- [marketplace.md](marketplace.md) - Marketplace distribution
