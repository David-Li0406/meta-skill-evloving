---
name: infra-ops
description: Manages infrastructure standards including Supabase migrations, RLS policies, and environment variables. Use when changing the database schema or deployment process.
---

# Infrastructure Ops Skill

This skill governs the backend and deployment integrity of THE LOST+UNFOUNDS.

## Database & Supabase Standards

### 1. Migrations (SQL)
- **Pattern**: Every migration must be idempotent.
- **Check-and-Execute**: Use `DO $$` blocks to check for existence before `INSERT` or `CREATE`.
- **Constraint Safety**: Never assume a column is UNIQUE. Always check by slug or ID before inserting.

### 2. RLS (Row Level Security)
- **Default Deny**: New tables should have RLS enabled and a `service_role` or `authenticated` policy.
- **Service Role**: Sensitive operations (like newsletter sending) should use the `SUPABASE_SERVICE_ROLE_KEY` via server-side handlers.

## Environment Management
- **Local .env**: Always check `.env.local` for local development.
- **Vercel**: Use the `set-vercel-env.sh` script to sync environment variables.
- **Secrets**: NEVER hardcode API keys. Use the `lib/api-handlers` pattern to fetch secrets.

## Zoho Mail Integration
- **OAuth**: Use the `_zoho-mail-handler.ts` and associated refresh token logic.
- **Error Handling**: Surface specific Zoho status codes if a send fails.

## Deployment Verification
- **Build Logs**: After deployment, ALWAYS check Vercel logs for "Silent Failures" or JSON parsing errors.
- **URL Check**: Verify the `https://www.thelostandunfounds.com/sql` page correctly lists new scripts.
