---
title: Minimize Lock Contention in Threaded Code
impact: MEDIUM
impactDescription: reduces serialization, improves parallel throughput
tags: conc, threading, locks, contention
---

## Minimize Lock Contention in Threaded Code

Long-held locks serialize execution, negating concurrency benefits. Keep critical sections minimal and consider lock-free alternatives.

**Incorrect (lock held during I/O):**

```python
import threading

cache_lock = threading.Lock()
cache: dict[str, Data] = {}

def get_data(key: str) -> Data:
    with cache_lock:  # Lock held during slow I/O
        if key not in cache:
            cache[key] = fetch_from_database(key)  # Blocks all threads
        return cache[key]
```

**Correct (minimize critical section):**

```python
import threading

cache_lock = threading.Lock()
cache: dict[str, Data] = {}

def get_data(key: str) -> Data:
    # Check without lock first
    with cache_lock:
        if key in cache:
            return cache[key]

    # Fetch outside lock (may have duplicate fetches, but no blocking)
    data = fetch_from_database(key)

    with cache_lock:
        cache.setdefault(key, data)  # Only insert if still missing
        return cache[key]
```

**Alternative (RLock for reentrant access):**

```python
# Use RLock when same thread may need to acquire lock multiple times
cache_lock = threading.RLock()
```

Reference: [threading.Lock documentation](https://docs.python.org/3/library/threading.html#lock-objects)
