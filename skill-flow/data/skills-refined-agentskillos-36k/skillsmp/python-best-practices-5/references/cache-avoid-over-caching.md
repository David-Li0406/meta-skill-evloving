---
title: Avoid Over-Caching Low-Value Operations
impact: LOW-MEDIUM
impactDescription: cache overhead may exceed computation cost
tags: cache, optimization, profiling, overhead
---

## Avoid Over-Caching Low-Value Operations

Caching adds overhead: hash computation, dictionary lookups, memory usage. Only cache operations where computation cost significantly exceeds cache overhead.

**Incorrect (caching trivial operations):**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def double(x: int) -> int:
    return x * 2
    # Hash + lookup overhead exceeds multiplication cost

@lru_cache(maxsize=1000)
def format_name(first: str, last: str) -> str:
    return f"{first} {last}"
    # String formatting is fast, caching adds overhead
```

**Correct (cache expensive operations only):**

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def parse_config(config_path: str) -> Config:
    # File I/O + parsing is expensive
    with open(config_path) as f:
        return parse_yaml(f.read())

@lru_cache(maxsize=1000)
def compile_regex(pattern: str) -> re.Pattern:
    # Regex compilation is expensive
    return re.compile(pattern)
```

**Profile before caching:**

```python
import cProfile

# Profile to identify actual bottlenecks
cProfile.run("process_data(large_dataset)")
# Only cache functions that appear in profiler output
```

Reference: [Python profiling documentation](https://docs.python.org/3/library/profile.html)
