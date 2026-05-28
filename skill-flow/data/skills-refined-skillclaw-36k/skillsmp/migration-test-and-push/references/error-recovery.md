# Error Recovery

Common error scenarios and their fixes.

## Commit Fails (sqlfluff errors) {#commit-fails}

**Problem**: SQL syntax errors or anti-patterns detected by pre-commit hook.

**Symptoms**:
```
sqlfluff validation failed!
  Line 15: Missing semicolon
  Line 32: Column "email" does not exist
```

**Fix**:
1. Read error messages carefully
2. Fix SQL in migration file
3. Run skill again (re-attempts commit)

**No database changes made** - safe to retry.

## Local Test Fails {#local-test-fails}

**Problem**: Migration breaks on `npx supabase db reset`.

**Common causes**:
- Column already exists
- Table already exists
- Constraint violation
- Missing dependency

**Symptoms**:
```
ERROR: column "email" already exists
LINE 15: ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

**Fix - Make idempotent**:
```sql
-- BAD: Fails if column exists
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- GOOD: Idempotent
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name='users' AND column_name='email'
  ) THEN
    ALTER TABLE users ADD COLUMN email VARCHAR(255);
  END IF;
END $$;
```

**Recovery**:
1. Fix migration SQL
2. Run `npx supabase db reset`
3. Run skill again

**No production changes made** - safe to retry.

## Production Push Fails {#production-push-fails}

**Problem**: Migration works locally but fails in production.

**Common causes**:
- Production has different data than local
- Migration assumes empty tables
- Constraint violations with real data
- Foreign key references

**Symptoms**:
```
ERROR: relation "user_preferences" does not exist
LINE 42: INSERT INTO user_preferences...
```

**Important**:
- **DO NOT** try pushing same migration again
- Production is UNCHANGED (still safe)
- Local is now OUT OF SYNC with production

**Fix**:
1. Analyze why production differs from local
2. Create NEW corrective migration
3. Test with realistic data
4. Deploy new migration

**To resync local with production**:
```bash
# Delete failed migration locally
rm supabase/migrations/20251224000000_failing_migration.sql

# Reset local
npx supabase db reset
```

## Type Generation Fails {#type-generation-fails}

**Problem**: Cannot connect to Supabase or generate types.

**Symptoms**:
```
Error connecting to Supabase project
```

**Fix - Run manually**:
```bash
npx supabase gen types typescript --project-id jbbdfbjihbpntjrmkcwf > src/integrations/supabase/types.ts
git add src/integrations/supabase/types.ts
git commit -m "chore: update Supabase types after migration"
```

**Note**: Migration is still successful - types are just documentation.

## Permission Denied (BLOCKED by hook) {#blocked-by-hook}

**Problem**: Bash validator blocks `db push` command.

**Symptoms**:
```
BLOCKED: supabase db push to remote (use --local)
```

**Fix**:
This is expected! The skill handles permission management automatically.

If running manually:
1. Edit `.claude/hooks/bash_validator.py`
2. Add `r"supabase\s+db\s+push"` to `ALLOWED_PATTERNS`
3. Run the push command
4. Remove the pattern after push

## Project Not Linked {#project-not-linked}

**Problem**: Supabase CLI doesn't know which project to push to.

**Symptoms**:
```
Cannot find project ref. Have you run supabase link?
```

**Fix**:
```bash
npx supabase link --project-ref jbbdfbjihbpntjrmkcwf
```

## Migration Files Out of Order {#out-of-order}

**Problem**: Local migrations have timestamps before last remote migration.

**Symptoms**:
```
Found local migration files to be inserted before the last migration on remote database
```

**Fix**:
```bash
# Force apply out-of-order migrations
npx supabase db push --include-all
```

**Prevention**: Always use current timestamp when creating migrations.

## pgTAP Tests Fail {#pgtap-fails}

**Problem**: Database tests fail after reset.

**Symptoms**:
```
not ok 1 - Table 'salesforce_connections' should exist
```

**Common causes**:
- Migration has syntax error
- Table name mismatch (test vs migration)
- RLS policy name mismatch

**Fix**:
1. Check migration file for typos
2. Verify test assertions match migration
3. Run `npx supabase db reset` to retry

## Worker Not Processing {#worker-stuck}

**Problem**: After db reset, worker stops processing events.

**Symptoms**:
- Automation events not processed
- No worker log output
- Worker appears running but idle

**Cause**: PostgreSQL connection invalidated but not auto-reconnected.

**Fix**:
```bash
# Find and kill worker
wmic process where "commandline like '%worker%' and name='node.exe'" get processid
taskkill //F //PID [PID]

# Restart
npm run worker:dev
```

## Backup Restore Needed

**Problem**: Migration caused data corruption, need to restore.

**Restore command**:
```bash
PGPASSWORD="<password>" pg_restore \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  --clean \
  supabase/backups/pre_migration_YYYYMMDD_HHMMSS.dump
```

**Warning**: This OVERWRITES current production data with backup state.
