---
title: Use Async File I/O for Non-Blocking Operations
impact: CRITICAL
impactDescription: eliminates blocking waits, 80% latency reduction
tags: io, async, aiofiles, file-operations
---

## Use Async File I/O for Non-Blocking Operations

Synchronous file operations block the event loop, preventing other coroutines from running. Use `aiofiles` or similar libraries for async file I/O to maintain concurrency.

**Incorrect (blocks event loop during file read):**

```python
async def process_config():
    with open("config.json", "r") as f:
        data = f.read()  # Blocks entire event loop
    return json.loads(data)
```

**Correct (non-blocking file read):**

```python
import aiofiles

async def process_config():
    async with aiofiles.open("config.json", "r") as f:
        data = await f.read()  # Other coroutines can run
    return json.loads(data)
```

**When NOT to use this pattern:**
- Small config files read once at startup (blocking is acceptable)
- Performance-critical paths where `aiofiles` overhead matters (use sync I/O in executor)

Reference: [aiofiles documentation](https://github.com/Tinche/aiofiles)
