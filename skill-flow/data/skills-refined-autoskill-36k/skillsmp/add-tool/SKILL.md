---
name: add-tool
description: Add a new tool to an existing backend agent. Use when adding tool to agent, creating new agent capability, extending agent functionality, or when user says "add tool", "new tool", "agent capability", or "extend agent".
allowed-tools: Read, Edit, Grep
---

# Add Tool to Agent

This skill adds a new tool to an existing agent following the established patterns.

## Prerequisites

Before adding a tool, gather:
1. **Target agent** (which agent file to modify)
2. **Tool name** (snake_case, e.g., `search_messages`)
3. **Tool purpose** (what it does)
4. **Parameters** (inputs the tool accepts)
5. **Return value** (what the tool returns)

## Steps

### 1. Add Tool Definition

Add to `TOOL_DEFINITIONS` in the agent file:

```python
{
    "name": "tool_name",
    "description": "Detailed description. Be specific so Claude knows when to use it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "What this parameter is for",
            },
            "param2": {
                "type": "integer",
                "description": "What this parameter is for",
                "minimum": 1,
                "maximum": 100,
            },
            "optional_param": {
                "type": "boolean",
                "description": "Optional parameter with default",
            },
        },
        "required": ["param1"],
    },
},
```

### 2. Add Tool Handler

Add case to the `_handle_tool` method's match statement:

```python
case "tool_name":
    result = await self._tool_name(**tool_input)
```

### 3. Implement Tool Method

Add the implementation method:

```python
async def _tool_name(
    self,
    param1: str,
    param2: int = 10,
    optional_param: bool = False,
) -> dict[str, Any]:
    """
    Brief description of what this tool does.

    Args:
        param1: Description
        param2: Description with default
        optional_param: Description

    Returns:
        Result dictionary
    """
    # If calling MCP server:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{self.mcp_base_url}/tools/tool_name",
            json={
                "param1": param1,
                "param2": param2,
                "optional_param": optional_param,
            },
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
```

### 4. Update System Prompt

Add tool description to `SYSTEM_PROMPT`:

```python
### tool_name
Use this tool when {specific situation}. Provide {required params}.
Returns {what it returns}.
```

## Tool Schema Reference

### Supported Types

| Type | JSON Schema | Python Type |
|------|-------------|-------------|
| String | `"type": "string"` | `str` |
| Integer | `"type": "integer"` | `int` |
| Number | `"type": "number"` | `float` |
| Boolean | `"type": "boolean"` | `bool` |
| Array | `"type": "array", "items": {...}` | `list` |
| Object | `"type": "object", "properties": {...}` | `dict` |

### Constraints

```python
# String constraints
"minLength": 1,
"maxLength": 100,
"pattern": "^[a-z]+$",
"enum": ["option1", "option2"],

# Number constraints
"minimum": 0,
"maximum": 100,
"exclusiveMinimum": 0,
"multipleOf": 5,

# Array constraints
"minItems": 1,
"maxItems": 10,
"uniqueItems": True,
```

## Checklist

After adding, verify:

- [ ] Tool definition added to `TOOL_DEFINITIONS`
- [ ] Case added to `_handle_tool` match statement
- [ ] Implementation method created with proper typing
- [ ] System prompt updated with tool description
- [ ] Tool works with MCP server (if applicable)
- [ ] Error handling returns structured error dict

## Common Patterns

### MCP Tool Call

```python
async def _tool_name(self, param: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{self.mcp_base_url}/tools/tool_name",
            json={"param": param},
            timeout=30.0,
        )
        response.raise_for_status()
        return response.json()
```

### Database Operation

```python
async def _tool_name(self, param: str) -> dict:
    async with self.db_session_factory() as session:
        result = await some_service.do_operation(session, param)
        return {"success": True, "data": result}
```

### Error Handling

```python
async def _tool_name(self, param: str) -> dict:
    try:
        # ... operation ...
        return {"success": True, "data": result}
    except SomeError as e:
        return {"error": True, "message": str(e)}
```

## Reference

- `.claude/rules/backend/agents.md` - Agent patterns and anti-patterns
