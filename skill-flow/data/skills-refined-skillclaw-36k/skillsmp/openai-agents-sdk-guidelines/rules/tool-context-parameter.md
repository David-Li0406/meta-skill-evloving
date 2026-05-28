---
title: Access RunContextWrapper in Tools
impact: MEDIUM
impactDescription: Enables tools to access shared state and dependencies
tags: tool, context, dependency-injection, state
---

## Access RunContextWrapper in Tools

**Impact: MEDIUM (enables tools to access shared state and dependencies)**

Tools can receive the `RunContextWrapper` as their first parameter to access shared context, dependencies, and state.

**Incorrect (no access to context):**

```python
from agents import function_tool

@function_tool
def get_user_orders(user_id: str) -> str:
    """Get orders for a user."""
    # How do we know which user is making the request?
    # How do we access the database connection?
    return "orders"
```

**Correct (using RunContextWrapper):**

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

@dataclass
class AppContext:
    current_user_id: str
    db_connection: object
    logger: object

@function_tool
async def get_user_orders(ctx: RunContextWrapper[AppContext]) -> str:
    """Get orders for the current user.
    
    Fetches order history from the database for the authenticated user.
    """
    user_id = ctx.context.current_user_id
    db = ctx.context.db_connection
    ctx.context.logger.info(f"Fetching orders for {user_id}")
    
    # Use injected dependencies
    orders = await db.query(f"SELECT * FROM orders WHERE user_id = '{user_id}'")
    return str(orders)

agent = Agent[AppContext](
    name="Order Agent",
    tools=[get_user_orders],
)

# Pass context when running
context = AppContext(
    current_user_id="usr_123",
    db_connection=db,
    logger=logger,
)
result = await Runner.run(agent, "Show my orders", context=context)
```

**Context must be first parameter:**

```python
@function_tool
def tool_with_context(
    ctx: RunContextWrapper[AppContext],  # Must be first
    query: str,                           # Other params follow
    limit: int = 10,
) -> str:
    """Tool that uses context and has other parameters."""
    return f"Results for {ctx.context.current_user_id}: {query}"
```

Reference: [Context Documentation](https://openai.github.io/openai-agents-python/context/)
