---
name: mcp-develop
description: Build MCP (Model Context Protocol) servers that expose tools, resources, and prompts to AI applications. Emphasizes Streamable HTTP transport for production deployments (supports multiple clients, sessions, resumability). Covers Python SDK setup, server implementation, transport configuration, and testing. Use when creating MCP servers, integrating tools with Claude/ChatGPT, or building AI-accessible APIs.
---

# MCP Server Development Guide

Guide for building Model Context Protocol (MCP) servers that expose tools, resources, and prompts to AI applications like Claude and ChatGPT.

## Specification Version Check

**Current Version**: `2025-11-25`

Before starting development, verify you're using the latest specification:
- **Specification**: https://modelcontextprotocol.io/specification/2025-11-25
- **Changelog**: https://modelcontextprotocol.io/specification/2025-11-25/changelog

Key changes in 2025-11-25:
- Tasks utility (experimental) for durable request tracking
- Icon metadata for tools/resources/prompts
- OAuth Client ID Metadata Documents
- Polling SSE streams support
- HTTP 403 for invalid Origin headers

## What is MCP?

MCP is an open protocol enabling AI applications to connect to external tools and data sources. Think of it as a "USB-C port" for AI - a standardized interface for connecting any AI application to any tool.

**Core Capabilities:**
- **Tools**: Executable functions AI models can call (search, calculate, API calls)
- **Resources**: Data and context exposed to users/AI (files, database records)
- **Prompts**: Templated messages and workflows

**Official Documentation:**
- Introduction: https://modelcontextprotocol.io/docs/getting-started/intro
- Build Server: https://modelcontextprotocol.io/docs/develop/build-server
- SDKs: https://modelcontextprotocol.io/docs/sdk

## Transport Types

MCP supports two standard transports:

| Transport | Use Case | Clients | Complexity |
|-----------|----------|---------|------------|
| **stdio** | Local tools, Claude Desktop | Single | Low |
| **Streamable HTTP** | Remote servers, production | Multiple concurrent | Medium-High |

### Prefer Streamable HTTP for Production

**stdio** is simpler but limited to local subprocess communication.

**Streamable HTTP** is the recommended transport for:
- Production deployments
- Multiple concurrent AI clients
- Remote server hosting
- Session management and resumability
- Web-accessible tools

## Streamable HTTP Transport

Full specification: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports

### Architecture

- Single HTTP endpoint supporting POST and GET (e.g., `https://example.com/mcp`)
- Optional Server-Sent Events (SSE) for streaming responses
- Session management via `Mcp-Session-Id` header
- Protocol version via `MCP-Protocol-Version` header

### Required Security

```python
# MANDATORY for all HTTP MCP servers:

# 1. Validate Origin header (DNS rebinding protection)
@app.middleware("http")
async def validate_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    if origin and not is_allowed_origin(origin):
        return JSONResponse(status_code=403, content={"error": "Invalid origin"})
    return await call_next(request)

# 2. Bind to localhost only when running locally
# Use 127.0.0.1, NOT 0.0.0.0

# 3. Implement authentication for all connections
```

### HTTP Methods

**POST /mcp** - Client sends messages to server:
- JSON-RPC request → Server returns JSON or SSE stream
- JSON-RPC notification/response → Server returns 202 Accepted

**GET /mcp** - Client listens for server messages:
- Returns SSE stream with server-initiated requests/notifications
- Server may return 405 if SSE not supported

### Session Flow

```
1. Client: POST InitializeRequest (no session ID)
   Server: 200 OK + Mcp-Session-Id header

2. Client: All subsequent requests include Mcp-Session-Id header

3. Client: DELETE /mcp with session ID (optional termination)
   Server: Session expired → 404 Not Found
```

### Required Headers

```http
POST /mcp HTTP/1.1
Content-Type: application/json
Accept: application/json, text/event-stream
MCP-Protocol-Version: 2025-11-25
Mcp-Session-Id: <session-id>  # After initialization
```

## Python SDK Setup

**Repository**: https://github.com/modelcontextprotocol/python-sdk

### Installation

```bash
pip install mcp
```

### Basic Server (stdio transport)

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search",
            description="Search for information",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search":
        query = arguments["query"]
        # Perform search
        result = f"Results for: {query}"
        return [TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream)

    asyncio.run(main())
```

### HTTP Server (Streamable HTTP transport)

For production, wrap the MCP server with FastAPI:

```python
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse, JSONResponse
from mcp.server import Server
from mcp.types import Tool, TextContent
import json
import uuid

app = FastAPI()

# MCP Server instance
mcp_server = Server("my-http-server")

# Session storage (use Redis in production)
sessions: dict[str, dict] = {}

@mcp_server.list_tools()
async def list_tools():
    return [
        Tool(
            name="greet",
            description="Greet a person",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        )
    ]

@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "greet":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

@app.middleware("http")
async def validate_origin(request: Request, call_next):
    """Validate Origin header for security"""
    origin = request.headers.get("origin")
    allowed_origins = ["http://localhost:3000", "https://claude.ai"]

    if origin and origin not in allowed_origins:
        return JSONResponse(
            status_code=403,
            content={"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid origin"}}
        )
    return await call_next(request)

@app.post("/mcp")
async def handle_post(request: Request):
    """Handle MCP messages via POST"""
    body = await request.json()
    session_id = request.headers.get("mcp-session-id")
    protocol_version = request.headers.get("mcp-protocol-version", "2025-03-26")

    # Handle initialization
    if body.get("method") == "initialize":
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"protocol_version": protocol_version}

        response = {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "protocolVersion": "2025-11-25",
                "serverInfo": {"name": "my-http-server", "version": "1.0.0"},
                "capabilities": {"tools": {}}
            }
        }
        return JSONResponse(
            content=response,
            headers={"Mcp-Session-Id": session_id}
        )

    # Validate session for other requests
    if not session_id or session_id not in sessions:
        return JSONResponse(status_code=400, content={"error": "Invalid session"})

    # Handle tool calls and other methods
    # ... process JSON-RPC message through mcp_server

    return JSONResponse(content={"jsonrpc": "2.0", "id": body.get("id"), "result": {}})

@app.get("/mcp")
async def handle_get(request: Request):
    """SSE stream for server-initiated messages"""
    session_id = request.headers.get("mcp-session-id")

    if not session_id or session_id not in sessions:
        return JSONResponse(status_code=400, content={"error": "Invalid session"})

    async def event_stream():
        # Send keep-alive or server-initiated messages
        yield f"data: {json.dumps({'type': 'ping'})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.delete("/mcp")
async def handle_delete(request: Request):
    """Terminate session"""
    session_id = request.headers.get("mcp-session-id")

    if session_id and session_id in sessions:
        del sessions[session_id]
        return Response(status_code=204)

    return JSONResponse(status_code=404, content={"error": "Session not found"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)  # localhost only!
```

## Testing Your Server

### MCP Inspector

Use the official MCP Inspector for testing:
https://modelcontextprotocol.io/docs/tools/inspector

### Manual Testing with curl

```bash
# Initialize session
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "MCP-Protocol-Version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","clientInfo":{"name":"test","version":"1.0"}}}'

# List tools (with session ID from init response)
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: <session-id>" \
  -H "MCP-Protocol-Version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# Call a tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: <session-id>" \
  -H "MCP-Protocol-Version: 2025-11-25" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"greet","arguments":{"name":"World"}}}'
```

## Connecting to Claude Code

### Local Server (stdio)

Add to `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Remote Server (HTTP)

Add to `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "my-http-server": {
      "url": "https://my-server.example.com/mcp"
    }
  }
}
```

## Available SDKs

All SDKs provide identical functionality:

| Language | Repository |
|----------|------------|
| Python | https://github.com/modelcontextprotocol/python-sdk |
| TypeScript | https://github.com/modelcontextprotocol/typescript-sdk |
| Go | https://github.com/modelcontextprotocol/go-sdk |
| Kotlin | https://github.com/modelcontextprotocol/kotlin-sdk |
| Java | https://github.com/modelcontextprotocol/java-sdk |
| C# | https://github.com/modelcontextprotocol/csharp-sdk |
| Rust | https://github.com/modelcontextprotocol/rust-sdk |
| Swift | https://github.com/modelcontextprotocol/swift-sdk |
| Ruby | https://github.com/modelcontextprotocol/ruby-sdk |
| PHP | https://github.com/modelcontextprotocol/php-sdk |

## Quick Reference

### JSON-RPC Methods

| Method | Description |
|--------|-------------|
| `initialize` | Start session, negotiate capabilities |
| `initialized` | Client confirms initialization |
| `tools/list` | List available tools |
| `tools/call` | Execute a tool |
| `resources/list` | List available resources |
| `resources/read` | Read a resource |
| `prompts/list` | List available prompts |
| `prompts/get` | Get a prompt template |

### Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success with JSON body |
| 202 | Accepted (notifications) |
| 400 | Bad request / missing session |
| 403 | Invalid origin |
| 404 | Session expired |
| 405 | Method not allowed |

## Checklist for New MCP Server

- [ ] Choose transport: stdio (local) or Streamable HTTP (production)
- [ ] Install SDK: `pip install mcp`
- [ ] Define tools with proper JSON Schema input definitions
- [ ] Implement tool handlers
- [ ] For HTTP: Add Origin validation middleware
- [ ] For HTTP: Bind to 127.0.0.1 for local, implement auth for remote
- [ ] For HTTP: Implement session management
- [ ] Test with MCP Inspector
- [ ] Add to Claude Code config (`.claude/mcp.json`)
- [ ] Document available tools for users

## Reference Links

- **Protocol Specification**: https://modelcontextprotocol.io/specification/2025-11-25
- **Transport Details**: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- **Server Features**: https://modelcontextprotocol.io/specification/2025-11-25/server
- **Security Best Practices**: https://modelcontextprotocol.io/specification/2025-11-25/basic/security
- **Build Server Guide**: https://modelcontextprotocol.io/docs/develop/build-server
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
