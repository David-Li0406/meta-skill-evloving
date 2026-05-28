---
title: Use Chunking for ProcessPoolExecutor
impact: MEDIUM
impactDescription: reduces IPC overhead by 10-100×
tags: conc, multiprocessing, chunking, ipc
---

## Use Chunking for ProcessPoolExecutor

Each task submitted to ProcessPoolExecutor incurs inter-process communication (IPC) overhead. Batch small tasks into chunks to amortize this cost.

**Incorrect (IPC overhead per item):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_pixels(pixels: list[Pixel]) -> list[Color]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(transform_pixel, pixels))
    # 1M pixels = 1M IPC round trips
```

**Correct (chunked processing):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_chunk(chunk: list[Pixel]) -> list[Color]:
    return [transform_pixel(pixel) for pixel in chunk]

def process_pixels(pixels: list[Pixel], chunk_size: int = 1000) -> list[Color]:
    chunks = [pixels[i:i + chunk_size] for i in range(0, len(pixels), chunk_size)]

    with ProcessPoolExecutor() as executor:
        results = executor.map(process_chunk, chunks)

    return [color for chunk_result in results for color in chunk_result]
    # 1M pixels = 1K IPC round trips
```

**Alternative (use chunksize parameter):**

```python
with ProcessPoolExecutor() as executor:
    results = list(executor.map(transform_pixel, pixels, chunksize=1000))
```

Reference: [ProcessPoolExecutor documentation](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor)
