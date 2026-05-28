---
title: Keep computed() Pure - No Side Effects
impact: HIGH
impactDescription: Side effects in computed cause duplicate operations and unpredictable behavior
tags: signals, computed, pure-function, side-effects, reactivity
---

## Keep computed() Pure - No Side Effects

computed() signals must be pure functions that only transform input values and return results. Angular may call computed() multiple times during optimization, causing unintended side effects to run repeatedly.

**Incorrect (Side effects in computed):**

```typescript
// ❌ Side effects: logging, DOM manipulation, HTTP calls
@Component({...})
export class ProductListComponent {
  products = signal<Product[]>([]);

  // BAD: Console log runs multiple times unexpectedly
  totalPrice = computed(() => {
    console.log('Calculating total...'); // Side effect!
    return this.products().reduce((sum, p) => sum + p.price, 0);
  });

  // BAD: Mutating external state
  processedProducts = computed(() => {
    this.analyticsService.track('products-viewed'); // Side effect!
    return this.products().filter(p => p.active);
  });

  // BAD: Async operations (will NOT work)
  enrichedProducts = computed(async () => { // DON'T DO THIS
    const products = this.products();
    return await this.enrichData(products); // Signals are synchronous!
  });
}
```

**Correct (Pure computed, effects for side effects):**

```typescript
@Component({...})
export class ProductListComponent {
  products = signal<Product[]>([]);

  // ✅ Pure computed - only derives new value
  totalPrice = computed(() =>
    this.products().reduce((sum, p) => sum + p.price, 0)
  );

  // ✅ Pure computed - filter is a pure operation
  activeProducts = computed(() =>
    this.products().filter(p => p.active)
  );

  // ✅ Use effect() for side effects
  constructor() {
    effect(() => {
      const products = this.products();
      console.log(`Products updated: ${products.length} items`);
      this.analyticsService.track('products-viewed', { count: products.length });
    });
  }
}
```

---

**Incorrect (Mutating signal values):**

```typescript
// ❌ Mutating the array directly
@Component({...})
export class TodoComponent {
  todos = signal<Todo[]>([]);

  sortedTodos = computed(() => {
    const items = this.todos();
    items.sort((a, b) => a.priority - b.priority); // Mutates original!
    return items;
  });
}
```

**Correct (Immutable operations):**

```typescript
// ✅ Create new array, don't mutate
@Component({...})
export class TodoComponent {
  todos = signal<Todo[]>([]);

  sortedTodos = computed(() =>
    [...this.todos()].sort((a, b) => a.priority - b.priority)
    // Or use toSorted() in modern JS
    // this.todos().toSorted((a, b) => a.priority - b.priority)
  );

  // ✅ Using spread for objects
  todosWithStatus = computed(() =>
    this.todos().map(todo => ({
      ...todo,
      statusLabel: todo.done ? 'Complete' : 'Pending'
    }))
  );
}
```

---

**Incorrect (Expensive operations without memoization):**

```typescript
// ❌ Heavy computation runs on every access
@Component({...})
export class DataGridComponent {
  data = signal<Row[]>([]);
  filter = signal('');

  // Problem: Complex filtering runs every time filteredData() is accessed
  filteredData = computed(() => {
    return this.data()
      .filter(row => this.matchesFilter(row, this.filter()))
      .sort((a, b) => this.complexSort(a, b))
      .map(row => this.transformRow(row));
  });
}
```

**Correct (Break into smaller computed signals):**

```typescript
// ✅ Chain computed signals - each only recomputes when its deps change
@Component({...})
export class DataGridComponent {
  data = signal<Row[]>([]);
  filter = signal('');
  sortField = signal<keyof Row>('name');

  // Each step is memoized independently
  filteredData = computed(() =>
    this.data().filter(row =>
      row.name.toLowerCase().includes(this.filter().toLowerCase())
    )
  );

  sortedData = computed(() =>
    [...this.filteredData()].sort((a, b) =>
      String(a[this.sortField()]).localeCompare(String(b[this.sortField()]))
    )
  );

  // Only re-transforms when sortedData changes
  displayData = computed(() =>
    this.sortedData().map(row => ({
      ...row,
      displayName: `${row.firstName} ${row.lastName}`
    }))
  );
}
```

---

**Correct patterns for computed():**

```typescript
@Component({...})
export class ExamplesComponent {
  user = signal<User | null>(null);
  items = signal<Item[]>([]);
  searchTerm = signal('');

  // ✅ Derive boolean state
  isLoggedIn = computed(() => this.user() !== null);

  // ✅ Derive formatted values
  displayName = computed(() => {
    const user = this.user();
    return user ? `${user.firstName} ${user.lastName}` : 'Guest';
  });

  // ✅ Filter/map operations
  visibleItems = computed(() =>
    this.items().filter(item =>
      item.name.toLowerCase().includes(this.searchTerm().toLowerCase())
    )
  );

  // ✅ Aggregate calculations
  stats = computed(() => ({
    total: this.items().length,
    visible: this.visibleItems().length,
    avgPrice: this.items().reduce((s, i) => s + i.price, 0) / this.items().length || 0
  }));

  // ✅ Combine multiple signals
  viewModel = computed(() => ({
    user: this.user(),
    items: this.visibleItems(),
    stats: this.stats(),
    isLoggedIn: this.isLoggedIn()
  }));
}
```

**Why it matters:**
- Angular may execute computed() multiple times for optimization
- Side effects (logging, analytics, mutations) will run unpredictably
- computed() is lazy and memoized - only re-runs when dependencies change
- Keeping computed pure makes behavior predictable and testable

Reference: [Angular Signals Guide](https://angular.dev/guide/signals#computed-signals)
