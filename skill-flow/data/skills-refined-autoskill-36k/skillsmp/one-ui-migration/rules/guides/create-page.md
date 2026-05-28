# Guide: Creating a New Page

## Overview

Create a complete CRUD page with table, create/edit dialog.

## Required Tools

| Tool | Purpose |
|------|---------|
| [page-layout](../tools/ui/page-layout.md) | Page structure |
| [common-table](../tools/common-table.md) | Data table |
| [dialog](../tools/ui/dialogs.md) | Create/edit dialog |
| [signal-store](../tools/signal-store.md) | State management |
| [transloco](../tools/transloco.md) | Translation |

---

## Steps

### 1. Create Store (Domain Layer)

```typescript
// domain/feature.store.ts
export const FeatureStore = signalStore(
  withState({ ...loadingInitialState, items: [] }),
  withMethods((store, api = inject(FeatureApiService)) => ({
    loadItems: queryMethod<void, Item[]>({
      store,
      observe: () => api.getAll$(),
      next: (items) => patchState(store, { items })
    }),
    createItem: mutationMethod<CreateInput, Item>({...}),
    deleteItems: mutationMethod<string[], void>({...})
  }))
);
```

### 2. Create Table Component (UI Layer)

```typescript
// ui/feature-table.component.ts
@Component({
  selector: 'one-ui-feature-table',
  imports: [CommonTableComponent, TranslocoModule, ...],
  templateUrl: './feature-table.component.html'
})
export class FeatureTableComponent {
  tableData = input.required<Item[]>();
  loading = input<boolean>(false);
  add = output<void>();
  edit = output<Item>();
  delete = output<string[]>();
}
```

### 3. Create Dialog Component (Features Layer)

```typescript
// features/feature-dialog/feature-dialog.component.ts
@Component({
  selector: 'one-ui-feature-dialog',
  imports: [MatDialogModule, ReactiveFormsModule, ...],
  templateUrl: './feature-dialog.component.html'
})
export class FeatureDialogComponent {
  readonly #store = inject(FeatureStore);
  readonly #dialogRef = inject(MatDialogRef);
  // ...
}
```

### 4. Create Page Component (Features Layer)

```typescript
// features/feature-page.component.ts
@Component({
  selector: 'one-ui-feature-page',
  imports: [TranslocoModule, BreadcrumbComponent, MxPageTitleComponent, FeatureTableComponent],
  template: `
    <div *transloco="let t" class="gl-page-content">
      <one-ui-breadcrumb />
      <mx-page-title [title]="t('features.xxx.page_title')" />
      <div class="content-wrapper">
        <one-ui-feature-table
          [tableData]="items()"
          [loading]="loading()"
          (add)="openCreateDialog()"
          (edit)="openEditDialog($event)"
          (delete)="onDelete($event)"
          (refresh)="store.loadItems()"
        />
      </div>
    </div>
  `,
  styles: `:host { display: block; }`
})
export class FeaturePageComponent {
  readonly store = inject(FeatureStore);
  readonly #dialog = inject(MatDialog);
  readonly #viewContainerRef = inject(ViewContainerRef);
  // ...
}
```

### 5. Configure Routes (Shell Layer)

```typescript
// shell/feature.routes.ts
export const createRoutes = (): Route[] => [
  {
    path: '',
    component: FeaturePageComponent,
    providers: [FeatureStore, FeatureApiService],
    resolve: { data: () => inject(FeatureStore).loadItems() }
  }
];
```

---

## File Structure

```
libs/mxsecurity/{feature}/
├── domain/
│   ├── feature.model.ts
│   ├── feature.api.ts
│   └── feature.store.ts
├── features/
│   ├── feature-page.component.ts
│   └── feature-dialog/
│       ├── feature-dialog.component.ts
│       └── feature-dialog.component.html
├── ui/
│   └── feature-table/
│       ├── feature-table.component.ts
│       └── feature-table.component.html
└── shell/
    └── feature.routes.ts
```

---

## Checklist

- [ ] Store uses `queryMethod` / `mutationMethod`
- [ ] Table uses `input()` / `output()`, does not inject Store
- [ ] Dialog opened with `viewContainerRef`
- [ ] Page uses `gl-page-content` + `content-wrapper`
- [ ] Translation keys from Legacy
