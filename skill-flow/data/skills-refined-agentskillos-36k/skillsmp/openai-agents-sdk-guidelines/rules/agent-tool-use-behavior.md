---
title: Control Tool Output Processing with tool_use_behavior
impact: MEDIUM
impactDescription: Optimizes tool result handling
tags: agent, tools, behavior, optimization
---

## Control Tool Output Processing with tool_use_behavior

**Impact: MEDIUM (optimizes tool result handling)**

Use `tool_use_behavior` to control whether tool outputs are processed by the LLM or returned directly.

**Default behavior (run_llm_again):**

```python
from agents import Agent, function_tool

@function_tool
def get_stock_price(symbol: str) -> str:
    """Returns the current stock price."""
    return f"${symbol}: $150.25"

agent = Agent(
    name="Stock Agent",
    instructions="Get stock prices for the user.",
    tools=[get_stock_price],
    tool_use_behavior="run_llm_again",  # Default: LLM processes tool output
)
```

**Stop on first tool (bypass LLM post-processing):**

```python
from agents import Agent, function_tool

@function_tool
def get_raw_data(query: str) -> str:
    """Returns raw data that doesn't need LLM processing."""
    return '{"status": "success", "data": [1, 2, 3]}'

agent = Agent(
    name="Data Agent",
    tools=[get_raw_data],
    tool_use_behavior="stop_on_first_tool",  # Tool output is final
)
```

**Stop at specific tools:**

```python
from agents import Agent, function_tool
from agents.agent import StopAtTools

@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny"

@function_tool
def sum_numbers(a: int, b: int) -> int:
    return a + b

agent = Agent(
    name="Mixed Agent",
    tools=[get_weather, sum_numbers],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"]),
)
```

Reference: [Agents Documentation - Tool Use Behavior](https://openai.github.io/openai-agents-python/agents/#tool-use-behavior)
