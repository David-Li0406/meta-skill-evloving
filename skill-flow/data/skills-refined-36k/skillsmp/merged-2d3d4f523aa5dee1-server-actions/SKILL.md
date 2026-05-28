---
name: server-actions
description: Use this skill when creating Next.js Server Actions with TypeScript, focusing on best practices for forms, mutations, validation, and error handling.
---

# Server Actions Skill

Create Next.js Server Actions with TypeScript following best practices for validation, error handling, and React integration.

## Overview

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

## Common Use Cases

Use this skill when the user requests:

- "Create a server action"
- "Handle form submission"
- "Implement data mutation"
- "Add optimistic updates"
- "Fix server action errors"
- "Revalidate cache after update"

## Related Skills

- [neon-database-management](../neon-database-management/SKILL.md) - Database queries
- [component-development](../component-development/SKILL.md) - Client components using actions
- [webapp-testing](../webapp-testing/SKILL.md) - Testing action flows

---

**Last Updated:** January 19, 2026  
**Maintained By:** Development Team  
**Status:** ✅ Production Ready with RLS Support