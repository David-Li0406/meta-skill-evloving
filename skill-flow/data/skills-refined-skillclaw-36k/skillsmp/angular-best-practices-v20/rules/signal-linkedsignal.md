---
title: Use linkedSignal for Derived + Writable State
impact: MEDIUM
impactDescription: linkedSignal fills the gap between read-only computed and fully manual signal
tags: signals, linkedSignal, computed, state-management, reactivity
---

## Use linkedSignal for Derived + Writable State

linkedSignal() creates a signal that derives its value from other signals (like computed) but can also be manually written to (unlike computed). Perfect for state that should reset when dependencies change but allow user overrides.

**The Problem: computed() is read-only:**

```typescript
// ❌ computed is read-only - can't handle user selection
@Component({...})
export class ProductSelectorComponent {
  products = signal<Product[]>([]);

  // Derived from products, but what if user wants to select different one?
  selectedProduct = computed(() => this.products()[0]);

  selectProduct(product: Product) {
    // ERROR: Cannot set computed signal!
    this.selectedProduct.set(product);
  }
}
```

**Workaround with plain signal has issues:**

```typescript
// ❌ Plain signal doesn't auto-reset when products change
@Component({...})
export class ProductSelectorComponent {
  products = signal<Product[]>([]);
  selectedProduct = signal<Product | null>(null);

  constructor() {
    // Must manually sync - error prone
    effect(() => {
      const products = this.products();
      if (products.length > 0) {
        this.selectedProduct.set(products[0]);
      }
    }, { allowSignalWrites: true }); // Code smell!
  }
}
```

**Correct (linkedSignal):**

```typescript
// ✅ linkedSignal: derives from source + allows manual override
@Component({...})
export class ProductSelectorComponent {
  products = signal<Product[]>([]);

  // Auto-selects first product, resets when products change
  // But can also be manually set by user
  selectedProduct = linkedSignal(() => this.products()[0] ?? null);

  selectProduct(product: Product) {
    this.selectedProduct.set(product); // Works!
  }

  loadProducts(products: Product[]) {
    this.products.set(products);
    // selectedProduct automatically resets to first item
  }
}
```

---

**Use Case: Form with resettable default:**

```typescript
// ✅ Quantity selector that resets when product changes
@Component({
  template: `
    <select [(ngModel)]="selectedProduct">
      @for (p of products(); track p.id) {
        <option [ngValue]="p">{{ p.name }}</option>
      }
    </select>

    <input
      type="number"
      [ngModel]="quantity()"
      (ngModelChange)="quantity.set($event)"
      [max]="selectedProduct()?.maxQuantity ?? 10"
    />
  `
})
export class OrderFormComponent {
  products = signal<Product[]>([]);

  // Resets to first product when products change
  selectedProduct = linkedSignal(() => this.products()[0] ?? null);

  // Resets to 1 when selected product changes
  quantity = linkedSignal(() => 1);

  // Or reset to product's default quantity
  quantityWithDefault = linkedSignal(() =>
    this.selectedProduct()?.defaultQuantity ?? 1
  );
}
```

---

**Use Case: Preserve selection if still valid:**

```typescript
// ✅ Advanced: Keep selection if it's still in the new list
@Component({...})
export class SmartSelectorComponent {
  options = signal<Option[]>([]);

  selectedOption = linkedSignal({
    source: this.options,
    computation: (options, previous) => {
      // If previous selection is still valid, keep it
      if (previous && options.some(o => o.id === previous.id)) {
        return previous;
      }
      // Otherwise, select first option
      return options[0] ?? null;
    }
  });
}
```

---

**computed vs linkedSignal decision tree:**

```typescript
@Component({...})
export class ComparisonComponent {
  items = signal<Item[]>([]);
  filter = signal('');

  // ✅ computed: Pure derivation, no user interaction needed
  filteredItems = computed(() =>
    this.items().filter(i => i.name.includes(this.filter()))
  );

  // ✅ computed: Aggregate value, read-only
  totalCount = computed(() => this.items().length);

  // ✅ linkedSignal: Default from source, but user can override
  selectedItem = linkedSignal(() => this.filteredItems()[0] ?? null);

  // ✅ linkedSignal: Pagination that resets on filter change
  currentPage = linkedSignal(() => 1); // Resets to 1 when deps accessed inside change
}
```

---

**When to use each:**

| Scenario | Use |
|----------|-----|
| Derive read-only value | `computed()` |
| Derive value + allow user override | `linkedSignal()` |
| Reset state when dependency changes | `linkedSignal()` |
| Independent state, no derivation | `signal()` |
| Access previous value during computation | `linkedSignal({ computation })` |

---

**Incorrect (effect with allowSignalWrites):**

```typescript
// ❌ Anti-pattern: effect to sync derived state
@Component({...})
export class BadComponent {
  source = signal<string[]>([]);
  selected = signal<string | null>(null);

  constructor() {
    effect(() => {
      const items = this.source();
      this.selected.set(items[0] ?? null);
    }, { allowSignalWrites: true }); // Avoid this!
  }
}
```

**Correct (linkedSignal):**

```typescript
// ✅ linkedSignal is designed for this exact use case
@Component({...})
export class GoodComponent {
  source = signal<string[]>([]);
  selected = linkedSignal(() => this.source()[0] ?? null);
}
```

**Why it matters:**
- linkedSignal expresses intent: "derived with override capability"
- Avoids `allowSignalWrites` code smell in effects
- Automatic reset behavior is declarative and predictable
- Previous value access enables smart selection preservation

Reference: [Angular linkedSignal](https://angular.dev/guide/signals#linked-signal)
