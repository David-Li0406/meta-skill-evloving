---
title: Never Use KEYS Command in Production
impact: CRITICAL
impactDescription: KEYS blocks entire Redis server, causes outages
tags: commands, performance, production, scan
---

## Never Use KEYS Command in Production

The KEYS command scans the entire keyspace in a single blocking operation. With millions of keys, it can freeze Redis for seconds or minutes, causing cascading failures. Always use SCAN for pattern matching in production.

**See also:** [key-use-scan-not-keys](./key-use-scan-not-keys.md) for detailed SCAN patterns.

**Why KEYS is Dangerous:**
- O(n) complexity where n = ALL keys in database
- Single-threaded blocking operation
- 1M keys ≈ 1 second block
- 100M keys ≈ minutes of blocking
- Affects ALL clients, not just the caller

**Incorrect:**

```python
import redis
r = redis.Redis()

# NEVER DO THIS IN PRODUCTION
keys = r.keys("user:*")  # Blocks entire Redis!
keys = r.keys("cache:*")  # Disaster waiting to happen
keys = r.keys("*")  # Worst case - scans everything
```

**Correct:**

```python
import redis
r = redis.Redis()

# Use SCAN iterator
for key in r.scan_iter(match="user:*", count=100):
    process(key)

# Or collect into list
keys = list(r.scan_iter(match="user:*", count=100))
```

Reference: [Redis SCAN vs KEYS](https://redis.io/commands/scan/)
