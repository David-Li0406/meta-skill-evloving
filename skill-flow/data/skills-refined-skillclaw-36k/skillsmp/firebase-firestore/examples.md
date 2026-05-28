# Firebase Query Examples

Complete CRUD operation examples with proper types, error handling, and logging.

## Complete Module Example

```typescript
// features/budget/server/db/budget-queries.ts
import "server-only";

import { FieldValue } from "firebase-admin/firestore";

import { db } from "~/lib/firebase";
import { categorizeDbError, DbError } from "~/lib/firebase/errors";
import { createLogger } from "~/lib/logger";

import type {
  Budget,
  CreateBudgetDto,
  UpdateBudgetDto,
} from "../../types/budget";

// ═══════════════════════════════════════════════════════════════
// Constants
// ═══════════════════════════════════════════════════════════════

const COLLECTION = "budgets";
const RESOURCE = "Budget";

// ═══════════════════════════════════════════════════════════════
// Logger
// ═══════════════════════════════════════════════════════════════

const logger = createLogger({ module: "budget-db" });

// ═══════════════════════════════════════════════════════════════
// Transform Function
// ═══════════════════════════════════════════════════════════════

function transformToBudget(
  docId: string,
  data: FirebaseFirestore.DocumentData
): Budget {
  return {
    id: docId,
    ...data,
    createdAt: data.createdAt?.toDate(),
    updatedAt: data.updatedAt?.toDate(),
  } as Budget;
}

// ═══════════════════════════════════════════════════════════════
// READ Operations
// ═══════════════════════════════════════════════════════════════

/**
 * Get a single budget by ID
 */
export async function getBudgetById(
  id: string
): Promise<[null, Budget] | [DbError, null]> {
  // Input validation
  if (!id?.trim()) {
    const error = DbError.validation("Invalid budget id provided", RESOURCE);
    logger.warn({ errorCode: error.code }, "Validation failed");
    return [error, null];
  }

  try {
    const doc = await db.collection(COLLECTION).doc(id).get();

    if (!doc.exists) {
      const error = DbError.notFound(RESOURCE);
      logger.warn({ budgetId: id, errorCode: error.code }, "Budget not found");
      return [error, null];
    }

    const data = doc.data();
    if (!data) {
      const error = DbError.dataCorruption(RESOURCE);
      logger.error({ budgetId: id, errorCode: error.code }, "Data undefined");
      return [error, null];
    }

    logger.info({ budgetId: id }, "Budget retrieved");
    return [null, transformToBudget(doc.id, data)];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({
      budgetId: id,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable,
    }, "Query failed");
    return [dbError, null];
  }
}

/**
 * Get all budgets for a user
 */
export async function getBudgetsByUserId(
  userId: string
): Promise<[null, Budget[]] | [DbError, null]> {
  if (!userId?.trim()) {
    const error = DbError.validation("Invalid userId provided", RESOURCE);
    logger.warn({ errorCode: error.code }, "Validation failed");
    return [error, null];
  }

  try {
    const snapshot = await db
      .collection(COLLECTION)
      .where("userId", "==", userId)
      .orderBy("createdAt", "desc")
      .get();

    const budgets = snapshot.docs.map((doc) =>
      transformToBudget(doc.id, doc.data())
    );

    logger.info({ userId, count: budgets.length }, "Budgets retrieved");
    return [null, budgets];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({
      userId,
      errorCode: dbError.code,
      isRetryable: dbError.isRetryable,
    }, "Query failed");
    return [dbError, null];
  }
}

/**
 * Get budgets with pagination
 */
export async function getBudgetsPaginated(
  userId: string,
  options: { limit?: number; startAfter?: string } = {}
): Promise<[null, { budgets: Budget[]; hasMore: boolean }] | [DbError, null]> {
  const { limit = 10, startAfter } = options;

  if (!userId?.trim()) {
    return [DbError.validation("Invalid userId", RESOURCE), null];
  }

  try {
    let query = db
      .collection(COLLECTION)
      .where("userId", "==", userId)
      .orderBy("createdAt", "desc")
      .limit(limit + 1); // Fetch one extra to check for more

    // Start after cursor
    if (startAfter) {
      const cursorDoc = await db.collection(COLLECTION).doc(startAfter).get();
      if (cursorDoc.exists) {
        query = query.startAfter(cursorDoc);
      }
    }

    const snapshot = await query.get();
    const docs = snapshot.docs;

    // Check if there are more results
    const hasMore = docs.length > limit;
    const budgets = docs
      .slice(0, limit)
      .map((doc) => transformToBudget(doc.id, doc.data()));

    logger.info({ userId, count: budgets.length, hasMore }, "Paginated query");
    return [null, { budgets, hasMore }];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ userId, errorCode: dbError.code }, "Pagination failed");
    return [dbError, null];
  }
}

// ═══════════════════════════════════════════════════════════════
// CREATE Operations
// ═══════════════════════════════════════════════════════════════

/**
 * Create a new budget
 */
export async function createBudget(
  data: Omit<CreateBudgetDto, "createdAt" | "updatedAt">
): Promise<[null, Budget] | [DbError, null]> {
  // Validate required fields
  if (!data.userId?.trim()) {
    return [DbError.validation("userId is required", RESOURCE), null];
  }
  if (!data.name?.trim()) {
    return [DbError.validation("name is required", RESOURCE), null];
  }

  try {
    const createData: CreateBudgetDto = {
      ...data,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp(),
    };

    const docRef = await db.collection(COLLECTION).add(createData);

    // Construct return object without extra read
    const budget: Budget = {
      id: docRef.id,
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Budget;

    logger.info({ budgetId: docRef.id, userId: data.userId }, "Budget created");
    return [null, budget];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({
      userId: data.userId,
      errorCode: dbError.code,
    }, "Create failed");
    return [dbError, null];
  }
}

/**
 * Create budget with specific ID (for predefined data)
 */
export async function createBudgetWithId(
  id: string,
  data: Omit<CreateBudgetDto, "createdAt" | "updatedAt">
): Promise<[null, Budget] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("id is required", RESOURCE), null];
  }

  try {
    // Check if already exists
    const existing = await db.collection(COLLECTION).doc(id).get();
    if (existing.exists) {
      return [DbError.alreadyExists(RESOURCE), null];
    }

    const createData: CreateBudgetDto = {
      ...data,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp(),
    };

    await db.collection(COLLECTION).doc(id).set(createData);

    const budget: Budget = {
      id,
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Budget;

    logger.info({ budgetId: id }, "Budget created with ID");
    return [null, budget];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ budgetId: id, errorCode: dbError.code }, "Create failed");
    return [dbError, null];
  }
}

// ═══════════════════════════════════════════════════════════════
// UPDATE Operations
// ═══════════════════════════════════════════════════════════════

/**
 * Update a budget
 */
export async function updateBudget(
  id: string,
  data: UpdateBudgetDto
): Promise<[null, Budget] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid budget id", RESOURCE), null];
  }

  try {
    const docRef = db.collection(COLLECTION).doc(id);

    // Check if exists
    const doc = await docRef.get();
    if (!doc.exists) {
      const error = DbError.notFound(RESOURCE);
      logger.warn({ budgetId: id, errorCode: error.code }, "Not found");
      return [error, null];
    }

    // Perform update
    await docRef.update({
      ...data,
      updatedAt: FieldValue.serverTimestamp(),
    });

    // Re-read for merged state
    const updated = await docRef.get();
    const budget = transformToBudget(id, updated.data()!);

    logger.info({ budgetId: id }, "Budget updated");
    return [null, budget];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({
      budgetId: id,
      errorCode: dbError.code,
    }, "Update failed");
    return [dbError, null];
  }
}

/**
 * Update specific fields (partial update)
 */
export async function updateBudgetFields(
  id: string,
  fields: Partial<Pick<Budget, "name" | "amount" | "status">>
): Promise<[null, true] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid budget id", RESOURCE), null];
  }

  if (Object.keys(fields).length === 0) {
    return [DbError.validation("No fields to update", RESOURCE), null];
  }

  try {
    const docRef = db.collection(COLLECTION).doc(id);

    // Check exists
    const doc = await docRef.get();
    if (!doc.exists) {
      return [DbError.notFound(RESOURCE), null];
    }

    await docRef.update({
      ...fields,
      updatedAt: FieldValue.serverTimestamp(),
    });

    logger.info({ budgetId: id, fields: Object.keys(fields) }, "Fields updated");
    return [null, true];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ budgetId: id, errorCode: dbError.code }, "Update failed");
    return [dbError, null];
  }
}

// ═══════════════════════════════════════════════════════════════
// DELETE Operations
// ═══════════════════════════════════════════════════════════════

/**
 * Delete a budget
 */
export async function deleteBudget(
  id: string
): Promise<[null, true] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid budget id", RESOURCE), null];
  }

  try {
    const docRef = db.collection(COLLECTION).doc(id);

    // Check exists
    const doc = await docRef.get();
    if (!doc.exists) {
      const error = DbError.notFound(RESOURCE);
      logger.warn({ budgetId: id, errorCode: error.code }, "Not found");
      return [error, null];
    }

    await docRef.delete();

    logger.info({ budgetId: id }, "Budget deleted");
    return [null, true];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({
      budgetId: id,
      errorCode: dbError.code,
    }, "Delete failed");
    return [dbError, null];
  }
}

/**
 * Delete all budgets for a user
 */
export async function deleteUserBudgets(
  userId: string
): Promise<[null, number] | [DbError, null]> {
  if (!userId?.trim()) {
    return [DbError.validation("Invalid userId", RESOURCE), null];
  }

  try {
    const snapshot = await db
      .collection(COLLECTION)
      .where("userId", "==", userId)
      .get();

    if (snapshot.empty) {
      logger.info({ userId }, "No budgets to delete");
      return [null, 0];
    }

    // Batch delete
    const batch = db.batch();
    snapshot.docs.forEach((doc) => {
      batch.delete(doc.ref);
    });

    await batch.commit();

    logger.info({ userId, count: snapshot.size }, "User budgets deleted");
    return [null, snapshot.size];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ userId, errorCode: dbError.code }, "Batch delete failed");
    return [dbError, null];
  }
}

// ═══════════════════════════════════════════════════════════════
// BATCH Operations
// ═══════════════════════════════════════════════════════════════

/**
 * Create multiple budgets in a batch
 */
export async function createBudgetsBatch(
  budgets: Array<Omit<CreateBudgetDto, "createdAt" | "updatedAt">>
): Promise<[null, Budget[]] | [DbError, null]> {
  if (budgets.length === 0) {
    return [null, []];
  }

  if (budgets.length > 500) {
    return [
      DbError.validation("Batch size exceeds 500 documents", RESOURCE),
      null,
    ];
  }

  try {
    const batch = db.batch();
    const results: Budget[] = [];

    for (const data of budgets) {
      const docRef = db.collection(COLLECTION).doc();
      const createData: CreateBudgetDto = {
        ...data,
        createdAt: FieldValue.serverTimestamp(),
        updatedAt: FieldValue.serverTimestamp(),
      };

      batch.set(docRef, createData);

      results.push({
        id: docRef.id,
        ...data,
        createdAt: new Date(),
        updatedAt: new Date(),
      } as Budget);
    }

    await batch.commit();

    logger.info({ count: results.length }, "Batch create completed");
    return [null, results];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ errorCode: dbError.code }, "Batch create failed");
    return [dbError, null];
  }
}
```

## Query with Composite Index

```typescript
/**
 * Complex query requiring composite index
 * Create index: userId ASC, status ASC, createdAt DESC
 */
export async function getActiveBudgetsByUser(
  userId: string,
  options: { limit?: number } = {}
): Promise<[null, Budget[]] | [DbError, null]> {
  const { limit = 20 } = options;

  try {
    const snapshot = await db
      .collection(COLLECTION)
      .where("userId", "==", userId)
      .where("status", "==", "active")
      .orderBy("createdAt", "desc")
      .limit(limit)
      .get();

    const budgets = snapshot.docs.map((doc) =>
      transformToBudget(doc.id, doc.data())
    );

    return [null, budgets];

  } catch (error) {
    // Check for index error
    if (error instanceof Error && error.message.includes("index")) {
      logger.error({ error: error.message }, "Missing composite index");
    }
    return [categorizeDbError(error, RESOURCE), null];
  }
}
```

## Subcollection Query

```typescript
// features/budget/server/db/expense-queries.ts

const BUDGET_COLLECTION = "budgets";
const EXPENSE_SUBCOLLECTION = "expenses";

/**
 * Get expenses for a budget (subcollection)
 */
export async function getExpensesByBudget(
  budgetId: string
): Promise<[null, Expense[]] | [DbError, null]> {
  if (!budgetId?.trim()) {
    return [DbError.validation("Invalid budgetId", "Expense"), null];
  }

  try {
    const snapshot = await db
      .collection(BUDGET_COLLECTION)
      .doc(budgetId)
      .collection(EXPENSE_SUBCOLLECTION)
      .orderBy("date", "desc")
      .get();

    const expenses = snapshot.docs.map((doc) =>
      transformToExpense(doc.id, doc.data())
    );

    return [null, expenses];

  } catch (error) {
    return [categorizeDbError(error, "Expense"), null];
  }
}

/**
 * Add expense to budget
 */
export async function addExpense(
  budgetId: string,
  data: Omit<CreateExpenseDto, "createdAt" | "updatedAt">
): Promise<[null, Expense] | [DbError, null]> {
  try {
    const expenseData: CreateExpenseDto = {
      ...data,
      createdAt: FieldValue.serverTimestamp(),
      updatedAt: FieldValue.serverTimestamp(),
    };

    const docRef = await db
      .collection(BUDGET_COLLECTION)
      .doc(budgetId)
      .collection(EXPENSE_SUBCOLLECTION)
      .add(expenseData);

    const expense: Expense = {
      id: docRef.id,
      ...data,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Expense;

    return [null, expense];

  } catch (error) {
    return [categorizeDbError(error, "Expense"), null];
  }
}
```

## Transaction Example

```typescript
/**
 * Transfer amount between budgets (atomic operation)
 */
export async function transferBetweenBudgets(
  fromId: string,
  toId: string,
  amount: number
): Promise<[null, true] | [DbError, null]> {
  if (amount <= 0) {
    return [DbError.validation("Amount must be positive", RESOURCE), null];
  }

  try {
    await db.runTransaction(async (transaction) => {
      const fromRef = db.collection(COLLECTION).doc(fromId);
      const toRef = db.collection(COLLECTION).doc(toId);

      const [fromDoc, toDoc] = await Promise.all([
        transaction.get(fromRef),
        transaction.get(toRef),
      ]);

      if (!fromDoc.exists || !toDoc.exists) {
        throw new Error("One or both budgets not found");
      }

      const fromData = fromDoc.data()!;
      const toData = toDoc.data()!;

      if (fromData.amount < amount) {
        throw new Error("Insufficient funds");
      }

      transaction.update(fromRef, {
        amount: fromData.amount - amount,
        updatedAt: FieldValue.serverTimestamp(),
      });

      transaction.update(toRef, {
        amount: toData.amount + amount,
        updatedAt: FieldValue.serverTimestamp(),
      });
    });

    logger.info({ fromId, toId, amount }, "Transfer completed");
    return [null, true];

  } catch (error) {
    const dbError = categorizeDbError(error, RESOURCE);
    logger.error({ fromId, toId, amount, errorCode: dbError.code }, "Transfer failed");
    return [dbError, null];
  }
}
```

## Real-time Listener (for special cases)

```typescript
/**
 * Set up real-time listener for budget changes
 * Note: Admin SDK listeners are for server-side use only
 */
export function watchBudget(
  budgetId: string,
  onUpdate: (budget: Budget | null) => void,
  onError: (error: DbError) => void
): () => void {
  const unsubscribe = db
    .collection(COLLECTION)
    .doc(budgetId)
    .onSnapshot(
      (doc) => {
        if (doc.exists) {
          onUpdate(transformToBudget(doc.id, doc.data()!));
        } else {
          onUpdate(null);
        }
      },
      (error) => {
        onError(categorizeDbError(error, RESOURCE));
      }
    );

  return unsubscribe;
}
```
