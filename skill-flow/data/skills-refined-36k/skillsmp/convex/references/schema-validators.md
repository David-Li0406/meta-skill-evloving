# Schema & Validators

## Where Schema Lives

Always define schema in **`convex/schema.ts`**:

```ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  messages: defineTable({
    body: v.string(),
    author: v.string(),
  }).index("by_author", ["author"]),
});
```

## System Fields

Convex automatically adds these fields to every document:

- `_id: v.id(tableName)`
- `_creationTime: v.number()`

You **never** declare these in the schema; Convex adds them.

## Available Validators

Common validators:

- `v.string()`
- `v.number()`
- `v.boolean()`
- `v.id("tableName")`
- `v.array(v.string())`
- `v.object({ ... })`
- `v.record(keyValidator, valueValidator)`
- `v.null()`
- `v.int64()` (for `bigint`)
- `v.optional(validator)` - makes a field optional
- `v.union(v1, v2, ...)` - union of multiple types

**Do not use** `v.map()` or `v.set()` – they're not supported.

## Validator Example

```ts
import { v } from "convex/values";

const messageValidator = v.object({
  body: v.string(),
  author: v.string(),
  pinned: v.optional(v.boolean()),
});
```

## Return Validators

Safe policy for return validators:

- **Always** define `args` validators
- For `returns`:
  - You **may omit** `returns` initially for simple endpoints
  - If you *do* add it, make sure it's correct and stays synced with the actual return value
  - If a function returns `null`, `returns: v.null()` is fine

Example with returns:

```ts
export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(v.null(), v.object({ name: v.string() })),
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});
```
