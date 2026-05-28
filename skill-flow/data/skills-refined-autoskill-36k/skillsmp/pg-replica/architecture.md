# PostgreSQL Replica Architecture

## Infrastructure

| Component              | Value                                         |
| ---------------------- | --------------------------------------------- |
| **Host**               | hal9000                                       |
| **Service**            | `postgresql-replica.service`                  |
| **Port**               | 5432 (TCP via localhost)                      |
| **PostgreSQL Version** | 17                                            |
| **Data Directory**     | `/storage-fast/pg_base` (ZFS dataset)         |
| **WAL Archive**        | `/mnt/storage20tb/quantierra/wal`             |
| **S3 Source**          | `s3://quantierra-backups/postgresql-archive/` |

## Replication Mode

Archive-based recovery (not streaming replication):

- WAL files are synced from S3 daily at 3 AM via systemd timer
- Local WAL archive is replayed continuously
- Lag depends on S3 sync frequency and WAL generation rate

## Configuration Notes

- **`ignore_invalid_pages = on`**: Required because base backup was a ZFS snapshot (not pg_basebackup). This allows recovery to skip pages that may have inconsistent checksums due to snapshot timing.

## Scheduled Tasks

| Task             | Schedule             |
| ---------------- | -------------------- |
| WAL Sync from S3 | Daily at 3 AM        |
| ZFS Snapshots    | Every 3 days at 4 AM |

## Connection Requirements

When connecting manually (not via helper scripts), always use:

```
Host: localhost (or -h localhost)
Port: 5432 (or -p 5432)
```

**Never**:

- Use `-p 5432` without `-h localhost` (socket path issues)
- Try to find socket files (use TCP via localhost)

## NixOS Module

Configuration: `modules/services/postgresql-replica/`
Host config: `hosts/hal9000/default.nix`
