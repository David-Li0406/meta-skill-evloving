# Infinite Queries Reference

## Cursor-Based Pagination

```tsx
import { createServerFn } from '@tanstack/react-start';
import { useInfiniteQuery } from '@tanstack/react-query';

// Server function with cursor
const getPosts = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({ cursor: z.string().optional(), limit: z.number().default(20) }),
  )
  .handler(async ({ data }) => {
    const posts = await db.query.posts.findMany({
      where: data.cursor
        ? gt(posts.createdAt, new Date(data.cursor))
        : undefined,
      orderBy: desc(posts.createdAt),
      limit: data.limit + 1, // Fetch one extra to check hasMore
    });

    const hasMore = posts.length > data.limit;
    const items = hasMore ? posts.slice(0, -1) : posts;
    const nextCursor = hasMore
      ? items.at(-1)?.createdAt.toISOString()
      : undefined;

    return { items, nextCursor };
  });

// Query options factory
function postsInfiniteOptions() {
  return {
    queryKey: ['posts', 'infinite'],
    queryFn: ({ pageParam }) =>
      getPosts({ data: { cursor: pageParam, limit: 20 } }),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  };
}

// Component usage
function PostList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isPending } =
    useInfiniteQuery(postsInfiniteOptions());

  if (isPending) return <PostListSkeleton />;

  return (
    <>
      {data.pages.map((page, i) => (
        <Fragment key={i}>
          {page.items.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </Fragment>
      ))}
      <LoadMoreButton
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
        loading={isFetchingNextPage}
        hasMore={hasNextPage}
      />
    </>
  );
}
```

## Offset-Based Pagination

```tsx
const getPostsOffset = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({ page: z.number().default(1), limit: z.number().default(20) }),
  )
  .handler(async ({ data }) => {
    const offset = (data.page - 1) * data.limit;

    const [items, [{ count: total }]] = await Promise.all([
      db.query.posts.findMany({
        orderBy: desc(posts.createdAt),
        limit: data.limit,
        offset,
      }),
      db.select({ count: count() }).from(posts),
    ]);

    return {
      items,
      meta: {
        page: data.page,
        limit: data.limit,
        total,
        totalPages: Math.ceil(total / data.limit),
      },
    };
  });

function postsPageOptions(page: number) {
  return queryOptions({
    queryKey: ['posts', 'paginated', { page }],
    queryFn: () => getPostsOffset({ data: { page, limit: 20 } }),
    placeholderData: keepPreviousData, // Keep old data while fetching new page
  });
}
```

## Intersection Observer Auto-Loading

```tsx
import { useInView } from 'react-intersection-observer';

function InfinitePostList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery(postsInfiniteOptions());

  const { ref, inView } = useInView({ threshold: 0 });

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  return (
    <>
      {data?.pages.map((page, i) => (
        <Fragment key={i}>
          {page.items.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </Fragment>
      ))}

      {/* Sentinel element */}
      <div ref={ref} className="h-10">
        {isFetchingNextPage && <Spinner />}
      </div>
    </>
  );
}
```

## Bidirectional Infinite Scroll

```tsx
const { data, fetchNextPage, fetchPreviousPage, hasPreviousPage, hasNextPage } =
  useInfiniteQuery({
    queryKey: ['messages', chatId],
    queryFn: ({ pageParam }) =>
      getMessages({
        data: {
          chatId,
          cursor: pageParam.cursor,
          direction: pageParam.direction,
        },
      }),
    initialPageParam: { cursor: undefined, direction: 'backward' as const },
    getNextPageParam: (lastPage) =>
      lastPage.nextCursor
        ? { cursor: lastPage.nextCursor, direction: 'forward' as const }
        : undefined,
    getPreviousPageParam: (firstPage) =>
      firstPage.prevCursor
        ? { cursor: firstPage.prevCursor, direction: 'backward' as const }
        : undefined,
  });
```
