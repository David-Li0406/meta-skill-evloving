# MCP Configuration Patterns

Configuration file and directory patterns for detecting MCP.

## Confidence

**Detection Confidence**: 90%

## Configuration Files

| File | Description |
|------|-------------|
| `claude_desktop_config.json` | Claude Desktop MCP configuration |
| `mcp.json` | Generic MCP configuration |
| `mcp-config.json` | Alternative config name |
| `.mcp/config.json` | Directory-based config |
| `mcp-server.json` | Server-specific config |

## Configuration Directories

| Directory | Description |
|-----------|-------------|
| `.mcp/` | MCP configuration directory |
| `mcp-servers/` | Server implementations |

## Configuration Keys

### claude_desktop_config.json

```json
{
  "mcpServers": {
    "server-name": {
      "command": "...",
      "args": ["..."],
      "env": {}
    }
  }
}
```

### mcp.json

```json
{
  "name": "server-name",
  "version": "1.0.0",
  "protocol_version": "2024-11-05"
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MCP_SERVER_*` | Server-specific configuration |
| `MCP_DEBUG` | Enable debug mode |
| `MCP_LOG_LEVEL` | Logging verbosity |
| `MCP_TRANSPORT` | Transport type (stdio, sse) |

## Detection Logic

1. Check for configuration files in root directory
2. Check for `.mcp/` directory presence
3. Parse JSON files for `mcpServers` key
4. Check environment for `MCP_*` variables
