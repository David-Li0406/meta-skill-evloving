---
name: convex-best-practices
description: Use this skill when you want to build production-ready Convex applications by following best practices for function organization, query optimization, validation, TypeScript usage, and error handling.
---

# Convex Best Practices

Build production-ready Convex applications by following established patterns for function organization, query optimization, validation, TypeScript usage, and error handling.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Best Practices](https://docs.convex.dev/understanding/best-practices/)
- Error Handling: [Error Handling Documentation](https://docs.convex.dev/functions/error-handling)
- Write Conflicts: [Write Conflicts Documentation](https://docs.convex.dev/error#1)
- For broader context: [LLMs Documentation](https://docs.convex.dev/llms.txt)

## Instructions

### The Zen of Convex

1. **Convex manages the hard parts** - Let Convex handle caching, real-time sync, and consistency.
2. **Functions are the API** - Design your functions as your application's interface.
3. **Schema is truth** - Define your data model explicitly in `schema.ts`.
4. **TypeScript everywhere** - Leverage end-to-end type safety.
5. **Queries are reactive** - Think in terms of subscriptions, not requests.

### Function Organization

Organize your Convex functions by domain:

```typescript
// convex/users.ts - User-related functions
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

export const get = query({
  args: { userId: v.id("users") },
  returns: v.union(v.object({
    _id: v.id("users"),
    _creationTime: v.number(),
    name: v.string(),
    email: v.string(),
  }), v.null()),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```

### Argument and Return Validation

Always define validators for arguments AND return types:

```typescript
export const createTask = mutation({
  args: {
    title: v.string(),
    description: v.optional(v.string()),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  },
  returns: v.id("tasks"),
  handler: async (ctx, args) => {
    return await ctx.db.insert("tasks", {
      title: args.title,
      description: args.description,
      priority: args.priority,
      completed: false,
      createdAt: Date.now(),
    });
  },
});
```

### Query Patterns

Use indexes instead of filters for efficient queries:

```typescript
// Example of using indexes in queries
```