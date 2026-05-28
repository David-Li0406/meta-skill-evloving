---
name: mcp-integration
description: Use this skill when you need to integrate Model Context Protocol (MCP) servers into Claude Code plugins, whether for adding, configuring, or discovering MCP servers.
---

# MCP Integration for Claude Code Plugins

## Overview

Model Context Protocol (MCP) enables Claude Code plugins to integrate with external services and APIs by providing structured tool access. Use MCP integration to expose external service capabilities as tools within Claude Code.

**Key capabilities:**

- Connect to external services (databases, APIs, file systems)
- Provide 10+ related tools from a single service
- Handle OAuth and complex authentication flows
- Bundle MCP servers with plugins for automatic setup

## MCP Server Configuration Methods

Plugins can bundle MCP servers in two ways:

### Method 1: Dedicated .mcp.json (Recommended)

Create a `.mcp.json` file at the plugin root:

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}"
    }
  }
}
```

**Benefits:**

- Clear separation of concerns
- Easier to maintain
- Better for multiple servers

### Method 2: Inline in plugin.json

Add an `mcpServers` field to `plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Benefits:**

- Single configuration file
- Good for simple single-server plugins

## Discovering MCP Servers

Find existing MCP servers for your plugin using PulseMCP, the comprehensive MCP server directory with 6,800+ servers.

**Discovery workflow:**

1. Search PulseMCP using Tavily extract on `https://www.pulsemcp.com/servers?q=[keyword]`
2. Evaluate results by classification (official vs community), popularity, and relevance
3. Fetch detail pages for GitHub links and configuration examples
4. Generate `.mcp.json` configuration based on server type

## MCP Server Types

### stdio (Local Process)

Execute local MCP servers as child processes. Best for local tools and custom servers.

**Configuration:**

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"],
    "env": {
      "LOG_LEVEL": "debug"
    }
  }
}
```

**Use cases:**

- File system access
- Local database connections
- Custom MCP servers
- NPM-packaged MCP servers

**Process management:**

- Claude Code spawns and manages the process
- Communicates via stdin/stdout
- Terminates when Claude Code exits

### SSE (Server-Sent Events)

Connect to hosted MCP servers using Server-Sent Events for real-time updates.

### HTTP and WebSocket

Integrate with external services using HTTP and WebSocket protocols for communication.

**Configuration examples and use cases for these types can be added as needed.**