# Column Definitions Reference

## Custom Header with Sorting

```tsx
import { Button } from '@oakoss/ui';

{
  accessorKey: 'email',
  header: ({ column }) => (
    <Button
      variant="ghost"
      onPress={() => column.toggleSorting(column.getIsSorted() === 'asc')}
    >
      Email
      <ArrowUpDown className="ml-2 size-4" />
    </Button>
  ),
}
```

## Formatted Cell

```tsx
{
  accessorKey: 'amount',
  header: () => <div className="text-right">Amount</div>,
  cell: ({ row }) => {
    const amount = parseFloat(row.getValue('amount'));
    const formatted = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
    return <div className="text-right font-medium">{formatted}</div>;
  },
}
```

## Actions Column

```tsx
import { Menu, MenuItem, MenuTrigger, Button, Popover } from '@oakoss/ui';

{
  id: 'actions',
  enableHiding: false,
  cell: ({ row }) => {
    const item = row.original;
    return (
      <MenuTrigger>
        <Button variant="ghost" aria-label="Actions">
          <MoreHorizontal className="size-4" />
        </Button>
        <Popover>
          <Menu>
            <MenuItem onAction={() => navigator.clipboard.writeText(item.id)}>
              Copy ID
            </MenuItem>
            <MenuItem>View</MenuItem>
            <MenuItem>Delete</MenuItem>
          </Menu>
        </Popover>
      </MenuTrigger>
    );
  },
}
```

## Select All Column

```tsx
import { Checkbox } from '@oakoss/ui';

{
  id: 'select',
  header: ({ table }) => (
    <Checkbox
      isSelected={table.getIsAllPageRowsSelected()}
      isIndeterminate={table.getIsSomePageRowsSelected()}
      onChange={(isSelected) => table.toggleAllPageRowsSelected(isSelected)}
      aria-label="Select all"
    />
  ),
  cell: ({ row }) => (
    <Checkbox
      isSelected={row.getIsSelected()}
      onChange={(isSelected) => row.toggleSelected(isSelected)}
      aria-label="Select row"
    />
  ),
  enableSorting: false,
  enableHiding: false,
}
```

## Type-Safe Column Helper

```tsx
import { createColumnHelper } from '@tanstack/react-table';

const columnHelper = createColumnHelper<Person>();

const columns = [
  columnHelper.accessor('name', { header: 'Name' }),
  columnHelper.accessor((row) => `${row.first} ${row.last}`, {
    id: 'fullName',
    header: 'Full Name',
  }),
  columnHelper.display({
    id: 'actions',
    cell: ({ row }) => <ActionMenu row={row} />,
  }),
];
```

## Sorting

```tsx
const [sorting, setSorting] = useState<SortingState>([]);

const table = useReactTable({
  state: { sorting },
  onSortingChange: setSorting,
  getSortedRowModel: getSortedRowModel(),
});

// Header with sort indicators
{
  accessorKey: 'name',
  header: ({ column }) => (
    <Button variant="ghost" onPress={() => column.toggleSorting()}>
      Name
      {column.getIsSorted() === 'asc' && <ChevronUp />}
      {column.getIsSorted() === 'desc' && <ChevronDown />}
    </Button>
  ),
}
```

## Filtering

### Column Filter

```tsx
import { TextField } from '@oakoss/ui';

const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);

const table = useReactTable({
  state: { columnFilters },
  onColumnFiltersChange: setColumnFilters,
  getFilteredRowModel: getFilteredRowModel(),
});

<TextField
  label="Filter emails"
  value={(table.getColumn('email')?.getFilterValue() as string) ?? ''}
  onChange={(value) => table.getColumn('email')?.setFilterValue(value)}
/>;
```

### Global Filter

```tsx
const [globalFilter, setGlobalFilter] = useState('');

const table = useReactTable({
  state: { globalFilter },
  onGlobalFilterChange: setGlobalFilter,
  getFilteredRowModel: getFilteredRowModel(),
});

<TextField
  label="Search all"
  value={globalFilter}
  onChange={(value) => setGlobalFilter(value)}
/>;
```

### Built-in Filter Functions

| Function         | Description               |
| ---------------- | ------------------------- |
| `includesString` | Case-insensitive contains |
| `equalsString`   | Exact match               |
| `inNumberRange`  | Range `[min, max]`        |
| `arrIncludes`    | Array includes value      |
| `arrIncludesAll` | Array includes all        |

## Fuzzy Filtering

```tsx
import { rankItem, compareItems } from '@tanstack/match-sorter-utils';

declare module '@tanstack/react-table' {
  interface FilterFns {
    fuzzy: FilterFn<unknown>;
  }
}

const fuzzyFilter: FilterFn<unknown> = (row, columnId, value, addMeta) => {
  const itemRank = rankItem(row.getValue(columnId), value);
  addMeta({ itemRank });
  return itemRank.passed;
};

const table = useReactTable({
  filterFns: { fuzzy: fuzzyFilter },
  globalFilterFn: 'fuzzy',
});
```

## Pagination

```tsx
const table = useReactTable({
  getPaginationRowModel: getPaginationRowModel(),
});

// Controls
<Button
  onPress={() => table.previousPage()}
  isDisabled={!table.getCanPreviousPage()}
>
  Previous
</Button>
<Button
  onPress={() => table.nextPage()}
  isDisabled={!table.getCanNextPage()}
>
  Next
</Button>

// Info
<span>Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}</span>

// Page size
<Select
  label="Rows per page"
  selectedKey={String(table.getState().pagination.pageSize)}
  onSelectionChange={(key) => table.setPageSize(Number(key))}
>
  {[10, 20, 50].map((size) => (
    <SelectItem key={size} id={String(size)}>{size}</SelectItem>
  ))}
</Select>
```

### Pagination Methods

| Method                 | Description            |
| ---------------------- | ---------------------- |
| `nextPage()`           | Next page              |
| `previousPage()`       | Previous page          |
| `setPageIndex(n)`      | Go to page (0-indexed) |
| `setPageSize(n)`       | Set rows per page      |
| `getPageCount()`       | Total pages            |
| `getCanNextPage()`     | Can go forward         |
| `getCanPreviousPage()` | Can go back            |

## Column Visibility

```tsx
import { Menu, MenuItem, MenuTrigger, Button, Popover } from '@oakoss/ui';

const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({});

const table = useReactTable({
  state: { columnVisibility },
  onColumnVisibilityChange: setColumnVisibility,
});

<MenuTrigger>
  <Button variant="outline">Columns</Button>
  <Popover>
    <Menu>
      {table
        .getAllColumns()
        .filter((col) => col.getCanHide())
        .map((column) => (
          <MenuItem key={column.id} onAction={() => column.toggleVisibility()}>
            {column.getIsVisible() ? '✓ ' : '  '}
            {column.id}
          </MenuItem>
        ))}
    </Menu>
  </Popover>
</MenuTrigger>;
```
