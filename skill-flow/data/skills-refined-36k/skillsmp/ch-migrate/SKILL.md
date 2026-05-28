---
name: ch-migrate
description: Use when integrating ClickHouse migrations into a project, setting up ch-migrate, creating migration files, bootstrapping ClickHouse databases, or troubleshooting ClickHouse Alembic issues. Triggers on "ClickHouse migration", "ch-migrate", "Alembic ClickHouse", "bootstrap ClickHouse", "migration user", "EXCHANGE TABLES".
---

# ch-migrate: ClickHouse Migration Tool

## Overview

`ch-migrate` is a CLI tool for managing ClickHouse schema migrations built on Alembic. It handles multi-environment configuration, role-based access control, and ClickHouse Cloud compatibility.

**Install:** `uv add clickhouse-alembic` or `pip install clickhouse-alembic`

## CLI Quick Reference

| Command | Description |
|---------|-------------|
| `ch-migrate init [PATH] [--name NAME]` | Initialize project structure |
| `ch-migrate bootstrap ENV [--dry-run]` | Create database, roles, users |
| `ch-migrate new ENV NAME [--table X]` | Create migration (optionally with SQL file) |
| `ch-migrate up ENV [-r REV]` | Apply migrations (default: head, or to REV) |
| `ch-migrate down ENV [-r REV]` | Rollback (default: last, or to REV) |
| `ch-migrate status ENV` | Show current migration state |
| `ch-migrate history ENV` | Show migration history |
| `ch-migrate skill [--user\|--project]` | Install Claude skill for ch-migrate |

**Options for `new`:** `--table NAME`, `--view NAME`, `--dict NAME` create SQL history files organized by object name in `migrations/sql/history/{tables|views|dictionaries}/{object_name}/`.

## Project Structure

```
project/
├── config.yaml           # ClickHouse hosts and settings
├── .env.local            # Secrets (gitignored)
├── alembic.ini           # Alembic configuration
└── migrations/
    ├── env.py            # Alembic environment
    ├── versions/         # Migration Python files
    └── sql/
        ├── bootstrap/    # Custom bootstrap SQL (optional)
        └── history/      # Object-centric SQL versions
            ├── tables/
            ├── views/
            └── dictionaries/
```

## Configuration

### config.yaml

```yaml
project:
  name: my_project

defaults:
  port: 8443                    # 8123 for local HTTP
  secure: true                  # false for local Docker
  admin_user: default
  # Optional users (uncomment to enable):
  # mcp_user_name: mcp_reader   # Read-only for AI tools
  # dict_reader_name: dict_reader

environments:
  dev:
    host: dev.clickhouse.cloud  # or localhost for Docker
    database: my_project_dev
    migration_user: migration_dev
    # aws_region: us-east-1  # Optional: for region-scoped SSM lookups
    # Optional SSM paths (if set, fetches from SSM directly):
    # Supports JSON key extraction: /path/to/param#json_key
    # ssm:
    #   admin_password: /my_project/dev/admin_password
    #   migration_password: /my_project/credentials#password

  staging:
    host: staging.clickhouse.cloud
    database: my_project_staging
    migration_user: migration_staging

  production:
    host: prod.clickhouse.cloud
    database: my_project
    migration_user: migration_prod
```

### .env.local

```bash
# Required
CH_DEV_MIGRATION_PASSWORD=your-migration-password
CH_DEV_ADMIN_PASSWORD=your-admin-password    # For bootstrap only

# Optional (if mcp_user_name configured)
CH_DEV_MCP_PASSWORD=your-mcp-password

# Repeat for staging/production with appropriate env name
CH_PRODUCTION_MIGRATION_PASSWORD=prod-password
CH_PRODUCTION_ADMIN_PASSWORD=prod-admin-password
```

## Integration Workflow

### For Existing Projects

```bash
# 1. Install
uv add clickhouse-alembic

# 2. Initialize (in project root or subdirectory)
ch-migrate init ./migrations --name my_project

# 3. Configure
# Edit migrations/config.yaml with your hosts
# Create migrations/.env.local with passwords

# 4. Bootstrap (safe on existing databases)
ch-migrate bootstrap dev --dry-run   # Preview
ch-migrate bootstrap dev             # Execute

# 5. Create baseline migration (documents existing schema)
ch-migrate new dev baseline

# 6. Apply baseline
ch-migrate up dev
```

### For New Projects (with Docker)

```bash
# Start ClickHouse
docker run -d --name clickhouse -p 8123:8123 \
  -e CLICKHOUSE_PASSWORD=admin123 clickhouse/clickhouse-server

# Initialize and configure for local (port 8123, secure: false)
ch-migrate init --name my_project
# Edit config.yaml: host: localhost, port: 8123, secure: false
# Create .env.local with CH_DEV_ADMIN_PASSWORD=admin123

ch-migrate bootstrap dev
ch-migrate new dev create_users_table --table users
ch-migrate up dev
```

## Migration Patterns

### Basic Table

```python
from alembic import op
from clickhouse_alembic import get_db

def upgrade():
    db = get_db()
    op.execute(f"""
        CREATE TABLE {db}.users (
            id UInt64,
            email String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY id
    """)

def downgrade():
    db = get_db()
    op.execute(f"DROP TABLE IF EXISTS {db}.users")
```

### Zero-Downtime with EXCHANGE TABLES

For schema changes that preserve data:

```python
def upgrade():
    db = get_db()

    # 1. Create new table with updated schema
    op.execute(f"""
        CREATE TABLE {db}.users_new (
            id UInt64,
            email String,
            phone String,  -- new column
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree() ORDER BY id
    """)

    # 2. Copy data with transformation
    op.execute(f"""
        INSERT INTO {db}.users_new
        SELECT id, email, '' as phone, created_at FROM {db}.users
    """)

    # 3. Atomic swap
    op.execute(f"EXCHANGE TABLES {db}.users AND {db}.users_new")

    # 4. Drop old
    op.execute(f"DROP TABLE {db}.users_new")
```

### Using SQL Files

```python
from clickhouse_alembic import get_db, read_sql

def upgrade():
    db = get_db()
    # Reads from migrations/sql/history/tables/users/2026_01_08_1400_abc123.sql
    op.execute(read_sql("history/tables/users/2026_01_08_1400_abc123.sql", db=db))
```

## Roles Created by Bootstrap

| Role | Purpose |
|------|---------|
| `{project}_migration_role` | Schema changes (CREATE/DROP/ALTER TABLE/VIEW/DICTIONARY), data ops (SELECT/INSERT/DELETE/TRUNCATE), introspection |
| `{project}_readonly_role` | SELECT + SHOW (if mcp_user configured) |
| `{project}_dict_role` | Dictionary source access (if dict_reader configured) |

Note: Bootstrap uses explicit grants (not `GRANT ALL`) for ClickHouse Cloud compatibility.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "migration_user required" | Add `migration_user: username` to environment in config.yaml |
| "Connection refused" | Check host/port. Local Docker: port 8123, secure: false |
| Passwords not loading | Ensure .env.local exists in project root (not migrations/) |
| Bootstrap hangs | Verify admin_password is correct for admin_user |
| "Database does not exist" | Run `ch-migrate bootstrap ENV` first |

### Verify Configuration

```bash
# Check what SQL would run
ch-migrate bootstrap dev --dry-run

# Should show masked passwords like:
# CREATE USER IF NOT EXISTS migration_dev
# IDENTIFIED BY '********';
```

## ClickHouse Cloud Notes

- Uses standard engines (MergeTree, ReplacingMergeTree) - auto-upgraded to Shared* on Cloud
- Default port 8443 (HTTPS), use 8123 for local HTTP
- DDL is non-transactional - migrations can't be atomically rolled back
- Each `op.execute()` runs one statement
