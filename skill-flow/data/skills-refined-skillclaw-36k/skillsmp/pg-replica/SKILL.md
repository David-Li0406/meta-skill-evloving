---
name: pg-replica
description: Manage the PostgreSQL 17 read replica on hal9000. Use this skill when asked to check PostgreSQL status, run queries on the replica, view replication lag, manage WAL archives, or interact with the hal9000 database. Always use the helper scripts in the scripts/ directory rather than constructing SSH commands manually.
---

# PostgreSQL 17 Replica Management

Manage the read replica of Quantierra's PostgreSQL 17 database running on hal9000.

## Quick Reference

| Task                                | Script                               |
| ----------------------------------- | ------------------------------------ |
| Quick status                        | `pg17-status`                        |
| Full status (service + replication) | `pg17-full-status`                   |
| Replication lag                     | `pg17-lag`                           |
| Run query                           | `pg17-query "SELECT ..." [database]` |
| List databases                      | `pg17-databases`                     |
| List tables                         | `pg17-tables <database>`             |
| View logs                           | `pg17-logs [lines]`                  |
| WAL archive status                  | `pg17-wal-status`                    |
| Active connections                  | `pg17-connections`                   |
| ZFS snapshots                       | `pg17-snapshots`                     |

## Usage

**Always use the helper scripts** located in `.claude/skills/pg-replica/scripts/`. These scripts handle SSH connection, proper port (5432), and host (localhost) configuration automatically.

```bash
# Check replica status
.claude/skills/pg-replica/scripts/pg17-status

# Run a query
.claude/skills/pg-replica/scripts/pg17-query "SELECT count(*) FROM users" quantierra

# View last 100 lines of logs
.claude/skills/pg-replica/scripts/pg17-logs 100
```

## Remote Commands (on hal9000)

For operations not covered by scripts, SSH to hal9000 and use these system commands:

| Command                                      | Description                             |
| -------------------------------------------- | --------------------------------------- |
| `sudo pg17-wal-sync`                         | Trigger WAL sync from S3                |
| `sudo pg17-create-snapshot`                  | Create ZFS snapshot                     |
| `sudo pg17-rollback`                         | Rollback to latest snapshot             |
| `sudo pg17-activate`                         | Promote to writable (stops replication) |
| `sudo systemctl <action> postgresql-replica` | Service control (start/stop/restart)    |

## Switching Between Standby and Read/Write Modes

The systemd service always starts in **standby mode** (it creates `standby.signal` on startup). To switch modes, you must manage postgres manually.

### Promote to Read/Write (stop replication)

```bash
# Stop the systemd service
ssh hal9000 "sudo systemctl stop postgresql-replica"

# Remove standby.signal and start postgres manually
ssh hal9000 "sudo rm -f /storage-fast/pg_base/standby.signal && sudo -u postgres /run/current-system/sw/bin/postgres -D /storage-fast/pg_base &"
```

### Return to Standby Mode

```bash
# Stop the manual postgres process
ssh hal9000 "sudo pkill -u postgres postgres"

# Restart the systemd service (will recreate standby.signal)
ssh hal9000 "sudo systemctl start postgresql-replica"
```

**Note:** The `pg17-activate` script attempts to promote while the service is running, but this conflicts with the pre-start script. For reliable mode switching, use the manual steps above.

## Architecture

See [architecture.md](architecture.md) for detailed infrastructure information.
