---
name: nextjs-16-proxy-patterns-and-authentication
description: Use this skill when implementing authentication, request interception, and route protection in Next.js 16 using the new proxy pattern.
---

# Next.js 16 Proxy Patterns and Authentication

## Overview

In Next.js 16, the `middleware` file convention has been replaced with `proxy`, clarifying the focus on network boundaries and routing. This skill provides guidance on implementing authentication, request interception, and modifying requests before they reach your application.

## Key Changes in Next.js 16

1. **File Renaming**: `middleware.ts` is now `proxy.ts`.
2. **Function Renaming**: `export function middleware()` is now `export function proxy()`.
3. **Runtime Change**: Proxy runs in the Node.js runtime instead of the Edge runtime.
4. **Configuration Updates**: The configuration option `skipMiddlewareUrlNormalize` is now `skipProxyUrlNormalize`.

## When to Use This Skill

Use this skill when:
- Setting up request interception (authentication, redirects, headers).
- Replacing old middleware functionality with the new proxy pattern.
- Implementing authentication checks before page rendering.
- Adding or modifying request/response headers.
- Performing redirects based on request conditions.
- Working with cookies or authentication in the request flow.

## Project Implementation

### Basic Proxy Example

```typescript
// proxy.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Public routes that don't require authentication
  const isPublicRoute = 
    pathname === '/login' || 
    pathname === '/register' || 
    pathname.startsWith('/api/auth');

  // Protected routes that require authentication
  const isProtectedRoute = 
    pathname.startsWith('/dashboard') || 
    pathname.startsWith('/profile') ||
    pathname.startsWith('/api/private');

  if (isProtectedRoute && !isPublicRoute) {
    const cookieStore = await import('next/headers').then(m => m.cookies());
    const token = cookieStore.get('auth-token');

    if (!token) {
      const loginUrl = new URL('/login', request.url);
      loginUrl.searchParams.set('callbackUrl', pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### Matcher Configuration

The `config.matcher` pattern determines which routes the proxy runs on:

```typescript
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

### Session Validation

To validate the session, you can use the following pattern:

```typescript
export async function proxy(request: NextRequest) {
  const cookieStore = await import('next/headers').then(m => m.cookies());
  const token = cookieStore.get('auth-token');

  if (!token) {
    // Handle unauthenticated access
  }

  return NextResponse.next();
}
```

### Redirect Authenticated Users Away

To prevent authenticated users from accessing login or registration pages:

```typescript
if (isAuthenticated && (pathname === '/login' || pathname === '/register')) {
  return NextResponse.redirect(new URL('/', request.url));
}
```

## Common Patterns

### A. Simple Path Protection

```typescript
const protectedPaths = ['/admin', '/dashboard'];
const isProtected = protectedPaths.includes(pathname);

if (isProtected && !isAuthenticated) {
  return NextResponse.redirect(new URL('/login', request.url));
}
```

### B. Role-Based Protection

```typescript
const adminPaths = ['/admin'];
const isAdmin = session?.user?.role === 'admin';

if (adminPaths.some((p) => pathname.startsWith(p)) && !isAdmin) {
  return NextResponse.redirect(new URL('/unauthorized', request.url));
}
```

### C. CORS Headers

To handle CORS in your proxy:

```typescript
const allowedOrigins = ['https://example.com'];

export async function proxy(request: NextRequest) {
  const origin = request.headers.get('origin') ?? '';
  const isAllowedOrigin = allowedOrigins.includes(origin);

  const response = NextResponse.next();
  if (isAllowedOrigin) {
    response.headers.set('Access-Control-Allow-Origin', origin);
  }

  return response;
}
```

## Debugging and Testing

### Enable Logging

```typescript
const DEBUG = process.env.NODE_ENV === 'development';

export async function proxy(request: NextRequest) {
  if (DEBUG) {
    console.log(`[PROXY] ${request.method} ${request.nextUrl.pathname}`);
  }
  return NextResponse.next();
}
```

### Testing Protected Routes

You can test protected routes using curl:

```bash
# Without authentication
curl -i http://localhost:3000/dashboard
# Should redirect to login

# With session cookie
curl -i -b "session=..." http://localhost:3000/dashboard
# Should return 200
```

## Security Best Practices

1. **Always Validate Session State**: Ensure that the session is properly validated.
2. **Use Secure Headers**: Set appropriate headers for authenticated requests.
3. **Never Log Sensitive Data**: Avoid logging sensitive information such as tokens.

## Migration from Middleware

### Step 1: Rename the Function

```typescript
// BEFORE
export function middleware(request) {}

// AFTER
export async function proxy(request) {}
```

### Step 2: Rename the File

```bash
mv middleware.ts proxy.ts
```

### Step 3: Update Imports

Most cases won't need imports to change, as they are framework-level.

### Step 4: Verify Config

Ensure the matcher configuration is correct.

## Resources

- [Next.js 16 Upgrade Guide](https://nextjs.org/docs/getting-started/upgrading)
- [Next.js Proxy Documentation](https://nextjs.org/docs/app/building-your-application/routing/middleware)

## Version

This skill is based on **Next.js 16.1.1** (January 2026).