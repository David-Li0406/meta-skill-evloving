---
name: context-database-schema
description: Use this skill for managing Supabase PostgreSQL schemas, including migrations, RLS policies, and type generation. It is applicable when working with database schema changes, migrations, data modeling, or type definitions.
---

# Database Schema

Manage Supabase database schema, migrations, and type definitions.

## Overview

PostgreSQL schema via Supabase with RLS policies. See `docs/database/SCHEMA.md`.

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

- `supabase/migrations/` - All migrations (sequential)
- Format: `YYYYMMDD_description.sql`
- Key prefixes: `*clerk*`, `*plaid*`, `*eodhd*`

### End-to-end Checklist (schema changes)

1. **Work in Railway dev shell**
   - Confirm: `echo $RAILWAY_ENVIRONMENT` is non-empty.
   - Use the dev `DATABASE_URL` and `SUPABASE_PROJECT_ID`.

2. **Apply migrations to dev**
   ```bash
   cd supabase
   supabase db push
   ```
   - If this fails on **old** migrations, follow the health check flow below (registry repair or idempotent DDL) before proceeding.

3. **Regenerate types and manifest**
   ```bash
   # From repo root, still in Railway shell
   export SUPABASE_PROJECT_ID=klrrntdswlvjdqusahdk  # or injected value
   make schema:generate
   ```

4. **Verify schema parity**
   ```bash
   cd backend
   PYTHONPATH=. poetry run python ../scripts/verify_generated_schemas.py
   ```

5. **Commit everything together**
   - In a feature branch:
     - `supabase/migrations/**` changes
     - `supabase/schemas/**` changes
     - Regenerated types and manifests
     - Updated `backend/schemas/generated/**`

### Migration Health Check

Before adding or merging new migrations:

1. **Verify registry vs schema**
   - Run in Railway shell:
     ```bash
     cd supabase
     supabase db push
     ```

2. **If db push fails on old migrations**
   - Do **not** hack the schema via ad‑hoc SQL.
   - Instead, repair the registry or make old migrations idempotent.

3. **New migrations (forward-only rule)**
   - Prefer `CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS`, and `CREATE INDEX IF NOT EXISTS` when possible.

4. **Dev/test-data migrations hygiene**
   - **Dev/test-data migrations** must live under `supabase/dev_migrations/`, NOT `supabase/migrations/`.

## Schema Definitions

- `supabase/schemas/public/` - Table definitions
- `supabase/schemas/public/tables/` - Individual table files

## Type Generation

- `supabase/types/database.types.ts` - Generated TypeScript types
- Generate via: `supabase gen types typescript`

## Backend Types

- `backend/schemas/generated/` - Generated Python types (if any)

## Key Tables and Recent Changes

### Holdings Table (`public.holdings`)

**Core columns:**
- `id`, `account_id`, `security_id`, `quantity`, `cost_basis`
- `created_at`, `updated_at`, `closed_at`

**Active vs Closed Holdings:**
- **Active holdings**: `closed_at IS NULL`
- **Closed positions**: `closed_at IS NOT NULL`, `quantity` conventionally `0`

### Holdings Snapshots Table (`public.holdings_snapshots`)

**Purpose**: Append-only time-series snapshots for historical portfolio analytics.

### Provider Security Mappings (`public.provider_security_mappings`)

**Purpose**: Map provider security IDs to canonical securities.

## Recent Changes

The **bd-k1c epic** introduced several schema enhancements, including holdings soft-close semantics and time-series snapshots.

## Documentation

- **Internal**: `docs/database/SCHEMA.md`

## Related Areas

- See `context-clerk-integration` for RLS patterns
- See `context-plaid-integration` for plaid_prices table and provider mappings
- See `context-symbol-resolution` for securities table
- See `context-portfolio` for holdings views and analytics