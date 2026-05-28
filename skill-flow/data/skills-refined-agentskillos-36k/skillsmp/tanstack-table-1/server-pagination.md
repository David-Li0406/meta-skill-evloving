# Server-Side Pagination Reference

## Server Function with Pagination

```tsx
import { createServerFn } from '@tanstack/react-start';
import { db, users, count, desc, asc, ilike } from '@oakoss/database';

const getUsers = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({
      page: z.number().default(1),
      pageSize: z.number().default(10),
      sortBy: z.string().optional(),
      sortOrder: z.enum(['asc', 'desc']).optional(),
      filter: z.string().optional(),
    }),
  )
  .handler(async ({ data }) => {
    const { page, pageSize, sortBy, sortOrder, filter } = data;
    const offset = (page - 1) * pageSize;

    // Build query
    let query = db.select().from(users);

    if (filter) {
      query = query.where(ilike(users.name, `%${filter}%`));
    }

    if (sortBy) {
      const column = users[sortBy as keyof typeof users];
      query = query.orderBy(sortOrder === 'desc' ? desc(column) : asc(column));
    }

    const [items, [{ count: total }]] = await Promise.all([
      query.limit(pageSize).offset(offset),
      db.select({ count: count() }).from(users),
    ]);

    return {
      items,
      meta: { page, pageSize, total, totalPages: Math.ceil(total / pageSize) },
    };
  });
```

## Server-Paginated Table Component

```tsx
'use client';

import {
  useQuery,
  keepPreviousData,
  queryOptions,
} from '@tanstack/react-query';
import { useReactTable, getCoreRowModel } from '@tanstack/react-table';

type PaginationState = { pageIndex: number; pageSize: number };
type SortingState = { id: string; desc: boolean }[];

function usersQueryOptions(
  pagination: PaginationState,
  sorting: SortingState,
  filter: string,
) {
  return queryOptions({
    queryKey: ['users', 'list', pagination, sorting, filter],
    queryFn: () =>
      getUsers({
        data: {
          page: pagination.pageIndex + 1,
          pageSize: pagination.pageSize,
          sortBy: sorting[0]?.id,
          sortOrder: sorting[0]?.desc ? 'desc' : 'asc',
          filter,
        },
      }),
    placeholderData: keepPreviousData,
  });
}

function UsersTable() {
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  });
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const { data, isPending, isFetching } = useQuery(
    usersQueryOptions(pagination, sorting, globalFilter),
  );

  const table = useReactTable({
    data: data?.items ?? [],
    columns,
    pageCount: data?.meta.totalPages ?? -1,
    state: { pagination, sorting, globalFilter },
    onPaginationChange: setPagination,
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
  });

  if (isPending) return <TableSkeleton />;

  return (
    <div className="relative">
      {isFetching && <LoadingOverlay />}
      <DataTable table={table} columns={columns} />
      <ServerPagination table={table} totalCount={data?.meta.total} />
    </div>
  );
}
```

## URL Search Params Integration

```tsx
import { createFileRoute, useNavigate } from '@tanstack/react-router';
import { zodValidator } from '@tanstack/zod-adapter';

// Sync table state with URL for shareable links
const searchSchema = z.object({
  page: z.number().default(1),
  size: z.number().default(10),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).optional(),
  q: z.string().optional(),
});

export const Route = createFileRoute('/users')({
  validateSearch: zodValidator(searchSchema),
  loaderDeps: ({ search }) => search,
  loader: async ({ context, deps }) => {
    await context.queryClient.ensureQueryData(
      usersQueryOptions(
        { pageIndex: deps.page - 1, pageSize: deps.size },
        deps.sort ? [{ id: deps.sort, desc: deps.order === 'desc' }] : [],
        deps.q ?? '',
      ),
    );
  },
});

function UsersPage() {
  const search = Route.useSearch();
  const navigate = useNavigate();

  // Convert URL params to table state
  const pagination = { pageIndex: search.page - 1, pageSize: search.size };
  const sorting = search.sort
    ? [{ id: search.sort, desc: search.order === 'desc' }]
    : [];

  const handlePaginationChange = (updater: Updater<PaginationState>) => {
    const newPagination =
      typeof updater === 'function' ? updater(pagination) : updater;
    navigate({
      search: (prev) => ({
        ...prev,
        page: newPagination.pageIndex + 1,
        size: newPagination.pageSize,
      }),
    });
  };

  const handleSortingChange = (updater: Updater<SortingState>) => {
    const newSorting =
      typeof updater === 'function' ? updater(sorting) : updater;
    navigate({
      search: (prev) => ({
        ...prev,
        sort: newSorting[0]?.id,
        order: newSorting[0]?.desc ? 'desc' : 'asc',
      }),
    });
  };

  // ... table setup with these handlers
}
```

## Server-Side Filtering

### Faceted Filters with Server Data

```tsx
const getFilterOptions = createServerFn({ method: 'GET' }).handler(async () => {
  const [statuses, roles] = await Promise.all([
    db.selectDistinct({ status: users.status }).from(users),
    db.selectDistinct({ role: users.role }).from(users),
  ]);

  return {
    status: statuses.map((s) => s.status),
    role: roles.map((r) => r.role),
  };
});

function FilterToolbar() {
  const { data: options } = useQuery({
    queryKey: ['users', 'filter-options'],
    queryFn: getFilterOptions,
    staleTime: 1000 * 60 * 10, // Cache for 10 minutes
  });

  return (
    <div className="flex gap-2">
      {options?.status && (
        <FacetedFilter
          column={table.getColumn('status')}
          title="Status"
          options={options.status.map((s) => ({ label: s, value: s }))}
        />
      )}
      {options?.role && (
        <FacetedFilter
          column={table.getColumn('role')}
          title="Role"
          options={options.role.map((r) => ({ label: r, value: r }))}
        />
      )}
    </div>
  );
}
```

### Column Filters to Server Query

```tsx
function buildServerFilters(columnFilters: ColumnFiltersState) {
  const filters: Record<string, string | string[]> = {};

  for (const filter of columnFilters) {
    if (Array.isArray(filter.value)) {
      filters[filter.id] = filter.value;
    } else {
      filters[filter.id] = String(filter.value);
    }
  }

  return filters;
}

// In server function
const getUsersFiltered = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({
      filters: z.record(z.union([z.string(), z.array(z.string())])).optional(),
      // ... other params
    }),
  )
  .handler(async ({ data }) => {
    let query = db.select().from(users);

    if (data.filters) {
      for (const [key, value] of Object.entries(data.filters)) {
        const column = users[key as keyof typeof users];
        if (Array.isArray(value)) {
          query = query.where(inArray(column, value));
        } else {
          query = query.where(eq(column, value));
        }
      }
    }

    return query;
  });
```
