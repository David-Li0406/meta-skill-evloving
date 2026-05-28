---
title: Choose the Right Concurrency Model
impact: MEDIUM
impactDescription: 2-8× improvement with correct model selection
tags: conc, asyncio, threading, multiprocessing, gil
---

## Choose the Right Concurrency Model

Python offers three concurrency models, each suited for different workloads. Choosing wrong limits scalability or adds unnecessary overhead.

**Decision guide:**

```python
# I/O-bound: asyncio (best) or threading
# CPU-bound: multiprocessing (bypasses GIL)
# Mixed: hybrid approach

# I/O-bound examples: web requests, database queries, file I/O
# CPU-bound examples: image processing, data compression, ML inference
```

**Incorrect (threading for CPU-bound work):**

```python
from concurrent.futures import ThreadPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ThreadPoolExecutor(max_workers=8) as executor:
        return list(executor.map(resize_image, images))
    # GIL prevents true parallelism - limited to 1 CPU core
```

**Correct (multiprocessing for CPU-bound work):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ProcessPoolExecutor(max_workers=8) as executor:
        return list(executor.map(resize_image, images))
    # Each process has its own GIL - true parallelism
```

**Correct (asyncio for I/O-bound work):**

```python
async def fetch_all_pages(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[session.get(url) for url in urls]
        )
    # Single thread handles thousands of concurrent connections
```

Reference: [Concurrency in Python](https://docs.python.org/3/library/concurrency.html)
