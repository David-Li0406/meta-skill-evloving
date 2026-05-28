# Angular 20 Syntax

## Control Flow

| Angular 16 | Angular 20 |
|------------|------------|
| `*ngIf="x"` | `@if (x) { }` |
| `*ngIf="x; else tpl"` | `@if (x) { } @else { }` |
| `*ngFor="let i of arr"` | `@for (i of arr; track i.id) { }` |
| `[ngSwitch]="x"` | `@switch (x) { @case (v) { } }` |

### Examples

```html
<!-- ❌ Angular 16 -->
<div *ngIf="isLoading; else content">Loading...</div>
<ng-template #content>
  <div *ngFor="let item of items">{{ item.name }}</div>
</ng-template>

<!-- ✅ Angular 20 -->
@if (isLoading()) {
  <div>Loading...</div>
} @else {
  @for (item of items(); track item.id) {
    <div>{{ item.name }}</div>
  }
}
```

## Dependency Injection

| Angular 16 | Angular 20 |
|------------|------------|
| `constructor(private svc: X)` | `readonly #svc = inject(X);` |
| `@Inject(TOKEN) val` | `#val = inject(TOKEN);` |

### Example

```typescript
// ❌ Angular 16
export class MyComponent {
  constructor(
    private store: FeatureStore,
    private dialog: MatDialog,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}
}

// ✅ Angular 20
export class MyComponent {
  readonly #store = inject(FeatureStore);
  readonly #dialog = inject(MatDialog);
  readonly data = inject<DialogData>(MAT_DIALOG_DATA);
}
```

## Component I/O

| Angular 16 | Angular 20 |
|------------|------------|
| `@Input() x: T` | `x = input<T>();` |
| `@Input() x!: T` | `x = input.required<T>();` |
| `@Output() e = new EventEmitter<T>()` | `e = output<T>();` |

### Example

```typescript
// ❌ Angular 16
export class TableComponent {
  @Input() data: Item[] = [];
  @Input() loading!: boolean;
  @Output() edit = new EventEmitter<Item>();
  @Output() delete = new EventEmitter<string[]>();
}

// ✅ Angular 20
export class TableComponent {
  data = input<Item[]>([]);
  loading = input.required<boolean>();
  edit = output<Item>();
  delete = output<string[]>();
}
```

## Signals

| Angular 16 | Angular 20 |
|------------|------------|
| `new BehaviorSubject<T>(v)` | `signal<T>(v)` |
| `subject.value` | `sig()` |
| `subject.next(v)` | `sig.set(v)` |
| `combineLatest([a$, b$])` | `computed(() => [a(), b()])` |
| `\| async` | `()` (signal call) |

### Example

```typescript
// ❌ Angular 16
export class MyComponent {
  private isOpen$ = new BehaviorSubject<boolean>(false);

  toggle() {
    this.isOpen$.next(!this.isOpen$.value);
  }
}

// Template
<div *ngIf="isOpen$ | async">Content</div>

// ✅ Angular 20
export class MyComponent {
  readonly isOpen = signal(false);

  toggle() {
    this.isOpen.set(!this.isOpen());
  }
}

// Template
@if (isOpen()) {
  <div>Content</div>
}
```

## Computed Values

```typescript
// ❌ Angular 16
get filteredItems(): Item[] {
  return this.items.filter(i => i.active);
}

// ✅ Angular 20
readonly filteredItems = computed(() =>
  this.items().filter(i => i.active)
);
```

## i18n (Translation)

| Angular 16 | Angular 20 |
|------------|------------|
| `@ngx-translate` | `@jsverse/transloco` |
| `{{ 'key' \| translate }}` | `{{ t('key') }}` |
| `translate.instant('key')` | `transloco.translate('key')` |

### Template Example

```html
<!-- ❌ Angular 16 -->
<div>{{ 'general.common.name' | translate }}</div>

<!-- ✅ Angular 20 -->
<div *transloco="let t">
  {{ t('general.common.name') }}
</div>
```

## Buttons

| Angular 16 | Angular 20 |
|------------|------------|
| `mat-raised-button` | `mat-flat-button` |

## Standalone Components

All components must be standalone (no NgModule):

```typescript
@Component({
  selector: 'one-ui-feature',
  standalone: true,  // Default in Angular 20, can omit
  imports: [CommonModule, MatButtonModule, TranslocoModule],
  template: `...`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeatureComponent {}
```
