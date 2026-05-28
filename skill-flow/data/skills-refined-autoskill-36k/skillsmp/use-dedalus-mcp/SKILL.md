---
name: use-dedalus-mcp
description: 'Use when developers need to build MCP (Model Context Protocol) servers with dedalus_mcp—covers creating tools via @tool, exposing resources via @resource, defining user prompts via @prompt, using context utilities (progress, info, cancellation), and registering components modularly with collect().'
---

# Dedalus MCP Server

`dedalus_mcp` is a Python framework for building MCP (Model Context Protocol) servers. Build once, works with any MCP-compatible client.

## Installation

```bash
pip install dedalus-mcp dedalus-labs
```

## Quick Start

```python
from dedalus_mcp import MCPServer, tool

@tool(description="Add two numbers")
def add(a: int, b: int) -> int:
    return a + b

server = MCPServer("calculator")
server.collect(add)

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.serve())
```

Run with: `python server.py` → Serves at `http://127.0.0.1:8000/mcp`

## Server Primitives

MCP servers expose three types of capabilities:

| Primitive | Control | Description |
|-----------|---------|-------------|
| **Tools** | Model | Functions the LLM calls during reasoning |
| **Resources** | Model/User | Data the LLM can read for context |
| **Prompts** | User | Message templates users select and render |

## Tools

Tools let agents call your Python functions. Decorate, register, serve.

### Basic Tool

```python
from dedalus_mcp import tool

@tool(description="Multiply two numbers")
def multiply(a: int, b: int) -> int:
    return a * b
```

Type hints become JSON Schema automatically.

### Async Tools

```python
import httpx

@tool(description="Fetch user data")
async def get_user(user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.example.com/users/{user_id}")
        return resp.json()
```

### Context Access

Use `get_context()` for logging, progress, and cancellation:

```python
import anyio
from dedalus_mcp import tool, get_context

@tool(description="Process files with progress")
async def process_files(paths: list[str]) -> dict:
    ctx = get_context()
    
    # Logging
    await ctx.info("Starting", data={"count": len(paths)})
    
    processed = 0
    try:
        # Progress tracking
        async with ctx.progress(total=len(paths)) as tracker:
            for path in paths:
                await anyio.sleep(0.01)  # Simulate work
                processed += 1
                await tracker.advance(1)
    except anyio.get_cancelled_exc_class():
        await ctx.warning("Cancelled", data={"processed": processed})
        raise
    
    return {"processed": processed}
```

### Context Methods

| Method | Description |
|--------|-------------|
| `ctx.info(msg, data={})` | Info-level log |
| `ctx.debug(msg, data={})` | Debug-level log |
| `ctx.warning(msg, data={})` | Warning-level log |
| `ctx.progress(total=N)` | Progress tracker context manager |
| `ctx.cancelled` | Check if request was cancelled |

## Resources

Resources provide read-only data for LLM context.

### Basic Resource

```python
from dedalus_mcp import resource

@resource("config://app", description="Application config")
def get_config() -> str:
    return json.dumps({"debug": True, "version": "1.0"})
```

### Decorator Parameters

```python
@resource(
    uri="file:///data/users.json",
    name="Users Database",
    description="All user records",
    mime_type="application/json"
)
def users_data() -> str:
    return json.dumps(load_users())
```

### Binary Resources

```python
@resource("image://logo", mime_type="image/png")
def logo() -> bytes:
    return Path("logo.png").read_bytes()
```

### Resource Templates

For dynamic URIs:

```python
from dedalus_mcp import resource_template

@resource_template(
    "user-profile",
    uri_template="resource://users/{user_id}",
    description="User profile by ID",
)
async def user_profile(user_id: str) -> str:
    user = await fetch_user(user_id)
    return json.dumps(user)
```

## Prompts

Prompts are user-controlled message templates.

### Basic Prompt

```python
from dedalus_mcp import prompt

@prompt("summarize", description="Summarize content")
def summarize_prompt(arguments: dict[str, str] | None):
    text = (arguments or {}).get("text", "")
    return [("user", f"Please summarize:\n\n{text}")]
```

### Multi-Message Prompt

```python
@prompt("code-review", description="Review code for issues")
def code_review(arguments: dict[str, str] | None):
    code = (arguments or {}).get("code", "")
    language = (arguments or {}).get("language", "python")
    return [
        ("user", f"Review this {language} code for bugs and improvements:"),
        ("user", f"```{language}\n{code}\n```"),
    ]
```

### Async Prompt with Context

```python
@prompt("generate-report", description="Generate a report")
async def generate_report(arguments: dict[str, str] | None):
    ctx = get_context()
    await ctx.info("Rendering prompt", data={"args": arguments or {}})
    return [("user", "Generate a concise weekly report for this project.")]
```

## Server Registration

### Modular Pattern

Dedalus decouples decoration from registration:

```python
from dedalus_mcp import MCPServer, tool

# Decorator just attaches metadata
@tool(description="Add numbers")
def add(a: int, b: int) -> int:
    return a + b

# collect() registers with server
server = MCPServer("calculator")
server.collect(add)
```

Same tool can be registered with multiple servers:

```python
server_a.collect(add)
server_b.collect(add)
```

### Collect from Modules

```python
from tools import math_tools, text_tools

server = MCPServer("multi")
server.collect_from(math_tools, text_tools)
```

### Binding Context Manager

```python
server = MCPServer("my-server")

with server.binding():
    # All decorated functions here auto-register
    @tool(description="...")
    def my_tool(): ...
```

## Running the Server

```python
server = MCPServer("my-server")
server.collect(add, multiply, get_config)

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.serve())
```

Default: `http://127.0.0.1:8000/mcp`

### Custom Port

```python
asyncio.run(server.serve(port=9000))
```

## Testing

### Unit Test Tools Directly

Tools are just functions:

```python
def test_add():
    assert add(2, 3) == 5

async def test_async_tool():
    result = await fetch_user("123")
    assert result["id"] == "123"
```

### Test Registration

```python
def test_registration():
    server = MCPServer("test")
    server.collect(add, multiply)
    
    names = list(server.tool_names)
    assert "add" in names
    assert "multiply" in names
```

### Isolation

Each test gets a clean state (no globals):

```python
def test_a():
    server = MCPServer("test-a")
    server.collect(tool_a)
    # No teardown needed

def test_b():
    server = MCPServer("test-b")
    server.collect(tool_b)
    # Completely independent
```

## Connecting with Dedalus SDK

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

client = AsyncDedalus()
runner = DedalusRunner(client)

# Hosted MCP server (marketplace slug)
response = await runner.run(
    input="Search for auth docs",
    model="anthropic/claude-sonnet-4-20250514",
    mcp_servers=["your-org/your-server"],
)

# Local MCP server
response = await runner.run(
    input="Add 5 and 3",
    model="openai/gpt-4o-mini",
    mcp_servers=["http://localhost:8000/mcp"],
)
```

## References

- **Elicitation**: See [references/elicitation.md](references/elicitation.md) for user input collection
- **Sampling**: See [references/sampling.md](references/sampling.md) for nested LLM calls
- **Client**: See [references/client.md](references/client.md) for MCPClient usage
