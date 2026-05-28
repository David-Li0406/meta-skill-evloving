---
title: Always Configure maxmemory Limit
impact: CRITICAL
impactDescription: prevents OOM crashes, enables predictable behavior
tags: memory, configuration, maxmemory, stability
---

## Always Configure maxmemory Limit

Always set a `maxmemory` limit for Redis. Without it, Redis uses unlimited memory and will be killed by the OS OOM killer when it exhausts system memory, causing data loss and outages.

**Why maxmemory is Critical:**
- Without limit: Redis grows until OS kills it
- OOM killer: Abrupt termination, no graceful handling
- Data loss: Unsaved data is lost
- Cascading failure: Dependent services fail

**Recommended Settings:**
- Set maxmemory to 75-80% of available RAM
- Leave room for OS, persistence operations, and fork()
- Configure appropriate eviction policy

**Incorrect (no memory limit):**

```bash
# redis.conf - Anti-pattern: no maxmemory set
# maxmemory <bytes>  # Commented out or missing
# Redis will use unlimited memory!

# Anti-pattern: maxmemory too high
maxmemory 64gb  # On a 64GB machine - no room for OS!
```

```python
import redis
r = redis.Redis()

# Anti-pattern: No monitoring for memory pressure
def cache_data(key, value):
    r.set(key, value)  # Keep adding without checking memory
```

**Correct (configure maxmemory):**

```bash
# redis.conf - Production configuration

# Set maxmemory to ~75% of available RAM
# For 8GB machine:
maxmemory 6gb

# For 32GB machine:
maxmemory 24gb

# Must also set eviction policy (see memory-choose-eviction-policy)
maxmemory-policy allkeys-lru

# Optional: memory samples for eviction accuracy
maxmemory-samples 10
```

```bash
# Set at runtime via CLI
redis-cli CONFIG SET maxmemory 6gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Verify settings
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET maxmemory-policy

# Check current memory usage
redis-cli INFO memory
```

```python
import redis
r = redis.Redis()

# Correct 1: Check memory before operations
def check_memory_health():
    """Check if Redis has sufficient memory"""
    info = r.info("memory")
    used = info['used_memory']
    max_mem = info.get('maxmemory', 0)

    if max_mem == 0:
        print("WARNING: maxmemory not configured!")
        return False

    usage_pct = (used / max_mem) * 100
    print(f"Memory usage: {usage_pct:.1f}% ({used / 1024 / 1024:.1f}MB / {max_mem / 1024 / 1024:.1f}MB)")

    if usage_pct > 90:
        print("WARNING: Memory usage critical!")
        return False

    return True

# Correct 2: Graceful handling of memory pressure
def safe_cache_set(key, value, ttl=3600):
    """Set with memory-aware error handling"""
    try:
        r.setex(key, ttl, value)
        return True
    except redis.ResponseError as e:
        if "OOM" in str(e):
            # Handle OOM - Redis maxmemory reached with noeviction
            print(f"Redis OOM: Cannot write {key}")
            return False
        raise

# Correct 3: Memory monitoring and alerting
def get_memory_stats():
    """Get detailed memory statistics"""
    info = r.info("memory")
    return {
        "used_memory": info["used_memory"],
        "used_memory_human": info["used_memory_human"],
        "used_memory_peak": info["used_memory_peak"],
        "used_memory_peak_human": info["used_memory_peak_human"],
        "maxmemory": info.get("maxmemory", 0),
        "maxmemory_human": info.get("maxmemory_human", "0B"),
        "maxmemory_policy": info.get("maxmemory_policy", "noeviction"),
        "mem_fragmentation_ratio": info.get("mem_fragmentation_ratio", 0),
        "used_memory_rss": info.get("used_memory_rss", 0),
    }

def alert_on_high_memory(threshold_pct=85):
    """Alert if memory usage exceeds threshold"""
    stats = get_memory_stats()
    max_mem = stats["maxmemory"]

    if max_mem == 0:
        raise ValueError("maxmemory not configured - critical!")

    usage_pct = (stats["used_memory"] / max_mem) * 100

    if usage_pct >= threshold_pct:
        return {
            "alert": True,
            "message": f"Redis memory at {usage_pct:.1f}%",
            "used": stats["used_memory_human"],
            "max": stats["maxmemory_human"],
        }
    return {"alert": False}
```

```python
# Docker/Kubernetes configuration

# Docker Compose
"""
services:
  redis:
    image: redis:7
    command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
    deploy:
      resources:
        limits:
          memory: 3g  # Container limit > maxmemory (for fork/persistence)
"""

# Kubernetes ConfigMap
"""
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.conf: |
    maxmemory 2gb
    maxmemory-policy allkeys-lru
    maxmemory-samples 10
"""
```

```javascript
// Node.js - Memory monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function checkMemoryHealth() {
    const info = await redis.info('memory');
    const lines = info.split('\r\n');
    const stats = {};

    lines.forEach(line => {
        const [key, value] = line.split(':');
        if (key && value) stats[key] = value;
    });

    const used = parseInt(stats.used_memory);
    const max = parseInt(stats.maxmemory || '0');

    if (max === 0) {
        console.warn('maxmemory not configured!');
        return false;
    }

    const usagePct = (used / max) * 100;
    console.log(`Memory: ${usagePct.toFixed(1)}%`);

    return usagePct < 90;
}
```

Reference: [Redis Memory Management](https://redis.io/docs/management/optimization/memory-optimization/)
