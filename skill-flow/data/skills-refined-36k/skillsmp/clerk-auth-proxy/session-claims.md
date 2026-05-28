# Session Claims and User Metadata

## Overview

Clerk provides three types of user metadata:
- **publicMetadata** - Included in JWT, readable everywhere
- **privateMetadata** - Server-only, never in JWT
- **unsafeMetadata** - User-editable via Clerk components

## Type Definitions

### Custom Session Claims

Define custom JWT claims in `types/clerk.d.ts`:

```typescript
export {};

declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      onboardingComplete?: boolean;
      role?: "user" | "admin" | "moderator";
      plan?: "free" | "pro" | "enterprise";
      teamId?: string;
    };
  }
}
```

### User Public Metadata

The `UserPublicMetadata` interface extends with your custom fields:

```typescript
// types/clerk.d.ts
declare global {
  interface UserPublicMetadata {
    onboardingComplete?: boolean;
    role?: "user" | "admin" | "moderator";
    plan?: "free" | "pro" | "enterprise";
    teamId?: string;
  }

  interface CustomJwtSessionClaims {
    metadata: UserPublicMetadata;
  }
}
```

## Reading Session Claims

### In Proxy (proxy.ts)

```typescript
export default clerkMiddleware(async (auth, req) => {
  const { sessionClaims } = await auth();

  // Access custom claims
  const onboardingComplete = sessionClaims?.metadata?.onboardingComplete;
  const userRole = sessionClaims?.metadata?.role;

  if (userRole !== "admin") {
    return NextResponse.redirect(new URL("/unauthorized", req.url));
  }
});
```

### In Server Components

```typescript
import { auth } from "@clerk/nextjs/server";

export default async function Page() {
  const { sessionClaims } = await auth();

  const isAdmin = sessionClaims?.metadata?.role === "admin";
  const plan = sessionClaims?.metadata?.plan ?? "free";

  return (
    <div>
      {isAdmin && <AdminPanel />}
      <PlanBadge plan={plan} />
    </div>
  );
}
```

### In Server Actions

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";

export async function adminAction(): ActionResponse {
  const { sessionClaims } = await auth();

  if (sessionClaims?.metadata?.role !== "admin") {
    return { success: false, error: "Admin access required" };
  }

  // Admin logic...
}
```

## Updating User Metadata

### Using clerkClient

```typescript
import "server-only";

import { clerkClient } from "@clerk/nextjs/server";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-db" });

export async function updateUserMetadata(
  userId: string,
  metadata: Partial<UserPublicMetadata>
): Promise<[null, User] | [DbError, null]> {
  // Input validation
  if (!userId?.trim()) {
    const error = DbError.validation("Invalid userId provided");
    logger.warn({ userId, errorCode: error.code }, "Invalid userId");
    return [error, null];
  }

  if (!metadata || Object.keys(metadata).length === 0) {
    const error = DbError.validation("Empty metadata provided");
    logger.warn({ userId, errorCode: error.code }, "Empty metadata");
    return [error, null];
  }

  try {
    logger.info({ userId, metadata }, "Updating user metadata");

    const client = await clerkClient();
    const updatedUser = await client.users.updateUser(userId, {
      publicMetadata: metadata
    });

    logger.info({ userId }, "User metadata updated successfully");
    return [null, updatedUser];
  } catch (error) {
    const dbError = categorizeDbError(error, "User");
    logger.error(
      { userId, errorCode: dbError.code, isRetryable: dbError.isRetryable },
      "Error updating user metadata"
    );
    return [dbError, null];
  }
}
```

### Common Metadata Operations

#### Mark Onboarding Complete

```typescript
await updateUserMetadata(userId, {
  onboardingComplete: true
});
```

#### Update User Role

```typescript
await updateUserMetadata(userId, {
  role: "admin"
});
```

#### Update Subscription Plan

```typescript
await updateUserMetadata(userId, {
  plan: "pro"
});
```

#### Set Multiple Fields

```typescript
await updateUserMetadata(userId, {
  onboardingComplete: true,
  plan: "pro",
  teamId: "team_123"
});
```

## Session Token Refresh

When you update `publicMetadata`, the JWT is not immediately updated. The new claims appear:

1. **On next request** - After the current session token expires
2. **On explicit refresh** - When user refreshes the page
3. **On sign out/in** - New token is generated

### Forcing Session Refresh

If you need immediate update, redirect or refresh:

```typescript
"use server";

import { redirect } from "next/navigation";

export async function completeOnboarding(userId: string): RedirectAction {
  await updateUserMetadata(userId, { onboardingComplete: true });

  // Redirect forces new request with updated claims
  redirect("/dashboard");
}
```

## Best Practices

### 1. Minimal Claims Data

Keep JWT claims small - include only essential data:

```typescript
// Good - minimal data
interface CustomJwtSessionClaims {
  metadata: {
    role: string;
    onboardingComplete: boolean;
  };
}

// Bad - too much data in JWT
interface CustomJwtSessionClaims {
  metadata: {
    role: string;
    permissions: string[];      // Could be large array
    settings: UserSettings;     // Complex object
    history: ActionHistory[];   // Potentially unbounded
  };
}
```

### 2. Use Private Metadata for Sensitive Data

```typescript
// Public metadata - safe to expose
await client.users.updateUser(userId, {
  publicMetadata: {
    role: "admin",
    plan: "pro"
  }
});

// Private metadata - server-only
await client.users.updateUser(userId, {
  privateMetadata: {
    internalNotes: "VIP customer",
    apiQuotaOverride: 10000,
    billingId: "cus_xxx"
  }
});
```

### 3. Type Safety

Always define types for your metadata:

```typescript
// types/clerk.d.ts
export {};

declare global {
  // Define the shape of public metadata
  interface UserPublicMetadata {
    onboardingComplete?: boolean;
    role?: "user" | "admin";
    plan?: "free" | "pro";
  }

  // JWT claims use the same shape
  interface CustomJwtSessionClaims {
    metadata: UserPublicMetadata;
  }
}
```

### 4. Defensive Access

Always use optional chaining when accessing claims:

```typescript
// Good - defensive
const role = sessionClaims?.metadata?.role ?? "user";
const isAdmin = sessionClaims?.metadata?.role === "admin";

// Bad - may throw
const role = sessionClaims.metadata.role;  // Error if null
```

## Accessing Metadata on Client

For client-side access, use Clerk's hooks:

```typescript
"use client";

import { useUser } from "@clerk/nextjs";

export function UserPlanBadge() {
  const { user, isLoaded } = useUser();

  if (!isLoaded) return <Skeleton />;

  const plan = user?.publicMetadata?.plan ?? "free";

  return <Badge>{plan}</Badge>;
}
```

**Note**: Client-side metadata may be stale. For critical checks, always verify on the server.
