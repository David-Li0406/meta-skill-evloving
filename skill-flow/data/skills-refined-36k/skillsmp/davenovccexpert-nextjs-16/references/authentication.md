<overview>
Authentication in Next.js 16 using the Data Access Layer (DAL) pattern. Proxy/middleware is NOT safe for auth - always verify at data access point.
</overview>

<key_principle>
**CVE-2025-29927 lesson:** Middleware authentication can be bypassed under load.

**Solution:** Data Access Layer (DAL) pattern - verify auth at every data access point.

```
Client Request
    ↓
proxy.ts (check cookie EXISTS, not validity)
    ↓
Server Component / Server Action
    ↓
Data Access Layer (VALIDATE session here)
    ↓
Database / API
```
</key_principle>

<dal_implementation>
**Core DAL file:**

```typescript
// lib/dal.ts
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { cache } from 'react'
import { SignJWT, jwtVerify } from 'jose'

const secretKey = process.env.AUTH_SECRET!
const key = new TextEncoder().encode(secretKey)

// Session type
interface Session {
  userId: string
  email: string
  role: 'user' | 'admin'
  expiresAt: Date
}

// Cached user fetch - runs once per request
export const getUser = cache(async () => {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session?.value) {
    return null
  }

  try {
    const { payload } = await jwtVerify(session.value, key)
    return payload as Session
  } catch {
    return null
  }
})

// Require authentication
export async function requireAuth() {
  const user = await getUser()
  if (!user) {
    redirect('/login')
  }
  return user
}

// Require specific role
export async function requireRole(role: 'admin') {
  const user = await requireAuth()
  if (user.role !== role) {
    redirect('/unauthorized')
  }
  return user
}

// Create session
export async function createSession(userId: string, email: string, role: string) {
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days

  const session = await new SignJWT({ userId, email, role, expiresAt })
    .setProtectedHeader({ alg: 'HS256' })
    .setExpirationTime('7d')
    .sign(key)

  const cookieStore = await cookies()
  cookieStore.set('session', session, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    expires: expiresAt,
    path: '/',
  })
}

// Delete session
export async function deleteSession() {
  const cookieStore = await cookies()
  cookieStore.delete('session')
}
```
</dal_implementation>

<usage_patterns>
<pattern name="protected-page">
**Protect a page:**

```tsx
// app/(dashboard)/dashboard/page.tsx
import { requireAuth } from '@/lib/dal'

export default async function DashboardPage() {
  const user = await requireAuth()  // Redirects if not authenticated

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
      <DashboardContent userId={user.userId} />
    </div>
  )
}
```
</pattern>

<pattern name="protected-layout">
**Protect a route group:**

```tsx
// app/(dashboard)/layout.tsx
import { requireAuth } from '@/lib/dal'

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const user = await requireAuth()

  return (
    <div className="flex">
      <Sidebar user={user} />
      <main>{children}</main>
    </div>
  )
}
```

**Note:** Layout checks run on initial load but not on every navigation. Always check in pages/components that need fresh auth.
</pattern>

<pattern name="protected-server-action">
**Protect Server Actions:**

```typescript
// lib/actions/profile.ts
'use server'

import { requireAuth } from '@/lib/dal'
import { updateTag } from 'next/cache'

export async function updateProfile(formData: FormData) {
  const user = await requireAuth()  // Always check!

  const name = formData.get('name') as string

  await db.users.update({
    where: { id: user.userId },
    data: { name },
  })

  updateTag(`user-${user.userId}`)
  return { success: true }
}
```
</pattern>

<pattern name="conditional-ui">
**Conditional rendering based on auth:**

```tsx
// components/Header.tsx
import { getUser } from '@/lib/dal'
import Link from 'next/link'

export async function Header() {
  const user = await getUser()

  return (
    <header>
      <nav>
        <Link href="/">Home</Link>
        {user ? (
          <>
            <Link href="/dashboard">Dashboard</Link>
            <LogoutButton />
          </>
        ) : (
          <Link href="/login">Login</Link>
        )}
      </nav>
    </header>
  )
}
```
</pattern>

<pattern name="role-based-access">
**Role-based access control:**

```tsx
// app/admin/page.tsx
import { requireRole } from '@/lib/dal'

export default async function AdminPage() {
  const admin = await requireRole('admin')

  return <AdminDashboard />
}

// lib/actions/admin.ts
'use server'

export async function deleteUser(userId: string) {
  const admin = await requireRole('admin')

  await db.users.delete({ where: { id: userId } })
  updateTag('users')
}
```
</pattern>
</usage_patterns>

<auth_actions>
**Login/Logout Server Actions:**

```typescript
// lib/actions/auth.ts
'use server'

import { createSession, deleteSession } from '@/lib/dal'
import { redirect } from 'next/navigation'
import bcrypt from 'bcryptjs'

export async function login(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Validate input
  if (!email || !password) {
    return { error: 'Email and password are required' }
  }

  // Find user
  const user = await db.users.findUnique({ where: { email } })
  if (!user) {
    return { error: 'Invalid credentials' }
  }

  // Verify password
  const valid = await bcrypt.compare(password, user.passwordHash)
  if (!valid) {
    return { error: 'Invalid credentials' }
  }

  // Create session
  await createSession(user.id, user.email, user.role)

  redirect('/dashboard')
}

export async function logout() {
  await deleteSession()
  redirect('/login')
}

export async function register(formData: FormData) {
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  // Validate
  if (!email || !password || password.length < 8) {
    return { error: 'Invalid input' }
  }

  // Check if exists
  const existing = await db.users.findUnique({ where: { email } })
  if (existing) {
    return { error: 'Email already registered' }
  }

  // Create user
  const passwordHash = await bcrypt.hash(password, 12)
  const user = await db.users.create({
    data: { email, passwordHash, role: 'user' },
  })

  // Create session
  await createSession(user.id, user.email, user.role)

  redirect('/dashboard')
}
```
</auth_actions>

<proxy_usage>
**Proxy for basic redirect (optional, adds UX but not security):**

```typescript
// proxy.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Only check cookie EXISTS - NOT validity
  const hasSession = request.cookies.has('session')

  // Redirect unauthenticated users from protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!hasSession) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Redirect authenticated users from auth pages
  if (request.nextUrl.pathname.startsWith('/login')) {
    if (hasSession) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/register'],
}
```

**Important:** This is only for UX (faster redirects). Real auth happens in DAL.
</proxy_usage>

<auth_libraries>
**Auth.js (NextAuth) v5:**

```bash
npm install next-auth@beta
```

```typescript
// auth.ts
import NextAuth from 'next-auth'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        email: {},
        password: {},
      },
      authorize: async (credentials) => {
        // Validate credentials
        const user = await validateUser(credentials)
        return user
      },
    }),
  ],
})

// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers

// Use in DAL
import { auth } from '@/auth'

export async function getUser() {
  const session = await auth()
  return session?.user ?? null
}
```

**Clerk:**

```bash
npm install @clerk/nextjs
```

```typescript
// middleware.ts (Clerk uses its own middleware)
import { clerkMiddleware } from '@clerk/nextjs/server'
export default clerkMiddleware()

// In components
import { currentUser } from '@clerk/nextjs/server'

export default async function Page() {
  const user = await currentUser()
  // ...
}
```
</auth_libraries>

<anti_patterns>
<anti_pattern name="proxy-only-auth">
**Problem:** Relying only on proxy for authentication

**Why bad:** Can be bypassed, doesn't protect Server Actions

**Fix:** Always verify in DAL, treat proxy as UX optimization only
</anti_pattern>

<anti_pattern name="client-side-auth">
**Problem:** Auth checks only on client

```tsx
'use client'
export function ProtectedContent() {
  const { user } = useAuth()
  if (!user) return null  // BAD - server still renders content
  return <SecretData />
}
```

**Fix:** Protect on server, hydrate on client
</anti_pattern>
</anti_patterns>
