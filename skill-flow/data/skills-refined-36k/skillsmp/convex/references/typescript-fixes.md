# Fixing TS2589 "Type instantiation is excessively deep"

Large Convex codebases (50+ exported functions) can trigger TypeScript's recursion limit when computing the generated `api` type. This manifests as TS2589 errors throughout the codebase.

## Root Cause

The generated `fullApi` type in `_generated/api.d.ts` grows exponentially with the number of exported functions. TypeScript exhausts its recursion depth computing this massive type.

## Best Solution: Enable Static API Generation

Add a `convex.json` file at your Convex package root:

```json
{
  "codegen": {
    "staticApi": true,
    "staticDataModel": true
  }
}
```

Then regenerate types with `npx convex codegen` or restart `convex dev`.

**Benefits:**
- Eliminates all TS2589 errors immediately
- Greatly improves autocomplete and incremental typechecking performance

**Tradeoffs:**
- Types only update when `convex dev` is running
- Jump-to-definition no longer works (must manually navigate to files)
- Functions default to `v.any()` without explicit return validators

**Important:** When using static API, you must use dot notation for internal references:
```ts
// Bad - string path indexing doesn't work with static API
internal['actions/foo'].myAction

// Good - use dot notation
internal.actions.foo.myAction
```

## Alternative: Add Explicit Return Types to Handlers

If you can't use static API, break the type inference chain by adding explicit return types:

**Bad – TypeScript tries to infer the return type:**

```ts
export const get = query({
  args: { id: v.id("items") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  },
});
```

**Good – Explicit return type stops inference chain:**

```ts
export const get = query({
  args: { id: v.id("items") },
  handler: async (ctx, args): Promise<Doc<"items"> | null> => {
    return await ctx.db.get(args.id);
  },
});
```

## Common Return Type Patterns

```ts
import type { Doc, Id } from "./_generated/dataModel";

// Single document
handler: async (ctx, args): Promise<Doc<"items"> | null> => { ... }

// Array of documents
handler: async (ctx, args): Promise<Doc<"items">[]> => { ... }

// Custom object
handler: async (ctx, args): Promise<{ id: Id<"items">; name: string } | null> => { ... }

// Void/null return
handler: async (ctx, args): Promise<null> => { ... return null; }

// Insert returns Id
handler: async (ctx, args): Promise<Id<"items">> => { ... }
```

## Helper Functions for Shared Logic

Instead of `ctx.runQuery` within the same file (which creates circular type references), extract shared logic to plain async functions:

```ts
// Bad – circular reference
export const getItem = query({
  handler: async (ctx, args) => {
    return await ctx.runQuery(api.items.getItemInternal, args); // ❌ Circular
  },
});

// Good – helper function
async function getItemById(ctx: QueryCtx, id: Id<"items">): Promise<Doc<"items"> | null> {
  return await ctx.db.get(id);
}

export const getItem = query({
  args: { id: v.id("items") },
  handler: async (ctx, args): Promise<Doc<"items"> | null> => {
    return await getItemById(ctx, args.id);
  },
});
```

## When Calling from Actions

Use `internalMutation`/`internalQuery` to avoid circular `api` references:

```ts
// dataRooms.ts
export const addDocumentInternal = internalMutation({
  args: { roomId: v.id("dataRooms"), documentId: v.id("documents") },
  handler: async (ctx, args): Promise<null> => {
    // ... implementation
    return null;
  },
});

export const addDocumentFromExternal = action({
  handler: async (ctx, args) => {
    // Use internal.* instead of api.* to avoid circular reference
    await ctx.runMutation(internal.dataRooms.addDocumentInternal, args);
  },
});
```

## Priority Order for Fixing

1. Start with files that export the most functions
2. Focus on queries/mutations called from actions first
3. Add return types to public API functions before internal ones
