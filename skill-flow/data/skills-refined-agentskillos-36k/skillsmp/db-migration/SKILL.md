---
name: db-migration
version: 1.0.0
lastUpdated: 2026-01-18
description: Generate Firestore data migration scripts for schema changes, field additions, and data transformations. Use when migrating data, adding fields, or restructuring collections.
tags: [database, firebase, firestore, migration, schema]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Add 'tags' field to all budget documents
  - Rename 'categoryId' to 'categoryIds' across expenses collection
  - Migrate user preferences to new structure
  - Remove deprecated 'oldField' from all documents
---

# Firestore Migration Skill

Generate safe, idempotent migration scripts for Firestore data changes. This skill helps you evolve your database schema without data loss.

## Context

This skill creates migration scripts for:

- Adding new fields to existing documents
- Renaming or restructuring fields
- Transforming data formats
- Removing deprecated fields
- Backfilling computed values
- Splitting or merging collections

## Migration Principles

1. **Idempotent**: Running twice produces the same result
2. **Resumable**: Can continue from where it left off if interrupted
3. **Dry-run first**: Always preview changes before applying
4. **Batched**: Process documents in batches to avoid timeouts
5. **Logged**: Track progress and errors for debugging

## Instructions

When the user requests a migration:

### 1. Analyze the Change

Gather information about:
- Source collection name
- Current document structure
- Target document structure
- Number of documents affected (estimate)
- Any dependencies or relationships

### 2. Assess Risk Level

| Risk | Criteria | Approach |
|------|----------|----------|
| Low | Adding optional field | Direct migration |
| Medium | Restructuring data | Migration with validation |
| High | Removing/renaming fields | Dual-write period recommended |
| Critical | Changing primary keys | Manual review required |

### 3. Generate Migration Script

**File Location:** `scripts/migrations/YYYY-MM-DD-description.ts`

**Script Template:**

```typescript
/**
 * Migration: [Description]
 * Created: [Date]
 * Author: [Name]
 *
 * Purpose:
 * [Detailed description of what this migration does]
 *
 * Affected Collection: [collection-name]
 * Estimated Documents: [number]
 *
 * Rollback Strategy:
 * [How to undo this migration if needed]
 */

import { db } from "~/lib/firebase";
import { FieldValue } from "firebase-admin/firestore";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "migration-[name]" });

// Configuration
const COLLECTION_NAME = "collection-name";
const BATCH_SIZE = 500;
const DRY_RUN_DEFAULT = true;

interface MigrationOptions {
  dryRun?: boolean;
  startAfter?: string; // Document ID to resume from
  limit?: number; // Max documents to process (for testing)
}

interface MigrationResult {
  processed: number;
  updated: number;
  skipped: number;
  errors: number;
  dryRun: boolean;
  lastDocId?: string;
}

export async function migrate(
  options: MigrationOptions = {}
): Promise<MigrationResult> {
  const { dryRun = DRY_RUN_DEFAULT, startAfter, limit } = options;

  logger.info({ dryRun, startAfter, limit }, "Starting migration");

  const result: MigrationResult = {
    processed: 0,
    updated: 0,
    skipped: 0,
    errors: 0,
    dryRun
  };

  try {
    let query = db
      .collection(COLLECTION_NAME)
      .orderBy("__name__")
      .limit(BATCH_SIZE);

    if (startAfter) {
      const startDoc = await db.collection(COLLECTION_NAME).doc(startAfter).get();
      if (startDoc.exists) {
        query = query.startAfter(startDoc);
      }
    }

    let hasMore = true;
    let totalLimit = limit ?? Infinity;

    while (hasMore && result.processed < totalLimit) {
      const snapshot = await query.get();

      if (snapshot.empty) {
        hasMore = false;
        break;
      }

      const batch = db.batch();
      let batchCount = 0;

      for (const doc of snapshot.docs) {
        if (result.processed >= totalLimit) break;

        result.processed++;
        result.lastDocId = doc.id;

        const data = doc.data();

        // Skip condition: Check if already migrated
        if (shouldSkip(data)) {
          result.skipped++;
          logger.debug({ docId: doc.id }, "Skipping already migrated document");
          continue;
        }

        try {
          const updates = computeUpdates(data);

          if (!dryRun) {
            batch.update(doc.ref, {
              ...updates,
              updatedAt: FieldValue.serverTimestamp()
            });
            batchCount++;
          }

          result.updated++;
          logger.debug({ docId: doc.id, updates }, "Document will be updated");
        } catch (error) {
          result.errors++;
          logger.error({ docId: doc.id, error }, "Error processing document");
        }
      }

      // Commit batch
      if (!dryRun && batchCount > 0) {
        await batch.commit();
        logger.info(
          { batchCount, totalProcessed: result.processed },
          "Batch committed"
        );
      }

      // Prepare next batch
      const lastDoc = snapshot.docs[snapshot.docs.length - 1];
      query = db
        .collection(COLLECTION_NAME)
        .orderBy("__name__")
        .startAfter(lastDoc)
        .limit(BATCH_SIZE);
    }

    logger.info(result, "Migration completed");
    return result;
  } catch (error) {
    logger.error({ error, result }, "Migration failed");
    throw error;
  }
}

/**
 * Determine if a document should be skipped (already migrated)
 */
function shouldSkip(data: FirebaseFirestore.DocumentData): boolean {
  // TODO: Implement skip logic based on migration requirements
  // Example: return data.newField !== undefined;
  return false;
}

/**
 * Compute the updates to apply to a document
 */
function computeUpdates(
  data: FirebaseFirestore.DocumentData
): Record<string, unknown> {
  // TODO: Implement update logic based on migration requirements
  // Example:
  // return {
  //   newField: computeNewFieldValue(data),
  //   oldField: FieldValue.delete()
  // };
  return {};
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const dryRun = !args.includes("--apply");
  const startAfter = args.find(a => a.startsWith("--start-after="))?.split("=")[1];
  const limit = args.find(a => a.startsWith("--limit="))?.split("=")[1];

  console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    FIRESTORE MIGRATION                        ║
╠══════════════════════════════════════════════════════════════╣
║  Mode: ${dryRun ? "DRY RUN (no changes will be made)" : "APPLY (changes will be committed)"}
║  Collection: ${COLLECTION_NAME}
${startAfter ? `║  Starting after: ${startAfter}\n` : ""}${limit ? `║  Limit: ${limit}\n` : ""}╚══════════════════════════════════════════════════════════════╝
  `);

  migrate({
    dryRun,
    startAfter,
    limit: limit ? parseInt(limit, 10) : undefined
  })
    .then((result) => {
      console.log("\n📊 Migration Results:");
      console.log(`   Processed: ${result.processed}`);
      console.log(`   Updated: ${result.updated}`);
      console.log(`   Skipped: ${result.skipped}`);
      console.log(`   Errors: ${result.errors}`);
      if (result.lastDocId) {
        console.log(`   Last Doc ID: ${result.lastDocId}`);
      }
      if (result.dryRun) {
        console.log("\n⚠️  This was a DRY RUN. Use --apply to commit changes.");
      }
      process.exit(result.errors > 0 ? 1 : 0);
    })
    .catch((error) => {
      console.error("\n❌ Migration failed:", error);
      process.exit(1);
    });
}
```

### 4. Usage Instructions

Include these in the migration file:

```markdown
## How to Run

1. **Preview changes (dry run):**
   ```bash
   npx ts-node scripts/migrations/YYYY-MM-DD-description.ts
   ```

2. **Apply changes:**
   ```bash
   npx ts-node scripts/migrations/YYYY-MM-DD-description.ts --apply
   ```

3. **Resume from specific document:**
   ```bash
   npx ts-node scripts/migrations/YYYY-MM-DD-description.ts --apply --start-after=docId123
   ```

4. **Test with limited documents:**
   ```bash
   npx ts-node scripts/migrations/YYYY-MM-DD-description.ts --limit=10
   ```
```

### 5. Update Type Definitions

After migration, update relevant type files:

```typescript
// Before
export type ResourceBase = {
  name: string;
};

// After
export type ResourceBase = {
  name: string;
  newField: string; // Added in migration YYYY-MM-DD
};
```

## Common Migration Patterns

### Adding a New Field

```typescript
function shouldSkip(data: FirebaseFirestore.DocumentData): boolean {
  return data.newField !== undefined;
}

function computeUpdates(data: FirebaseFirestore.DocumentData) {
  return {
    newField: "defaultValue" // or computed from existing data
  };
}
```

### Renaming a Field

```typescript
function shouldSkip(data: FirebaseFirestore.DocumentData): boolean {
  return data.newFieldName !== undefined && data.oldFieldName === undefined;
}

function computeUpdates(data: FirebaseFirestore.DocumentData) {
  return {
    newFieldName: data.oldFieldName,
    oldFieldName: FieldValue.delete()
  };
}
```

### Restructuring Nested Data

```typescript
function computeUpdates(data: FirebaseFirestore.DocumentData) {
  // Flatten nested structure
  return {
    "settings.theme": data.preferences?.theme ?? "light",
    "settings.language": data.preferences?.language ?? "pl",
    preferences: FieldValue.delete()
  };
}
```

### Converting Data Types

```typescript
function computeUpdates(data: FirebaseFirestore.DocumentData) {
  // Convert string array to object map
  const tagsMap = (data.tags as string[])?.reduce(
    (acc, tag) => ({ ...acc, [tag]: true }),
    {}
  ) ?? {};

  return {
    tagsMap,
    tags: FieldValue.delete()
  };
}
```

## Safety Checklist

Before running migration with `--apply`:

- [ ] Dry run completed successfully
- [ ] Sample of changes reviewed manually
- [ ] Database backup created (or point-in-time recovery enabled)
- [ ] Type definitions ready to update
- [ ] Rollback script prepared (for high-risk migrations)
- [ ] Team notified of migration window
- [ ] Monitoring in place for errors

## Rollback Considerations

For reversible migrations, include a rollback function:

```typescript
export async function rollback(options: MigrationOptions = {}) {
  // Reverse the migration logic
  function computeRollbackUpdates(data: FirebaseFirestore.DocumentData) {
    return {
      oldFieldName: data.newFieldName,
      newFieldName: FieldValue.delete()
    };
  }
  // ... rest of migration logic with rollback updates
}
```

## Questions to Ask

When unclear about the migration:

- What is the current structure of affected documents?
- How many documents need to be migrated?
- Is there a deadline or maintenance window?
- What happens to the application during migration?
- Do we need dual-write support during transition?
- What's the rollback strategy if something goes wrong?
