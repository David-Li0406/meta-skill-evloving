---
title: Use Dynamic Instructions for Context-Aware Prompts
impact: HIGH
impactDescription: Enables personalized agent behavior
tags: agent, instructions, dynamic, context
---

## Use Dynamic Instructions for Context-Aware Prompts

**Impact: HIGH (enables personalized agent behavior)**

When instructions need to vary based on context (user info, time, etc.), use a function instead of a static string.

**Incorrect (hardcoded instructions):**

```python
from agents import Agent

agent = Agent(
    name="Assistant",
    instructions="Help the user with their questions.",  # Generic, no personalization
)
```

**Correct (dynamic instructions):**

```python
from agents import Agent, RunContextWrapper
from dataclasses import dataclass

@dataclass
class UserContext:
    name: str
    is_premium: bool

def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    user = context.context
    premium_note = " You can offer advanced features." if user.is_premium else ""
    return f"The user's name is {user.name}. Help them with their questions.{premium_note}"

agent = Agent[UserContext](
    name="Assistant",
    instructions=dynamic_instructions,
)
```

**Both sync and async functions work:**

```python
async def async_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    # Can do async operations like fetching user preferences
    prefs = await fetch_user_preferences(context.context.uid)
    return f"User prefers {prefs.language}. Help them accordingly."
```

Reference: [Agents Documentation - Dynamic Instructions](https://openai.github.io/openai-agents-python/agents/#dynamic-instructions)
