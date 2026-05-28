# TanStack Advanced Patterns

## Query Patterns

### Dependent Queries

```typescript
// Query that depends on another query's result
export function useShootoutWithJobs(shootoutId: number) {
  const shootoutQuery = useShootout(shootoutId);

  const jobsQuery = useQuery({
    queryKey: ['shootouts', shootoutId, 'jobs'],
    queryFn: () => fetchJSON<Job[]>(`/shootouts/${shootoutId}/jobs`),
    enabled: !!shootoutQuery.data, // Only run when shootout loaded
  });

  return { shootout: shootoutQuery, jobs: jobsQuery };
}
```

### Infinite Queries (Pagination)

```typescript
export function useInfiniteShootouts() {
  return useInfiniteQuery({
    queryKey: ['shootouts', 'infinite'],
    queryFn: ({ pageParam = 0 }) =>
      fetchJSON<{ items: Shootout[]; nextCursor: number | null }>(
        `/shootouts?cursor=${pageParam}&limit=20`
      ),
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    initialPageParam: 0,
  });
}

// Usage
function ShootoutList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteShootouts();

  return (
    <>
      {data?.pages.map(page =>
        page.items.map(shootout => <ShootoutCard key={shootout.id} {...shootout} />)
      )}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </>
  );
}
```

### Optimistic Updates

```typescript
export function useDeleteShootout() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) =>
      fetch(`/api/shootouts/${id}`, { method: 'DELETE', credentials: 'include' }),
    onMutate: async (deletedId) => {
      await queryClient.cancelQueries({ queryKey: ['shootouts'] });

      const previous = queryClient.getQueryData<Shootout[]>(['shootouts']);

      queryClient.setQueryData<Shootout[]>(['shootouts'], (old) =>
        old?.filter((s) => s.id !== deletedId)
      );

      return { previous };
    },
    onError: (err, id, context) => {
      queryClient.setQueryData(['shootouts'], context?.previous);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['shootouts'] });
    },
  });
}
```

### Prefetching

```typescript
// Prefetch on hover
function ShootoutCard({ shootout }: { shootout: Shootout }) {
  const queryClient = useQueryClient();

  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: ['shootouts', shootout.id],
      queryFn: () => fetchJSON(`/shootouts/${shootout.id}`),
      staleTime: 60000,
    });
  };

  return (
    <a href={`/shootouts/${shootout.id}`} onMouseEnter={prefetch}>
      {shootout.title}
    </a>
  );
}
```

## Form Patterns

### Form with Async Validation

```typescript
const form = useForm({
  defaultValues: { title: '' },
  onSubmit: async ({ value }) => {
    await createShootout(value);
  },
});

<form.Field
  name="title"
  validators={{
    onChange: ({ value }) =>
      value.length < 3 ? 'At least 3 characters' : undefined,
    onChangeAsync: async ({ value }) => {
      const exists = await checkTitleExists(value);
      return exists ? 'Title already taken' : undefined;
    },
    onChangeAsyncDebounceMs: 500,
  }}
>
  {(field) => (/* ... */)}
</form.Field>
```

### Dynamic Form Fields

```typescript
interface SignalChain {
  id: string;
  amp: string;
  cab: string;
}

function PipelineBuilder() {
  const form = useForm({
    defaultValues: {
      title: '',
      chains: [] as SignalChain[],
    },
  });

  return (
    <form.Field name="chains" mode="array">
      {(field) => (
        <>
          {field.state.value.map((_, i) => (
            <form.Field key={i} name={`chains[${i}].amp`}>
              {(ampField) => (
                <input
                  value={ampField.state.value}
                  onChange={(e) => ampField.handleChange(e.target.value)}
                />
              )}
            </form.Field>
          ))}
          <button
            type="button"
            onClick={() => field.pushValue({ id: crypto.randomUUID(), amp: '', cab: '' })}
          >
            Add Chain
          </button>
        </>
      )}
    </form.Field>
  );
}
```

## Table Patterns

### Sorting

```typescript
import { getSortedRowModel, SortingState } from '@tanstack/react-table';

function SortableTable({ data }: { data: Shootout[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <thead>
      {table.getHeaderGroups().map(headerGroup => (
        <tr key={headerGroup.id}>
          {headerGroup.headers.map(header => (
            <th
              key={header.id}
              onClick={header.column.getToggleSortingHandler()}
              className="cursor-pointer select-none"
            >
              {flexRender(header.column.columnDef.header, header.getContext())}
              {{ asc: ' ↑', desc: ' ↓' }[header.column.getIsSorted() as string] ?? ''}
            </th>
          ))}
        </tr>
      ))}
    </thead>
  );
}
```

### Filtering

```typescript
import { getFilteredRowModel, ColumnFiltersState } from '@tanstack/react-table';

function FilterableTable({ data }: { data: Shootout[] }) {
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const table = useReactTable({
    data,
    columns,
    state: { columnFilters, globalFilter },
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <>
      <input
        placeholder="Search..."
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        className="mb-4 px-3 py-2 border rounded-md"
      />
      <table>{/* ... */}</table>
    </>
  );
}
```

### Row Selection

```typescript
import { RowSelectionState } from '@tanstack/react-table';

function SelectableTable({ data }: { data: Shootout[] }) {
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

  const columns = [
    {
      id: 'select',
      header: ({ table }) => (
        <input
          type="checkbox"
          checked={table.getIsAllRowsSelected()}
          onChange={table.getToggleAllRowsSelectedHandler()}
        />
      ),
      cell: ({ row }) => (
        <input
          type="checkbox"
          checked={row.getIsSelected()}
          onChange={row.getToggleSelectedHandler()}
        />
      ),
    },
    // ... other columns
  ];

  const table = useReactTable({
    data,
    columns,
    state: { rowSelection },
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
  });

  const selectedRows = table.getSelectedRowModel().rows;
  // Do something with selected rows...
}
```

## WebSocket Integration

```typescript
// Real-time job progress with Query
export function useJobProgress(jobId: string) {
  const queryClient = useQueryClient();

  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/ws/jobs/${jobId}`);

    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      queryClient.setQueryData(['jobs', jobId], (old: Job | undefined) => ({
        ...old,
        ...update,
      }));
    };

    return () => ws.close();
  }, [jobId, queryClient]);

  return useQuery({
    queryKey: ['jobs', jobId],
    queryFn: () => fetchJSON<Job>(`/jobs/${jobId}`),
  });
}
```
