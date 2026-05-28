# Async Patterns in Python

Guide to asyncio and async/await in Python.

## Basic Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    # Simulated async operation
    await asyncio.sleep(1)
    return {"url": url, "data": "..."}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

## Running Multiple Tasks

```python
async def main():
    # Concurrent execution
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    
    # With timeout
    try:
        result = await asyncio.wait_for(fetch_data("url"), timeout=5.0)
    except asyncio.TimeoutError:
        print("Timeout!")
```

## Async Context Managers

```python
class DatabaseConnection:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

async with DatabaseConnection() as db:
    await db.query("SELECT * FROM users")
```

## Async Generators

```python
async def fetch_pages(url: str):
    page = 1
    while page <= 10:
        await asyncio.sleep(0.5)
        yield f"Page {page} from {url}"
        page += 1

async for page in fetch_pages("example.com"):
    print(page)
```

## Common Patterns

### Producer-Consumer

```python
async def producer(queue: asyncio.Queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(0.1)

async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        print(f"Processing {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue),
    )
```

### Semaphore (Rate Limiting)

```python
sem = asyncio.Semaphore(5)  # Max 5 concurrent

async def limited_task(n: int):
    async with sem:
        await asyncio.sleep(1)
        return n

tasks = [limited_task(i) for i in range(100)]
results = await asyncio.gather(*tasks)
```

## Best Practices

1. Use `asyncio.run()` for the entry point
2. Prefer `asyncio.gather()` over manual task management
3. Use async context managers for resources
4. Add timeouts to prevent hanging
5. Use semaphores for rate limiting
6. Avoid `asyncio.create_task()` unless necessary
