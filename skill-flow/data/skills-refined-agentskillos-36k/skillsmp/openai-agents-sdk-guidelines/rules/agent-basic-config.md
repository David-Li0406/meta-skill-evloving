---
title: Configure Agent with Name, Instructions, and Tools
impact: CRITICAL
impactDescription: Foundation of all agent workflows
tags: agent, configuration, instructions, tools
---

## Configure Agent with Name, Instructions, and Tools

**Impact: CRITICAL (foundation of all agent workflows)**

Every agent requires a `name` and should have clear `instructions`. Configure `model`, `tools`, and `model_settings` based on your use case.

**Incorrect (missing instructions, unclear purpose):**

```python
from agents import Agent

agent = Agent(name="agent")  # No instructions, unclear purpose
```

**Correct (clear configuration):**

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Weather Assistant",
    instructions="You help users check weather conditions. Always provide temperature and conditions.",
    model="gpt-4o",
    tools=[get_weather],
    model_settings=ModelSettings(temperature=0.7),
)
```

**Key properties:**

- `name`: Required string identifying the agent
- `instructions`: System prompt guiding agent behavior
- `model`: Which LLM to use (e.g., "gpt-4o", "gpt-4o-mini")
- `tools`: List of tools the agent can use
- `model_settings`: Temperature, top_p, tool_choice, etc.
- `mcp_servers`: MCP servers providing additional tools

Reference: [Agents Documentation](https://openai.github.io/openai-agents-python/agents/)
