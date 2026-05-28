---
title: Force Tool Usage with ModelSettings.tool_choice
impact: HIGH
impactDescription: Ensures required tools are called
tags: agent, tools, tool-choice, model-settings
---

## Force Tool Usage with ModelSettings.tool_choice

**Impact: HIGH (ensures required tools are called)**

When an agent must use a specific tool, set `tool_choice` in `ModelSettings` to force the LLM to call it.

**Incorrect (hoping LLM calls the tool):**

```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Get the weather for the user's city.",
    tools=[get_weather],
    # LLM might respond without calling the tool
)
```

**Correct (forcing tool usage):**

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather Agent",
    instructions="Get the weather for the user's city.",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="get_weather"),  # Force this tool
)
```

**Valid `tool_choice` values:**

- `"auto"`: LLM decides whether to use tools (default)
- `"required"`: LLM must use a tool (chooses which one)
- `"none"`: LLM must not use any tool
- `"tool_name"`: LLM must use the specified tool

**Important:** Set `reset_tool_choice=True` (default) to prevent infinite loops after tool calls.

Reference: [Agents Documentation - Forcing Tool Use](https://openai.github.io/openai-agents-python/agents/#forcing-tool-use)
