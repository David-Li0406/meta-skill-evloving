---
title: Make Data Available to LLMs via Instructions or Tools
impact: MEDIUM
impactDescription: Context object is not visible to LLM
tags: context, llm, visibility, instructions, tools
---

## Make Data Available to LLMs via Instructions or Tools

**Impact: MEDIUM (context object is not visible to LLM)**

The `RunContextWrapper.context` object is **not** sent to the LLM. To make data visible to the LLM, use instructions, input, or tools.

**Incorrect (expecting LLM to see context):**

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper

@dataclass
class UserContext:
    name: str
    preferred_language: str

agent = Agent[UserContext](
    name="Assistant",
    instructions="Help the user.",  # LLM doesn't know user's name!
)

context = UserContext(name="Alice", preferred_language="Spanish")
# LLM cannot see context.name or context.preferred_language
result = await Runner.run(agent, "Hello", context=context)
```

**Correct (exposing via dynamic instructions):**

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper

@dataclass
class UserContext:
    name: str
    preferred_language: str

def personalized_instructions(
    ctx: RunContextWrapper[UserContext], 
    agent: Agent
) -> str:
    return f"""Help the user named {ctx.context.name}.
    They prefer responses in {ctx.context.preferred_language}."""

agent = Agent[UserContext](
    name="Assistant",
    instructions=personalized_instructions,
)

context = UserContext(name="Alice", preferred_language="Spanish")
result = await Runner.run(agent, "Hello", context=context)
# LLM now knows user's name and language preference
```

**Correct (exposing via tools for on-demand access):**

```python
from agents import Agent, RunContextWrapper, function_tool

@function_tool
def get_user_preferences(ctx: RunContextWrapper[UserContext]) -> str:
    """Get the current user's preferences."""
    return f"Name: {ctx.context.name}, Language: {ctx.context.preferred_language}"

agent = Agent[UserContext](
    name="Assistant",
    instructions="Help the user. Use get_user_preferences when you need their info.",
    tools=[get_user_preferences],
)
```

**Methods to expose data to LLM:**

1. **Instructions**: Good for always-relevant info (user name, date)
2. **Input**: Good for request-specific context
3. **Tools**: Good for on-demand data (fetched when needed)
4. **Retrieval/Web Search**: Good for grounding in external data

Reference: [Context Documentation - Agent/LLM Context](https://openai.github.io/openai-agents-python/context/#agentllm-context)
