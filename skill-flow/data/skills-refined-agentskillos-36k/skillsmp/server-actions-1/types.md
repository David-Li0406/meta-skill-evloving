# Server Action Types

## Core Type Definitions

Copy these type definitions to `lib/action-types.ts` in your project:

```typescript
// lib/action-types.ts

/**
 * Success state returned by server actions
 * @template T - The type of data returned on success
 */
type ActionStateSuccess<T> = {
  /** Indicates the action completed successfully */
  success: true;
  /** The data returned by the action */
  data: T;
  /** Optional success message for user feedback */
  message?: string;
};

/**
 * Failure state returned by server actions
 */
type ActionStateFailed = {
  /** Indicates the action failed */
  success: false;
  /** Error message describing what went wrong */
  error: string;
  /** Field-specific validation errors for forms */
  fieldErrors?: Record<string, string[]>;
};

/**
 * Response type for actions that return data
 * @template T - The type of data returned on success (defaults to unknown)
 *
 * @example
 * ```typescript
 * export async function getUser(id: string): ActionResponse<User> {
 *   const [error, user] = await getUserById(id);
 *   if (error) return { success: false, error: error.message };
 *   return { success: true, data: user };
 * }
 * ```
 */
export type ActionResponse<T = unknown> = Promise<ActionStateSuccess<T> | ActionStateFailed>;

/**
 * Response type for actions that redirect on success
 * Uses `never` to indicate the function doesn't return on success
 *
 * @example
 * ```typescript
 * export async function createPost(data: FormData): RedirectAction {
 *   const [error, post] = await createPostInDb(data);
 *   if (error) return { success: false, error: error.message };
 *   redirect(`/posts/${post.id}`);
 * }
 * ```
 */
export type RedirectAction = Promise<never | ActionStateFailed>;
```

## Type Usage Guide

### ActionResponse<T> - For Data-Returning Actions

Use when the action returns data that the client needs to process.

```typescript
// ✅ Good: Action returns the created resource
export async function createUser(data: CreateUserDto): ActionResponse<User> {
  const [error, user] = await createUserInDb(data);

  if (error) {
    return { success: false, error: error.message };
  }

  return {
    success: true,
    data: user,
    message: "User created successfully"
  };
}

// Client usage
const result = await createUser(formData);
if (result.success) {
  console.log("Created user:", result.data);
  toast.success(result.message);
} else {
  toast.error(result.error);
}
```

### RedirectAction - For Navigation Actions

Use when the action should redirect the user on success (e.g., form submissions, onboarding flows).

```typescript
// ✅ Good: Action redirects after successful mutation
export async function submitForm(data: FormData): RedirectAction {
  const [error] = await processForm(data);

  if (error) {
    return { success: false, error: error.message };
  }

  // Redirect - this never returns
  redirect("/success");
}

// Client usage - only error state needs handling
const result = await submitForm(formData);
// If we reach here, it failed (redirect would have thrown)
if (!result.success) {
  toast.error(result.error);
}
```

### ActionStateFailed with fieldErrors - For Form Validation

Use `fieldErrors` to return field-specific validation errors for form handling.

```typescript
export async function registerUser(formData: FormData): ActionResponse<User> {
  const parsed = userSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  });

  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
      // Example fieldErrors:
      // {
      //   email: ["Invalid email format"],
      //   password: ["Password must be at least 8 characters"]
      // }
    };
  }

  // ... create user
}

// Client usage with field-specific error display
const result = await registerUser(formData);
if (!result.success && result.fieldErrors) {
  // Display errors next to form fields
  Object.entries(result.fieldErrors).forEach(([field, errors]) => {
    setFieldError(field, errors[0]);
  });
}
```

## Discriminated Union Pattern

The `success` boolean acts as a discriminant for type narrowing:

```typescript
const result = await myAction();

if (result.success) {
  // TypeScript knows this is ActionStateSuccess<T>
  console.log(result.data);    // ✅ Accessible
  console.log(result.message); // ✅ Accessible (optional)
  console.log(result.error);   // ❌ Type error - doesn't exist
} else {
  // TypeScript knows this is ActionStateFailed
  console.log(result.error);       // ✅ Accessible
  console.log(result.fieldErrors); // ✅ Accessible (optional)
  console.log(result.data);        // ❌ Type error - doesn't exist
}
```

## Type Guards

Create type guards for additional safety:

```typescript
// lib/action-types.ts

export function isActionSuccess<T>(
  result: Awaited<ActionResponse<T>>
): result is ActionStateSuccess<T> {
  return result.success === true;
}

export function isActionFailed(
  result: Awaited<ActionResponse<unknown>>
): result is ActionStateFailed {
  return result.success === false;
}

// Usage
const result = await createUser(data);
if (isActionSuccess(result)) {
  // TypeScript knows result.data is User
  return result.data;
}
```

## Generic Constraints

When your action works with specific resource types:

```typescript
// Generic action for any entity with an ID
export async function deleteEntity<T extends { id: string }>(
  entity: T,
  deleteFunction: (id: string) => Promise<[Error | null, void]>
): ActionResponse<void> {
  const [error] = await deleteFunction(entity.id);

  if (error) {
    return { success: false, error: error.message };
  }

  return { success: true, data: undefined };
}
```

## Integration with useActionState

When using React's `useActionState` hook, the action signature changes:

```typescript
// Action compatible with useActionState
// First parameter is the previous state (from useActionState)
export async function createPost(
  previousState: ActionStateFailed | ActionStateSuccess<Post> | null,
  formData: FormData
): ActionResponse<Post> {
  // Validation
  const title = formData.get("title") as string;
  if (!title) {
    return { success: false, error: "Title is required" };
  }

  // Create post
  const [error, post] = await createPostInDb({ title });
  if (error) {
    return { success: false, error: error.message };
  }

  return { success: true, data: post };
}

// Client component
"use client";
import { useActionState } from "react";
import { createPost } from "./actions";

export function PostForm() {
  const [state, formAction, pending] = useActionState(createPost, null);

  return (
    <form action={formAction}>
      <input name="title" />
      {state && !state.success && <p>{state.error}</p>}
      <button disabled={pending}>Create</button>
    </form>
  );
}
```

## Type Exports Summary

```typescript
// lib/action-types.ts - Complete file

type ActionStateSuccess<T> = {
  success: true;
  data: T;
  message?: string;
};

type ActionStateFailed = {
  success: false;
  error: string;
  fieldErrors?: Record<string, string[]>;
};

export type ActionResponse<T = unknown> = Promise<ActionStateSuccess<T> | ActionStateFailed>;
export type RedirectAction = Promise<never | ActionStateFailed>;

// Optional type guards
export function isActionSuccess<T>(
  result: Awaited<ActionResponse<T>>
): result is ActionStateSuccess<T> {
  return result.success === true;
}

export function isActionFailed(
  result: Awaited<ActionResponse<unknown>>
): result is ActionStateFailed {
  return result.success === false;
}
```
