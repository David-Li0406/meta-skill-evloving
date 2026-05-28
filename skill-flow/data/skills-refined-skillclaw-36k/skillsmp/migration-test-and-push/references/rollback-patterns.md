# Rollback Patterns

Analysis patterns for migration rollback planning.

## Operation Categories

### Reversible Operations

These can be rolled back with a simple DROP statement:

| Operation | Rollback |
|-----------|----------|
| `CREATE TABLE table_name` | `DROP TABLE IF EXISTS table_name CASCADE` |
| `CREATE INDEX idx_name` | `DROP INDEX IF EXISTS idx_name` |
| `CREATE POLICY policy_name` | `DROP POLICY IF EXISTS policy_name ON table_name` |
| `CREATE FUNCTION func_name` | `DROP FUNCTION IF EXISTS func_name` |
| `CREATE TRIGGER trigger_name` | `DROP TRIGGER IF EXISTS trigger_name ON table_name` |
| `ADD COLUMN col_name` | `ALTER TABLE t DROP COLUMN IF EXISTS col_name` |
| `ADD CONSTRAINT` | `ALTER TABLE t DROP CONSTRAINT IF EXISTS name` |

Example rollback script:
```sql
-- Rollback for 20251224000000_salesforce_connections.sql
BEGIN;

DROP POLICY IF EXISTS "Users can view own connections" ON salesforce_connections;
DROP POLICY IF EXISTS "Users can manage own connections" ON salesforce_connections;
DROP TABLE IF EXISTS public.salesforce_connections CASCADE;

COMMIT;
```

### Partially Reversible Operations

These can be reversed but may lose data:

| Operation | Impact | Rollback |
|-----------|--------|----------|
| `ALTER COLUMN type` (expanding) | Safe | Reverse ALTER |
| `ALTER COLUMN type` (shrinking) | Data truncation | May fail |
| `ALTER COLUMN SET DEFAULT` | Previous default lost | Set old default |
| `ALTER COLUMN SET NOT NULL` | Nulls filled with default | DROP NOT NULL |

Example:
```sql
-- Forward: Expand varchar
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(500);

-- Rollback: Shrink (may fail if data > 255)
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(255);
```

### Irreversible Operations

These CANNOT be rolled back without a backup:

| Operation | Data Loss | Recovery |
|-----------|-----------|----------|
| `DROP TABLE` | Complete | Restore from backup |
| `DROP COLUMN` | Column data | Restore from backup |
| `TRUNCATE` | All rows | Restore from backup |
| `DELETE` (mass) | Deleted rows | Restore from backup |
| Data migration | Original values | Restore from backup |

**Always create backup before these operations!**

## Rollback Script Generation

For each migration, generate rollback SQL:

### Template
```sql
-- Rollback for [migration_file]
-- WARNING: Run only if forward migration needs to be undone
-- Created: [date]

BEGIN;

-- Reverse operations in OPPOSITE order of migration

-- [rollback statements here]

COMMIT;
```

### Example: New Table with Policies
```sql
-- Forward migration
CREATE TABLE salesforce_connections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  instance_url TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE salesforce_connections ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own" ON salesforce_connections
  FOR SELECT USING (auth.uid() = user_id);
```

```sql
-- Rollback script
BEGIN;

DROP POLICY IF EXISTS "Users can view own" ON salesforce_connections;
DROP TABLE IF EXISTS public.salesforce_connections CASCADE;

COMMIT;
```

### Example: Adding Columns
```sql
-- Forward migration
ALTER TABLE sessions ADD COLUMN sf_opportunity_id TEXT;
ALTER TABLE sessions ADD COLUMN sf_last_sync TIMESTAMPTZ;
```

```sql
-- Rollback script
BEGIN;

ALTER TABLE sessions DROP COLUMN IF EXISTS sf_last_sync;
ALTER TABLE sessions DROP COLUMN IF EXISTS sf_opportunity_id;

COMMIT;
```

## Rollback Decision Matrix

| Situation | Action |
|-----------|--------|
| Migration failed mid-execution | Assess damage, may need manual cleanup |
| Feature needs to be reverted | Run rollback script if reversible |
| Data corruption detected | Restore from backup |
| Performance issues | Analyze, may need index adjustment |

## Pre-Migration Checklist

Before any migration with destructive operations:

- [ ] Backup created (pg_dump)
- [ ] Rollback script prepared
- [ ] Rollback script tested in dev
- [ ] Team notified of potential rollback
- [ ] Monitoring alerts configured
- [ ] Runbook for rollback procedure documented
