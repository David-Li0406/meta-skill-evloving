# TanStack Table Skill

This skill provides comprehensive patterns for implementing data tables using TanStack Table (React Table v8).

## Purpose

Use this skill when:
- Building data tables with sorting, filtering, pagination
- Implementing editable tables
- Creating complex table interactions
- Working with large datasets
- Customizing table behavior and appearance

## Core Documentation

@tanstack-table-implementation.md - Complete TanStack Table implementation guide

## Overview

TanStack Table is a headless table library that provides:
- Sorting (client and server-side)
- Filtering
- Pagination
- Column visibility
- Row selection
- Editable cells
- Custom cell rendering
- Virtualization support

## Basic Table Pattern

### 1. Define Column Structure

```typescript
import { ColumnDef } from "@tanstack/react-table";
import { Student } from "@zod-schema/student";

const columns: ColumnDef<Student>[] = [
  {
    accessorKey: "studentID",
    header: "Student ID",
    cell: ({ row }) => row.getValue("studentID"),
  },
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => row.getValue("name"),
  },
  {
    accessorKey: "grade",
    header: "Grade",
    cell: ({ row }) => row.getValue("grade"),
  },
  {
    id: "actions",
    header: "Actions",
    cell: ({ row }) => (
      <button onClick={() => handleEdit(row.original)}>
        Edit
      </button>
    ),
  },
];
```

### 2. Initialize Table Instance

```typescript
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
} from "@tanstack/react-table";

function MyTable({ data }: { data: Student[] }) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div>
      <table>
        {/* Render table */}
      </table>
    </div>
  );
}
```

### 3. Render Table

```typescript
<table>
  <thead>
    {table.getHeaderGroups().map((headerGroup) => (
      <tr key={headerGroup.id}>
        {headerGroup.headers.map((header) => (
          <th key={header.id}>
            {header.isPlaceholder
              ? null
              : flexRender(
                  header.column.columnDef.header,
                  header.getContext()
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
          <td key={cell.id}>
            {flexRender(cell.column.columnDef.cell, cell.getContext())}
          </td>
        ))}
      </tr>
    ))}
  </tbody>
</table>
```

## Sorting

### Client-Side Sorting

```typescript
const columns: ColumnDef<Student>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <button onClick={() => column.toggleSorting()}>
        Name {column.getIsSorted() === "asc" ? "↑" : column.getIsSorted() === "desc" ? "↓" : ""}
      </button>
    ),
    enableSorting: true,
  },
];

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  state: {
    sorting,
  },
  onSortingChange: setSorting,
});
```

### Server-Side Sorting

```typescript
const [sorting, setSorting] = useState<SortingState>([]);

// Fetch data based on sorting state
const { data } = useQuery({
  queryKey: ["students", sorting],
  queryFn: () => fetchStudents({
    sortBy: sorting[0]?.id,
    sortDir: sorting[0]?.desc ? "desc" : "asc",
  }),
});

const table = useReactTable({
  data: data?.students ?? [],
  columns,
  state: { sorting },
  onSortingChange: setSorting,
  manualSorting: true, // Tell table sorting is handled server-side
});
```

## Filtering

### Global Filter

```typescript
const [globalFilter, setGlobalFilter] = useState("");

const table = useReactTable({
  data,
  columns,
  state: {
    globalFilter,
  },
  onGlobalFilterChange: setGlobalFilter,
  getFilteredRowModel: getFilteredRowModel(),
});

// UI
<input
  value={globalFilter}
  onChange={(e) => setGlobalFilter(e.target.value)}
  placeholder="Search all columns..."
/>
```

### Column-Specific Filters

```typescript
const columns: ColumnDef<Student>[] = [
  {
    accessorKey: "grade",
    header: "Grade",
    filterFn: "equals",
    meta: {
      filterVariant: "select",
    },
  },
];

// Custom filter UI
{header.column.getCanFilter() && (
  <input
    value={(header.column.getFilterValue() ?? "") as string}
    onChange={(e) => header.column.setFilterValue(e.target.value)}
  />
)}
```

## Pagination

```typescript
const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  initialState: {
    pagination: {
      pageSize: 10,
      pageIndex: 0,
    },
  },
});

// Pagination UI
<div>
  <button
    onClick={() => table.previousPage()}
    disabled={!table.getCanPreviousPage()}
  >
    Previous
  </button>
  <span>
    Page {table.getState().pagination.pageIndex + 1} of{" "}
    {table.getPageCount()}
  </span>
  <button
    onClick={() => table.nextPage()}
    disabled={!table.getCanNextPage()}
  >
    Next
  </button>
</div>
```

## Editable Tables

### Editable Cell Pattern

```typescript
const EditableCell = ({
  getValue,
  row,
  column,
  table,
}: CellContext<Student, unknown>) => {
  const initialValue = getValue();
  const [value, setValue] = useState(initialValue);

  const onBlur = () => {
    table.options.meta?.updateData(row.index, column.id, value);
  };

  useEffect(() => {
    setValue(initialValue);
  }, [initialValue]);

  return (
    <input
      value={value as string}
      onChange={(e) => setValue(e.target.value)}
      onBlur={onBlur}
    />
  );
};

const columns: ColumnDef<Student>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: EditableCell,
  },
];

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  meta: {
    updateData: (rowIndex: number, columnId: string, value: unknown) => {
      setData((old) =>
        old.map((row, index) => {
          if (index === rowIndex) {
            return {
              ...old[rowIndex],
              [columnId]: value,
            };
          }
          return row;
        })
      );
    },
  },
});
```

## Row Selection

```typescript
const [rowSelection, setRowSelection] = useState({});

const columns: ColumnDef<Student>[] = [
  {
    id: "select",
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
  state: {
    rowSelection,
  },
  onRowSelectionChange: setRowSelection,
  enableRowSelection: true,
});

// Get selected rows
const selectedRows = table.getSelectedRowModel().rows;
```

## Custom Cell Rendering

### Status Badge Cell

```typescript
{
  accessorKey: "status",
  header: "Status",
  cell: ({ row }) => {
    const status = row.getValue("status");
    return (
      <span className={
        status === "active"
          ? "bg-green-100 text-green-800 px-2 py-1 rounded"
          : "bg-gray-100 text-gray-800 px-2 py-1 rounded"
      }>
        {status}
      </span>
    );
  },
}
```

### Action Buttons Cell

```typescript
{
  id: "actions",
  header: "Actions",
  cell: ({ row }) => (
    <div className="flex gap-2">
      <button
        onClick={() => handleEdit(row.original)}
        className="text-blue-600 hover:text-blue-800"
      >
        Edit
      </button>
      <button
        onClick={() => handleDelete(row.original.id)}
        className="text-red-600 hover:text-red-800"
      >
        Delete
      </button>
    </div>
  ),
}
```

### Nested Object Access

```typescript
{
  accessorFn: (row) => row.student.name,
  id: "studentName",
  header: "Student Name",
  cell: (info) => info.getValue(),
}
```

## Column Visibility

```typescript
const [columnVisibility, setColumnVisibility] = useState({});

const table = useReactTable({
  data,
  columns,
  state: {
    columnVisibility,
  },
  onColumnVisibilityChange: setColumnVisibility,
});

// Toggle UI
<div>
  {table.getAllColumns().map((column) => (
    <label key={column.id}>
      <input
        type="checkbox"
        checked={column.getIsVisible()}
        onChange={column.getToggleVisibilityHandler()}
      />
      {column.id}
    </label>
  ))}
</div>
```

## Advanced Patterns

### Loading State

```typescript
function MyTable() {
  const { data, isLoading } = useQuery({
    queryKey: ["students"],
    queryFn: fetchStudents,
  });

  const table = useReactTable({
    data: data?.students ?? [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return <table>{/* ... */}</table>;
}
```

### Empty State

```typescript
{table.getRowModel().rows.length === 0 ? (
  <tr>
    <td colSpan={columns.length} className="text-center py-8">
      No data available
    </td>
  </tr>
) : (
  table.getRowModel().rows.map((row) => (
    // ... row rendering
  ))
)}
```

### Sticky Headers

```typescript
<thead className="sticky top-0 bg-white z-10">
  {/* Header rows */}
</thead>
```

### Responsive Tables

```typescript
<div className="overflow-x-auto">
  <table className="min-w-full">
    {/* Table content */}
  </table>
</div>
```

## Performance Optimization

### Memoize Columns

```typescript
const columns = useMemo<ColumnDef<Student>[]>(
  () => [
    {
      accessorKey: "name",
      header: "Name",
    },
    // ... more columns
  ],
  []
);
```

### Virtualization for Large Datasets

```typescript
import { useVirtualizer } from "@tanstack/react-virtual";

const rowVirtualizer = useVirtualizer({
  count: table.getRowModel().rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 35,
});
```

## Styling with Tailwind

```typescript
<table className="min-w-full divide-y divide-gray-200">
  <thead className="bg-gray-50">
    <tr>
      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
        Header
      </th>
    </tr>
  </thead>
  <tbody className="bg-white divide-y divide-gray-200">
    <tr className="hover:bg-gray-50">
      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
        Cell
      </td>
    </tr>
  </tbody>
</table>
```

## Common Patterns

### CRUD Table with Mutations

```typescript
function StudentTable() {
  const { data } = useStudentsQuery();
  const updateMutation = useUpdateStudentMutation();
  const deleteMutation = useDeleteStudentMutation();

  const columns = useMemo<ColumnDef<Student>[]>(
    () => [
      { accessorKey: "name", header: "Name" },
      {
        id: "actions",
        cell: ({ row }) => (
          <>
            <button onClick={() => updateMutation.mutate(row.original)}>
              Edit
            </button>
            <button onClick={() => deleteMutation.mutate(row.original.id)}>
              Delete
            </button>
          </>
        ),
      },
    ],
    [updateMutation, deleteMutation]
  );

  // ... table setup
}
```

## Integration with Other Skills

- For overall architecture → Use `architecture` skill
- For backend data fetching → Use `data-flow` skill
- For styling and components → Use `component-system` skill
- For implementation process → Use `workflows` skill
