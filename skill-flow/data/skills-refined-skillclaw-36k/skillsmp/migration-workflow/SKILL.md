---
name: migration-workflow
description: Create, validate, and apply Supabase migrations with idempotent SQL, RLS checks, and types regeneration. Use when the user mentions migrations, db diff, schema changes, or type generation.
---
# Migration Workflow

## Quick Start

1. Identify schema change intent and target tables.
2. Create a new migration using the documented workflow.
3. Validate idempotency and RLS policy coverage.
4. Apply migration to hosted Supabase.
5. Regenerate types and verify.

## Steps

- Follow `docs/DATABASE_PIPELINE.md` and `docs/supabase_branching.md` for the approved flow.
- Prefer repo scripts when available:
  - `scripts/apply-single-migration.mjs`
  - `scripts/apply-remote-migrations.mjs`
- Ensure migration SQL uses `IF NOT EXISTS` and is safe to re‑run.
- After applying: regenerate types in `src/lib/generated/database.types.ts`.

## Checks

- RLS enabled on new tables.
- Policies tested or verified.
- No Docker‑dependent Supabase commands.
