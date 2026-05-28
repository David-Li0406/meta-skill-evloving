# Backup and Restore

## Create Backup

### Full Backup (Database + Files)
```bash
bench --site development.localhost backup --backup-path "backups"
```

Creates a complete backup including database and uploaded files.

**Output files:**
- `YYYYMMDD_HHMMSS-sitename-database.sql.gz` - Compressed database dump
- `YYYYMMDD_HHMMSS-sitename-files.tar` - Tar archive of uploaded files
- `YYYYMMDD_HHMMSS-sitename-site_config_backup.json` - Site configuration (includes encryption_key)

### Database Only Backup
```bash
bench --site development.localhost backup --only-db --backup-path "backups"
```

Creates only the database backup, skipping files for faster backup.

### Custom Backup Path
```bash
bench --site development.localhost backup --backup-path "/path/to/backups"
```

## Restore from Backup

### Complete Restore Workflow

**Always follow these steps when restoring a backup:**

#### Step 1: Check Database Size
```bash
# Check compressed backup size
ls -lh backups/*.sql.gz

# For uncompressed size estimate (multiply compressed by ~10)
gzip -l backups/20251224_151238-gruposoldamundo_frappe_cloud-database.sql.gz
```

#### Step 2: Configure MariaDB Memory (Required for Large Backups)
```bash
# Check current settings
mariadb -h mariadb -u root -p123 -e "SHOW VARIABLES LIKE 'max_allowed_packet';"

# Set increased memory limits (required for databases > 100MB)
mariadb -h mariadb -u root -p123 -e "SET GLOBAL max_allowed_packet=536870912; SHOW VARIABLES LIKE 'max_allowed_packet';"
```

**Memory guidelines:**
- **max_allowed_packet**: Set to 512MB (536870912) for large restores

#### Step 3: Restore Database
```bash
# Database and files
bench --site development.localhost restore \
    --db-root-password 123 \
    "backups/20251224_151238-gruposoldamundo_frappe_cloud-database.sql.gz" \
    --with-public-files "backups/20251224_151238-gruposoldamundo_frappe_cloud-files.tar"

# Database only
bench --site development.localhost restore \
    --db-root-password 123 \
    "backups/backup-database.sql.gz"
```

#### Step 4: Run Migrations
```bash
# Required after restore to sync schema with current app versions
bench --site development.localhost migrate
```

#### Step 5: Set Admin Password
```bash
# Reset to known password after restore
bench --site development.localhost set-admin-password admin
```

### Quick Restore Commands

For experienced users, combined command:
```bash
# Configure MariaDB
mariadb -h mariadb -u root -p123 -e "SET GLOBAL max_allowed_packet=536870912;"

# Restore, migrate, and set password
cd /workspace/development/frappe-bench && \
bench --site development.localhost restore --db-root-password 123 \
    "backups/20260111_144516-gruposoldamundo_frappe_cloud-database.sql.gz" && \
bench --site development.localhost migrate && \
bench --site development.localhost set-admin-password admin
```

## Important: Encryption Key Handling

When restoring to a **recreated site** (one that was dropped and created again), the new site will have a different `encryption_key`. This will prevent encrypted fields from being decrypted.

**Required steps:**

1. Extract encryption_key from `site_config_backup.json`:
   ```bash
   cat backups/20251224_151238-gruposoldamundo_frappe_cloud-site_config_backup.json
   ```

2. Set the encryption_key on the new site **BEFORE** restoring:
   ```bash
   bench --site development.localhost set-config encryption_key "your-encryption-key-from-backup"
   ```

3. Now restore the database:
   ```bash
   bench --site development.localhost restore \
       --db-root-password 123 \
       "backups/backup-database.sql.gz"
   ```

**Why this matters:** Frappe encrypts sensitive fields (passwords, API keys) in the database. Without the correct encryption_key, these fields cannot be decrypted, causing errors and data loss.

## Backup Locations

### Default Location
```
./sites/development.localhost/private/backups/
```

### Custom Location
Specify with `--backup-path` flag to store backups elsewhere.

## Best Practices

- **Before major changes**: Always create a backup
- **Production backups**: Include both database and files
- **Large databases**: See [database-operations.md](database-operations.md) for MariaDB memory configuration
- **Keep site_config_backup.json**: Essential for encryption_key recovery
- **Test restores**: Periodically test backup restoration to ensure they work
