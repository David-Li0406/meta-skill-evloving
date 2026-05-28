<overview>
proxy.ts replaces middleware.ts in Next.js 16. It runs on Node.js runtime and is strictly for routing operations (rewrites, redirects, headers). NOT for authentication or business logic.
</overview>

<key_changes>
**Next.js 15 → Next.js 16:**

| Aspect | Next.js 15 | Next.js 16 |
|--------|------------|------------|
| File | `middleware.ts` | `proxy.ts` |
| Export | `middleware()` | `proxy()` |
| Runtime | Edge or Node | Node only |
| Auth | Common (but problematic) | NOT recommended |
| Purpose | Various | Routing only |
</key_changes>

<migration>
**Automatic migration:**
```bash
npx @next/codemod@latest rename-middleware-to-proxy .
```

**Manual migration:**

1. Rename file:
```bash
mv src/middleware.ts src/proxy.ts
# OR
mv middleware.ts proxy.ts
```

2. Update export:
```typescript
// Before (middleware.ts)
export function middleware(request: NextRequest) {
  // ...
}

// After (proxy.ts)
export function proxy(request: NextRequest) {
  // ...
}
```

3. Remove runtime export:
```typescript
// REMOVE this line - proxy only runs on Node.js
export const runtime = 'edge'
```
</migration>

<valid_use_cases>
**Proxy IS for:**

<use_case name="redirects">
```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function proxy(request: NextRequest) {
  // Redirect old URLs
  if (request.nextUrl.pathname.startsWith('/old-blog')) {
    return NextResponse.redirect(
      new URL('/blog' + request.nextUrl.pathname.slice(9), request.url)
    )
  }

  return NextResponse.next()
}
```
</use_case>

<use_case name="rewrites">
```typescript
export function proxy(request: NextRequest) {
  // A/B testing via rewrite
  const bucket = request.cookies.get('ab-bucket')?.value || 'a'

  if (request.nextUrl.pathname === '/pricing') {
    return NextResponse.rewrite(
      new URL(`/pricing-${bucket}`, request.url)
    )
  }

  return NextResponse.next()
}
```
</use_case>

<use_case name="headers">
```typescript
export function proxy(request: NextRequest) {
  const response = NextResponse.next()

  // Add security headers
  response.headers.set('X-Frame-Options', 'DENY')
  response.headers.set('X-Content-Type-Options', 'nosniff')

  // Add request ID for tracing
  response.headers.set('X-Request-ID', crypto.randomUUID())

  return response
}
```
</use_case>

<use_case name="geo-routing">
```typescript
export function proxy(request: NextRequest) {
  const country = request.geo?.country || 'US'

  // Route to country-specific content
  if (request.nextUrl.pathname === '/') {
    return NextResponse.rewrite(
      new URL(`/${country.toLowerCase()}`, request.url)
    )
  }

  return NextResponse.next()
}
```
</use_case>

<use_case name="basic-session-check">
```typescript
export function proxy(request: NextRequest) {
  // ONLY check cookie existence, NOT validity
  const hasSession = request.cookies.has('session')

  // Protected routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !hasSession) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}
```

**Important:** This only checks if the cookie EXISTS. Actual session validation must happen in the Data Access Layer.
</use_case>
</valid_use_cases>

<invalid_use_cases>
**Proxy is NOT for:**

<anti_pattern name="auth-validation">
**Problem:** Validating sessions in proxy

```typescript
// BAD - don't do this in proxy
export async function proxy(request: NextRequest) {
  const session = request.cookies.get('session')

  // DON'T validate tokens here
  const user = await validateJWT(session?.value)
  if (!user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}
```

**Why:** CVE-2025-29927 showed middleware auth can be bypassed. Validation must happen at data access point.

**Fix:** Move to Data Access Layer
```typescript
// lib/dal.ts
export async function getUser() {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    redirect('/login')
  }

  // Validate HERE, not in proxy
  const user = await validateJWT(session.value)
  if (!user) {
    redirect('/login')
  }

  return user
}
```
</anti_pattern>

<anti_pattern name="database-calls">
**Problem:** Database access in proxy

```typescript
// BAD
export async function proxy(request: NextRequest) {
  const user = await db.users.findUnique({ where: { ... } })
  // ...
}
```

**Why:** Proxy should be fast and lightweight. DB calls add latency to every request.

**Fix:** Move to Server Components or API routes
</anti_pattern>

<anti_pattern name="business-logic">
**Problem:** Complex logic in proxy

```typescript
// BAD
export async function proxy(request: NextRequest) {
  const cart = await getCart()
  const hasSubscription = await checkSubscription()
  if (cart.total > 100 && !hasSubscription) {
    // Complex business rules...
  }
}
```

**Fix:** Handle in Server Components or Server Actions
</anti_pattern>
</invalid_use_cases>

<configuration>
**Matcher config (same as middleware):**

```typescript
// proxy.ts
export const config = {
  matcher: [
    // Match all paths except static files and API routes
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
}

// OR specific paths
export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

**Matcher patterns:**
- `/dashboard/:path*` - Match `/dashboard` and all sub-paths
- `/api/:path*` - Match all API routes
- `/((?!api|_next).*)` - Negative lookahead to exclude patterns
</configuration>

<auth_alternative>
**Recommended auth pattern for Next.js 16:**

```typescript
// 1. proxy.ts - Only check cookie existence
export function proxy(request: NextRequest) {
  const hasSession = request.cookies.has('session')

  if (request.nextUrl.pathname.startsWith('/dashboard') && !hasSession) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

// 2. lib/dal.ts - Validate session at data access
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import { cache } from 'react'

export const getUser = cache(async () => {
  const cookieStore = await cookies()
  const session = cookieStore.get('session')

  if (!session) {
    return null
  }

  const user = await validateSession(session.value)
  return user
})

export async function requireAuth() {
  const user = await getUser()
  if (!user) {
    redirect('/login')
  }
  return user
}

// 3. Any protected page/component
export default async function DashboardPage() {
  const user = await requireAuth()  // Auth check HERE

  return <Dashboard user={user} />
}

// 4. Server Actions - ALWAYS check auth
'use server'
export async function updateProfile(formData: FormData) {
  const user = await requireAuth()  // Auth check HERE too

  await db.users.update({
    where: { id: user.id },
    data: { ... }
  })
}
```
</auth_alternative>
