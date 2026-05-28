# Queries with useQuery

Use `useQuery` for real-time reactive data access in React components. Queries automatically update when data changes.

## Basic Query Pattern

```typescript
"use client";

import { useQuery } from "@evolu/react";
import { evolu } from "@/lib/evolu";

// 1. Define queries outside components using Kysely query builder
const todosQuery = evolu.createQuery((db) =>
  db
    .selectFrom("todo")
    .select(["id", "title", "isCompleted", "createdAt"])
    .where("isDeleted", "is not", evolu.sqliteTrue)
    .where("title", "is not", null)
    .orderBy("createdAt", "desc")
);

// 2. Use queries in components
function TodoList() {
  const { rows } = useQuery(todosQuery);

  return (
    <ul>
      {rows.map((todo) => (
        <li key={todo.id}>
          {todo.title} - {todo.isCompleted ? "Done" : "Pending"}
        </li>
      ))}
    </ul>
  );
}
```

## Single Item Query

```typescript
// Query for a specific item
const todoByIdQuery = (id: TodoId) =>
  evolu.createQuery((db) =>
    db
      .selectFrom("todo")
      .select(["id", "title", "isCompleted"])
      .where("id", "=", id)
  );

function TodoDetail({ id }: { id: TodoId }) {
  const { row } = useQuery(todoByIdQuery(id));

  if (!row) return <div>Not found</div>;
  return <div>{row.title}</div>;
}
```

## Key Patterns

| Pattern | Description |
|---------|-------------|
| `{ rows }` | Use for lists of items |
| `{ row }` | Use for single items |
| `.where("isDeleted", "is not", evolu.sqliteTrue)` | **Always** filter soft-deleted rows |
| `.where("title", "is not", null)` | Filter null values when using NonEmptyString |

## Avoiding Suspense Waterfall

Use `useQueries` to load multiple queries in parallel:

```typescript
import { useQueries } from "@evolu/react";

function Dashboard() {
  const [todos, categories] = useQueries([todosQuery, categoriesQuery]);

  // Both queries load in parallel
  return (
    <div>
      <TodoList rows={todos.rows} />
      <CategoryList rows={categories.rows} />
    </div>
  );
}
```

## Queries with Relationships

```typescript
const todosWithCategoryQuery = evolu.createQuery((db) =>
  db
    .selectFrom("todo")
    .leftJoin("category", "todo.categoryId", "category.id")
    .select([
      "todo.id",
      "todo.title",
      "todo.isCompleted",
      "category.name as categoryName",
    ])
    .where("todo.isDeleted", "is not", evolu.sqliteTrue)
    .orderBy("todo.createdAt", "desc")
);
```

## Conditional Queries

```typescript
const todosByStatusQuery = (completed: boolean) =>
  evolu.createQuery((db) =>
    db
      .selectFrom("todo")
      .selectAll()
      .where("isDeleted", "is not", evolu.sqliteTrue)
      .where(
        "isCompleted",
        completed ? "is" : "is not",
        evolu.sqliteTrue
      )
  );
```
