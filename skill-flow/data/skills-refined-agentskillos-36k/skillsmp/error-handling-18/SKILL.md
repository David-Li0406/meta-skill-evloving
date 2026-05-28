---
name: error-handling
version: 1.0.0
lastUpdated: 2026-01-18
description: Comprehensive error handling patterns for Next.js applications. Covers database errors (DbError), server action errors, React error boundaries, toast notifications for user feedback, and structured logging.
tags: [error-handling, DbError, error-boundary, toast, logging, server-actions]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
context: fork
agent: general-purpose
user-invocable: true
examples:
  - How to handle database errors
  - Error boundary patterns
  - Toast notifications for errors
  - Server action error handling
---

# Error Handling Skill

Comprehensive error handling patterns for Next.js applications.

> **Reference Files:**
> - [patterns.md](./patterns.md) - Error handling patterns by layer
> - [examples.md](./examples.md) - Practical code examples

## Error Handling Philosophy

**Principles:**
1. **Never expose internal errors to users** - Log details server-side, show friendly messages client-side
2. **Use typed errors** - DbError class for database, ActionResponse for server actions
3. **Fail gracefully** - Error boundaries, fallback UI, retry mechanisms
4. **Log everything** - Structured logging with context for debugging
5. **Provide feedback** - Toast notifications for user-facing errors

## Error Handling Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                              │
│  • Error Boundaries (React)                                  │
│  • Toast Notifications (user feedback)                       │
│  • Form field errors (inline validation)                     │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                  Server Action Layer                         │
│  • ActionResponse<T> / RedirectAction types                  │
│  • Zod validation with fieldErrors                           │
│  • Toast cookies for redirect feedback                       │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                   Database Layer                             │
│  • DbError class (typed errors)                              │
│  • Tuple pattern [error, data]                               │
│  • categorizeDbError() helper                                │
└─────────────────────────────────────────────────────────────┘
                              ↑
┌─────────────────────────────────────────────────────────────┐
│                   Logging Layer                              │
│  • Pino structured logging                                   │
│  • Error context (errorCode, isRetryable, userId)            │
│  • Log before returning error                                │
└─────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Database Layer (DbError)

```typescript
import { categorizeDbError, DbError } from "~/lib/firebase/errors";

// Tuple pattern - always return [error, data]
export async function getById(id: string): Promise<[null, Data] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid id"), null];
  }

  try {
    const doc = await db.collection("items").doc(id).get();
    if (!doc.exists) {
      return [DbError.notFound("Item"), null];
    }
    return [null, transform(doc)];
  } catch (error) {
    const dbError = categorizeDbError(error, "Item");
    logger.error({ errorCode: dbError.code, id }, "Database error");
    return [dbError, null];
  }
}
```

### Server Action Layer

```typescript
import { setToastCookie } from "~/lib/toast/server/toast.cookie";
import type { ActionResponse } from "~/lib/action-types";

export async function createItem(data: FormData): ActionResponse<Item> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Unauthorized" };
  }

  // Validation errors - return fieldErrors for form display
  const parsed = schema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }

  // Database errors - toast + generic message
  const [error, item] = await createItemInDb(parsed.data);
  if (error) {
    await setToastCookie("Failed to create item", "error");
    return { success: false, error: "Unable to create item" };
  }

  await setToastCookie("Item created!", "success");
  return { success: true, data: item };
}
```

### Client Layer (Error Boundary)

```typescript
// app/error.tsx - Catches unhandled errors
"use client";

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error tracking service
    logError(error);
  }, [error]);

  return (
    <div className="error-container">
      <h2>Something went wrong</h2>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```

## DbError Properties

| Property | Type | Description |
|----------|------|-------------|
| `code` | string | Error code (validation, not-found, permission-denied, etc.) |
| `message` | string | User-friendly error message |
| `isRetryable` | boolean | True for transient errors (network, timeout) |
| `isNotFound` | boolean | True when resource doesn't exist |
| `isAlreadyExists` | boolean | True when creating existing resource |
| `isPermissionDenied` | boolean | True for auth/permission issues |

## Static Factory Methods

```typescript
DbError.notFound("User")           // Resource not found
DbError.alreadyExists("Budget")    // Resource already exists
DbError.validation("Invalid input") // Validation failed
DbError.dataCorruption("Event")    // Document exists but data invalid
DbError.permissionDenied()         // Auth/permission issue
```

## Error Response Flow

```
Database Error
    ↓
categorizeDbError() → DbError with properties
    ↓
Log error with context (logger.error)
    ↓
Return tuple [error, null]
    ↓
Server Action checks error properties
    ↓
Set toast cookie for user feedback
    ↓
Return ActionResponse with generic message
    ↓
Client displays toast + handles state
```

## Related Skills

- `firebase-firestore` - DbError class and database patterns
- `server-actions` - ActionResponse types and patterns
- `toast-notifications` - User feedback via toasts
- `structured-logging` - Pino logging patterns
