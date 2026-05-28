---
name: create-mcp-servers
description: Use this skill when building Model Context Protocol (MCP) servers to extend Claude's capabilities with custom tools, resources, and prompts, integrating external services and APIs.
---

# Skill body

## Overview

MCP (Model Context Protocol) servers allow Claude to interact with external tools and services. This skill guides you through creating, configuring, and integrating MCP servers using both Python and TypeScript.

## Essential Principles

1. **Never Hardcode Secrets**: Use `${VAR}` expansion in configs and environment variables in code.
2. **Use `cwd` Property**: Isolate dependencies by specifying the working directory.
3. **Always Use Absolute Paths**: Use commands like `which uv` to find paths.
4. **One Server Per Directory**: Organize each server in its own directory.
5. **Use `uv` for Python**: It handles virtual environments automatically.

## Quick Start: Creating an MCP Server

### 1. Project Setup

#### Python

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv venv && source venv/bin/activate
pip install mcp
```

#### TypeScript

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
```

### 2. Basic Server Template

#### Python Example

Create `my_server.py`:

```python
#!/usr/bin/env python3
"""my_server.py - A simple MCP server"""

from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.tool()
async def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

#### TypeScript Example

Create `src/index.ts`:

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "my-server", version: "1.0.0" });

server.setRequestHandler("tools/hello", async (input) => {
    return `Hello, ${input.name}!`;
});
```

### 3. Register with Claude

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python3",
      "args": ["/path/to/my_server.py"]
    }
  }
}
```

## Adding MCP Servers

### HTTP Transport (Recommended)

```bash
claude mcp add --transport http <name> <url>
```

### stdio Transport (Local Servers)

```bash
claude mcp add --transport stdio <name> -- <command> [args...]
```

## Security Checklist

- Never ask users to paste secrets into chat.
- Always use environment variables for credentials.
- Verify environment variable existence without showing values.

## Conclusion

This skill provides a comprehensive guide to creating and integrating MCP servers, enabling Claude to leverage external tools and services effectively.