# Firebase Best Practices & Patterns

Best practices, common patterns, and anti-patterns for Firestore database operations.

## Best Practices

### 1. Always Validate Input

```typescript
// ✅ Good - Validate before any database operation
export async function getById(id: string): Promise<[null, Resource] | [DbError, null]> {
  if (!id?.trim()) {
    return [DbError.validation("Invalid id provided", RESOURCE), null];
  }
  // ... proceed with query
}

// ❌ Bad - No input validation
export async function getById(id: string) {
  const doc = await db.collection("items").doc(id).get(); // Will fail with cryptic error
}
```

### 2. Use Tuple Return Pattern

```typescript
// ✅ Good - Explicit error handling with tuples
export async function getById(id: string): Promise<[null, Resource] | [DbError, null]> {
  try {
    // ...
    return [null, resource];
  } catch (error) {
    return [categorizeDbError(error, RESOURCE), null];
  }
}

// ❌ Bad - Throwing exceptions
export async function getById(id: string): Promise<Resource> {
  try {
    // ...
    return resource;
  } catch (error) {
    throw new Error("Database error"); // Loses error context
  }
}
```

### 3. Check Document Exists and Data

```typescript
// ✅ Good - Check both existence and data
const doc = await db.collection(COLLECTION).doc(id).get();

if (!doc.exists) {
  return [DbError.notFound(RESOURCE), null];
}

const data = doc.data();
if (!data) {
  return [DbError.dataCorruption(RESOURCE), null];
}

return [null, transform(doc.id, data)];

// ❌ Bad - Assuming data exists
const doc = await db.collection(COLLECTION).doc(id).get();
return transform(doc.id, doc.data()!); // May crash
```

### 4. Log at Every Error Point

```typescript
// ✅ Good - Structured logging with context
if (!doc.exists) {
  const error = DbError.notFound(RESOURCE);
  logger.warn({ resourceId: id, errorCode: error.code }, "Resource not found");
  return [error, null];
}

// ❌ Bad - No logging
if (!doc.exists) {
  return [DbError.notFound(RESOURCE), null]; // Silent failure
}
```

### 5. Use Constants for Collection Names

```typescript
// ✅ Good - Constants at top of file
const COLLECTION = "budgets";
const RESOURCE = "Budget";

export async function getBudgetById(id: string) {
  const doc = await db.collection(COLLECTION).doc(id).get();
  // ...
}

// ❌ Bad - Hardcoded strings
export async function getBudgetById(id: string) {
  const doc = await db.collection("budgets").doc(id).get();
  // Typo-prone, hard to refactor
}
```

### 6. Use server-only Package

```typescript
// ✅ Good - Prevent client-side bundling
import "server-only";

import { db } from "~/lib/firebase";

// ❌ Bad - Can accidentally be imported on client
import { db } from "~/lib/firebase";
```

### 7. Create Transform Functions

```typescript
// ✅ Good - Dedicated transform function
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

// Usage
return [null, transformToBudget(doc.id, data)];

// ❌ Bad - Inline transformation
return [null, {
  id: doc.id,
  ...doc.data(),
  createdAt: doc.data()?.createdAt?.toDate(),
  // Duplicated everywhere, easy to miss fields
}];
```

### 8. Use FieldValue for Timestamps

```typescript
// ✅ Good - Server timestamp for consistency
const data: CreateBudgetDto = {
  name: "Budget",
  createdAt: FieldValue.serverTimestamp(),
  updatedAt: FieldValue.serverTimestamp(),
};

// ❌ Bad - Client-side date
const data = {
  name: "Budget",
  createdAt: new Date(), // Client clock may be wrong
  updatedAt: new Date(),
};
```

### 9. Avoid Unnecessary Reads

```typescript
// ✅ Good - Construct object from input (no extra read)
export async function createBudget(data: CreateBudgetDto) {
  const docRef = await db.collection(COLLECTION).add(data);

  // Construct from known input
  const budget: Budget = {
    id: docRef.id,
    ...data,
    createdAt: new Date(),
    updatedAt: new Date(),
  } as Budget;

  return [null, budget];
}

// ❌ Bad - Extra read after create
export async function createBudget(data: CreateBudgetDto) {
  const docRef = await db.collection(COLLECTION).add(data);

  // Unnecessary read
  const doc = await docRef.get();
  return [null, transformToBudget(doc.id, doc.data()!)];
}
```

### 10. Batch Operations for Multiple Writes

```typescript
// ✅ Good - Batch for multiple operations
const batch = db.batch();

for (const item of items) {
  const docRef = db.collection(COLLECTION).doc();
  batch.set(docRef, item);
}

await batch.commit(); // Single network call

// ❌ Bad - Sequential writes
for (const item of items) {
  await db.collection(COLLECTION).add(item); // N network calls
}
```

## Anti-Patterns to Avoid

### 1. Mixing Async Patterns

```typescript
// ❌ Bad - Mixing async/await with callbacks
db.collection("items").get().then((snapshot) => {
  snapshot.docs.forEach(async (doc) => { // async in forEach!
    await processDoc(doc); // Won't wait properly
  });
});

// ✅ Good - Consistent async/await
const snapshot = await db.collection("items").get();
for (const doc of snapshot.docs) {
  await processDoc(doc);
}

// Or parallel
await Promise.all(snapshot.docs.map((doc) => processDoc(doc)));
```

### 2. Ignoring Errors

```typescript
// ❌ Bad - Empty catch
try {
  await db.collection("items").doc(id).delete();
} catch (error) {
  // Silent failure
}

// ✅ Good - Handle and log
try {
  await db.collection("items").doc(id).delete();
} catch (error) {
  const dbError = categorizeDbError(error, RESOURCE);
  logger.error({ id, errorCode: dbError.code }, "Delete failed");
  return [dbError, null];
}
```

### 3. Over-fetching Data

```typescript
// ❌ Bad - Fetching all fields when only need few
const snapshot = await db.collection("users").get();
const names = snapshot.docs.map((doc) => doc.data().name);

// ✅ Good - Use select() for specific fields
const snapshot = await db
  .collection("users")
  .select("name", "email") // Only fetch needed fields
  .get();
```

### 4. N+1 Query Pattern

```typescript
// ❌ Bad - Query in a loop
const budgets = await getBudgets(userId);
for (const budget of budgets) {
  const expenses = await getExpenses(budget.id); // N queries!
}

// ✅ Good - Batch query or redesign data model
const budgets = await getBudgets(userId);
const budgetIds = budgets.map((b) => b.id);

// Use collection group query or denormalize data
const expenses = await db
  .collectionGroup("expenses")
  .where("budgetId", "in", budgetIds.slice(0, 10)) // Firestore limit
  .get();
```

### 5. Using any Type

```typescript
// ❌ Bad - Using any
const data: any = doc.data();
return data;

// ✅ Good - Proper typing
const data = doc.data() as BudgetFirestore;
return transformToBudget(doc.id, data);
```

### 6. Hardcoded Limits

```typescript
// ❌ Bad - Magic numbers
const snapshot = await db.collection("items").limit(100).get();

// ✅ Good - Named constants or parameters
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

export async function getItems(options: { limit?: number } = {}) {
  const limit = Math.min(options.limit || DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE);
  // ...
}
```

## Performance Patterns

### 1. Use Indexes for Compound Queries

```typescript
// Requires composite index: userId ASC, status ASC, createdAt DESC
const snapshot = await db
  .collection("budgets")
  .where("userId", "==", userId)
  .where("status", "==", "active")
  .orderBy("createdAt", "desc")
  .get();
```

Create in `firestore.indexes.json`:
```json
{
  "indexes": [
    {
      "collectionGroup": "budgets",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "status", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

### 2. Denormalize for Read Performance

```typescript
// Instead of joining collections, denormalize
type Budget = {
  id: string;
  userId: string;
  userName: string; // Denormalized from users collection
  // ...
};

// Update denormalized data when source changes
export async function updateUserName(userId: string, newName: string) {
  // Update user document
  await db.collection("users").doc(userId).update({ name: newName });

  // Update all budgets with this user
  const budgets = await db
    .collection("budgets")
    .where("userId", "==", userId)
    .get();

  const batch = db.batch();
  budgets.docs.forEach((doc) => {
    batch.update(doc.ref, { userName: newName });
  });

  await batch.commit();
}
```

### 3. Use Cursors for Pagination

```typescript
// ✅ Good - Cursor-based pagination
export async function getPage(startAfterDoc?: DocumentSnapshot) {
  let query = db.collection("items").orderBy("createdAt").limit(20);

  if (startAfterDoc) {
    query = query.startAfter(startAfterDoc);
  }

  return query.get();
}

// ❌ Bad - Offset pagination (expensive at scale)
export async function getPage(offset: number) {
  return db.collection("items")
    .orderBy("createdAt")
    .offset(offset) // Reads and discards offset documents
    .limit(20)
    .get();
}
```

## Security Patterns

### 1. Validate User Ownership

```typescript
export async function getBudgetForUser(
  budgetId: string,
  userId: string
): Promise<[null, Budget] | [DbError, null]> {
  const [error, budget] = await getBudgetById(budgetId);

  if (error) return [error, null];

  // Verify ownership
  if (budget.userId !== userId) {
    logger.warn({ budgetId, userId }, "Unauthorized access attempt");
    return [DbError.permissionDenied(RESOURCE), null];
  }

  return [null, budget];
}
```

### 2. Sanitize User Input

```typescript
export async function createBudget(data: CreateBudgetInput) {
  // Sanitize string inputs
  const sanitized = {
    name: data.name.trim().slice(0, 100), // Trim and limit length
    description: data.description?.trim().slice(0, 500),
    // Don't allow users to set system fields
    // userId: data.userId, // ❌ Don't trust client
  };

  // Set userId from authenticated session
  const { userId } = await auth();

  const createData: CreateBudgetDto = {
    ...sanitized,
    userId, // ✅ From trusted source
    createdAt: FieldValue.serverTimestamp(),
    updatedAt: FieldValue.serverTimestamp(),
  };

  return db.collection(COLLECTION).add(createData);
}
```

### 3. Use Transactions for Critical Operations

```typescript
// Money transfer must be atomic
export async function transfer(fromId: string, toId: string, amount: number) {
  return db.runTransaction(async (transaction) => {
    const fromDoc = await transaction.get(db.collection("accounts").doc(fromId));
    const toDoc = await transaction.get(db.collection("accounts").doc(toId));

    if (!fromDoc.exists || !toDoc.exists) {
      throw new Error("Account not found");
    }

    const fromBalance = fromDoc.data()!.balance;
    if (fromBalance < amount) {
      throw new Error("Insufficient funds");
    }

    transaction.update(fromDoc.ref, { balance: fromBalance - amount });
    transaction.update(toDoc.ref, { balance: toDoc.data()!.balance + amount });
  });
}
```

## File Organization

```
features/
└── budget/
    ├── types/
    │   └── budget.ts              # Type definitions
    ├── data/
    │   └── predefined-budgets.ts  # Seed data (if any)
    └── server/
        └── db/
            ├── budget-queries.ts   # CRUD operations
            └── seed-budgets.ts     # Seeding logic (if any)
```

## Checklist

Before submitting database code:

- [ ] Input validation for all parameters
- [ ] Tuple return pattern used
- [ ] Document existence checked
- [ ] Data existence checked after `.data()`
- [ ] Structured logging at error points
- [ ] Constants for collection/resource names
- [ ] `server-only` import present
- [ ] Transform function for type conversion
- [ ] No unnecessary database reads
- [ ] Batch operations for multiple writes
- [ ] User ownership/permissions verified
- [ ] No sensitive data in logs
