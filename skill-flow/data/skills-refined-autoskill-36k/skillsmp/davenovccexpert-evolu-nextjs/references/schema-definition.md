# Schema Definition

Define schemas using branded types for compile-time type safety and runtime validation.

## Complete Example

```typescript
import {
  id,
  InferType,
  maxLength,
  NonEmptyString,
  nullOr,
  SqliteBoolean,
} from "@evolu/common";

// 1. Create branded ID types for each table
const TodoId = id("Todo");
type TodoId = InferType<typeof TodoId>;

const CategoryId = id("Category");
type CategoryId = InferType<typeof CategoryId>;

// 2. Create constrained string types
const NonEmptyString100 = maxLength(100, NonEmptyString);
type NonEmptyString100 = InferType<typeof NonEmptyString100>;

const NonEmptyString50 = maxLength(50, NonEmptyString);
type NonEmptyString50 = InferType<typeof NonEmptyString50>;

// 3. Define the schema
const Schema = {
  todo: {
    id: TodoId,
    title: NonEmptyString100,
    isCompleted: nullOr(SqliteBoolean),
    categoryId: nullOr(CategoryId),
  },
  category: {
    id: CategoryId,
    name: NonEmptyString50,
  },
};
```

## Key Rules

| Pattern | Purpose |
|---------|---------|
| `id("TableName")` | Branded ID types - prevents mixing IDs across tables |
| `NonEmptyString` + `maxLength()` | Validated strings with length constraints |
| `nullOr()` | Optional fields - Evolu uses SQLite which prefers null over undefined |
| `SqliteBoolean` | Boolean fields (stored as 0/1 in SQLite) |

## Automatic System Columns

Every row automatically includes:

| Column | Type | Description |
|--------|------|-------------|
| `createdAt` | timestamp | When row was created |
| `updatedAt` | timestamp | When row was last modified |
| `isDeleted` | SqliteBoolean | Soft delete flag |
| `ownerId` | string | ID of the data owner |
