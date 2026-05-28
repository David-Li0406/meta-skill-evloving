# Production Mode - Detailed Steps

Full 16-step production deployment with all safety checks.

## Steps 1-4: Pre-Commit Testing

Same as [local-mode.md](local-mode.md) steps 1-4:
1. Verify migration date
2. Reset local database (`npx supabase db reset`)
3. Run pgTAP tests (`npm run test:sql`)
4. Check for missing tests

**Critical**: Complete ALL testing before committing!

## Step 5: Commit to Git

Stage and commit migration files:

```bash
git add supabase/migrations/
git commit -m "feat(db): add [migration description]"
```

Pre-commit hook runs automatically:
- Validates SQL syntax with sqlfluff
- Checks for common anti-patterns
- Fails if validation errors found

If commit fails, see [error-recovery.md](error-recovery.md#commit-fails).

## Step 6: Analyze Rollback Strategy

Read the migration file and categorize statements:

| Type | Operations | Rollback |
|------|------------|----------|
| Reversible | `CREATE TABLE`, `ADD COLUMN`, `CREATE INDEX` | `DROP` |
| Partial | `ALTER COLUMN` | May lose precision |
| Irreversible | `DROP TABLE`, `DROP COLUMN`, `TRUNCATE` | Backup restore only |

Generate rollback SQL:
```sql
-- Example for CREATE TABLE salesforce_connections
DROP TABLE IF EXISTS public.salesforce_connections CASCADE;
```

Show rollback analysis to user:
```
Rollback Analysis:

Migration: 20251224000000_salesforce_connections.sql

Reversible operations:
  CREATE TABLE salesforce_connections → DROP TABLE
  CREATE POLICY ... → DROP POLICY

Irreversible operations:
  None detected

Rollback SQL (save this!):
  DROP TABLE IF EXISTS public.salesforce_connections CASCADE;
```

For irreversible changes, warn explicitly:
```
WARNING: This migration contains IRREVERSIBLE changes!

  - DROP COLUMN users.legacy_email
  - TRUNCATE TABLE temp_imports

Backup REQUIRED before proceeding.
```

See [rollback-patterns.md](rollback-patterns.md) for detailed patterns.

## Step 7: Check Locking Impact

Scan migration for blocking operations:

| Pattern | Impact | Fix |
|---------|--------|-----|
| `ALTER TABLE` without timeout | May lock table | Add `SET lock_timeout = '30s'` |
| `CREATE INDEX` without CONCURRENTLY | Blocks writes | Use `CREATE INDEX CONCURRENTLY` |
| `VACUUM FULL` | Exclusive lock | Schedule during maintenance |
| Large `UPDATE`/`DELETE` | Row locks | Batch operations |

If blocking operations found, warn:
```
Locking Impact Warning:

  Line 15: ALTER TABLE accounts ADD COLUMN ...
    May lock table during operation
    Consider: SET lock_timeout = '30s';

  Line 42: CREATE INDEX idx_sessions_date ...
    Will block writes during creation
    Consider: CREATE INDEX CONCURRENTLY ...
```

Suggested pattern:
```sql
SET statement_timeout = '300s';
SET lock_timeout = '30s';
```

## Step 8: Request Permission

The `npx supabase db push` command is blocked by `bash_validator.py` for safety.

Use AskUserQuestion:
```typescript
{
  questions: [{
    question: "To push migrations, I need to temporarily enable 'supabase db push'. Allow this?",
    header: "Permission",
    options: [
      { label: "Yes, enable temporarily", description: "Auto-revoked after push" },
      { label: "No, cancel", description: "Run command manually" }
    ],
    multiSelect: false
  }]
}
```

If approved, modify `.claude/hooks/bash_validator.py`:

Add to `ALLOWED_PATTERNS` array:
```python
r"supabase\s+db\s+push",  # TEMPORARY: migration-test-and-push skill
```

## Step 9: Dry-Run Preview

Show what will be pushed:

```bash
npx supabase db push --dry-run
```

Output:
```
Would apply the following migrations:
  20251224000000_salesforce_connections.sql

No changes will be made to the database.
```

**Note**: Dry-run does NOT validate SQL syntax - only shows which files would apply.

## Step 10: Get Final Approval

Use AskUserQuestion (REQUIRED):
```typescript
{
  questions: [{
    question: "Ready to push migration to PRODUCTION database?",
    header: "Production Push",
    options: [
      { label: "Yes, push now", description: "Apply to live database (irreversible)" },
      { label: "No, cancel", description: "Keep migration local only" }
    ],
    multiSelect: false
  }]
}
```

Only proceed if user explicitly approves.

## Step 11: Create Production Backup

Before pushing, create a backup:

```bash
mkdir -p supabase/backups

PGPASSWORD="<db_password>" pg_dump \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  --schema=public \
  -Fc \
  > supabase/backups/pre_migration_$(date +%Y%m%d_%H%M%S).dump
```

The password is in `.env.local` as `SUPABASE_DB_PASSWORD`.

Show confirmation:
```
Production Backup Created

  File: supabase/backups/pre_migration_20251228_143052.dump
  Size: 2.4 MB
  Schema: public

  To restore:
    pg_restore -h <host> -U <user> -d postgres --clean <file>
```

## Step 12: Push to Production

Execute the push:

```bash
npx supabase db push
```

Expected output:
```
Applying migrations to remote database...
  20251224000000_salesforce_connections.sql
Migrated supabase/migrations/20251224000000_salesforce_connections.sql
```

If push fails, see [error-recovery.md](error-recovery.md#production-push-fails).

## Step 13: Verify Migration Applied

Query the schema_migrations table:

```bash
PGPASSWORD="<password>" psql \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  -c "SELECT version, statements_applied_at FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 3;"
```

Expected output:
```
      version       |    statements_applied_at
--------------------+----------------------------
 20251224000000     | 2025-12-28 14:31:05.123456  ← NEW
 20251220123456     | 2025-12-20 12:35:00.000000
```

Confirm:
```
Migration Verified

  Version: 20251224000000_salesforce_connections
  Applied at: 2025-12-28 14:31:05 UTC

  Migration is now LIVE in production!
```

## Step 14: Revoke Permission (Automatic)

Remove the temporary pattern from `.claude/hooks/bash_validator.py`:

Remove this line from `ALLOWED_PATTERNS`:
```python
r"supabase\s+db\s+push",  # TEMPORARY: migration-test-and-push skill
```

No user approval needed - this is security restoration.

## Step 15: Generate Types

Generate TypeScript types from production:

```bash
npx supabase gen types typescript --project-id jbbdfbjihbpntjrmkcwf > src/integrations/supabase/types.ts
```

If this fails, see [error-recovery.md](error-recovery.md#type-generation-fails).

## Step 16: Commit Types

Stage and commit the updated types:

```bash
git add src/integrations/supabase/types.ts
git commit -m "chore: update Supabase types after migration"
```

## Final Output

```
Migration Test & Push COMPLETE!

Timeline:
  1. Committed: 20251224000000_salesforce_connections.sql
  2. Local test: PASSED
  3. User approved production push
  4. Backup created: pre_migration_20251228_143052.dump
  5. Pushed to production
  6. Verified: Migration applied at 14:31:05 UTC
  7. Types generated and committed

Your migration is now LIVE in production!

Next steps:
  - Test the feature in production UI
  - Monitor error logs for issues
  - If problems occur, create rollback migration
```
