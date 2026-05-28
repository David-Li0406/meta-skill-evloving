---
title: Use config.matcher for Efficiency
impact: MEDIUM-HIGH
impactDescription: Prevents middleware from running on unnecessary routes
tags: middleware, matcher, routing, optimization
---

## Use config.matcher for Efficiency

Without a matcher, middleware runs on every request including static assets. Use matcher to limit middleware to only the routes that need it.

**Incorrect (no matcher):**

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  // ❌ Runs on EVERY request:
  // - Every page navigation
  // - Every static asset (_next/static/*)
  // - Every image
  // - Every API route
  // - Favicon, robots.txt, etc.

  console.log('Middleware:', request.nextUrl.pathname)
  return NextResponse.next()
}

// No config - runs everywhere 😱
```

**Correct (targeted with matcher):**

```typescript
// middleware.ts
import { NextResponse } from 'next/server'

export function middleware(request: NextRequest) {
  // Only runs on matched routes
  return NextResponse.next()
}

export const config = {
  matcher: [
    // Match all paths except static files and images
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ]
}
```

**Common matcher patterns:**

```typescript
export const config = {
  // Protected routes only
  matcher: ['/dashboard/:path*', '/account/:path*', '/admin/:path*'],
}

// API routes only
export const config = {
  matcher: ['/api/:path*'],
}

// Everything except API and static
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}

// Specific paths with regex
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/((?!public).)*', // API except /api/public/*
  ],
}

// Multiple matchers with different needs
export const config = {
  matcher: [
    // Auth required
    '/dashboard/:path*',
    '/settings/:path*',
    // Rate limiting
    '/api/:path*',
    // Localization
    '/(en|es|fr)/:path*',
  ],
}
```

**Conditional logic inside middleware:**

```typescript
export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname

  // Auth check only for dashboard
  if (path.startsWith('/dashboard')) {
    if (!request.cookies.get('token')) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Rate limit only for API
  if (path.startsWith('/api')) {
    // Rate limiting logic
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
}
```

Reference: [Middleware Matcher](https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher)
