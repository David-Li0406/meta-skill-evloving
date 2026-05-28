# Bridge Tool Extension Reference

Bridges can wrap existing Scribe tools with custom behavior and register entirely new tools.

## Concepts

### Tool Wrapping

Wrap existing Scribe tools to add pre/post processing:

```python
original: append_entry(message, status)
         │
         ▼
┌─────────────────────────────┐
│     BridgeToolWrapper       │
├─────────────────────────────┤
│  pre_hook(args, kwargs)     │ ← Modify arguments
│         │                   │
│         ▼                   │
│  original_tool(*args)       │ ← Call original
│         │                   │
│         ▼                   │
│  post_hook(result)          │ ← Modify result
└─────────────────────────────┘
         │
         ▼
    wrapped result
```

### Custom Tools

Register entirely new tools exposed via MCP:

```
MCP Server
    │
    ├── scribe.append_entry     (core tool)
    ├── scribe.set_project      (core tool)
    ├── mybridge:audit          (custom tool)
    └── mybridge:sync           (custom tool)
```

## BridgeToolWrapper

### Import

```python
from scribe_mcp.bridges import BridgeToolWrapper
```

### Constructor

```python
wrapper = BridgeToolWrapper(
    bridge_id: str,
    tool_name: str,
    original_tool: Callable
)
```

### Adding Hooks

#### `add_pre_hook()`

```python
def add_pre_hook(self, hook: Callable) -> "BridgeToolWrapper":
    """Add a pre-execution hook. Returns self for chaining."""
```

**Hook signature:**
```python
async def pre_hook(args: tuple, kwargs: dict) -> tuple[tuple, dict]:
    """Modify arguments before tool execution."""
    return args, kwargs
```

**Sync hooks are also supported:**
```python
def pre_hook(args, kwargs):
    return args, kwargs
```

#### `add_post_hook()`

```python
def add_post_hook(self, hook: Callable) -> "BridgeToolWrapper":
    """Add a post-execution hook. Returns self for chaining."""
```

**Hook signature:**
```python
async def post_hook(result: Any, args: tuple, kwargs: dict) -> Any:
    """Modify result after tool execution."""
    return result
```

### Execution

```python
result = await wrapper(*args, **kwargs)
```

**Execution flow:**
1. Execute all pre-hooks in order
2. Call original tool with modified args
3. Execute all post-hooks in order
4. Return final result

### Error Isolation

Hook failures are isolated:
```python
def failing_pre_hook(args, kwargs):
    raise ValueError("Hook failed")
    # Exception logged, execution continues
    # Original args/kwargs used
```

### Example

```python
from scribe_mcp.bridges import BridgeToolWrapper

# Original tool
async def append_entry(message: str, status: str = "info") -> dict:
    return {"message": message, "status": status, "logged": True}

# Create wrapper
wrapper = BridgeToolWrapper("my_bridge", "append_entry", append_entry)

# Add pre-hook to inject metadata
async def add_bridge_meta(args, kwargs):
    kwargs["meta"] = kwargs.get("meta", {})
    kwargs["meta"]["bridge_id"] = "my_bridge"
    return args, kwargs

# Add post-hook to audit
async def audit_result(result, args, kwargs):
    print(f"Logged: {result['message']}")
    result["audited"] = True
    return result

# Chain hooks
wrapper.add_pre_hook(add_bridge_meta).add_post_hook(audit_result)

# Use wrapped tool
result = await wrapper(message="Test", status="success")
# Result: {"message": "Test", "status": "success", "logged": True, "audited": True}
```

## BridgeToolRegistry

### Import

```python
from scribe_mcp.bridges import BridgeToolRegistry, get_tool_registry
```

### Global Singleton

```python
registry = get_tool_registry()
```

### Methods

#### `wrap_tool()`

```python
def wrap_tool(
    self,
    bridge_id: str,
    tool_name: str,
    original_tool: Callable
) -> BridgeToolWrapper:
    """Wrap an existing tool and register it."""
```

Returns the wrapper for adding hooks.

#### `register_custom_tool()`

```python
def register_custom_tool(
    self,
    bridge_id: str,
    tool_name: str,
    implementation: Callable,
    schema: Optional[Dict] = None,
    description: str = ""
) -> None:
    """Register a completely custom tool."""
```

**Parameters:**
- `bridge_id`: Bridge identifier
- `tool_name`: Tool name (without prefix)
- `implementation`: Async callable
- `schema`: JSON Schema for parameters
- `description`: Human-readable description

#### `get_wrapped_tool()`

```python
def get_wrapped_tool(
    self,
    bridge_id: str,
    tool_name: str
) -> Optional[BridgeToolWrapper]:
    """Get a wrapped tool by bridge and name."""
```

#### `get_custom_tool()`

```python
def get_custom_tool(
    self,
    bridge_id: str,
    tool_name: str
) -> Optional[Callable]:
    """Get a custom tool by bridge and name."""
```

#### `list_bridge_tools()`

```python
def list_bridge_tools(self, bridge_id: str) -> Dict[str, List[str]]:
    """List all tools for a bridge."""
```

Returns:
```python
{
    "wrapped": ["append_entry", "query_entries"],
    "custom": ["audit", "sync"]
}
```

#### `list_all_custom_tools()`

```python
def list_all_custom_tools(self) -> List[Dict[str, Any]]:
    """List all custom tools for MCP registration."""
```

Returns:
```python
[
    {
        "bridge_id": "my_bridge",
        "tool_name": "audit",
        "full_name": "my_bridge:audit",
        "description": "Custom audit logging",
        "schema": {"project": "string", "action": "string"}
    }
]
```

#### `unregister_bridge_tools()`

```python
def unregister_bridge_tools(self, bridge_id: str) -> None:
    """Remove all tools for a bridge."""
```

## MCP Integration

### Tool Namespacing

Custom tools are namespaced with bridge ID:
```
bridge_id:tool_name
```

Examples:
- `council_mcp:orchestrate`
- `analytics_bridge:report`
- `my_bridge:audit`

### Server Integration

In `server.py`:

```python
from bridges.tools import get_tool_registry

# List tools
@server.list_tools()
async def handle_list_tools():
    tools = [...]  # Core Scribe tools

    # Add bridge custom tools
    registry = get_tool_registry()
    for tool in registry.list_all_custom_tools():
        tools.append({
            "name": tool["full_name"],
            "description": tool["description"],
            "inputSchema": tool["schema"]
        })

    return tools

# Call tool
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if ":" in name:
        # Bridge custom tool
        bridge_id, tool_name = name.split(":", 1)
        tool = get_tool_registry().get_custom_tool(bridge_id, tool_name)
        if tool:
            return await tool(**arguments)

    # Core Scribe tool
    ...
```

## Complete Examples

### Wrapped Tool Example

```python
from scribe_mcp.bridges import get_tool_registry
from scribe_mcp.tools.append_entry import append_entry

# Get registry
registry = get_tool_registry()

# Wrap append_entry
wrapped = registry.wrap_tool("council_mcp", "append_entry", append_entry)

# Add audit hook
async def audit_entries(result, args, kwargs):
    # Log all entries to audit system
    await audit_system.log(result)
    return result

wrapped.add_post_hook(audit_entries)

# Now all append_entry calls through this wrapper are audited
```

### Custom Tool Example

```python
from scribe_mcp.bridges import get_tool_registry

registry = get_tool_registry()

# Define custom tool
async def orchestrate(
    agents: list,
    task: str,
    timeout_seconds: int = 300
) -> dict:
    """Orchestrate multiple agents for a task."""
    results = []
    for agent in agents:
        result = await run_agent(agent, task, timeout_seconds)
        results.append(result)
    return {
        "task": task,
        "agents": agents,
        "results": results,
        "success": all(r["success"] for r in results)
    }

# Register with schema
registry.register_custom_tool(
    bridge_id="council_mcp",
    tool_name="orchestrate",
    implementation=orchestrate,
    schema={
        "type": "object",
        "properties": {
            "agents": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of agent IDs"
            },
            "task": {
                "type": "string",
                "description": "Task description"
            },
            "timeout_seconds": {
                "type": "integer",
                "default": 300,
                "description": "Timeout per agent"
            }
        },
        "required": ["agents", "task"]
    },
    description="Orchestrate multiple agents for a task"
)

# Tool available as: council_mcp:orchestrate
```

### Plugin with Tools

```python
from scribe_mcp.bridges import BridgePlugin, get_tool_registry

class MyBridgePlugin(BridgePlugin):

    async def on_activate(self) -> None:
        """Register tools when bridge activates."""
        registry = get_tool_registry()

        # Register custom tools
        registry.register_custom_tool(
            self.bridge_id,
            "sync",
            self._sync_tool,
            description="Sync with external system"
        )

        registry.register_custom_tool(
            self.bridge_id,
            "status",
            self._status_tool,
            description="Get sync status"
        )

    async def on_deactivate(self) -> None:
        """Unregister tools when bridge deactivates."""
        registry = get_tool_registry()
        registry.unregister_bridge_tools(self.bridge_id)

    async def _sync_tool(self, project: str) -> dict:
        """Custom sync tool implementation."""
        return {"synced": True, "project": project}

    async def _status_tool(self) -> dict:
        """Custom status tool implementation."""
        return {"healthy": True, "last_sync": "2025-01-01T00:00:00Z"}
```

## Best Practices

### 1. Clean Up on Deactivate

```python
async def on_deactivate(self) -> None:
    registry = get_tool_registry()
    registry.unregister_bridge_tools(self.bridge_id)
```

### 2. Provide Good Schemas

```python
registry.register_custom_tool(
    bridge_id,
    "my_tool",
    implementation,
    schema={
        "type": "object",
        "properties": {
            "required_param": {"type": "string", "description": "..."},
            "optional_param": {"type": "integer", "default": 10}
        },
        "required": ["required_param"]
    },
    description="Clear description of what tool does"
)
```

### 3. Keep Hooks Fast

```python
# Good: Quick modification
async def pre_hook(args, kwargs):
    kwargs["timestamp"] = time.time()
    return args, kwargs

# Bad: Long operation
async def pre_hook(args, kwargs):
    await external_api.validate()  # Slow!
    return args, kwargs
```

### 4. Handle Errors Gracefully

```python
async def custom_tool(data: dict) -> dict:
    try:
        result = await process(data)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```
