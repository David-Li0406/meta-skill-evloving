---
title: Use lru_cache for Expensive Pure Functions
impact: LOW-MEDIUM
impactDescription: eliminates redundant computation, O(1) cached lookups
tags: cache, lru-cache, memoization, functools
---

## Use lru_cache for Expensive Pure Functions

`functools.lru_cache` memoizes function results, eliminating redundant computation for repeated calls with the same arguments.

**Incorrect (recomputes every call):**

```python
def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
    # fib(40) = 2^40 recursive calls
```

**Correct (memoized, linear complexity):**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
    # fib(40) = 40 unique calls
```

**Cache management:**

```python
@lru_cache(maxsize=1000)
def fetch_user_permissions(user_id: int) -> set[str]:
    return set(db.get_permissions(user_id))

# Check cache statistics
print(fetch_user_permissions.cache_info())

# Clear cache when data changes
fetch_user_permissions.cache_clear()
```

**Requirements for caching:**
- Function must be pure (same inputs → same outputs)
- Arguments must be hashable (no lists, dicts)

Reference: [functools.lru_cache documentation](https://docs.python.org/3/library/functools.html#functools.lru_cache)
