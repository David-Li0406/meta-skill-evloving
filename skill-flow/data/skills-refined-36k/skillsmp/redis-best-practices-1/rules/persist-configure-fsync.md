---
title: Configure Appropriate fsync Policy
impact: HIGH
impactDescription: balances durability vs write performance
tags: persistence, aof, fsync, durability, performance
---

## Configure Appropriate fsync Policy

Choose the right `appendfsync` policy for AOF based on your durability requirements. The fsync policy determines when data is actually written to disk, affecting both data safety and performance.

**fsync Policies:**
| Policy | Behavior | Data Loss Risk | Performance |
|--------|----------|----------------|-------------|
| `always` | fsync after every write | None | Slowest (~50% impact) |
| `everysec` | fsync every second | Up to 1 second | Good (recommended) |
| `no` | OS decides when to flush | Seconds to minutes | Fastest |

**Incorrect (mismatched policy and requirements):**

```bash
# Anti-pattern 1: 'always' for non-critical cache
appendonly yes
appendfsync always  # Unnecessary for cache, kills performance

# Anti-pattern 2: 'no' for important data
appendonly yes
appendfsync no  # Could lose significant data on crash
# OS might buffer for 30+ seconds

# Anti-pattern 3: Enabling AOF without understanding trade-offs
appendonly yes
# Missing appendfsync directive - defaults to 'everysec' but not explicit
```

**Correct (policy matches requirements):**

```bash
# Correct 1: Financial/transactional data - maximum durability
# redis.conf
appendonly yes
appendfsync always
# Every write is immediately durable
# Accept ~50% write performance reduction

# Correct 2: General application data - balanced (RECOMMENDED)
# redis.conf
appendonly yes
appendfsync everysec
# At most 1 second of data loss
# Minimal performance impact

# Correct 3: Session store - performance priority
# Sessions can be regenerated, prioritize speed
# redis.conf
appendonly yes
appendfsync no
# Fastest AOF writes, OS handles flushing
# OR: Just use RDB snapshots

# Correct 4: Hybrid - RDB for restarts, AOF for durability
# redis.conf
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes  # Faster AOF loading
```

```python
import redis
r = redis.Redis()

# Monitor AOF health
def check_aof_health():
    """Check AOF persistence health"""
    info = r.info("persistence")

    if not info.get("aof_enabled"):
        return {"enabled": False}

    return {
        "enabled": True,
        "current_size_mb": info.get("aof_current_size", 0) / 1024 / 1024,
        "base_size_mb": info.get("aof_base_size", 0) / 1024 / 1024,
        "pending_rewrite": info.get("aof_rewrite_scheduled", 0) == 1,
        "rewrite_in_progress": info.get("aof_rewrite_in_progress", 0) == 1,
        "last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec", -1),
        "last_write_status": info.get("aof_last_write_status", "unknown"),
        "buffer_size": info.get("aof_buffer_length", 0),
    }

# Change fsync policy at runtime (use with caution)
def set_fsync_policy(policy):
    """
    Change AOF fsync policy.
    Valid values: 'always', 'everysec', 'no'
    """
    if policy not in ['always', 'everysec', 'no']:
        raise ValueError(f"Invalid policy: {policy}")

    r.config_set("appendfsync", policy)
    return r.config_get("appendfsync")

# Temporarily relax fsync during bulk operations
def bulk_import_with_relaxed_fsync(import_func):
    """
    Temporarily use 'no' fsync during bulk import.
    WARNING: Data may be lost if Redis crashes during import.
    """
    original_policy = r.config_get("appendfsync").get("appendfsync")

    try:
        # Relax fsync for bulk import
        r.config_set("appendfsync", "no")

        # Perform bulk import
        import_func()

        # Force AOF rewrite to persist everything
        r.bgrewriteaof()

    finally:
        # Restore original policy
        r.config_set("appendfsync", original_policy)
```

```bash
# Monitor AOF during operation
redis-cli INFO persistence | grep aof

# Example output:
# aof_enabled:1
# aof_rewrite_in_progress:0
# aof_rewrite_scheduled:0
# aof_last_rewrite_time_sec:2
# aof_current_rewrite_time_sec:-1
# aof_last_bgrewrite_status:ok
# aof_last_write_status:ok
# aof_current_size:1234567
# aof_base_size:1000000
# aof_pending_rewrite:0
# aof_buffer_length:0
```

```python
# Performance benchmarking different fsync policies
def benchmark_fsync_policies():
    """
    Benchmark write performance with different fsync policies.
    Run on test instance only!
    """
    import time
    results = {}

    for policy in ['always', 'everysec', 'no']:
        r.config_set("appendfsync", policy)
        time.sleep(0.1)  # Let setting take effect

        # Benchmark
        start = time.time()
        pipe = r.pipeline()
        for i in range(10000):
            pipe.set(f"bench:{i}", f"value{i}")
        pipe.execute()
        elapsed = time.time() - start

        results[policy] = {
            "writes": 10000,
            "time_sec": elapsed,
            "writes_per_sec": 10000 / elapsed
        }

        # Cleanup
        for i in range(10000):
            r.delete(f"bench:{i}")

    return results

# Typical results:
# 'always': ~5,000 writes/sec (slowest)
# 'everysec': ~50,000 writes/sec (good balance)
# 'no': ~70,000 writes/sec (fastest)
```

Reference: [Redis AOF Configuration](https://redis.io/docs/management/persistence/#append-only-file)
