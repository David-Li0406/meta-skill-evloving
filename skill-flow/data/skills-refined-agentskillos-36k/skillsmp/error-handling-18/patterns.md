# Error Handling Patterns

## Pattern 1: Database Layer Errors

### Tuple Return Pattern

Always return `[error, data]` tuple from database functions.

```typescript
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "user-db" });

export async function getUserById(
  userId: string
): Promise<[null, User] | [DbError, null]> {
  // 1. Input validation
  if (!userId?.trim()) {
    const error = DbError.validation("Invalid userId provided");
    logger.warn({ userId, errorCode: error.code }, "Invalid input");
    return [error, null];
  }

  try {
    // 2. Database operation
    const doc = await db.collection("users").doc(userId).get();

    // 3. Not found check
    if (!doc.exists) {
      const error = DbError.notFound("User");
      logger.warn({ userId, errorCode: error.code }, "User not found");
      return [error, null];
    }

    // 4. Data integrity check
    const data = doc.data();
    if (!data) {
      const error = DbError.dataCorruption("User");
      logger.error({ userId, errorCode: error.code }, "Data undefined");
      return [error, null];
    }

    // 5. Success
    return [null, transformToUser(doc.id, data)];
  } catch (error) {
    // 6. Categorize unexpected errors
    const dbError = categorizeDbError(error, "User");
    logger.error({
      userId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Database error");
    return [dbError, null];
  }
}
```

### Error Categorization

```typescript
// lib/firebase/errors.ts
export function categorizeDbError(error: unknown, resource: string): DbError {
  if (error instanceof FirebaseError) {
    switch (error.code) {
      case "not-found":
        return DbError.notFound(resource);
      case "already-exists":
        return DbError.alreadyExists(resource);
      case "permission-denied":
      case "unauthenticated":
        return DbError.permissionDenied();
      case "unavailable":
      case "deadline-exceeded":
        return new DbError(error.code, `${resource} temporarily unavailable`, true);
      default:
        return new DbError(error.code, `${resource} operation failed`, false);
    }
  }
  return new DbError("unknown", `Unexpected error with ${resource}`, false);
}
```

## Pattern 2: Server Action Errors

### Standard Action Response

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import { revalidatePath } from "next/cache";
import { createLogger } from "~/lib/logger";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { ActionResponse } from "~/lib/action-types";

const logger = createLogger({ module: "budget-actions" });

export async function createBudget(
  formData: FormData
): ActionResponse<Budget> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    logger.warn({ action: "createBudget" }, "Unauthorized access attempt");
    return { success: false, error: "Please sign in to continue" };
  }

  // 2. Validation with field-level errors
  const parsed = createBudgetSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    logger.warn({
      userId,
      action: "createBudget",
      errors: parsed.error.flatten().fieldErrors
    }, "Validation failed");

    return {
      success: false,
      error: "Please check the form for errors",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 3. Database operation
  const [error, budget] = await createBudgetInDb(userId, parsed.data);

  if (error) {
    logger.error({
      userId,
      action: "createBudget",
      errorCode: error.code,
      isRetryable: error.isRetryable
    }, "Failed to create budget");

    // User-friendly toast
    await setToastCookie("Failed to create budget. Please try again.", "error");

    // Generic error message (don't expose internals)
    return { success: false, error: "Unable to create budget" };
  }

  // 4. Success
  logger.info({ userId, budgetId: budget.id }, "Budget created");
  await setToastCookie("Budget created successfully!", "success");
  revalidatePath("/budgets");

  return { success: true, data: budget };
}
```

### Redirect Action with Error Handling

```typescript
"use server";

import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { RedirectAction } from "~/lib/action-types";

export async function deleteBudget(budgetId: string): RedirectAction {
  const { userId } = await auth();
  if (!userId) {
    await setToastCookie("Please sign in", "error");
    return redirect("/sign-in");
  }

  const [error] = await deleteBudgetInDb(userId, budgetId);

  if (error) {
    if (error.isNotFound) {
      await setToastCookie("Budget not found", "warning");
      return redirect("/budgets");
    }

    await setToastCookie("Failed to delete budget", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Budget deleted", "success");
  return redirect("/budgets");
}
```

## Pattern 3: Page Loader Errors

### Handling Errors in Server Components

```typescript
// app/budgets/[id]/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect, notFound } from "next/navigation";
import { getBudgetById } from "~/features/budget/server/db/budgets";

export default async function BudgetPage({
  params
}: {
  params: Promise<{ id: string }>
}) {
  const { userId } = await auth();
  if (!userId) {
    redirect("/sign-in");
  }

  const { id } = await params;
  const [error, budget] = await getBudgetById(userId, id);

  if (error) {
    // Not found - show 404 page
    if (error.isNotFound) {
      notFound();
    }

    // Retryable error - let error.tsx handle with retry button
    if (error.isRetryable) {
      throw new Error("Service temporarily unavailable");
    }

    // Permission denied - redirect
    if (error.isPermissionDenied) {
      redirect("/unauthorized");
    }

    // Unknown error - throw for error boundary
    throw new Error("Unable to load budget");
  }

  return <BudgetDetails budget={budget} />;
}
```

## Pattern 4: React Error Boundaries

### Root Error Boundary

```typescript
// app/error.tsx
"use client";

import { useEffect } from "react";
import { Button } from "@szum-tech/design-system";

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to server for monitoring
    fetch("/api/log-error", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: error.message,
        digest: error.digest,
        stack: error.stack?.slice(0, 1000)
      })
    });
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="text-muted-foreground">
        We're sorry, but something unexpected happened.
      </p>
      <div className="flex gap-2">
        <Button onClick={reset}>Try again</Button>
        <Button variant="outline" onClick={() => window.location.href = "/"}>
          Go home
        </Button>
      </div>
    </div>
  );
}
```

### Feature-Specific Error Boundary

```typescript
// app/budgets/error.tsx
"use client";

import { useEffect } from "react";
import { Button } from "@szum-tech/design-system";
import { useRouter } from "next/navigation";

export default function BudgetsError({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const router = useRouter();

  useEffect(() => {
    console.error("Budgets error:", error);
  }, [error]);

  return (
    <div className="p-8 text-center">
      <h2 className="text-xl font-semibold mb-4">
        Unable to load budgets
      </h2>
      <p className="text-muted-foreground mb-6">
        There was a problem loading your budgets. Please try again.
      </p>
      <div className="flex justify-center gap-2">
        <Button onClick={reset}>Retry</Button>
        <Button variant="outline" onClick={() => router.push("/")}>
          Back to Dashboard
        </Button>
      </div>
    </div>
  );
}
```

## Pattern 5: Form Error Handling

### With useActionState

```typescript
"use client";

import { useActionState } from "react";
import { Button, Input, Label } from "@szum-tech/design-system";
import { createBudget } from "../server/actions/create-budget";

export function BudgetForm() {
  const [state, formAction, isPending] = useActionState(createBudget, null);

  return (
    <form action={formAction} className="space-y-4">
      {/* General error message */}
      {state?.error && !state.fieldErrors && (
        <div className="bg-destructive/10 text-destructive p-3 rounded-md">
          {state.error}
        </div>
      )}

      <div>
        <Label htmlFor="name">Budget Name</Label>
        <Input
          id="name"
          name="name"
          disabled={isPending}
          aria-invalid={!!state?.fieldErrors?.name}
          aria-describedby={state?.fieldErrors?.name ? "name-error" : undefined}
        />
        {/* Field-level error */}
        {state?.fieldErrors?.name && (
          <p id="name-error" className="text-sm text-destructive mt-1">
            {state.fieldErrors.name[0]}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="amount">Amount</Label>
        <Input
          id="amount"
          name="amount"
          type="number"
          disabled={isPending}
          aria-invalid={!!state?.fieldErrors?.amount}
        />
        {state?.fieldErrors?.amount && (
          <p className="text-sm text-destructive mt-1">
            {state.fieldErrors.amount[0]}
          </p>
        )}
      </div>

      <Button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Budget"}
      </Button>
    </form>
  );
}
```

## Pattern 6: API Route Error Handling

```typescript
// app/api/webhooks/stripe/route.ts
import { NextResponse } from "next/server";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "stripe-webhook" });

export async function POST(request: Request) {
  const startTime = performance.now();

  try {
    const signature = request.headers.get("stripe-signature");

    if (!signature) {
      logger.warn({}, "Missing Stripe signature");
      return NextResponse.json(
        { error: "Missing signature" },
        { status: 400 }
      );
    }

    const body = await request.text();
    const event = stripe.webhooks.constructEvent(body, signature, secret);

    logger.info({ eventType: event.type, eventId: event.id }, "Processing webhook");

    // Handle event...
    await handleWebhookEvent(event);

    const durationMs = Math.round(performance.now() - startTime);
    logger.info({ eventId: event.id, durationMs }, "Webhook processed");

    return NextResponse.json({ received: true });
  } catch (error) {
    const durationMs = Math.round(performance.now() - startTime);

    if (error instanceof Stripe.errors.StripeSignatureVerificationError) {
      logger.warn({ durationMs }, "Invalid webhook signature");
      return NextResponse.json(
        { error: "Invalid signature" },
        { status: 400 }
      );
    }

    logger.error({
      durationMs,
      error: error instanceof Error ? error.message : "Unknown"
    }, "Webhook processing failed");

    return NextResponse.json(
      { error: "Processing failed" },
      { status: 500 }
    );
  }
}
```

## Anti-Patterns

### Don't Expose Internal Errors

```typescript
// ❌ Bad - exposes stack trace and internal details
catch (error) {
  return { success: false, error: error.message };
}

// ✅ Good - log internally, return generic message
catch (error) {
  logger.error({ error: error.message, userId }, "Operation failed");
  return { success: false, error: "Unable to complete operation" };
}
```

### Don't Forget to Log

```typescript
// ❌ Bad - no logging
if (error) {
  return { success: false, error: "Failed" };
}

// ✅ Good - log before returning
if (error) {
  logger.error({ errorCode: error.code, userId }, "Operation failed");
  return { success: false, error: "Failed" };
}
```

### Don't Throw in Server Actions

```typescript
// ❌ Bad - throwing in server action
export async function createItem() {
  if (!valid) throw new Error("Invalid");
  // ...
}

// ✅ Good - return error response
export async function createItem(): ActionResponse {
  if (!valid) {
    return { success: false, error: "Invalid input" };
  }
  // ...
}
```

### Don't Ignore Error Properties

```typescript
// ❌ Bad - treats all errors the same
if (error) {
  return redirect("/error");
}

// ✅ Good - handle based on error type
if (error) {
  if (error.isNotFound) notFound();
  if (error.isRetryable) throw error; // Let error boundary handle
  if (error.isPermissionDenied) redirect("/unauthorized");
  throw new Error("Unknown error");
}
```
