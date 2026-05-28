<schema_patterns>

<basic_table_with_index>
```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    role: v.union(v.literal("admin"), v.literal("user")),
  })
    .index("by_email", ["email"])
    .index("by_role", ["role"]),

  posts: defineTable({
    authorId: v.id("users"),
    title: v.string(),
    content: v.string(),
    status: v.union(v.literal("draft"), v.literal("published")),
  })
    .index("by_author", ["authorId"])
    .index("by_author_and_status", ["authorId", "status"]),
});
```
</basic_table_with_index>

<discriminated_unions>
```typescript
results: defineTable(
  v.union(
    v.object({
      kind: v.literal("success"),
      data: v.string(),
    }),
    v.object({
      kind: v.literal("error"),
      errorMessage: v.string(),
    }),
  ),
),
```
</discriminated_unions>

<system_fields>
Every document automatically has:
- `_id: v.id("tableName")`
- `_creationTime: v.number()`
</system_fields>

</schema_patterns>

<indexes>

<use_indexes_not_filters>
NEVER use `.filter()` in queries. Define indexes in schema and use `.withIndex()`:

```typescript
// BAD - Don't do this
const messages = await ctx.db
  .query("messages")
  .filter((q) => q.eq(q.field("channelId"), channelId))
  .collect();

// GOOD - Use indexes
const messages = await ctx.db
  .query("messages")
  .withIndex("by_channel", (q) => q.eq("channelId", channelId))
  .collect();
```

**Index naming:** Include all fields in the name: `by_channel`, `by_user_and_status`, etc.
</use_indexes_not_filters>

</indexes>

<pagination_pattern>
```typescript
import { paginationOptsValidator } from "convex/server";

export const listPosts = query({
  args: {
    paginationOpts: paginationOptsValidator,
    authorId: v.optional(v.id("users")),
  },
  returns: v.object({
    page: v.array(v.object({
      _id: v.id("posts"),
      _creationTime: v.number(),
      title: v.string(),
      // ... other fields
    })),
    isDone: v.boolean(),
    continueCursor: v.union(v.string(), v.null()),
  }),
  handler: async (ctx, args) => {
    let query = ctx.db.query("posts");

    if (args.authorId) {
      query = query.withIndex("by_author", (q) =>
        q.eq("authorId", args.authorId!)
      );
    }

    return await query.order("desc").paginate(args.paginationOpts);
  },
});
```
</pagination_pattern>

<http_endpoints>
```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

http.route({
  path: "/webhook/stripe",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    const body = await req.text();
    const signature = req.headers.get("stripe-signature");

    // Process webhook...

    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```
</http_endpoints>

<scheduling>
```typescript
// In a mutation
await ctx.scheduler.runAfter(0, internal.emails.send, { userId });
await ctx.scheduler.runAfter(60000, internal.cleanup.expired, {}); // 1 minute

// Cron jobs (convex/crons.ts)
import { cronJobs } from "convex/server";
import { internal } from "./_generated/api";

const crons = cronJobs();
crons.interval("cleanup", { hours: 1 }, internal.cleanup.run, {});
export default crons;
```
</scheduling>
