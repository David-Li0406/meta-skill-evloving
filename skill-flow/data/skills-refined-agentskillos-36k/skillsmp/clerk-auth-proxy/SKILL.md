---
name: clerk-auth-proxy
version: 1.0.0
lastUpdated: 2026-01-18
description: Implement Clerk authentication with Next.js 16 proxy pattern, session claims, onboarding gates, and user metadata management. Use when working with authentication, authorization, or user session management.
tags: [clerk, authentication, next.js, proxy, session-claims, onboarding]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Add authentication check to a server action
  - Implement onboarding gate for new users
  - Update user metadata after completing a flow
  - Create protected route with role-based access
---

# Clerk Authentication & Proxy Skill

Implement Clerk authentication in Next.js 16 using the proxy pattern (not middleware!), manage session claims, and handle user metadata.

> **Reference Files:**
> - [proxy-patterns.md](./proxy-patterns.md) - Next.js 16 proxy configuration
> - [session-claims.md](./session-claims.md) - Custom session claims and metadata
> - [onboarding-gate.md](./onboarding-gate.md) - Onboarding flow patterns
> - [examples.md](./examples.md) - Complete code examples
> - [testing.md](./testing.md) - Testing authenticated flows

## Critical: Next.js 16 Uses Proxy, NOT Middleware

**IMPORTANT**: Next.js 16 introduced the proxy pattern which replaces the traditional `middleware.ts` for Clerk.

| Next.js Version | File Name | Runtime |
|-----------------|-----------|---------|
| 15 and earlier | `middleware.ts` | Edge Runtime |
| **16+** | **`proxy.ts`** | **Node.js Runtime** |

The proxy pattern provides:
- Full Node.js runtime (not Edge limitations)
- Better async/await support
- Access to all Node.js APIs
- Improved performance

## Quick Start

### 1. Authentication Check in Server Actions

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import type { ActionResponse } from "~/lib/action-types";

export async function myAction(data: InputType): ActionResponse<OutputType> {
  // 1. Always check authentication first
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Your business logic here
  // ...
}
```

### 2. Authentication Check in Page Loaders

```typescript
import { auth } from "@clerk/nextjs/server";
import { redirect, unauthorized } from "next/navigation";

async function loadData() {
  const { userId, isAuthenticated, sessionClaims } = await auth();

  if (!isAuthenticated) {
    return unauthorized();
  }

  // Check custom session claims
  if (sessionClaims?.metadata.onboardingComplete !== true) {
    redirect("/onboarding");
  }

  // Load user data...
}
```

### 3. Updating User Metadata

```typescript
import { clerkClient } from "@clerk/nextjs/server";

const client = await clerkClient();
await client.users.updateUser(userId, {
  publicMetadata: {
    onboardingComplete: true,
    role: "user"
  }
});
```

## Key Concepts

### Authentication Object

The `auth()` function returns:

```typescript
interface AuthObject {
  userId: string | null;           // Clerk user ID
  isAuthenticated: boolean;        // Is user logged in
  sessionClaims: CustomJwtSessionClaims | null;  // Custom claims
  redirectToSignIn: (opts?) => Response;  // Redirect helper
}
```

### Session Claims Type Definition

Define custom claims in `types/clerk.d.ts`:

```typescript
export {};

declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      onboardingComplete?: boolean;
      role?: "user" | "admin";
    };
  }
}
```

### Public vs Private Metadata

| Type | Visibility | Use Case |
|------|------------|----------|
| `publicMetadata` | Included in session token, readable on client | Onboarding status, roles, preferences |
| `privateMetadata` | Server-only, never sent to client | Internal flags, sensitive data |
| `unsafeMetadata` | User-editable via Clerk components | Profile preferences, settings |

## File Locations

| Purpose | File |
|---------|------|
| Proxy configuration | `proxy.ts` (root) |
| Session claims types | `types/clerk.d.ts` |
| Auth helpers | `features/auth/server/db/user.ts` |
| Providers setup | `components/providers.tsx` |

## Common Patterns

### Protected Server Action

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";

export async function protectedAction(): ActionResponse {
  const { userId, isAuthenticated } = await auth();

  if (!isAuthenticated || !userId) {
    return { success: false, error: "Unauthorized" };
  }

  // Action logic...
}
```

### Protected Page with Redirect

```typescript
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function ProtectedPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  // Page content...
}
```

### Onboarding Gate Pattern

See [onboarding-gate.md](./onboarding-gate.md) for complete implementation.

## Security Checklist

When implementing authentication:

1. **Always verify `userId`** - Never trust client-provided user IDs
2. **Check authorization** - Verify user owns the resource they're accessing
3. **Use `server-only`** - Mark auth modules with `server-only` package
4. **Log auth events** - Log authentication failures for security monitoring
5. **Handle edge cases** - Expired sessions, revoked tokens

## Running and Testing

```bash
# Type check
npm run type-check

# Run auth-related tests
npm run test -- features/auth

# E2E tests with authentication
npm run test:e2e
```

## Related Skills

- `server-actions` - For implementing server actions with auth checks
- `firebase-firestore` - For database operations after authentication
