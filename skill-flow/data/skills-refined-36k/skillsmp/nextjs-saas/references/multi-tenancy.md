# Multi-Tenancy Patterns

## Overview

Multi-tenancy allows a single application to serve multiple isolated customers (tenants). This guide covers:

- Data model design
- Row-Level Security (RLS)
- Tenant context management
- Data isolation patterns

## Data Model

### Hierarchical Structure

```
User (auth.users)
  └── Tenant (organization, workspace, team)
        ├── Tenant Settings
        ├── Projects
        ├── Assets
        └── Other tenant-scoped data
```

### Database Schema

```sql
-- Tenants table
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User-tenant membership (many-to-many)
CREATE TABLE tenant_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  role TEXT DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member')),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(tenant_id, user_id)
);

-- Tenant-scoped data (example: projects)
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tenant_members_user ON tenant_members(user_id);
CREATE INDEX idx_tenant_members_tenant ON tenant_members(tenant_id);
CREATE INDEX idx_projects_tenant ON projects(tenant_id);
```

## Row-Level Security (RLS)

RLS ensures data isolation at the database level.

### Enable RLS

```sql
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenant_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

### Tenant Policies

```sql
-- Users can view tenants they belong to
CREATE POLICY "Users can view own tenants"
  ON tenants FOR SELECT
  USING (
    id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid()
    )
  );

-- Only owners can update tenant settings
CREATE POLICY "Owners can update tenants"
  ON tenants FOR UPDATE
  USING (
    id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid() AND role = 'owner'
    )
  );
```

### Data Policies

```sql
-- Users can view projects in their tenants
CREATE POLICY "Users can view tenant projects"
  ON projects FOR SELECT
  USING (
    tenant_id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid()
    )
  );

-- Users can create projects in their tenants
CREATE POLICY "Users can create projects"
  ON projects FOR INSERT
  WITH CHECK (
    tenant_id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid()
    )
  );

-- Users can update projects in their tenants
CREATE POLICY "Users can update projects"
  ON projects FOR UPDATE
  USING (
    tenant_id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid()
    )
  );

-- Only admins/owners can delete projects
CREATE POLICY "Admins can delete projects"
  ON projects FOR DELETE
  USING (
    tenant_id IN (
      SELECT tenant_id FROM tenant_members
      WHERE user_id = auth.uid() AND role IN ('owner', 'admin')
    )
  );
```

## Tenant Context

For the TenantProvider Context implementation, see `references/state-management.md` → "Basic Context Structure".

The key addition for multi-tenancy: fetch tenants from Supabase and persist `activeTenantId` to localStorage.

### Tenant Switcher Component

```typescript
// components/shared/tenant-switcher.tsx
'use client'

import { Check, ChevronsUpDown, PlusCircle } from 'lucide-react'
import { useTenant } from '@/contexts/tenant-context'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useState } from 'react'

export function TenantSwitcher() {
  const { tenants, activeTenant, setActiveTenant, loading } = useTenant()
  const [open, setOpen] = useState(false)

  if (loading) {
    return (
      <Button variant="outline" className="w-[200px]" disabled>
        Loading...
      </Button>
    )
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          className="w-[200px] justify-between"
        >
          {activeTenant?.name ?? 'Select workspace'}
          <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search..." />
          <CommandList>
            <CommandEmpty>No workspace found.</CommandEmpty>
            <CommandGroup>
              {tenants.map((tenant) => (
                <CommandItem
                  key={tenant.id}
                  value={tenant.id}
                  onSelect={() => {
                    setActiveTenant(tenant.id)
                    setOpen(false)
                  }}
                >
                  <Check
                    className={cn(
                      'mr-2 h-4 w-4',
                      activeTenant?.id === tenant.id ? 'opacity-100' : 'opacity-0'
                    )}
                  />
                  {tenant.name}
                </CommandItem>
              ))}
            </CommandGroup>
            <CommandSeparator />
            <CommandGroup>
              <CommandItem onSelect={() => setOpen(false)}>
                <PlusCircle className="mr-2 h-4 w-4" />
                Create workspace
              </CommandItem>
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
```

## Scoped Data Fetching

### Server-Side

```typescript
// app/(dashboard)/projects/page.tsx
import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'

export default async function ProjectsPage() {
  const supabase = await createClient()

  const cookieStore = await cookies()
  const activeTenantId = cookieStore.get('activeTenantId')?.value

  if (!activeTenantId) {
    return <div>Please select a workspace</div>
  }

  const { data: projects } = await supabase
    .from('projects')
    .select('*')
    .eq('tenant_id', activeTenantId)
    .order('created_at', { ascending: false })

  return <ProjectsList projects={projects ?? []} />
}
```

### Client-Side

```typescript
// hooks/use-projects.ts
'use client'

import { useState, useEffect, useCallback } from 'react'
import { createClient } from '@/utils/supabase/client'
import { useTenant } from '@/contexts/tenant-context'

export function useProjects() {
  const { activeTenantId } = useTenant()
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  const supabase = createClient()

  const fetchProjects = useCallback(async () => {
    if (!activeTenantId) {
      setProjects([])
      setLoading(false)
      return
    }

    setLoading(true)
    const { data } = await supabase
      .from('projects')
      .select('*')
      .eq('tenant_id', activeTenantId)
      .order('created_at', { ascending: false })

    setProjects(data ?? [])
    setLoading(false)
  }, [activeTenantId, supabase])

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  return { projects, loading, refresh: fetchProjects }
}
```

## Creating Tenant-Scoped Data

```typescript
// app/(dashboard)/projects/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { cookies } from 'next/headers'
import { createClient } from '@/utils/supabase/server'

export async function createProject(formData: FormData) {
  const supabase = await createClient()

  const cookieStore = await cookies()
  const tenantId = cookieStore.get('activeTenantId')?.value

  if (!tenantId) {
    return { error: 'No workspace selected' }
  }

  const { error } = await supabase.from('projects').insert({
    name: formData.get('name'),
    tenant_id: tenantId,
  })

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/projects')
  return { success: true }
}
```

## Best Practices

1. **Always use RLS** - Never rely solely on application-level filtering
2. **Explicit tenant_id** - Include tenant_id in queries as defense-in-depth
3. **Validate tenant access** - Check user has access before operations
4. **Audit logging** - Log tenant-scoped actions
5. **Tenant-aware caching** - Include tenant_id in cache keys
6. **Test isolation** - Write tests that verify data isolation
