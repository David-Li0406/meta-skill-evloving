---
title: Use RunContextWrapper for Dependencies and State
impact: MEDIUM
impactDescription: Clean dependency injection for agents and tools
tags: context, dependency-injection, state, RunContextWrapper
---

## Use RunContextWrapper for Dependencies and State

**Impact: MEDIUM (clean dependency injection for agents and tools)**

Use a context object to pass dependencies (database, logger, config) and state (user info, session data) to agents and tools.

**Incorrect (global state or no dependency injection):**

```python
from agents import Agent, function_tool

# Global state - bad for testing, concurrency issues
current_user = None
db_connection = None

@function_tool
def get_orders() -> str:
    """Get user orders."""
    global current_user, db_connection
    return str(db_connection.query(f"SELECT * FROM orders WHERE user={current_user}"))
```

**Correct (using context):**

```python
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

@dataclass
class AppContext:
    user_id: str
    db: object
    logger: object
    feature_flags: dict

@function_tool
async def get_orders(ctx: RunContextWrapper[AppContext]) -> str:
    """Get orders for the current user."""
    ctx.context.logger.info(f"Fetching orders for {ctx.context.user_id}")
    orders = await ctx.context.db.query_orders(ctx.context.user_id)
    return str(orders)

@function_tool
def check_feature(ctx: RunContextWrapper[AppContext], feature: str) -> bool:
    """Check if a feature is enabled."""
    return ctx.context.feature_flags.get(feature, False)

agent = Agent[AppContext](
    name="Order Agent",
    instructions="Help users with their orders.",
    tools=[get_orders, check_feature],
)

# Create and pass context
context = AppContext(
    user_id="usr_123",
    db=database_connection,
    logger=app_logger,
    feature_flags={"new_ui": True},
)

result = await Runner.run(agent, "Show my orders", context=context)
```

**Key points:**

- Context is **not** sent to the LLM - it's local only
- Same context type must be used across all agents/tools in a run
- Use `Agent[ContextType]` for type checking

Reference: [Context Documentation](https://openai.github.io/openai-agents-python/context/)
