---
id: backup-strategies
name: "Backup Strategies"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Backup Strategies

## Overview

Backup strategies ensure data protection, business continuity, and disaster recovery capabilities. This methodology covers backup types, retention policies, automation, testing, and recovery procedures across various infrastructure types.

## When to Use

- Setting up data protection for applications
- Implementing disaster recovery (DR) plans
- Meeting compliance requirements (GDPR, HIPAA)
- Protecting against ransomware and data loss
- Planning infrastructure migrations

## Process/Steps

### 1. Backup Fundamentals

**Backup Types:**
```yaml
backup_types:
  full_backup:
    description: "Complete copy of all data"
    pros: ["Fast recovery", "Self-contained"]
    cons: ["Storage intensive", "Time consuming"]
    frequency: "Weekly or monthly"

  incremental_backup:
    description: "Only changes since last backup"
    pros: ["Fast", "Storage efficient"]
    cons: ["Slower recovery", "Chain dependency"]
    frequency: "Daily or hourly"

  differential_backup:
    description: "Changes since last full backup"
    pros: ["Faster than full", "Easier recovery than incremental"]
    cons: ["Growing size over time"]
    frequency: "Daily"

  snapshot:
    description: "Point-in-time copy"
    pros: ["Instant", "Space efficient (COW)"]
    cons: ["Same storage system risk"]
    frequency: "Hourly or on-demand"

  continuous_replication:
    description: "Real-time data sync"
    pros: ["Near-zero RPO"]
    cons: ["Complex", "Expensive"]
    frequency: "Continuous"
```

**3-2-1 Backup Rule:**
```
3 copies of data
├── 1 primary (production)
├── 1 local backup
└── 1 offsite backup

2 different media types
├── Disk storage
└── Object storage / tape

1 offsite copy
└── Different geographic location
```

### 2. Database Backups

**PostgreSQL:**
```bash
#!/bin/bash
# postgres_backup.sh

DB_NAME="mydb"
BACKUP_DIR="/var/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Full backup with pg_dump
pg_dump -h localhost -U postgres -Fc $DB_NAME > \
  "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Parallel dump for large databases
pg_dump -h localhost -U postgres -Fc -j 4 $DB_NAME > \
  "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"

# Base backup for PITR (Point-in-Time Recovery)
pg_basebackup -h localhost -U replication -D "$BACKUP_DIR/base_$TIMESTAMP" \
  -Ft -z -P -X stream

# Upload to S3
aws s3 cp "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump" \
  "s3://backups-bucket/postgres/${DB_NAME}/"

# Cleanup old backups
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete
```

**MySQL/MariaDB:**
```bash
#!/bin/bash
# mysql_backup.sh

DB_NAME="mydb"
BACKUP_DIR="/var/backups/mysql"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Full backup with mysqldump
mysqldump -u root -p"$MYSQL_PASSWORD" \
  --single-transaction \
  --routines \
  --triggers \
  --quick \
  $DB_NAME | gzip > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

# XtraBackup for large databases (no locking)
xtrabackup --backup --target-dir="$BACKUP_DIR/xtrabackup_$TIMESTAMP" \
  --user=root --password="$MYSQL_PASSWORD"

# Prepare backup
xtrabackup --prepare --target-dir="$BACKUP_DIR/xtrabackup_$TIMESTAMP"

# Incremental backup
xtrabackup --backup --target-dir="$BACKUP_DIR/inc_$TIMESTAMP" \
  --incremental-basedir="$BACKUP_DIR/xtrabackup_base" \
  --user=root --password="$MYSQL_PASSWORD"
```

**MongoDB:**
```bash
#!/bin/bash
# mongodb_backup.sh

BACKUP_DIR="/var/backups/mongodb"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# mongodump
mongodump --uri="mongodb://localhost:27017" \
  --out="$BACKUP_DIR/$TIMESTAMP" \
  --gzip

# For replica set with oplog
mongodump --uri="mongodb://localhost:27017" \
  --out="$BACKUP_DIR/$TIMESTAMP" \
  --oplog \
  --gzip

# Archive format
mongodump --uri="mongodb://localhost:27017" \
  --archive="$BACKUP_DIR/backup_$TIMESTAMP.gz" \
  --gzip
```

### 3. File System Backups

**Restic (Modern Backup Tool):**
```bash
# Initialize repository
restic init --repo s3:s3.amazonaws.com/backup-bucket

# Backup with exclude patterns
restic backup /var/www /etc \
  --repo s3:s3.amazonaws.com/backup-bucket \
  --exclude="*.log" \
  --exclude="node_modules" \
  --exclude=".git" \
  --tag production

# List snapshots
restic snapshots --repo s3:s3.amazonaws.com/backup-bucket

# Restore
restic restore latest --repo s3:s3.amazonaws.com/backup-bucket \
  --target /restore

# Restore specific files
restic restore latest --repo s3:s3.amazonaws.com/backup-bucket \
  --target /restore \
  --include "/var/www/config.php"

# Prune old backups
restic forget --repo s3:s3.amazonaws.com/backup-bucket \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune
```

**BorgBackup:**
```bash
# Initialize repository
borg init --encryption=repokey /backup/borg-repo

# Create backup
borg create --stats --progress \
  /backup/borg-repo::'{hostname}-{now}' \
  /var/www /etc \
  --exclude '*.log' \
  --exclude 'node_modules'

# List archives
borg list /backup/borg-repo

# Restore
borg extract /backup/borg-repo::archive-name

# Prune
borg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=12 \
  /backup/borg-repo
```

**Rsync:**
```bash
# Basic rsync backup
rsync -avz --delete \
  /var/www/ \
  user@backup-server:/backups/www/

# With bandwidth limit and exclude
rsync -avz --delete \
  --bwlimit=10000 \
  --exclude='*.log' \
  --exclude='cache/*' \
  /var/www/ \
  user@backup-server:/backups/www/

# Incremental with hard links
rsync -avz --delete \
  --link-dest=/backups/www/latest \
  /var/www/ \
  user@backup-server:/backups/www/$(date +%Y%m%d)/

# Create 'latest' symlink
ssh user@backup-server "ln -snf /backups/www/$(date +%Y%m%d) /backups/www/latest"
```

### 4. Kubernetes Backups

**Velero:**
```bash
# Install Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.8.0 \
  --bucket velero-backups \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1 \
  --secret-file ./credentials-velero

# Create backup
velero backup create my-backup \
  --include-namespaces myapp \
  --include-resources pods,deployments,services,configmaps,secrets

# Schedule backup
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces myapp \
  --ttl 720h

# Restore
velero restore create --from-backup my-backup

# Restore to different namespace
velero restore create --from-backup my-backup \
  --namespace-mappings myapp:myapp-restored
```

**Velero Configuration:**
```yaml
# Backup with resource filter
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: myapp-backup
  namespace: velero
spec:
  includedNamespaces:
    - myapp
    - myapp-db
  includedResources:
    - pods
    - deployments
    - services
    - configmaps
    - secrets
    - persistentvolumeclaims
  excludedResources:
    - events
  labelSelector:
    matchLabels:
      app: myapp
  storageLocation: default
  volumeSnapshotLocations:
    - default
  ttl: 720h0m0s

---
# Scheduled backup
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces:
      - myapp
    ttl: 720h0m0s
```

### 5. Cloud Backups

**AWS Backup:**
```hcl
# Terraform AWS Backup configuration

resource "aws_backup_vault" "main" {
  name = "main-backup-vault"

  tags = {
    Environment = "production"
  }
}

resource "aws_backup_plan" "daily" {
  name = "daily-backup-plan"

  rule {
    rule_name         = "daily-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"

    lifecycle {
      cold_storage_after = 30
      delete_after       = 365
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr_region.arn
      lifecycle {
        delete_after = 365
      }
    }
  }

  rule {
    rule_name         = "weekly-backup"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 ? * SUN *)"

    lifecycle {
      cold_storage_after = 90
      delete_after       = 730
    }
  }
}

resource "aws_backup_selection" "databases" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "database-selection"
  plan_id      = aws_backup_plan.daily.id

  resources = [
    "arn:aws:rds:*:*:db:*",
    "arn:aws:dynamodb:*:*:table/*"
  ]

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}
```

**S3 Versioning and Lifecycle:**
```hcl
resource "aws_s3_bucket" "backups" {
  bucket = "company-backups"
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    id     = "backup-lifecycle"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 730
    }
  }
}

resource "aws_s3_bucket_replication_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id
  role   = aws_iam_role.replication.arn

  rule {
    id     = "cross-region-replication"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.backups_dr.arn
      storage_class = "STANDARD_IA"
    }
  }
}
```

### 6. Backup Monitoring and Testing

**Backup Verification Script:**
```bash
#!/bin/bash
# verify_backup.sh

BACKUP_PATH="$1"
VERIFY_DIR="/tmp/backup_verify"
ALERT_EMAIL="ops@example.com"

# Cleanup
rm -rf "$VERIFY_DIR"
mkdir -p "$VERIFY_DIR"

# Test restoration
echo "Testing backup restoration..."
if pg_restore -l "$BACKUP_PATH" > /dev/null 2>&1; then
    echo "Backup file is valid"

    # Full restore test
    pg_restore -d backup_test "$BACKUP_PATH"

    # Verify data integrity
    EXPECTED_TABLES=50
    ACTUAL_TABLES=$(psql -d backup_test -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public'")

    if [ "$ACTUAL_TABLES" -ge "$EXPECTED_TABLES" ]; then
        echo "Data integrity check passed"
    else
        echo "Data integrity check failed"
        mail -s "Backup Verification Failed" "$ALERT_EMAIL" <<< "Table count mismatch"
        exit 1
    fi
else
    echo "Backup file is corrupted"
    mail -s "Backup Verification Failed" "$ALERT_EMAIL" <<< "Backup file corrupted"
    exit 1
fi

# Cleanup test database
psql -c "DROP DATABASE backup_test"
```

**Monitoring with Prometheus:**
```yaml
# prometheus-rules.yaml
groups:
  - name: backup-alerts
    rules:
      - alert: BackupNotRecent
        expr: time() - backup_last_success_timestamp > 86400
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "Backup is more than 24 hours old"
          description: "Last successful backup was {{ humanizeTimestamp $value }}"

      - alert: BackupFailed
        expr: backup_last_status == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Backup job failed"

      - alert: BackupSizeDrop
        expr: (backup_size_bytes - backup_size_bytes offset 1d) / backup_size_bytes offset 1d < -0.5
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Backup size dropped by more than 50%"
```

### 7. Disaster Recovery

**DR Runbook:**
```yaml
disaster_recovery:
  rto: 4_hours  # Recovery Time Objective
  rpo: 1_hour   # Recovery Point Objective

  scenarios:
    database_corruption:
      detection: "Automated monitoring alert"
      steps:
        - stop_application_writes
        - identify_corruption_time
        - restore_from_point_in_time
        - verify_data_integrity
        - resume_operations
      estimated_time: 2_hours

    region_outage:
      detection: "AWS Health Dashboard + monitoring"
      steps:
        - activate_dns_failover
        - verify_dr_region_databases
        - scale_dr_region_compute
        - update_configuration
        - resume_operations
      estimated_time: 4_hours

    ransomware:
      detection: "Security alert + file integrity monitoring"
      steps:
        - isolate_affected_systems
        - identify_attack_vector
        - restore_from_air_gapped_backup
        - security_hardening
        - resume_operations
      estimated_time: 8_hours

  testing_schedule:
    full_dr_test: quarterly
    backup_restore_test: monthly
    runbook_review: quarterly
```

## Best Practices

### Planning
1. **Define RTO/RPO** - Know your requirements
2. **Document everything** - Runbooks, procedures
3. **Test regularly** - Untested backups are not backups
4. **Automate** - Reduce human error

### Storage
1. **3-2-1 rule** - Multiple copies, locations
2. **Encryption** - Encrypt backups at rest
3. **Immutable backups** - Protect against ransomware
4. **Retention policies** - Balance cost and compliance

### Operations
1. **Monitor backup jobs** - Alert on failures
2. **Verify integrity** - Regular restore tests
3. **Version backups** - Keep multiple generations
4. **Log everything** - Audit trail

### Security
1. **Encrypt in transit** - TLS for transfers
2. **Access control** - Least privilege
3. **Separate credentials** - Backup-specific access
4. **Air-gapped copies** - For critical data

## Templates/Examples

### Backup Policy Document

```markdown
# Backup Policy

## Scope
This policy covers all production systems and databases.

## Backup Schedule
| System | Type | Frequency | Retention |
|--------|------|-----------|-----------|
| PostgreSQL | Full | Daily 02:00 UTC | 30 days |
| PostgreSQL | WAL | Continuous | 7 days |
| MongoDB | Full | Daily 03:00 UTC | 30 days |
| Application Files | Incremental | Hourly | 7 days |
| Application Files | Full | Weekly Sunday | 90 days |

## Storage Locations
- Primary: AWS S3 us-east-1
- Secondary: AWS S3 eu-west-1 (cross-region replication)
- Archive: AWS Glacier (after 90 days)

## Recovery Objectives
- RTO: 4 hours
- RPO: 1 hour

## Testing Schedule
- Monthly: Automated restore test
- Quarterly: Full DR test
- Annually: DR documentation review

## Responsibilities
- DevOps Team: Backup configuration and monitoring
- Security Team: Encryption key management
- Management: Policy approval and compliance
```

### Cron Jobs for Backups

```bash
# /etc/cron.d/backups

# Database backups
0 2 * * * postgres /opt/scripts/backup_postgres.sh >> /var/log/backup/postgres.log 2>&1
0 3 * * * root /opt/scripts/backup_mysql.sh >> /var/log/backup/mysql.log 2>&1

# File backups
0 * * * * root /opt/scripts/backup_files_hourly.sh >> /var/log/backup/files.log 2>&1
0 4 * * 0 root /opt/scripts/backup_files_weekly.sh >> /var/log/backup/files.log 2>&1

# Verification
0 6 * * * root /opt/scripts/verify_backups.sh >> /var/log/backup/verify.log 2>&1

# Cleanup
0 5 * * * root /opt/scripts/cleanup_old_backups.sh >> /var/log/backup/cleanup.log 2>&1
```

## References

- [Restic Documentation](https://restic.readthedocs.io/)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/)
- [Velero Documentation](https://velero.io/docs/)
- [AWS Backup](https://docs.aws.amazon.com/aws-backup/)
- [PostgreSQL Backup and Recovery](https://www.postgresql.org/docs/current/backup.html)
