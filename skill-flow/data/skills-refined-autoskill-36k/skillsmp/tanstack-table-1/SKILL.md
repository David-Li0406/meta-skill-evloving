---
name: tanstack-table
description: Build data tables with TanStack Table and React Aria Components. Use when creating tables, implementing sorting, filtering, pagination, row selection, or column visibility.
---

# TanStack Table

## Quick Start

```sh
pnpm add @tanstack/react-table
```

```tsx
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from '@tanstack/react-table';

const columns: ColumnDef<Person>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'email', header: 'Email' },
];

function DataTable({ data }: { data: Person[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table className="w-full border-collapse">
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id} className="border p-2 text-left">
                {flexRender(
                  header.column.columnDef.header,
                  header.getContext(),
                )}
              </th>
            ))}
          </tr>
        ))}
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
  );
}
```

## Row Models

Import only what you need:

```tsx
import {
  getCoreRowModel, // Required
  getSortedRowModel, // Sorting
  getFilteredRowModel, // Filtering
  getPaginationRowModel, // Pagination
} from '@tanstack/react-table';
```

## Column Definitions

```tsx
// Basic
{ accessorKey: 'email', header: 'Email' }

// Computed value
{ accessorFn: (row) => `${row.first} ${row.last}`, id: 'fullName', header: 'Name' }

// Custom cell
{
  accessorKey: 'amount',
  cell: ({ row }) => formatCurrency(row.getValue('amount')),
}

// Actions column
{
  id: 'actions',
  cell: ({ row }) => <ActionMenu item={row.original} />,
}
```

## State Management Pattern

```tsx
const [sorting, setSorting] = useState<SortingState>([]);
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

const table = useReactTable({
  data,
  columns,
  state: { sorting, columnFilters, rowSelection },
  onSortingChange: setSorting,
  onColumnFiltersChange: setColumnFilters,
  onRowSelectionChange: setRowSelection,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
});
```

## Common Operations

| Task              | Method                         |
| ----------------- | ------------------------------ |
| Sort column       | `column.toggleSorting()`       |
| Filter column     | `column.setFilterValue(value)` |
| Next page         | `table.nextPage()`             |
| Select row        | `row.toggleSelected()`         |
| Hide column       | `column.toggleVisibility()`    |
| Get original data | `row.original`                 |

## Project Structure

```sh
apps/web/src/routes/payments/
├── columns.tsx      # Column definitions
├── data-table.tsx   # DataTable component
└── index.tsx        # Route (fetches data)
```

## Common Mistakes

| Mistake                          | Correct Pattern                                     |
| -------------------------------- | --------------------------------------------------- |
| Missing `getCoreRowModel`        | Always required as base row model                   |
| Importing all row models         | Only import what you use                            |
| Not using `flexRender`           | Required for both static and dynamic content        |
| Missing `key` on rows            | Use `row.id` as key                                 |
| Accessing data directly          | Use `row.original` for the original data            |
| Client pagination for large data | Use `manualPagination: true` for server-side        |
| Missing table state              | Control sorting/filtering via state props           |
| Over-abstracting table           | Each table is unique, don't create generic wrappers |

## Delegation

- **Pattern discovery**: For finding existing table implementations, use `Explore` agent
- **Code review**: After implementing tables, delegate to `code-reviewer` agent

## Topic References

- [Server Pagination](server-pagination.md) - Server-side pagination, URL sync, faceted filters
- [Infinite Scroll](infinite-scroll.md) - Cursor pagination, intersection observer, virtual scrolling
- [Column Definitions](column-definitions.md) - Headers, cells, sorting, filtering, visibility
- [Reusable Components](reusable-components.md) - DataTable components, skeletons, full example
