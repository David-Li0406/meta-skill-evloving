# Practical Examples

## Complete CRUD Error Handling

### Database Layer

```typescript
// features/budget/server/db/budgets.ts
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";
import type { Budget, CreateBudgetDto, UpdateBudgetDto } from "../types/budget";

const logger = createLogger({ module: "budget-db" });
const COLLECTION_NAME = "budgets";
const RESOURCE_NAME = "Budget";

// CREATE
export async function createBudget(
  userId: string,
  data: CreateBudgetDto
): Promise<[null, Budget] | [DbError, null]> {
  if (!userId?.trim()) {
    const error = DbError.validation("Invalid userId");
    logger.warn({ errorCode: error.code }, "Create budget: invalid userId");
    return [error, null];
  }

  logger.debug({ userId, budgetName: data.name }, "Creating budget");

  try {
    const docRef = await db.collection(COLLECTION_NAME).add({
      ...data,
      userId,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp()
    });

    const doc = await docRef.get();
    const budget = transformToBudget(doc.id, doc.data()!);

    logger.info({ userId, budgetId: budget.id }, "Budget created");
    return [null, budget];
  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({
      userId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Failed to create budget");
    return [dbError, null];
  }
}

// READ
export async function getBudgetById(
  userId: string,
  budgetId: string
): Promise<[null, Budget] | [DbError, null]> {
  if (!userId?.trim() || !budgetId?.trim()) {
    const error = DbError.validation("Invalid userId or budgetId");
    logger.warn({ userId, budgetId, errorCode: error.code }, "Invalid input");
    return [error, null];
  }

  logger.debug({ userId, budgetId }, "Fetching budget");

  try {
    const doc = await db.collection(COLLECTION_NAME).doc(budgetId).get();

    if (!doc.exists) {
      const error = DbError.notFound(RESOURCE_NAME);
      logger.warn({ userId, budgetId, errorCode: error.code }, "Budget not found");
      return [error, null];
    }

    const data = doc.data()!;

    // Check ownership
    if (data.userId !== userId) {
      const error = DbError.permissionDenied();
      logger.warn({ userId, budgetId, ownerId: data.userId }, "Access denied");
      return [error, null];
    }

    return [null, transformToBudget(doc.id, data)];
  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({
      userId,
      budgetId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Failed to fetch budget");
    return [dbError, null];
  }
}

// UPDATE
export async function updateBudget(
  userId: string,
  budgetId: string,
  data: UpdateBudgetDto
): Promise<[null, Budget] | [DbError, null]> {
  // First verify ownership
  const [existsError, existing] = await getBudgetById(userId, budgetId);
  if (existsError) {
    return [existsError, null];
  }

  logger.debug({ userId, budgetId }, "Updating budget");

  try {
    await db.collection(COLLECTION_NAME).doc(budgetId).update({
      ...data,
      updatedAt: FieldValue.serverTimestamp()
    });

    // Fetch updated document
    const doc = await db.collection(COLLECTION_NAME).doc(budgetId).get();
    const budget = transformToBudget(doc.id, doc.data()!);

    logger.info({ userId, budgetId }, "Budget updated");
    return [null, budget];
  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({
      userId,
      budgetId,
      errorCode: dbError.code
    }, "Failed to update budget");
    return [dbError, null];
  }
}

// DELETE
export async function deleteBudget(
  userId: string,
  budgetId: string
): Promise<[null, void] | [DbError, null]> {
  // Verify ownership first
  const [existsError] = await getBudgetById(userId, budgetId);
  if (existsError) {
    return [existsError, null];
  }

  logger.debug({ userId, budgetId }, "Deleting budget");

  try {
    await db.collection(COLLECTION_NAME).doc(budgetId).delete();
    logger.info({ userId, budgetId }, "Budget deleted");
    return [null, undefined];
  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({
      userId,
      budgetId,
      errorCode: dbError.code
    }, "Failed to delete budget");
    return [dbError, null];
  }
}
```

### Server Actions Layer

```typescript
// features/budget/server/actions/budget-actions.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { createLogger } from "~/lib/logger";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import {
  createBudget as createBudgetDb,
  updateBudget as updateBudgetDb,
  deleteBudget as deleteBudgetDb
} from "../db/budgets";
import { createBudgetSchema, updateBudgetSchema } from "../schemas/budget";
import type { ActionResponse, RedirectAction } from "~/lib/action-types";
import type { Budget } from "../types/budget";

const logger = createLogger({ module: "budget-actions" });

// CREATE
export async function createBudgetAction(
  formData: FormData
): ActionResponse<Budget> {
  const { userId } = await auth();

  if (!userId) {
    logger.warn({ action: "createBudget" }, "Unauthorized");
    return { success: false, error: "Please sign in to continue" };
  }

  // Validate
  const parsed = createBudgetSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    logger.warn({
      userId,
      action: "createBudget",
      fieldErrors: Object.keys(parsed.error.flatten().fieldErrors)
    }, "Validation failed");

    return {
      success: false,
      error: "Please check the form for errors",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Create
  const [error, budget] = await createBudgetDb(userId, parsed.data);

  if (error) {
    logger.error({
      userId,
      action: "createBudget",
      errorCode: error.code
    }, "Create failed");

    await setToastCookie("Failed to create budget", "error");
    return { success: false, error: "Unable to create budget" };
  }

  logger.info({ userId, budgetId: budget.id }, "Budget created via action");
  await setToastCookie(`Budget "${budget.name}" created!`, "success");
  revalidatePath("/budgets");

  return { success: true, data: budget };
}

// UPDATE
export async function updateBudgetAction(
  budgetId: string,
  formData: FormData
): ActionResponse<Budget> {
  const { userId } = await auth();

  if (!userId) {
    return { success: false, error: "Please sign in" };
  }

  const parsed = updateBudgetSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return {
      success: false,
      error: "Invalid data",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  const [error, budget] = await updateBudgetDb(userId, budgetId, parsed.data);

  if (error) {
    if (error.isNotFound) {
      await setToastCookie("Budget not found", "warning");
      return { success: false, error: "Budget not found" };
    }
    if (error.isPermissionDenied) {
      await setToastCookie("You don't have permission", "error");
      return { success: false, error: "Permission denied" };
    }

    await setToastCookie("Failed to update budget", "error");
    return { success: false, error: "Unable to update budget" };
  }

  await setToastCookie("Budget updated!", "success");
  revalidatePath("/budgets");
  revalidatePath(`/budgets/${budgetId}`);

  return { success: true, data: budget };
}

// DELETE with redirect
export async function deleteBudgetAction(budgetId: string): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    await setToastCookie("Please sign in", "error");
    return redirect("/sign-in");
  }

  const [error] = await deleteBudgetDb(userId, budgetId);

  if (error) {
    if (error.isNotFound) {
      await setToastCookie("Budget already deleted", "info");
      return redirect("/budgets");
    }
    if (error.isPermissionDenied) {
      await setToastCookie("You can't delete this budget", "error");
      return redirect("/budgets");
    }

    await setToastCookie("Failed to delete budget", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Budget deleted", "success");
  revalidatePath("/budgets");
  return redirect("/budgets");
}
```

### Page with Error Handling

```typescript
// app/budgets/[id]/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect, notFound } from "next/navigation";
import { getBudgetById } from "~/features/budget/server/db/budgets";
import { BudgetDetails } from "~/features/budget/components/budget-details";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function BudgetPage({ params }: PageProps) {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  const { id } = await params;
  const [error, budget] = await getBudgetById(userId, id);

  if (error) {
    if (error.isNotFound) {
      notFound();
    }
    if (error.isPermissionDenied) {
      redirect("/unauthorized");
    }
    if (error.isRetryable) {
      // Let error.tsx handle with retry button
      throw new Error("Service temporarily unavailable");
    }
    // Unknown error
    throw new Error("Unable to load budget");
  }

  return <BudgetDetails budget={budget} />;
}
```

### Error Boundary

```typescript
// app/budgets/[id]/error.tsx
"use client";

import { useEffect } from "react";
import { Button } from "@szum-tech/design-system";
import { useRouter } from "next/navigation";
import { AlertCircle } from "lucide-react";

export default function BudgetError({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const router = useRouter();

  useEffect(() => {
    // Log error (could send to monitoring service)
    console.error("Budget page error:", error.message, error.digest);
  }, [error]);

  const isTemporary = error.message.includes("temporarily");

  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4 p-8">
      <AlertCircle className="h-12 w-12 text-destructive" />

      <h2 className="text-xl font-semibold">
        {isTemporary ? "Service Temporarily Unavailable" : "Unable to Load Budget"}
      </h2>

      <p className="text-muted-foreground text-center max-w-md">
        {isTemporary
          ? "We're experiencing some issues. Please try again in a moment."
          : "There was a problem loading this budget. It may have been deleted or you may not have access."}
      </p>

      <div className="flex gap-2">
        <Button onClick={reset}>
          Try Again
        </Button>
        <Button variant="outline" onClick={() => router.push("/budgets")}>
          Back to Budgets
        </Button>
      </div>
    </div>
  );
}
```

### Form Component with Error Display

```typescript
// features/budget/components/budget-form.tsx
"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { Button, Input, Label, Card } from "@szum-tech/design-system";
import { AlertCircle } from "lucide-react";
import { createBudgetAction } from "../server/actions/budget-actions";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" disabled={pending} className="w-full">
      {pending ? "Creating..." : "Create Budget"}
    </Button>
  );
}

export function BudgetForm() {
  const [state, formAction] = useActionState(createBudgetAction, null);

  return (
    <Card className="p-6">
      <form action={formAction} className="space-y-4">
        {/* General error banner */}
        {state?.error && !state.fieldErrors && (
          <div className="flex items-center gap-2 p-3 rounded-md bg-destructive/10 text-destructive">
            <AlertCircle className="h-4 w-4" />
            <span>{state.error}</span>
          </div>
        )}

        {/* Name field */}
        <div className="space-y-2">
          <Label htmlFor="name">Budget Name</Label>
          <Input
            id="name"
            name="name"
            placeholder="e.g., Monthly Groceries"
            aria-invalid={!!state?.fieldErrors?.name}
            aria-describedby={state?.fieldErrors?.name ? "name-error" : undefined}
            className={state?.fieldErrors?.name ? "border-destructive" : ""}
          />
          {state?.fieldErrors?.name && (
            <p id="name-error" className="text-sm text-destructive">
              {state.fieldErrors.name[0]}
            </p>
          )}
        </div>

        {/* Amount field */}
        <div className="space-y-2">
          <Label htmlFor="amount">Amount</Label>
          <Input
            id="amount"
            name="amount"
            type="number"
            step="0.01"
            min="0"
            placeholder="0.00"
            aria-invalid={!!state?.fieldErrors?.amount}
            aria-describedby={state?.fieldErrors?.amount ? "amount-error" : undefined}
            className={state?.fieldErrors?.amount ? "border-destructive" : ""}
          />
          {state?.fieldErrors?.amount && (
            <p id="amount-error" className="text-sm text-destructive">
              {state.fieldErrors.amount[0]}
            </p>
          )}
        </div>

        <SubmitButton />
      </form>
    </Card>
  );
}
```

### Not Found Page

```typescript
// app/budgets/[id]/not-found.tsx
import Link from "next/link";
import { Button } from "@szum-tech/design-system";
import { FileQuestion } from "lucide-react";

export default function BudgetNotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] gap-4 p-8">
      <FileQuestion className="h-16 w-16 text-muted-foreground" />

      <h2 className="text-2xl font-semibold">Budget Not Found</h2>

      <p className="text-muted-foreground text-center max-w-md">
        The budget you're looking for doesn't exist or has been deleted.
      </p>

      <Button asChild>
        <Link href="/budgets">View All Budgets</Link>
      </Button>
    </div>
  );
}
```

### API Error Logging Endpoint

```typescript
// app/api/log-error/route.ts
import { NextResponse } from "next/server";
import { createLogger } from "~/lib/logger";
import { auth } from "@clerk/nextjs/server";

const logger = createLogger({ module: "client-error" });

export async function POST(request: Request) {
  try {
    const { userId } = await auth();
    const { message, digest, stack, url, userAgent } = await request.json();

    logger.error({
      source: "client",
      userId: userId ?? "anonymous",
      digest,
      url,
      userAgent: userAgent?.slice(0, 200),
      stack: stack?.slice(0, 1000)
    }, `Client error: ${message}`);

    return NextResponse.json({ logged: true });
  } catch (error) {
    logger.error({ error: "Failed to log client error" }, "Error logging failed");
    return NextResponse.json({ logged: false }, { status: 500 });
  }
}
```
