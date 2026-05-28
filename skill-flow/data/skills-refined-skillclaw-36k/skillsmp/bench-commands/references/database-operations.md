# Database Operations

## Run Migrations

### Standard Migration
```bash
bench --site development.localhost migrate
```

Runs all pending database migrations for installed apps.

### Fast Migration (Skip Search Index)
```bash
bench --site development.localhost migrate --skip-search-index
```

Faster migration by skipping search index rebuild. Recommended during active development.

## Run Specific Patch

```bash
# Run a specific patch
bench --site development.localhost run-patch tweaks.patches.2025.patch_name

# Force re-run a patch
bench --site development.localhost run-patch --force soldamundo.patches.2025.patch_name
```

**Patch format:** `app_name.patches.YYYY.patch_file_name` (without .py extension)

## Access Database Console

### MariaDB Console (Site Context)
```bash
bench --site development.localhost mariadb
```

Opens MariaDB console for the site's database. Automatically connects to the correct database.

### Direct MariaDB Connection (Root)
```bash
mariadb -h mariadb -u root -p123
```

Connects as root user. Use this for:
- Server-wide configuration
- Managing multiple databases
- Setting global variables

### Frappe Python Console
```bash
bench --site development.localhost console
```

Opens an interactive Python console with full Frappe context loaded.

**Common console commands:**
```python
# Get a document
doc = frappe.get_doc("DocType", "name")

# Run SQL queries
frappe.db.sql("SELECT * FROM tabUser LIMIT 5")

# Commit changes
frappe.db.commit()

# Get current site
frappe.local.site
```

## MariaDB Runtime Configuration

**Required before restoring large backups** to prevent memory/packet size errors.

### Connect to MariaDB
```bash
mariadb -h mariadb -u root -p123
```

### Set Maximum Packet Size (512MB)
```sql
-- For large backup/restore operations
SET GLOBAL max_allowed_packet=536870912;

-- View current setting
SHOW VARIABLES LIKE 'max_allowed_packet';
```

**When to use:** Before restoring production backups or working with large databases (>100MB).

**Default:** Usually 16MB or 64MB - too small for large restore operations.

### Exit MariaDB
```sql
EXIT;
```

## Making Configuration Permanent

Runtime settings are **lost when MariaDB container restarts**.

To persist settings, add them to `/workspace/.devcontainer/docker-compose.yml`:

```yaml
services:
    mariadb:
        command:
            - --max_allowed_packet=536870912
```

## Performance Tuning Guidelines

| Database Size | max_allowed_packet | Notes |
|--------------|-------------------|-------|
| < 100MB | Default (16MB) | No tuning needed |
| 100MB - 1GB | 64MB | Minimal tuning |
| 1GB - 5GB | 128MB - 512MB | Moderate tuning |
| > 5GB | 512MB+ | Full tuning required |

## Troubleshooting

### "Access denied for user" after container restart

**Error:**
```
pymysql.err.OperationalError: (1045, "Access denied for user '_xxxxx'@'172.x.x.x' (using password: YES)")
```

**Cause:** When MariaDB container restarts, database users created at runtime are lost while the databases themselves persist. The site_config.json still contains the credentials, but the user no longer exists in MariaDB.

**Solution:**

1. Get database credentials from site config:
```bash
cat sites/development.localhost/site_config.json
# Look for: db_name, db_password
```

2. Recreate the database user:
```bash
mariadb -h mariadb -u root -p123 <<EOF
DROP USER IF EXISTS 'DB_USER'@'%';
CREATE USER 'DB_USER'@'%' IDENTIFIED BY 'DB_PASSWORD';
GRANT ALL PRIVILEGES ON \`DB_NAME\`.* TO 'DB_USER'@'%';
FLUSH PRIVILEGES;
EOF
```

Replace `DB_USER`, `DB_PASSWORD`, and `DB_NAME` with values from site_config.json.

**Example:**
```bash
mariadb -h mariadb -u root -p123 <<EOF
DROP USER IF EXISTS '_54cc49b9a1aab38b'@'%';
CREATE USER '_54cc49b9a1aab38b'@'%' IDENTIFIED BY '1KFLli6XZnKEKcGp';
GRANT ALL PRIVILEGES ON \`_54cc49b9a1aab38b\`.* TO '_54cc49b9a1aab38b'@'%';
FLUSH PRIVILEGES;
EOF
```

3. Retry the failed command (e.g., `bench --site development.localhost migrate`)

### "Packet too large" errors
```sql
SET GLOBAL max_allowed_packet=536870912;
```

### "Lost connection during query"
- Increase max_allowed_packet
- Check available memory
- Restart MariaDB container if needed

## Common Operations

### Check Database Size
```sql
SELECT
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'your_database_name'
GROUP BY table_schema;
```

### Show All Databases
```sql
SHOW DATABASES;
```

### Switch Database
```sql
USE database_name;
```

### Show Tables
```sql
SHOW TABLES;
```
