---
title: Implement TTL for Time-Sensitive Caches
impact: LOW-MEDIUM
impactDescription: prevents stale data, controls memory growth
tags: cache, ttl, expiration, cachetools
---

## Implement TTL for Time-Sensitive Caches

`lru_cache` has no expiration. For time-sensitive data, use `cachetools.TTLCache` or implement manual expiration to prevent stale results.

**Incorrect (stale data indefinitely):**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_exchange_rate(currency: str) -> float:
    return fetch_current_rate(currency)
    # Returns stale rate until cache_clear() is called
```

**Correct (TTL-based expiration):**

```python
from cachetools import TTLCache
from cachetools.keys import hashkey

exchange_cache: TTLCache[str, float] = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL

def get_exchange_rate(currency: str) -> float:
    if currency not in exchange_cache:
        exchange_cache[currency] = fetch_current_rate(currency)
    return exchange_cache[currency]
```

**Alternative (decorator with TTL):**

```python
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=1000, ttl=300))
def get_exchange_rate(currency: str) -> float:
    return fetch_current_rate(currency)
```

Reference: [cachetools documentation](https://cachetools.readthedocs.io/)
