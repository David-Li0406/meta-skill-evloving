---
title: Expose Agents as Callable Tools
impact: HIGH
impactDescription: Enables manager pattern for multi-agent orchestration
tags: tool, agents-as-tools, orchestration, multi-agent
---

## Expose Agents as Callable Tools

**Impact: HIGH (enables manager pattern for multi-agent orchestration)**

Use `agent.as_tool()` to expose an agent as a tool for another agent, enabling centralized orchestration.

**Basic usage:**

```python
from agents import Agent, Runner

spanish_agent = Agent(
    name="Spanish Translator",
    instructions="Translate the input to Spanish.",
)

french_agent = Agent(
    name="French Translator",
    instructions="Translate the input to French.",
)

orchestrator = Agent(
    name="Translation Manager",
    instructions="Translate user requests to the requested language(s).",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_spanish",
            tool_description="Translate text to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_french",
            tool_description="Translate text to French",
        ),
    ],
)

result = await Runner.run(orchestrator, "Say 'Hello' in Spanish and French")
```

**Custom output extraction:**

```python
from agents import Agent, RunResult

async def extract_json(run_result: RunResult) -> str:
    """Extract only JSON from the sub-agent's output."""
    output = str(run_result.final_output)
    # Custom extraction logic
    return output

data_agent = Agent(name="Data Agent", instructions="Return data as JSON")

tool = data_agent.as_tool(
    tool_name="get_data",
    tool_description="Get structured data",
    custom_output_extractor=extract_json,
)
```

**Conditional tool enabling:**

```python
from agents import Agent, RunContextWrapper, AgentBase

def is_premium_user(ctx: RunContextWrapper, agent: AgentBase) -> bool:
    return ctx.context.is_premium

premium_agent = Agent(name="Premium Agent", instructions="Premium features")

orchestrator = Agent(
    name="Main Agent",
    tools=[
        premium_agent.as_tool(
            tool_name="premium_features",
            tool_description="Access premium features",
            is_enabled=is_premium_user,  # Only available for premium users
        ),
    ],
)
```

Reference: [Tools Documentation - Agents as Tools](https://openai.github.io/openai-agents-python/tools/#agents-as-tools)
