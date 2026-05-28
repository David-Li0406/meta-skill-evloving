# MCP Server Configuration - Google Gemini CLI

Gemini CLI supports MCP servers with both user and project-level configurations.

## Basic Commands

```bash
# List MCP servers
gemini mcp list

# Add MCP server
gemini mcp add [options] <name> <commandOrUrl> [args...]

# Add with scope
gemini mcp add <name> <command> --scope user     # User level
gemini mcp add <name> <command> --scope project  # Project level

# Remove a server
gemini mcp remove <server-name>
```

## Transport Configuration

Gemini CLI uses different URL keys for different transport types:

**HTTP Transport:**
```json
{
  "mcpServers": {
    "playwright": {
      "httpUrl": "http://url/mcp"
    }
  }
}
```

**SSE Transport:**
```json
{
  "mcpServers": {
    "playwright": {
      "url": "http://url/sse"
    }
  }
}
```

**stdio Transport:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    }
  }
}
```

## Configuration File Locations

- **User level**: `~/.gemini/settings.json`
- **Project level**: `.gemini/settings.json` (in project root)
