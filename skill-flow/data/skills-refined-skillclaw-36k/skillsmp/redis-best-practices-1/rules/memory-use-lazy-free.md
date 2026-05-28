---
title: Enable Lazy Freeing for Large Deletions
impact: MEDIUM
impactDescription: prevents blocking during large key deletions
tags: memory, lazy-free, unlink, performance
---

## Enable Lazy Freeing for Large Deletions

Use `UNLINK` instead of `DEL` for large keys, and enable lazy freeing options. Deleting large keys (millions of elements) blocks Redis for seconds. Lazy freeing moves memory reclamation to background threads.

**Commands:**
- `DEL`: Synchronous delete (blocks Redis)
- `UNLINK`: Asynchronous delete (returns immediately, memory freed in background)

**Lazy Freeing Options:**
- `lazyfree-lazy-eviction`: Async eviction when maxmemory reached
- `lazyfree-lazy-expire`: Async deletion of expired keys
- `lazyfree-lazy-server-del`: Async for implicit deletions (RENAME, etc.)
- `lazyfree-lazy-user-del`: Make DEL behave like UNLINK
- `lazyfree-lazy-user-flush`: Async FLUSHALL/FLUSHDB

**Incorrect (blocking deletions):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: DEL on large key
r.delete("huge_set")  # Blocks Redis if set has millions of members!

# Anti-pattern 2: Mass deletion blocking
def clear_cache_bad():
    for key in r.scan_iter(match="cache:*"):
        r.delete(key)  # Each delete might block

# Anti-pattern 3: FLUSHDB without ASYNC
r.flushdb()  # Blocks entire database clear

# Anti-pattern 4: RENAME that deletes large key
r.rename("new_data", "old_large_data")  # Implicitly deletes old_large_data, blocks!
```

**Correct (non-blocking deletions):**

```python
import redis
r = redis.Redis()

# Correct 1: Use UNLINK for potentially large keys
def delete_key_safe(key):
    """Delete key without blocking Redis"""
    r.unlink(key)  # Returns immediately, memory freed in background

# Correct 2: Use UNLINK for batch deletions
def clear_cache_safe(pattern="cache:*", batch_size=1000):
    """Delete keys matching pattern without blocking"""
    pipe = r.pipeline()
    count = 0

    for key in r.scan_iter(match=pattern, count=100):
        pipe.unlink(key)  # Use UNLINK, not DELETE
        count += 1

        if count % batch_size == 0:
            pipe.execute()
            pipe = r.pipeline()

    if count % batch_size != 0:
        pipe.execute()

    return count

# Correct 3: Async flush
def flush_database_safe():
    """Flush database without blocking"""
    r.flushdb(asynchronous=True)  # Non-blocking flush

def flush_all_safe():
    """Flush all databases without blocking"""
    r.flushall(asynchronous=True)

# Correct 4: Check key size before choosing delete method
def smart_delete(key, size_threshold=10000):
    """Use UNLINK for large keys, DEL for small ones"""
    key_type = r.type(key).decode()

    # Estimate size based on type
    if key_type == "string":
        size = r.strlen(key)
    elif key_type == "list":
        size = r.llen(key)
    elif key_type == "set":
        size = r.scard(key)
    elif key_type == "zset":
        size = r.zcard(key)
    elif key_type == "hash":
        size = r.hlen(key)
    else:
        size = 0

    if size > size_threshold:
        r.unlink(key)  # Async for large keys
    else:
        r.delete(key)  # Sync is fine for small keys
```

```bash
# Enable lazy freeing in redis.conf
# redis.conf

# Async eviction when maxmemory is reached
lazyfree-lazy-eviction yes

# Async deletion of expired keys
lazyfree-lazy-expire yes

# Async for implicit deletions (RENAME overwriting, etc.)
lazyfree-lazy-server-del yes

# Make DEL behave like UNLINK (Redis 6.0+)
lazyfree-lazy-user-del yes

# Async FLUSHALL and FLUSHDB
lazyfree-lazy-user-flush yes

# Number of threads for lazy freeing (Redis 6.0+)
# Default is 1, increase for heavy deletion workloads
io-threads 4
io-threads-do-reads yes
```

```python
# Correct 5: Configure lazy freeing at runtime
def configure_lazy_free():
    """Enable lazy freeing options"""
    configs = [
        ("lazyfree-lazy-eviction", "yes"),
        ("lazyfree-lazy-expire", "yes"),
        ("lazyfree-lazy-server-del", "yes"),
        ("lazyfree-lazy-user-del", "yes"),
        ("lazyfree-lazy-user-flush", "yes"),
    ]

    for key, value in configs:
        try:
            r.config_set(key, value)
            print(f"Set {key} = {value}")
        except redis.ResponseError as e:
            print(f"Could not set {key}: {e}")

def check_lazy_free_config():
    """Check current lazy free settings"""
    settings = {}
    for key in [
        "lazyfree-lazy-eviction",
        "lazyfree-lazy-expire",
        "lazyfree-lazy-server-del",
        "lazyfree-lazy-user-del",
        "lazyfree-lazy-user-flush",
    ]:
        try:
            value = r.config_get(key)
            settings[key] = value.get(key, "unknown")
        except:
            settings[key] = "not supported"

    return settings
```

```python
# Correct 6: Handle large data structure cleanup
def cleanup_large_sorted_set(key, keep_count=1000):
    """
    Trim sorted set to keep only top N elements.
    Uses ZREMRANGEBYRANK which can be slow for large sets.
    Consider chunked approach for very large sets.
    """
    current_size = r.zcard(key)

    if current_size <= keep_count:
        return 0

    # Remove elements beyond keep_count (from the bottom)
    # ZREMRANGEBYRANK removes by index, 0 is lowest score
    removed = r.zremrangebyrank(key, 0, -(keep_count + 1))
    return removed

def cleanup_large_list(key, max_length=10000):
    """Keep only the most recent max_length items in a list"""
    r.ltrim(key, 0, max_length - 1)

def expire_instead_of_delete(key, expire_seconds=1):
    """
    Alternative to immediate delete: set short TTL.
    Key will be deleted asynchronously by Redis expiry mechanism.
    """
    r.expire(key, expire_seconds)
```

```javascript
// Node.js
const Redis = require('ioredis');
const redis = new Redis();

// Use UNLINK for large keys
async function deleteKeySafe(key) {
    await redis.unlink(key);
}

// Batch delete with UNLINK
async function clearCacheSafe(pattern) {
    const stream = redis.scanStream({ match: pattern, count: 100 });
    const pipeline = redis.pipeline();
    let count = 0;

    for await (const keys of stream) {
        for (const key of keys) {
            pipeline.unlink(key);
            count++;

            if (count % 1000 === 0) {
                await pipeline.exec();
                pipeline = redis.pipeline();
            }
        }
    }

    await pipeline.exec();
    return count;
}

// Async flush
await redis.flushdb('ASYNC');
```

Reference: [Redis Lazy Freeing](https://redis.io/docs/management/optimization/memory-optimization/#lazy-freeing)
