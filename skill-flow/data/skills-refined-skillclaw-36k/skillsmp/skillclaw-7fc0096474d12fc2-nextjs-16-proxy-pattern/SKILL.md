---
name: nextjs-16-proxy-pattern
description: Use this skill when implementing the new proxy pattern in Next.js 16 for authentication, route protection, and request interception.
---

# Next.js 16 Proxy Pattern

This skill covers the new **proxy pattern** introduced in Next.js 16, which replaces the legacy `middleware.ts` approach. The proxy is optimized for Vercel's serverless environment and provides cleaner semantics.

## Key Changes in Next.js 16

### File and Function Renaming

- **File Renaming**: `middleware.ts` → `proxy.ts`
- **Function Renaming**: `export function middleware()` → `export function proxy()`

### Runtime Changes

- The proxy runs in the `nodejs` runtime (not `edge` runtime).
- Configuration updates include changes like `skipMiddlewareUrlNormalize` to `skipProxyUrlNormalize`.

## Project Implementation

### Protected Routes Example

The `proxy.ts` file implements authentication-based route protection. Here are examples of protected and public routes:

**Protected Routes:**
- `/diary` - User personal diary
- `/collections` - User quote collections
- `/episodes` - Episode ratings and notes
- `/characters` - Comments and follows

**Public Routes:**
- `/` - Home page
- `/guide` - Public guide
- `/login` - Sign-in page
- `/register` - Sign-up page
- `/api` - API routes (handled separately)

### Route Pattern Matching

To protect routes correctly, ensure both variants are covered:

```typescript
const protectedPaths = [
  "/diary",
  "/collections",
  "/episodes", // Protects /episodes (list)
  "/episodes/", // Protects /episodes/ (with trailing)
  "/characters", // Protects /characters (list)
  "/characters/", // Protects /characters/ (with trailing)
];
```

### Example of Request Interception

Here’s how to implement authentication checks in the new proxy pattern:

```typescript
// proxy.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function proxy(request: NextRequest) {
  const cookieStore = await import('next/headers').then(m => m.cookies());
  const token = cookieStore.get('auth-token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
};
```

## When to Use This Skill

Use this skill when:
- Setting up request interception (authentication, redirects, headers)
- Replacing old middleware functionality with proxy
- Implementing authentication checks before page rendering
- Adding/modifying request/response headers
- Performing redirects based on request conditions
- Working with cookies or authentication in the request flow