---
name: convex-migrations
description: Use this skill when you need to evolve your Convex database schema safely, including adding new fields, backfilling data, removing deprecated fields, and maintaining zero-downtime deployments.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Database Schemas](https://docs.convex.dev/database/schemas)
- Schema Overview: [Convex Database](https://docs.convex.dev/database)
- Migration Patterns: [Migrate Data from Postgres to Convex](https://stack.convex.dev/migrate-data-postgres-to-convex)
- For broader context: [LLMs Overview](https://docs.convex.dev/llms.txt)

## Migration Philosophy

Convex handles schema evolution differently than traditional databases:

- No explicit migration files or commands
- Schema changes deploy instantly with `npx convex dev`
- Existing data is not automatically transformed
- Use optional fields and backfill mutations for safe migrations

## Instructions

### Adding New Fields

Start with optional fields, then backfill:

```typescript
// Step 1: Add optional field to schema
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    // New field - start as optional
    avatarUrl: v.optional(v.string()),
  }),
});
```

```typescript
// Step 2: Update code to handle both cases
// convex/users.ts
import { query } from "./_generated/server";
import { v } from "convex/values";

export const getUser = query({
  args: { userId: v.id("users") },
  returns: v.union(
    v.object({
      _id: v.id("users"),
      name: v.string(),
      email: v.string(),
      avatarUrl: v.union(v.string(), v.null()),
    }),
    v.null()
  ),
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) return null;

    return {
      _id: user._id,
      name: user.name,
      email: user.email,
      // Handle missing field gracefully
      avatarUrl: user.avatarUrl ?? null,
    };
  },
});
```

```typescript
// Step 3: Backfill existing documents
// convex/migrations.ts
import { internalMutation } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";

// Implement backfill logic here
```