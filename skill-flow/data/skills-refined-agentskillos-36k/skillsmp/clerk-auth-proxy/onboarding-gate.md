# Onboarding Gate Pattern

## Overview

The onboarding gate ensures users complete a required flow (e.g., profile setup, preferences) before accessing the main application. This pattern uses:

1. **Proxy-level redirect** - Redirects incomplete users to `/onboarding`
2. **Session claims** - `onboardingComplete` flag in JWT
3. **Layout protection** - Double-check in onboarding layout
4. **Completion action** - Update Clerk metadata on finish

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           User Request                               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          proxy.ts                                    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ if (authenticated && !onboardingComplete) {                  │    │
│  │   redirect("/onboarding")                                    │    │
│  │ }                                                            │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
    ┌───────────────────────────┐   ┌───────────────────────────────┐
    │   /onboarding/*           │   │   Main App Routes             │
    │                           │   │   (requires onboardingComplete) │
    │   1. /onboarding/welcome  │   │                                │
    │   2. /onboarding/prefs    │   │   /, /dashboard, etc.          │
    │   3. /onboarding/complete │   │                                │
    └───────────────────────────┘   └───────────────────────────────┘
                    │
                    ▼
    ┌───────────────────────────┐
    │  completeOnboarding()     │
    │  - Update Firestore       │
    │  - Update Clerk metadata  │
    │  - Redirect to /          │
    └───────────────────────────┘
```

## Implementation

### 1. Proxy Configuration (proxy.ts)

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

const isPublicRoute = createRouteMatcher(["/sign-in(.*)", "/sign-up(.*)"]);
const isOnboardingRoute = createRouteMatcher(["/onboarding(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  const { isAuthenticated, sessionClaims, redirectToSignIn } = await auth();

  // Allow onboarding route for authenticated users (even if incomplete)
  if (isAuthenticated && isOnboardingRoute(req)) {
    return NextResponse.next();
  }

  // Redirect unauthenticated users to sign-in
  if (!isAuthenticated && !isPublicRoute(req)) {
    return redirectToSignIn({ returnBackUrl: req.url });
  }

  // Gate: Redirect users who haven't completed onboarding
  if (isAuthenticated && !sessionClaims?.metadata?.onboardingComplete) {
    const onboardingUrl = new URL("/onboarding", req.url);
    return NextResponse.redirect(onboardingUrl);
  }

  // Allow authenticated users with completed onboarding
  if (isAuthenticated && !isPublicRoute(req)) {
    return NextResponse.next();
  }
});

export const config = {
  matcher: [
    "/((?!_next|api|trpc|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)"
  ]
};
```

### 2. Session Claims Type (types/clerk.d.ts)

```typescript
export {};

declare global {
  interface CustomJwtSessionClaims {
    metadata: {
      onboardingComplete?: boolean;
    };
  }
}
```

### 3. Onboarding Layout Protection

The layout provides secondary protection and handles already-onboarded users:

```typescript
// app/onboarding/layout.tsx
import type React from "react";
import { auth } from "@clerk/nextjs/server";
import { redirect, unauthorized } from "next/navigation";
import { OnboardingStepper } from "~/features/onboarding/components/onboarding-stepper";
import { getOnboardingById } from "~/features/onboarding/server/db/onboarding";
import logger from "~/lib/logger";

async function loadData() {
  const { userId, isAuthenticated, sessionClaims } = await auth();

  // Not authenticated - show unauthorized page
  if (!isAuthenticated) {
    logger.warn("User not authenticated in onboarding layout");
    return unauthorized();
  }

  // Already onboarded - redirect to main app
  if (sessionClaims?.metadata.onboardingComplete === true) {
    logger.info("User already onboarded, redirecting to home");
    redirect("/");
  }

  // Load onboarding state from database
  const [, onboarding] = await getOnboardingById(userId);

  return { onboarding };
}

export default async function OnboardingLayout({
  children
}: {
  children: React.ReactNode;
}) {
  const { onboarding } = await loadData();

  return (
    <main className="bg-app-foreground min-h-dvh">
      <div className="container py-20">
        <h1 className="text-heading-h3 mb-8">Welcome</h1>
        <OnboardingStepper hideNav={!onboarding}>
          {children}
        </OnboardingStepper>
      </div>
    </main>
  );
}
```

### 4. Completion Server Action

```typescript
// features/onboarding/server/actions/complete-onboarding.ts
"use server";

import { FieldValue } from "firebase-admin/firestore";
import { redirect } from "next/navigation";
import { updateUserMetadata } from "~/features/auth/server/db/user";
import { updateOnboarding } from "~/features/onboarding/server/db/onboarding";
import type { Onboarding, UpdateOnboardingDto } from "~/features/onboarding/types/onboarding";
import type { RedirectAction } from "~/lib/action-types";
import { createLogger } from "~/lib/logger";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

const logger = createLogger({ module: "onboarding-actions" });

export async function completeOnboarding(onboarding: Onboarding): RedirectAction {
  logger.info({ onboardingId: onboarding.id }, "Completing onboarding");

  // 1. Update onboarding document in Firestore
  const updateData: UpdateOnboardingDto = {
    completed: true,
    completedAt: FieldValue.serverTimestamp()
  };

  const [dbError] = await updateOnboarding(onboarding.id, updateData);
  if (dbError) {
    logger.error({
      onboardingId: onboarding.id,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Failed to mark onboarding as completed");
    return { success: false, error: dbError.message };
  }

  logger.info({ onboardingId: onboarding.id }, "Onboarding marked completed in DB");

  // 2. Update Clerk user metadata
  const [metadataError] = await updateUserMetadata(onboarding.id, {
    onboardingComplete: true
  });

  if (metadataError) {
    logger.error({
      userId: onboarding.id,
      errorCode: metadataError.code
    }, "Failed to update Clerk metadata");
    return { success: false, error: "Failed to update session" };
  }

  logger.info({ userId: onboarding.id }, "Clerk metadata updated");

  // 3. Show success toast and redirect
  await setToastCookie("Welcome! Your account is now set up.", "success");
  return redirect("/");
}
```

### 5. User Metadata Update Helper

```typescript
// features/auth/server/db/user.ts
import "server-only";

import { clerkClient, type User } from "@clerk/nextjs/server";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-db" });

export async function updateUserMetadata(
  userId: string,
  metadata: Partial<UserPublicMetadata>
): Promise<[null, User] | [DbError, null]> {
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
    logger.info({ userId, metadata }, "Updating Clerk user metadata");

    const client = await clerkClient();
    const updatedUser = await client.users.updateUser(userId, {
      publicMetadata: metadata
    });

    logger.info({ userId }, "Clerk user metadata updated successfully");
    return [null, updatedUser];
  } catch (error) {
    const dbError = categorizeDbError(error, "User");
    logger.error({
      userId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Error updating Clerk user metadata");
    return [dbError, null];
  }
}
```

## Multi-Step Onboarding

For multi-step onboarding flows, track progress in your database:

### Onboarding Steps Type

```typescript
// features/onboarding/types/onboarding.ts
export const OnboardingSteps = {
  WELCOME: "welcome",
  PREFERENCES: "preferences",
  BUDGET_SETUP: "budget-setup",
  BUDGET_DETAILS: "budget-details",
  COMPLETE: "complete"
} as const;

export type OnboardingStep = typeof OnboardingSteps[keyof typeof OnboardingSteps];

export type OnboardingBase = {
  completed: boolean;
  currentStep: OnboardingStep;
  preferences?: PreferencesData;
  budget?: BudgetData;
  completedAt?: Date;
};
```

### Step Navigation

```typescript
// features/onboarding/server/actions/navigate-step.ts
"use server";

import { redirect } from "next/navigation";
import type { RedirectAction } from "~/lib/action-types";

const STEP_ORDER: OnboardingStep[] = [
  "welcome",
  "preferences",
  "budget-setup",
  "budget-details",
  "complete"
];

export async function goToNextStep(
  onboarding: Onboarding,
  currentStep: OnboardingStep
): RedirectAction {
  const currentIndex = STEP_ORDER.indexOf(currentStep);
  const nextStep = STEP_ORDER[currentIndex + 1];

  if (!nextStep) {
    return { success: false, error: "Already at final step" };
  }

  await updateOnboarding(onboarding.id, { currentStep: nextStep });

  return redirect(`/onboarding/${nextStep}`);
}
```

## Edge Cases

### 1. User Signs Up But Leaves Before Completing

The proxy will always redirect them back to `/onboarding` until they complete.

### 2. User Tries to Access Onboarding After Completing

The layout redirects them to `/` (home).

### 3. Session Token Not Yet Refreshed

After updating Clerk metadata, the JWT may not be immediately updated. The redirect in `completeOnboarding` forces a new request which gets fresh claims.

### 4. Database Update Succeeds But Clerk Update Fails

Log the error and return failure. The user will retry, and idempotent operations will handle duplicates.

## Testing Onboarding Gate

### E2E Test Example

```typescript
// tests/e2e/onboarding.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Onboarding Gate", () => {
  test("redirects new user to onboarding", async ({ page }) => {
    // Sign in as new user (without onboardingComplete)
    await signInAsNewUser(page);

    // Try to access dashboard
    await page.goto("/dashboard");

    // Should be redirected to onboarding
    await expect(page).toHaveURL(/\/onboarding/);
  });

  test("allows completed user to access app", async ({ page }) => {
    // Sign in as completed user
    await signInAsCompletedUser(page);

    // Access dashboard
    await page.goto("/dashboard");

    // Should stay on dashboard
    await expect(page).toHaveURL("/dashboard");
  });

  test("redirects completed user away from onboarding", async ({ page }) => {
    // Sign in as completed user
    await signInAsCompletedUser(page);

    // Try to access onboarding
    await page.goto("/onboarding");

    // Should be redirected to home
    await expect(page).toHaveURL("/");
  });
});
```
