---
title: Choose Appropriate Eviction Policy
impact: CRITICAL
impactDescription: wrong policy causes data loss or OOM errors
tags: memory, eviction, maxmemory-policy, cache
---

## Choose Appropriate Eviction Policy

Configure the right `maxmemory-policy` for your use case. The eviction policy determines which keys Redis removes when memory limit is reached. Wrong policy can cause important data loss or OOM errors blocking writes.

**Available Policies:**
| Policy | Behavior | Use Case |
|--------|----------|----------|
| `noeviction` | Return error on writes | When data loss is unacceptable |
| `allkeys-lru` | Evict least recently used | General caching |
| `allkeys-lfu` | Evict least frequently used | Caching with popularity |
| `volatile-lru` | LRU among keys with TTL | Mixed cache + persistent data |
| `volatile-lfu` | LFU among keys with TTL | Mixed with popularity |
| `allkeys-random` | Random eviction | When all keys equal priority |
| `volatile-random` | Random among keys with TTL | Mixed, no preference |
| `volatile-ttl` | Evict shortest TTL first | When TTL indicates priority |

**Incorrect (wrong policy for use case):**

```bash
# Anti-pattern 1: noeviction for cache
# redis.conf
maxmemory 2gb
maxmemory-policy noeviction  # Writes fail when full!
# Result: Application errors when cache is full

# Anti-pattern 2: volatile-* when no keys have TTL
maxmemory-policy volatile-lru
# If no keys have TTL, behaves like noeviction!
# Result: OOM errors even though eviction is configured

# Anti-pattern 3: allkeys-* when some data must persist
maxmemory-policy allkeys-lru
# Will evict ANY key including important non-cache data
# Result: Critical data randomly deleted
```

**Correct (policy matches use case):**

```bash
# Correct 1: Pure cache - use allkeys-lru or allkeys-lfu
# redis.conf
maxmemory 4gb
maxmemory-policy allkeys-lru  # General caching
# OR
maxmemory-policy allkeys-lfu  # Better for skewed access patterns

# Correct 2: Cache + persistent data - use volatile-*
# Set TTL on cache keys, no TTL on persistent keys
maxmemory 4gb
maxmemory-policy volatile-lru
# Only keys with TTL are evicted

# Correct 3: Session store - volatile-ttl
maxmemory 2gb
maxmemory-policy volatile-ttl
# Sessions expiring soonest are evicted first

# Correct 4: Primary database (no eviction acceptable)
maxmemory 8gb
maxmemory-policy noeviction
# Application must handle OOM errors gracefully
```

```python
import redis
r = redis.Redis()

# Correct 1: Verify eviction policy matches your needs
def verify_eviction_config():
    """Check that eviction policy is appropriate"""
    info = r.info("memory")
    policy = info.get("maxmemory_policy", "unknown")
    max_mem = info.get("maxmemory", 0)

    print(f"maxmemory: {max_mem}")
    print(f"maxmemory-policy: {policy}")

    if policy == "noeviction":
        print("WARNING: noeviction policy - writes will fail when memory full")

    if policy.startswith("volatile"):
        # Check if we actually have keys with TTL
        all_keys = r.dbsize()
        with_ttl = check_keys_with_ttl_sample()
        if with_ttl < all_keys * 0.1:
            print(f"WARNING: volatile policy but only {with_ttl}/{all_keys} keys have TTL")

def check_keys_with_ttl_sample(sample_size=1000):
    """Sample keys to estimate how many have TTL"""
    count = 0
    with_ttl = 0

    for key in r.scan_iter(count=100):
        ttl = r.ttl(key)
        if ttl > 0:  # Has TTL (not -1 = no TTL, not -2 = doesn't exist)
            with_ttl += 1
        count += 1
        if count >= sample_size:
            break

    return with_ttl

# Correct 2: Cache pattern with volatile-lru
# Set TTL on cache keys, persistent keys have no TTL
def cache_set(key, value, ttl=3600):
    """Cache with TTL (eligible for eviction)"""
    r.setex(f"cache:{key}", ttl, value)

def persist_set(key, value):
    """Persistent data without TTL (protected from volatile eviction)"""
    r.set(f"data:{key}", value)  # No TTL = protected with volatile-* policy

# Correct 3: Handle eviction in application
def get_or_compute(key, compute_func, ttl=3600):
    """
    Cache pattern that handles evicted keys gracefully.
    If key was evicted, recompute and cache again.
    """
    value = r.get(key)
    if value is None:
        value = compute_func()
        r.setex(key, ttl, value)
    return value

# Correct 4: Monitor eviction
def get_eviction_stats():
    """Monitor key evictions"""
    info = r.info("stats")
    return {
        "evicted_keys": info.get("evicted_keys", 0),
        "keyspace_hits": info.get("keyspace_hits", 0),
        "keyspace_misses": info.get("keyspace_misses", 0),
    }

def alert_on_eviction_rate(threshold_per_second=100):
    """Alert if eviction rate is too high"""
    stats1 = get_eviction_stats()
    time.sleep(1)
    stats2 = get_eviction_stats()

    eviction_rate = stats2["evicted_keys"] - stats1["evicted_keys"]
    if eviction_rate > threshold_per_second:
        print(f"HIGH EVICTION RATE: {eviction_rate}/sec")
        return True
    return False
```

```bash
# Runtime policy change
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Check eviction statistics
redis-cli INFO stats | grep evicted

# Tune eviction sampling (higher = more accurate, slightly slower)
redis-cli CONFIG SET maxmemory-samples 10
```

```python
# Policy selection decision tree

def recommend_eviction_policy(
    is_pure_cache: bool,
    has_ttl_on_cache_keys: bool,
    has_persistent_data: bool,
    access_pattern: str  # "uniform" or "skewed"
):
    """Recommend eviction policy based on use case"""

    if not is_pure_cache and has_persistent_data:
        if has_ttl_on_cache_keys:
            # Mixed: cache (with TTL) + persistent (no TTL)
            if access_pattern == "skewed":
                return "volatile-lfu"
            return "volatile-lru"
        else:
            # Must use noeviction if can't lose data
            return "noeviction"

    # Pure cache
    if access_pattern == "skewed":
        return "allkeys-lfu"  # Frequently accessed items kept
    return "allkeys-lru"  # Recently accessed items kept

# Examples:
# Pure cache: allkeys-lru or allkeys-lfu
# Session store: volatile-ttl (shortest TTL evicted first)
# Mixed workload: volatile-lru (only cache keys have TTL)
# Database: noeviction (handle OOM in app)
```

Reference: [Redis Eviction Policies](https://redis.io/docs/manual/eviction/)
