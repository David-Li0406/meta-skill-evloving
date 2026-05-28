---
title: Avoid Async Overhead for CPU-Bound Work
impact: CRITICAL
impactDescription: 2-8× improvement using multiprocessing for CPU-bound work
tags: async, cpu-bound, overhead, multiprocessing
---

## Avoid Async Overhead for CPU-Bound Work

Async/await adds overhead (~2-5μs per await) for coroutine scheduling. For CPU-bound work, this overhead provides no benefit since the GIL prevents true parallelism. Use multiprocessing instead.

**Incorrect (async overhead with no concurrency benefit):**

```python
async def process_images(images: list[Image]) -> list[Thumbnail]:
    results = []
    for image in images:
        thumbnail = await asyncio.to_thread(resize_image, image)
        results.append(thumbnail)  # Still sequential due to GIL
    return results
```

**Correct (true parallelism with ProcessPoolExecutor):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(resize_image, images))
```

**Alternative (hybrid approach for mixed workloads):**

```python
async def process_mixed_workload(
    images: list[Image],
    urls: list[str],
) -> tuple[list[Thumbnail], list[Response]]:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        # CPU-bound in process pool
        thumbnails = loop.run_in_executor(
            executor, lambda: list(map(resize_image, images))
        )
        # I/O-bound with asyncio
        responses = asyncio.gather(*[fetch_url(url) for url in urls])

        return await asyncio.gather(thumbnails, responses)
```

Reference: [Concurrency in Python](https://docs.python.org/3/library/asyncio-dev.html#concurrency-and-multithreading)
