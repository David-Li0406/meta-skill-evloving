---
name: nextjs-saas
description: Use when building multi-tenant SaaS with Next.js App Router and Supabase. Covers project structure, proxy pattern for auth, component patterns, state management, and Row-Level Security.
license: Complete terms in LICENSE.txt
---

# Next.js SaaS Application Patterns

Patterns and architecture for building production-grade, multi-tenant SaaS applications using Next.js 16+, React 19, App Router, Supabase auth and modern tooling.

## When to Use This Skill

- Starting a new Next.js SaaS project
- Adding multi-tenancy to an existing Next.js app
- Implementing the proxy pattern for auth (API vs UI routes)
- Setting up authentication with Supabase
- Integrating Shadcn/ui component library
- Implementing Context-based state management
- Structuring App Router projects for scale

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| Directory layout, route groups | `references/project-structure.md` |
| Proxy pattern, middleware auth | `references/proxy-pattern.md` |
| Server/Client components, Shadcn | `references/component-patterns.md` |
| Context, hooks, localStorage | `references/state-management.md` |
| Tailwind v4, CSS Modules, theming | `references/styling.md` |
| Supabase auth, server actions | `references/authentication.md` |
| RLS, tenant isolation, data scoping | `references/multi-tenancy.md` |
| App config, env vars, TypeScript | `references/configuration.md` |

## Recommended Stack

```
Framework:    Next.js 16+ (App Router, Turbopack)
Language:     TypeScript (strict mode)
Runtime:      React 19
Styling:      Tailwind CSS v4 + CSS Modules
Components:   Shadcn/ui + Radix primitives
Database:     Supabase (Postgres + Auth + RLS)
State:        React Context + localStorage
```

## Core Principles

### 1. Default to Server Components
Only add `'use client'` when you need interactivity (useState, onClick, browser APIs).

### 2. No Inline Styles - CSS Modules Required
Never use `style={{ }}` props. Every component with custom styling must have a companion `.module.css` file. Use `data-*` attributes for state-dependent styles.

### 3. Context Over Redux
For most SaaS apps, React Context + localStorage is sufficient. Only add Zustand/Redux for complex cross-tree state.

### 4. Proxy Pattern for Auth
Separate API route authentication (return 401 JSON) from UI route authentication (redirect to login). Never redirect API consumers.

### 5. Route Groups for Layouts
Use `(dashboard)`, `(marketing)`, `(auth)` to share layouts without affecting URLs.

### 6. RLS for Multi-Tenancy
Supabase Row-Level Security ensures data isolation at the database level - never rely on frontend filtering alone.

### 7. CSS Variables for Theming
Enable white-label/customization by using CSS custom properties that can be updated at runtime.

## Project Structure Overview

```
├── app/
│   ├── (dashboard)/        # Protected routes with shared layout
│   ├── (marketing)/        # Public marketing pages
│   ├── auth/               # OAuth callbacks
│   ├── login/              # Auth pages + server actions
│   └── api/                # API routes
├── components/
│   ├── ui/                 # Shadcn primitives
│   ├── shared/             # Cross-feature components
│   └── [feature]/          # Feature-specific
├── contexts/               # React Context providers
├── hooks/                  # Custom hooks
├── lib/                    # Utilities (cn, supabase client)
├── utils/
│   └── supabase/
│       ├── client.ts       # Browser client
│       ├── server.ts       # Server client
│       ├── middleware.ts   # Session refresh for UI routes
│       └── apiAuth.ts      # API route auth handler
├── types/                  # TypeScript definitions
├── config/                 # App configuration
└── proxy.ts                # Auth routing layer
```

See `references/project-structure.md` for detailed layout and route group patterns.

## The Proxy Pattern

The proxy pattern separates authentication handling for API routes vs UI routes:

```typescript
// proxy.ts
import { type NextRequest, NextResponse } from 'next/server'
import { updateSession } from '@/utils/supabase/middleware'
import { handleApiAuth } from '@/utils/supabase/apiAuth'

const PUBLIC_API_ROUTES = [
  '/api/health',
  '/api/auth/callback',
  '/api/webhooks/stripe',
]

export async function proxy(request: NextRequest) {
  const pathname = request.nextUrl.pathname

  // API routes: return 401 JSON, never redirect
  if (pathname.startsWith('/api/')) {
    if (PUBLIC_API_ROUTES.some(route => pathname.startsWith(route))) {
      return NextResponse.next()
    }
    return handleApiAuth(request)
  }

  // UI routes: may redirect to login
  return await updateSession(request)
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

**Key insight:** API consumers (mobile apps, webhooks, external services) expect 401 responses, not redirects. UI routes can redirect to login.

See `references/proxy-pattern.md` for full implementation details.

## Key Patterns at a Glance

### Server Component (Data Fetching)
```typescript
// app/(dashboard)/projects/page.tsx
import { createClient } from '@/utils/supabase/server'

export default async function ProjectsPage() {
  const supabase = await createClient()
  const { data } = await supabase.from('projects').select()
  return <ProjectsList projects={data} />
}
```

### Client Component (Interactivity)
```typescript
// components/shared/theme-toggle.tsx
'use client'
import { useState } from 'react'

export function ThemeToggle() {
  const [dark, setDark] = useState(false)
  return <button onClick={() => setDark(!dark)}>Toggle</button>
}
```

### Context Provider
```typescript
// contexts/tenant-context.tsx
'use client'
const TenantContext = createContext<TenantContextType | undefined>(undefined)

export function TenantProvider({ children }) {
  const [tenantId, setTenantId] = useState<string | null>(null)
  return (
    <TenantContext.Provider value={{ tenantId, setTenantId }}>
      {children}
    </TenantContext.Provider>
  )
}

export const useTenant = () => useContext(TenantContext)
```

### Server Action (Mutations)
```typescript
// app/login/actions.ts
'use server'
import { redirect } from 'next/navigation'
import { createClient } from '@/utils/supabase/server'

export async function login(formData: FormData) {
  const supabase = await createClient()
  const { error } = await supabase.auth.signInWithPassword({
    email: formData.get('email') as string,
    password: formData.get('password') as string
  })
  if (error) return { error: error.message }
  redirect('/dashboard')
}
```

### API Route Auth Handler
```typescript
// utils/supabase/apiAuth.ts
export async function handleApiAuth(request: NextRequest) {
  const response = NextResponse.next()

  const supabase = createServerClient(/* ... */)
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Inject user info for downstream handlers
  response.headers.set('X-User-Id', user.id)
  response.headers.set('X-User-Email', user.email || '')

  return response
}
```

## References

Detailed documentation for each topic area:

- **`references/project-structure.md`** - Directory conventions, route groups, file organization
- **`references/proxy-pattern.md`** - Auth routing, API vs UI handling, public routes
- **`references/component-patterns.md`** - Server vs Client components, Shadcn setup, composition
- **`references/state-management.md`** - Context patterns, custom hooks, persistence
- **`references/styling.md`** - Tailwind v4 config, CSS Modules, dynamic theming
- **`references/authentication.md`** - Supabase auth flow, server actions, OAuth
- **`references/multi-tenancy.md`** - RLS policies, tenant isolation, data scoping
- **`references/configuration.md`** - App config, environment variables, TypeScript setup
