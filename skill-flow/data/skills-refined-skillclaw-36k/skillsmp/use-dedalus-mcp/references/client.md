# MCPClient Reference

Connect to MCP servers programmatically.

## Basic Usage

```python
import asyncio
from dedalus_mcp.client import MCPClient

async def main():
    client = await MCPClient.connect("http://127.0.0.1:8000/mcp")
    try:
        # List tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools.tools]}")
        
        # Call a tool
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(f"Result: {result}")
    finally:
        await client.close()

asyncio.run(main())
```

## Connection Methods

### URL Connection

```python
client = await MCPClient.connect("http://localhost:8000/mcp")
```

### With Authentication

```python
from dedalus_mcp.client import MCPClient, BearerAuth

client = await MCPClient.connect(
    "http://localhost:8000/mcp",
    auth=BearerAuth(access_token="your-token")
)
```

## Tools

### List Tools

```python
tools = await client.list_tools()

for tool in tools.tools:
    print(f"Name: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Schema: {tool.inputSchema}")
```

### Call Tool

```python
result = await client.call_tool("tool_name", {"param1": "value1"})
```

## Resources

### List Resources

```python
resources = await client.list_resources()

for r in resources.resources:
    print(f"URI: {r.uri}")
    print(f"Name: {r.name}")
    print(f"Type: {r.mimeType}")
```

### Read Resource

```python
content = await client.read_resource("config://app")
print(content)
```

### Resource Schema

| Field | Type | Description |
|-------|------|-------------|
| `uri` | `str` | Resource identifier (e.g., `file:///config.json`) |
| `name` | `str` | Human-readable name |
| `description` | `str | None` | Description of contents |
| `mimeType` | `str | None` | Content type (e.g., `application/json`) |

## Prompts

### List Prompts

```python
prompts = await client.list_prompts()

for p in prompts.prompts:
    print(f"Name: {p.name}")
    print(f"Description: {p.description}")
    print(f"Arguments: {p.arguments}")
```

### Get Prompt

```python
result = await client.get_prompt("summarize", {"text": "..."})

for message in result.messages:
    print(f"{message.role}: {message.content}")
```

## Resource Templates

Resource templates show what URI patterns exist:

```python
# Template: user://{user_id}/profile
# Use with actual URI:
content = await client.read_resource("user://123/profile")
```

## Error Handling

```python
from dedalus_mcp.client import MCPError

try:
    result = await client.call_tool("unknown_tool", {})
except MCPError as e:
    print(f"MCP Error: {e}")
```

## Context Manager

```python
async with await MCPClient.connect("http://localhost:8000/mcp") as client:
    result = await client.call_tool("add", {"a": 1, "b": 2})
    # Client automatically closed
```

## Roots (Workspace Access)

Update workspace roots during a session:

```python
await client.set_roots([
    {"uri": "file:///path/to/project"},
    {"uri": "file:///path/to/config"},
])
```

## Best Practices

1. **Always close connections** - Use context manager or explicit `close()`
2. **Handle errors** - MCP calls can fail
3. **Check capabilities** - Not all servers support all features
4. **Use async** - All client methods are async
