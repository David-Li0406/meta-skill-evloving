---
name: supabase-project
description: Project-specific Supabase usage patterns, clients, and migration workflow for this repo.
---

# Supabase Project Skill

This skill documents **how to use Supabase in this project** with the correct clients, schema-aware patterns, and migration workflow.

## Golden Rules (Project Specific)

1. **Supabase is the single source of truth** for data and engagement counts.
2. **Never run database reset commands** (e.g., `supabase db reset`).
3. **Never assume columns**. Always confirm schema from the **live database**.
4. **User prefers manual control of migrations** — only run a migration when explicitly asked.
5. **Always verify against live Supabase** before Supabase-related changes.

## Clients and When to Use Them

### Server Route Handlers (authenticated)
Use the helper that respects cookies and auth sessions:
```ts
import { createRouteHandlerClientAsync } from '@/lib/supabase/client-helper'

const supabase = await createRouteHandlerClientAsync()
const { data, error } = await supabase.from('posts').select('*')
```

### Server Read-Only for Public/Unauthenticated
Use service-role when a request is unauthenticated and still needs public data:
```ts
import { supabaseAdmin } from '@/lib/supabase-admin'

const { data, error } = await supabaseAdmin.from('posts').select('*')
```

### Server Action / Backend Logic
Use the same cookie-aware server client:
```ts
import { createServerActionClientAsync } from '@/lib/supabase/client-helper'
const supabase = await createServerActionClientAsync()
```

### Client Components
Use browser client:
```ts
import { createBrowserClient } from '@supabase/ssr'

const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

## Live Verification (Required)

**Preferred method**: Direct live SQL via `psql` using environment variables from `.env.local`.

Example (PowerShell):
```powershell
$env:PGPASSWORD = "<SUPABASE_DB_PASSWORD>"
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -h <SUPABASE_DB_HOST> -p <SUPABASE_DB_PORT> -U <SUPABASE_DB_USER> -d <SUPABASE_DB_NAME> -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name='posts' ORDER BY ordinal_position;"
```

Fallback method (read-only): use `supabaseAdmin` to query `information_schema` if `psql` is not available.

## Schema Sources (Use After Live Verification)

- **Types**: `types/database.ts` (authoritative for column names/types)
- **Migrations**: `supabase/migrations/*.sql`
- **Docs**: `docs/HOW_TO_READ_FROM_SUPABASE.md`

## Migration Workflow (Manual Only)

Follow `docs/scripts/HOW_TO_RUN_MIGRATIONS.md`. Preferred command:
```bash
npm run db:migrate supabase/migrations/<file>.sql
```

Do not run migrations unless explicitly requested.

## Common Patterns Used in This Repo

### Engagement Data
- Do **not** rely on cached counts in `posts`.
- Use RPCs (e.g., `get_entity_engagement`, `get_multiple_entities_engagement`) for counts.

### Visibility
- Visibility values: `public`, `friends`, `followers`, `private`.
- Enforce visibility at API layer for unauthenticated requests.

## Related Files

- `lib/supabase-admin.ts`
- `lib/supabase/client-helper.ts`
- `lib/supabase.ts` (admin client with timeout)
- `app/api/*` (route handlers using these patterns)
