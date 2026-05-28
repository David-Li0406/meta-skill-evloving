<function_syntax>
ALWAYS use the new function syntax with explicit argument and return validators:

```typescript
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.object({
    _id: v.id("users"),
    _creationTime: v.number(),
    name: v.string(),
    email: v.string(),
  }),
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) throw new Error("User not found");
    return user;
  },
});
```

<rules>
- ALWAYS include `args` and `returns` validators
- If function returns nothing, use `returns: v.null()` and `return null;`
- Use `v.null()` for null values (NOT `undefined`)
- Use `v.id("tableName")` for document IDs, not `v.string()`
</rules>
</function_syntax>

<public_vs_internal>
Use the right function type based on access needs:

- `query`, `mutation`, `action` - **Public API**, exposed to internet
- `internalQuery`, `internalMutation`, `internalAction` - **Private**, only callable from other Convex functions

```typescript
// Public - can be called from client
export const listPublicPosts = query({ ... });

// Internal - only callable from other Convex functions
export const processPayment = internalMutation({ ... });
```

Use `api.file.function` for public, `internal.file.function` for internal references.
</public_vs_internal>

<actions_for_external_apis>
Use `action` for external API calls. Actions cannot access `ctx.db` directly.

```typescript
"use node";  // Add this for Node.js APIs
import { action, internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";

export const sendEmail = action({
  args: { to: v.string(), subject: v.string(), body: v.string() },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Call external API
    await emailService.send(args);

    // Save to database via mutation (actions can't use ctx.db)
    await ctx.runMutation(internal.emails.logSent, {
      to: args.to,
      sentAt: Date.now()
    });
    return null;
  },
});
```

<rules>
- Add `"use node";` at top of file for Node.js APIs
- Actions can't access `ctx.db` - use `ctx.runMutation` or `ctx.runQuery`
- Minimize calls to queries/mutations from actions (race condition risk)
</rules>
</actions_for_external_apis>

<validators_reference>
| Convex Type | Validator | TS Type | Notes |
|-------------|-----------|---------|-------|
| Id | `v.id("table")` | `Id<"table">` | Document reference |
| Null | `v.null()` | `null` | Use instead of undefined |
| Int64 | `v.int64()` | `bigint` | For large integers |
| Float64 | `v.number()` | `number` | All numbers |
| Boolean | `v.boolean()` | `boolean` | |
| String | `v.string()` | `string` | Max 1MB UTF-8 |
| Bytes | `v.bytes()` | `ArrayBuffer` | Binary data |
| Array | `v.array(v)` | `Array<T>` | Max 8192 items |
| Object | `v.object({})` | `object` | Max 1024 fields |
| Record | `v.record(k, v)` | `Record<K, V>` | Dynamic keys |
| Optional | `v.optional(v)` | `T \| undefined` | Optional field |
| Union | `v.union(a, b)` | `A \| B` | Type union |
| Literal | `v.literal("x")` | `"x"` | Exact value |
</validators_reference>

<typescript_types>
Be strict with types, especially document IDs:

```typescript
import { Id, Doc } from "./_generated/dataModel";

// Use specific ID types, not string
async function getUser(ctx: QueryCtx, userId: Id<"users">): Promise<Doc<"users"> | null> {
  return await ctx.db.get(userId);
}

// For records with ID keys
const userMap: Record<Id<"users">, string> = {};
```

<type_helpers>
- `Id<"tableName">` - Typed document ID
- `Doc<"tableName">` - Full document type with `_id` and `_creationTime`
</type_helpers>
</typescript_types>
