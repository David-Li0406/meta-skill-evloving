# MXsecurity Table Migration - Basics

## Comparison Analysis

### Old MXsecurity Account Table (Angular 16)

**Location**: `/Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/account`

**Features**:

- Uses `MatTableDataSource` with `MatSort` and `MatPaginator`
- Columns: select, edit, enable, username, authority, passwordExpire
- Uses `SelectionModel` for multi-selection
- Filter functionality with search input
- Responsive design (expansion panels for mobile)
- Business logic mixed in component (not DDD compliant)

**Issues**:

- ❌ Uses legacy Angular Material (`@angular/material/legacy-*`)
- ❌ Uses old `*ngIf`, `*ngFor` syntax
- ❌ Business logic in component (HTTP calls, data transformation)
- ❌ No separation of concerns

---

### Shared TableComponent (Target)

**Location**: `libs/shared/ui/src/lib/table/common-table.component.ts`

**Features**:
| Feature | Support | Notes |
|---------|---------|-------|
| Multi-selection | ✅ `selectable` | With checkbox, disabled per row |
| Edit button | ✅ `editable` | With disabled per row |
| Sorting | ✅ Built-in | MatSort integrated |
| Pagination | ✅ Built-in | MatPaginator integrated |
| Disable page change | ✅ `[disableChangePage]="true"` | Hide page navigation buttons |
| Hide page size | ✅ `[hidePageSize]="true"` | Hide "Items per page" dropdown |
| Search/Filter | ✅ `searchable` | With MxTableSearch |
| Sticky header | ✅ `headerSticky` | |
| Expandable rows | ✅ `expandable` | With detail template |
| Custom columns | ✅ `tableColumnsTemplate` | For custom rendering |
| Toolbar | ✅ `leftToolbarTemplate`, `rightToolbarTemplate` | For add/delete buttons |
| Footer | ✅ `tableFooterTemplate` | For max size display |
| Loading state | ✅ `loading` | |

---

## Conclusion: Can Use Shared TableComponent

The shared `CommonTableComponent` in `libs/shared/ui/src/lib/table` **CAN** be directly used for MXsecurity migration. It provides all required features.

---

## Table Title with leftToolbarTemplate

When a table needs a title (e.g., from legacy `<mat-card-title>`), use `#leftToolbarTemplate` with `mx-table__title` class:

```html
<one-ui-common-table searchable [data]="tableData()" [columns]="columns()">
  <ng-template #leftToolbarTemplate>
    <span class="mx-table__title">{{ t('features.xxx.table_title') }}</span>
  </ng-template>
</one-ui-common-table>
```

### Table Title with Auto-Refresh

For status tables that need title, time, and auto-refresh button:

```html
<one-ui-common-table searchable [data]="tableData()" [columns]="columns()">
  <ng-template #leftToolbarTemplate>
    <span class="mx-table__title">{{ t('features.xxx.table_title') }}</span>
  </ng-template>
  <ng-template #rightToolbarTemplate>
    <span class="update-time">{{ formattedTime() }}</span>
    <button
      mat-icon-button
      [matTooltip]="autoRefresh() ? t('general.tooltip.auto_refresh_enabled') : t('general.tooltip.auto_refresh_disabled')"
      (click)="onToggleAutoRefresh()"
    >
      <mat-icon [svgIcon]="autoRefresh() ? 'icon:sync_alt' : 'icon:sync_disabled'"></mat-icon>
    </button>
  </ng-template>
</one-ui-common-table>
```

**Component SCSS for update-time:**

```scss
.update-time {
  font-size: 14px;
  color: var(--mx-on-surface-variant);
}
```

**Legacy to New Mapping:**

| Legacy | New |
|--------|-----|
| `<mat-card-title>Title</mat-card-title>` | `<span class="mx-table__title">Title</span>` in `#leftToolbarTemplate` |
| Last update time in header | `<span class="update-time">` in `#rightToolbarTemplate` |
| Auto-refresh button in header | `mat-icon-button` in `#rightToolbarTemplate` |

---

## Table Toolbar Button Style

**Table toolbar buttons (Add/Delete) must use:**

- **Button type:** `mat-stroked-button` (outlined button)
- **Add button text:** `{{ t('general.button.create') }}`
- **Delete button text:** `{{ t('general.button.delete') }}`
- **No icons** - text only

```html
<!-- ✅ Correct: mat-stroked-button with text -->
<button mat-stroked-button [disabled]="isExceedTableSize()" (click)="addAccount.emit()">
  {{ t('general.button.create') }}
</button>

<button mat-stroked-button (click)="onDeleteAccount()">{{ t('general.button.delete') }}</button>

<!-- ❌ Incorrect: mat-button with icon -->
<button mat-button (click)="addAccount.emit()">
  <mat-icon svgIcon="icon:add"></mat-icon>
  {{ t('general.common_action.add') }}
</button>
```

---

## Migration Pattern

### Reference: MAF Account Settings Table

**Location**: `libs/maf/act-account/ui/src/lib/account-settings-table`

This is the pattern to follow:

```typescript
// account-table.component.ts (UI Layer)
@Component({
  selector: 'one-ui-account-table',
  imports: [CommonTableComponent, TranslocoModule, MatTooltipModule, MatButtonModule, MatIconModule],
  templateUrl: './account-table.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AccountTableComponent {
  // Inputs
  readonly tableData = input.required<AccountTableDataItem[]>();
  readonly tableMaxSize = input.required<number>();

  // Outputs
  addAccount = output<void>();
  editAccount = output<AccountTableDataItem>();
  deleteAccount = output<number[]>();

  // Internal state
  selection: AccountTableDataItem[] = [];

  // Columns definition
  readonly columns: Signal<TableColumn<AccountTableDataItem>[]> = computed(() => {
    return [
      {
        key: '_select',
        disable: (row) => row.isCurrentUser // Disable select for current user
      },
      {
        key: 'enable',
        header: this.transloco.translate('general.common.status')
      },
      {
        key: 'username',
        header: this.transloco.translate('general.common_account.username')
      },
      {
        key: 'authority',
        header: this.transloco.translate('general.common_account.authority')
      },
      {
        key: 'passwordExpire',
        header: this.transloco.translate('features.account_management.password_expire')
      }
    ];
  });

  readonly isExceedTableSize = computed(() => {
    return this.tableData().length >= this.tableMaxSize();
  });

  select(data: AccountTableDataItem[]) {
    this.selection = data;
  }

  onDeleteAccount() {
    this.deleteAccount.emit(this.selection.map((item) => item.key));
  }
}
```

### Template Pattern

```html
<!-- account-table.component.html -->
<one-ui-common-table
  *transloco="let t"
  headerSticky
  selectable
  editable
  [data]="tableData()"
  [columns]="columns()"
  (edit)="editAccount.emit($event)"
  (select)="select($event)"
>
  <!-- Right Toolbar: Add/Delete buttons -->
  <ng-template #rightToolbarTemplate>
    @if (selection.length === 0) {
    <span
      [matTooltip]="t('features.account_management.rule_size_limitation', { size: tableMaxSize() })"
      [matTooltipDisabled]="!isExceedTableSize()"
    >
      <button mat-stroked-button [disabled]="isExceedTableSize()" (click)="addAccount.emit()">
        {{ t('general.button.create') }}
      </button>
    </span>
    } @if (selection.length >= 1) {
    <button mat-stroked-button (click)="onDeleteAccount()">{{ t('general.button.delete') }}</button>
    }
  </ng-template>

  <!-- Custom Column Templates (if needed) -->
  <ng-template #tableColumnsTemplate>
    <!-- Enable/Status column with MxStatusComponent -->
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

  <!-- Footer: Max size display -->
  <ng-template #tableFooterTemplate>
    <span oneUiTableMaxSize>{{ t('general.table_function.limit_count') }} {{ tableMaxSize() }}</span>
  </ng-template>
</one-ui-common-table>
```

---

## Column Mapping

| Old Column       | New Column Key   | Notes                                |
| ---------------- | ---------------- | ------------------------------------ |
| `select`         | `_select`        | Built-in, use `selectable` attribute |
| `edit`           | `_edit`          | Built-in, use `editable` attribute   |
| `enable`         | `enable`         | May need custom template for styling |
| `username`       | `username`       | Direct mapping                       |
| `authority`      | `authority`      | Direct mapping                       |
| `passwordExpire` | `passwordExpire` | Direct mapping                       |
| `dummy`          | (not needed)     | Remove                               |
