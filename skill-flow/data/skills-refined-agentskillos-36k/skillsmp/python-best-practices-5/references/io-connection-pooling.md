---
title: Use Connection Pooling for Database and HTTP Clients
impact: CRITICAL
impactDescription: eliminates connection overhead, 50-200ms per request savings
tags: io, connection-pool, database, http-client
---

## Use Connection Pooling for Database and HTTP Clients

Creating a new connection for each request incurs TCP handshake, TLS negotiation, and authentication overhead. Connection pools reuse established connections.

**Incorrect (new connection per request):**

```python
async def get_user(user_id: int) -> User:
    conn = await asyncpg.connect(DATABASE_URL)  # 50-200ms overhead
    try:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**row)
    finally:
        await conn.close()
```

**Correct (reuse pooled connection):**

```python
# Create pool once at startup
pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)

async def get_user(user_id: int) -> User:
    async with pool.acquire() as conn:  # Near-instant connection
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**row)
```

**For HTTP clients (httpx):**

```python
# Reuse client with connection pooling
client = httpx.AsyncClient(limits=httpx.Limits(max_connections=100))

async def fetch_data(url: str) -> dict:
    response = await client.get(url)
    return response.json()
```

Reference: [asyncpg connection pooling](https://magicstack.github.io/asyncpg/current/api/index.html#connection-pools)
