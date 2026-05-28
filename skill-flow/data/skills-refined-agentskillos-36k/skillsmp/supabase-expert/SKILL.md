---
name: supabase-expert
description: Expert in Supabase database management, querying patterns, and migration workflows specific to this project.
---

# Supabase Expert

This skill provides comprehensive knowledge for interacting with Supabase in this project, using the **Supabase CLI** (`npx supabase`) and the `supabaseAdmin` client.

## Project Configuration

- **Project ID**: `nmrohtlcfqujtfgcyqhw`
- **CLI Version**: supabase 2.33.9 (dev dependency)
- **Types Location**: `types/database.ts`
- **Migrations Location**: `supabase/migrations/`

## Working CLI Commands

### ✅ Database Operations
```bash
npx supabase db push                    # Apply pending migrations
npx supabase db push --include-all      # Apply ALL migrations (use for new ones)
npx supabase db push --dry-run          # Preview without applying
npx supabase db reset                   # Reset local DB with migrations
npx supabase status                     # Show service status
npx supabase start                      # Start local services
npx supabase stop                       # Stop local services
```

### ✅ Migration Management
```bash
npx supabase migration list             # Show migration status
npx supabase migration repair --status reverted YYYYMMDD  # Fix history
npx supabase migration repair --status applied YYYYMMDD   # Mark as applied
npx supabase migration new [name]       # Create new migration
```

### ✅ Type Generation
```bash
npm run types:generate                  # Generate TS types from schema
npm run db:types                        # Alias for types:generate
npm run schema:download                 # Download schema + generate types
```

### ✅ Direct SQL Queries (using psql)
PostgreSQL is installed at: `C:\Program Files\PostgreSQL\17\bin\psql.exe`

To query the live database:
```powershell
# Set password from .env.local and run query
$env:PGPASSWORD = "<password_from_env>"; 
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -h db.nmrohtlcfqujtfgcyqhw.supabase.co -p 5432 -U postgres -d postgres -c "SELECT count(*) FROM table_name;"
```

## ❌ Commands That Don't Work
```bash
supabase [command]              # Not installed globally (use npx!)
./node_modules/.bin/supabase    # Path issues on Windows
```

## Important Notes

1. **Exit Code 0 = Success**: Ignore npm error messages if exit code is 0
2. **Use `--include-all`**: Required for new migrations
3. **Delete Bad Migrations**: Remove problematic SQL files before retrying
4. **Repair History**: Use `migration repair` for mismatched states

## Server-Side Querying Pattern

Use `supabaseAdmin` from `@/lib/supabase/server`:

```typescript
import { supabaseAdmin } from '@/lib/supabase/server'

const { data, error } = await supabaseAdmin
  .from('table_name')
  .select('id, column_a, related_data(id, name)')
  .eq('status', 'active')
  .limit(10)

if (error) {
  console.error('Error:', error)
  return []
}
return data
```

## Relevant Documentation
- `docs/public-docs/CLI_USAGE_GUIDE.md`: Complete CLI reference
- `docs/public-docs/CLI_CONFIG_FIX_AND_MIGRATION.md`: Config troubleshooting
- `docs/HOW_TO_READ_FROM_SUPABASE.md`: Query patterns
- `docs/scripts/HOW_TO_RUN_MIGRATIONS.md`: Migration workflow
