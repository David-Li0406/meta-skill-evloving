# Common Pitfalls: Angular Syntax

## 1. Mixing Old and New Control Flow

```typescript
// ❌ Don't mix
<div *ngIf="condition">
  @for (item of items; track item.id) {
    {{ item }}
  }
</div>

// ✅ Use new syntax consistently
@if (condition) {
  @for (item of items; track item.id) {
    <div>{{ item }}</div>
  }
}
```

---

## 2. Forgetting `track` in `@for`

```typescript
// ❌ Missing track
@for (item of items) {
  <div>{{ item }}</div>
}

// ✅ Always provide track
@for (item of items; track item.id) {
  <div>{{ item }}</div>
}
```

### Common Track Patterns

```html
<!-- Track by id (most common) -->
@for (item of items; track item.id) { ... }

<!-- Track by unique property -->
@for (option of options; track option.value) { ... }

<!-- Track by index (when no unique id) -->
@for (item of items; track $index) { ... }

<!-- Track by object identity (simple primitives) -->
@for (value of values; track value) { ... }
```

---

## 3. Using Module-based Patterns

```typescript
// ❌ Don't create NgModules
@NgModule({
  declarations: [MyComponent],
  imports: [CommonModule]
})
export class MyModule {}

// ✅ Use standalone everywhere
@Component({
  standalone: true,
  imports: [CommonModule]
})
export class MyComponent {}
```

---

## 4. Not Using Signals with SignalStore

```typescript
// ❌ Mixing observables unnecessarily
export class MyComponent {
  data$ = this.store.data$.pipe(...);
}

// ✅ Use signals directly
export class MyComponent {
  data = computed(() => this.store.data());
}
```

---

## 5. mxLabelOptionalText - Use Default Value

```html
<!-- ❌ WRONG - Don't specify mxLabelOptionalText, use default -->
<mat-label mxLabel mxLabelOptional [mxLabelOptionalText]="t('general.label.optional')">
  {{ t('features.email_settings.mail_server') }}
</mat-label>

<!-- ✅ CORRECT - Use default value -->
<mat-label mxLabel mxLabelOptional>
  {{ t('features.email_settings.mail_server') }}
</mat-label>
```

---

## 6. langChanged() Must Be Called in Injection Context

`langChanged()` uses `inject()` internally, so it **must** be called at class field level (injection context), NOT inside `computed()`.

```typescript
// ❌ WRONG - inject() fails because computed() is not an injection context
export class MyComponent {
  readonly options = computed(() => {
    langChanged(); // ❌ ERROR: NG0203 inject() must be called from injection context
    return [...];
  });
}

// ✅ CORRECT - Call langChanged() at class field level, use returned signal in computed()
export class MyComponent {
  readonly #transloco = inject(TranslocoService);
  readonly #langChanged = langChanged(); // ✅ Called at field level (injection context)

  readonly options = computed(() => {
    this.#langChanged(); // ✅ Call the stored signal to trigger reactivity
    return [
      { value: 1, text: this.#transloco.translate('key1') },
      { value: 2, text: this.#transloco.translate('key2') }
    ];
  });
}
```

Reference: `libs/mxsecurity/account-page/ui/src/lib/account-table/account-table.component.ts`

---

## 7. Constructor vs inject() with Field Initializers

**CRITICAL**: When using field initializers that depend on injected services, you MUST use `inject()` instead of constructor injection.

```typescript
// ❌ WRONG - Constructor injection with field initializer
export class MyComponent {
  readonly form = this.#fb.group({ ... }); // ❌ ERROR: #fb is undefined!

  constructor(private fb: NonNullableFormBuilder) {
    this.#fb = fb;  // Too late! Field initializer already ran
  }
}

// ✅ CORRECT - Use inject() for field initializers
export class MyComponent {
  readonly #fb = inject(NonNullableFormBuilder);  // ✅ Available immediately
  readonly form = this.#fb.group({ ... });  // ✅ Works!
}
```

### Why This Happens

Field initializers run BEFORE the constructor body. With constructor injection, the injected service isn't available until the constructor runs, but field initializers have already executed by then.

---

## 8. input() vs @Input() Signal Behavior

```typescript
// ❌ WRONG - Treating input signal as property
export class MyComponent {
  readonly data = input<Data>();

  ngOnInit() {
    console.log(this.data);  // ❌ Logs the Signal, not the value!
  }
}

// ✅ CORRECT - Call the signal to get value
export class MyComponent {
  readonly data = input<Data>();

  ngOnInit() {
    console.log(this.data());  // ✅ Logs the actual value
  }
}
```

---

## 9. output() vs @Output() EventEmitter

```typescript
// ❌ WRONG - Using EventEmitter with output()
export class MyComponent {
  readonly save = new EventEmitter<Data>();  // ❌ Don't mix patterns
}

// ✅ CORRECT - Use output() function
export class MyComponent {
  readonly save = output<Data>();  // ✅ Returns OutputEmitterRef

  onSave() {
    this.save.emit(this.form.getRawValue());
  }
}
```

---

## 10. computed() vs effect() Usage

```typescript
// ❌ WRONG - Using effect() for derived state
export class MyComponent {
  filteredItems: Item[] = [];

  constructor() {
    effect(() => {
      this.filteredItems = this.items().filter(i => i.active);  // ❌ Side effect for state
    });
  }
}

// ✅ CORRECT - Use computed() for derived state
export class MyComponent {
  readonly filteredItems = computed(() =>
    this.items().filter(i => i.active)  // ✅ Pure derivation
  );
}

// ✅ CORRECT - Use effect() for side effects (logging, API calls)
export class MyComponent {
  constructor() {
    effect(() => {
      console.log('Items changed:', this.items());  // ✅ Side effect
    });
  }
}
```

---

## 11. viewChild() Signal Query

```typescript
// ❌ WRONG - Old @ViewChild pattern
export class MyComponent {
  @ViewChild('myElement') myElement?: ElementRef;

  ngAfterViewInit() {
    this.myElement?.nativeElement.focus();
  }
}

// ✅ CORRECT - Use viewChild() signal query
export class MyComponent {
  readonly myElement = viewChild<ElementRef>('myElement');

  constructor() {
    effect(() => {
      const el = this.myElement();
      if (el) {
        el.nativeElement.focus();
      }
    });
  }
}
```

---

## Quick Reference: Old vs New Syntax

| Old | New |
|-----|-----|
| `*ngIf="condition"` | `@if (condition) { }` |
| `*ngFor="let item of items"` | `@for (item of items; track item.id) { }` |
| `[ngSwitch]="value"` | `@switch (value) { }` |
| `@Input()` | `input()` |
| `@Output()` | `output()` |
| `@ViewChild()` | `viewChild()` |
| `@ViewChildren()` | `viewChildren()` |
| `@ContentChild()` | `contentChild()` |
| `@ContentChildren()` | `contentChildren()` |
| `constructor(private svc: Service)` | `inject(Service)` |
