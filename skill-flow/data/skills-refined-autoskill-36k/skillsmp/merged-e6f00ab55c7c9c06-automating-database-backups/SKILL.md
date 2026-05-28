---
name: automating-database-backups
description: Automate database backup processes with scheduling, compression, and encryption for PostgreSQL, MySQL, MongoDB, and SQLite.
---

# Overview

This skill streamlines the creation of database backup solutions. It generates scripts, configures schedules, and provides comprehensive restore procedures, ensuring data safety and efficient recovery.

## How It Works

1. **Analyze Requirements**: Determine the database type (PostgreSQL, MySQL, MongoDB, or SQLite) and backup requirements (frequency, retention).
2. **Generate Scripts**: Create backup scripts with compression and encryption.
3. **Schedule Backups**: Set up cron jobs for automated, scheduled backups.
4. **Document Restore**: Generate clear, concise restore procedures.

## When to Use This Skill

This skill activates when you need to:
- Create a backup schedule for a database.
- Automate the database backup process.
- Generate scripts for database restoration.
- Implement a disaster recovery plan for a database.

## Examples

### Example 1: Setting up Daily Backups for PostgreSQL

User request: "Create daily backups for my PostgreSQL database."

The skill will:
1. Generate a `pg_dump` script with compression and encryption.
2. Create a cron job to run the backup script daily.

### Example 2: Automating Weekly Backups for MongoDB

User request: "Automate weekly backups for my MongoDB database."

The skill will:
1. Generate a `mongodump` script with compression and encryption.
2. Create a cron job to run the backup script weekly and implement a retention policy.

## Best Practices

- **Retention Policies**: Implement clear retention policies to manage storage space.
- **Testing Restores**: Regularly test restore procedures to ensure data integrity.
- **Secure Storage**: Store backups in secure, encrypted locations, preferably offsite.

## Integration

This skill can integrate with cloud storage plugins (S3, GCS, Azure) for offsite backup storage and monitoring plugins for backup success/failure alerts.

## Quick Start

### PostgreSQL Backup
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/postgresql"
DB_NAME="<database_name>"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"

pg_dump -h <host> -U <user> -d "$DB_NAME" \
  --format=custom \
  --compress=9 \
  --file="$BACKUP_FILE"

# Encrypt with GPG (optional)
gpg --symmetric --cipher-algo AES256 --batch --passphrase-file /etc/backup.key "$BACKUP_FILE"
rm "$BACKUP_FILE"
```

### MySQL Backup
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/mysql"
DB_NAME="<database_name>"
DATE=$(date +%Y%m%d_%H%M%S)

mysqldump -h <host> -u <user> -p"<password>" \
  --single-transaction \
  --routines \
  --triggers \
  "$DB_NAME" | gzip > "${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"
```

### MongoDB Backup
```bash
#!/bin/bash
mongodump --uri="mongodb://<host>:<port" \
  --db=<database_name> \
  --out=/var/backups/mongodb/$(date +%Y%m%d_%H%M%S) \
  --gzip
```

## Instructions

### Step 1: Gather Requirements
Ask the user for:
- Database type (PostgreSQL, MySQL, MongoDB, SQLite)
- Database connection details (host, port, database name)
- Backup schedule (cron expression or frequency)
- Retention policy (days to keep)
- Encryption requirement (yes/no)
- Backup destination (local path, S3, GCS)

### Step 2: Generate Backup Script
Use a script generator to create a customized backup script.

### Step 3: Schedule with Cron
Create cron entries for the backup scripts.

### Step 4: Validate Backup
After backup completes, validate integrity.

### Step 5: Generate Restore Procedure
Create matching restore script.

## Cron Schedule Reference

| Schedule | Cron Expression | Description |
|----------|-----------------|-------------|
| Daily 2 AM | `0 2 * * *` | Low-traffic window |
| Every 6 hours | `0 */6 * * *` | Frequent backups |
| Weekly Sunday | `0 2 * * 0` | Weekly full backup |
| Monthly 1st | `0 2 1 * *` | Monthly archive |

## Retention Policy Example

```bash
# Keep daily backups for 7 days
# Keep weekly backups for 4 weeks
# Keep monthly backups for 12 months

find /var/backups -name "*.gz" -mtime +7 -delete  # Daily cleanup
find /var/backups/weekly -mtime +28 -delete       # Weekly cleanup
find /var/backups/monthly -mtime +365 -delete     # Monthly cleanup
```

## Output

- **Backup Scripts**: Database-specific shell scripts with compression and encryption
- **Cron Entries**: Ready-to-install crontab configurations
- **Restore Scripts**: Matching restore procedures for each backup type
- **Validation Reports**: Integrity check results for backup files

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | DB not running | Check service status |
| Permission denied | Wrong credentials | Verify user has backup privileges |
| Disk full | No space | Check space and clean old backups |
| Lock timeout | Active transactions | Use `--single-transaction` for MySQL |

## Resources

- Backup guides for PostgreSQL, MySQL, MongoDB, and SQLite.
- Security and storage best practices.
- Cron scheduling reference.