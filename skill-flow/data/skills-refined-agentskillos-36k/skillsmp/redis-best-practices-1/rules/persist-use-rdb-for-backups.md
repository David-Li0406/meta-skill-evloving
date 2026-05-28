---
title: Use RDB for Backups and Disaster Recovery
impact: HIGH
impactDescription: enables fast restores and offsite backups
tags: persistence, rdb, backup, disaster-recovery
---

## Use RDB for Backups and Disaster Recovery

Use RDB snapshots for backups, replication seeding, and disaster recovery. RDB files are compact, easy to transfer, and enable fast restores. Always have a backup strategy even if using AOF for durability.

**RDB Benefits for Backups:**
- Single compact file
- Easy to copy/transfer
- Fast restore (faster than AOF replay)
- Perfect for point-in-time recovery
- Good for seeding replicas

**Incorrect (no backup strategy):**

```bash
# Anti-pattern 1: Relying only on AOF, no RDB
save ""  # No RDB snapshots
appendonly yes
# AOF is for durability, not ideal for backups:
# - Larger files
# - Slower to restore
# - Can't easily transfer

# Anti-pattern 2: No automated backup copies
save 60 1000
# RDB saved but:
# - Not copied offsite
# - No retention policy
# - No backup verification

# Anti-pattern 3: Backing up from primary during high load
# Causes fork() overhead on primary
```

**Correct (proper backup strategy):**

```bash
# Correct 1: Enable RDB with appropriate schedule
# redis.conf
save 900 1        # Every 15 min if >= 1 key changed
save 300 10       # Every 5 min if >= 10 keys changed
save 60 10000     # Every 1 min if >= 10000 keys changed

rdbcompression yes  # Compress with LZF
rdbchecksum yes     # Add CRC64 checksum for integrity
dbfilename dump.rdb
dir /var/lib/redis/

# Correct 2: Also enable AOF for durability
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes  # Hybrid: RDB + AOF tail
```

```python
import redis
import shutil
import os
from datetime import datetime

r = redis.Redis()

# Correct 3: Trigger manual backup
def create_backup():
    """Trigger RDB snapshot and wait for completion"""
    # Get last save time before triggering
    info = r.info("persistence")
    last_save = info["rdb_last_save_time"]

    # Trigger background save
    r.bgsave()

    # Wait for save to complete
    while True:
        info = r.info("persistence")
        if info["rdb_last_save_time"] > last_save:
            if info["rdb_last_bgsave_status"] == "ok":
                return True
            else:
                raise Exception(f"BGSAVE failed: {info['rdb_last_bgsave_status']}")
        time.sleep(0.5)

# Correct 4: Copy RDB to backup location
def backup_rdb(backup_dir="/backups/redis"):
    """Copy RDB file to backup location with timestamp"""
    # Get RDB file location
    config = r.config_get("dir", "dbfilename")
    rdb_dir = config.get("dir", "/var/lib/redis")
    rdb_file = config.get("dbfilename", "dump.rdb")
    source = os.path.join(rdb_dir, rdb_file)

    if not os.path.exists(source):
        raise FileNotFoundError(f"RDB file not found: {source}")

    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"dump_{timestamp}.rdb")

    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(source, dest)

    return dest

# Correct 5: Full backup procedure
def perform_backup(backup_dir="/backups/redis"):
    """Complete backup procedure"""
    print("1. Triggering BGSAVE...")
    create_backup()

    print("2. Copying RDB file...")
    backup_path = backup_rdb(backup_dir)

    print("3. Verifying backup...")
    # Verify file size is reasonable
    size = os.path.getsize(backup_path)
    info = r.info("persistence")
    expected_size = info.get("rdb_last_cow_size", 0)

    print(f"Backup complete: {backup_path} ({size / 1024 / 1024:.1f} MB)")
    return backup_path
```

```bash
#!/bin/bash
# Correct 6: Backup script for cron

REDIS_DIR="/var/lib/redis"
BACKUP_DIR="/backups/redis"
RETENTION_DAYS=7
S3_BUCKET="s3://mycompany-backups/redis"

# Trigger BGSAVE
redis-cli BGSAVE

# Wait for save to complete
while [ "$(redis-cli LASTSAVE)" == "$LAST_SAVE" ]; do
    sleep 1
done

# Copy RDB with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp ${REDIS_DIR}/dump.rdb ${BACKUP_DIR}/dump_${TIMESTAMP}.rdb

# Optional: Upload to S3
aws s3 cp ${BACKUP_DIR}/dump_${TIMESTAMP}.rdb ${S3_BUCKET}/

# Cleanup old backups
find ${BACKUP_DIR} -name "dump_*.rdb" -mtime +${RETENTION_DAYS} -delete

echo "Backup completed: dump_${TIMESTAMP}.rdb"
```

```python
# Correct 7: Backup from replica (recommended for production)
def backup_from_replica(replica_host, replica_port=6379):
    """
    Take backups from replica to avoid impacting primary.
    Fork for BGSAVE can cause latency spike on primary.
    """
    replica = redis.Redis(host=replica_host, port=replica_port)

    # Verify this is actually a replica
    info = replica.info("replication")
    if info["role"] != "slave":
        raise Exception("Target is not a replica!")

    # Check replication lag
    lag = info.get("master_repl_offset", 0) - info.get("slave_repl_offset", 0)
    if lag > 1000000:  # 1MB lag threshold
        print(f"Warning: Replica lag is {lag} bytes")

    # Trigger backup on replica
    replica.bgsave()

    # Wait and copy...
    print("Backup triggered on replica")
```

```python
# Correct 8: Verify backup integrity
def verify_backup(backup_path):
    """Verify RDB backup file integrity"""
    import subprocess

    # Use redis-check-rdb tool
    result = subprocess.run(
        ["redis-check-rdb", backup_path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Backup verified: {backup_path}")
        return True
    else:
        print(f"Backup corrupted: {result.stderr}")
        return False
```

Reference: [Redis RDB Persistence](https://redis.io/docs/management/persistence/#rdb-advantages)
