# Proxy Patterns (Next.js 16)

## Overview

Next.js 16 introduced the proxy pattern which replaces `middleware.ts` for authentication.

**Key file: `proxy.ts` in project root**

## Basic Proxy Structure

```typescript
/**
 * Next.js 16 Proxy (formerly middleware.ts)
 * This file runs on the Node.js runtime and defines the app's network boundary.
 * @see https://nextjs.org/docs/app/guides/upgrading/version-16#middleware-to-proxy
 */
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

// Define route matchers
const isPublicRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)"]);
const isApiRoute = createRouteMatcher(["/api(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  const { isAuthenticated, redirectToSignIn } = await auth();

  // Public routes - allow access
  if (isPublicRoute(req)) {
    return NextResponse.next();
  }

  // Protected routes - require authentication
  if (!isAuthenticated) {
    return redirectToSignIn({ returnBackUrl: req.url });
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    // Skip Next.js internals, static files, and API routes
    "/((?!_next|api|trpc|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)"
  ]
};
```

## Route Matchers

### Creating Route Matchers

```typescript
import { createRouteMatcher } from "@clerk/nextjs/server";

// Exact routes
const isHomePage = createRouteMatcher(["/"]);

// Wildcard routes (matches /sign-in, /sign-in/factor-one, etc.)
const isAuthRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)"]);

// Multiple routes
const isPublicRoute = createRouteMatcher([
  "/",
  "/about",
  "/pricing",
  "/sign-in(.*)",
  "/sign-up(.*)"
]);

// API routes
const isApiRoute = createRouteMatcher(["/api(.*)", "/trpc(.*)"]);
```

### Matcher Patterns

| Pattern | Matches |
|---------|---------|
| `/path` | Exact path only |
| `/path(.*)` | Path and all sub-paths |
| `/path/(.*)` | Only sub-paths (not `/path` itself) |
| `/(path1\|path2)` | Either path1 or path2 |

## Auth Object Properties

```typescript
export default clerkMiddleware(async (auth, req) => {
  const {
    isAuthenticated,     // boolean - is user logged in
    userId,              // string | null - Clerk user ID
    sessionClaims,       // CustomJwtSessionClaims | null
    redirectToSignIn,    // (opts?) => Response - redirect helper
    protect,             // (opts?) => void - throws if unauthorized
  } = await auth();
});
```

## Common Proxy Patterns

### Pattern 1: Simple Public/Private Split

```typescript
const isPublicRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)", "/"]);

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    const { isAuthenticated, redirectToSignIn } = await auth();
    if (!isAuthenticated) {
      return redirectToSignIn({ returnBackUrl: req.url });
    }
  }
  return NextResponse.next();
});
```

### Pattern 2: Role-Based Access

```typescript
const isAdminRoute = createRouteMatcher(["/admin(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  const { isAuthenticated, sessionClaims, redirectToSignIn } = await auth();

  if (isAdminRoute(req)) {
    if (!isAuthenticated) {
      return redirectToSignIn({ returnBackUrl: req.url });
    }
    if (sessionClaims?.metadata?.role !== "admin") {
      return NextResponse.redirect(new URL("/unauthorized", req.url));
    }
  }

  return NextResponse.next();
});
```

### Pattern 3: Onboarding Gate (Project Pattern)

```typescript
const isPublicRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)"]);
const isOnboardingRoute = createRouteMatcher(["/onboarding(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  const { isAuthenticated, sessionClaims, redirectToSignIn } = await auth();

  // Allow onboarding route for authenticated users
  if (isAuthenticated && isOnboardingRoute(req)) {
    return NextResponse.next();
  }

  // Redirect unauthenticated users to sign-in
  if (!isAuthenticated && !isPublicRoute(req)) {
    return redirectToSignIn({ returnBackUrl: req.url });
  }

  // Redirect users who haven't completed onboarding
  if (isAuthenticated && !sessionClaims?.metadata?.onboardingComplete) {
    const onboardingUrl = new URL("/onboarding", req.url);
    return NextResponse.redirect(onboardingUrl);
  }

  return NextResponse.next();
});
```

### Pattern 4: API Route Protection

```typescript
const isApiRoute = createRouteMatcher(["/api(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  if (isApiRoute(req)) {
    const { isAuthenticated } = await auth();
    if (!isAuthenticated) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }
  }
  return NextResponse.next();
});
```

## Config Matcher

The `config.matcher` determines which routes the proxy runs on:

```typescript
export const config = {
  matcher: [
    // Standard matcher - skip static files and Next.js internals
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",

    // Always run for API routes
    "/(api|trpc)(.*)"
  ]
};
```

### Common Exclusions

| Pattern | Purpose |
|---------|---------|
| `_next` | Next.js build output |
| `api` | API routes (handle separately) |
| `\\.(?:css\|js)` | Static assets |
| `\\.(?:png\|jpg\|webp)` | Images |
| `favicon.ico` | Favicon |

## Debugging

### Log Route Matching

```typescript
export default clerkMiddleware(async (auth, req) => {
  console.log("Proxy running for:", req.nextUrl.pathname);
  console.log("Is public:", isPublicRoute(req));

  const { isAuthenticated, userId } = await auth();
  console.log("Is authenticated:", isAuthenticated);
  console.log("User ID:", userId);

  // ...
});
```

### Check Session Claims

```typescript
export default clerkMiddleware(async (auth, req) => {
  const { sessionClaims } = await auth();
  console.log("Session claims:", JSON.stringify(sessionClaims, null, 2));
  // ...
});
```

## Migration from Middleware

If migrating from Next.js 15 middleware:

1. Rename `middleware.ts` to `proxy.ts`
2. Update imports (same, but runtime changes)
3. Remove Edge Runtime limitations workarounds
4. Test all protected routes

```typescript
// Before (middleware.ts - Edge Runtime)
import { clerkMiddleware } from "@clerk/nextjs/server";
export default clerkMiddleware();
export const config = { matcher: [...] };

// After (proxy.ts - Node.js Runtime)
import { clerkMiddleware } from "@clerk/nextjs/server";
export default clerkMiddleware();
export const config = { matcher: [...] };
// File location and name changed, API is the same
```
