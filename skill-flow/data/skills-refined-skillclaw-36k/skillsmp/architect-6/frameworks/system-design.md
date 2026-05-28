# System Design Framework

## Purpose

Design system architecture that enables velocity while maintaining quality. Keep it simple until complexity is proven necessary.

---

## Core Principles

### 1. Start Monolithic

**Default architecture for MVP:**

```
┌─────────────────────────────────────────┐
│           NEXT.JS APPLICATION           │
├─────────────────────────────────────────┤
│  Pages/Routes │ Components │ Hooks      │
├─────────────────────────────────────────┤
│  API Routes   │ Server Actions          │
├─────────────────────────────────────────┤
│  Services     │ Utils      │ Types      │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│            SUPABASE                      │
│  Database │ Auth │ Storage │ Realtime   │
└─────────────────────────────────────────┘
```

### 2. Layer Responsibilities

| Layer | Responsibility | Don't Put Here |
|-------|----------------|----------------|
| **Pages/Routes** | Layout, routing, page-level data fetch | Business logic |
| **Components** | UI rendering, local state | API calls, data fetching |
| **Hooks** | Reusable stateful logic | Complex business rules |
| **API Routes** | HTTP handling, validation | Database queries directly |
| **Services** | Business logic, database ops | UI concerns |
| **Utils** | Pure helper functions | Stateful operations |

### 3. Data Flow

```
User Action
    │
    ▼
Component (UI)
    │
    ▼
Hook (if reusable) or direct call
    │
    ▼
API Route / Server Action
    │
    ▼
Service Layer
    │
    ▼
Database (via Supabase client)
    │
    ▼
Response back up the chain
```

---

## Component Patterns

### File Organization

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Auth-required routes
│   │   ├── dashboard/
│   │   └── settings/
│   ├── (marketing)/       # Public routes
│   │   ├── page.tsx       # Landing
│   │   └── pricing/
│   ├── api/               # API routes
│   │   └── v1/
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── forms/             # Form components
│   ├── layouts/           # Layout components
│   └── features/          # Feature-specific
├── lib/
│   ├── supabase/          # Supabase clients
│   │   ├── client.ts      # Browser client
│   │   ├── server.ts      # Server client
│   │   └── admin.ts       # Admin client
│   ├── services/          # Business logic
│   └── utils/             # Helper functions
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript types
└── config/                # App configuration
```

### Component Types

**Server Components (default in App Router):**
```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: projects } = await supabase
    .from('projects')
    .select('*')

  return <ProjectList projects={projects} />
}
```

**Client Components (when needed):**
```typescript
// components/features/project-form.tsx
'use client'

import { useState } from 'react'

export function ProjectForm() {
  const [name, setName] = useState('')
  // Interactive logic here
}
```

**When to Use Client Components:**
- User interactions (clicks, inputs)
- Browser APIs (localStorage, geolocation)
- React state/effects
- Third-party client libraries

---

## API Design Patterns

### Route Handler Pattern

```typescript
// app/api/v1/projects/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data, error } = await supabase
    .from('projects')
    .select('*')

  if (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }

  return NextResponse.json(data)
}

export async function POST(request: Request) {
  const supabase = await createClient()
  const body = await request.json()

  // Validate with Zod
  const validated = projectSchema.safeParse(body)
  if (!validated.success) {
    return NextResponse.json(
      { error: validated.error.issues },
      { status: 400 }
    )
  }

  const { data, error } = await supabase
    .from('projects')
    .insert(validated.data)
    .select()
    .single()

  if (error) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    )
  }

  return NextResponse.json(data, { status: 201 })
}
```

### Server Actions Pattern

```typescript
// lib/actions/projects.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'

export async function createProject(formData: FormData) {
  const supabase = await createClient()

  const { error } = await supabase
    .from('projects')
    .insert({
      name: formData.get('name'),
      description: formData.get('description')
    })

  if (error) {
    return { error: error.message }
  }

  revalidatePath('/dashboard')
  return { success: true }
}
```

---

## State Management

### Hierarchy

```
1. Server State (Supabase + React Query/SWR)
   └── For: Database data, user data

2. URL State (searchParams, pathname)
   └── For: Filters, pagination, tabs

3. Local State (useState)
   └── For: Form inputs, UI toggles

4. Global Client State (Zustand)
   └── For: Theme, sidebar state, modals
```

### Implementation

**Server State (React Query):**
```typescript
// hooks/use-projects.ts
import { useQuery } from '@tanstack/react-query'
import { createClient } from '@/lib/supabase/client'

export function useProjects() {
  const supabase = createClient()

  return useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('projects')
        .select('*')
      if (error) throw error
      return data
    }
  })
}
```

**Global State (Zustand):**
```typescript
// lib/stores/ui-store.ts
import { create } from 'zustand'

interface UIStore {
  sidebarOpen: boolean
  toggleSidebar: () => void
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen }))
}))
```

---

## Error Handling

### Error Boundaries

```typescript
// app/error.tsx
'use client'

export default function Error({
  error,
  reset
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

### API Error Pattern

```typescript
// lib/utils/api-response.ts
export function apiError(message: string, status: number = 500) {
  return NextResponse.json(
    { error: message, success: false },
    { status }
  )
}

export function apiSuccess<T>(data: T, status: number = 200) {
  return NextResponse.json(
    { data, success: true },
    { status }
  )
}
```

---

## When to Add Complexity

### Signals That You Need More

| Signal | Consider Adding |
|--------|-----------------|
| API routes > 20 | Service layer abstraction |
| State shared across many components | Global state management |
| Complex form validation | Form library (react-hook-form) |
| Heavy client-side computation | Web Workers |
| Real-time features needed | Supabase Realtime |
| Background jobs needed | Edge Functions or external service |
| Search needed | Supabase full-text or Algolia |

### Signals to Keep It Simple

- Less than 10 API endpoints
- Team size = 1
- MVP stage
- No complex domain logic
- Standard CRUD operations

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Prop drilling 5+ levels | Maintenance nightmare | Context or state library |
| API calls in components | Coupling, no caching | Use hooks with React Query |
| Business logic in API routes | Hard to test | Extract to service layer |
| Massive components | Hard to maintain | Extract smaller components |
| Over-abstracting early | Premature complexity | Wait until pattern repeats 3x |
