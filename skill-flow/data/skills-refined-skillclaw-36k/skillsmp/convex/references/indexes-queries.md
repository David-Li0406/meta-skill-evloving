# Indexes, Queries, and Search

This is where most Convex mistakes happen. Be extra careful.

## Index Basics

Define indexes on tables with `.index(name, [fields...])`.

Rules:
- Index names **must be unique** per table
- Index names should include the field names: e.g. `by_channel_and_author` for `["channelId", "authorId"]`
- Convex automatically adds `_creationTime` as the **final index column** and provides built-in index **`by_creation_time`** for all tables
- **Never** define your own `.index("by_creation_time", ["_creationTime"])` – that's always wrong
- **Never** include `_creationTime` as a column in a custom index

**Bad:**

```ts
.index("by_creation_time", ["_creationTime"]) // ❌
.index("by_author_and_creation_time", ["author", "_creationTime"]) // ❌
```

**Good:**

```ts
.index("by_author", ["author"]) // Convex implicitly adds _creationTime
```

## Querying with Indexes

You should **not** use `.filter()` in queries. Use `.withIndex()` instead.

**Bad:**

```ts
// ❌ Do not do this
await ctx.db
  .query("messages")
  .filter(q => q.eq(q.field("author"), args.author))
  .collect();
```

**Good:**

```ts
const messages = await ctx.db
  .query("messages")
  .withIndex("by_author", q => q.eq("author", args.author))
  .order("desc")
  .collect();
```

## Ordering

- By default, queries return docs in ascending `_creationTime`
- You can explicitly specify:
  - `.order("asc")`
  - `.order("desc")`
- For indexed queries, ordering is based on index columns, with `_creationTime` as last column

## Pagination

Use `paginationOptsValidator` from `convex/server`:

```ts
import { paginationOptsValidator } from "convex/server";

export const listWithExtraArg = query({
  args: {
    paginationOpts: paginationOptsValidator,
    author: v.string(),
  },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_author", q => q.eq("author", args.author))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

`paginationOpts` fields:
- `numItems: number`
- `cursor: string | null`

Return value of `.paginate()`:
- `page`: array of documents
- `isDone`: boolean
- `continueCursor`: string

## Full-Text Search

Define search index in schema:

```ts
messages: defineTable({
  body: v.string(),
  channel: v.string(),
}).searchIndex("search_body", {
  searchField: "body",
  filterFields: ["channel"],
});
```

Query:

```ts
const messages = await ctx.db
  .query("messages")
  .withSearchIndex("search_body", q =>
    q.search("body", "hello hi").eq("channel", "#general"),
  )
  .take(10);
```

## Query Guidelines

- **Do not** use `.delete()` on queries (it doesn't exist)
  - Instead: `.collect()` results or iterate them, then `ctx.db.delete(doc._id)` from a mutation
- For a single doc from a query:
  - Use `.unique()` when you expect exactly one match (throws if multiple)
- For large result sets, prefer async iteration:

```ts
for await (const row of ctx.db.query("messages")) {
  // ...
}
```

- Avoid heavy operations in queries; they must complete within **1 second**

## Mutation Guidelines

- Use `ctx.db.insert(table, doc)` to insert
- Use `ctx.db.patch(id, partial)` for **partial updates**
- Use `ctx.db.replace(id, fullDoc)` for **full replacement** (throws if not exists)
