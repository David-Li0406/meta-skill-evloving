---
title: Monitor and Handle Memory Fragmentation
impact: MEDIUM-HIGH
impactDescription: high fragmentation wastes 20-50% memory
tags: memory, fragmentation, monitoring, defragmentation
---

## Monitor and Handle Memory Fragmentation

Monitor memory fragmentation ratio and take action when it's too high. Fragmentation occurs when Redis allocates and frees memory repeatedly, leaving gaps. High fragmentation wastes memory and can cause OOM even with available space.

**Fragmentation Ratio:**
- `mem_fragmentation_ratio = used_memory_rss / used_memory`
- **< 1.0**: Redis using swap (very bad!)
- **1.0 - 1.5**: Healthy
- **> 1.5**: Moderate fragmentation
- **> 2.0**: High fragmentation, action needed

**Causes of Fragmentation:**
- Frequent key creation/deletion
- Variable-size updates
- Large deletions followed by small writes
- Long-running instances without restarts

**Incorrect (ignoring fragmentation):**

```python
import redis
r = redis.Redis()

# Anti-pattern: Not monitoring fragmentation
def check_memory_bad():
    info = r.info("memory")
    print(f"Used memory: {info['used_memory_human']}")
    # Missing fragmentation check!

# Anti-pattern: Assuming used_memory is all that matters
def has_memory_available_bad(needed_bytes):
    info = r.info("memory")
    max_mem = info.get("maxmemory", 0)
    used = info["used_memory"]
    return (max_mem - used) > needed_bytes
# Wrong! RSS (actual memory) could be much higher due to fragmentation
```

**Correct (monitoring and handling fragmentation):**

```python
import redis
r = redis.Redis()

# Correct 1: Monitor fragmentation ratio
def check_memory_health():
    """Comprehensive memory health check including fragmentation"""
    info = r.info("memory")

    used = info["used_memory"]
    rss = info["used_memory_rss"]
    frag_ratio = info["mem_fragmentation_ratio"]
    frag_bytes = info.get("mem_fragmentation_bytes", rss - used)

    health = {
        "used_memory": info["used_memory_human"],
        "used_memory_rss": info["used_memory_rss_human"],
        "fragmentation_ratio": frag_ratio,
        "fragmentation_bytes": frag_bytes,
        "status": "healthy"
    }

    if frag_ratio < 1.0:
        health["status"] = "critical"
        health["issue"] = "Using swap memory!"
    elif frag_ratio > 2.0:
        health["status"] = "warning"
        health["issue"] = f"High fragmentation: {frag_ratio:.2f}"
        health["wasted_memory"] = f"{frag_bytes / 1024 / 1024:.1f} MB"
    elif frag_ratio > 1.5:
        health["status"] = "moderate"
        health["issue"] = f"Moderate fragmentation: {frag_ratio:.2f}"

    return health

def alert_on_fragmentation(threshold=1.5):
    """Alert when fragmentation exceeds threshold"""
    info = r.info("memory")
    frag_ratio = info["mem_fragmentation_ratio"]

    if frag_ratio < 1.0:
        return {
            "alert": "CRITICAL",
            "message": "Redis is using swap! Performance severely degraded.",
            "ratio": frag_ratio
        }
    elif frag_ratio > threshold:
        frag_bytes = info.get("mem_fragmentation_bytes", 0)
        return {
            "alert": "WARNING",
            "message": f"Memory fragmentation at {frag_ratio:.2f}",
            "ratio": frag_ratio,
            "wasted_mb": frag_bytes / 1024 / 1024
        }

    return {"alert": None}

# Correct 2: Check if active defragmentation is running
def check_defrag_status():
    """Check active defragmentation status"""
    info = r.info("memory")
    return {
        "active_defrag_running": info.get("active_defrag_running", 0),
        "active_defrag_hits": info.get("active_defrag_hits", 0),
        "active_defrag_misses": info.get("active_defrag_misses", 0),
        "active_defrag_key_hits": info.get("active_defrag_key_hits", 0),
        "active_defrag_key_misses": info.get("active_defrag_key_misses", 0),
    }
```

```bash
# Enable active defragmentation (Redis 4.0+)
# redis.conf

# Enable active defrag (off by default)
activedefrag yes

# Start defrag when fragmentation > 10%
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10

# Stop when fragmentation < 5%
active-defrag-threshold-upper 100

# CPU effort (1-25% of idle CPU)
active-defrag-cycle-min 1
active-defrag-cycle-max 25

# Max scan per cycle (reduce for latency-sensitive workloads)
active-defrag-max-scan-fields 1000
```

```python
# Correct 3: Enable/configure defrag at runtime
def configure_defragmentation():
    """Enable and configure active defragmentation"""
    # Enable active defrag
    r.config_set("activedefrag", "yes")

    # Start defrag when fragmentation exceeds 10%
    r.config_set("active-defrag-threshold-lower", "10")

    # Aggressive defrag above 50% fragmentation
    r.config_set("active-defrag-threshold-upper", "50")

    # CPU usage for defrag (1-25% of idle CPU)
    r.config_set("active-defrag-cycle-min", "5")
    r.config_set("active-defrag-cycle-max", "25")

    # Ignore if fragmented memory < 100MB
    r.config_set("active-defrag-ignore-bytes", "104857600")

def disable_defragmentation():
    """Disable defrag during performance-critical periods"""
    r.config_set("activedefrag", "no")

# Correct 4: Manual defrag trigger (Redis 7.2+)
def trigger_manual_defrag():
    """Trigger one-time defragmentation"""
    try:
        r.execute_command("MEMORY", "DEFRAG")
        print("Manual defragmentation triggered")
    except redis.ResponseError as e:
        print(f"Defrag not available: {e}")
```

```python
# Correct 5: Strategies to prevent fragmentation

def prevent_fragmentation_tips():
    """Best practices to minimize fragmentation"""
    return """
    1. Use consistent value sizes when possible
    2. Set TTL on temporary keys (automatic cleanup)
    3. Use UNLINK instead of DEL for large keys (async delete)
    4. Consider periodic restarts for long-running instances
    5. Enable active defragmentation for write-heavy workloads
    6. Monitor fragmentation ratio in your metrics
    """

# Use UNLINK for large key deletion
def delete_large_key(key):
    """Delete key asynchronously to reduce blocking and fragmentation"""
    r.unlink(key)  # Non-blocking delete
    # vs r.delete(key) which blocks

# Batch delete with UNLINK
def delete_keys_by_pattern(pattern):
    """Delete keys matching pattern using async UNLINK"""
    pipe = r.pipeline()
    count = 0

    for key in r.scan_iter(match=pattern, count=100):
        pipe.unlink(key)
        count += 1

        if count % 1000 == 0:
            pipe.execute()
            pipe = r.pipeline()

    if count % 1000 != 0:
        pipe.execute()

    return count
```

```bash
# Monitor fragmentation from CLI
redis-cli INFO memory | grep frag

# Output:
# mem_fragmentation_ratio:1.23
# mem_fragmentation_bytes:12345678

# Memory doctor (Redis 4.0+)
redis-cli MEMORY DOCTOR

# Detailed memory stats
redis-cli MEMORY STATS
```

Reference: [Redis Active Defragmentation](https://redis.io/docs/management/optimization/memory-optimization/#active-defragmentation)
