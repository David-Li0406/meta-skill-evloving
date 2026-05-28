# Firestore Migration - Examples

## Example 1: Adding a New Field

**Scenario:** Add a `tags` field to all documents in the `budgets` collection.

**Before:**
```typescript
// Budget document structure
{
  id: "budget-1",
  name: "Monthly Budget",
  amount: 5000,
  currency: "PLN",
  createdAt: Timestamp,
  updatedAt: Timestamp
}
```

**After:**
```typescript
// Budget document structure with tags
{
  id: "budget-1",
  name: "Monthly Budget",
  amount: 5000,
  currency: "PLN",
  tags: [],  // New field
  createdAt: Timestamp,
  updatedAt: Timestamp
}
```

**Migration Script:**
```typescript
// scripts/migrations/add-tags-to-budgets.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "migration-add-tags" });

const COLLECTION_NAME = "budgets";
const BATCH_SIZE = 500;

interface MigrationStats {
  processed: number;
  updated: number;
  skipped: number;
  errors: number;
}

export async function addTagsToBudgets(options: { dryRun?: boolean } = {}) {
  const { dryRun = true } = options;

  logger.info({ dryRun }, "Starting migration: add tags to budgets");

  const stats: MigrationStats = {
    processed: 0,
    updated: 0,
    skipped: 0,
    errors: 0
  };

  try {
    const snapshot = await db.collection(COLLECTION_NAME).get();

    logger.info({ totalDocs: snapshot.size }, "Fetched documents");

    const batches: FirebaseFirestore.WriteBatch[] = [];
    let currentBatch = db.batch();
    let operationsInBatch = 0;

    for (const doc of snapshot.docs) {
      stats.processed++;

      const data = doc.data();

      // Skip if already has tags field
      if (data.tags !== undefined) {
        stats.skipped++;
        logger.debug({ docId: doc.id }, "Document already has tags field");
        continue;
      }

      if (dryRun) {
        logger.info({ docId: doc.id, currentData: data }, "Would add tags: []");
        stats.updated++;
      } else {
        currentBatch.update(doc.ref, {
          tags: [],
          updatedAt: FieldValue.serverTimestamp()
        });

        stats.updated++;
        operationsInBatch++;

        // Commit batch if it reaches size limit
        if (operationsInBatch >= BATCH_SIZE) {
          batches.push(currentBatch);
          currentBatch = db.batch();
          operationsInBatch = 0;
        }
      }
    }

    // Add remaining batch
    if (operationsInBatch > 0 && !dryRun) {
      batches.push(currentBatch);
    }

    // Commit all batches
    if (!dryRun && batches.length > 0) {
      logger.info({ batchCount: batches.length }, "Committing batches");

      for (const [index, batch] of batches.entries()) {
        await batch.commit();
        logger.info({ batchIndex: index + 1, total: batches.length }, "Batch committed");
      }
    }

    logger.info({ stats }, "Migration completed");
    return { success: true, stats };
  } catch (error) {
    logger.error({ error, stats }, "Migration failed");
    return { success: false, error, stats };
  }
}

// Run migration
if (require.main === module) {
  const dryRun = process.argv.includes("--dry-run");

  addTagsToBudgets({ dryRun })
    .then((result) => {
      console.log("Migration result:", result);
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error("Migration error:", error);
      process.exit(1);
    });
}
```

**Usage:**
```bash
# Dry run (preview changes)
npx tsx scripts/migrations/add-tags-to-budgets.ts --dry-run

# Apply migration
npx tsx scripts/migrations/add-tags-to-budgets.ts
```

---

## Example 2: Renaming a Field

**Scenario:** Rename `categoryId` to `categoryIds` (string → array) in `expenses` collection.

**Before:**
```typescript
{
  id: "expense-1",
  amount: 50,
  categoryId: "food",  // Single category
  description: "Lunch"
}
```

**After:**
```typescript
{
  id: "expense-1",
  amount: 50,
  categoryIds: ["food"],  // Array of categories
  description: "Lunch"
}
```

**Migration Script:**
```typescript
// scripts/migrations/rename-category-id.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "migration-rename-category" });

const COLLECTION_NAME = "expenses";
const BATCH_SIZE = 500;

export async function renameCategoryIdToIds(options: { dryRun?: boolean } = {}) {
  const { dryRun = true } = options;

  logger.info({ dryRun }, "Starting migration: rename categoryId to categoryIds");

  const stats = {
    processed: 0,
    updated: 0,
    skipped: 0,
    errors: 0
  };

  try {
    // Query documents that still have old field
    const snapshot = await db
      .collection(COLLECTION_NAME)
      .where("categoryId", "!=", null)
      .get();

    logger.info({ totalDocs: snapshot.size }, "Found documents with old field");

    const batches: FirebaseFirestore.WriteBatch[] = [];
    let currentBatch = db.batch();
    let operationsInBatch = 0;

    for (const doc of snapshot.docs) {
      stats.processed++;

      const data = doc.data();

      // Skip if already migrated
      if (data.categoryIds !== undefined) {
        stats.skipped++;
        continue;
      }

      if (dryRun) {
        logger.info({
          docId: doc.id,
          oldValue: data.categoryId,
          newValue: [data.categoryId]
        }, "Would rename field");
        stats.updated++;
      } else {
        // Add new field, remove old field
        currentBatch.update(doc.ref, {
          categoryIds: [data.categoryId],  // Convert to array
          categoryId: FieldValue.delete(), // Remove old field
          updatedAt: FieldValue.serverTimestamp()
        });

        stats.updated++;
        operationsInBatch++;

        if (operationsInBatch >= BATCH_SIZE) {
          batches.push(currentBatch);
          currentBatch = db.batch();
          operationsInBatch = 0;
        }
      }
    }

    if (operationsInBatch > 0 && !dryRun) {
      batches.push(currentBatch);
    }

    if (!dryRun && batches.length > 0) {
      for (const batch of batches) {
        await batch.commit();
      }
    }

    logger.info({ stats }, "Migration completed");
    return { success: true, stats };
  } catch (error) {
    logger.error({ error, stats }, "Migration failed");
    return { success: false, error, stats };
  }
}
```

---

## Example 3: Data Transformation

**Scenario:** Convert `amount` from cents (number) to object with currency.

**Before:**
```typescript
{
  id: "expense-1",
  amount: 5000,  // cents
  description: "Groceries"
}
```

**After:**
```typescript
{
  id: "expense-1",
  amount: {
    value: 5000,
    currency: "PLN"
  },
  description: "Groceries"
}
```

**Migration Script:**
```typescript
// scripts/migrations/transform-amount-to-object.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";

export async function transformAmountToObject(options: { dryRun?: boolean; defaultCurrency?: string } = {}) {
  const { dryRun = true, defaultCurrency = "PLN" } = options;

  const snapshot = await db.collection("expenses").get();

  const batch = db.batch();
  let count = 0;

  for (const doc of snapshot.docs) {
    const data = doc.data();

    // Skip if already transformed
    if (typeof data.amount === "object") {
      continue;
    }

    if (dryRun) {
      console.log({
        docId: doc.id,
        oldAmount: data.amount,
        newAmount: {
          value: data.amount,
          currency: data.currency || defaultCurrency
        }
      });
    } else {
      batch.update(doc.ref, {
        amount: {
          value: data.amount,
          currency: data.currency || defaultCurrency
        },
        updatedAt: FieldValue.serverTimestamp()
      });

      count++;

      // Commit in batches of 500
      if (count % 500 === 0) {
        await batch.commit();
      }
    }
  }

  if (!dryRun && count % 500 !== 0) {
    await batch.commit();
  }

  return { processed: snapshot.size, updated: count };
}
```

---

## Example 4: Backfilling Computed Values

**Scenario:** Add computed `totalExpenses` field to user profiles.

**Before:**
```typescript
{
  id: "user-1",
  name: "John Doe",
  email: "john@example.com"
}
```

**After:**
```typescript
{
  id: "user-1",
  name: "John Doe",
  email: "john@example.com",
  totalExpenses: 15000  // Backfilled from expenses collection
}
```

**Migration Script:**
```typescript
// scripts/migrations/backfill-total-expenses.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";

export async function backfillTotalExpenses(options: { dryRun?: boolean } = {}) {
  const { dryRun = true } = options;

  const usersSnapshot = await db.collection("users").get();

  for (const userDoc of usersSnapshot.docs) {
    const userId = userDoc.id;

    // Calculate total from expenses
    const expensesSnapshot = await db
      .collection("expenses")
      .where("userId", "==", userId)
      .get();

    const total = expensesSnapshot.docs.reduce((sum, doc) => {
      return sum + (doc.data().amount || 0);
    }, 0);

    if (dryRun) {
      console.log({
        userId,
        expenseCount: expensesSnapshot.size,
        totalExpenses: total
      });
    } else {
      await userDoc.ref.update({
        totalExpenses: total,
        updatedAt: FieldValue.serverTimestamp()
      });
    }
  }

  return { processed: usersSnapshot.size };
}
```

---

## Example 5: Removing Deprecated Fields

**Scenario:** Remove deprecated `oldStatus` field from all budgets.

**Migration Script:**
```typescript
// scripts/migrations/remove-old-status.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";

export async function removeOldStatusField(options: { dryRun?: boolean } = {}) {
  const { dryRun = true } = options;

  const snapshot = await db
    .collection("budgets")
    .where("oldStatus", "!=", null)
    .get();

  console.log(`Found ${snapshot.size} documents with oldStatus field`);

  const batch = db.batch();
  let count = 0;

  for (const doc of snapshot.docs) {
    if (dryRun) {
      console.log({
        docId: doc.id,
        oldStatus: doc.data().oldStatus,
        action: "Would delete oldStatus field"
      });
    } else {
      batch.update(doc.ref, {
        oldStatus: FieldValue.delete(),
        updatedAt: FieldValue.serverTimestamp()
      });

      count++;

      if (count % 500 === 0) {
        await batch.commit();
      }
    }
  }

  if (!dryRun && count % 500 !== 0) {
    await batch.commit();
  }

  return { processed: snapshot.size, updated: count };
}
```

---

## Example 6: Conditional Migration

**Scenario:** Update only budgets where `status === "draft"` to `status === "pending"`.

**Migration Script:**
```typescript
// scripts/migrations/update-draft-status.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";

export async function updateDraftStatus(options: { dryRun?: boolean } = {}) {
  const { dryRun = true } = options;

  // Query only documents matching condition
  const snapshot = await db
    .collection("budgets")
    .where("status", "==", "draft")
    .get();

  console.log(`Found ${snapshot.size} draft budgets`);

  const batch = db.batch();

  for (const doc of snapshot.docs) {
    if (dryRun) {
      console.log({
        docId: doc.id,
        currentStatus: "draft",
        newStatus: "pending"
      });
    } else {
      batch.update(doc.ref, {
        status: "pending",
        updatedAt: FieldValue.serverTimestamp()
      });
    }
  }

  if (!dryRun) {
    await batch.commit();
  }

  return { processed: snapshot.size };
}
```

---

## Migration Template

```typescript
// scripts/migrations/template.ts
import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "migration-[name]" });

const COLLECTION_NAME = "your-collection";
const BATCH_SIZE = 500;

interface MigrationOptions {
  dryRun?: boolean;
  batchSize?: number;
}

interface MigrationStats {
  processed: number;
  updated: number;
  skipped: number;
  errors: number;
}

export async function migrateSomething(options: MigrationOptions = {}) {
  const { dryRun = true, batchSize = BATCH_SIZE } = options;

  logger.info({ dryRun, batchSize }, "Starting migration");

  const stats: MigrationStats = {
    processed: 0,
    updated: 0,
    skipped: 0,
    errors: 0
  };

  try {
    // 1. Fetch documents (use query to filter if possible)
    const snapshot = await db.collection(COLLECTION_NAME).get();

    logger.info({ totalDocs: snapshot.size }, "Fetched documents");

    // 2. Process in batches
    const batches: FirebaseFirestore.WriteBatch[] = [];
    let currentBatch = db.batch();
    let operationsInBatch = 0;

    for (const doc of snapshot.docs) {
      stats.processed++;

      const data = doc.data();

      // 3. Check if migration is needed
      if (shouldSkip(data)) {
        stats.skipped++;
        continue;
      }

      // 4. Apply transformation
      const updates = transformData(data);

      if (dryRun) {
        logger.info({ docId: doc.id, updates }, "Would update document");
        stats.updated++;
      } else {
        currentBatch.update(doc.ref, {
          ...updates,
          updatedAt: FieldValue.serverTimestamp()
        });

        stats.updated++;
        operationsInBatch++;

        if (operationsInBatch >= batchSize) {
          batches.push(currentBatch);
          currentBatch = db.batch();
          operationsInBatch = 0;
        }
      }
    }

    // 5. Commit remaining batch
    if (operationsInBatch > 0 && !dryRun) {
      batches.push(currentBatch);
    }

    // 6. Commit all batches
    if (!dryRun && batches.length > 0) {
      logger.info({ batchCount: batches.length }, "Committing batches");

      for (const [index, batch] of batches.entries()) {
        await batch.commit();
        logger.info({ batchIndex: index + 1, total: batches.length }, "Batch committed");
      }
    }

    logger.info({ stats }, "Migration completed");
    return { success: true, stats };
  } catch (error) {
    logger.error({ error, stats }, "Migration failed");
    return { success: false, error, stats };
  }
}

function shouldSkip(data: any): boolean {
  // Implement skip logic
  return false;
}

function transformData(data: any): Record<string, any> {
  // Implement transformation logic
  return {};
}

// CLI runner
if (require.main === module) {
  const dryRun = !process.argv.includes("--apply");

  migrateSomething({ dryRun })
    .then((result) => {
      console.log("Migration result:", result);
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error("Migration error:", error);
      process.exit(1);
    });
}
```

---

## Best Practices

### 1. Always Use Dry Run First
```bash
# Preview changes
npx tsx scripts/migrations/my-migration.ts --dry-run

# Apply after verifying
npx tsx scripts/migrations/my-migration.ts
```

### 2. Make Migrations Idempotent
```typescript
// Check if already migrated
if (data.newField !== undefined) {
  stats.skipped++;
  continue;
}
```

### 3. Use Batched Writes
```typescript
// Commit every 500 operations
if (operationsInBatch >= 500) {
  await batch.commit();
  batch = db.batch();
  operationsInBatch = 0;
}
```

### 4. Log Everything
```typescript
logger.info({ docId, oldValue, newValue }, "Migrating document");
logger.error({ docId, error }, "Migration failed for document");
```

### 5. Handle Errors Gracefully
```typescript
try {
  await batch.commit();
} catch (error) {
  logger.error({ error }, "Batch commit failed");
  stats.errors++;
  // Continue with next batch
}
```

### 6. Backup Before Major Migrations
```bash
# Export collection before migration
gcloud firestore export gs://your-bucket/backup-$(date +%Y%m%d)
```

### 7. Use Queries to Filter
```typescript
// Only fetch documents that need migration
const snapshot = await db
  .collection("budgets")
  .where("oldField", "!=", null)
  .get();
```
