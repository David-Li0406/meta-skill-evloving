---
name: database-designer
description: Design, review, and evolve the TRR Backend 2025 database (Supabase/Postgres + RLS) including schema modeling, indexes, migrations, rollout plans, and S3 metadata patterns. Use when adding or changing tables, RLS policies, indexes, or storage metadata; when reviewing query performance or migration safety; or when preparing DB design reviews and checklists for TRR.
---

# Database Designer (TRR Backend 2025)

Use this skill to design and document Postgres/Supabase schema changes, write repo-compatible migrations, and produce safe rollout/verification plans. The target stack is Supabase (Postgres + RLS) and AWS S3 for file storage with metadata in Postgres.

## Repo-aware context (read first)

Open these references before proposing changes:
- `skills/database-designer/references/repo-context.md` for the current TRR schema, Supabase layout, and access patterns.
- `skills/database-designer/references/templates.sql` for migration, RLS, triggers, and index templates.
- `skills/database-designer/references/examples.md` for concrete TRR-style examples (new table, S3 metadata, multi-tenant RLS).
- `skills/database-designer/references/tooling.md` for schema docs, EXPLAIN, and index verification commands.
- `skills/database-designer/references/playbooks.md` for scalability and architecture decision frameworks.

## Inputs expected

Collect these from the requester before designing:
- Feature spec or user stories.
- Entities and relationships (new or modified).
- Query patterns (read/write hot paths, filters, joins, pagination, sorting).
- Scale assumptions (row counts, growth rate, access frequency).
- Tenancy model (single-tenant vs tenant_id vs org membership).
- Data retention and privacy requirements (GDPR/erasure, audit trails).
- S3 usage (bucket, access model, object lifecycle expectations).

## Outputs produced

Always produce concrete, repo-compatible artifacts:
- ERD or table list with keys, constraints, nullability, and references.
- SQL migration(s) under `supabase/migrations/` (no destructive ops on prod).
- RLS policies (copy/paste ready) and policy checklist.
- Index plan with rationale (btree/GIN/BRIN/partial/composite).
- Rollout plan (expand/contract, backfill, validation, rollback).
- Verification checklist (EXPLAIN, pg_stat_statements, data sanity checks).

## Workflow (follow in order)

1) **Discover the current state**
   - Read `supabase/schema_docs/*` and `supabase/migrations/*`.
   - Identify existing entities, keys, and constraints in `core`.
   - Review API/ingestion usage in `api/routers/*`, `trr_backend/repositories/*`, and `scripts/*`.

2) **Model the change**
   - Propose tables/columns with types and constraints.
   - Decide cascade rules, soft-delete strategy, and audit fields.
   - Decide normalization vs denormalization (document tradeoffs).
   - Choose tenancy strategy and RLS pattern.
   - Define access-control rules for reads/writes.

3) **Index and performance plan**
   - Map query patterns to index choices.
   - Decide on partial/composite/GIN/BRIN as needed.
   - Note potential partitioning if growth or retention needs it.

4) **Migration + RLS artifacts**
   - Generate SQL migrations compatible with Supabase (`supabase/migrations/NNNN_*.sql`).
   - Add RLS policies and grants.
   - Include updated_at triggers or audit tables if required.
   - If an ORM appears later, mirror migrations there; otherwise stick to SQL.

5) **Rollout plan (zero/minimal downtime)**
   - Use expand/contract patterns: add columns, backfill, dual-write, cutover.
   - For indexes, use `CREATE INDEX CONCURRENTLY` when needed.
   - Document rollback and verification steps.

6) **Validate and verify**
   - Provide EXPLAIN (ANALYZE, BUFFERS) workflow.
   - Verify indexes are used and constraints hold.
   - Update `supabase/schema_docs` and check diffs.

## RLS patterns (use templates)

Use the policy templates in `references/templates.sql` and the checklist below. Default to:
- `owner access` for user-owned rows.
- `org membership` for shared resources.
- `role-based access` for admin/editor/viewer tiering.
- `service role bypass` only for background jobs.

RLS checklist:
- Define SELECT/INSERT/UPDATE/DELETE policies explicitly.
- Ensure INSERT uses `with check` and UPDATE uses `using` + `with check`.
- Confirm service-role bypass is isolated and minimal.
- Verify policies in Supabase Studio or with test queries.

## S3 integration pattern

Use the S3 metadata pattern in `references/examples.md`:
- Store `bucket`, `key`, `content_type`, `size_bytes`, `checksum/etag`, `owner_id`, `org_id`, and timestamps.
- Keep access control in Postgres with RLS (presigned URL generation uses service role).
- Ensure lifecycle and deletion are consistent (DB row + object).

## Do-not-do guardrails

- Do not run destructive DDL in production (drops, truncates, or rewrites) without explicit approval.
- Do not put metadata blobs inside `external_ids` (IDs only).
- Do not create broad RLS policies without least-privilege checks.
- Do not backfill without an escape hatch or rate limits.
- Do not ignore index maintenance for hot paths.

## Database Design Review Checklist

- [ ] Tables modeled with clear PKs, FKs, and nullability.
- [ ] FK cascade rules documented and intentional.
- [ ] RLS policies defined for select/insert/update/delete.
- [ ] Service-role bypass only where necessary.
- [ ] Indexes match query filters/sorts/joins.
- [ ] Migration plan is expand/contract with rollback.
- [ ] Backfill approach is idempotent and safe.
- [ ] EXPLAIN plan documented for hot queries.
- [ ] Growth expectations and partitioning considerations documented.
- [ ] S3 metadata and lifecycle alignment defined (if files involved).

## Examples (load when needed)

- See `references/examples.md` for:
  - New table + RLS + indexes + migration plan + verification.
  - S3 file metadata table + RLS.
  - Multi-tenant access control example.
