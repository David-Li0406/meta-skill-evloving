# Guide: Creating a Table

## Overview

Create a data table with selection, editing, search, and sorting features.

## Required Tools

| Tool | Purpose |
|------|---------|
| [common-table](../tools/common-table.md) | Table component |
| [transloco](../tools/transloco.md) | Column header translation |
| [mx-components](../tools/mx-components.md) | MxStatus for status display |

---

## Steps

### 1. Create Table Component (UI Layer)

```typescript
// ui/feature-table/feature-table.component.ts
@Component({
  selector: 'one-ui-feature-table',
  imports: [
    CommonTableComponent,
    TranslocoModule,
    MatButtonModule,
    MatSortModule,
    MatTableModule,
    MxStatusComponent,
    oneUiTableMaxSizeDirective
  ],
  templateUrl: './feature-table.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeatureTableComponent {
  readonly #transloco = inject(TranslocoService);

  // Inputs - Do NOT inject Store!
  tableData = input.required<Item[]>();
  tableMaxSize = input.required<number>();
  loading = input<boolean>(false);

  // Outputs
  add = output<void>();
  edit = output<Item>();
  delete = output<string[]>();
  refresh = output<void>();

  selection: Item[] = [];

  readonly columns = computed(() => [
    {
      key: SELECT_COLUMN_KEY,
      disable: (row) => row.isCurrentUser
    },
    { key: 'name', header: this.#transloco.translate('general.common.name') },
    {
      key: 'status',
      header: this.#transloco.translate('general.common.status'),
      noAutoGenerate: true,
      filter: (data, filter) => {
        const status = data.enabled
          ? this.#transloco.translate('general.common.enable')
          : this.#transloco.translate('general.common.disable');
        return status.toLowerCase().includes(filter.toLowerCase());
      }
    },
    { key: EDIT_COLUMN_KEY, stickyEnd: true }
  ]);

  onDelete() {
    const ids = this.selection.map(item => item.id);
    this.delete.emit(ids);
  }
}
```

### 2. Create Table Template

```html
<!-- feature-table.component.html -->
<one-ui-common-table
  *transloco="let t"
  headerSticky selectable editable
  [data]="tableData()" [columns]="columns()" [loading]="loading()"
  (edit)="edit.emit($event)" (select)="selection = $event"
>
  <!-- Toolbar: Refresh → Create → Delete order -->
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

  <!-- Custom columns -->
  <ng-template #tableColumnsTemplate>
    <ng-container matColumnDef="status">
      <th *matHeaderCellDef mat-header-cell mat-sort-header>
        {{ t('general.common.status') }}
      </th>
      <td *matCellDef="let row" mat-cell>
        @if (row.enabled) {
          <mx-status statusType="success" statusIcon="icon:task_alt" [statusText]="t('general.common.enable')" />
        } @else {
          <mx-status statusType="neutral" statusIcon="icon:hide_source" [statusText]="t('general.common.disable')" />
        }
      </td>
    </ng-container>
  </ng-template>

  <!-- Footer -->
  <ng-template #tableFooterTemplate>
    <span oneUiTableMaxSize>{{ t('general.table_function.limit_count') }} {{ tableMaxSize() }}</span>
  </ng-template>
</one-ui-common-table>
```

### 3. Use in Page

```typescript
// features/feature-page.component.ts
<one-ui-feature-table
  [tableData]="items()"
  [tableMaxSize]="tableMaxSize()"
  [loading]="loading()"
  (add)="openCreateDialog()"
  (edit)="openEditDialog($event)"
  (delete)="onDelete($event)"
  (refresh)="store.loadItems()"
/>
```

---

## Custom Column Notes

1. Set `noAutoGenerate: true`
2. Provide `filter` function (otherwise search won't work)
3. Import `MatSortModule` (otherwise `mat-sort-header` won't work)

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

## Checklist

- [ ] Table is in UI Layer (does not inject Store)
- [ ] Uses `input()` / `output()`
- [ ] Toolbar order: Refresh → Create → Delete
- [ ] Custom columns have `filter` function
- [ ] Import `MatSortModule`
- [ ] Long text uses `gl-ellipsis-text` + `mxAutoTooltip`
