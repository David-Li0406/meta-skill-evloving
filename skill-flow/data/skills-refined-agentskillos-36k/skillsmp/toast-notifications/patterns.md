# Usage Patterns

## Pattern 1: Toast After Redirect

Use this when the server action redirects to another page after completion.

```typescript
"use server";

import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function createResource(data: FormData): RedirectAction {
  const [error, resource] = await createResourceInDb(data);

  if (error) {
    await setToastCookie("Failed to create resource", "error");
    return { success: false, error: error.message };
  }

  // Toast will appear on the redirected page
  await setToastCookie("Resource created successfully!", "success");
  return redirect(`/resources/${resource.id}`);
}
```

## Pattern 2: Toast Without Redirect

Use when returning data to the same page (e.g., form submissions that stay on page).

```typescript
"use server";

import { revalidatePath } from "next/cache";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { ActionResponse } from "~/lib/action-types";

export async function updateProfile(data: FormData): ActionResponse {
  const [error] = await updateProfileInDb(data);

  if (error) {
    await setToastCookie("Failed to update profile", "error");
    return { success: false, error: error.message };
  }

  await setToastCookie("Profile updated!", "success");
  revalidatePath("/settings");

  return { success: true, data: null };
}
```

## Pattern 3: Conditional Toast Types

Use different toast types based on the operation result.

```typescript
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function processItems(ids: string[]): ActionResponse {
  let successCount = 0;
  let errorCount = 0;

  for (const id of ids) {
    const [error] = await processItem(id);
    if (error) errorCount++;
    else successCount++;
  }

  // Choose toast type based on results
  if (errorCount === 0) {
    await setToastCookie(`Processed ${successCount} items`, "success");
  } else if (successCount === 0) {
    await setToastCookie("Failed to process items", "error");
  } else {
    await setToastCookie(
      `Processed ${successCount} items, ${errorCount} failed`,
      "warning"
    );
  }

  return { success: errorCount === 0, data: { successCount, errorCount } };
}
```

## Pattern 4: Toast with Custom Duration

Use longer duration for important messages or when more reading time is needed.

```typescript
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";

// Standard toast (default ~5 seconds)
await setToastCookie("Quick notification", "info");

// Longer toast for important information
await setToastCookie(
  "Important: Your subscription expires in 3 days. Please renew to avoid service interruption.",
  "warning",
  10000  // 10 seconds
);

// Short toast for confirmations
await setToastCookie("Saved", "success", 2000);  // 2 seconds
```

## Pattern 5: Toast Before Redirect

Always set the toast cookie BEFORE calling redirect.

```typescript
"use server";

import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function handleAction(): RedirectAction {
  // ... do work ...

  // ✅ CORRECT: Set toast before redirect
  await setToastCookie("Action completed", "success");
  return redirect("/dashboard");

  // ❌ WRONG: Code after redirect never executes
  // return redirect("/dashboard");
  // await setToastCookie("This never runs", "success");
}
```

## Pattern 6: Toast in Authentication Flows

Use toasts to communicate auth state changes.

```typescript
"use server";

import { auth, signOut } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function handleSignOut() {
  const { userId } = await auth();

  if (userId) {
    await setToastCookie("You have been signed out", "info");
  }

  await signOut({ redirectTo: "/" });
}

export async function requireAuth(): RedirectAction {
  const { userId } = await auth();

  if (!userId) {
    await setToastCookie("Please sign in to continue", "warning");
    return redirect("/sign-in");
  }

  // User is authenticated, continue...
  return redirect("/dashboard");
}
```

## Pattern 7: Toast in Validation Errors

Use toasts for general validation messages, fieldErrors for specific fields.

```typescript
"use server";

import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { ActionResponse } from "~/lib/action-types";

export async function submitForm(data: FormData): ActionResponse {
  const parsed = formSchema.safeParse(Object.fromEntries(data));

  if (!parsed.success) {
    // General toast for validation failure
    await setToastCookie("Please check the form for errors", "warning");

    // Return field-specific errors for the form
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // ... continue with valid data
}
```

## Pattern 8: Toast in Multi-Step Flows

Use toasts to guide users through multi-step processes.

```typescript
"use server";

import { redirect } from "next/navigation";
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

export async function completeStep1(data: FormData): RedirectAction {
  const [error] = await saveStep1Data(data);

  if (error) {
    await setToastCookie("Failed to save. Please try again.", "error");
    return { success: false, error: error.message };
  }

  // Guide to next step
  return redirect("/onboarding/step-2");
}

export async function completeOnboarding(): RedirectAction {
  const [error] = await finalizeOnboarding();

  if (error) {
    await setToastCookie("Setup failed. Please try again.", "error");
    return { success: false, error: error.message };
  }

  // Celebratory message for completion
  await setToastCookie("Welcome! Your account is ready.", "success", 8000);
  return redirect("/dashboard");
}
```

## Anti-Patterns

### Don't Include Sensitive Information

```typescript
// ❌ Bad - exposes internal details
await setToastCookie(`User ${userId} failed auth with code ${errorCode}`, "error");

// ✅ Good - generic user-friendly message
await setToastCookie("Authentication failed. Please try again.", "error");
```

### Don't Use Toast for Inline Validation

```typescript
// ❌ Bad - toast for inline field errors
await setToastCookie("Email is required", "error");
await setToastCookie("Password must be 8 characters", "error");

// ✅ Good - return fieldErrors for inline display
return {
  success: false,
  error: "Validation failed",
  fieldErrors: {
    email: ["Email is required"],
    password: ["Password must be 8 characters"]
  }
};
```

### Don't Stack Multiple Toasts

```typescript
// ❌ Bad - multiple toasts confuse users
await setToastCookie("Step 1 complete", "success");
await setToastCookie("Step 2 complete", "success");
await setToastCookie("Step 3 complete", "success");

// ✅ Good - single summary toast
await setToastCookie("All steps completed successfully!", "success");
```

### Don't Use Toast for Debugging

```typescript
// ❌ Bad - debug information in toast
await setToastCookie(`Debug: ${JSON.stringify(data)}`, "info");

// ✅ Good - use structured logging
logger.debug({ data }, "Processing data");
```
