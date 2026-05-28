---
title: Use asyncio.Queue for Producer-Consumer Patterns
impact: MEDIUM
impactDescription: enables backpressure and controlled concurrency
tags: conc, asyncio, queue, producer-consumer
---

## Use asyncio.Queue for Producer-Consumer Patterns

`asyncio.Queue` provides async-safe producer-consumer coordination with backpressure support, preventing memory exhaustion from fast producers.

**Incorrect (unbounded list accumulation):**

```python
async def process_stream(stream: AsyncIterator[Event]) -> None:
    events = []
    async for event in stream:
        events.append(event)  # Memory grows unbounded

    for event in events:
        await process_event(event)
```

**Correct (bounded queue with backpressure):**

```python
async def process_stream(stream: AsyncIterator[Event]) -> None:
    queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=100)

    async def producer():
        async for event in stream:
            await queue.put(event)  # Blocks when queue full
        await queue.put(None)  # Sentinel to signal completion

    async def consumer():
        while (event := await queue.get()) is not None:
            await process_event(event)
            queue.task_done()

    await asyncio.gather(producer(), consumer())
```

**Multiple consumers:**

```python
async def run_workers(queue: asyncio.Queue, num_workers: int = 5):
    async def worker():
        while True:
            task = await queue.get()
            await process_task(task)
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]
    await queue.join()  # Wait for all tasks to complete
```

Reference: [asyncio.Queue documentation](https://docs.python.org/3/library/asyncio-queue.html)
