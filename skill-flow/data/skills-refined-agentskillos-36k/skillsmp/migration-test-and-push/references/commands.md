# Command Reference

All commands used by the migration skill.

## Project Constants

| Environment | Project ID             | Pooler Host                           | Pooler Port | Username                        |
| ----------- | ---------------------- | ------------------------------------- | ----------- | ------------------------------- |
| Staging     | `vsrlvwhnchughfcbilqn` | `aws-0-us-west-2.pooler.supabase.com` | `5432`      | `postgres.vsrlvwhnchughfcbilqn` |
| Production  | `jbbdfbjihbpntjrmkcwf` | `aws-0-us-west-1.pooler.supabase.com` | `6543`      | `postgres.jbbdfbjihbpntjrmkcwf` |

## Pre-Flight Checks

```bash
# List migration files
ls -la supabase/migrations/*.sql

# Check git status
git status

# Check Supabase status
npx supabase status

# Link to staging
npx supabase link --project-ref vsrlvwhnchughfcbilqn

# Link to production
npx supabase link --project-ref jbbdfbjihbpntjrmkcwf
```

## Local Testing

```bash
# Reset local database (applies all migrations)
npx supabase db reset

# Run pgTAP tests
npm run test:sql

# Generate types from local database
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

## Worker Management

```bash
# Find worker PID (Windows)
wmic process where "commandline like '%worker%' and name='node.exe'" get processid

# Kill worker
taskkill //F //PID [PID]

# Restart worker
npm run worker:dev
```

## Staging Push

```bash
# Link to staging first
npx supabase link --project-ref vsrlvwhnchughfcbilqn

# Dry-run (show what would be pushed)
npx supabase db push --dry-run

# Push to staging
npx supabase db push

# Verify staging migration
PGPASSWORD="<password>" psql \
  -h aws-0-us-west-2.pooler.supabase.com \
  -p 5432 \
  -U postgres.vsrlvwhnchughfcbilqn \
  -d postgres \
  -c "SELECT version FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 1;"
```

## Production Push

```bash
# Link to production first
npx supabase link --project-ref jbbdfbjihbpntjrmkcwf

# Dry-run (show what would be pushed)
npx supabase db push --dry-run

# Push to production (requires permission)
npx supabase db push

# Force push out-of-order migrations
npx supabase db push --include-all
```

## Backup

```bash
# Create backup directory
mkdir -p supabase/backups

# Backup production database
PGPASSWORD="<password>" pg_dump \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  --schema=public \
  -Fc \
  > supabase/backups/pre_migration_$(date +%Y%m%d_%H%M%S).dump

# Restore from backup
PGPASSWORD="<password>" pg_restore \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  --clean \
  supabase/backups/<backup_file>.dump
```

## Type Generation

```bash
# From production (after push)
npx supabase gen types typescript --project-id jbbdfbjihbpntjrmkcwf > src/integrations/supabase/types.ts

# From local (during testing)
npx supabase gen types typescript --local > src/integrations/supabase/types.ts
```

## Verification

```bash
# Check migration status in staging
PGPASSWORD="<password>" psql \
  -h aws-0-us-west-2.pooler.supabase.com \
  -p 5432 \
  -U postgres.vsrlvwhnchughfcbilqn \
  -d postgres \
  -c "SELECT version, statements_applied_at FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 5;"

# Check migration status in production
PGPASSWORD="<password>" psql \
  -h aws-0-us-west-1.pooler.supabase.com \
  -p 6543 \
  -U postgres.jbbdfbjihbpntjrmkcwf \
  -d postgres \
  -c "SELECT version, statements_applied_at FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 5;"
```

## Git Operations

```bash
# Stage migration files
git add supabase/migrations/

# Commit migration
git commit -m "feat(db): add [description]"

# Stage types file
git add src/integrations/supabase/types.ts

# Commit types
git commit -m "chore: update Supabase types after migration"
```

## Environment Variables

| Variable                 | Location     | Purpose                      |
| ------------------------ | ------------ | ---------------------------- |
| `SUPABASE_DB_PASSWORD`   | `.env.local` | Production database password |
| `VITE_SUPABASE_URL`      | `.env.local` | Supabase project URL         |
| `VITE_SUPABASE_ANON_KEY` | `.env.local` | Supabase anon key            |

## Pre-Flight Checklist

Before starting:

- [ ] Migration file exists in `supabase/migrations/`
- [ ] Migration uses idempotent patterns (IF NOT EXISTS)
- [ ] RLS policies included for new tables
- [ ] Git working directory is clean
- [ ] Local Supabase is running
- [ ] Time available to monitor production after push
