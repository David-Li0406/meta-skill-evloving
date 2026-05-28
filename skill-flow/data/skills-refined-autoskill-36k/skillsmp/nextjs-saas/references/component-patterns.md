# Component Patterns

## Critical Rule: No Inline Styles

Every component that needs custom styling beyond Tailwind utilities must have a companion `.module.css` file. Never use `style={{ }}` props.

```typescript
// BAD
<div style={{ width: collapsed ? '60px' : '280px' }}>

// GOOD - use data attributes + CSS Module
<div className={styles.sidebar} data-collapsed={collapsed}>
```

See `references/styling.md` for the complete CSS Modules pattern.

## Server vs Client Components

### Default: Server Components

Server Components are the default in App Router. They:
- Run only on the server
- Can directly access databases, file system, env vars
- Don't add to client bundle size
- Cannot use hooks or browser APIs

```typescript
// app/(dashboard)/projects/page.tsx
// This is a Server Component (no 'use client' directive)
import { createClient } from '@/utils/supabase/server'

export default async function ProjectsPage() {
  const supabase = await createClient()
  const { data: projects } = await supabase.from('projects').select()

  return (
    <div>
      <h1>Projects</h1>
      <ProjectsList projects={projects} />
    </div>
  )
}
```

### When to Use Client Components

Add `'use client'` directive when you need:

| Need | Example |
|------|---------|
| React hooks | `useState`, `useEffect`, `useContext` |
| Event handlers | `onClick`, `onChange`, `onSubmit` |
| Browser APIs | `localStorage`, `window`, `navigator` |
| Interactivity | Forms, modals, dropdowns, toggles |
| Third-party client libs | Chart libraries, drag-and-drop |

```typescript
// components/shared/theme-toggle.tsx
'use client'

import { useState, useEffect } from 'react'
import { Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function ThemeToggle() {
  const [dark, setDark] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('theme')
    if (stored === 'dark') setDark(true)
  }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  }, [dark])

  return (
    <Button variant="ghost" size="icon" onClick={() => setDark(!dark)}>
      {dark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  )
}
```

### Composition Pattern

Keep Server Components at the top, pass data down to Client Components:

```typescript
// app/(dashboard)/projects/page.tsx (Server Component)
import { createClient } from '@/utils/supabase/server'
import { ProjectsTable } from './_components/projects-table'

export default async function ProjectsPage() {
  const supabase = await createClient()
  const { data: projects } = await supabase.from('projects').select()

  // Server fetches data, Client handles interactivity
  return <ProjectsTable initialProjects={projects ?? []} />
}
```

```typescript
// app/(dashboard)/projects/_components/projects-table.tsx (Client Component)
'use client'

import { useState } from 'react'

interface Project {
  id: string
  name: string
  status: string
}

export function ProjectsTable({ initialProjects }: { initialProjects: Project[] }) {
  const [projects, setProjects] = useState(initialProjects)
  const [filter, setFilter] = useState('')

  const filtered = projects.filter(p =>
    p.name.toLowerCase().includes(filter.toLowerCase())
  )

  return (
    <div>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter projects..."
        className="mb-4 px-3 py-2 border rounded"
      />
      <table>
        {/* Table content */}
      </table>
    </div>
  )
}
```

## Shadcn/ui Integration

### Installation

```bash
pnpm dlx shadcn@latest init
```

Choose these options:
- Style: `new-york` (cleaner, more professional)
- Base color: `slate` (neutral, works for SaaS)
- CSS variables: `yes` (enables theming)

### Configuration

```json
// components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui"
  }
}
```

### Adding Components

```bash
# Add individual components
pnpm dlx shadcn@latest add button dialog dropdown-menu

# Add multiple at once
pnpm dlx shadcn@latest add button card dialog input label select tabs
```

### Usage

```typescript
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'

export function CreateProjectDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create Project</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Project</DialogTitle>
        </DialogHeader>
        {/* Form content */}
      </DialogContent>
    </Dialog>
  )
}
```

## Loading States

### Route-Level Loading

```typescript
// app/(dashboard)/projects/loading.tsx
export default function Loading() {
  return (
    <div className="space-y-4">
      <div className="h-8 w-48 bg-muted animate-pulse rounded" />
      <div className="h-64 bg-muted animate-pulse rounded" />
    </div>
  )
}
```

### Suspense Boundaries

```typescript
// app/(dashboard)/projects/page.tsx
import { Suspense } from 'react'
import { ProjectsList } from './_components/projects-list'
import { ProjectsListSkeleton } from './_components/skeleton'

export default function ProjectsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Projects</h1>
      <Suspense fallback={<ProjectsListSkeleton />}>
        <ProjectsList />
      </Suspense>
    </div>
  )
}
```

## Error Handling

### Route Error Boundary

```typescript
// app/(dashboard)/projects/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-xl font-semibold mb-2">Something went wrong</h2>
      <p className="text-muted-foreground mb-4">
        {error.message || 'An unexpected error occurred'}
      </p>
      <Button onClick={reset}>Try again</Button>
    </div>
  )
}
```

### Global Error Boundary

```typescript
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h2 className="text-xl font-semibold mb-4">Something went wrong</h2>
          <button onClick={reset}>Try again</button>
        </div>
      </body>
    </html>
  )
}
```

## Forms with Server Actions

### Form Component

```typescript
// components/forms/project-form.tsx
'use client'

import { useActionState } from 'react'
import { createProject } from '@/app/(dashboard)/projects/actions'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export function ProjectForm() {
  const [state, action, pending] = useActionState(createProject, null)

  return (
    <form action={action} className="space-y-4">
      <div>
        <Label htmlFor="name">Project Name</Label>
        <Input id="name" name="name" required />
        {state?.errors?.name && (
          <p className="text-sm text-destructive mt-1">{state.errors.name}</p>
        )}
      </div>

      <div>
        <Label htmlFor="description">Description</Label>
        <Input id="description" name="description" />
      </div>

      {state?.error && (
        <p className="text-sm text-destructive">{state.error}</p>
      )}

      <Button type="submit" disabled={pending}>
        {pending ? 'Creating...' : 'Create Project'}
      </Button>
    </form>
  )
}
```

### Server Action

```typescript
// app/(dashboard)/projects/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { createClient } from '@/utils/supabase/server'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  description: z.string().max(500).optional(),
})

export async function createProject(prevState: unknown, formData: FormData) {
  const parsed = schema.safeParse({
    name: formData.get('name'),
    description: formData.get('description'),
  })

  if (!parsed.success) {
    return { errors: parsed.error.flatten().fieldErrors }
  }

  const supabase = await createClient()
  const { error } = await supabase.from('projects').insert(parsed.data)

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/projects')
  redirect('/projects')
}
```

## Collapsible Sidebar Pattern

For stateful components like collapsible sidebars, use CSS Modules with `data-*` attributes.

See `references/styling.md` → "Stateful Component with Module" for the complete sidebar implementation with CSS Module.
