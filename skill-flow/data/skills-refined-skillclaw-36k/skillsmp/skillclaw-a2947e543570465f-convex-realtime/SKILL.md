---
name: convex-realtime
description: Use this skill when building reactive applications with Convex, leveraging real-time subscriptions, optimistic updates, intelligent caching, and cursor-based pagination.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Client Documentation](https://docs.convex.dev/client/react)
- Optimistic Updates: [Optimistic Updates Documentation](https://docs.convex.dev/client/react/optimistic-updates)
- Pagination: [Pagination Documentation](https://docs.convex.dev/database/pagination)
- For broader context: [LLMs Documentation](https://docs.convex.dev/llms.txt)

## Instructions

### How Convex Realtime Works

1. **Automatic Subscriptions** - `useQuery` creates a subscription that updates automatically.
2. **Smart Caching** - Query results are cached and shared across components.
3. **Consistency** - All subscriptions see a consistent view of the database.
4. **Efficient Updates** - Only re-renders when relevant data changes.

### Basic Subscriptions

```typescript
// React component with real-time data
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskList({ userId }: { userId: Id<"users"> }) {
  // Automatically subscribes and updates in real-time
  const tasks = useQuery(api.tasks.list, { userId });

  if (tasks === undefined) {
    return <div>Loading...</div>;
  }

  return (
    <ul>
      {tasks.map((task) => (
        <li key={task._id}>{task.title}</li>
      ))}
    </ul>
  );
}
```

### Conditional Queries

```typescript
import { useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function UserProfile({ userId }: { userId: Id<"users"> | null }) {
  // Skip query when userId is null
  const user = useQuery(
    api.users.get,
    userId ? { userId } : "skip"
  );

  if (userId === null) {
    return <div>Select a user</div>;
  }

  if (user === undefined) {
    return <div>Loading...</div>;
  }

  return <div>{user.name}</div>;
}
```

### Mutations with Real-time Updates

```typescript
import { useMutation, useQuery } from "convex/react";
import { api } from "../convex/_generated/api";

function TaskManager({ userId }: { userId: Id<"users"> }) {
  const tasks = useQuery(api.tasks.list, { userId });
  const createTask = useMutation(api.tasks.create);
  // Additional mutation logic here
}
```