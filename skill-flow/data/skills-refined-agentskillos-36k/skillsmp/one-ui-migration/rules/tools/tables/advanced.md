# MXsecurity Table Migration - Advanced Features

## Table Footer Styling

When using `#tableFooterTemplate` with table max size display, you **MUST** import and apply the `oneUiTableMaxSizeDirective`:

**Component TypeScript:**

```typescript
import { oneUiTableMaxSizeDirective } from '@one-ui/mxsecurity/shared/domain';

@Component({
  imports: [
    CommonTableComponent,
    // ... other imports
    oneUiTableMaxSizeDirective  // ✅ Required for footer styling
  ]
})
```

**Template:**

```html
<ng-template #tableFooterTemplate>
  <!-- ✅ Add oneUiTableMaxSize directive to the span -->
  <span oneUiTableMaxSize>{{ t('general.table_function.limit_count') }} {{ tableMaxSize() }}</span>
</ng-template>
```

The directive applies the following styles to the footer:

- Flex layout with space-between
- Proper padding and alignment
- Text styling classes (`text-on-surface-variant`, `gl-body-sm`)

---

## Hardcode tableMaxSize in Template

For simple tables where `tableMaxSize` is a static value, **hardcode it directly in the template** instead of passing it through the store.

### ❌ Don't do this (over-engineered)

```typescript
// arp-page.def.ts - Unnecessary file
export const ARP_PAGE_DEFAULTS = {
  TABLE_MAX_SIZE: 1024
} as const;

// arp-page.store.ts - Unnecessary computed
withComputed((state) => ({
  tableData: computed(() => state.arpEntries()),
  tableMaxSize: computed(() => ARP_PAGE_DEFAULTS.TABLE_MAX_SIZE)  // ❌ Over-engineered
}))

// arp-table.component.ts - Unnecessary input
readonly tableMaxSize = input.required<number>();  // ❌ Over-engineered

// arp-page.component.html - Unnecessary binding
<one-ui-arp-table [tableData]="tableData()" [tableMaxSize]="tableMaxSize()" />  // ❌ Over-engineered
```

### ✅ Do this instead (simple and direct)

```typescript
// arp-page.store.ts - Clean store
withComputed((state) => ({
  tableData: computed(() => state.arpEntries())
  // No tableMaxSize needed
}))

// arp-table.component.ts - No tableMaxSize input needed
readonly tableData = input.required<ArpTableDataItem[]>();
// No tableMaxSize input

// arp-page.component.html - Clean binding
<one-ui-arp-table [tableData]="tableData()" (refresh)="onRefresh()" />
```

```html
<!-- arp-table.component.html - Hardcode the value directly -->
<ng-template #tableFooterTemplate>
  <span oneUiTableMaxSize>{{ t('general.table_function.limit_count') }} 1024</span>
</ng-template>
```

### When to hardcode vs pass as input

| Scenario                                                 | Approach                |
| -------------------------------------------------------- | ----------------------- |
| Static value that never changes                          | ✅ Hardcode in template |
| Value from API response                                  | Pass as input           |
| Value that varies by configuration                       | Pass as input           |
| Value used in business logic (e.g., `isExceedTableSize`) | Pass as input           |

---

## CRITICAL: Paginator Configuration

**If the old system's table does NOT have page change or page size functionality, you MUST disable these in the new table:**

```html
<one-ui-common-table
  *transloco="let t"
  headerSticky
  selectable
  [data]="tableData()"
  [columns]="columns()"
  [disableChangePage]="true"
  [hidePageSize]="true"
  (select)="select($event)"
></one-ui-common-table>
```

| Property              | Default | Description                                   |
| --------------------- | ------- | --------------------------------------------- |
| `[disableChangePage]` | `false` | Hides the page navigation buttons (< 1 2 3 >) |
| `[hidePageSize]`      | `false` | Hides the "Items per page" dropdown           |

### How to Determine

Check the old system's paginator configuration:

```html
<!-- Old system with full paginator (keep defaults) -->
<mat-paginator [pageSizeOptions]="[10, 20, 50]" showFirstLastButtons></mat-paginator>

<!-- Old system with limited paginator (add disableChangePage/hidePageSize) -->
<mat-paginator [pageSize]="10"></mat-paginator>
<!-- or no paginator at all -->
```

### Example: Simple Table with Fixed Page Size

```html
<!-- ✅ Correct: Old system had no page change/size options -->
<one-ui-common-table
  *transloco="let t"
  headerSticky
  selectable
  [data]="tableData()"
  [columns]="columns()"
  [disableChangePage]="true"
  [hidePageSize]="true"
  (select)="select($event)"
>
  <!-- ... templates ... -->
</one-ui-common-table>

<!-- ❌ Incorrect: Leaving paginator with full functionality when old system didn't have it -->
<one-ui-common-table [data]="tableData()" [columns]="columns()">
  <!-- Missing disableChangePage and hidePageSize -->
</one-ui-common-table>
```

**IMPORTANT:** Always check the old system's pagination behavior before migrating. The new table should match the old system's functionality exactly.

---

## Migration Checklist

- [ ] Create `TableDataItem` interface in domain layer
- [ ] Create `TableComponent` in UI layer
- [ ] Define columns using `TableColumn<TableDataItem>`
- [ ] Use `input()` for data and config
- [ ] Use `output()` for events (add, edit, delete, refresh)
- [ ] Implement toolbar templates (`#rightToolbarTemplate`)
- [ ] Add custom column templates if needed (e.g., status styling with `MxStatus`)
- [ ] Use `@one-ui/shared/ui` for `CommonTableComponent`
- [ ] Import `MatTableModule` and `MatSortModule` for custom column templates
- [ ] Set `noAutoGenerate: true` for custom template columns
- [ ] Add custom `filter` function for translated/formatted columns
- [ ] Add `EDIT_COLUMN_KEY` with `stickyEnd: true` if table is editable
- [ ] Import `oneUiTableMaxSizeDirective` for footer styling
- [ ] **Check old system's paginator** - add `[disableChangePage]` and `[hidePageSize]` if needed
- [ ] Test selection, sorting, pagination, search
