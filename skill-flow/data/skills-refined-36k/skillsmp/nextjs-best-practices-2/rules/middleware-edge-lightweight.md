---
title: Keep Middleware Lightweight
impact: MEDIUM-HIGH
impactDescription: Middleware runs on every matched request - heavy logic adds latency
tags: middleware, edge, performance, latency
---

## Keep Middleware Lightweight

Middleware runs on the Edge Runtime before every matched request. Heavy operations block the entire request, adding latency to every page load.

**Incorrect (heavy middleware):**

```typescript
// middleware.ts
import { NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
  // ❌ Database query on every request
  const user = await db.users.findUnique({
    where: { id: request.cookies.get('userId')?.value }
  })

  // ❌ External API call
  const permissions = await fetch('https://auth.example.com/check', {
    body: JSON.stringify({ userId: user?.id })
  })

  // ❌ Heavy computation
  const analytics = computeComplexAnalytics(request)

  // ❌ Large data processing
  const recommendations = await generatePersonalizedContent(user)

  return NextResponse.next()
}
```

**Correct (lightweight middleware):**

```typescript
// middleware.ts
import { NextResponse } from 'next/server'

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  // ✓ Simple token validation (no DB)
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // ✓ Quick JWT decode (no verification - verify in route)
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      if (payload.exp < Date.now() / 1000) {
        return NextResponse.redirect(new URL('/login', request.url))
      }
    } catch {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // ✓ Simple header manipulation
  const response = NextResponse.next()
  response.headers.set('x-request-id', crypto.randomUUID())

  return response
}

// Use matcher to limit which routes run middleware
export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
}
```

**Move heavy logic to routes:**

```typescript
// middleware.ts - just redirect
export function middleware(request: NextRequest) {
  if (!request.cookies.get('session')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

// app/dashboard/page.tsx - full auth check
export default async function Dashboard() {
  const session = await getServerSession() // Full validation here
  if (!session) redirect('/login')

  const user = await getUser(session.userId)
  return <DashboardContent user={user} />
}
```

Reference: [Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)
