# Common Workflows

Complete step-by-step workflows for common Frappe bench operations.

## Table of Contents

- [Fresh Install Workflow](#fresh-install-workflow)
- [Restore from Production Backup Workflow](#restore-from-production-backup-workflow)
- [Quick Reinstall Apps Workflow](#quick-reinstall-apps-workflow)
- [Large Database Restore Workflow](#large-database-restore-workflow)
- [New App Development Workflow](#new-app-development-workflow)
- [Production Deployment Preparation](#production-deployment-preparation)

---

## Fresh Install Workflow

Complete setup of a new development environment from scratch.

### Steps

#### 1. Drop Existing Site (if exists)
```bash
bench drop-site development.localhost --db-root-password 123
```

#### 2. Create New Site
```bash
bench new-site development.localhost --admin-password admin --db-root-password 123
```

#### 3. Install Apps
```bash
bench --site development.localhost install-app soldamundo tweaks
```

Or install one at a time:
```bash
bench --site development.localhost install-app soldamundo
bench --site development.localhost install-app tweaks
```

#### 4. Enable Developer Mode
```bash
bench --site development.localhost set-config developer_mode 1
```

#### 5. Run Migrations
```bash
bench --site development.localhost migrate
```

#### 6. Clear Cache and Build
```bash
bench clear-cache
bench build
```

#### 7. Start Server
```bash
bench start
```

### Verification

Visit http://localhost:8000 and login with:
- **Username:** Administrator
- **Password:** admin

---

## Restore from Production Backup Workflow

Restore a production database backup to development environment.

### Prerequisites

- Production backup files in `backups/` directory:
  - Database: `YYYYMMDD_HHMMSS-sitename-database.sql.gz`
  - Files (optional): `YYYYMMDD_HHMMSS-sitename-files.tar`
  - Site config: `YYYYMMDD_HHMMSS-sitename-site_config_backup.json`

### Steps

#### 1. Check Database Size (Required)

```bash
# Check compressed backup size
ls -lh backups/*.sql.gz

# Estimate uncompressed size (typically 8-12x compressed)
gzip -l backups/20251224_151238-gruposoldamundo_frappe_cloud-database.sql.gz
```

**Memory requirements:**
- < 100MB: No special configuration needed
- 100MB - 1GB: Set max_allowed_packet to 128MB
- 1GB - 5GB: Set max_allowed_packet to 512MB
- > 5GB: Follow [Large Database Restore Workflow](#large-database-restore-workflow)

#### 2. Configure MariaDB Memory (Required for Backups > 100MB)

```bash
# Check current settings
mariadb -h mariadb -u root -p123 -e "SHOW VARIABLES LIKE 'max_allowed_packet';"

# Set increased memory limits
mariadb -h mariadb -u root -p123 <<EOF
SET GLOBAL max_allowed_packet=536870912;
SHOW VARIABLES LIKE 'max_allowed_packet';
EOF
```

**Why:** Production databases require increased packet size to prevent "packet too large" errors during restore.

#### 3. Drop Existing Site (For Fresh Restore)
```bash
bench drop-site development.localhost --db-root-password 123
```

**Skip this step** if restoring to existing site (encryption_key already correct).

#### 4. Create New Site (Only if Dropped)
```bash
bench new-site development.localhost --admin-password admin --db-root-password 123
```

**Important:** This creates a new encryption_key that won't match the backup.

#### 5. Set Encryption Key from Backup (Only for Recreated Sites)

Extract encryption_key from site_config_backup.json:
```bash
cat backups/20251224_151238-gruposoldamundo_frappe_cloud-site_config_backup.json
```

Look for the `encryption_key` field and copy its value.

Set it on the new site:
```bash
bench --site development.localhost set-config encryption_key "your-encryption-key-from-backup"
```

**Critical:** Must be done BEFORE restoring database, or encrypted fields will be unreadable.

**Skip this step** if restoring to existing site with correct encryption_key.

#### 6. Restore Database and Files
```bash
# Database and files
bench --site development.localhost restore \
    --db-root-password 123 \
    "backups/20251224_151238-gruposoldamundo_frappe_cloud-database.sql.gz" \
    --with-public-files "backups/20251224_151238-gruposoldamundo_frappe_cloud-files.tar"

# Database only (faster)
bench --site development.localhost restore \
    --db-root-password 123 \
    "backups/20251224_151238-gruposoldamundo_frappe_cloud-database.sql.gz"
```

#### 7. Run Migrations (Required)
```bash
bench --site development.localhost migrate
```

**Always run migrations** after restore to sync schema with current app versions.

#### 8. Set Admin Password (Required)
```bash
bench --site development.localhost set-admin-password admin
```

**Why:** Production backups have production passwords. Reset to known development password.

#### 9. Clear Cache and Start
```bash
bench clear-cache
bench start
```

### Post-Restore Checks

1. **Login:** Verify admin password works (from backup, not "admin")
2. **Data:** Check that key records are present
3. **Encrypted fields:** Verify passwords/API keys are accessible
4. **Files:** Check uploaded files are accessible (if restored with-public-files)

### Troubleshooting

**"Packet too large" error:**
- Increase `max_allowed_packet` as shown in step 1

**"Can't decrypt" errors:**
- Verify encryption_key was set correctly before restore
- Check site_config.json has correct encryption_key

**"Out of memory" errors:**
- Increase `max_allowed_packet` further
- Check available system memory

---

## Quick Reinstall Apps Workflow

Reinstall apps without dropping the site (preserves custom configuration).

### Steps

#### 1. Uninstall Apps
```bash
bench --site development.localhost uninstall-app soldamundo --yes --no-backup
bench --site development.localhost uninstall-app tweaks --yes --no-backup
```

#### 2. Install Apps
```bash
bench --site development.localhost install-app soldamundo
bench --site development.localhost install-app tweaks
```

#### 3. Run Migrations
```bash
bench --site development.localhost migrate
```

#### 4. Clear Cache
```bash
bench clear-cache
```

#### 5. Restart Server
```bash
pkill -SIGINT -f bench
bench start
```

### When to Use

- Testing app installation process
- Fixing corrupted app data
- Resetting app to clean state
- Preserving site configuration

### Limitations

- Doesn't reset site configuration
- Doesn't clean up orphaned data
- May leave residual custom fields

For complete reset, use [Fresh Install Workflow](#fresh-install-workflow).

---

## Large Database Restore Workflow

Specialized workflow for restoring very large databases (>5GB).

### Prerequisites

- Production backup (database.sql.gz)
- Sufficient disk space (3x compressed file size)
- Sufficient memory (8GB+ recommended)

### Steps

#### 1. Stop Bench Server
```bash
pkill -SIGINT -f bench
pkill -SIGINT -f socketio
```

#### 2. Configure MariaDB

Connect as root:
```bash
mariadb -h mariadb -u root -p123
```

Set maximum limits:
```sql
-- Increase packet size to 1GB
SET GLOBAL max_allowed_packet=1073741824;

-- Increase transaction isolation timeout
SET GLOBAL innodb_lock_wait_timeout=600;

-- View settings
SHOW VARIABLES LIKE 'max_allowed_packet';
SHOW VARIABLES LIKE 'innodb_lock_wait_timeout';

EXIT;
```

#### 3. Create Fresh Site
```bash
bench drop-site development.localhost --db-root-password 123
bench new-site development.localhost --admin-password admin --db-root-password 123
```

#### 4. Set Encryption Key
```bash
# Extract from backup
cat backups/YYYYMMDD_HHMMSS-sitename-site_config_backup.json

# Set on new site
bench --site development.localhost set-config encryption_key "key-from-backup"
```

#### 5. Restore Database (No Files Yet)
```bash
bench --site development.localhost restore \
    --db-root-password 123 \
    "backups/YYYYMMDD_HHMMSS-sitename-database.sql.gz"
```

**Note:** Restore can take 30+ minutes for large databases. Be patient.

#### 6. Optimize Database (Optional)
```bash
bench --site development.localhost mariadb
```

In MariaDB:
```sql
-- Analyze tables
ANALYZE TABLE `tabDocType`;

-- Optimize key tables
OPTIMIZE TABLE `tabUser`;
OPTIMIZE TABLE `tabItem`;

EXIT;
```

#### 7. Restore Files (if needed)
```bash
# Extract files manually
cd sites/development.localhost/public
tar -xzf /path/to/backups/YYYYMMDD_HHMMSS-sitename-files.tar

# Fix permissions
cd ../../..
bench setup requirements
```

#### 8. Run Migrations
```bash
bench --site development.localhost migrate --skip-search-index
```

Use `--skip-search-index` for faster migration on large databases.

#### 9. Rebuild Search Index (Optional)
```bash
bench --site development.localhost build-search-index
```

Can be done later if time-consuming.

#### 10. Clear Cache and Start
```bash
bench clear-cache
bench start
```

### Performance Tips

**Before restore:**
- Close unnecessary applications
- Ensure sufficient swap space
- Monitor disk space during restore

**After restore:**
- Rebuild search index during off-hours
- Consider table partitioning for huge tables
- Run ANALYZE TABLE periodically

---

## New App Development Workflow

Setting up environment for developing a new Frappe app.

### Steps

#### 1. Create App
```bash
bench new-app myapp
```

Follow prompts to enter:
- App name
- App description
- Author
- Email
- License

#### 2. Install App to Site
```bash
bench --site development.localhost install-app myapp
```

#### 3. Enable Developer Mode
```bash
bench --site development.localhost set-config developer_mode 1
bench --site development.localhost clear-cache
```

#### 4. Create DocTypes via UI

Visit http://localhost:8000/app/doctype/new and create your doctypes.

#### 5. Set Up Git Repository
```bash
cd apps/myapp
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/myapp.git
git push -u origin main
```

#### 6. Development Loop

```bash
# Terminal 1: Run server
bench start

# Terminal 2: Watch for changes
bench watch

# Make code changes
# ... edit files ...

# Changes auto-rebuild with bench watch
# Refresh browser to see changes
```

#### 7. Test Changes
```bash
# Write tests in tests/ directory
# Run tests
bench --site development.localhost run-tests --app myapp
```

### Best Practices

- **Use developer mode:** Auto-reloads DocTypes
- **Run bench watch:** Auto-rebuilds assets
- **Test frequently:** Run tests before committing
- **Clear cache:** When changes don't reflect
- **Version control:** Commit small, logical changes

---

## Production Deployment Preparation

Preparing development code for production deployment.

### Pre-Deployment Checklist

#### 1. Run Full Test Suite
```bash
bench --site development.localhost run-tests --app myapp --coverage
```

Ensure all tests pass and coverage is adequate.

#### 2. Disable Developer Mode
```bash
bench --site development.localhost set-config developer_mode 0
```

#### 3. Build Production Assets
```bash
bench build --production
```

Minifies and optimizes JavaScript/CSS.

#### 4. Check for Errors
```bash
bench --site development.localhost doctor
```

Verify no configuration issues.

#### 5. Create Migration Scripts

If database changes were made:
```bash
cd apps/myapp/myapp/patches
# Create patch file
# Test patch
bench --site development.localhost run-patch myapp.patches.YYYY.patch_name
```

#### 6. Document Changes

Create CHANGELOG.md or update documentation:
- New features
- Breaking changes
- Migration notes
- Configuration changes

#### 7. Version Bump

Update version in:
- `apps/myapp/myapp/__init__.py`
- `apps/myapp/package.json` (if applicable)
- `apps/myapp/setup.py` or `pyproject.toml`

#### 8. Create Git Tag
```bash
cd apps/myapp
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

#### 9. Create Backup of Current Production
```bash
# On production server
bench --site production.site backup --backup-path "backups/pre-deployment"
```

#### 10. Test Update Process

In development:
```bash
# Simulate production update
bench update --apps myapp
bench --site development.localhost migrate
```

### Deployment Steps (On Production)

```bash
# 1. Maintenance mode
bench --site production.site set-maintenance-mode on

# 2. Backup
bench --site production.site backup

# 3. Pull updates
bench update --apps myapp

# 4. Run migrations
bench --site production.site migrate

# 5. Build assets
bench build --production

# 6. Clear cache
bench clear-cache

# 7. Restart
sudo systemctl restart supervisor
sudo systemctl restart nginx

# 8. Exit maintenance mode
bench --site production.site set-maintenance-mode off

# 9. Verify
# Check site is accessible
# Check key functionality
# Monitor error logs
```

### Rollback Plan

If deployment fails:
```bash
# 1. Maintenance mode
bench --site production.site set-maintenance-mode on

# 2. Restore backup
bench --site production.site restore "backup-file.sql.gz"

# 3. Revert code
cd apps/myapp
git checkout v0.9.0  # previous version

# 4. Rebuild
bench build --production

# 5. Clear cache and restart
bench clear-cache
sudo systemctl restart supervisor

# 6. Exit maintenance
bench --site production.site set-maintenance-mode off
```

---

## Quick Reference

| Workflow | Time Estimate | Complexity | Risk Level |
|----------|---------------|------------|------------|
| Fresh Install | 10-15 min | Low | Low |
| Restore Production | 30-60 min | Medium | Medium |
| Quick Reinstall | 5-10 min | Low | Low |
| Large DB Restore | 1-3 hours | High | Medium |
| New App Setup | 15-20 min | Low | Low |
| Production Deploy | 20-40 min | High | High |

### When to Use Which Workflow

- **Complete reset needed:** Fresh Install
- **Production data needed:** Restore from Production
- **App testing:** Quick Reinstall
- **Large production data:** Large Database Restore
- **Starting new project:** New App Development
- **Going live:** Production Deployment Preparation
