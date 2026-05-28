---
title: Configure AOF Rewrite Properly
impact: MEDIUM
impactDescription: prevents AOF from growing unbounded, manages disk usage
tags: persistence, aof, rewrite, disk-space
---

## Configure AOF Rewrite Properly

Configure automatic AOF rewriting to prevent the AOF file from growing unbounded. Rewriting compacts the AOF by generating the minimal set of commands to recreate the current dataset.

**Why AOF Rewriting:**
- AOF grows with every write operation
- Old/overwritten data remains in file
- Rewrite creates minimal command set
- Reduces disk usage and restart time

**Rewrite Triggers:**
- Automatic: Based on size percentage growth
- Manual: `BGREWRITEAOF` command

**Incorrect (no or poor rewrite config):**

```bash
# Anti-pattern 1: No automatic rewrite
# redis.conf
appendonly yes
auto-aof-rewrite-percentage 0  # Disabled!
# AOF grows forever, fills disk

# Anti-pattern 2: Rewrite too aggressive
auto-aof-rewrite-percentage 10
auto-aof-rewrite-min-size 1mb
# Rewrites constantly, causes overhead

# Anti-pattern 3: Never rewriting manually
# File grows to 100GB, restart takes hours
```

**Correct (proper rewrite configuration):**

```bash
# Correct 1: Recommended automatic rewrite settings
# redis.conf
appendonly yes
appendfsync everysec

# Rewrite when AOF is 100% larger than after last rewrite
auto-aof-rewrite-percentage 100

# Don't rewrite unless AOF is at least 64MB
auto-aof-rewrite-min-size 64mb

# Use RDB preamble for faster loading (Redis 4.0+)
aof-use-rdb-preamble yes

# Don't fsync during rewrite (faster, slightly less safe)
no-appendfsync-on-rewrite no  # 'yes' for better performance

# Truncate incomplete AOF on load rather than error
aof-load-truncated yes
```

```python
import redis
r = redis.Redis()

# Monitor AOF size and rewrite status
def check_aof_status():
    """Check AOF file status"""
    info = r.info("persistence")

    if not info.get("aof_enabled"):
        return {"enabled": False}

    current_size = info.get("aof_current_size", 0)
    base_size = info.get("aof_base_size", 0)

    # Calculate growth percentage
    if base_size > 0:
        growth_pct = ((current_size - base_size) / base_size) * 100
    else:
        growth_pct = 0

    return {
        "enabled": True,
        "current_size_mb": current_size / 1024 / 1024,
        "base_size_mb": base_size / 1024 / 1024,
        "growth_percentage": growth_pct,
        "rewrite_in_progress": info.get("aof_rewrite_in_progress", 0) == 1,
        "rewrite_scheduled": info.get("aof_rewrite_scheduled", 0) == 1,
        "last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec", -1),
    }

# Trigger manual rewrite
def trigger_aof_rewrite(wait=True):
    """Trigger background AOF rewrite"""
    info = r.info("persistence")
    if info.get("aof_rewrite_in_progress"):
        print("Rewrite already in progress")
        return False

    print("Triggering BGREWRITEAOF...")
    r.bgrewriteaof()

    if wait:
        while True:
            info = r.info("persistence")
            if not info.get("aof_rewrite_in_progress"):
                break
            time.sleep(1)
            print(".", end="", flush=True)

        print("\nRewrite complete")
        return info.get("aof_last_bgrewrite_status") == "ok"

    return True

# Alert on large AOF growth
def alert_on_aof_growth(threshold_pct=150):
    """Alert if AOF has grown significantly since last rewrite"""
    status = check_aof_status()

    if not status.get("enabled"):
        return {"alert": False, "reason": "AOF not enabled"}

    if status["growth_percentage"] > threshold_pct:
        return {
            "alert": True,
            "message": f"AOF grown {status['growth_percentage']:.0f}% since last rewrite",
            "current_size_mb": status["current_size_mb"],
            "base_size_mb": status["base_size_mb"],
            "recommendation": "Consider manual BGREWRITEAOF or check auto-rewrite settings"
        }

    return {"alert": False}
```

```python
# Schedule rewrite during low-traffic periods
import schedule
import time

def maintenance_rewrite():
    """Perform AOF rewrite during maintenance window"""
    status = check_aof_status()

    # Only rewrite if significant growth
    if status.get("growth_percentage", 0) > 50:
        print(f"AOF growth: {status['growth_percentage']:.0f}%, triggering rewrite")
        trigger_aof_rewrite(wait=True)
    else:
        print(f"AOF growth: {status['growth_percentage']:.0f}%, skipping rewrite")

# Schedule for 3 AM daily
schedule.every().day.at("03:00").do(maintenance_rewrite)

# Or run manually during maintenance
# trigger_aof_rewrite(wait=True)
```

```bash
# Check AOF rewrite settings at runtime
redis-cli CONFIG GET auto-aof-rewrite-*

# Modify rewrite threshold
redis-cli CONFIG SET auto-aof-rewrite-percentage 100
redis-cli CONFIG SET auto-aof-rewrite-min-size 67108864  # 64MB

# Manual rewrite
redis-cli BGREWRITEAOF

# Monitor rewrite progress
redis-cli INFO persistence | grep aof_rewrite
```

```python
# Correct: Handle no-appendfsync-on-rewrite trade-off
def configure_aof_rewrite_safety(prioritize_performance=False):
    """
    Configure AOF rewrite behavior.

    no-appendfsync-on-rewrite:
    - 'yes': Don't fsync during rewrite (faster, may lose up to 30s on crash)
    - 'no': Continue fsync during rewrite (safer, may cause latency)
    """
    if prioritize_performance:
        # Faster rewrites, but may lose data if crash during rewrite
        r.config_set("no-appendfsync-on-rewrite", "yes")
        print("Set no-appendfsync-on-rewrite=yes (faster, less safe)")
    else:
        # Safer, but may have latency spikes during rewrite
        r.config_set("no-appendfsync-on-rewrite", "no")
        print("Set no-appendfsync-on-rewrite=no (safer, may have latency)")

# Verify AOF integrity
def verify_aof():
    """Check AOF file for corruption"""
    import subprocess

    config = r.config_get("dir")
    aof_dir = config.get("dir", "/var/lib/redis")

    # Redis 7+ uses appendonlydir
    aof_path = os.path.join(aof_dir, "appendonlydir")
    if not os.path.exists(aof_path):
        aof_path = os.path.join(aof_dir, "appendonly.aof")

    result = subprocess.run(
        ["redis-check-aof", "--fix", aof_path],
        capture_output=True,
        text=True
    )

    return result.returncode == 0, result.stdout
```

Reference: [Redis AOF Rewrite](https://redis.io/docs/management/persistence/#log-rewriting)
