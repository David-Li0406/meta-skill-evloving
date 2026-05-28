---
name: context-database-schema
description: |
  Supabase PostgreSQL schema management, 86+ migrations, RLS policies, and type generation.
  Handles table creation, schema changes, migrations, foreign key constraints, and migration workflows.
  Use when working with database schema, migrations, data modeling, or type definitions,
  or when user mentions database changes, table modifications, schema updates, migration failures,
  "relation does not exist" errors, foreign key issues, Supabase schema operations, users table, accounts table, or holdings table.
tags: [database, schema, migrations, supabase]
---

# Database Schema

Navigate database schema, 90+ migrations (legacy), and type definitions.

> [!NOTE]
> As of bd-k9tw (Dec 2025), migrations are documented in `supabase/migrations/README.md`.
> The legacy Supabase workflow is deprecated - use Alembic for new migrations.

## Overview

PostgreSQL schema via Supabase with RLS policies. See `docs/database/SCHEMA.md`.

## Database Access

**✅ PRIMARY: Railway Postgres (pgvector)**

The database is a standard PostgreSQL container hosted on Railway.
Connection string: `DATABASE_URL` (in Railway environment).

```bash
# Verify environment
echo $RAILWAY_ENVIRONMENT

# Interactive Shell
railway run --service pgvector -- psql "$DATABASE_URL"

# Quick Checks
railway run --service pgvector -- psql "$DATABASE_URL" -c "\dt"
railway run --service pgvector -- psql "$DATABASE_URL" -c "SELECT count(*) FROM users;"
```

**⚠️ LEGACY: Supabase**
Supabase is DEPRECATED for runtime operations. Only use for archival or reference.
See `docs/STRATEGIC_MIGRATION_PLAN_RAILWAY.md` for migration details.

## Migrations

### The New Standard: Alembic
We are transitioning to standard **Alembic** migrations located in `backend/migrations/versions`.
- **Create**: `cd backend && poetry run alembic revision -m "description"`
- **Apply**: `cd backend && poetry run alembic upgrade head`

### Manual SQL (Railway)
For non-Alembic changes:
```bash
railway run --service pgvector -- psql "$DATABASE_URL" -f my_script.sql
```

### ⚠️ LEGACY: Supabase Migrations
The `supabase/migrations/` directory and CLI `supabase db push` workflow are **DEPRECATED**.
- Existing migrations (86+) are preserved for historical reference/archival.
- Do **NOT** add new migrations here for Railway.
- Do **NOT** rely on Supabase migration registry markers.

### End-to-end Checklist (schema changes)
(Legacy Supabase workflow below - use only if strictly necessary during transition)

Any time you change schema (tables, columns, indexes, RLS) or add Supabase migrations:

If `supabase db push` fails with "Remote migration versions not found" (Drift), do **NOT** run manual SQL in Dashboard. This creates a vicious cycle.

**Fix:**
1. Ensure `DATABASE_URL` is set in Railway (required for CLI).
2. Run repair to sync registry with local files:
   ```bash
   # In Railway shell
   supabase migration repair --status applied <version_id>
   # Or for batch:
   supabase migration repair --status applied 20251129... 20251204...
   ```
3. Then run `supabase db push` for new migrations.

#### Ghost Versions: "Remote migration versions not found in local migrations directory"

**Symptom:** CLI reports versions in the database that don't exist locally (e.g., `20250925`, `20251123`, `20251124`).

**Root Cause Analysis - Two Scenarios:**

**Scenario A: Missing Registry Marker Files (prime-radiant-ai pattern)**
- The project uses "registry markers" - bare YYYYMMDD versions inserted into the registry as checkpoints (e.g., '20250925', '20251123')
- Each marker requires a corresponding `YYYYMMDD_registry_marker.sql` file locally
- If the marker file is missing/deleted, CLI fails even though the marker serves a valid purpose
- **These are NOT errors to fix by reverting** - they're intentional checkpoints

**Scenario B: True Ghost Versions**
- Migrations manually applied via Dashboard SQL Editor without creating local files
- Old migrations that were deleted/renamed locally but still in registry
- Registry pollution from incorrect repair attempts

**⚠️ CRITICAL: Do NOT edit migration SQL files to add IF NOT EXISTS guards as a workaround. This doesn't fix the root cause.**

**Railway Authentication Issue:**
- If you get `password authentication failed` errors, you're not authenticated with the production database.
- **Fix:** Use `railway run supabase ...` instead of plain `supabase ...` commands. This injects the correct `DATABASE_URL`.

**Step-by-Step Fix:**

**1. Identify what's in the registry:**
```bash
# In Railway shell
railway run supabase migration list
# OR query the registry directly
railway run -- psql "$DATABASE_URL" -c \
  "SELECT version FROM supabase_migrations.schema_migrations ORDER BY version;"
```

**2. Compare with local files:**
```bash
# List local migration files
ls supabase/migrations/*.sql | sed 's/.*\///;s/_.*//' | sort
```

**3. Determine fix strategy based on version type:**

**For Registry Markers (Scenario A):**
- If version is a bare date (8 digits, no timestamp) like `20251124`
- AND there are other migrations with that prefix (e.g., `20251124_advisor_feedback.sql`)
- **Fix:** Create a marker file to satisfy CLI:
  ```bash
  cd supabase/migrations
  cat > 20251124_registry_marker.sql <<'EOF'
  -- Marker migration for version 20251124
  -- Context: Registry checkpoint from schema repair
  --
  -- This file exists solely to satisfy Supabase CLI's requirement that every
  -- version present in supabase_migrations.schema_migrations has a matching
  -- local migration file whose name begins with the same version prefix.
  --
  -- The actual schema changes for this period were applied via timestamped
  -- migrations or golden schema bootstrap scripts.
  -- No additional DDL should be added here.

  EOF
  ```
- This is safe and maintains the checkpoint system

**For True Ghost Versions (Scenario B):**
- If version doesn't correspond to any local files AND wasn't an intentional marker
- **Fix:** Revert from registry:
  ```bash
  railway run supabase migration repair --status reverted <ghost_version>
  ```
- This removes the ghost WITHOUT dropping database objects
- Only do this if you're certain it's not an intentional marker

**4. Verify and push:**
```bash
railway run supabase migration list  # Should show no errors
railway run supabase db push         # Should succeed for new migrations
```

**Prevention:**
- **If using registry markers:** Keep marker files in version control alongside the migrations they checkpoint
- **Document marker strategy:** Add comments in marker files explaining their purpose (see example above)
- **Prefer timestamped migrations:** Use full `YYYYMMDDHHMMSS` format to avoid ambiguity
- **Never manually run migration SQL in Dashboard** - always use `supabase db push`
- **If you must use Dashboard for emergency fixes:** Generate a proper migration file afterward with `supabase db diff`

**Registry Marker Strategy Trade-offs:**
- ✅ **Pros:** Clear checkpoints for which batches of migrations are applied; useful for repair scripts
- ❌ **Cons:** Extra files to maintain; CLI confusion if markers are missing; not a Supabase best practice
- **Alternative:** Eliminate markers entirely, use only timestamped migrations, and repair registry only when truly needed

## Schema Definitions

- `supabase/schemas/public/` - Table definitions
- `supabase/schemas/public/tables/` - Individual table files

## Type Generation

- `supabase/types/database.types.ts` - Generated TypeScript types
- Generate via: `supabase gen types typescript`

## Backend Types

- `backend/schemas/generated/` - Generated Python types (if any)

## Scripts

- `scripts/db-commands/` - Database utilities
- `backend/migrations/versions/` - Alembic migrations (if used)

## Key Tables and Recent Changes

### Holdings Table (`public.holdings`)

**Core columns:**
- `id`, `account_id`, `security_id`, `quantity`, `cost_basis`
- `created_at`, `updated_at`, `closed_at`

**Active vs Closed Holdings (bd-k1c.4):**
- **Active holdings**: `closed_at IS NULL` - current portfolio positions
- **Closed positions**: `closed_at IS NOT NULL`, `quantity` conventionally `0`
- Plaid pipeline **soft-closes** positions that disappear from broker snapshots (doesn't delete)
- Manual holdings are NOT auto-closed by provider sync

**Index:**
- Partial index `idx_holdings_closed_at ON holdings(closed_at) WHERE closed_at IS NULL` for efficient active holdings queries

**Current portfolio views**: Filter with `WHERE closed_at IS NULL`

### Holdings Snapshots Table (`public.holdings_snapshots`)

**Purpose**: Append-only time-series snapshots for historical portfolio analytics (bd-k1c.6)

**Core columns:**
- `snapshot_at` (TIMESTAMPTZ) - snapshot time, typically daily at market close
- `user_id`, `account_id`, `security_id`
- `quantity`, `cost_basis`, `market_value`, `price_source`

**Key constraints:**
- `UNIQUE (snapshot_at, account_id, security_id)` for idempotency
- Indexes on `(user_id, snapshot_at DESC)`, `(account_id, snapshot_at DESC)`, `(security_id, snapshot_at DESC)`

**Relationship to holdings:**
- Snapshots derived from active holdings + price data
- Snapshot job: `backend/scripts/create_holdings_snapshot.py`

### Provider Security Mappings (`public.provider_security_mappings`)

**Purpose**: Map provider security IDs to canonical securities

**Natural key (bd-k1c.3):**
- `UNIQUE (brokerage_connection_id, provider_security_id)`
- `provider_security_id VARCHAR(255)` - stable provider-side identifier (e.g., Plaid `security_id`)
- `provider_payload JSONB` - retained for audit, NOT in uniqueness constraint

**Index:**
- `idx_provider_security_mappings_provider_security_id` for fast lookups

**Used by:**
- `RawDataService.get_existing_security_mapping`
- `SecurityResolver._link_provider_mapping` (upserts on natural key)

## Recent bd-k1c Changes

The **bd-k1c epic** (Plaid portfolio pipeline hardening) introduced several schema enhancements:

- **Holdings soft-close semantics** (`closed_at` column) - distinguishes active vs closed positions
- **Time-series snapshots** (`holdings_snapshots` table) - enables historical analytics
- **Provider mapping refinement** (`provider_security_id` natural key) - more robust brokerage integrations

See `docs/bd-k1c/EPIC_OVERVIEW.md` for full context and child features.

## Documentation

- **Internal**: `docs/database/SCHEMA.md`

## Related Areas

- See `context-clerk-integration` for RLS patterns
- See `context-plaid-integration` for plaid_prices table and provider mappings
- See `context-symbol-resolution` for securities table
- See `context-portfolio` for holdings views and analytics
