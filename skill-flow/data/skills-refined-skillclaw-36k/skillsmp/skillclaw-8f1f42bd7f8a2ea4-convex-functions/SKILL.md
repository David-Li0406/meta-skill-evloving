---
name: convex-functions
description: Use this skill when you need to write queries, mutations, actions, and HTTP actions in Convex with proper argument validation, error handling, and runtime considerations.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Functions Documentation](https://docs.convex.dev/functions)
- Query Functions: [Query Functions Documentation](https://docs.convex.dev/functions/query-functions)
- Mutation Functions: [Mutation Functions Documentation](https://docs.convex.dev/functions/mutation-functions)
- Actions: [Actions Documentation](https://docs.convex.dev/functions/actions)
- HTTP Actions: [HTTP Actions Documentation](https://docs.convex.dev/functions/http-actions)
- For broader context: [LLMS Documentation](https://docs.convex.dev/llms.txt)

## Instructions

### Function Types Overview

| Type      | Database Access | External APIs | Caching         | Use Case            |
|-----------|----------------|---------------|------------------|---------------------|
| Query     | Read-only      | No            | Yes, reactive     | Fetching data       |
| Mutation  | Read/Write     | No            | No               | Modifying data      |
| Action    | Via runQuery/runMutation | Yes | No               | External integrations|
| HTTP Action| Via runQuery/runMutation | Yes | No               | Webhooks, APIs      |

### Queries

Queries are reactive, cached, and read-only:

```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      _creationTime: v.number(),
      name: v.string(),
      email: v.string(),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});

// Query with index
export const listUserTasks = query({
  args: { userId: v.id("users") },
  returns: v.array(v.object({
    _id: v.id("tasks"),
    _creationTime: v.number(),
    title: v.string(),
    completed: v.boolean(),
  })),
  handler: async (ctx, args) => {
    return await ctx.db
      .query("tasks")
      .withIndex("by_user", (q) => q.eq("userId", args.userId))
      .order("desc")
      .collect();
  },
});
```

### Mutations

Mutations modify the database and are transactional:

```typescript
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { ConvexError } from "convex/values";

export const createTask = mutation({
  args: { userId: v.id("users"), title: v.string() },
  handler: async (ctx, args) => {
    // Implementation for creating a task
  },
});
```