# Practical Examples

## Database Query Logging

```typescript
// features/budget/server/db/budgets.ts
import { createLogger } from "~/lib/logger";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { db } from "~/lib/firebase";

const logger = createLogger({ module: "budget-db" });

const COLLECTION_NAME = "budgets";

export async function getBudgetById(
  userId: string,
  budgetId: string
): Promise<[null, Budget] | [DbError, null]> {
  // Input validation logging
  if (!userId?.trim()) {
    logger.warn({ budgetId }, "getBudgetById called without userId");
    return [DbError.validation("Invalid userId"), null];
  }

  logger.debug({ userId, budgetId }, "Fetching budget");

  try {
    const doc = await db.collection(COLLECTION_NAME).doc(budgetId).get();

    if (!doc.exists) {
      logger.warn({ userId, budgetId }, "Budget not found");
      return [DbError.notFound("Budget"), null];
    }

    const data = doc.data();
    if (data?.userId !== userId) {
      logger.warn({ userId, budgetId, ownerId: data?.userId }, "Budget access denied");
      return [DbError.permissionDenied(), null];
    }

    logger.info({ userId, budgetId }, "Budget fetched successfully");
    return [null, transformBudget(doc.id, data)];
  } catch (error) {
    const dbError = categorizeDbError(error, "Budget");
    logger.error({
      userId,
      budgetId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Failed to fetch budget");
    return [dbError, null];
  }
}

export async function createBudget(
  userId: string,
  data: CreateBudgetDto
): Promise<[null, Budget] | [DbError, null]> {
  logger.info({ userId, budgetName: data.name }, "Creating budget");

  try {
    const docRef = await db.collection(COLLECTION_NAME).add({
      ...data,
      userId,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp()
    });

    logger.info({
      userId,
      budgetId: docRef.id,
      budgetName: data.name
    }, "Budget created successfully");

    const doc = await docRef.get();
    return [null, transformBudget(doc.id, doc.data()!)];
  } catch (error) {
    const dbError = categorizeDbError(error, "Budget");
    logger.error({
      userId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Failed to create budget");
    return [dbError, null];
  }
}
```

## Server Action Logging

```typescript
// features/budget/server/actions/create-budget.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { revalidatePath } from "next/cache";
import { createLogger } from "~/lib/logger";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { createBudget as createBudgetDb } from "../db/budgets";
import type { ActionResponse } from "~/lib/action-types";
import type { Budget } from "../types/budget";

const logger = createLogger({ module: "budget-actions" });

export async function createBudget(
  data: CreateBudgetFormData
): ActionResponse<Budget> {
  const { userId } = await auth();

  if (!userId) {
    logger.warn({ action: "createBudget" }, "Unauthorized access attempt");
    return { success: false, error: "Unauthorized" };
  }

  logger.info({
    userId,
    action: "createBudget",
    budgetName: data.name
  }, "Starting budget creation");

  // Validate input
  const parsed = createBudgetSchema.safeParse(data);
  if (!parsed.success) {
    logger.warn({
      userId,
      action: "createBudget",
      errors: parsed.error.flatten().fieldErrors
    }, "Validation failed");

    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Create budget
  const [error, budget] = await createBudgetDb(userId, parsed.data);

  if (error) {
    logger.error({
      userId,
      action: "createBudget",
      errorCode: error.code,
      isRetryable: error.isRetryable
    }, "Budget creation failed");

    await setToastCookie("Failed to create budget", "error");
    return { success: false, error: error.message };
  }

  logger.info({
    userId,
    action: "createBudget",
    budgetId: budget.id
  }, "Budget created successfully");

  await setToastCookie("Budget created successfully!", "success");
  revalidatePath("/budgets");

  return { success: true, data: budget };
}
```

## API Route Logging

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from "next/headers";
import { NextResponse } from "next/server";
import { createLogger } from "~/lib/logger";
import Stripe from "stripe";

const logger = createLogger({ module: "stripe-webhook" });

export async function POST(request: Request) {
  const startTime = performance.now();
  const headersList = await headers();
  const signature = headersList.get("stripe-signature");

  logger.debug({ hasSignature: !!signature }, "Webhook received");

  if (!signature) {
    logger.warn({}, "Missing stripe signature");
    return NextResponse.json({ error: "Missing signature" }, { status: 400 });
  }

  let event: Stripe.Event;

  try {
    const body = await request.text();
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (error) {
    logger.error({
      error: error instanceof Error ? error.message : "Unknown error"
    }, "Webhook signature verification failed");
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  logger.info({
    eventType: event.type,
    eventId: event.id
  }, "Processing webhook event");

  try {
    switch (event.type) {
      case "payment_intent.succeeded":
        await handlePaymentSuccess(event.data.object as Stripe.PaymentIntent);
        break;
      case "payment_intent.payment_failed":
        await handlePaymentFailure(event.data.object as Stripe.PaymentIntent);
        break;
      default:
        logger.debug({ eventType: event.type }, "Unhandled event type");
    }

    const durationMs = Math.round(performance.now() - startTime);
    logger.info({
      eventType: event.type,
      eventId: event.id,
      durationMs
    }, "Webhook processed successfully");

    return NextResponse.json({ received: true });
  } catch (error) {
    const durationMs = Math.round(performance.now() - startTime);
    logger.error({
      eventType: event.type,
      eventId: event.id,
      durationMs,
      error: error instanceof Error ? error.message : "Unknown error"
    }, "Webhook processing failed");

    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }
}
```

## Cron Job Logging

```typescript
// app/api/cron/cleanup/route.ts
import { createLogger } from "~/lib/logger";
import { NextResponse } from "next/server";

const logger = createLogger({ module: "cron-cleanup" });

export async function GET() {
  const startTime = performance.now();

  logger.info({}, "Starting cleanup job");

  try {
    const expiredSessions = await deleteExpiredSessions();
    const oldLogs = await archiveOldLogs();
    const orphanedFiles = await cleanupOrphanedFiles();

    const durationMs = Math.round(performance.now() - startTime);

    logger.info({
      expiredSessions,
      oldLogs,
      orphanedFiles,
      durationMs
    }, "Cleanup job completed");

    return NextResponse.json({
      success: true,
      cleaned: {
        sessions: expiredSessions,
        logs: oldLogs,
        files: orphanedFiles
      }
    });
  } catch (error) {
    const durationMs = Math.round(performance.now() - startTime);

    logger.error({
      durationMs,
      error: error instanceof Error ? error.message : "Unknown error"
    }, "Cleanup job failed");

    return NextResponse.json({ error: "Cleanup failed" }, { status: 500 });
  }
}
```

## Authentication Flow Logging

```typescript
// features/auth/server/actions/complete-onboarding.ts
"use server";

import { auth, clerkClient } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { createLogger } from "~/lib/logger";
import { completeOnboardingInDb } from "../db/onboarding";

const logger = createLogger({ module: "auth-onboarding" });

export async function completeOnboarding(): RedirectAction {
  const { userId, sessionClaims } = await auth();

  if (!userId) {
    logger.warn({}, "completeOnboarding called without authentication");
    return redirect("/sign-in");
  }

  // Check if already completed
  if (sessionClaims?.metadata?.onboardingComplete) {
    logger.info({ userId }, "Onboarding already complete, redirecting");
    return redirect("/");
  }

  logger.info({ userId }, "Completing onboarding");

  // Update database
  const [dbError] = await completeOnboardingInDb(userId);
  if (dbError) {
    logger.error({
      userId,
      errorCode: dbError.code
    }, "Failed to update onboarding in database");
    return { success: false, error: "Failed to complete onboarding" };
  }

  // Update Clerk metadata
  try {
    const client = await clerkClient();
    await client.users.updateUserMetadata(userId, {
      publicMetadata: {
        onboardingComplete: true
      }
    });

    logger.info({ userId }, "Onboarding completed successfully");
  } catch (error) {
    logger.error({
      userId,
      error: error instanceof Error ? error.message : "Unknown error"
    }, "Failed to update Clerk metadata");
    return { success: false, error: "Failed to update user metadata" };
  }

  return redirect("/");
}
```

## Background Job Logging

```typescript
// lib/jobs/process-notifications.ts
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "notifications-job" });

export async function processNotificationQueue() {
  const batchSize = 100;
  let processedCount = 0;
  let errorCount = 0;

  logger.info({ batchSize }, "Starting notification processing");

  const notifications = await getUnsentNotifications(batchSize);

  logger.debug({
    notificationCount: notifications.length
  }, "Fetched notifications to process");

  for (const notification of notifications) {
    try {
      await sendNotification(notification);
      await markNotificationSent(notification.id);
      processedCount++;

      logger.debug({
        notificationId: notification.id,
        userId: notification.userId,
        type: notification.type
      }, "Notification sent");
    } catch (error) {
      errorCount++;

      logger.error({
        notificationId: notification.id,
        userId: notification.userId,
        error: error instanceof Error ? error.message : "Unknown error"
      }, "Failed to send notification");

      await markNotificationFailed(notification.id, error);
    }
  }

  logger.info({
    processedCount,
    errorCount,
    totalCount: notifications.length,
    successRate: `${Math.round((processedCount / notifications.length) * 100)}%`
  }, "Notification processing completed");

  return { processed: processedCount, errors: errorCount };
}
```

## Error Boundary Logging

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
    // Log error to server
    fetch("/api/log-error", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: error.message,
        digest: error.digest,
        stack: error.stack
      })
    });
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-xl font-semibold mb-4">Something went wrong!</h2>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}

// app/api/log-error/route.ts
import { createLogger } from "~/lib/logger";
import { NextResponse } from "next/server";

const logger = createLogger({ module: "client-error" });

export async function POST(request: Request) {
  const { message, digest, stack } = await request.json();

  logger.error({
    digest,
    stack: stack?.slice(0, 500),  // Truncate stack trace
    source: "client"
  }, `Client error: ${message}`);

  return NextResponse.json({ logged: true });
}
```
