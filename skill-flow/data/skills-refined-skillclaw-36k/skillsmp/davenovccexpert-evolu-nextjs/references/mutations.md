# CRUD Mutations

Use the `useEvolu` hook to access mutation functions.

## Create

```typescript
"use client";

import { useEvolu, NonEmptyString100 } from "@/lib/evolu";

function TodoForm() {
  const { create } = useEvolu();

  const handleCreate = (title: string) => {
    // Validate and parse the title
    const parsedTitle = NonEmptyString100.from(title);
    if (!parsedTitle.ok) {
      // Handle validation error
      console.error(parsedTitle.error);
      return;
    }

    // Create new row - ID is auto-generated
    create("todo", {
      title: parsedTitle.value,
      isCompleted: evolu.sqliteFalse,
    });
  };

  return <form>{/* form implementation */}</form>;
}
```

## Update

```typescript
function TodoItem({ todo }: { todo: { id: TodoId; title: string; isCompleted: boolean | null } }) {
  const { update } = useEvolu();

  // Toggle completion
  const toggleComplete = () => {
    update("todo", {
      id: todo.id,
      isCompleted: todo.isCompleted ? evolu.sqliteFalse : evolu.sqliteTrue,
    });
  };

  // Update title
  const rename = (newTitle: string) => {
    const parsed = NonEmptyString100.from(newTitle);
    if (!parsed.ok) return;

    update("todo", {
      id: todo.id,
      title: parsed.value,
    });
  };

  return <div>{/* component implementation */}</div>;
}
```

## Delete (Soft Delete)

```typescript
// Soft delete - set isDeleted flag
const deleteTodo = () => {
  update("todo", {
    id: todo.id,
    isDeleted: evolu.sqliteTrue,
  });
};
```

## Batch Updates

```typescript
function clearCompleted() {
  const { rows } = useQuery(completedTodosQuery);
  const { update } = useEvolu();

  rows.forEach((todo) => {
    update("todo", { id: todo.id, isDeleted: evolu.sqliteTrue });
  });
}
```

## Mutation Rules

| Operation | Method | Notes |
|-----------|--------|-------|
| Create | `create(tableName, data)` | ID is auto-generated, returns the ID |
| Update | `update(tableName, { id, ...changes })` | ID is **required** |
| Delete | `update(tableName, { id, isDeleted: evolu.sqliteTrue })` | Use soft delete |

## Important

- **Always validate** data using branded type `.from()` method before mutations
- Soft deletes enable sync across devices and time travel (undo)
- Never use hard deletes - Evolu doesn't support them by design
