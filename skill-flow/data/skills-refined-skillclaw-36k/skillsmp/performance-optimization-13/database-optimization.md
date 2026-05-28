# Database Query Optimization

## Query Performance Principles

1. **Always limit results** - Never fetch unbounded collections
2. **Use indexes** - Ensure queries use composite indexes
3. **Fetch in parallel** - Use Promise.all for independent queries
4. **Avoid N+1** - Batch related data fetching
5. **Denormalize for reads** - Duplicate data to avoid joins

## Firestore-Specific Patterns

### Efficient Queries

```typescript
// ❌ Bad: No limit, fetches all documents
const query = db.collection("budgets");

// ❌ Bad: Client-side filtering
const allDocs = await db.collection("budgets").get();
const filtered = allDocs.docs.filter(d => d.data().userId === userId);

// ✅ Good: Server-side filtering with limit
const query = db.collection("budgets")
  .where("userId", "==", userId)
  .orderBy("createdAt", "desc")
  .limit(20);
```

### Pagination

```typescript
// Cursor-based pagination (efficient)
async function getPagedResults(
  userId: string,
  pageSize: number = 20,
  lastDoc?: QueryDocumentSnapshot
) {
  let query = db.collection("budgets")
    .where("userId", "==", userId)
    .orderBy("createdAt", "desc")
    .limit(pageSize);

  if (lastDoc) {
    query = query.startAfter(lastDoc);
  }

  const snapshot = await query.get();

  return {
    items: snapshot.docs.map(transform),
    lastDoc: snapshot.docs[snapshot.docs.length - 1],
    hasMore: snapshot.docs.length === pageSize
  };
}
```

### Composite Indexes

```typescript
// Queries requiring indexes
const query = db.collection("expenses")
  .where("userId", "==", userId)
  .where("category", "==", "food")
  .orderBy("date", "desc");

// Create index in Firebase Console or firestore.indexes.json
{
  "indexes": [
    {
      "collectionGroup": "expenses",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "category", "order": "ASCENDING" },
        { "fieldPath": "date", "order": "DESCENDING" }
      ]
    }
  ]
}
```

## Avoiding N+1 Queries

### Problem: Fetching Related Data in Loop

```typescript
// ❌ Bad: N+1 queries
async function getBudgetsWithExpenses(userId: string) {
  const budgets = await getBudgets(userId);

  // This makes N additional queries!
  for (const budget of budgets) {
    budget.expenses = await getExpenses(budget.id);
  }

  return budgets;
}
```

### Solution 1: Batch Query

```typescript
// ✅ Good: Batch query
async function getBudgetsWithExpenses(userId: string) {
  const budgets = await getBudgets(userId);
  const budgetIds = budgets.map(b => b.id);

  // Single query for all expenses
  const allExpenses = await db.collection("expenses")
    .where("budgetId", "in", budgetIds.slice(0, 30))  // Firestore "in" limit
    .get();

  // Group by budget
  const expensesByBudget = groupBy(allExpenses, "budgetId");

  return budgets.map(budget => ({
    ...budget,
    expenses: expensesByBudget[budget.id] || []
  }));
}
```

### Solution 2: Denormalization

```typescript
// Store expense summary in budget document
interface Budget {
  id: string;
  name: string;
  totalExpenses: number;      // Denormalized
  expenseCount: number;       // Denormalized
  lastExpenseDate: Date;      // Denormalized
}

// Update on expense create/update/delete
async function addExpense(budgetId: string, amount: number) {
  const batch = db.batch();

  // Add expense
  const expenseRef = db.collection("expenses").doc();
  batch.set(expenseRef, { budgetId, amount, date: new Date() });

  // Update denormalized data
  const budgetRef = db.collection("budgets").doc(budgetId);
  batch.update(budgetRef, {
    totalExpenses: FieldValue.increment(amount),
    expenseCount: FieldValue.increment(1),
    lastExpenseDate: new Date()
  });

  await batch.commit();
}
```

## Parallel Data Fetching

### Independent Queries

```typescript
// ❌ Bad: Sequential (waterfall)
async function loadDashboard(userId: string) {
  const user = await getUser(userId);
  const budgets = await getBudgets(userId);
  const expenses = await getRecentExpenses(userId);
  const notifications = await getNotifications(userId);
  return { user, budgets, expenses, notifications };
}

// ✅ Good: Parallel
async function loadDashboard(userId: string) {
  const [user, budgets, expenses, notifications] = await Promise.all([
    getUser(userId),
    getBudgets(userId),
    getRecentExpenses(userId),
    getNotifications(userId)
  ]);
  return { user, budgets, expenses, notifications };
}
```

### With Error Handling

```typescript
async function loadDashboard(userId: string) {
  const results = await Promise.allSettled([
    getUser(userId),
    getBudgets(userId),
    getNotifications(userId)
  ]);

  const [userResult, budgetsResult, notificationsResult] = results;

  return {
    user: userResult.status === "fulfilled" ? userResult.value : null,
    budgets: budgetsResult.status === "fulfilled" ? budgetsResult.value : [],
    notifications: notificationsResult.status === "fulfilled"
      ? notificationsResult.value
      : [],
    errors: results.filter(r => r.status === "rejected")
  };
}
```

## Caching Strategies

### Next.js Data Cache

```typescript
// Automatic caching in Server Components
async function BudgetList({ userId }: { userId: string }) {
  // Cached by default
  const [error, budgets] = await getBudgets(userId);
  return <List items={budgets} />;
}

// Time-based revalidation
export const revalidate = 60;  // Revalidate every 60 seconds

// On-demand revalidation
import { revalidatePath, revalidateTag } from "next/cache";

// After mutation
await createBudget(data);
revalidatePath("/budgets");
// or
revalidateTag("budgets");
```

### Request Deduplication

```typescript
// React automatically dedupes fetch requests in same render pass
async function Page() {
  return (
    <>
      <UserHeader />  {/* Calls getUser() */}
      <UserProfile /> {/* Also calls getUser() - deduped! */}
    </>
  );
}
```

## Query Performance Logging

```typescript
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "db-performance" });

export async function measureQuery<T>(
  name: string,
  queryFn: () => Promise<T>
): Promise<T> {
  const start = performance.now();

  try {
    const result = await queryFn();
    const duration = Math.round(performance.now() - start);

    if (duration > 500) {
      logger.warn({ query: name, durationMs: duration }, "Slow query detected");
    } else {
      logger.debug({ query: name, durationMs: duration }, "Query completed");
    }

    return result;
  } catch (error) {
    const duration = Math.round(performance.now() - start);
    logger.error({ query: name, durationMs: duration, error }, "Query failed");
    throw error;
  }
}

// Usage
const budgets = await measureQuery("getBudgets", () => getBudgets(userId));
```

## Anti-Patterns

### Don't Fetch Without Limits

```typescript
// ❌ Dangerous: Could fetch millions of documents
const all = await db.collection("logs").get();

// ✅ Safe: Always limit
const recent = await db.collection("logs")
  .orderBy("timestamp", "desc")
  .limit(100)
  .get();
```

### Don't Filter Client-Side

```typescript
// ❌ Bad: Fetches all, filters on client
const allUsers = await db.collection("users").get();
const activeUsers = allUsers.docs.filter(d => d.data().active);

// ✅ Good: Filter on server
const activeUsers = await db.collection("users")
  .where("active", "==", true)
  .get();
```

### Don't Ignore Query Costs

```typescript
// ❌ Bad: Complex query with high read cost
const query = db.collection("expenses")
  .where("userId", "==", userId)
  .where("amount", ">", 100)
  .where("category", "in", ["food", "transport", "entertainment"])
  .orderBy("date", "desc");

// ✅ Better: Simplify or denormalize
// Consider storing "highValue" boolean for amounts > 100
const query = db.collection("expenses")
  .where("userId", "==", userId)
  .where("highValue", "==", true)
  .orderBy("date", "desc")
  .limit(50);
```
