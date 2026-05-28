# Component Patterns

## Table of Contents

1. [One Component, One Responsibility](#one-component-one-responsibility)
2. [Headless Components](#headless-components)
3. [Container/Presenter Pattern](#containerpresenter-pattern)
4. [Composition Over Configuration](#composition-over-configuration)
5. [UI Component Rules](#ui-component-rules)

---

## One Component, One Responsibility

Each unit must do exactly one job clearly.

- **Containers**: fetch/derive/manage remote state → no markup complexity
- **Presenters**: render UI → no queries/mutations/side effects
- **Custom hooks**: encapsulate reusable logic → no JSX
- A UI component must never validate schema logic or fetch data

> Predictable code is easy to debug, test, reuse, and delete.

---

## Headless Components

Build components that separate logic from presentation.

See [headless-components.md](headless-components.md) for comprehensive guidance on implementing headless components with Radix-style composition.

---

## Container/Presenter Pattern

Keep stateful logic (data fetching, auth, feature flags) in a container, and make the presentational component dumb, token-driven, and storybooked. Avoid large components with nested rendering functions.

### Example Implementation

```tsx
// Container: owns data fetching, retries, and access checks
export function RevenueCardContainer() {
  const { data, error, isLoading } = useRevenue()

  if (isLoading) return <RevenueCardView state="loading" />
  if (error) return <RevenueCardView state="error" message="Revenue unavailable" />
  if (!data || data.value === 0) return <RevenueCardView state="empty" message="No revenue yet" />

  return <RevenueCardView state="ready" value={data.value} previousValue={data.previousValue} />
}

// Presentational: pure UI, tokens only
export function RevenueCardView({ state, value, previousValue, message }: RevenueCardViewProps) {
  if (state === 'loading') return <MetricCard loading label="Revenue" />
  if (state === 'error') return <MetricCard label="Revenue" error message={message} />
  if (state === 'empty') return <MetricCard label="Revenue" empty message={message} />

  return (
    <MetricCard label="Revenue" value={value} previousValue={previousValue} format="currency" />
  )
}
```

### Storybook Contract

Capture the four canonical states—loading, empty, error, ready—do not invent new ones.

```tsx
// RevenueCardView.stories.tsx
export const Loading = { args: { state: 'loading' } }
export const Empty = { args: { state: 'empty', message: 'No revenue yet' } }
export const Error = { args: { state: 'error', message: 'Revenue unavailable' } }
export const Ready = { args: { state: 'ready', value: 124500, previousValue: 110600 } }

// Playground: single canvas to view all states side by side
export const Playground = {
  render: () => (
    <div className="grid gap-4 md:grid-cols-2">
      <RevenueCardView state="loading" />
      <RevenueCardView state="empty" message="No revenue yet" />
      <RevenueCardView state="error" message="Revenue unavailable" />
      <RevenueCardView state="ready" value={124500} previousValue={110600} />
    </div>
  ),
}
```

> To learn how to mock the API requests needed for container component stories and write interactive tests, see the [Advanced Storybook Guide](references/advanced-storybook.md).

Containers stay thin and easy to regenerate. Presentational pieces stay consistent, testable, and visualized.

---

## Composition Over Configuration

### No God Components

Do not create components with endless props:

```tsx
// DO NOT DO THIS
<DataTable
  data={transactions}
  columns={columns}
  pagination={true}
  paginationPosition="bottom"
  pageSize={10}
  pageSizeOptions={[10, 25, 50]}
  sortable={true}
  defaultSortColumn="date"
  defaultSortDirection="desc"
  filterable={true}
  filterPosition="header"
  filterDebounce={300}
  selectable={true}
  selectionMode="multiple"
  onSelectionChange={handleSelection}
  expandable={true}
  expandedRowRender={renderExpandedRow}
  loading={isLoading}
  loadingComponent={<CustomLoader />}
  emptyState={<EmptyTransactions />}
  rowActions={rowActions}
  rowActionsPosition="end"
  headerSticky={true}
  stickyOffset={64}
  virtualized={true}
  rowHeight={52}
  overscan={5}
/>
```

Nobody can reason about 60 props and their interactions.

### Use Composition Instead

Build complex interfaces from focused, single-purpose pieces:

```tsx
// Each piece does one thing well
<DataTable data={transactions} columns={columns}>
  <DataTableToolbar>
    <DataTableFilter column="status" options={statusOptions} placeholder="Filter by status" />
    <DataTableFilter column="type" options={typeOptions} placeholder="Filter by type" />
    <DataTableSearch placeholder="Search transactions..." />
    <DataTableViewOptions />
  </DataTableToolbar>

  <DataTableHeader sticky offset={64} />

  <DataTableBody
    loading={isLoading}
    emptyState={<EmptyTransactions />}
    expandedRow={row => <TransactionDetails transaction={row} />}
  />

  <DataTableFooter>
    <DataTableSelection mode="multiple" onSelectionChange={handleSelection} />
    <DataTablePagination pageSize={10} pageSizeOptions={[10, 25, 50]} />
  </DataTableFooter>
</DataTable>
```

Each piece has a clear purpose. When requirements change you reorganize JSX rather than hunting through props.

This principle scales to every complex component:

- **Forms**: FormField, FormLabel, FormControl, FormMessage
- **Dialogs**: DialogTrigger, DialogContent, DialogHeader, DialogFooter
- **Navigation**: NavRoot, NavList, NavItem, NavLink

Small pieces, clearly named, easy to learn.

---

## UI Component Rules

- Always import UI from `components/ui`
- UI sources must follow priority:
  1. **Radix UI**
  2. **shadcn-ui**
  3. **Composition of existing components**
  4. **New components as a last resort**
- Never introduce additional UI libraries
