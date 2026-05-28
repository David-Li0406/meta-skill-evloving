# Elicitation Reference

Collect user input during tool execution.

## Basic Elicitation

Use `ctx.elicit()` to request input from the user:

```python
from dedalus_mcp import tool, get_context

@tool(description="Create a new project")
async def create_project() -> str:
    ctx = get_context()
    
    result = await ctx.elicit(
        "What should the project be named?",
        response_type=str,
    )
    
    if result.action == "accept":
        return f"Created project: {result.data}"
    return "Cancelled"
```

## Response Types

### String Input

```python
result = await ctx.elicit("Enter name:", response_type=str)
name = result.data  # str
```

### Boolean Confirmation

```python
result = await ctx.elicit("Proceed?", response_type=bool)
confirmed = result.data  # bool
```

### Pydantic Models

```python
from pydantic import BaseModel

class DeployConfig(BaseModel):
    environment: str
    replicas: int
    dry_run: bool

@tool
async def deploy_with_config() -> str:
    ctx = get_context()
    
    result = await ctx.elicit(
        "Configure deployment:",
        response_type=DeployConfig,
    )
    
    if result.action == "accept":
        config = result.data
        return f"Deploying {config.replicas} replicas to {config.environment}"
    return "Cancelled"
```

## Result Handling

The `result` object has:

| Field | Type | Description |
|-------|------|-------------|
| `action` | `str` | `"accept"` or `"cancel"` |
| `data` | `T` | Typed response data (when accepted) |

### Pattern

```python
result = await ctx.elicit(...)

if result.action == "accept":
    # Use result.data
    pass
elif result.action == "cancel":
    # Handle cancellation
    return "Operation cancelled"
```

## Progressive Disclosure

Collect complex information step-by-step:

```python
@tool(description="Create new project")
async def create_project() -> str:
    ctx = get_context()
    
    # Step 1: Get project name
    name_result = await ctx.elicit("Project name:", response_type=str)
    if name_result.action != "accept":
        return "Cancelled"
    
    # Step 2: Get project type
    type_result = await ctx.elicit("Project type (web/api/cli):", response_type=str)
    if type_result.action != "accept":
        return "Cancelled"
    
    # Step 3: Confirm
    confirm = await ctx.elicit(
        f"Create {type_result.data} project '{name_result.data}'?",
        response_type=bool,
    )
    
    if confirm.action == "accept" and confirm.data:
        return f"Created {name_result.data}"
    return "Cancelled"
```

## Best Practices

1. **Keep prompts clear** - Users should understand what's expected
2. **Handle cancellation** - Always check `result.action`
3. **Use appropriate types** - Pydantic models for complex input
4. **Progressive disclosure** - Don't ask for everything at once
5. **Provide defaults** - Use Pydantic defaults where sensible
