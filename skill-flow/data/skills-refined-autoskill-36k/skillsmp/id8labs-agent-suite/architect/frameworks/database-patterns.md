# Database Patterns Framework

## Purpose

Design database schemas that are simple, performant, and maintainable. Optimized for Supabase/PostgreSQL.

---

## Core Principles

### 1. Start Simple

- One table per core entity
- No premature normalization
- Add complexity only when proven necessary

### 2. Supabase-First

- Leverage built-in features
- Use RLS for authorization
- Embrace real-time where beneficial

### 3. Type-Safe

- Generate TypeScript types from schema
- Use enums for constrained values
- Document with comments

---

## Common Patterns

### User Profile Pattern

```sql
-- Users are created by Supabase Auth
-- This extends with app-specific data

create table public.profiles (
  id uuid references auth.users(id) on delete cascade primary key,
  email text unique not null,
  full_name text,
  avatar_url text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Auto-create profile on signup
create function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name, avatar_url)
  values (
    new.id,
    new.email,
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  );
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- RLS
alter table public.profiles enable row level security;

create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);
```

### Tenant/Organization Pattern

```sql
create table public.organizations (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  slug text unique not null,
  owner_id uuid references public.profiles(id) not null,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

create table public.organization_members (
  id uuid default gen_random_uuid() primary key,
  organization_id uuid references public.organizations(id) on delete cascade not null,
  user_id uuid references public.profiles(id) on delete cascade not null,
  role text not null default 'member' check (role in ('owner', 'admin', 'member')),
  created_at timestamptz default now() not null,
  unique(organization_id, user_id)
);

-- RLS: Users can view orgs they belong to
create policy "View member organizations"
  on public.organizations for select
  using (
    exists (
      select 1 from public.organization_members
      where organization_id = id
      and user_id = auth.uid()
    )
  );
```

### Owned Resource Pattern

```sql
-- Resources owned by a user

create table public.projects (
  id uuid default gen_random_uuid() primary key,
  owner_id uuid references public.profiles(id) on delete cascade not null,
  name text not null,
  description text,
  status text not null default 'active' check (status in ('active', 'archived', 'deleted')),
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Index for common queries
create index projects_owner_id_idx on public.projects(owner_id);
create index projects_status_idx on public.projects(status);

-- RLS
alter table public.projects enable row level security;

create policy "Users can CRUD own projects"
  on public.projects for all
  using (auth.uid() = owner_id);
```

### Shared Resource Pattern

```sql
-- Resources shared between users

create table public.documents (
  id uuid default gen_random_uuid() primary key,
  owner_id uuid references public.profiles(id) not null,
  title text not null,
  content jsonb default '{}'::jsonb,
  visibility text not null default 'private'
    check (visibility in ('private', 'team', 'public')),
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

create table public.document_shares (
  id uuid default gen_random_uuid() primary key,
  document_id uuid references public.documents(id) on delete cascade not null,
  user_id uuid references public.profiles(id) on delete cascade not null,
  permission text not null default 'view' check (permission in ('view', 'edit', 'admin')),
  created_at timestamptz default now() not null,
  unique(document_id, user_id)
);

-- RLS: Can view if owner, shared with, or public
create policy "View accessible documents"
  on public.documents for select
  using (
    owner_id = auth.uid()
    or visibility = 'public'
    or exists (
      select 1 from public.document_shares
      where document_id = id
      and user_id = auth.uid()
    )
  );
```

### Soft Delete Pattern

```sql
-- Never actually delete, just mark

alter table public.projects add column deleted_at timestamptz;

-- Update RLS to exclude deleted
create policy "View non-deleted projects"
  on public.projects for select
  using (
    auth.uid() = owner_id
    and deleted_at is null
  );

-- Soft delete function
create function public.soft_delete_project(project_id uuid)
returns void as $$
begin
  update public.projects
  set deleted_at = now()
  where id = project_id
  and owner_id = auth.uid();
end;
$$ language plpgsql security definer;
```

### Audit Log Pattern

```sql
create table public.audit_logs (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id),
  action text not null,
  table_name text not null,
  record_id uuid not null,
  old_data jsonb,
  new_data jsonb,
  created_at timestamptz default now() not null
);

-- Trigger function for auditing
create function public.audit_trigger()
returns trigger as $$
begin
  if TG_OP = 'INSERT' then
    insert into public.audit_logs (user_id, action, table_name, record_id, new_data)
    values (auth.uid(), 'INSERT', TG_TABLE_NAME, NEW.id, to_jsonb(NEW));
    return NEW;
  elsif TG_OP = 'UPDATE' then
    insert into public.audit_logs (user_id, action, table_name, record_id, old_data, new_data)
    values (auth.uid(), 'UPDATE', TG_TABLE_NAME, NEW.id, to_jsonb(OLD), to_jsonb(NEW));
    return NEW;
  elsif TG_OP = 'DELETE' then
    insert into public.audit_logs (user_id, action, table_name, record_id, old_data)
    values (auth.uid(), 'DELETE', TG_TABLE_NAME, OLD.id, to_jsonb(OLD));
    return OLD;
  end if;
end;
$$ language plpgsql security definer;

-- Apply to tables that need auditing
create trigger projects_audit
  after insert or update or delete on public.projects
  for each row execute procedure public.audit_trigger();
```

---

## Supabase-Specific Patterns

### Generated TypeScript Types

```bash
# Generate types from schema
npx supabase gen types typescript --project-id $PROJECT_ID > src/types/database.ts
```

```typescript
// Using generated types
import { Database } from '@/types/database'

type Project = Database['public']['Tables']['projects']['Row']
type NewProject = Database['public']['Tables']['projects']['Insert']
type UpdateProject = Database['public']['Tables']['projects']['Update']
```

### Real-Time Subscriptions

```typescript
// Subscribe to changes
const subscription = supabase
  .channel('projects')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'projects',
      filter: `owner_id=eq.${userId}`
    },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()
```

### Edge Function Database Access

```typescript
// supabase/functions/process-webhook/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js'

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // Use service role for admin operations
  const { data, error } = await supabase
    .from('projects')
    .update({ processed: true })
    .eq('id', projectId)

  return new Response(JSON.stringify({ success: true }))
})
```

---

## RLS Best Practices

### Policy Naming Convention

```sql
-- Format: "{action} {description}"
create policy "Select own rows" on public.projects for select ...
create policy "Insert own rows" on public.projects for insert ...
create policy "Update own rows" on public.projects for update ...
create policy "Delete own rows" on public.projects for delete ...
```

### Common RLS Patterns

```sql
-- Owner-only access
using (auth.uid() = owner_id)

-- Organization member access
using (
  exists (
    select 1 from public.organization_members
    where organization_id = organizations.id
    and user_id = auth.uid()
  )
)

-- Role-based access
using (
  exists (
    select 1 from public.organization_members
    where organization_id = organizations.id
    and user_id = auth.uid()
    and role in ('owner', 'admin')
  )
)

-- Public read, owner write
for select using (true)
for insert using (auth.uid() = owner_id)
for update using (auth.uid() = owner_id)
```

---

## Indexing Strategy

### When to Add Indexes

```sql
-- Foreign keys (auto-created in some DBs, manual in Postgres)
create index projects_owner_id_idx on public.projects(owner_id);

-- Frequently filtered columns
create index projects_status_idx on public.projects(status);

-- Frequently sorted columns
create index projects_created_at_idx on public.projects(created_at desc);

-- Composite for common query patterns
create index projects_owner_status_idx on public.projects(owner_id, status);

-- Partial index for common filters
create index active_projects_idx on public.projects(owner_id)
  where status = 'active';
```

### When NOT to Add Indexes

- Tables with < 1000 rows
- Columns rarely filtered/sorted
- Columns with low cardinality (true/false)
- Before you have actual slow queries

---

## Migration Workflow

```bash
# Create migration
npx supabase migration new create_projects_table

# Edit migration file
# supabase/migrations/TIMESTAMP_create_projects_table.sql

# Apply locally
npx supabase db reset

# Push to remote
npx supabase db push

# Or generate diff from local changes
npx supabase db diff -f my_changes
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No RLS | Security vulnerability | Always enable RLS |
| RLS in app code | Can be bypassed | Use database policies |
| Over-normalization | Complexity, slow queries | Start simple |
| No indexes on FKs | Slow joins | Index foreign keys |
| Storing files in DB | Bloat, slow | Use Supabase Storage |
| UUIDs as text | Inefficient | Use native uuid type |
| No timestamps | Hard to debug | Always add created_at, updated_at |
