# Plugin-Provided MCP Servers

Bundling MCP servers with Claude Code plugins for automatic distribution and setup.

**Note**: For comprehensive plugin bundling, distribution, and manifest configuration, use the **managing-plugins skill**. This file focuses specifically on MCP-related aspects of plugin architecture.

## Overview

Plugins can include MCP servers that:
- Start automatically when plugin is enabled
- Provide tools and resources alongside other plugin components
- Require no manual user configuration
- Update when plugin updates

## Configuration

**For plugin.json structure and bundling**: See managing-plugins skill

Two options for defining plugin MCP servers:

### Option 1: .mcp.json at Plugin Root

```json
{
  "mcpServers": {
    "plugin-api": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"],
      "env": {
        "API_KEY": "${API_KEY}",
        "DATA_DIR": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### Option 2: Inline in plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "mcpServers": {
    "plugin-api": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server"
    }
  }
}
```

## Path Variable: ${CLAUDE_PLUGIN_ROOT}

Reference plugin files using `${CLAUDE_PLUGIN_ROOT}` variable:

- **Expands to:** Absolute path to plugin directory
- **Works in:** command, args, env values, anywhere paths needed
- **Example:** `${CLAUDE_PLUGIN_ROOT}/servers/api-server`
- **Benefits:** Portable across machines, works regardless of plugin install location

**Example:**

```json
{
  "mcpServers": {
    "server": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/server.py",
      "args": [
        "--config",
        "${CLAUDE_PLUGIN_ROOT}/config/settings.json",
        "--cache",
        "${CLAUDE_PLUGIN_ROOT}/cache"
      ],
      "env": {
        "PLUGIN_HOME": "${CLAUDE_PLUGIN_ROOT}",
        "SERVER_PORT": "8080"
      }
    }
  }
}
```

## Environment Variables

Plugin MCP servers can access:
- Custom environment variables set in `env` field
- System environment variables available to Claude Code
- `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths

```json
{
  "mcpServers": {
    "api": {
      "type": "stdio",
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "PLUGIN_HOME": "${CLAUDE_PLUGIN_ROOT}",
        "API_TOKEN": "${API_TOKEN}",              // User env var
        "LOG_LEVEL": "info",                      // Hardcoded
        "NODE_ENV": "production"
      }
    }
  }
}
```

## Lifecycle and Startup

**Automatic startup:**
- When plugin is enabled, its MCP servers start automatically
- Servers remain running while plugin is active
- Restart Claude Code to apply MCP changes (enable/disable servers)

**Priority resolution:**
When user configures MCP with same name as plugin MCP:
1. User configuration takes precedence
2. Plugin server is not loaded
3. Only one server per name active at a time

**Scope precedence (for plugin MCPs):**
```
User > Project > Local > Plugin
```

If user configures a server with same name as plugin, user config wins.

## Viewing Plugin MCP Servers

Users check available servers including plugin MCPs:

```bash
/mcp
```

Output shows:
- Enterprise servers
- User-configured servers
- Project servers
- Local servers
- **Plugin servers** (marked with plugin indicator)

## Plugin MCP Architecture

### Directory Structure

```
my-plugin/
├── plugin.json
├── .mcp.json
├── skills/
│   └── managing-data/
│       └── SKILL.md
├── commands/
│   └── analyze.md
├── servers/
│   ├── api-server
│   ├── db-server.py
│   └── requirements.txt
├── config/
│   └── settings.json
├── data/
│   └── resources.json
└── README.md
```

### Server Bundling

Servers included in plugin package:
- Executable files in `servers/` directory
- Python scripts with dependencies listed in requirements.txt
- Node.js servers with package.json
- Configuration files in `config/` directory
- Data files in `data/` directory

All files packaged together when plugin distributed.

## Example: Complete Plugin with MCP

**plugin.json:**
```json
{
  "name": "database-tools",
  "version": "1.0.0",
  "description": "Database query and management tools",
  "mcpServers": {
    "database": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${CLAUDE_PLUGIN_ROOT}/servers/db-server.py",
        "--config",
        "${CLAUDE_PLUGIN_ROOT}/config/db.json"
      ],
      "env": {
        "DB_CONNECTION_STRING": "${DB_CONNECTION_STRING}",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

**.mcp.json:**
```json
{
  "mcpServers": {
    "database": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${CLAUDE_PLUGIN_ROOT}/servers/db-server.py",
        "--config",
        "${CLAUDE_PLUGIN_ROOT}/config/db.json"
      ],
      "env": {
        "DB_CONNECTION_STRING": "${DB_CONNECTION_STRING}"
      }
    }
  }
}
```

## Creating Plugin MCPs

### Step 1: Develop Server

Create server in `servers/` directory:

**servers/db-server.py:**
```python
#!/usr/bin/env python3
import json
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("database")

@mcp.tool()
def query_database(sql: str) -> dict:
    """Execute SQL query against configured database."""
    db_conn = os.getenv("DB_CONNECTION_STRING")
    # Query implementation...
    return {"results": [...]}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

### Step 2: Create Configuration

**config/db.json:**
```json
{
  "timeout": 30,
  "max_connections": 10,
  "log_queries": true
}
```

### Step 3: Define in Plugin

Add to `.mcp.json` or `plugin.json`:

```json
{
  "mcpServers": {
    "database": {
      "type": "stdio",
      "command": "python",
      "args": [
        "${CLAUDE_PLUGIN_ROOT}/servers/db-server.py",
        "--config",
        "${CLAUDE_PLUGIN_ROOT}/config/db.json"
      ],
      "env": {
        "DB_CONNECTION_STRING": "${DB_CONNECTION_STRING}"
      }
    }
  }
}
```

### Step 4: Test

Enable plugin, verify server starts:

```bash
/mcp
# Should show: database (from plugin)
```

## User Configuration for Plugin MCPs

Users can:
- Override plugin MCP with user configuration (same name takes precedence)
- Use environment variables to customize plugin MCPs
- Disable plugins entirely to stop MCP servers

Cannot:
- Remove plugin MCPs (would require uninstalling plugin)
- Modify plugin MCP definitions (define in plugin, not user config)
- Use local/project scope to override plugin MCPs (user scope takes precedence)

## Benefits of Plugin MCPs

**Automatic distribution:**
- Everyone gets same tools when plugin installed
- No manual MCP configuration needed

**Simplified setup:**
- Users don't need to know server implementation details
- Authentication, paths, ports handled by plugin

**Consistency:**
- Team uses same MCP versions
- Updates when plugin updates
- No configuration drift

**Easy integration:**
- MCPs bundled with related skills and commands
- Comprehensive feature sets in single plugin

## Common Plugin MCP Patterns

### Pattern 1: Single Tool Server

Plugin provides one focused server:

```json
{
  "mcpServers": {
    "analytics": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/analytics-server"
    }
  }
}
```

### Pattern 2: Multiple Specialized Servers

Plugin provides multiple servers for different concerns:

```json
{
  "mcpServers": {
    "api": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-gateway"
    },
    "database": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server"
    },
    "cache": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/cache-server"
    }
  }
}
```

### Pattern 3: Configurable via Environment

Plugin adapts to environment:

```json
{
  "mcpServers": {
    "api": {
      "type": "stdio",
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "env": {
        "API_ENV": "${API_ENVIRONMENT:-development}",
        "API_KEY": "${PLUGIN_API_KEY}",
        "CACHE_DIR": "${CLAUDE_PLUGIN_ROOT}/cache"
      }
    }
  }
}
```

## Troubleshooting Plugin MCPs

**Server not starting:**
- Verify executable file permissions: `chmod +x ${CLAUDE_PLUGIN_ROOT}/servers/api-server`
- Check command syntax in .mcp.json
- Verify ${CLAUDE_PLUGIN_ROOT} expands correctly
- Restart Claude Code

**Environment variables not set:**
- Plugin MCPs use system env variables
- User must set before starting Claude Code
- Check: `echo $VAR_NAME` before running claude

**Port conflicts:**
- If plugin server uses specific port, ensure it's available
- Use environment variable to customize port: `"port": "${PLUGIN_PORT:-8080}"`

**Multiple plugins with same server name:**
- Later plugin loaded overrides earlier one
- User configuration always takes precedence
- Rename servers to avoid conflicts: `plugin1-api`, `plugin2-api`
