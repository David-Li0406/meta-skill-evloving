---
title: Understand RDB vs AOF Persistence
impact: CRITICAL
impactDescription: wrong choice can cause data loss or performance issues
tags: persistence, rdb, aof, durability, backup
---

## Understand RDB vs AOF Persistence

Choose the right persistence strategy based on your durability requirements and performance constraints. RDB and AOF have different trade-offs, and you can use both together.

**RDB (Redis Database Backup):**
- Point-in-time snapshots
- Compact single-file backups
- Faster restarts
- Can lose data since last snapshot
- Good for: Backups, disaster recovery, replication

**AOF (Append Only File):**
- Logs every write operation
- More durable (configurable fsync)
- Larger files, slower restarts
- Can lose data based on fsync policy
- Good for: Durability-critical applications

**Comparison:**
| Aspect | RDB | AOF |
|--------|-----|-----|
| Durability | Minutes of data loss | Seconds/none |
| File size | Compact | Larger |
| Restart speed | Fast | Slower |
| Write performance | Periodic impact | Continuous (small) |
| Best for | Backups | Durability |

**Incorrect (misunderstanding persistence):**

```bash
# Anti-pattern 1: No persistence for production data
# redis.conf
save ""  # RDB disabled
appendonly no  # AOF disabled
# All data lost on restart!

# Anti-pattern 2: AOF with no fsync (cache behavior)
appendonly yes
appendfsync no  # OS decides when to flush - can lose seconds of data
# Might as well use RDB if durability doesn't matter

# Anti-pattern 3: RDB only for critical data
save 900 1     # Save every 15 min if 1 key changed
save 300 10    # Save every 5 min if 10 keys changed
save 60 10000  # Save every 60s if 10000 keys changed
# With heavy writes, might lose up to 15 minutes of data!
```

**Correct (choose based on requirements):**

```bash
# Correct 1: Cache only (no persistence needed)
# Data can be regenerated, performance is priority
# redis.conf
save ""
appendonly no

# Correct 2: Moderate durability (RDB + AOF everysec)
# Balance of durability and performance
# redis.conf
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec  # Lose at most 1 second of data
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Correct 3: Maximum durability (AOF always)
# Critical financial/transactional data
# redis.conf
appendonly yes
appendfsync always  # Fsync after every write - slowest but safest
# Note: Significant performance impact

# Correct 4: Recommended production setup
# RDB for backups + AOF for durability
# redis.conf
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes

appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite no  # Safer, but may impact latency during rewrite
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-use-rdb-preamble yes  # Hybrid: RDB for fast load + AOF for recent ops
```

```python
import redis
r = redis.Redis()

# Check current persistence configuration
def check_persistence_config():
    """Get current persistence settings"""
    config = {}

    # RDB settings
    rdb_save = r.config_get("save")
    config["rdb"] = {
        "save_rules": rdb_save.get("save", ""),
        "compression": r.config_get("rdbcompression").get("rdbcompression"),
        "checksum": r.config_get("rdbchecksum").get("rdbchecksum"),
    }

    # AOF settings
    config["aof"] = {
        "enabled": r.config_get("appendonly").get("appendonly"),
        "fsync_policy": r.config_get("appendfsync").get("appendfsync"),
        "rewrite_percentage": r.config_get("auto-aof-rewrite-percentage").get("auto-aof-rewrite-percentage"),
        "rewrite_min_size": r.config_get("auto-aof-rewrite-min-size").get("auto-aof-rewrite-min-size"),
    }

    # Persistence status
    info = r.info("persistence")
    config["status"] = {
        "rdb_last_save_time": info.get("rdb_last_save_time"),
        "rdb_last_bgsave_status": info.get("rdb_last_bgsave_status"),
        "aof_enabled": info.get("aof_enabled"),
        "aof_last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec"),
        "aof_current_size": info.get("aof_current_size"),
    }

    return config

# Verify persistence is working
def verify_persistence_health():
    """Check if persistence is healthy"""
    info = r.info("persistence")
    issues = []

    # Check RDB
    if info.get("rdb_last_bgsave_status") != "ok":
        issues.append(f"RDB save failed: {info.get('rdb_last_bgsave_status')}")

    rdb_age = time.time() - info.get("rdb_last_save_time", 0)
    if rdb_age > 3600:  # > 1 hour
        issues.append(f"RDB snapshot is {rdb_age/3600:.1f} hours old")

    # Check AOF
    if info.get("aof_enabled"):
        if info.get("aof_last_write_status") != "ok":
            issues.append(f"AOF write failed: {info.get('aof_last_write_status')}")

        if info.get("aof_rewrite_in_progress"):
            issues.append("AOF rewrite in progress")

    return {"healthy": len(issues) == 0, "issues": issues}
```

```python
# Decision guide for persistence
def recommend_persistence(
    is_cache_only: bool,
    max_acceptable_data_loss_seconds: int,
    write_throughput: str,  # "low", "medium", "high"
    restart_time_critical: bool
):
    """Recommend persistence configuration"""

    if is_cache_only:
        return {
            "recommendation": "No persistence",
            "config": {"save": "", "appendonly": "no"},
            "rationale": "Data can be regenerated, no persistence needed"
        }

    if max_acceptable_data_loss_seconds == 0:
        return {
            "recommendation": "AOF with appendfsync always",
            "config": {
                "appendonly": "yes",
                "appendfsync": "always",
                "save": "900 1 300 10 60 10000"  # Keep RDB for backups
            },
            "rationale": "Zero data loss required. Note: ~50% write performance impact",
            "warning": "High write throughput may be impacted significantly"
        }

    if max_acceptable_data_loss_seconds <= 1:
        return {
            "recommendation": "AOF with appendfsync everysec",
            "config": {
                "appendonly": "yes",
                "appendfsync": "everysec",
                "save": "900 1 300 10 60 10000",
                "aof-use-rdb-preamble": "yes"
            },
            "rationale": "At most 1 second data loss, good performance"
        }

    # More tolerant of data loss
    return {
        "recommendation": "RDB snapshots",
        "config": {
            "save": "900 1 300 10 60 10000",
            "appendonly": "no"
        },
        "rationale": f"Acceptable data loss, RDB provides good backup"
    }
```

Reference: [Redis Persistence](https://redis.io/docs/management/persistence/)
