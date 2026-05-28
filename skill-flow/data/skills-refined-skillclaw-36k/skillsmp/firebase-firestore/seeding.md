# Firebase Seeding Patterns

Patterns for seeding Firestore with predefined data.

## Architecture Overview

```
lib/
└── firebase/
    ├── seeder.ts          # Generic seeding utilities
    └── auto-seed.ts       # Auto-seeding orchestrator

features/
└── [feature]/
    ├── data/
    │   └── predefined-[resource].ts  # Predefined data
    └── server/
        └── db/
            └── seed-[resource].ts    # Feature-specific seeder
```

## Core Seeding Types

```typescript
// lib/firebase/seeder.ts

import { FieldValue } from "firebase-admin/firestore";

/**
 * Item with predefined ID for seeding
 */
export type SeedItem<T> = {
  id: string;
} & T;

/**
 * Configuration for seeding a collection
 */
export type SeedCollectionConfig<T> = {
  /** Firestore collection name */
  collectionName: string;
  /** Data to seed (must include id) */
  data: SeedItem<T>[];
  /** Force update existing documents */
  forceUpdate?: boolean;
  /** Custom transform before writing */
  transformItem?: (item: SeedItem<T>) => Record<string, unknown>;
};

/**
 * Result of seeding operation
 */
export type SeedStats = {
  created: number;
  updated: number;
  skipped: number;
  errors: number;
  total: number;
};
```

## Generic Seeding Utilities

```typescript
// lib/firebase/seeder.ts
import "server-only";

import { FieldValue } from "firebase-admin/firestore";

import { db } from "~/lib/firebase";
import { createLogger } from "~/lib/logger";

const logger = createLogger({ module: "seeder" });

/**
 * Check if a collection needs seeding
 */
export async function shouldSeedCollection(
  collectionName: string
): Promise<boolean> {
  try {
    const snapshot = await db.collection(collectionName).limit(1).get();
    return snapshot.empty;
  } catch (error) {
    logger.error({ collectionName, error }, "Failed to check collection");
    return false;
  }
}

/**
 * Seed a collection with predefined data
 * Creates missing documents, optionally updates existing ones
 */
export async function seedCollection<T extends Record<string, unknown>>(
  config: SeedCollectionConfig<T>
): Promise<SeedStats> {
  const {
    collectionName,
    data,
    forceUpdate = false,
    transformItem,
  } = config;

  const stats: SeedStats = {
    created: 0,
    updated: 0,
    skipped: 0,
    errors: 0,
    total: data.length,
  };

  logger.info(
    { collectionName, count: data.length, forceUpdate },
    "Starting seed"
  );

  for (const item of data) {
    try {
      const { id, ...fields } = item;
      const docRef = db.collection(collectionName).doc(id);
      const doc = await docRef.get();

      // Transform item if function provided
      const dataToWrite = transformItem
        ? transformItem(item)
        : {
            ...fields,
            isPredefined: true,
            createdAt: FieldValue.serverTimestamp(),
            updatedAt: FieldValue.serverTimestamp(),
          };

      if (!doc.exists) {
        // Create new document
        await docRef.set(dataToWrite);
        stats.created++;
        logger.debug({ collectionName, id }, "Document created");
      } else if (forceUpdate) {
        // Update existing document
        await docRef.update({
          ...fields,
          isPredefined: true,
          updatedAt: FieldValue.serverTimestamp(),
        });
        stats.updated++;
        logger.debug({ collectionName, id }, "Document updated");
      } else {
        // Skip existing
        stats.skipped++;
        logger.debug({ collectionName, id }, "Document skipped");
      }
    } catch (error) {
      stats.errors++;
      logger.error(
        { collectionName, itemId: item.id, error },
        "Failed to seed item"
      );
    }
  }

  logger.info(
    {
      collectionName,
      created: stats.created,
      updated: stats.updated,
      skipped: stats.skipped,
      errors: stats.errors,
    },
    "Seed completed"
  );

  return stats;
}

/**
 * Seed multiple collections
 */
export async function seedDatabase(
  collections: Array<SeedCollectionConfig<Record<string, unknown>>>
): Promise<Record<string, SeedStats>> {
  const results: Record<string, SeedStats> = {};

  for (const config of collections) {
    results[config.collectionName] = await seedCollection(config);
  }

  return results;
}
```

## Predefined Data Definition

```typescript
// features/budget/data/predefined-budget-templates.ts

import type { BudgetTemplateBase } from "../types/budget-template";
import type { SeedItem } from "~/lib/firebase/seeder";

export type PredefinedBudgetTemplate = SeedItem<BudgetTemplateBase>;

export const PREDEFINED_BUDGET_TEMPLATES: PredefinedBudgetTemplate[] = [
  {
    id: "young_professional",
    name: "Young Professional",
    description: "Ideal for early career individuals with stable income",
    isRecommended: true,
    allocations: {
      needs: 50,
      wants: 30,
      savings: 20,
    },
    categories: [
      {
        name: "Housing",
        percentage: 30,
        icon: "home",
        color: "#4F46E5",
        type: "needs",
      },
      {
        name: "Transportation",
        percentage: 10,
        icon: "car",
        color: "#059669",
        type: "needs",
      },
      // ... more categories
    ],
  },
  {
    id: "family",
    name: "Family Budget",
    description: "Balanced budget for families with children",
    isRecommended: false,
    allocations: {
      needs: 60,
      wants: 20,
      savings: 20,
    },
    categories: [
      // ... categories
    ],
  },
  {
    id: "aggressive_saver",
    name: "Aggressive Saver",
    description: "For those pursuing FIRE or rapid wealth building",
    isRecommended: false,
    allocations: {
      needs: 40,
      wants: 10,
      savings: 50,
    },
    categories: [
      // ... categories
    ],
  },
  {
    id: "student",
    name: "Student Budget",
    description: "Optimized for students with limited income",
    isRecommended: false,
    allocations: {
      needs: 60,
      wants: 25,
      savings: 15,
    },
    categories: [
      // ... categories
    ],
  },
  {
    id: "custom",
    name: "Custom Template",
    description: "Start from scratch with full customization",
    isRecommended: false,
    allocations: {
      needs: 0,
      wants: 0,
      savings: 0,
    },
    categories: [],
  },
];
```

## Feature-Specific Seeder

```typescript
// features/budget/server/db/seed-budget-templates.ts
import "server-only";

import { seedCollection, shouldSeedCollection } from "~/lib/firebase/seeder";
import { createLogger } from "~/lib/logger";

import {
  PREDEFINED_BUDGET_TEMPLATES,
  type PredefinedBudgetTemplate,
} from "../../data/predefined-budget-templates";

const COLLECTION = "budget_templates";
const logger = createLogger({ module: "seed-budget-templates" });

/**
 * Seed budget templates collection
 */
export async function seedBudgetTemplates(
  options: { force?: boolean } = {}
): Promise<{ stats: SeedStats; seeded: boolean }> {
  const { force = false } = options;

  // Check if seeding is needed
  if (!force) {
    const needsSeeding = await shouldSeedCollection(COLLECTION);
    if (!needsSeeding) {
      logger.info("Budget templates already exist, skipping seed");
      return {
        seeded: false,
        stats: {
          created: 0,
          updated: 0,
          skipped: PREDEFINED_BUDGET_TEMPLATES.length,
          errors: 0,
          total: PREDEFINED_BUDGET_TEMPLATES.length,
        },
      };
    }
  }

  logger.info({ force }, "Seeding budget templates");

  const stats = await seedCollection<PredefinedBudgetTemplate>({
    collectionName: COLLECTION,
    data: PREDEFINED_BUDGET_TEMPLATES,
    forceUpdate: force,
  });

  return { stats, seeded: stats.created > 0 || stats.updated > 0 };
}
```

## Auto-Seeding on Application Start

```typescript
// lib/firebase/auto-seed.ts
import "server-only";

import { createLogger } from "~/lib/logger";

import { seedBudgetTemplates } from "~/features/budget/server/db/seed-budget-templates";
// Import other seeders as needed

const logger = createLogger({ module: "auto-seed" });

let hasSeeded = false;

/**
 * Auto-seed database on application startup
 * Only runs once per application lifecycle
 */
export async function autoSeedDatabase(): Promise<void> {
  // Prevent multiple seedings
  if (hasSeeded) {
    return;
  }

  hasSeeded = true;

  try {
    logger.info("Starting auto-seed");

    // Run all seeders
    const results = await Promise.allSettled([
      seedBudgetTemplates(),
      // Add more seeders here:
      // seedCategories(),
      // seedCurrencies(),
    ]);

    // Log results
    results.forEach((result, index) => {
      if (result.status === "fulfilled") {
        logger.info({ result: result.value }, `Seeder ${index} completed`);
      } else {
        logger.error({ error: result.reason }, `Seeder ${index} failed`);
      }
    });

    logger.info("Auto-seed completed");
  } catch (error) {
    logger.error({ error }, "Auto-seed failed");
    // Don't throw - allow app to continue even if seeding fails
  }
}
```

## Integration with Application

### In Root Layout

```typescript
// app/layout.tsx
import { autoSeedDatabase } from "~/lib/firebase/auto-seed";

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Auto-seed on first request
  await autoSeedDatabase();

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Manual Seeding API

```typescript
// app/api/seed/route.ts
import { NextResponse } from "next/server";

import { seedBudgetTemplates } from "~/features/budget/server/db/seed-budget-templates";
// Import other seeders

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const force = searchParams.get("force") === "true";

  try {
    const results = await Promise.all([
      seedBudgetTemplates({ force }),
      // Add more seeders
    ]);

    return NextResponse.json({
      success: true,
      results: {
        budgetTemplates: results[0],
        // Map more results
      },
    });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: String(error) },
      { status: 500 }
    );
  }
}
```

Usage:
- `GET /api/seed` - Seed missing data only
- `GET /api/seed?force=true` - Force re-seed all data

## Best Practices

### 1. Use Stable IDs

```typescript
// ✅ Good - Stable, meaningful IDs
const data = [
  { id: "young_professional", name: "Young Professional" },
  { id: "family", name: "Family Budget" },
];

// ❌ Bad - Random IDs
const data = [
  { id: crypto.randomUUID(), name: "Young Professional" }, // Different each time
];
```

### 2. Mark Predefined Data

```typescript
// ✅ Good - Flag predefined items
const dataToWrite = {
  ...fields,
  isPredefined: true, // Helps distinguish from user-created
  createdAt: FieldValue.serverTimestamp(),
  updatedAt: FieldValue.serverTimestamp(),
};
```

### 3. Preserve User Modifications

```typescript
// ✅ Good - Default to not overwriting
export async function seedCollection(config) {
  const { forceUpdate = false } = config; // Default: don't overwrite

  if (doc.exists && !forceUpdate) {
    // User may have modified this document
    stats.skipped++;
    return;
  }
}
```

### 4. Handle Errors Gracefully

```typescript
// ✅ Good - Continue on individual failures
for (const item of data) {
  try {
    await docRef.set(dataToWrite);
    stats.created++;
  } catch (error) {
    stats.errors++; // Count error
    logger.error({ itemId: item.id, error }, "Failed");
    // Continue to next item
  }
}
```

### 5. Log All Operations

```typescript
// ✅ Good - Comprehensive logging
logger.info({ collectionName, count: data.length }, "Starting seed");
logger.debug({ collectionName, id }, "Document created");
logger.info({ created, updated, skipped, errors }, "Seed completed");
```

### 6. Don't Block Application Start

```typescript
// ✅ Good - Catch errors, don't throw
export async function autoSeedDatabase() {
  try {
    await seedBudgetTemplates();
  } catch (error) {
    logger.error({ error }, "Seed failed");
    // Don't throw - app should still work
  }
}
```

### 7. Support Force Re-seeding

```typescript
// ✅ Good - Allow force update for data migrations
export async function seedBudgetTemplates(options: { force?: boolean } = {}) {
  const { force = false } = options;

  // force=true will update existing documents
  const stats = await seedCollection({
    collectionName: COLLECTION,
    data: PREDEFINED_DATA,
    forceUpdate: force,
  });
}
```

## Migration Pattern

When predefined data changes, use force re-seed:

```typescript
// 1. Update predefined data
export const PREDEFINED_TEMPLATES = [
  {
    id: "young_professional",
    name: "Young Professional (Updated)", // Changed
    // ... new fields
  },
];

// 2. Force re-seed via API
// GET /api/seed?force=true

// 3. Or programmatically
await seedBudgetTemplates({ force: true });
```

## Testing Seeders

```typescript
// tests/unit/seeders/seed-budget-templates.test.ts
import { describe, it, expect, beforeEach, vi } from "vitest";

import { seedBudgetTemplates } from "~/features/budget/server/db/seed-budget-templates";
import { PREDEFINED_BUDGET_TEMPLATES } from "~/features/budget/data/predefined-budget-templates";

describe("seedBudgetTemplates", () => {
  it("should create all predefined templates", async () => {
    const result = await seedBudgetTemplates();

    expect(result.stats.created).toBe(PREDEFINED_BUDGET_TEMPLATES.length);
    expect(result.stats.errors).toBe(0);
    expect(result.seeded).toBe(true);
  });

  it("should skip existing templates without force", async () => {
    // First seed
    await seedBudgetTemplates();

    // Second seed without force
    const result = await seedBudgetTemplates();

    expect(result.stats.skipped).toBe(PREDEFINED_BUDGET_TEMPLATES.length);
    expect(result.seeded).toBe(false);
  });

  it("should update existing templates with force", async () => {
    // First seed
    await seedBudgetTemplates();

    // Force re-seed
    const result = await seedBudgetTemplates({ force: true });

    expect(result.stats.updated).toBe(PREDEFINED_BUDGET_TEMPLATES.length);
    expect(result.seeded).toBe(true);
  });
});
```
