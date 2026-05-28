---
name: nextjs
description: >
  Implement Next.js 15 patterns for PhotoVault including Server Components,
  Client Components, Server Actions, and API routes. Use when working with
  app router, middleware, data fetching, caching, loading states, or debugging
  hydration errors. Includes Next.js 15 async params and caching changes.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\nextjs-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/nextjs-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/nextjs-[task-name]-plan.md
   Write critique to: docs/claude/plans/nextjs-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Next.js 15 Integration

## Core Principles

### Server Components Are the Default

Every component is a Server Component unless marked with `'use client'`. Only add it when you NEED:
- `useState`, `useEffect`, or other React hooks
- Browser APIs (`window`, `document`, `localStorage`)
- Event handlers (`onClick`, `onChange`, etc.)

### Composition Over Conversion

Don't make entire pages client-side for one button.

```typescript
// ❌ BAD: Entire page client-side
'use client'
export default function Page() {
  const [count, setCount] = useState(0)
  return (
    <div>
      <h1>Static Title</h1>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  )
}

// ✅ GOOD: Only interactive part is client
// page.tsx (Server Component)
import { Counter } from './Counter'
export default function Page() {
  return (
    <div>
      <h1>Static Title</h1>
      <Counter />
    </div>
  )
}

// Counter.tsx (Client Component)
'use client'
export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

## Anti-Patterns

**Importing server-only code in client components**
```typescript
// WRONG: Build will fail
'use client'
import { createServerClient } from '@/lib/supabase/server'
```

**Sequential fetching when parallel is possible**
```typescript
// WRONG: Waterfall
const user = await getUser()
const posts = await getPosts()

// RIGHT: Parallel
const [user, posts] = await Promise.all([getUser(), getPosts()])
```

**Not handling loading states**
```typescript
// WRONG: Blank screen during fetch
export default async function Page() {
  const data = await slowFetch()
  return <div>{data}</div>
}

// RIGHT: Add loading.tsx
export default function Loading() {
  return <Skeleton />
}
```

**Forgetting revalidation after mutations**
```typescript
// WRONG: UI shows stale data
'use server'
export async function createPost(data: FormData) {
  await db.posts.create({ ... })
}

// RIGHT: Revalidate
'use server'
import { revalidatePath } from 'next/cache'
export async function createPost(data: FormData) {
  await db.posts.create({ ... })
  revalidatePath('/posts')
}
```

## Next.js 15 Specific Changes

### Async Request APIs

```typescript
// cookies() and headers() are now async
import { cookies } from 'next/headers'

// Old (Next.js 14)
const cookieStore = cookies()

// New (Next.js 15)
const cookieStore = await cookies()
```

### Async Params

```typescript
// params and searchParams are now Promises

// Old (Next.js 14)
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>
}

// New (Next.js 15)
export default async function Page({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  return <div>{id}</div>
}
```

### Caching Defaults Changed

```typescript
// Next.js 14: fetch cached by default
// Next.js 15: fetch NOT cached by default

// To cache in Next.js 15:
const data = await fetch(url, { cache: 'force-cache' })

// With revalidation:
const data = await fetch(url, { next: { revalidate: 3600 } })
```

## Server Action Pattern

```typescript
// src/app/actions/galleries.ts
'use server'

import { createServerClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const CreateGallerySchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
})

export async function createGallery(formData: FormData) {
  const result = CreateGallerySchema.safeParse({
    name: formData.get('name'),
    description: formData.get('description'),
  })

  if (!result.success) {
    return { success: false, errors: result.error.flatten().fieldErrors }
  }

  const supabase = await createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, errors: { _form: 'Not authenticated' } }
  }

  const { data, error } = await supabase
    .from('photo_galleries')
    .insert({ photographer_id: user.id, name: result.data.name })
    .select()
    .single()

  if (error) {
    return { success: false, errors: { _form: 'Failed to create gallery' } }
  }

  revalidatePath('/photographer/galleries')
  redirect(`/photographer/galleries/${data.id}`)
}
```

## API Route Pattern

```typescript
// src/app/api/galleries/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createServerClient } from '@/lib/supabase/server'

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params  // Next.js 15: await params
    const supabase = await createServerClient()

    const { data, error } = await supabase
      .from('photo_galleries')
      .select('*, photos(*)')
      .eq('id', id)
      .single()

    if (error) {
      if (error.code === 'PGRST116') {
        return NextResponse.json({ error: 'Not found' }, { status: 404 })
      }
      throw error
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error('GET error:', error)
    return NextResponse.json({ error: 'Internal error' }, { status: 500 })
  }
}
```

## PhotoVault Configuration

### App Structure

```
src/app/
├── (public)/           # No auth required
├── (auth)/             # Auth routes
├── photographer/       # Protected photographer portal
├── client/             # Protected client portal
├── api/                # API routes
└── layout.tsx          # Root layout
```

### Environment Variables

```bash
# Public (browser)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# Server-only (no NEXT_PUBLIC_)
SUPABASE_SERVICE_ROLE_KEY=
STRIPE_SECRET_KEY=
```

### Development

```bash
npm run dev -- -p 3002  # PhotoVault uses port 3002
```

## Debugging Checklist

1. Check for hydration errors in browser console
2. Verify `'use client'` is where it should be
3. Did you `await params` in Next.js 15?
4. Check env vars have correct `NEXT_PUBLIC_` prefix
5. Did you call `revalidatePath` after mutation?
