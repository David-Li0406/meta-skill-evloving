---
name: mcp-reference
description: Claude Code MCP (Model Context Protocol) server configuration reference. Use when adding MCP servers, configuring external tools, or integrating third-party services.
---

# Claude Code MCP Reference

MCP (Model Context Protocol) connects Claude to external tools and services.

## Configuration Locations

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | User (all projects) |
| `.claude/settings.json` | Project (team shared) |
| `.claude/settings.local.json` | Project (gitignored) |

## Basic Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | Executable to run |
| `args` | No | Command arguments |
| `env` | No | Environment variables |
| `cwd` | No | Working directory |
| `alwaysAllow` | No | Array of always-allowed tools |
| `disabled` | No | Boolean to disable server |

## Common MCP Servers

### Filesystem Server
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### GitHub Server
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    }
  }
}
```

### Database Server
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

## Plugin MCP Servers

In plugin's `.mcp.json` or `plugin.json`:

```json
{
  "mcpServers": {
    "plugin-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

Note: Use `${CLAUDE_PLUGIN_ROOT}` for plugin paths.

## Tool Permissions

### Always Allow Specific Tools
```json
{
  "mcpServers": {
    "github": {
      "command": "...",
      "alwaysAllow": [
        "create_issue",
        "list_repos"
      ]
    }
  }
}
```

### Interactive Permissions
If `alwaysAllow` not specified, Claude asks before using tools.

## Disabling Servers

```json
{
  "mcpServers": {
    "expensive-server": {
      "command": "...",
      "disabled": true
    }
  }
}
```

## Environment Variables

### From System Environment
```json
{
  "env": {
    "API_KEY": "${API_KEY}"
  }
}
```

### Direct Values
```json
{
  "env": {
    "DEBUG": "true"
  }
}
```

## Server Management

### List MCP Servers
```bash
/mcp
```

### Refresh Servers
```bash
/mcp refresh
```

### Check Server Status
Look in `/mcp` for connection status.

## Debugging MCP Servers

```bash
# Debug mode shows server initialization
claude --debug

# Test server manually
npx -y @modelcontextprotocol/server-name

# Check server logs
# Look for MCP-related output in debug
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Server not starting | Check command exists and is executable |
| Tools not appearing | Verify server implements MCP correctly |
| Permission denied | Check file/directory permissions |
| Environment vars missing | Verify env values are set |

## Example: Custom Python Server

```json
{
  "mcpServers": {
    "my-python-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "cwd": "/path/to/server",
      "env": {
        "PYTHONPATH": "/path/to/server"
      }
    }
  }
}
```

## Security Considerations

- Store secrets in environment variables, not in settings
- Use `.claude/settings.local.json` for sensitive configs
- Review server code before adding third-party servers
- Limit `alwaysAllow` to necessary tools only

---

For complete documentation, see:
- [mcp-full.md](mcp-full.md) - Complete MCP reference
