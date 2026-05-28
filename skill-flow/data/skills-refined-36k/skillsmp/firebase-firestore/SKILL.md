---
name: firebase-firestore
version: 1.0.0
lastUpdated: 2026-01-18
description: Create Firebase Firestore database queries with TypeScript, proper type lifecycle, error handling, and best practices for Next.js applications.
tags: [firebase, firestore, database, typescript, error-handling, server-only]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__context7__*
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Create database queries for user profiles
  - Implement CRUD operations for budget management
  - Add error handling to Firestore queries
  - Set up Firebase seeding for predefined data
---

# Firebase Firestore Skill

Create production-ready Firestore database queries with TypeScript, proper type lifecycle, structured error handling, and best practices.

## Quick Reference

| Document                      | Purpose                                     |
| ----------------------------- | ------------------------------------------- |
| [types.md](./types.md)        | Type utilities and lifecycle patterns       |
| [errors.md](./errors.md)      | DbError class and error categorization      |
| [config.md](./config.md)      | Firebase Admin SDK configuration            |
| [examples.md](./examples.md)  | Complete CRUD operation examples            |
| [patterns.md](./patterns.md)  | Best practices and anti-patterns            |
| [seeding.md](./seeding.md)    | Database seeding patterns                   |

## Instructions

### Before Implementation

1. **Read project context** at `.claude/project-context.md` for project-specific patterns
2. **Check existing patterns** in `lib/firebase/` for configuration
3. **Review feature structure** in `features/*/server/db/` for query patterns

### Workflow

1. **Define types** using the type lifecycle pattern (Base → Firestore → Application → DTOs)
2. **Create transform function** to convert Firestore data to application types
3. **Implement queries** with tuple return pattern `[DbError | null, Data | null]`
4. **Add error handling** using `DbError` class and `categorizeDbError`
5. **Include logging** with structured context at all error points
6. **Test edge cases** (empty inputs, not found, permissions)

### File Organization

```
features/
└── [feature]/
    ├── types/
    │   └── [resource].ts          # Type definitions
    └── server/
        └── db/
            ├── [resource]-queries.ts  # CRUD operations
            └── seed-[resource].ts     # Seeding (if needed)
```

## Core Concepts

### Type Lifecycle

Firebase requires different type representations at different stages:

```typescript
// 1. Base type - Business fields only
type ResourceBase = {
  name: string;
  status: "active" | "inactive";
};

// 2. Firestore type - With Timestamp objects
type ResourceFirestore = WithFirestoreTimestamps<ResourceBase>;

// 3. Application type - With id and Date objects
type Resource = WithDates<ResourceBase>;

// 4. Create DTO - For creating documents
type CreateResourceDto = CreateDto<ResourceBase>;

// 5. Update DTO - For updating documents
type UpdateResourceDto = UpdateDto<ResourceBase>;
```

See [types.md](./types.md) for complete type utilities.

### Error Handling Pattern

All database queries return tuples for explicit error handling:

```typescript
export async function getResourceById(
  id: string
): Promise<[null, Resource] | [DbError, null]> {
  // Input validation
  if (!id?.trim()) {
    return [DbError.validation("Invalid id provided"), null];
  }

  try {
    const doc = await db.collection(COLLECTION).doc(id).get();

    if (!doc.exists) {
      return [DbError.notFound(RESOURCE_NAME), null];
    }

    return [null, transformToResource(doc.id, doc.data()!)];
  } catch (error) {
    return [categorizeDbError(error, RESOURCE_NAME), null];
  }
}
```

See [errors.md](./errors.md) for complete error handling.

### Transform Functions

Convert Firestore documents to application types:

```typescript
function transformToResource(
  docId: string,
  data: FirebaseFirestore.DocumentData
): Resource {
  return {
    id: docId,
    ...data,
    // Convert Timestamp to Date
    createdAt: data.createdAt?.toDate(),
    updatedAt: data.updatedAt?.toDate(),
  } as Resource;
}
```

## Questions to Ask

Before implementing database queries, clarify:

1. **What is the resource name?** (e.g., "Budget", "User", "Category")
2. **What fields does the resource have?** (business fields only)
3. **Are there custom Date fields?** (beyond createdAt/updatedAt)
4. **What queries are needed?** (getById, getAll, getByUserId, etc.)
5. **Is seeding required?** (predefined data)
6. **What are the access patterns?** (by user, by status, etc.)

## Usage Examples

### Basic Query Function

```typescript
import "server-only";
import { db } from "~/lib/firebase";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";
import type { Budget } from "../types/budget";

const logger = createLogger({ module: "budget-db" });
const COLLECTION = "budgets";
const RESOURCE = "Budget";

export async function getBudgetById(
  id: string
): Promise<[null, Budget] | [DbError, null]> {
  if (!id?.trim()) {
    const error = DbError.validation("Invalid budget id");
    logger.warn({ errorCode: error.code }, "Validation failed");
    return [error, null];
  }

  try {
    const doc = await db.collection(COLLECTION).doc(id).get();

    if (!doc.exists) {
      logger.warn({ budgetId: id }, "Budget not found");
      return [DbError.notFound(RESOURCE), null];
    }

    logger.info({ budgetId: id }, "Budget retrieved");
    return [null, transformToBudget(doc.id, doc.data()!)];
  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ budgetId: id, errorCode: dbError.code }, "Query failed");
    return [dbError, null];
  }
}
```

### Usage in Server Actions

```typescript
export async function updateBudget(
  budgetId: string,
  data: UpdateBudgetDto
): ActionResponse<Budget> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Unauthorized" };
  }

  const [error, budget] = await updateBudgetInDb(budgetId, data);

  if (error) {
    if (error.isNotFound) {
      return { success: false, error: "Budget not found" };
    }
    return { success: false, error: error.message };
  }

  revalidatePath("/budgets");
  return { success: true, data: budget };
}
```

### Usage in Page Loaders

```typescript
async function loadBudget(budgetId: string) {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");

  const [error, budget] = await getBudgetById(budgetId);

  if (error) {
    if (error.isNotFound) notFound();
    if (error.isRetryable) throw error; // Let error.tsx handle
    throw new Error("Unable to load budget");
  }

  return budget;
}
```

## Related Documentation

- [types.md](./types.md) - Complete type utilities
- [errors.md](./errors.md) - Error handling patterns
- [config.md](./config.md) - Firebase configuration
- [examples.md](./examples.md) - Full CRUD examples
- [patterns.md](./patterns.md) - Best practices
- [seeding.md](./seeding.md) - Seeding patterns

## Related Skills

- `server-actions` - For implementing server actions that use these queries
- `db-migration` - For migrating Firestore data
