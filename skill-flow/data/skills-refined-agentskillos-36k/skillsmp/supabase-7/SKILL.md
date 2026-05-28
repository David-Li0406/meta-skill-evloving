---
name: supabase
description: V1.0 - Supabase database management, security fixes, and advisor issue resolution for the Dashboard project.
---

# Supabase Management

Expert guidance for managing the Dashboard's Supabase instance (project ref: `xofrtpzskdypkzhwxibo`).

## Quick Commands

| Task | Command |
|------|---------|
| Push migrations | `npx supabase db push --linked --yes` |
| Dump schema | `npx supabase db dump --linked --schema public` |
| List projects | `npx supabase projects list` |
| Get API keys | `npx supabase projects api-keys --project-ref xofrtpzskdypkzhwxibo` |
| Generate types | `bun db:types` |

## Security Best Practices

### SECURITY DEFINER Functions

All functions with `SECURITY DEFINER` MUST have `SET search_path = ''` to prevent search path injection:

```sql
CREATE OR REPLACE FUNCTION public.my_function()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
  -- Use fully qualified names: public.table_name
  RETURN new;
END;
$$;
```

### Trigger Functions

Trigger functions should:
1. Use `SECURITY DEFINER` with empty `search_path`
2. Revoke direct execute permissions (they're called by triggers, not users):

```sql
REVOKE ALL ON FUNCTION public.handle_xyz() FROM PUBLIC;
REVOKE ALL ON FUNCTION public.handle_xyz() FROM anon;
REVOKE ALL ON FUNCTION public.handle_xyz() FROM authenticated;
```

### RLS Helper Functions

Functions used in RLS policies (like `is_admin()`) should:
- Have `SECURITY DEFINER` with `SET search_path = ''`
- Keep `GRANT EXECUTE` for `authenticated` role

## Supabase Advisor Issues

### Security Issues (7 → 1 after migration 00026)

| Issue | Fix | Status |
|-------|-----|--------|
| Functions without `search_path` | Add `SET search_path = ''` | ✅ Fixed |
| Callable trigger functions | Revoke execute permissions | ✅ Fixed |
| HaveIBeenPwned password protection | **Requires Pro plan ($25/mo)** | ⚠️ Cannot fix on Free |

### Performance Issues (51)

These are informational only. Common ones:
- `SELECT name FROM pg_timezone_names` - Internal Postgres query
- `postgres-migrations` queries - Migration tooling
- Schema introspection queries - Supabase internals

**Action**: Monitor but don't stress—optimize when scaling.

## Dashboard Auth Settings

**Location**: Supabase Dashboard → Authentication → Attack Protection

| Setting | Status | Notes |
|---------|--------|-------|
| Captcha protection | Disabled | Optional |
| Leaked password protection | ❌ Pro only | Uses HaveIBeenPwned API |
| Min password length | 6 chars | Consider 8+ |

## Migration Naming Convention

```
supabase/migrations/000{XX}_{description}.sql
```

Current latest: `00026_fix_function_security.sql`

## Project Configuration

- **Organization**: HemSoft (Free tier)
- **Project**: dashboard
- **Region**: East US (North Virginia)
- **Branch**: main (Production)

## Debugging

### Check function security
```bash
npx supabase db dump --linked --schema public 2>&1 | Select-String -Pattern "SECURITY|search_path"
```

### View all public functions
```bash
npx supabase db dump --linked --schema public 2>&1 | Select-String -Pattern "CREATE OR REPLACE FUNCTION" -Context 0,10
```
