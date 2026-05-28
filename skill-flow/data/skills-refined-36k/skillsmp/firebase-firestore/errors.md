# Firebase Error Handling

Structured error handling for Firestore database operations.

## DbError Class

```typescript
// lib/firebase/errors.ts
import "server-only";

/**
 * Firestore error codes that indicate transient failures
 * These operations can be safely retried
 */
const RETRYABLE_ERROR_CODES = [
  "unavailable",
  "deadline-exceeded",
  "resource-exhausted",
  "aborted",
  "internal",
] as const;

/**
 * Structured database error with categorization
 */
export class DbError extends Error {
  /** Original Firestore error code or custom code */
  readonly code: string;

  /** Whether the operation can be retried */
  readonly isRetryable: boolean;

  /** Whether the resource was not found */
  readonly isNotFound: boolean;

  /** Whether the resource already exists */
  readonly isAlreadyExists: boolean;

  /** Whether permission was denied */
  readonly isPermissionDenied: boolean;

  /** Resource context (e.g., "Budget", "User") */
  readonly resourceName: string;

  constructor(
    message: string,
    code: string,
    resourceName: string,
    options: {
      isRetryable?: boolean;
      isNotFound?: boolean;
      isAlreadyExists?: boolean;
      isPermissionDenied?: boolean;
    } = {}
  ) {
    super(message);
    this.name = "DbError";
    this.code = code;
    this.resourceName = resourceName;
    this.isRetryable = options.isRetryable ?? false;
    this.isNotFound = options.isNotFound ?? false;
    this.isAlreadyExists = options.isAlreadyExists ?? false;
    this.isPermissionDenied = options.isPermissionDenied ?? false;
  }

  // ═══════════════════════════════════════════════════════════════
  // Static Factory Methods
  // ═══════════════════════════════════════════════════════════════

  /**
   * Resource not found in database
   */
  static notFound(resourceName: string): DbError {
    return new DbError(
      `${resourceName} not found`,
      "not-found",
      resourceName,
      { isNotFound: true }
    );
  }

  /**
   * Resource already exists (duplicate)
   */
  static alreadyExists(resourceName: string): DbError {
    return new DbError(
      `${resourceName} already exists`,
      "already-exists",
      resourceName,
      { isAlreadyExists: true }
    );
  }

  /**
   * Input validation failed
   */
  static validation(message: string, resourceName: string = "Resource"): DbError {
    return new DbError(
      message,
      "validation",
      resourceName
    );
  }

  /**
   * Document exists but data is invalid/corrupt
   */
  static dataCorruption(resourceName: string): DbError {
    return new DbError(
      `${resourceName} data is invalid or corrupted`,
      "data-corruption",
      resourceName
    );
  }

  /**
   * Permission denied for operation
   */
  static permissionDenied(resourceName: string): DbError {
    return new DbError(
      `Permission denied for ${resourceName}`,
      "permission-denied",
      resourceName,
      { isPermissionDenied: true }
    );
  }

  /**
   * Generic database error
   */
  static internal(resourceName: string, originalMessage?: string): DbError {
    return new DbError(
      originalMessage || `Database error for ${resourceName}`,
      "internal",
      resourceName,
      { isRetryable: true }
    );
  }
}

/**
 * Categorizes Firestore errors into structured DbError
 */
export function categorizeDbError(error: unknown, resourceName: string): DbError {
  // Handle Firestore errors with code property
  if (error && typeof error === "object" && "code" in error) {
    const firestoreError = error as { code: string; message?: string };
    const code = firestoreError.code;

    // Check for specific error codes
    if (code === "not-found") {
      return DbError.notFound(resourceName);
    }

    if (code === "already-exists") {
      return DbError.alreadyExists(resourceName);
    }

    if (code === "permission-denied" || code === "unauthenticated") {
      return DbError.permissionDenied(resourceName);
    }

    // Check if retryable
    const isRetryable = RETRYABLE_ERROR_CODES.includes(
      code as (typeof RETRYABLE_ERROR_CODES)[number]
    );

    return new DbError(
      firestoreError.message || `Database error: ${code}`,
      code,
      resourceName,
      { isRetryable }
    );
  }

  // Handle standard Error objects
  if (error instanceof Error) {
    return DbError.internal(resourceName, error.message);
  }

  // Handle unknown errors
  return DbError.internal(resourceName, String(error));
}
```

## Return Type Pattern

All database queries use tuple return type for explicit error handling:

```typescript
// Success: [null, Data]
// Error:   [DbError, null]
type QueryResult<T> = Promise<[null, T] | [DbError, null]>;
```

### Why Tuples?

1. **Explicit error handling** - Caller must handle both cases
2. **No try-catch boilerplate** - Error is part of return value
3. **Type-safe** - TypeScript narrows types correctly
4. **Consistent pattern** - Same structure across all queries

## Usage in Database Queries

### Read Operation

```typescript
export async function getResourceById(
  id: string
): Promise<[null, Resource] | [DbError, null]> {
  // 1. Input validation
  if (!id?.trim()) {
    const error = DbError.validation("Invalid id provided", RESOURCE_NAME);
    logger.warn({ errorCode: error.code }, "Validation failed");
    return [error, null];
  }

  try {
    // 2. Database query
    const doc = await db.collection(COLLECTION).doc(id).get();

    // 3. Not found check
    if (!doc.exists) {
      const error = DbError.notFound(RESOURCE_NAME);
      logger.warn({ resourceId: id, errorCode: error.code }, "Not found");
      return [error, null];
    }

    // 4. Data validation
    const data = doc.data();
    if (!data) {
      const error = DbError.dataCorruption(RESOURCE_NAME);
      logger.error({ resourceId: id, errorCode: error.code }, "Data undefined");
      return [error, null];
    }

    // 5. Success
    logger.info({ resourceId: id }, "Resource retrieved");
    return [null, transformToResource(doc.id, data)];

  } catch (error) {
    // 6. Categorize and log error
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({
      resourceId: id,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable
    }, "Query failed");
    return [dbError, null];
  }
}
```

### Create Operation

```typescript
export async function createResource(
  data: CreateResourceDto
): Promise<[null, Resource] | [DbError, null]> {
  try {
    const docRef = await db.collection(COLLECTION).add(data);

    // Option 1: Construct from input (faster, no extra read)
    const resource: Resource = {
      id: docRef.id,
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Resource;

    logger.info({ resourceId: docRef.id }, "Resource created");
    return [null, resource];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({ errorCode: dbError.code }, "Create failed");
    return [dbError, null];
  }
}
```

### Update Operation

```typescript
export async function updateResource(
  id: string,
  data: UpdateResourceDto
): Promise<[null, Resource] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid id", RESOURCE_NAME), null];
  }

  try {
    const docRef = db.collection(COLLECTION).doc(id);

    // Check if document exists
    const doc = await docRef.get();
    if (!doc.exists) {
      return [DbError.notFound(RESOURCE_NAME), null];
    }

    // Perform update
    await docRef.update({
      ...data,
      updatedAt: FieldValue.serverTimestamp(),
    });

    // Return updated resource (requires re-read for merged state)
    const updated = await docRef.get();
    return [null, transformToResource(id, updated.data()!)];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({ resourceId: id, errorCode: dbError.code }, "Update failed");
    return [dbError, null];
  }
}
```

### Delete Operation

```typescript
export async function deleteResource(
  id: string
): Promise<[null, true] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid id", RESOURCE_NAME), null];
  }

  try {
    const docRef = db.collection(COLLECTION).doc(id);

    // Optional: Check if exists before delete
    const doc = await docRef.get();
    if (!doc.exists) {
      return [DbError.notFound(RESOURCE_NAME), null];
    }

    await docRef.delete();

    logger.info({ resourceId: id }, "Resource deleted");
    return [null, true];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE_NAME);
    logger.error({ resourceId: id, errorCode: dbError.code }, "Delete failed");
    return [dbError, null];
  }
}
```

## Usage in Consumers

### In Server Actions

```typescript
export async function updateBudget(
  budgetId: string,
  formData: FormData
): ActionResponse<Budget> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Unauthorized" };
  }

  const [error, budget] = await updateBudgetInDb(budgetId, data);

  if (error) {
    // Handle specific error types
    if (error.isNotFound) {
      return { success: false, error: "Budget not found" };
    }
    if (error.isPermissionDenied) {
      return { success: false, error: "You don't have permission" };
    }
    // Generic error
    return { success: false, error: error.message };
  }

  revalidatePath("/budgets");
  return { success: true, data: budget };
}
```

### In Page Loaders

```typescript
async function loadBudget(budgetId: string) {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");

  const [error, budget] = await getBudgetById(budgetId);

  if (error) {
    // Not found → 404 page
    if (error.isNotFound) {
      notFound();
    }

    // Retryable → Let error boundary handle with retry UI
    if (error.isRetryable) {
      throw error;
    }

    // Permission → Redirect to appropriate page
    if (error.isPermissionDenied) {
      redirect("/unauthorized");
    }

    // Other errors → Generic error
    throw new Error("Unable to load budget");
  }

  return budget;
}
```

### In Route Handlers

```typescript
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const [error, resource] = await getResourceById(params.id);

  if (error) {
    if (error.isNotFound) {
      return NextResponse.json(
        { error: "Resource not found" },
        { status: 404 }
      );
    }
    if (error.isPermissionDenied) {
      return NextResponse.json(
        { error: "Permission denied" },
        { status: 403 }
      );
    }
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }

  return NextResponse.json({ data: resource });
}
```

## Logging Pattern

Always include structured context in error logs:

```typescript
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "budget-db" });

// Validation error
logger.warn({
  userId,
  errorCode: error.code
}, "Validation failed");

// Not found
logger.warn({
  userId,
  budgetId,
  errorCode: error.code
}, "Budget not found");

// Database error
logger.error({
  userId,
  budgetId,
  errorCode: dbError.code,
  isRetryable: dbError.isRetryable
}, "Database query failed");

// Success
logger.info({
  userId,
  budgetId
}, "Budget retrieved successfully");
```

## Error Code Reference

| Code | Description | Retryable | Factory Method |
|------|-------------|-----------|----------------|
| `not-found` | Document doesn't exist | No | `DbError.notFound()` |
| `already-exists` | Document already exists | No | `DbError.alreadyExists()` |
| `permission-denied` | No access to resource | No | `DbError.permissionDenied()` |
| `validation` | Input validation failed | No | `DbError.validation()` |
| `data-corruption` | Invalid document data | No | `DbError.dataCorruption()` |
| `unavailable` | Service temporarily unavailable | Yes | via `categorizeDbError()` |
| `deadline-exceeded` | Operation timed out | Yes | via `categorizeDbError()` |
| `resource-exhausted` | Quota exceeded | Yes | via `categorizeDbError()` |
| `aborted` | Operation aborted | Yes | via `categorizeDbError()` |
| `internal` | Internal server error | Yes | `DbError.internal()` |

## Best Practices

1. **Always validate inputs** before database operations
2. **Use factory methods** for common error types
3. **Log with context** at every error point
4. **Include isRetryable** in error logs for monitoring
5. **Handle not-found explicitly** in queries
6. **Check data exists** after successful get
7. **Use categorizeDbError** for unknown errors
8. **Keep error messages user-friendly** in responses
