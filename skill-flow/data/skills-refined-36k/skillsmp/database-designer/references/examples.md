# TRR Examples

## Example 1: New table for show social profiles (core.shows)

Goal: store social handles per show with safe RLS and indexes.

Schema:
```sql
create table core.show_social_profiles (
  id uuid primary key default gen_random_uuid(),
  show_id uuid not null references core.shows(id) on delete cascade,
  platform text not null,
  handle text not null,
  url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index concurrently show_social_profiles_show_id_idx
  on core.show_social_profiles (show_id);
create unique index concurrently show_social_profiles_unique
  on core.show_social_profiles (show_id, platform, handle);

alter table core.show_social_profiles enable row level security;

-- Public read (common for show metadata)
create policy show_social_profiles_public_read
on core.show_social_profiles
for select
using (true);

-- Service role write
create policy show_social_profiles_service_write
on core.show_social_profiles
for insert, update, delete
using (auth.role() = 'service_role')
with check (auth.role() = 'service_role');
```

Rollout plan:
1) Add table + indexes + RLS policies.
2) Backfill from external sources via service-role ingestion.
3) Verify read paths with EXPLAIN and API.
4) Add updates to schema docs (`make schema-docs`).

Verification:
- `EXPLAIN (ANALYZE, BUFFERS) select * from core.show_social_profiles where show_id = $1;`
- Ensure policies allow read with anon and write only via service role.

## Example 2: S3 file metadata table for show assets

Goal: track S3 object metadata and align access control with RLS.

Schema:
```sql
create table core.show_assets (
  id uuid primary key default gen_random_uuid(),
  show_id uuid not null references core.shows(id) on delete cascade,
  bucket text not null,
  object_key text not null,
  content_type text,
  size_bytes bigint,
  checksum text,
  owner_id uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create unique index concurrently show_assets_unique
  on core.show_assets (bucket, object_key);
create index concurrently show_assets_show_id_idx
  on core.show_assets (show_id);

alter table core.show_assets enable row level security;

-- Read: public or org-based depending on product rules
create policy show_assets_public_read
on core.show_assets
for select
using (true);

-- Write: service role only (uploads / metadata updates)
create policy show_assets_service_write
on core.show_assets
for insert, update, delete
using (auth.role() = 'service_role')
with check (auth.role() = 'service_role');
```

Access control model:
- Presigned URL generation uses service-role or trusted server endpoints.
- DB rows are the source of truth for visibility.
- Use deletion workflows to remove both DB row and S3 object.
- Use upserts keyed on (bucket, object_key) for idempotency.

Consistency checks:
- Orphaned objects: S3 object exists without DB row.
- Orphaned rows: DB row exists without S3 object.
- Lifecycle: ensure DB deletion triggers S3 delete; add periodic reconciliation.

## Example 3: Multi-tenant shows (adding org_id)

Goal: scope `core.shows` rows by organization.

Migration:
```sql
alter table core.shows add column if not exists org_id uuid;

create table if not exists core.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists core.org_memberships (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references core.organizations(id) on delete cascade,
  user_id uuid not null,
  role text not null default 'member',
  created_at timestamptz not null default now()
);

create index concurrently org_memberships_org_user_idx
  on core.org_memberships (org_id, user_id);

alter table core.shows enable row level security;

create policy shows_org_read
on core.shows
for select
using (
  exists (
    select 1 from core.org_memberships om
    where om.org_id = core.shows.org_id
      and om.user_id = auth.uid()
  )
);

create policy shows_org_write
on core.shows
for insert, update
with check (
  exists (
    select 1 from core.org_memberships om
    where om.org_id = core.shows.org_id
      and om.user_id = auth.uid()
      and om.role in ('admin', 'editor')
  )
);
```

Rollout plan:
1) Add `org_id` nullable.
2) Backfill org_id for existing shows.
3) Enforce RLS after backfill.
4) Optionally make `org_id` not null in a later migration.
