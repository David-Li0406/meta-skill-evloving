---
title: Keep Context Type Consistent Across Agents and Tools
impact: HIGH
impactDescription: Prevents runtime type errors
tags: context, type-safety, consistency, typing
---

## Keep Context Type Consistent Across Agents and Tools

**Impact: HIGH (prevents runtime type errors)**

All agents, tools, and handlers in a single run must use the same context type. Mixing types causes runtime errors.

**Incorrect (mixed context types):**

```python
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, function_tool

@dataclass
class UserContext:
    user_id: str

@dataclass  
class AdminContext:
    admin_id: str
    permissions: list[str]

# Tool expects UserContext
@function_tool
def get_profile(ctx: RunContextWrapper[UserContext]) -> str:
    return f"Profile for {ctx.context.user_id}"

# Tool expects AdminContext - INCOMPATIBLE!
@function_tool
def admin_action(ctx: RunContextWrapper[AdminContext]) -> str:
    return f"Admin {ctx.context.admin_id} acted"

# This agent mixes incompatible tools - will cause runtime errors
agent = Agent(
    name="Mixed Agent",
    tools=[get_profile, admin_action],  # Different context types!
)
```

**Correct (unified context type):**

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

@dataclass
class AppContext:
    user_id: str
    is_admin: bool
    permissions: list[str]

@function_tool
def get_profile(ctx: RunContextWrapper[AppContext]) -> str:
    """Get user profile."""
    return f"Profile for {ctx.context.user_id}"

@function_tool
def admin_action(ctx: RunContextWrapper[AppContext]) -> str:
    """Perform admin action (requires admin privileges)."""
    if not ctx.context.is_admin:
        return "Error: Admin privileges required"
    return f"Admin action by {ctx.context.user_id}"

# All tools use the same context type
agent = Agent[AppContext](
    name="App Agent",
    tools=[get_profile, admin_action],
)

# All agents in handoff chain must also use AppContext
specialist = Agent[AppContext](
    name="Specialist",
    instructions="Handle specialized tasks",
)

triage = Agent[AppContext](
    name="Triage",
    handoffs=[specialist],
    tools=[get_profile],
)
```

**Type hints help catch errors:**

```python
# IDE/mypy will warn about type mismatches
agent = Agent[AppContext](...)  # Explicitly typed
```

Reference: [Context Documentation](https://openai.github.io/openai-agents-python/context/)
