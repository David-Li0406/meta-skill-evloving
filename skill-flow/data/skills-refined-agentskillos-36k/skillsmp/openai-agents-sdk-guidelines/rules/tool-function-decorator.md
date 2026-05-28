---
title: Use @function_tool Decorator for Automatic Schema
impact: HIGH
impactDescription: Automatic tool schema from function signature
tags: tool, function-tool, decorator, schema
---

## Use @function_tool Decorator for Automatic Schema

**Impact: HIGH (automatic tool schema from function signature)**

The `@function_tool` decorator automatically creates tool name, description, and parameter schema from your Python function.

**Incorrect (manual tool definition):**

```python
from agents import FunctionTool

# Manual definition is verbose and error-prone
async def run_tool(ctx, args: str) -> str:
    import json
    parsed = json.loads(args)
    return f"Weather in {parsed['city']}: Sunny"

tool = FunctionTool(
    name="get_weather",
    description="Get weather for a city",
    params_json_schema={
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
    on_invoke_tool=run_tool,
)
```

**Correct (using @function_tool):**

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city.
    
    Args:
        city: The city name to get weather for.
    """
    return f"Weather in {city}: Sunny"

# Schema is automatically generated:
# - name: "get_weather"
# - description: "Get weather for a city."
# - params: {"city": {"type": "string", "description": "The city name..."}}
```

**Works with complex types:**

```python
from typing_extensions import TypedDict
from agents import function_tool

class Location(TypedDict):
    lat: float
    long: float

@function_tool
async def fetch_weather(location: Location) -> str:
    """Fetch weather for a location.
    
    Args:
        location: The geographic coordinates.
    """
    return "sunny"
```

**Override defaults:**

```python
@function_tool(
    name_override="weather_lookup",
    description_override="Custom description",
)
def get_weather(city: str) -> str:
    """Original docstring ignored when override provided."""
    return f"Weather in {city}: Sunny"
```

Reference: [Tools Documentation - Function Tools](https://openai.github.io/openai-agents-python/tools/#function-tools)
