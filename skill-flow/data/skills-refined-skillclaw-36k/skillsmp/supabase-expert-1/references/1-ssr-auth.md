# 1. Next.js 16 SSR & Auth Flow

**Impact: CRITICAL**

In 2026, all Supabase authentication in Next.js must be cookie-based and server-controlled to prevent session fixation and XSS-based JWT theft.

## 1.1 The Runtime Client Setup

You must use separate client initializers for Server Components, Server Actions, and Middleware.

### Server Client (Components/Actions)
```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet) => {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // The `setAll` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  )
}
```

## 1.2 Secure User Verification

**NEVER** trust `getSession()` on the server. Always use `getUser()`.

**Incorrect (Vulnerable to spoofing):**
```typescript
const { data: { session } } = await supabase.auth.getSession()
if (session) { /* ... */ }
```

**Correct (Secure):**
```typescript
const { data: { user }, error } = await supabase.auth.getUser()
if (user) { /* ... */ }
```
`getUser()` makes a network call to the Supabase Auth server to verify the JWT's integrity and expiration.

## 1.3 Automatic Session Refresh (Middleware)

Middleware ensures that the session is refreshed before the user hits a Server Component.

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => request.cookies.set(name, value))
          response = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options))
        },
      },
    }
  )

  await supabase.auth.getUser()
  return response
}
```

## 1.4 Partial Pre-rendering (PPR) Compatibility

When using PPR in Next.js 16, wrap authenticated components in `<Suspense>`.

```tsx
import { Suspense } from 'react'
import { UserProfile, Skeleton } from './components'

export default function Dashboard() {
  return (
    <main>
      <h1>Dashboard</h1>
      <Suspense fallback={<Skeleton />}>
        <UserProfile /> {/* This triggers dynamic rendering */}
      </Suspense>
    </main>
  )
}
```
The "Dashboard" header is pre-rendered statically, while the `UserProfile` (which calls `createClient`) is streamed once the session is verified.
