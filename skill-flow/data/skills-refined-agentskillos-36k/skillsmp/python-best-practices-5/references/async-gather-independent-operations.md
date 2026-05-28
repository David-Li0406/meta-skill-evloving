---
title: Use asyncio.gather() for Independent Operations
impact: CRITICAL
impactDescription: 2-10× improvement, N round trips to 1
tags: async, gather, parallelization, waterfalls
---

## Use asyncio.gather() for Independent Operations

When async operations have no interdependencies, execute them concurrently using `asyncio.gather()`. Sequential awaits serialize operations that could run in parallel.

**Incorrect (sequential execution, 3 round trips):**

```python
async def fetch_dashboard_data(user_id: int) -> DashboardData:
    user = await fetch_user(user_id)
    orders = await fetch_orders(user_id)
    notifications = await fetch_notifications(user_id)
    # Total time: user + orders + notifications
    return DashboardData(user, orders, notifications)
```

**Correct (parallel execution, 1 round trip):**

```python
async def fetch_dashboard_data(user_id: int) -> DashboardData:
    user, orders, notifications = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id),
        fetch_notifications(user_id),
    )
    # Total time: max(user, orders, notifications)
    return DashboardData(user, orders, notifications)
```

**Alternative (with error handling):**

```python
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    return_exceptions=True,  # Don't fail fast, collect all results
)
```

Reference: [asyncio.gather documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
