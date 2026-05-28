# Firebase Type Utilities

Complete type definitions for managing the Firestore data lifecycle.

## Type Lifecycle Overview

Firebase/Firestore requires different type representations at different stages:

```
┌─────────────────┐
│   Base Type     │  Business fields only (no id, no timestamps)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Firestore│ │  App   │  Firestore: Timestamp | App: Date + id
└────────┘ └────────┘
    │
    ├──────────┐
    ▼          ▼
┌────────┐ ┌────────┐
│CreateDto│ │UpdateDto│  DTOs for mutations
└────────┘ └────────┘
```

## Core Type Utilities

### Type Definitions

```typescript
// lib/firebase/types.ts
import type { FieldValue, Timestamp } from "firebase-admin/firestore";

/**
 * Standard timestamp fields added to all Firestore documents
 */
export type TimestampFields = {
  createdAt: Timestamp;
  updatedAt: Timestamp;
};

/**
 * Converts Date fields to Timestamp for Firestore storage
 * Adds createdAt and updatedAt as Timestamp
 */
export type WithFirestoreTimestamps<T> = {
  [K in keyof T]: T[K] extends Date
    ? Timestamp
    : T[K] extends Date | undefined
      ? Timestamp | undefined
      : T[K];
} & TimestampFields;

/**
 * Application type with id and Date objects
 * Converts Timestamp fields back to Date
 */
export type WithDates<T> = {
  id: string;
} & {
  [K in keyof T]: T[K] extends Date
    ? Date
    : T[K] extends Date | undefined
      ? Date | undefined
      : T[K];
} & {
  createdAt: Date;
  updatedAt: Date;
};

/**
 * DTO for creating new documents
 * All Date fields become FieldValue for server timestamps
 */
export type CreateDto<T> = {
  [K in keyof T]: T[K] extends Date
    ? FieldValue
    : T[K] extends Date | undefined
      ? FieldValue | undefined
      : T[K];
} & {
  createdAt: FieldValue;
  updatedAt: FieldValue;
};

/**
 * DTO for updating documents
 * All fields optional, Date fields become FieldValue
 * No createdAt (never update creation time)
 */
export type UpdateDto<T> = Partial<{
  [K in keyof T]: T[K] extends Date
    ? FieldValue | Timestamp
    : T[K] extends Date | undefined
      ? FieldValue | Timestamp | undefined
      : T[K];
}> & {
  updatedAt?: FieldValue;
};
```

## Usage Examples

### Basic Type (No Custom Dates)

```typescript
// features/budget/types/budget.ts
import type {
  WithFirestoreTimestamps,
  WithDates,
  CreateDto,
  UpdateDto,
} from "~/lib/firebase/types";

// 1. Base type - business fields only
export type BudgetBase = {
  userId: string;
  name: string;
  amount: number;
  currency: string;
  status: "active" | "archived";
};

// 2. Firestore type - raw data with Timestamp
export type BudgetFirestore = WithFirestoreTimestamps<BudgetBase>;
// Result: {
//   userId: string;
//   name: string;
//   amount: number;
//   currency: string;
//   status: "active" | "archived";
//   createdAt: Timestamp;
//   updatedAt: Timestamp;
// }

// 3. Application type - with id and Date
export type Budget = WithDates<BudgetBase>;
// Result: {
//   id: string;
//   userId: string;
//   name: string;
//   amount: number;
//   currency: string;
//   status: "active" | "archived";
//   createdAt: Date;
//   updatedAt: Date;
// }

// 4. Create DTO
export type CreateBudgetDto = CreateDto<BudgetBase>;
// Result: {
//   userId: string;
//   name: string;
//   amount: number;
//   currency: string;
//   status: "active" | "archived";
//   createdAt: FieldValue;
//   updatedAt: FieldValue;
// }

// 5. Update DTO
export type UpdateBudgetDto = UpdateDto<BudgetBase>;
// Result: Partial<{
//   userId: string;
//   name: string;
//   amount: number;
//   currency: string;
//   status: "active" | "archived";
//   updatedAt?: FieldValue;
// }>
```

### Type with Custom Date Fields

```typescript
// features/event/types/event.ts
import type {
  WithFirestoreTimestamps,
  WithDates,
  CreateDto,
  UpdateDto,
} from "~/lib/firebase/types";

// 1. Base type with custom date fields
export type EventBase = {
  title: string;
  description: string;
  scheduledAt: Date; // Custom date field
  expiresAt?: Date; // Optional custom date field
  status: "scheduled" | "completed" | "cancelled";
};

// 2. Firestore type - all Date fields become Timestamp
export type EventFirestore = WithFirestoreTimestamps<EventBase>;
// Result: {
//   title: string;
//   description: string;
//   scheduledAt: Timestamp;        // Converted
//   expiresAt?: Timestamp;         // Converted
//   createdAt: Timestamp;
//   updatedAt: Timestamp;
// }

// 3. Application type - preserves Date fields
export type Event = WithDates<EventBase>;
// Result: {
//   id: string;
//   title: string;
//   description: string;
//   scheduledAt: Date;
//   expiresAt?: Date;
//   createdAt: Date;
//   updatedAt: Date;
// }

// 4. Create DTO - Date fields become FieldValue
export type CreateEventDto = CreateDto<EventBase>;
// Result: {
//   title: string;
//   description: string;
//   scheduledAt: FieldValue;       // For server timestamp
//   expiresAt?: FieldValue;
//   createdAt: FieldValue;
//   updatedAt: FieldValue;
// }

// 5. Update DTO
export type UpdateEventDto = UpdateDto<EventBase>;
// Result: Partial<{
//   title?: string;
//   description?: string;
//   scheduledAt?: FieldValue | Timestamp;  // Can use specific date
//   expiresAt?: FieldValue | Timestamp;
//   updatedAt?: FieldValue;
// }>
```

### Type with Nested Objects

```typescript
// features/onboarding/types/onboarding.ts

// Nested types (no special handling needed)
export type OnboardingPreferences = {
  currency: string;
  locale: string;
  notifications: boolean;
};

export type OnboardingBudget = {
  templateId: string;
  monthlyIncome: number;
};

// Base type with nested objects
export type OnboardingBase = {
  userId: string;
  completed: boolean;
  currentStep: string;
  preferences?: OnboardingPreferences;
  budget?: OnboardingBudget;
};

// Generated types work the same way
export type OnboardingFirestore = WithFirestoreTimestamps<OnboardingBase>;
export type Onboarding = WithDates<OnboardingBase>;
export type CreateOnboardingDto = CreateDto<OnboardingBase>;
export type UpdateOnboardingDto = UpdateDto<OnboardingBase>;
```

### Type with Arrays

```typescript
// features/category/types/category.ts

export type CategoryItem = {
  id: string;
  name: string;
  icon: string;
  color: string;
};

export type CategoryBase = {
  userId: string;
  name: string;
  items: CategoryItem[]; // Array of objects
  tags: string[]; // Array of primitives
};

// Arrays are preserved as-is in all type variants
export type CategoryFirestore = WithFirestoreTimestamps<CategoryBase>;
export type Category = WithDates<CategoryBase>;
export type CreateCategoryDto = CreateDto<CategoryBase>;
export type UpdateCategoryDto = UpdateDto<CategoryBase>;
```

## Transform Functions

### Basic Transform

```typescript
// features/budget/server/db/budget-queries.ts

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
```

### Transform with Custom Dates

```typescript
// features/event/server/db/event-queries.ts

function transformToEvent(
  docId: string,
  data: FirebaseFirestore.DocumentData
): Event {
  return {
    id: docId,
    ...data,
    // Custom date fields
    scheduledAt: data.scheduledAt?.toDate(),
    expiresAt: data.expiresAt?.toDate(),
    // Standard timestamp fields
    createdAt: data.createdAt?.toDate(),
    updatedAt: data.updatedAt?.toDate(),
  } as Event;
}
```

### Generic Transform Helper

```typescript
// lib/firebase/utils.ts

/**
 * Converts Firestore Timestamp fields to Date objects
 */
export function timestampToDate(
  timestamp: FirebaseFirestore.Timestamp | undefined
): Date | undefined {
  return timestamp?.toDate();
}

/**
 * Creates a transform function for a given type
 */
export function createTransform<T>(
  dateFields: string[] = []
): (docId: string, data: FirebaseFirestore.DocumentData) => T {
  return (docId: string, data: FirebaseFirestore.DocumentData): T => {
    const result: Record<string, unknown> = {
      id: docId,
      ...data,
      createdAt: data.createdAt?.toDate(),
      updatedAt: data.updatedAt?.toDate(),
    };

    // Convert additional date fields
    for (const field of dateFields) {
      if (data[field]) {
        result[field] = data[field]?.toDate();
      }
    }

    return result as T;
  };
}

// Usage
const transformToEvent = createTransform<Event>(["scheduledAt", "expiresAt"]);
```

## Creating Documents

### Using FieldValue.serverTimestamp()

```typescript
import { FieldValue } from "firebase-admin/firestore";

// For new documents - use server timestamp
const createData: CreateBudgetDto = {
  userId: "user-123",
  name: "Monthly Budget",
  amount: 5000,
  currency: "PLN",
  status: "active",
  createdAt: FieldValue.serverTimestamp(),
  updatedAt: FieldValue.serverTimestamp(),
};

await db.collection("budgets").add(createData);
```

### Using Specific Dates

```typescript
import { Timestamp } from "firebase-admin/firestore";

// For custom date fields - convert Date to Timestamp
const createData: CreateEventDto = {
  title: "Team Meeting",
  description: "Weekly sync",
  scheduledAt: Timestamp.fromDate(new Date("2024-03-15T10:00:00")),
  expiresAt: Timestamp.fromDate(new Date("2024-03-15T12:00:00")),
  status: "scheduled",
  createdAt: FieldValue.serverTimestamp(),
  updatedAt: FieldValue.serverTimestamp(),
};
```

## Updating Documents

### Partial Update

```typescript
import { FieldValue } from "firebase-admin/firestore";

const updateData: UpdateBudgetDto = {
  name: "Updated Budget Name",
  status: "archived",
  updatedAt: FieldValue.serverTimestamp(),
};

await db.collection("budgets").doc(budgetId).update(updateData);
```

### Updating Date Fields

```typescript
import { Timestamp, FieldValue } from "firebase-admin/firestore";

const updateData: UpdateEventDto = {
  scheduledAt: Timestamp.fromDate(new Date("2024-03-20T14:00:00")),
  updatedAt: FieldValue.serverTimestamp(),
};

await db.collection("events").doc(eventId).update(updateData);
```

## Type Guards

```typescript
// lib/firebase/guards.ts

import type { Timestamp } from "firebase-admin/firestore";

export function isTimestamp(value: unknown): value is Timestamp {
  return (
    value !== null &&
    typeof value === "object" &&
    "toDate" in value &&
    typeof (value as Timestamp).toDate === "function"
  );
}

export function isDate(value: unknown): value is Date {
  return value instanceof Date && !isNaN(value.getTime());
}
```

## Best Practices

1. **Always define Base type first** - Contains only business logic fields
2. **Use type utilities consistently** - Don't manually add timestamp fields
3. **Create transform functions per resource** - Keep them close to query files
4. **Handle optional dates explicitly** - Check for undefined before calling toDate()
5. **Use FieldValue.serverTimestamp()** - For consistent server-side timestamps
6. **Document custom date fields** - In type definitions and README
