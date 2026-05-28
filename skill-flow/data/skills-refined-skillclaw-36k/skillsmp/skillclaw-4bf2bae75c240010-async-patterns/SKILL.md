---
name: async-patterns
description: Use this skill when implementing asynchronous programming patterns in Python, JavaScript/TypeScript, or other languages, particularly for concurrent code, handling promises, or optimizing I/O operations.
---

# Async Programming Patterns

## Core Concepts

### Event Loop
- Single-threaded execution model
- Non-blocking I/O operations
- Cooperative multitasking via yield points

### When to Use Async
- I/O-bound operations (network, disk, database)
- High concurrency requirements
- Real-time applications (WebSockets)

### When NOT to Use Async
- CPU-bound computation (use multiprocessing)
- Simple sequential scripts
- When overhead outweighs benefit

## Python Async Patterns

### Basic Pattern
```python
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Run concurrent requests
async def main():
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[fetch_data(u) for u in urls])
```

### Producer-Consumer Queue
```python
async def producer(queue: asyncio.Queue):
    for item in items:
        await queue.put(item)
    await queue.put(None)  # Sentinel

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        await process(item)
        queue.task_done()
```

### Rate Limiting with Semaphore
```python
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def rate_limited_request(url):
    async with semaphore:
        return await fetch(url)
```

### Timeout Handling
```python
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)
except asyncio.TimeoutError:
    handle_timeout()
```

## JavaScript/TypeScript Patterns

### Promise Patterns
```typescript
// Parallel execution
const results = await Promise.all([fetch1(), fetch2(), fetch3()]);

// First to complete
const fastest = await Promise.race([fetch1(), fetch2()]);

// All settled (includes failures)
const outcomes = await Promise.allSettled([fetch1(), fetch2()]);
```

### Async Iterator
```typescript
async function* paginate(url: string) {
  let cursor: string | null = null;
  do {
    const { data, nextCursor } = await fetchPage(url, cursor);
    yield* data;
    cursor = nextCursor;
  } while (cursor);
}

for await (const item of paginate('/api/items')) {
  process(item);
}
```

### Error Handling
```typescript
try {
    const result = await fetchData();
} catch (error) {
    console.error('Error fetching data:', error);
}
```