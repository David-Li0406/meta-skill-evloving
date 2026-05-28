# MCP Transports Reference

Transports define how MCP servers communicate with clients. The MCP SDK supports three transport types.

## Transport Overview

| Transport | Protocol | Use Case | Stateful |
|-----------|----------|----------|----------|
| **stdio** | Standard I/O | CLI tools, local agents | Yes |
| **SSE** | Server-Sent Events | Web clients, real-time | Yes |
| **streamable-http** | HTTP/REST | Production APIs, scalable | Configurable |

## Stdio Transport

Standard input/output transport for local communication.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Local Server")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Default is stdio
    mcp.run()
    # or explicitly:
    mcp.run(transport="stdio")
```

**Run server:**
```bash
python server.py
# or with uv
uv run server.py
```

**Best for:**
- Local development
- CLI-based tools
- Agent-to-server communication
- Claude Desktop integration

## SSE Transport

Server-Sent Events for web-based real-time communication.

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SSE Server")

@mcp.tool()
def get_status() -> dict:
    return {"status": "ok"}

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

**Run server:**
```bash
python server.py
# Server runs at http://localhost:8000
```

**Best for:**
- Web browser clients
- Real-time updates
- Event streaming

## Streamable HTTP Transport (Recommended for Production)

HTTP-based transport with optional stateless mode.

### Stateless Mode (Recommended)

```python
from mcp.server.fastmcp import FastMCP

# Stateless with JSON responses - best for production
mcp = FastMCP("Production Server", stateless_http=True, json_response=True)

@mcp.tool()
def process(data: str) -> dict:
    return {"processed": data}

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    # Server runs at http://localhost:8000/mcp
```

### Stateful Mode

```python
# Stateful - maintains session state
mcp = FastMCP("Stateful Server")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Configuration options:**
```python
# Stateless with SSE streaming (instead of JSON)
mcp = FastMCP("Server", stateless_http=True)

# Stateful (default)
mcp = FastMCP("Server")
```

**Best for:**
- Production deployments
- Scalable architectures
- REST API integration
- Load balancing

## Custom Port and Host

```python
if __name__ == "__main__":
    # SSE with custom port
    mcp.run(transport="sse", port=3000)

    # Streamable HTTP with custom settings
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8080,
    )
```

## Mounting in Existing ASGI App

### Basic Mount

```python
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Mounted Server", json_response=True)

@mcp.tool()
def hello() -> str:
    return "Hello from MCP!"

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# Run with: uvicorn server:app --reload
# Endpoint: http://localhost:8000/mcp/mcp
```

### Mount at Root Path

```python
# Configure to mount at root of path
mcp = FastMCP("Server", json_response=True, streamable_http_path="/")

app = Starlette(
    routes=[
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# Endpoint: http://localhost:8000/mcp (not /mcp/mcp)
```

### Multiple Servers

```python
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

# Create multiple MCP servers
tasks_mcp = FastMCP("Tasks", stateless_http=True, json_response=True)
users_mcp = FastMCP("Users", stateless_http=True, json_response=True)

@tasks_mcp.tool()
def list_tasks() -> list:
    return []

@users_mcp.tool()
def get_user(id: str) -> dict:
    return {"id": id}

# Configure paths
tasks_mcp.settings.streamable_http_path = "/"
users_mcp.settings.streamable_http_path = "/"

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(tasks_mcp.session_manager.run())
        await stack.enter_async_context(users_mcp.session_manager.run())
        yield

app = Starlette(
    routes=[
        Mount("/tasks", app=tasks_mcp.streamable_http_app()),
        Mount("/users", app=users_mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# Endpoints:
# - http://localhost:8000/tasks
# - http://localhost:8000/users
```

## SSE App Mount

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SSE Server")

app = Starlette(
    routes=[
        Mount("/", app=mcp.sse_app()),
    ]
)
```

## CORS Configuration

For browser clients, add CORS middleware:

```python
from starlette.middleware.cors import CORSMiddleware

app = Starlette(
    routes=[Mount("/mcp", app=mcp.streamable_http_app())],
    lifespan=lifespan,
)

app = CORSMiddleware(
    app,
    allow_origins=["*"],  # Configure for production
    allow_methods=["GET", "POST", "DELETE"],
    allow_credentials=True,
    expose_headers=["Mcp-Session-Id"],  # Required for sessions
)
```

## Client Connection Examples

### Stdio Client

```python
from mcp import stdio_client, ClientSession

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
```

### HTTP Client

```python
from mcp import streamablehttp_client, ClientSession

async def main():
    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read, write, _
    ):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
```

## Transport Selection Guide

| Scenario | Recommended Transport |
|----------|----------------------|
| Local development | stdio |
| Claude Desktop | stdio |
| Web application | streamable-http (stateless) |
| Real-time updates | SSE |
| Production API | streamable-http (stateless) |
| Multiple clients | streamable-http |
| Embedded in FastAPI | streamable-http (mount) |
