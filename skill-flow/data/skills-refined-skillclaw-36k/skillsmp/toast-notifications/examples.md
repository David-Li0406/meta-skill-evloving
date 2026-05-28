# Practical Examples

## Basic Server Action with Toast

```typescript
// features/budget/server/actions/create-budget.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { createBudgetInDb } from "../db/budgets";
import type { RedirectAction } from "~/lib/action-types";

export async function createBudget(formData: FormData): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    await setToastCookie("Please sign in to continue", "error");
    return redirect("/sign-in");
  }

  const name = formData.get("name") as string;
  const amount = Number(formData.get("amount"));

  // Validation
  if (!name || !amount) {
    await setToastCookie("Please fill in all fields", "warning");
    return { success: false, error: "Validation failed" };
  }

  // Create budget
  const [error, budget] = await createBudgetInDb(userId, { name, amount });

  if (error) {
    await setToastCookie("Failed to create budget. Please try again.", "error");
    return { success: false, error: error.message };
  }

  // Success
  await setToastCookie(`Budget "${name}" created successfully!`, "success");
  revalidatePath("/budgets");
  return redirect(`/budgets/${budget.id}`);
}
```

## Delete Action with Toast

```typescript
// features/budget/server/actions/delete-budget.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { deleteBudgetInDb, getBudgetById } from "../db/budgets";
import type { RedirectAction } from "~/lib/action-types";

export async function deleteBudget(budgetId: string): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    await setToastCookie("Unauthorized", "error");
    return redirect("/sign-in");
  }

  // Check ownership
  const [, budget] = await getBudgetById(userId, budgetId);

  if (!budget) {
    await setToastCookie("Budget not found", "error");
    return redirect("/budgets");
  }

  // Delete
  const [error] = await deleteBudgetInDb(userId, budgetId);

  if (error) {
    await setToastCookie("Failed to delete budget", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Budget deleted", "success");
  revalidatePath("/budgets");
  return redirect("/budgets");
}
```

## Form with useActionState and Toast

```typescript
// features/settings/components/profile-form.tsx
"use client";

import { useActionState } from "react";
import { Button, Input, Label } from "@szum-tech/design-system";
import { updateProfile } from "../server/actions/update-profile";

export function ProfileForm({ user }: { user: User }) {
  const [state, formAction, isPending] = useActionState(updateProfile, null);

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          name="name"
          defaultValue={user.name}
          disabled={isPending}
        />
        {state?.fieldErrors?.name && (
          <p className="text-red-500 text-sm">{state.fieldErrors.name[0]}</p>
        )}
      </div>

      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          defaultValue={user.email}
          disabled={isPending}
        />
      </div>

      <Button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Save Changes"}
      </Button>
    </form>
  );
}

// features/settings/server/actions/update-profile.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { revalidatePath } from "next/cache";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { updateUserProfile } from "../db/users";
import type { ActionResponse } from "~/lib/action-types";

export async function updateProfile(
  _prevState: unknown,
  formData: FormData
): ActionResponse {
  const { userId } = await auth();

  if (!userId) {
    await setToastCookie("Please sign in", "error");
    return { success: false, error: "Unauthorized" };
  }

  const name = formData.get("name") as string;
  const email = formData.get("email") as string;

  // Validate
  if (!name?.trim()) {
    return {
      success: false,
      error: "Name is required",
      fieldErrors: { name: ["Name is required"] }
    };
  }

  // Update
  const [error] = await updateUserProfile(userId, { name, email });

  if (error) {
    await setToastCookie("Failed to update profile", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Profile updated!", "success");
  revalidatePath("/settings");

  return { success: true, data: null };
}
```

## Onboarding Flow with Toast

```typescript
// features/onboarding/server/actions/complete-step.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { updateOnboarding } from "../db/onboarding";
import { OnboardingSteps } from "../types/onboarding";
import type { RedirectAction } from "~/lib/action-types";

export async function completeWelcomeStep(): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    return redirect("/sign-in");
  }

  const [error] = await updateOnboarding(userId, {
    currentStep: OnboardingSteps.PREFERENCES
  });

  if (error) {
    await setToastCookie("Something went wrong. Please try again.", "error");
    return { success: false, error: error.message };
  }

  return redirect(`/onboarding/${OnboardingSteps.PREFERENCES}`);
}

export async function completeOnboarding(): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    return redirect("/sign-in");
  }

  // Mark onboarding complete
  const [error] = await finalizeOnboarding(userId);

  if (error) {
    await setToastCookie("Failed to complete setup", "error");
    return { success: false, error: error.message };
  }

  // Welcome message
  await setToastCookie("Welcome! Your account is ready.", "success", 8000);
  return redirect("/dashboard");
}
```

## Authentication Actions with Toast

```typescript
// features/auth/server/actions/sign-out.ts
"use server";

import { auth, signOut } from "@clerk/nextjs/server";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function signOutAction() {
  const { userId } = await auth();

  if (userId) {
    await setToastCookie("You have been signed out", "info");
  }

  await signOut({ redirectTo: "/" });
}
```

## Error Handling with Different Toast Types

```typescript
// features/api/server/actions/external-api.ts
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { ActionResponse } from "~/lib/action-types";

export async function syncWithExternalService(): ActionResponse {
  try {
    const result = await callExternalAPI();

    if (result.partialSuccess) {
      await setToastCookie(
        `Synced ${result.successCount} of ${result.totalCount} items`,
        "warning"
      );
      return { success: true, data: result };
    }

    await setToastCookie("Sync completed successfully!", "success");
    return { success: true, data: result };

  } catch (error) {
    if (error instanceof RateLimitError) {
      await setToastCookie(
        "Rate limit reached. Please try again in a few minutes.",
        "warning"
      );
    } else if (error instanceof AuthenticationError) {
      await setToastCookie(
        "Authentication failed. Please reconnect your account.",
        "error"
      );
    } else {
      await setToastCookie(
        "Sync failed. Please try again later.",
        "error"
      );
    }

    return { success: false, error: "Sync failed" };
  }
}
```

## Toast with Info Messages

```typescript
// features/subscription/server/actions/check-plan.ts
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function checkPlanLimits(userId: string) {
  const usage = await getUsage(userId);
  const plan = await getPlan(userId);

  if (usage.percentage >= 80 && usage.percentage < 100) {
    await setToastCookie(
      `You've used ${usage.percentage}% of your plan. Consider upgrading.`,
      "info",
      10000  // Show longer
    );
  } else if (usage.percentage >= 100) {
    await setToastCookie(
      "You've reached your plan limit. Upgrade to continue.",
      "warning",
      10000
    );
  }

  return { usage, plan };
}
```

## Bulk Operations with Toast

```typescript
// features/admin/server/actions/bulk-actions.ts
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { revalidatePath } from "next/cache";
import type { ActionResponse } from "~/lib/action-types";

export async function bulkDeleteUsers(userIds: string[]): ActionResponse {
  let successCount = 0;
  let errorCount = 0;

  for (const userId of userIds) {
    const [error] = await deleteUser(userId);
    if (error) {
      errorCount++;
    } else {
      successCount++;
    }
  }

  if (errorCount === 0) {
    await setToastCookie(
      `Successfully deleted ${successCount} users`,
      "success"
    );
  } else if (successCount === 0) {
    await setToastCookie(
      `Failed to delete users. Please try again.`,
      "error"
    );
  } else {
    await setToastCookie(
      `Deleted ${successCount} users. ${errorCount} failed.`,
      "warning"
    );
  }

  revalidatePath("/admin/users");

  return {
    success: errorCount === 0,
    data: { successCount, errorCount }
  };
}
```

## File Upload with Toast

```typescript
// features/documents/server/actions/upload.ts
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import { revalidatePath } from "next/cache";
import type { ActionResponse } from "~/lib/action-types";

export async function uploadDocument(formData: FormData): ActionResponse {
  const file = formData.get("file") as File;

  if (!file || file.size === 0) {
    await setToastCookie("Please select a file to upload", "warning");
    return { success: false, error: "No file selected" };
  }

  // Check file size (10MB limit)
  if (file.size > 10 * 1024 * 1024) {
    await setToastCookie("File size must be less than 10MB", "error");
    return { success: false, error: "File too large" };
  }

  // Check file type
  const allowedTypes = ["application/pdf", "image/png", "image/jpeg"];
  if (!allowedTypes.includes(file.type)) {
    await setToastCookie("Only PDF and image files are allowed", "error");
    return { success: false, error: "Invalid file type" };
  }

  try {
    const document = await saveDocument(file);

    await setToastCookie(`"${file.name}" uploaded successfully`, "success");
    revalidatePath("/documents");

    return { success: true, data: document };
  } catch (error) {
    await setToastCookie("Upload failed. Please try again.", "error");
    return { success: false, error: "Upload failed" };
  }
}
```
