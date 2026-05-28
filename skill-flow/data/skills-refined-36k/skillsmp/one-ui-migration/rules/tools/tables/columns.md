# Table Migration - Column Configuration

## TableColumn API

```typescript
type TableColumn<R = any> = {
  key: string; // Column key (must match data property)
  header?: string; // Column header text
  sticky?: boolean; // Stick to left
  stickyEnd?: boolean; // Stick to right
  disabled?: boolean; // Disable sorting
  tooltip?: string; // Header tooltip
  visible?: boolean; // Show/hide column
  width?: string; // Column width
  noAutoGenerate?: boolean; // Use custom template
  filter?: (data: R, filter: string) => boolean; // Custom filter
  sort?: (data: R, sortId: string) => string | number; // Custom sort
  disable?: (data: R) => boolean; // Disable row action
  rowTooltip?: (data: R) => string; // Row tooltip
  rowTooltipDisable?: (data: R) => boolean; // Disable row tooltip
};

// Special column keys
const SELECT_COLUMN_KEY = '_select'; // Checkbox column
const EDIT_COLUMN_KEY = '_edit'; // Edit button column
const EXPAND_COLUMN_KEY = '_expand'; // Expand button column
```

---

## Enable/Status Column with MxStatus

When displaying enable/disable or status columns, use `MxStatusComponent` instead of plain text with CSS classes:

**Component TypeScript:**

```typescript
import { MxStatusComponent } from '@moxa/formoxa/mx-status';

@Component({
  imports: [
    CommonTableComponent,
    MxStatusComponent,  // ✅ Required for status display
    // ... other imports
  ]
})
```

**Template:**

```html
<ng-template #tableColumnsTemplate>
  <ng-container matColumnDef="enable">
    <th *matHeaderCellDef mat-header-cell mat-sort-header>{{ t('general.common.status') }}</th>
    <td *matCellDef="let row" mat-cell>
      @if (row.enableRaw === 1) {
      <mx-status statusType="success" statusIcon="icon:task_alt" [statusText]="t('general.common.enable')" />
      } @else {
      <mx-status statusType="neutral" statusIcon="icon:hide_source" [statusText]="t('general.common.disable')" />
      }
    </td>
  </ng-container>
</ng-template>
```

**MxStatus Props:**

| Prop         | Values                                    | Description                  |
| ------------ | ----------------------------------------- | ---------------------------- |
| `statusType` | `success`, `warning`, `error`, `neutral`  | Status color theme           |
| `statusIcon` | `icon:task_alt`, `icon:hide_source`, etc. | SVG icon name                |
| `statusText` | string                                    | Display text (use transloco) |

**Don't use plain text with CSS classes:**

```html
<!-- ❌ Incorrect: Plain text with CSS class -->
<td mat-cell [class]="row.enableClass">{{ row.enable }}</td>

<!-- ✅ Correct: Use MxStatusComponent -->
<td mat-cell>
  @if (row.enableRaw === 1) {
  <mx-status statusType="success" ... />
  } @else {
  <mx-status statusType="neutral" ... />
  }
</td>
```

---

## Custom Template Columns: noAutoGenerate and filter

When a column uses a custom template (via `#tableColumnsTemplate`), you **MUST**:

1. Set `noAutoGenerate: true` in the column configuration
2. Provide a custom `filter` function if the table has search functionality
3. **Import `MatTableModule` and `MatSortModule`** for the template directives to work

### Required Imports for Custom Column Templates

> ⚠️ **CRITICAL**: `CommonTableComponent` does NOT handle external template directives. You MUST import these modules in components that have `#tableColumnsTemplate`.

| Directives Used in Template                        | Required Module  |
| -------------------------------------------------- | ---------------- |
| `matColumnDef`, `*matHeaderCellDef`, `*matCellDef` | `MatTableModule` |
| `mat-sort-header`                                  | `MatSortModule`  |

```typescript
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';

@Component({
  imports: [
    CommonTableComponent,
    MatSortModule,   // ✅ Required for mat-sort-header in custom columns
    MatTableModule,  // ✅ Required for matColumnDef, *matHeaderCellDef, *matCellDef
    // ... other imports
  ]
})
```

**Common Error Message:**

```
A structural directive `matHeaderCellDef` was used in the template without a corresponding import in the component.
```

**Solution:** Add `MatTableModule` and `MatSortModule` imports to the component.

### Component TypeScript

```typescript
readonly columns: Signal<TableColumn<AccountTableDataItem>[]> = computed(() => {
  this.#langChanged();
  return [
    {
      key: SELECT_COLUMN_KEY,
      disable: (row: AccountTableDataItem) => row.loginOn
    },
    {
      key: 'enable',
      header: this.#transloco.translate('general.common.status'),
      noAutoGenerate: true,  // ✅ Required for custom template columns
      filter: (data: AccountTableDataItem, filter: string) => {
        // ✅ Custom filter for translated status text
        const searchText = filter.trim().toLowerCase();
        if (!searchText) {
          return true;
        }

        const enableStatus = data.enableRaw === 1
          ? this.#transloco.translate('general.common.enable')
          : this.#transloco.translate('general.common.disable');

        return enableStatus.toLowerCase().includes(searchText);
      }
    },
    {
      key: 'username',
      header: this.#transloco.translate('general.common_account.username')
    }
    // ... other columns
  ];
});
```

### Why is this important?

| Property         | Purpose                                              | When to Use                                                                              |
| ---------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `noAutoGenerate` | Tells the table to skip auto-generating cell content | Any column with custom `<ng-template>` in `#tableColumnsTemplate`                        |
| `filter`         | Custom search/filter logic for the column            | When the displayed text differs from raw data (e.g., translated status, formatted dates) |

### Common Mistakes

```typescript
// ❌ Incorrect: Missing noAutoGenerate for custom template column
{
  key: 'enable',
  header: this.#transloco.translate('general.common.status')
}

// ❌ Incorrect: Filtering on raw data instead of displayed text
{
  key: 'enable',
  noAutoGenerate: true,
  filter: (data, filter) => data.enableRaw.toString().includes(filter)  // Wrong!
}

// ✅ Correct: Filter on translated text that user sees
{
  key: 'enable',
  noAutoGenerate: true,
  filter: (data: AccountTableDataItem, filter: string) => {
    const searchText = filter.trim().toLowerCase();
    if (!searchText) { return true; }

    const enableStatus = data.enableRaw === 1
      ? this.#transloco.translate('general.common.enable')
      : this.#transloco.translate('general.common.disable');

    return enableStatus.toLowerCase().includes(searchText);
  }
}
```

---

## Edit Column with stickyEnd

When using the `editable` attribute on `<one-ui-common-table>`, you **MUST** add the `EDIT_COLUMN_KEY` to your columns array with `stickyEnd: true` to keep the edit button visible when scrolling horizontally.

**Component TypeScript:**

```typescript
import { EDIT_COLUMN_KEY, SELECT_COLUMN_KEY, type TableColumn } from '@one-ui/shared/domain';

readonly columns: Signal<TableColumn<AccountTableDataItem>[]> = computed(() => {
  return [
    {
      key: SELECT_COLUMN_KEY,
      disable: (row: AccountTableDataItem) => row.loginOn
    },
    {
      key: 'username',
      header: this.#transloco.translate('general.common_account.username')
    },
    // ... other columns
    {
      key: EDIT_COLUMN_KEY,
      stickyEnd: true  // ✅ Keep edit button visible on horizontal scroll
    }
  ];
});
```

**Template:**

```html
<one-ui-common-table
  *transloco="let t"
  selectable
  editable      <!-- ✅ Enable edit button -->
  [data]="tableData()"
  [columns]="columns()"
  (edit)="editAccount.emit($event)"
>
```

**Why `stickyEnd: true`?**

- Keeps the edit button column fixed to the right side of the table
- Ensures edit functionality is always accessible even with many columns
- Provides better UX for tables with horizontal scroll

---

## Action Column with #actionTemplate

When adding a custom action button (like re-auth, delete, etc.) besides the built-in edit button, use `#actionTemplate`.

### What `#actionTemplate` provides automatically:

- `stickyEnd` - Column sticks to the right
- `mxTableThIsAction` - Proper header styling
- `width: 1%` - Minimal column width (shrink to fit icon)
- Column position before edit button (edit is always rightmost)

### Component TypeScript

```typescript
import { EDIT_COLUMN_KEY, type TableColumn } from '@one-ui/shared/domain';
import { CommonTableComponent } from '@one-ui/shared/ui/table';

@Component({
  imports: [
    CommonTableComponent,
    MatIconModule,
    MatTooltipModule
    // ... other imports
  ]
})
export class MyTableComponent {
  readonly noPermission = input<boolean>(false);

  // ✅ No need to define action column - just define your data columns
  readonly columns: Signal<TableColumn<MyData>[]> = computed(() => {
    return [
      { key: 'name', header: 'Name' },
      { key: 'status', header: 'Status', noAutoGenerate: true },
      {
        key: EDIT_COLUMN_KEY,
        stickyEnd: true,
        disable: () => this.noPermission()
      }
    ];
  });

  onReauth(row: MyData) {
    // Handle reauth action
  }
}
```

### Template

```html
<one-ui-common-table *transloco="let t" editable [data]="tableData()" [columns]="columns()" (edit)="onEdit($event)">
  <!-- Action Column: Just provide #actionTemplate -->
  <ng-template #actionTemplate let-row>
    <mat-icon
      svgIcon="icon:task_alt"
      [matTooltip]="t('tooltip.reauth')"
      [matTooltipDisabled]="noPermission() || row.enable !== 1"
      (click)="!(noPermission() || row.enable !== 1) && onReauth(row)"
    />
  </ng-template>

  <!-- Other custom columns still use #tableColumnsTemplate -->
  <ng-template #tableColumnsTemplate>
    <ng-container matColumnDef="status">
      <th *matHeaderCellDef mat-header-cell>{{ t('status') }}</th>
      <td *matCellDef="let row" mat-cell>
        <mx-status ... />
      </td>
    </ng-container>
  </ng-template>
</one-ui-common-table>
```

### Column Order

The columns are displayed in this order:

1. Expand column (if expandable)
2. Select column (if selectable)
3. User-defined columns
4. **Action column** (if `#actionTemplate` exists)
5. **Edit column** (always rightmost, if editable)

### Comparison: Before vs After

**Before (manual column definition):**

```typescript
// ❌ Verbose: Need to define action column in columns array
columns = [
  { key: 'name', header: 'Name' },
  { key: 'reauth', header: '', noAutoGenerate: true }, // Extra definition needed
  { key: EDIT_COLUMN_KEY, stickyEnd: true }
];
```

```html
<!-- ❌ Verbose: Manual stickyEnd, mxTableThIsAction, width -->
<ng-template #tableColumnsTemplate>
  <ng-container matColumnDef="reauth" stickyEnd>
    <th *matHeaderCellDef mat-header-cell mxTableThIsAction></th>
    <td *matCellDef="let row" mat-cell style="width: 1%">
      <mat-icon ... />
    </td>
  </ng-container>
</ng-template>
```

**After (with #actionTemplate):**

```typescript
// ✅ Clean: No action column definition needed
columns = [
  { key: 'name', header: 'Name' },
  { key: EDIT_COLUMN_KEY, stickyEnd: true }
];
```

```html
<!-- ✅ Clean: Just provide content -->
<ng-template #actionTemplate let-row>
  <mat-icon ... />
</ng-template>
```

### When to use each approach

| Scenario                                     | Use                                              |
| -------------------------------------------- | ------------------------------------------------ |
| Action button (icon only, no header)         | `#actionTemplate`                                |
| Custom data display (status, formatted text) | `noAutoGenerate: true` + `#tableColumnsTemplate` |
| Built-in edit button                         | `EDIT_COLUMN_KEY` with `stickyEnd: true`         |
| Built-in checkbox selection                  | `SELECT_COLUMN_KEY`                              |

---

## Pagination Control

When you need to hide or disable pagination features, use these attributes on `<one-ui-common-table>`:

### Available Attributes

| Attribute            | Type      | Default | Description                              |
| -------------------- | --------- | ------- | ---------------------------------------- |
| `showTablePagination`| `boolean` | `true`  | Show/hide entire pagination bar          |
| `disableChangePage`  | `boolean` | `false` | Disable page navigation (prev/next)      |
| `hidePageSize`       | `boolean` | `false` | Hide page size selector dropdown         |
| `pageSize`           | `number`  | `50`    | Items per page                           |
| `pageSizeOptions`    | `number[]`| `[50, 100, 200, 1000]` | Page size options    |

### Usage Examples

**Hide pagination completely:**

```html
<one-ui-common-table
  [showTablePagination]="false"
  [data]="tableData()"
  [columns]="columns()"
>
```

**Show pagination bar but disable navigation and hide page size:**

```html
<one-ui-common-table
  [disableChangePage]="true"
  [hidePageSize]="true"
  [data]="tableData()"
  [columns]="columns()"
>
```

**Common use cases:**

| Scenario                              | Attributes                                     |
| ------------------------------------- | ---------------------------------------------- |
| Small fixed-size table (e.g., ≤20 items) | `[showTablePagination]="false"`             |
| Show count only, no navigation        | `[disableChangePage]="true" [hidePageSize]="true"` |
| Custom page size                      | `[pageSize]="20" [pageSizeOptions]="[10, 20, 50]"` |
