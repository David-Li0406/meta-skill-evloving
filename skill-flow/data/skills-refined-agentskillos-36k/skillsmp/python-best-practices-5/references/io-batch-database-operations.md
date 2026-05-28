---
title: Batch Database Operations to Reduce Round Trips
impact: CRITICAL
impactDescription: N round trips to 1, 10-100× improvement for bulk operations
tags: io, database, batching, bulk-operations
---

## Batch Database Operations to Reduce Round Trips

Each database query incurs network latency. Batching multiple operations into a single query eliminates N-1 round trips and reduces connection overhead.

**Incorrect (N database round trips):**

```python
async def update_user_statuses(user_ids: list[int], status: str):
    for user_id in user_ids:
        await db.execute(
            "UPDATE users SET status = $1 WHERE id = $2",
            status, user_id
        )  # 1000 users = 1000 round trips
```

**Correct (1 database round trip):**

```python
async def update_user_statuses(user_ids: list[int], status: str):
    await db.execute(
        "UPDATE users SET status = $1 WHERE id = ANY($2)",
        status, user_ids
    )  # 1000 users = 1 round trip
```

**Alternative (bulk insert with executemany):**

```python
async def insert_orders(orders: list[Order]):
    await db.executemany(
        "INSERT INTO orders (user_id, total) VALUES ($1, $2)",
        [(o.user_id, o.total) for o in orders]
    )
```

Reference: [asyncpg documentation](https://magicstack.github.io/asyncpg/current/)
