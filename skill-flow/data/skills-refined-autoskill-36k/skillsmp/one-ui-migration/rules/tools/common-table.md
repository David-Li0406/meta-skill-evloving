# CommonTableComponent

## What is this?

One-UI shared table component with selection, editing, search, and sorting features.

## When to use

When displaying CRUD lists.

## Import

```typescript
import { CommonTableComponent, SELECT_COLUMN_KEY, EDIT_COLUMN_KEY, oneUiTableMaxSizeDirective } from '@one-ui/shared/ui';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
```

---

## Basic Usage

```html
<one-ui-common-table
  *transloco="let t"
  headerSticky selectable editable
  [data]="tableData()" [columns]="columns()" [loading]="loading()"
  (edit)="edit.emit($event)" (select)="selection = $event"
>
  <ng-template #rightToolbarTemplate>
    <!-- Toolbar buttons -->
  </ng-template>
</one-ui-common-table>
```

---

## Features

| Feature | Type | Description |
|---------|------|-------------|
| `selectable` | boolean | Multi-select checkbox |
| `editable` | boolean | Edit button column |
| `searchable` | boolean | Search functionality |
| `headerSticky` | boolean | Fixed header |
| `expandable` | boolean | Expandable rows |
| `loading` | boolean | Loading state |

---

## Column Definition

```typescript
readonly columns = computed(() => [
  {
    key: SELECT_COLUMN_KEY,
    disable: (row) => row.isCurrentUser  // Disable selection
  },
  { key: 'name', header: this.#transloco.translate('general.common.name') },
  {
    key: 'status',
    header: this.#transloco.translate('general.common.status'),
    noAutoGenerate: true,  // Use custom template
    filter: (data, filter) => {
      const status = data.enabled ? 'Enabled' : 'Disabled';
      return status.toLowerCase().includes(filter.toLowerCase());
    }
  },
  { key: EDIT_COLUMN_KEY, stickyEnd: true }
]);
```

### Column API

| Property | Type | Description |
|----------|------|-------------|
| `key` | string | Column key (must match data property) |
| `header` | string | Column header |
| `stickyEnd` | boolean | Stick to right side |
| `noAutoGenerate` | boolean | Use custom template |
| `filter` | function | Custom search filter |
| `disable` | function | Disable row operations |

---

## Custom Column Template

```html
<ng-template #tableColumnsTemplate>
  <ng-container matColumnDef="status">
    <th *matHeaderCellDef mat-header-cell mat-sort-header>Status</th>
    <td *matCellDef="let row" mat-cell>
      <mx-status [statusType]="row.enabled ? 'success' : 'neutral'" />
    </td>
  </ng-container>
</ng-template>
```

⚠️ When using custom columns, you must import `MatSortModule`.

---

## Toolbar Button Order

**Fixed order**: Refresh → Create → Delete

```html
<ng-template #rightToolbarTemplate>
  <button mat-button (click)="refresh.emit()">
    <mat-icon svgIcon="icon:refresh"></mat-icon>
    {{ t('general.tooltip.refresh') }}
  </button>
  @if (selection.length === 0) {
    <button mat-stroked-button (click)="add.emit()">{{ t('general.button.create') }}</button>
  }
  @if (selection.length >= 1) {
    <button mat-stroked-button (click)="onDelete()">{{ t('general.button.delete') }}</button>
  }
</ng-template>
```

---

## Text Overflow Handling

```html
<td mat-cell *matCellDef="let row">
  <span class="gl-ellipsis-text" mxAutoTooltip [matTooltip]="row.description">
    {{ row.description }}
  </span>
</td>
```

```scss
.mat-column-description {
  min-width: 300px;
  max-width: 300px;
}
```

---

## Table Footer (oneUiTableMaxSize)

Display max item count in table footer.

```typescript
import { oneUiTableMaxSizeDirective } from '@one-ui/shared/ui';
```

```html
<one-ui-common-table ...>
  <!-- ... other templates ... -->

  <ng-template #tableFooterTemplate>
    <span oneUiTableMaxSize>{{ t('general.table_function.limit_count') }} {{ tableMaxSize() }}</span>
  </ng-template>
</one-ui-common-table>
```

In component:
```typescript
tableMaxSize = input.required<number>();  // Pass from store or config
```

---

## Common Mistakes

```typescript
// ❌ WRONG: Custom column missing filter function
{
  key: 'status',
  noAutoGenerate: true
  // Search won't work on this column
}

// ✅ CORRECT: Provide filter function
{
  key: 'status',
  noAutoGenerate: true,
  filter: (data, filter) => {
    const status = data.enabled ? 'Enabled' : 'Disabled';
    return status.toLowerCase().includes(filter.toLowerCase());
  }
}

// ❌ WRONG: Missing MatSortModule
@Component({
  imports: [CommonTableComponent, MatTableModule]  // mat-sort-header won't work
})

// ✅ CORRECT: Include MatSortModule
@Component({
  imports: [CommonTableComponent, MatTableModule, MatSortModule]
})
```

---

## Related Tools

- [transloco.md](./transloco.md) - Table header translation
- [mx-components.md](./mx-components.md) - MxStatus component
