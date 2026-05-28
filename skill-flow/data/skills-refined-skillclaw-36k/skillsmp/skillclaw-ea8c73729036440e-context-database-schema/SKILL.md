---
name: context-database-schema
description: Use this skill when managing Supabase PostgreSQL schemas, handling migrations, or addressing database-related issues.
---

# Database Schema Management

This skill provides guidance on managing Supabase PostgreSQL schemas, including migrations, RLS policies, and type generation.

## Overview

Utilize PostgreSQL schema via Supabase with RLS policies. Refer to `docs/database/SCHEMA.md` for detailed documentation.

## Database Access

**⚠️ CRITICAL: Must be in Railway shell for all database operations**

```bash
# Verify environment first
echo $RAILWAY_ENVIRONMENT  # Must be non-empty

# If empty, enter Railway shell:
railway shell
```

**Common Queries:**

```bash
# Quick introspection
psql "$DATABASE_URL" -c "\dt"  # List all tables
psql "$DATABASE_URL" -c "\d users"  # Describe users table
psql "$DATABASE_URL" -c "\d+ accounts"  # Detailed table info with indexes

# Core tables
psql "$DATABASE_URL" -c "SELECT * FROM users LIMIT 5;"
psql "$DATABASE_URL" -c "SELECT * FROM accounts WHERE user_id = 'user_xxx';"
psql "$DATABASE_URL" -c "SELECT * FROM holdings WHERE account_id = 'acc_xxx';"
```

## Migrations

### The New Standard: Alembic
Transition to standard **Alembic** migrations located in `backend/migrations/versions`.

- **Create Migration**: 
  ```bash
  cd backend && poetry run alembic revision -m "description"
  ```
- **Apply Migration**: 
  ```bash
  cd backend && poetry run alembic upgrade head
  ```

### Manual SQL (Railway)
For non-Alembic changes:
```bash
railway run --service pgvector -- psql "$DATABASE_URL" -f my_script.sql
```

### ⚠️ LEGACY: Supabase Migrations
The `supabase/migrations/` directory and CLI `supabase db push` workflow are **DEPRECATED**. Existing migrations (86+) are preserved for historical reference.

### End-to-end Checklist (schema changes)

1. **Work in Railway dev shell**
   - Confirm: `echo $RAILWAY_ENVIRONMENT` is non-empty.
   - Use the dev `DATABASE_URL` and `SUPABASE_PROJECT_ID`.

2. **Apply migrations to dev**
   ```bash
   cd supabase
   supabase db push
   ```
   - If this fails on **old** migrations, follow the health check flow before proceeding.

3. **Regenerate types and manifest**
   ```bash
   # Follow the necessary commands to regenerate types
   ```

Use this skill to effectively manage your database schema, handle migrations, and troubleshoot related issues.