---
title: Regularly Test Backup Recovery
impact: HIGH
impactDescription: untested backups are not backups
tags: persistence, backup, recovery, disaster-recovery, testing
---

## Regularly Test Backup Recovery

Regularly test restoring from backups. Untested backups are not backups - you won't know if they work until you need them. Automate recovery testing to verify backup integrity and document restoration procedures.

**What to Test:**
- RDB file loads correctly
- AOF file replays correctly
- Data integrity after restore
- Recovery time (RTO) meets requirements
- Documented procedure is accurate

**Incorrect (no recovery testing):**

```bash
# Anti-pattern 1: Assuming backups work
# "We run BGSAVE every hour, we're safe"
# But never tested if those backups actually restore

# Anti-pattern 2: Testing only once
# "We tested recovery during initial setup"
# Configuration changes, data grows, backups may no longer work

# Anti-pattern 3: No documented procedure
# Only one person knows how to restore
# They're on vacation when disaster strikes
```

**Correct (regular recovery testing):**

```python
import redis
import subprocess
import tempfile
import shutil
import os
import time

# Correct 1: Automated backup verification
def verify_rdb_backup(backup_path):
    """
    Verify RDB backup can be loaded by starting test Redis instance.
    """
    # Use redis-check-rdb for quick validation
    result = subprocess.run(
        ["redis-check-rdb", backup_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "valid": False,
            "error": result.stderr,
            "check": "redis-check-rdb"
        }

    # For thorough testing, actually load the backup
    return load_and_verify_backup(backup_path)

def load_and_verify_backup(backup_path):
    """
    Load backup in isolated Redis instance and verify.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy backup to temp directory
        shutil.copy(backup_path, os.path.join(tmpdir, "dump.rdb"))

        # Start isolated Redis instance
        port = 16379  # Different port to avoid conflicts
        process = subprocess.Popen([
            "redis-server",
            "--port", str(port),
            "--dir", tmpdir,
            "--dbfilename", "dump.rdb",
            "--appendonly", "no",
            "--daemonize", "no"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            time.sleep(2)  # Wait for startup

            # Connect and verify
            test_redis = redis.Redis(port=port)

            # Check basic connectivity
            test_redis.ping()

            # Get key count
            key_count = test_redis.dbsize()

            # Sample some keys to verify data
            sample_keys = list(test_redis.scan_iter(count=10))[:10]
            samples = []
            for key in sample_keys:
                key_type = test_redis.type(key).decode()
                samples.append({"key": key.decode(), "type": key_type})

            return {
                "valid": True,
                "key_count": key_count,
                "sample_keys": samples,
                "check": "full_load_test"
            }

        finally:
            process.terminate()
            process.wait()

# Correct 2: Scheduled recovery test
def scheduled_recovery_test(backup_dir="/backups/redis"):
    """
    Automated recovery test for cron/scheduler.
    """
    # Find latest backup
    backups = sorted([
        f for f in os.listdir(backup_dir)
        if f.endswith('.rdb')
    ], reverse=True)

    if not backups:
        return {"success": False, "error": "No backups found"}

    latest = os.path.join(backup_dir, backups[0])
    result = verify_rdb_backup(latest)

    # Log results
    log_entry = {
        "timestamp": time.time(),
        "backup_file": backups[0],
        "verification_result": result
    }

    # Alert on failure
    if not result.get("valid"):
        send_alert(f"Backup verification failed: {result}")

    return log_entry
```

```bash
#!/bin/bash
# Correct 3: Recovery test script

set -e

BACKUP_DIR="/backups/redis"
TEST_PORT=16379
LOG_FILE="/var/log/redis-recovery-test.log"

echo "$(date): Starting recovery test" >> $LOG_FILE

# Find latest backup
LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/*.rdb 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "$(date): ERROR - No backups found" >> $LOG_FILE
    exit 1
fi

echo "$(date): Testing backup: $LATEST_BACKUP" >> $LOG_FILE

# Validate with redis-check-rdb
if ! redis-check-rdb "$LATEST_BACKUP" >> $LOG_FILE 2>&1; then
    echo "$(date): ERROR - Backup failed validation" >> $LOG_FILE
    # Send alert
    exit 1
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
cp "$LATEST_BACKUP" "$TEMP_DIR/dump.rdb"

# Start test instance
redis-server --port $TEST_PORT --dir "$TEMP_DIR" --daemonize yes

sleep 3

# Verify
KEY_COUNT=$(redis-cli -p $TEST_PORT DBSIZE | grep -oP '\d+')
PING=$(redis-cli -p $TEST_PORT PING)

# Shutdown test instance
redis-cli -p $TEST_PORT SHUTDOWN NOSAVE 2>/dev/null || true

# Cleanup
rm -rf "$TEMP_DIR"

if [ "$PING" == "PONG" ] && [ "$KEY_COUNT" -gt 0 ]; then
    echo "$(date): SUCCESS - Backup verified, $KEY_COUNT keys" >> $LOG_FILE
    exit 0
else
    echo "$(date): ERROR - Verification failed" >> $LOG_FILE
    exit 1
fi
```

```python
# Correct 4: Document and automate the full procedure
RECOVERY_PROCEDURE = """
# Redis Disaster Recovery Procedure

## Prerequisites
- Access to backup storage (S3/NFS/local)
- Redis installed on target server
- Network access to application servers

## Recovery Steps

### 1. Stop Current Redis (if running)
```bash
redis-cli SHUTDOWN SAVE  # or NOSAVE if corrupted
```

### 2. Backup Current Data (if any)
```bash
mv /var/lib/redis/dump.rdb /var/lib/redis/dump.rdb.corrupted
mv /var/lib/redis/appendonlydir /var/lib/redis/appendonlydir.corrupted
```

### 3. Download Backup
```bash
# From S3
aws s3 cp s3://bucket/redis/dump_YYYYMMDD.rdb /var/lib/redis/dump.rdb

# Or from NFS
cp /backups/redis/dump_YYYYMMDD.rdb /var/lib/redis/dump.rdb
```

### 4. Set Permissions
```bash
chown redis:redis /var/lib/redis/dump.rdb
chmod 660 /var/lib/redis/dump.rdb
```

### 5. Start Redis
```bash
systemctl start redis
# or
redis-server /etc/redis/redis.conf
```

### 6. Verify Recovery
```bash
redis-cli PING  # Should return PONG
redis-cli DBSIZE  # Check key count
redis-cli INFO persistence  # Verify persistence status
```

### 7. Verify Application
- Test application connectivity
- Check critical data exists
- Monitor for errors

## Rollback
If recovery fails, restore from older backup or contact support.

## Contacts
- Primary: ops-team@company.com
- Escalation: infrastructure@company.com
"""

def print_recovery_procedure():
    print(RECOVERY_PROCEDURE)

# Correct 5: Measure Recovery Time
def measure_recovery_time(backup_path, target_port=16379):
    """Measure how long recovery takes (RTO)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy(backup_path, os.path.join(tmpdir, "dump.rdb"))

        start_time = time.time()

        process = subprocess.Popen([
            "redis-server",
            "--port", str(target_port),
            "--dir", tmpdir,
            "--daemonize", "no"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            # Wait for Redis to be ready
            test_redis = redis.Redis(port=target_port)
            while True:
                try:
                    if test_redis.ping():
                        break
                except:
                    pass
                time.sleep(0.1)

            recovery_time = time.time() - start_time
            key_count = test_redis.dbsize()

            return {
                "recovery_time_seconds": recovery_time,
                "key_count": key_count,
                "backup_size_mb": os.path.getsize(backup_path) / 1024 / 1024
            }

        finally:
            process.terminate()
            process.wait()
```

Reference: [Redis Backup and Restore](https://redis.io/docs/management/persistence/)
