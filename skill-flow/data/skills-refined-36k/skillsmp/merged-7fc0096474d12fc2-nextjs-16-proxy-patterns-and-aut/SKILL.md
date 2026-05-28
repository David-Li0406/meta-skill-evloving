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

## Complete Proxy Example with Authentication

### Implementation

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
    // Access cookies asynchronously
    const cookieStore = await import('next/headers').then(m => m.cookies());
    const token = cookieStore.get('auth-token');

    if (!token) {
      // Redirect to login page
      const loginUrl = new URL('/login', request.url);
      loginUrl.searchParams.set('callbackUrl', pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  // Continue with the request
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## Configuration Update

### Next.js 16 Configuration

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  skipProxyUrlNormalize: true,
}

module.exports = nextConfig;
```

## Common Patterns

### 1. Simple Authentication Check

```typescript
export async function proxy(request: NextRequest) {
  const cookieStore = await import('next/headers').then(m => m.cookies());
  const token = cookieStore.get('auth-token');

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}
```

### 2. Redirecting Based on Conditions

```typescript
if (isProtectedRoute && !token) {
  const loginUrl = new URL('/login', request.url);
  loginUrl.searchParams.set('callbackUrl', pathname);
  return NextResponse.redirect(loginUrl);
}
```

### 3. Modifying Response Headers

```typescript
const response = NextResponse.next();
response.headers.set('x-custom-header', 'proxy-value');
return response;
```

## Debugging Tips

- **Check Matcher Configuration**: Ensure the matcher includes the routes you want to protect.
- **Session Handling**: Verify that the session or authentication token is being passed correctly in the headers.

## Resources

- [Next.js 16 Upgrade Guide](https://nextjs.org/docs/getting-started/upgrading)
- [Next.js Proxy Documentation](https://nextjs.org/docs/app/building-your-application/routing/middleware)

## Conclusion

This skill provides a comprehensive guide for implementing the new proxy pattern in Next.js 16, focusing on authentication and request handling. Use it to ensure secure and efficient routing in your applications.