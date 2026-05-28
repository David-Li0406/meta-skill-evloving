---
name: server-actions
version: 1.0.0
lastUpdated: 2026-01-18
description: Create Next.js Server Actions with TypeScript following best practices for forms, mutations, validation, and error handling. Use when implementing server-side form handling, CRUD operations, or data mutations.
tags: [next.js, server-actions, forms, mutations, validation, zod, react-hook-form]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Create a server action for user registration form
  - Implement CRUD actions for budget management
  - Add form validation with Zod to the contact form
  - Create redirect action for onboarding flow
---

# Server Actions Skill

Create Next.js Server Actions with TypeScript following best practices for validation, error handling, and React integration.

> **Reference Files:**
> - [types.md](./types.md) - ActionResponse, RedirectAction type definitions
> - [examples.md](./examples.md) - Complete implementation examples
> - [patterns.md](./patterns.md) - Best practices and anti-patterns
> - [validation.md](./validation.md) - Zod schema patterns
> - [hooks.md](./hooks.md) - React hooks (useActionState, useFormStatus)
> - [react-hook-form.md](./react-hook-form.md) - React Hook Form integration

## First Step: Read Project Context

**IMPORTANT**: Before creating server actions, check project configuration files:

**`.claude/project-context.md`** for:
- Authentication provider (Clerk, NextAuth, JWT)
- Database patterns (tuple error handling, DbError class)
- Logging conventions

**`CLAUDE.md`** for:
- Server Actions patterns (ActionResponse type)
- Database error handling (DbError class)
- Toast notification system
- File organization conventions

## Context

This skill helps you create:

- **Form actions** - Handle form submissions with validation
- **CRUD operations** - Create, read, update, delete mutations
- **Redirect flows** - Multi-step wizards, onboarding
- **Data mutations** - Any server-side data changes

## Instructions

When the user requests a server action:

### 1. Analyze Requirements

Gather information about:
- What data does the action handle?
- Does it return data or redirect?
- What validation is needed?
- What authentication/authorization is required?
- What errors need to be handled?
- What cache paths need revalidation?

### 2. Choose Response Type

| Scenario                   | Type                 | Description                            |
|----------------------------|----------------------|----------------------------------------|
| Returns data               | `ActionResponse<T>`  | Action returns data to client          |
| Redirects on success       | `RedirectAction`     | Action navigates to new page           |
| Form with `useActionState` | Modified signature   | Accepts `previousState` as first param |

### 3. Create Server Action

**File Location:** `features/[feature]/server/actions/[action-name].ts`

**Standard Template:**

```typescript
"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { auth } from "@clerk/nextjs/server"; // or your auth provider
import { createLogger } from "~/lib/logger";
import type { ActionResponse, RedirectAction } from "~/lib/action-types";

const logger = createLogger({ module: "[feature]-actions" });

export async function actionName(data: InputType): ActionResponse<OutputType> {
  // 1. Authentication
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // 2. Validation
  const parsed = schema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // 3. Database operation
  const [error, result] = await dbOperation(parsed.data);
  if (error) {
    logger.error({ userId, error }, "Operation failed");
    return { success: false, error: "Operation failed" };
  }

  // 4. Revalidate cache
  revalidatePath("/affected-path");

  // 5. Return response
  logger.info({ userId, resultId: result.id }, "Operation succeeded");
  return { success: true, data: result };
}
```

### 4. Create Validation Schema

**File Location:** `features/[feature]/schemas/[schema-name].ts`

```typescript
import { z } from "zod";

export const inputSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address")
});

export type InputData = z.infer<typeof inputSchema>;
```

### 5. Integrate with React Component

Choose integration pattern based on form complexity:

| Complexity | Pattern                              | Use When                           |
|------------|--------------------------------------|------------------------------------|
| Simple     | `useActionState`                     | Native form, simple state          |
| Complex    | React Hook Form + `useTransition`    | Dynamic fields, complex validation |
| Redirect   | Bound action prop                    | Multi-step flows                   |

See [hooks.md](./hooks.md) and [react-hook-form.md](./react-hook-form.md) for implementation details.

## Core Patterns

### Error Handling

Use tuple pattern for database operations:

```typescript
const [error, data] = await dbOperation();
if (error) {
  if (error.isNotFound) return { success: false, error: "Not found" };
  if (error.isRetryable) return { success: false, error: "Please try again" };
  return { success: false, error: "Operation failed" };
}
```

### Cache Revalidation

Always revalidate after mutations:

```typescript
revalidatePath("/posts");        // Specific path
revalidateTag("posts");          // By cache tag
```

### Toast Notifications

For user feedback with redirects:

```typescript
import { setToastCookie } from "~/lib/toast/server/toast.cookie";

await setToastCookie("Saved successfully!", "success");
redirect("/dashboard");
```

### Security Checklist

1. ✅ Verify authentication (`await auth()`)
2. ✅ Check authorization (ownership, permissions)
3. ✅ Validate all inputs (Zod schema)
4. ✅ Log important operations
5. ✅ Never expose internal errors to client

## File Organization

```text
features/
  users/
    server/
      actions/
        create-user.ts
        update-user.ts
        delete-user.ts
        index.ts         # Re-exports
      db/
        users.ts
    schemas/
      user.ts
    types/
      user.ts
    components/
      user-form.tsx
```

## Running and Testing

```bash
# Type check
npm run type-check

# Run related tests
npm run test -- features/[feature]

# Test in Storybook (if form component)
npm run storybook:dev
```

## Questions to Ask

When creating server actions:

- What data does this action create/update/delete?
- Does it return data or redirect to another page?
- What validation rules apply to the input?
- What authentication/authorization is needed?
- What error cases should be handled?
- What paths/tags need cache revalidation?
- Should there be toast notification feedback?
- Is this part of a multi-step flow?
