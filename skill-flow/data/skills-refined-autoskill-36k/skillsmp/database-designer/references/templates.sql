-- Supabase/Postgres templates for TRR Backend

-- 1) Table template (core schema)
create table if not exists core.example_table (
  id uuid primary key default gen_random_uuid(),
  show_id uuid references core.shows(id) on delete cascade,
  name text not null,
  status text not null default 'active',
  metadata jsonb not null default '{}'::jsonb,
  created_by uuid,
  deleted_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- 2) updated_at trigger (core schema)
create or replace function core.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger example_table_set_updated_at
before update on core.example_table
for each row
execute function core.set_updated_at();

-- 3) RLS: enable + owner access
alter table core.example_table enable row level security;

create policy example_table_owner_select
on core.example_table
for select
using (auth.uid() = created_by);

create policy example_table_owner_insert
on core.example_table
for insert
with check (auth.uid() = created_by);

create policy example_table_owner_update
on core.example_table
for update
using (auth.uid() = created_by)
with check (auth.uid() = created_by);

create policy example_table_owner_delete
on core.example_table
for delete
using (auth.uid() = created_by);

-- 4) RLS: org membership (template, requires org_id + org_memberships table)
-- Assumes core.org_memberships(org_id, user_id, role)
create policy example_table_org_read
on core.example_table
for select
using (
  exists (
    select 1
    from core.org_memberships om
    where om.org_id = example_table.org_id
      and om.user_id = auth.uid()
  )
);

-- 5) RLS: role-based access (template)
create policy example_table_org_write
on core.example_table
for insert, update
with check (
  exists (
    select 1
    from core.org_memberships om
    where om.org_id = example_table.org_id
      and om.user_id = auth.uid()
      and om.role in ('admin', 'editor')
  )
);

-- 6) Service-role bypass (use sparingly)
create policy example_table_service_role
on core.example_table
for all
using (auth.role() = 'service_role')
with check (auth.role() = 'service_role');

-- 7) Index templates
create index concurrently if not exists example_table_show_id_idx
  on core.example_table (show_id);

create index concurrently if not exists example_table_status_partial_idx
  on core.example_table (status)
  where status = 'active';

create index concurrently if not exists example_table_not_deleted_idx
  on core.example_table (id)
  where deleted_at is null;

create index concurrently if not exists example_table_metadata_gin
  on core.example_table using gin (metadata);

-- 8) Audit table (optional)
create table if not exists core.audit_log (
  id uuid primary key default gen_random_uuid(),
  actor_id uuid,
  action text not null,
  entity_table text not null,
  entity_id uuid,
  changes jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
