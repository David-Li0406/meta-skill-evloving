# Infinite Scroll Reference

## Server Function with Cursor

```tsx
import { createServerFn } from '@tanstack/react-start';
import { db, users, lt, gt, desc, asc } from '@oakoss/database';

const getUsersInfinite = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({
      cursor: z.string().optional(),
      limit: z.number().default(20),
      sortBy: z.string().default('createdAt'),
      sortOrder: z.enum(['asc', 'desc']).default('desc'),
    }),
  )
  .handler(async ({ data }) => {
    const { cursor, limit, sortBy, sortOrder } = data;
    const column = users[sortBy as keyof typeof users];

    let query = db.select().from(users);

    if (cursor) {
      query = query.where(
        sortOrder === 'desc' ? lt(column, cursor) : gt(column, cursor),
      );
    }

    query = query
      .orderBy(sortOrder === 'desc' ? desc(column) : asc(column))
      .limit(limit + 1);

    const items = await query;
    const hasMore = items.length > limit;
    const data = hasMore ? items.slice(0, -1) : items;
    const nextCursor = hasMore ? data.at(-1)?.[sortBy] : undefined;

    return { items: data, nextCursor };
  });
```

## Infinite Table with Intersection Observer

```tsx
import { useInfiniteQuery, infiniteQueryOptions } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';

function usersInfiniteOptions() {
  return infiniteQueryOptions({
    queryKey: ['users', 'infinite'],
    queryFn: ({ pageParam }) =>
      getUsersInfinite({ data: { cursor: pageParam, limit: 20 } }),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

function InfiniteUsersTable() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, isPending } =
    useInfiniteQuery(usersInfiniteOptions());

  const { ref, inView } = useInView({ threshold: 0 });

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  // Flatten all pages into single array for table
  const flatData = useMemo(
    () => data?.pages.flatMap((page) => page.items) ?? [],
    [data],
  );

  const table = useReactTable({
    data: flatData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isPending) return <TableSkeleton />;

  return (
    <div className="max-h-[600px] overflow-auto">
      <table className="w-full">
        <thead className="sticky top-0 bg-background">
          {/* ... header content */}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="border p-2">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Sentinel for infinite scroll */}
      <div ref={ref} className="h-20 flex items-center justify-center">
        {isFetchingNextPage && <Spinner />}
        {!hasNextPage && flatData.length > 0 && (
          <p className="text-muted-foreground">No more items</p>
        )}
      </div>
    </div>
  );
}
```

## Virtual Scrolling with TanStack Virtual

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualTable() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery(usersInfiniteOptions());

  const flatData = useMemo(
    () => data?.pages.flatMap((page) => page.items) ?? [],
    [data],
  );

  const table = useReactTable({
    data: flatData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const { rows } = table.getRowModel();
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 52, // Row height
    overscan: 10,
  });

  // Fetch more when near bottom
  useEffect(() => {
    const lastItem = virtualizer.getVirtualItems().at(-1);
    if (!lastItem) return;

    if (
      lastItem.index >= rows.length - 5 &&
      hasNextPage &&
      !isFetchingNextPage
    ) {
      fetchNextPage();
    }
  }, [
    virtualizer.getVirtualItems(),
    hasNextPage,
    isFetchingNextPage,
    rows.length,
    fetchNextPage,
  ]);

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <table className="w-full">
        <thead className="sticky top-0 bg-background z-10">
          {/* ... header content */}
        </thead>
        <tbody>
          <tr
            style={{
              height: `${virtualizer.getTotalSize()}px`,
              position: 'relative',
            }}
          >
            <td colSpan={columns.length}>
              {virtualizer.getVirtualItems().map((virtualRow) => {
                const row = rows[virtualRow.index];
                return (
                  <tr
                    key={row.id}
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: `${virtualRow.size}px`,
                      transform: `translateY(${virtualRow.start}px)`,
                    }}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <td key={cell.id} className="border p-2">
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext(),
                        )}
                      </td>
                    ))}
                  </tr>
                );
              })}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
```
