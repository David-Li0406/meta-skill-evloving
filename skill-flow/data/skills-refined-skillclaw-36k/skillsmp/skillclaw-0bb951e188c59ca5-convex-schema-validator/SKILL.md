---
name: convex-schema-validator
description: Use this skill when you need to define and validate database schemas in Convex with proper typing, index configuration, optional fields, unions, and migration strategies for schema changes.
---

# Convex Schema Validator

Define and validate database schemas in Convex with proper typing, index configuration, optional fields, unions, and strategies for schema migrations.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Schemas](https://docs.convex.dev/database/schemas)
- Indexes: [Convex Indexes](https://docs.convex.dev/database/indexes)
- Data Types: [Convex Data Types](https://docs.convex.dev/database/types)
- For broader context: [Convex LLMS](https://docs.convex.dev/llms.txt)

## Instructions

### Basic Schema Definition

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    avatarUrl: v.optional(v.string()),
    createdAt: v.number(),
  }),
  
  tasks: defineTable({
    title: v.string(),
    description: v.optional(v.string()),
    completed: v.boolean(),
    userId: v.id("users"),
    priority: v.union(
      v.literal("low"),
      v.literal("medium"),
      v.literal("high")
    ),
  }),
});
```

### Validator Types

| Validator | TypeScript Type | Example |
|-----------|----------------|---------|
| `v.string()` | `string` | `"hello"` |
| `v.number()` | `number` | `42`, `3.14` |
| `v.boolean()` | `boolean` | `true`, `false` |
| `v.null()` | `null` | `null` |
| `v.int64()` | `bigint` | `9007199254740993n` |
| `v.bytes()` | `ArrayBuffer` | Binary data |
| `v.id("table")` | `Id<"table">` | Document reference |
| `v.array(v)` | `T[]` | `[1, 2, 3]` |
| `v.object({})` | `{ ... }` | `{ name: "..." }` |
| `v.optional(v)` | `T \| undefined` | Optional field |
| `v.union(...)` | `T1 \| T2` | Multiple types |
| `v.literal(x)` | `"x"` | Exact value |
| `v.any()` | `any` | Any value |
| `v.record(k, v)` | `Record<K, V>` | Dynamic keys |

### Index Configuration

```typescript
export default defineSchema({
  messages: defineTable({
    channelId: v.id("channels"),
    authorId: v.id("users"),
    content: v.string(),
    sentAt: v.number(),
  })
    // Single field index
    .index("by_channel", ["channelId"])
    // Compound index
    .index("by_channel_and_author", ["channelId", "authorId"])
});
```