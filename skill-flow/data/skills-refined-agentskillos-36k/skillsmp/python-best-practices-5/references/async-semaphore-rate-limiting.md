---
title: Use Semaphores for Concurrency Limiting
impact: CRITICAL
impactDescription: prevents resource exhaustion, controls connection limits
tags: async, semaphore, rate-limiting, concurrency-control
---

## Use Semaphores for Concurrency Limiting

Unbounded concurrency can exhaust resources (connections, file descriptors, memory). Use `asyncio.Semaphore` to limit concurrent operations.

**Incorrect (unbounded concurrency, may exhaust connections):**

```python
async def fetch_all_urls(urls: list[str]) -> list[Response]:
    return await asyncio.gather(
        *[fetch_url(url) for url in urls]
    )  # 10000 URLs = 10000 concurrent connections
```

**Correct (bounded concurrency with semaphore):**

```python
async def fetch_all_urls(urls: list[str], max_concurrent: int = 50) -> list[Response]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_limit(url: str) -> Response:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(
        *[fetch_with_limit(url) for url in urls]
    )  # Max 50 concurrent connections
```

**Alternative (bounded semaphore for stricter control):**

```python
# Raises ValueError if released more than acquired
semaphore = asyncio.BoundedSemaphore(max_concurrent)
```

Reference: [asyncio.Semaphore documentation](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore)
