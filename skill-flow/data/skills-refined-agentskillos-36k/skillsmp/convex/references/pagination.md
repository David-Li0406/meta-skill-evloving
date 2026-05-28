# Paginated Queries

Paginated queries return results in incremental pages for "Load More" buttons or infinite scroll UIs.

## Writing Paginated Query Functions

Convex uses cursor-based pagination. Define a query that:

1. Takes `paginationOpts` argument with `paginationOptsValidator`
2. Calls `.paginate(paginationOpts)` on a database query

```ts
import { v } from "convex/values";
import { query } from "./_generated/server";
import { paginationOptsValidator } from "convex/server";

export const list = query({
  args: { paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

### PaginationOptions

- `numItems: number` - maximum documents to return
- `cursor: string | null` - cursor for next page (null for first page)

### PaginationResult

- `page` - array of documents
- `isDone` - boolean, true if this is the last page
- `continueCursor` - string cursor for next page

### Additional Arguments

```ts
export const listByAuthor = query({
  args: { paginationOpts: paginationOptsValidator, author: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("messages")
      .withIndex("by_author", q => q.eq("author", args.author))
      .order("desc")
      .paginate(args.paginationOpts);
  },
});
```

### Transforming Results

Transform the `page` property before returning:

```ts
export const listWithTransformation = query({
  args: { paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    const results = await ctx.db
      .query("messages")
      .order("desc")
      .paginate(args.paginationOpts);
    return {
      ...results,
      page: results.page.map((message) => ({
        author: message.author.slice(0, 1),
        body: message.body.toUpperCase(),
      })),
    };
  },
});
```

## React: usePaginatedQuery

```tsx
import { usePaginatedQuery } from "convex/react";
import { api } from "../convex/_generated/api";

export function Messages() {
  const { results, status, loadMore } = usePaginatedQuery(
    api.messages.list,
    {},
    { initialNumItems: 5 },
  );

  return (
    <div>
      {results?.map(({ _id, body }) => <div key={_id}>{body}</div>)}
      <button onClick={() => loadMore(5)} disabled={status !== "CanLoadMore"}>
        Load More
      </button>
    </div>
  );
}
```

### Hook Arguments

1. Function reference (e.g., `api.messages.list`)
2. Arguments object (excluding `paginationOpts`)
3. Options: `{ initialNumItems: number }`

### Hook Return Value

- `results` - array of all loaded results
- `isLoading` - whether currently loading
- `status` - one of:
  - `"LoadingFirstPage"` - loading initial page
  - `"CanLoadMore"` - more items available
  - `"LoadingMore"` - loading another page
  - `"Exhausted"` - reached end of list
- `loadMore(n)` - callback to fetch `n` more items

### With Additional Arguments

```tsx
const { results, status, loadMore } = usePaginatedQuery(
  api.messages.listByAuthor,
  { author: "Alex" },
  { initialNumItems: 5 },
);
```

## Reactivity

Paginated queries are **completely reactive** - components auto-rerender when items are added, removed, or changed.

**Important:** Page sizes may change! If you request 10 items and one is removed, the page may shrink to 9. If items are added, pages may grow beyond initial size.

## Manual Pagination (Outside React)

For scripts or non-React contexts:

```ts
import { ConvexHttpClient } from "convex/browser";
import { api } from "../convex/_generated/api";

const client = new ConvexHttpClient(process.env.CONVEX_URL!);

async function getAllMessages() {
  let continueCursor = null;
  let isDone = false;
  let page;
  const results = [];

  while (!isDone) {
    ({ continueCursor, isDone, page } = await client.query(api.messages.list, {
      paginationOpts: { numItems: 5, cursor: continueCursor },
    }));
    results.push(...page);
  }

  return results;
}
```
