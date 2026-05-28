# Angular Best Practices (Angular 20+)

**Version 2.0.0**  
Community  
January 2026

> **Note:**  
> This document is for AI agents and LLMs to follow when maintaining,  
> generating, or refactoring Angular codebases. Optimized for Angular 20+.

---

## Abstract

Performance optimization guide for Angular 20+ applications with modern features including Signals, linkedSignal, httpResource, @defer blocks, standalone components (default), signal inputs/outputs, and native control flow syntax (@if, @for). Contains rules prioritized by impact for AI-assisted code generation and refactoring.

---

## Table of Contents

0. [Section 0](#0-section-0) — **MEDIUM**
   - 0.1 [Combine Multiple Array Iterations](#01-combine-multiple-array-iterations)
   - 0.2 [Keep computed() Pure - No Side Effects](#02-keep-computed-pure---no-side-effects)
   - 0.3 [Use CSS content-visibility for Off-Screen Content](#03-use-css-content-visibility-for-off-screen-content)
   - 0.4 [Use effect() Correctly - Avoid Anti-Patterns](#04-use-effect-correctly---avoid-anti-patterns)
   - 0.5 [Use Host Directives for Behavior Composition](#05-use-host-directives-for-behavior-composition)
   - 0.6 [Use Incremental Hydration for SSR](#06-use-incremental-hydration-for-ssr)
   - 0.7 [Use linkedSignal for Derived + Writable State](#07-use-linkedsignal-for-derived--writable-state)
   - 0.8 [Use Set/Map for O(1) Lookups](#08-use-setmap-for-o1-lookups)
   - 0.9 [Use Signal Inputs and Outputs](#09-use-signal-inputs-and-outputs)
   - 0.10 [Use Signal Inputs for Route Parameters](#010-use-signal-inputs-for-route-parameters)
   - 0.11 [Use Smart and Dumb Component Pattern](#011-use-smart-and-dumb-component-pattern)
1. [Change Detection](#1-change-detection) — **CRITICAL**
   - 1.1 [Detach Change Detector for Heavy Operations](#11-detach-change-detector-for-heavy-operations)
   - 1.2 [Run Non-UI Code Outside NgZone](#12-run-non-ui-code-outside-ngzone)
   - 1.3 [Use Angular Signals for Reactive State](#13-use-angular-signals-for-reactive-state)
   - 1.4 [Use OnPush Change Detection Strategy](#14-use-onpush-change-detection-strategy)
2. [Bundle & Lazy Loading](#2-bundle--lazy-loading) — **CRITICAL**
   - 2.1 [Avoid Barrel File Imports](#21-avoid-barrel-file-imports)
   - 2.2 [Defer Non-Critical Third-Party Scripts](#22-defer-non-critical-third-party-scripts)
   - 2.3 [Lazy Load Routes with loadComponent](#23-lazy-load-routes-with-loadcomponent)
   - 2.4 [Use @defer for Lazy Loading Components](#24-use-defer-for-lazy-loading-components)
   - 2.5 [Use Preload Strategies for Lazy Modules](#25-use-preload-strategies-for-lazy-modules)
   - 2.6 [Use Standalone Components](#26-use-standalone-components)
3. [RxJS Optimization](#3-rxjs-optimization) — **HIGH**
   - 3.1 [Avoid Nested Subscriptions](#31-avoid-nested-subscriptions)
   - 3.2 [Share Observables to Avoid Duplicate Requests](#32-share-observables-to-avoid-duplicate-requests)
   - 3.3 [Use Async Pipe Instead of Manual Subscribe](#33-use-async-pipe-instead-of-manual-subscribe)
   - 3.4 [Use Correct RxJS Mapping Operators](#34-use-correct-rxjs-mapping-operators)
   - 3.5 [Use Efficient RxJS Operators](#35-use-efficient-rxjs-operators)
   - 3.6 [Use takeUntilDestroyed for Cleanup](#36-use-takeuntildestroyed-for-cleanup)
4. [Template Performance](#4-template-performance) — **HIGH**
   - 4.1 [Avoid Function Calls in Templates](#41-avoid-function-calls-in-templates)
   - 4.2 [Use @for with track for Loops](#42-use-for-with-track-for-loops)
   - 4.3 [Use NgOptimizedImage for Images](#43-use-ngoptimizedimage-for-images)
   - 4.4 [Use Pure Pipes for Data Transformation](#44-use-pure-pipes-for-data-transformation)
   - 4.5 [Use Virtual Scrolling for Large Lists](#45-use-virtual-scrolling-for-large-lists)
5. [Dependency Injection](#5-dependency-injection) — **MEDIUM-HIGH**
   - 5.1 [Use Factory Providers for Complex Setup](#51-use-factory-providers-for-complex-setup)
   - 5.2 [Use InjectionToken for Type-Safe Configuration](#52-use-injectiontoken-for-type-safe-configuration)
   - 5.3 [Use providedIn root for Tree-Shaking](#53-use-providedin-root-for-tree-shaking)
6. [HTTP & Caching](#6-http--caching) — **MEDIUM**
   - 6.1 [Use Functional HTTP Interceptors](#61-use-functional-http-interceptors)
   - 6.2 [Use httpResource for Signal-Based HTTP](#62-use-httpresource-for-signal-based-http)
   - 6.3 [Use TransferState for SSR Hydration](#63-use-transferstate-for-ssr-hydration)
7. [Forms Optimization](#7-forms-optimization) — **MEDIUM**
   - 7.1 [Use Reactive Forms for Complex Forms](#71-use-reactive-forms-for-complex-forms)
8. [General Performance](#8-general-performance) — **LOW-MEDIUM**
   - 8.1 [Offload Heavy Computation to Web Workers](#81-offload-heavy-computation-to-web-workers)
   - 8.2 [Prevent Memory Leaks](#82-prevent-memory-leaks)

---

## 0. Section 0

**Impact: MEDIUM**

### 0.1 Combine Multiple Array Iterations

**Impact: LOW-MEDIUM (Reduces array iterations from N to 1)**

Multiple `.filter()`, `.map()`, or `.reduce()` calls iterate the array multiple times. When processing the same array for different purposes, combine into a single loop.

**Incorrect (3 iterations over same array):**

```typescript
@Component({...})
export class UserStatsComponent {
  users: User[] = [];

  getStats() {
    // ❌ Iterates users array 3 times
    const admins = this.users.filter(u => u.role === 'admin');
    const activeUsers = this.users.filter(u => u.isActive);
    const totalAge = this.users.reduce((sum, u) => sum + u.age, 0);

    return { admins, activeUsers, averageAge: totalAge / this.users.length };
  }
}
```

**Correct (1 iteration):**

```typescript
@Component({...})
export class UserStatsComponent {
  users: User[] = [];

  getStats() {
    // ✅ Single iteration, multiple results
    const admins: User[] = [];
    const activeUsers: User[] = [];
    let totalAge = 0;

    for (const user of this.users) {
      if (user.role === 'admin') admins.push(user);
      if (user.isActive) activeUsers.push(user);
      totalAge += user.age;
    }

    return { admins, activeUsers, averageAge: totalAge / this.users.length };
  }
}
```

**With reduce for complex aggregations:**

```typescript
// ❌ Bad - 4 iterations
const total = orders.reduce((sum, o) => sum + o.total, 0);
const count = orders.length;
const pending = orders.filter(o => o.status === 'pending').length;
const shipped = orders.filter(o => o.status === 'shipped').length;

// ✅ Good - 1 iteration with reduce
const stats = orders.reduce(
  (acc, order) => ({
    total: acc.total + order.total,
    count: acc.count + 1,
    pending: acc.pending + (order.status === 'pending' ? 1 : 0),
    shipped: acc.shipped + (order.status === 'shipped' ? 1 : 0)
  }),
  { total: 0, count: 0, pending: 0, shipped: 0 }
);
```

**Map and filter in one pass:**

```typescript
// ❌ Bad - 2 iterations
const activeUserNames = users
  .filter(u => u.isActive)
  .map(u => u.name);

// ✅ Good - 1 iteration with flatMap or reduce
const activeUserNames = users.flatMap(u =>
  u.isActive ? [u.name] : []
);

// Or with reduce
const activeUserNames = users.reduce<string[]>(
  (names, u) => u.isActive ? [...names, u.name] : names,
  []
);

// Or simple loop (fastest)
const activeUserNames: string[] = [];
for (const u of users) {
  if (u.isActive) activeUserNames.push(u.name);
}
```

**Grouping data:**

```typescript
// ❌ Bad - multiple filter calls for each group
const byStatus = {
  pending: orders.filter(o => o.status === 'pending'),
  processing: orders.filter(o => o.status === 'processing'),
  shipped: orders.filter(o => o.status === 'shipped'),
  delivered: orders.filter(o => o.status === 'delivered')
};

// ✅ Good - single iteration grouping
const byStatus = orders.reduce<Record<string, Order[]>>(
  (groups, order) => {
    const status = order.status;
    groups[status] = groups[status] || [];
    groups[status].push(order);
    return groups;
  },
  {}
);

// ✅ Even better with Object.groupBy (ES2024)
const byStatus = Object.groupBy(orders, order => order.status);
```

**In computed signals:**

```typescript
@Component({...})
export class OrderDashboardComponent {
  orders = input.required<Order[]>();

  // ❌ Bad - 3 computed = 3 iterations when orders change
  pendingOrders = computed(() =>
    this.orders().filter(o => o.status === 'pending')
  );
  totalRevenue = computed(() =>
    this.orders().reduce((sum, o) => sum + o.total, 0)
  );
  orderCount = computed(() => this.orders().length);

  // ✅ Good - 1 computed = 1 iteration
  stats = computed(() => {
    const orders = this.orders();
    const pending: Order[] = [];
    let revenue = 0;

    for (const order of orders) {
      if (order.status === 'pending') pending.push(order);
      revenue += order.total;
    }

    return {
      pending,
      revenue,
      count: orders.length
    };
  });
}
```

**When multiple iterations ARE okay:**

```typescript
// ✅ OK - small arrays (under 100 items)
const filtered = smallArray.filter(x => x.active).map(x => x.name);

// ✅ OK - readability matters more than micro-optimization
// When array is small and code is read often
const adults = users.filter(u => u.age >= 18);
const adultNames = adults.map(u => u.name);
```

**Why it matters:**

- 10,000 items × 3 iterations = 30,000 operations

- 10,000 items × 1 iteration = 10,000 operations (3× fewer)

- Each iteration has function call overhead

- Matters most for large datasets or frequent recalculations

Reference: [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array)

### 0.2 Keep computed() Pure - No Side Effects

**Impact: HIGH (Side effects in computed cause duplicate operations and unpredictable behavior)**

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

Reference: [https://angular.dev/guide/signals#computed-signals](https://angular.dev/guide/signals#computed-signals)

### 0.3 Use CSS content-visibility for Off-Screen Content

**Impact: HIGH (10× faster initial render by skipping off-screen layout)**

Apply `content-visibility: auto` to defer rendering of off-screen content. The browser skips layout and paint for elements not in the viewport, dramatically improving initial render time.

**Incorrect (renders all items immediately):**

```typescript
@Component({
  selector: 'app-message-list',
  template: `
    <div class="messages">
      <!-- All 1000 messages rendered and laid out immediately -->
      @for (message of messages; track message.id) {
        <div class="message">
          <app-avatar [user]="message.author" />
          <div class="content">{{ message.text }}</div>
          <span class="time">{{ message.time | date:'short' }}</span>
        </div>
      }
    </div>
  `,
  styles: [`
    .message {
      padding: 12px;
      border-bottom: 1px solid #eee;
    }
  `]
})
export class MessageListComponent {
  messages: Message[] = []; // 1000+ messages
}
```

**Correct (defers off-screen rendering):**

```typescript
@Component({
  selector: 'app-message-list',
  template: `
    <div class="messages">
      @for (message of messages; track message.id) {
        <div class="message">
          <app-avatar [user]="message.author" />
          <div class="content">{{ message.text }}</div>
          <span class="time">{{ message.time | date:'short' }}</span>
        </div>
      }
    </div>
  `,
  styles: [`
    .message {
      padding: 12px;
      border-bottom: 1px solid #eee;

      /* ✅ Skip layout/paint for off-screen items */
      content-visibility: auto;

      /* Hint at size to prevent layout shift when scrolling */
      contain-intrinsic-size: 0 80px;
    }
  `]
})
export class MessageListComponent {
  messages: Message[] = []; // 1000+ messages - no problem!
}
```

**For card layouts:**

```scss
// Product grid with many items
.product-card {
  content-visibility: auto;
  contain-intrinsic-size: 300px 400px; // width height

  // Also add containment for extra performance
  contain: layout style paint;
}
```

**For sections/pages:**

```typescript
@Component({
  selector: 'app-long-page',
  template: `
    <section class="hero">...</section>
    <section class="features content-section">...</section>
    <section class="testimonials content-section">...</section>
    <section class="pricing content-section">...</section>
    <section class="faq content-section">...</section>
    <section class="footer content-section">...</section>
  `,
  styles: [`
    .content-section {
      content-visibility: auto;
      contain-intrinsic-size: 0 500px; /* Estimated section height */
    }
  `]
})
export class LongPageComponent {}
```

**Dynamic height estimation:**

```typescript
@Component({
  selector: 'app-dynamic-list',
  template: `
    @for (item of items; track item.id) {
      <div
        class="item"
        [style.contain-intrinsic-size]="'0 ' + estimateHeight(item) + 'px'"
      >
        {{ item.content }}
      </div>
    }
  `,
  styles: [`
    .item {
      content-visibility: auto;
    }
  `]
})
export class DynamicListComponent {
  estimateHeight(item: Item): number {
    // Rough estimation based on content length
    const baseHeight = 60;
    const charsPerLine = 50;
    const lineHeight = 20;
    const lines = Math.ceil(item.content.length / charsPerLine);
    return baseHeight + (lines * lineHeight);
  }
}
```

**Combining with virtual scroll:**

```typescript
// For extremely long lists (10,000+ items), combine both:
// - Virtual scroll: only creates DOM nodes for visible items
// - content-visibility: optimizes the rendered items

@Component({
  template: `
    <cdk-virtual-scroll-viewport itemSize="80" class="list">
      <div
        *cdkVirtualFor="let item of items"
        class="item"
      >
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `,
  styles: [`
    .item {
      content-visibility: auto;
      contain-intrinsic-size: 0 80px;
    }
  `]
})
export class HugeListComponent {}
```

**When to use content-visibility:**

| Scenario | Recommendation |

|----------|----------------|

| List with 50-500 items | ✅ `content-visibility: auto` |

| List with 500+ items | ✅ Virtual scroll + content-visibility |

| Long scrolling page | ✅ On each section |

| Modal/dialog content | ❌ Usually all visible |

| Above-the-fold content | ❌ Must render immediately |

**Browser support note:**

```scss
// Progressive enhancement - works in Chrome, Edge, Opera
// Safari/Firefox ignore it safely
.item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;

  // Fallback for unsupported browsers (optional)
  @supports not (content-visibility: auto) {
    // No special handling needed - just renders normally
  }
}
```

**Why it matters:**

- 1000 items without content-visibility: browser computes layout for all 1000

- 1000 items with content-visibility: browser computes layout for ~10 visible

- Real-world impact: 10× faster initial paint for long lists

- No JavaScript required - pure CSS optimization

Reference: [https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility](https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility)

### 0.4 Use effect() Correctly - Avoid Anti-Patterns

**Impact: HIGH (Misused effects cause infinite loops, memory leaks, and unpredictable behavior)**

effect() should be your last resort for handling side effects. Misuse leads to infinite loops, memory leaks, and hard-to-debug behavior. Prefer computed() for derived values and direct signal updates for state changes.

**Incorrect (Writing to a signal you're reading):**

```typescript
// ❌ INFINITE LOOP - effect reads count, then writes to count
@Component({...})
export class CounterComponent {
  count = signal(0);

  constructor() {
    effect(() => {
      // Reads count, triggers effect
      // Writes count, triggers effect again
      // Infinite loop!
      this.count.set(this.count() + 1);
    });
  }
}
```

**Correct (Use computed or direct update):**

```typescript
// ✅ Use computed for derived values
@Component({...})
export class CounterComponent {
  count = signal(0);
  doubledCount = computed(() => this.count() * 2); // No effect needed!

  increment() {
    this.count.update(c => c + 1);
  }
}
```

---

**Incorrect (Nested effects):**

```typescript
// ❌ Memory leak - inner effect never destroyed
@Component({...})
export class BadComponent {
  user = signal<User | null>(null);

  constructor() {
    effect(() => {
      const user = this.user();
      if (user) {
        // Creates new effect on EVERY user change
        // Old effects never cleaned up!
        effect(() => {
          console.log('Nested effect:', user.name);
        });
      }
    });
  }
}
```

**Correct (Single effect with conditional logic):**

```typescript
// ✅ One effect, conditional inside
@Component({...})
export class GoodComponent {
  user = signal<User | null>(null);

  constructor() {
    effect(() => {
      const user = this.user();
      if (user) {
        console.log('User logged in:', user.name);
        this.analyticsService.identify(user.id);
      } else {
        console.log('User logged out');
        this.analyticsService.reset();
      }
    });
  }
}
```

---

**Incorrect (Using effect to sync state):**

```typescript
// ❌ Anti-pattern: effect to derive state
@Component({...})
export class BadSyncComponent {
  firstName = signal('');
  lastName = signal('');
  fullName = signal(''); // Should be computed!

  constructor() {
    // DON'T: Use effect to sync signals
    effect(() => {
      this.fullName.set(`${this.firstName()} ${this.lastName()}`);
    }, { allowSignalWrites: true });
  }
}
```

**Correct (Use computed for derived state):**

```typescript
// ✅ computed is the right tool for derived values
@Component({...})
export class GoodSyncComponent {
  firstName = signal('');
  lastName = signal('');
  fullName = computed(() => `${this.firstName()} ${this.lastName()}`);
}
```

---

**Incorrect (Effect for parent-to-child communication):**

```typescript
// ❌ Anti-pattern: calling child methods from parent effect
@Component({
  template: `<app-child #child />`
})
export class BadParentComponent {
  data = signal<Data | null>(null);
  @ViewChild('child') child!: ChildComponent;

  constructor() {
    effect(() => {
      const data = this.data();
      if (data) {
        this.child.updateData(data); // Imperative, fragile
      }
    });
  }
}
```

**Correct (Use input binding):**

```typescript
// ✅ Declarative data flow with inputs
@Component({
  template: `<app-child [data]="data()" />`
})
export class GoodParentComponent {
  data = signal<Data | null>(null);
}

// Child receives data reactively via input
@Component({...})
export class ChildComponent {
  data = input<Data | null>(null);

  processedData = computed(() => {
    const d = this.data();
    return d ? this.process(d) : null;
  });
}
```

---

**Correct use cases for effect():**

```typescript
@Component({...})
export class CorrectEffectUsageComponent {
  theme = signal<'light' | 'dark'>('light');
  searchQuery = signal('');
  user = signal<User | null>(null);

  constructor() {
    // ✅ Sync with external API (DOM, localStorage, etc.)
    effect(() => {
      document.body.classList.toggle('dark-mode', this.theme() === 'dark');
    });

    // ✅ Persist to localStorage
    effect(() => {
      localStorage.setItem('theme', this.theme());
    });

    // ✅ Logging/Analytics (non-reactive world)
    effect(() => {
      const user = this.user();
      if (user) {
        this.analytics.identify(user.id);
      }
    });

    // ✅ Trigger imperative APIs
    effect(() => {
      const query = this.searchQuery();
      if (query.length > 0) {
        this.autocomplete.updateSuggestions(query);
      }
    });
  }
}
```

---

**Using untracked() to prevent re-runs:**

```typescript
@Component({...})
export class SmartEffectComponent {
  query = signal('');
  page = signal(1);

  constructor() {
    // Only re-run when query changes, not when page changes
    effect(() => {
      const q = this.query(); // Tracked - triggers effect
      const p = untracked(() => this.page()); // Untracked - doesn't trigger

      this.logSearch(q, p);
    });
  }
}
```

**Effect cleanup:**

```typescript
@Component({...})
export class CleanupEffectComponent {
  elementId = signal('my-element');

  constructor() {
    effect((onCleanup) => {
      const id = this.elementId();
      const handler = () => console.log('clicked');

      document.getElementById(id)?.addEventListener('click', handler);

      // Cleanup runs before next effect execution and on destroy
      onCleanup(() => {
        document.getElementById(id)?.removeEventListener('click', handler);
      });
    });
  }
}
```

**Why it matters:**

- `allowSignalWrites: true` is a code smell - usually means you should use computed()

- Effects are for syncing with non-reactive external systems

- Nested effects = guaranteed memory leaks

- Circular signal writes = infinite loops

Reference: [https://angular.dev/guide/signals/effect](https://angular.dev/guide/signals/effect)

### 0.5 Use Host Directives for Behavior Composition

**Impact: MEDIUM (Reusable behaviors, cleaner components)**

Host directives compose reusable behaviors into components without inheritance, promoting composition and keeping components focused.

**Incorrect (Repeated behavior across components):**

```typescript
@Component({
  selector: 'app-button',
  template: `<ng-content />`
})
export class ButtonComponent {
  @HostBinding('class.focused') isFocused = false;
  @HostBinding('class.disabled') isDisabled = false;

  @HostListener('focus') onFocus() { this.isFocused = true; }
  @HostListener('blur') onBlur() { this.isFocused = false; }
}

@Component({
  selector: 'app-card',
  template: `<ng-content />`
})
export class CardComponent {
  // Same focus/disable logic duplicated...
  @HostBinding('class.focused') isFocused = false;
  @HostBinding('class.disabled') isDisabled = false;
}
```

**Correct (Reusable behavior directive):**

```typescript
@Directive({
  selector: '[focusable]',
  host: {
    'tabindex': '0',
    '(focus)': 'onFocus()',
    '(blur)': 'onBlur()',
    '[class.focused]': 'isFocused()'
  }
})
export class FocusableDirective {
  isFocused = signal(false);
  onFocus() { this.isFocused.set(true); }
  onBlur() { this.isFocused.set(false); }
}

@Component({
  selector: 'app-button',
  hostDirectives: [FocusableDirective],
  template: `<ng-content />`
})
export class ButtonComponent {}

@Component({
  selector: 'app-card',
  hostDirectives: [FocusableDirective],
  template: `<ng-content />`
})
export class CardComponent {}
```

**Why it matters:**

- Behaviors defined once, reused everywhere

- `hostDirectives` array composes multiple behaviors

- Inputs/outputs can be exposed via directive configuration

- No inheritance hierarchy needed

Reference: [https://angular.dev/guide/directives/directive-composition-api](https://angular.dev/guide/directives/directive-composition-api)

### 0.6 Use Incremental Hydration for SSR

**Impact: HIGH (Faster TTI, smaller JavaScript bundles)**

Incremental hydration defers JavaScript loading for below-fold components, reducing initial bundle size and improving Time to Interactive.

**Incorrect (Full hydration of all components):**

```typescript
@Component({
  template: `
    <app-header />
    <app-hero />
    <app-comments [postId]="postId" />      <!-- Heavy, below fold -->
    <app-recommendations />                  <!-- Heavy, below fold -->
    <app-footer />
  `
})
export class PostComponent {
  postId = input.required<string>();
}
```

**Correct (Incremental hydration with @defer):**

```typescript
@Component({
  template: `
    <app-header />
    <app-hero />

    @defer (hydrate on viewport) {
      <app-comments [postId]="postId()" />
    } @placeholder {
      <div class="comments-skeleton">Loading comments...</div>
    }

    @defer (hydrate on idle) {
      <app-recommendations />
    }

    @defer (hydrate never) {
      <app-footer />
    }
  `
})
export class PostComponent {
  postId = input.required<string>();
}
```

**Why it matters:**

- `hydrate on viewport` - Hydrates when scrolled into view

- `hydrate on idle` - Hydrates during browser idle time

- `hydrate on interaction` - Hydrates on user click/focus

- `hydrate never` - Never hydrates (static content only)

Reference: [https://angular.dev/guide/ssr](https://angular.dev/guide/ssr)

### 0.7 Use linkedSignal for Derived + Writable State

**Impact: MEDIUM (linkedSignal fills the gap between read-only computed and fully manual signal)**

linkedSignal() creates a signal that derives its value from other signals (like computed) but can also be manually written to (unlike computed). Perfect for state that should reset when dependencies change but allow user overrides.

**The Problem: computed() is read-only:**

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

**Use Case: Form with resettable default:**

---

**Use Case: Preserve selection if still valid:**

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

Reference: [https://angular.dev/guide/signals#linked-signal](https://angular.dev/guide/signals#linked-signal)

### 0.8 Use Set/Map for O(1) Lookups

**Impact: LOW-MEDIUM (O(n) to O(1) lookup performance)**

Convert arrays to Set/Map when performing repeated membership checks or key lookups. Array methods like `includes()`, `find()`, and `indexOf()` are O(n), while Set/Map operations are O(1).

**Incorrect (O(n) per lookup):**

```typescript
@Component({...})
export class UserListComponent {
  users: User[] = [];
  selectedIds: string[] = [];

  isSelected(userId: string): boolean {
    // ❌ O(n) - scans entire array for each check
    return this.selectedIds.includes(userId);
  }

  // With 1000 users and 100 selected, this is 100,000 comparisons
  // Called on every change detection cycle!
}
```

**Correct (O(1) per lookup):**

```typescript
@Component({...})
export class UserListComponent {
  users: User[] = [];
  selectedIds = new Set<string>();

  isSelected(userId: string): boolean {
    // ✅ O(1) - instant hash lookup
    return this.selectedIds.has(userId);
  }

  toggleSelection(userId: string) {
    if (this.selectedIds.has(userId)) {
      this.selectedIds.delete(userId);
    } else {
      this.selectedIds.add(userId);
    }
  }
}
```

**Filtering with Set:**

```typescript
// ❌ Bad - O(n×m) where n=items, m=allowedIds
const allowedIds = ['a', 'b', 'c', 'd', 'e'];
const filtered = items.filter(item => allowedIds.includes(item.id));

// ✅ Good - O(n) where n=items
const allowedIds = new Set(['a', 'b', 'c', 'd', 'e']);
const filtered = items.filter(item => allowedIds.has(item.id));
```

**Map for key-value lookups:**

```typescript
// ❌ Bad - O(n) find for each lookup
interface User { id: string; name: string; }
const users: User[] = [...];

function getUserName(id: string): string {
  const user = users.find(u => u.id === id); // O(n)
  return user?.name ?? 'Unknown';
}

// ✅ Good - O(1) Map lookup
const userMap = new Map(users.map(u => [u.id, u]));

function getUserName(id: string): string {
  return userMap.get(id)?.name ?? 'Unknown'; // O(1)
}
```

**Building lookup maps in services:**

```typescript
@Injectable({ providedIn: 'root' })
export class ProductService {
  private productsMap = new Map<string, Product>();

  loadProducts(): Observable<Product[]> {
    return this.http.get<Product[]>('/api/products').pipe(
      tap(products => {
        // Build map for O(1) lookups
        this.productsMap = new Map(products.map(p => [p.id, p]));
      })
    );
  }

  getProductById(id: string): Product | undefined {
    return this.productsMap.get(id); // O(1) instead of array.find()
  }

  getProductsByIds(ids: string[]): Product[] {
    return ids
      .map(id => this.productsMap.get(id))
      .filter((p): p is Product => p !== undefined);
  }
}
```

**Deduplication:**

```typescript
// ❌ Bad - O(n²) with indexOf
const unique = items.filter((item, index) =>
  items.indexOf(item) === index
);

// ✅ Good - O(n) with Set
const unique = [...new Set(items)];

// For objects, dedupe by key
const uniqueById = [...new Map(items.map(i => [i.id, i])).values()];
```

**When to use which:**

| Data Structure | Use Case |

|----------------|----------|

| `Set` | Unique values, membership checks |

| `Map` | Key-value pairs, lookups by ID |

| `Array` | Ordered data, iteration, small collections (<100 items) |

**Performance comparison:**

```typescript
Array.includes() on 10,000 items: ~0.5ms per lookup
Set.has() on 10,000 items: ~0.001ms per lookup (500× faster)
```

**Why it matters:**

- Change detection may call methods many times per second

- With large datasets, O(n) lookups become noticeable bottlenecks

- Set/Map use hash tables for constant-time operations

Reference: [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

### 0.9 Use Signal Inputs and Outputs

**Impact: HIGH (Better reactivity, type safety, simpler code)**

Signal inputs (`input()`) and outputs (`output()`) replace `@Input()` and `@Output()` decorators, providing better type inference and reactive tracking without `OnChanges`.

**Incorrect (Decorator-based with OnChanges):**

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <h2>{{ name }}</h2>
    <p>{{ email }}</p>
    <button (click)="onSelect()">Select</button>
  `
})
export class UserCardComponent implements OnChanges {
  @Input() name!: string;
  @Input() email = '';
  @Output() selected = new EventEmitter<string>();

  ngOnChanges(changes: SimpleChanges) {
    if (changes['name']) {
      console.log('Name changed:', this.name);
    }
  }

  onSelect() {
    this.selected.emit(this.name);
  }
}
```

**Correct (Signal inputs with effect):**

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <h2>{{ name() }}</h2>
    <p>{{ email() }}</p>
    <button (click)="handleClick()">Select</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  name = input.required<string>();
  email = input('');
  selected = output<string>();

  constructor() {
    effect(() => {
      console.log('Name changed:', this.name());
    });
  }

  handleClick() {
    this.selected.emit(this.name());
  }
}
```

**Why it matters:**

- `input.required<T>()` enforces required inputs at compile time

- `input(defaultValue)` provides type-inferred optional inputs

- `effect()` replaces `ngOnChanges` for reacting to input changes

- Signals integrate with OnPush for optimal performance

Reference: [https://angular.dev/guide/signals/inputs](https://angular.dev/guide/signals/inputs)

### 0.10 Use Signal Inputs for Route Parameters

**Impact: MEDIUM (Simpler routing, reactive route params)**

With `withComponentInputBinding()`, route parameters are automatically bound to component inputs. Combined with signal inputs, this eliminates manual `ActivatedRoute` subscriptions.

**Incorrect (Manual route parameter subscription):**

```typescript
@Component({
  template: `<h1>User {{ userId }}</h1>`
})
export class UserDetailComponent implements OnInit, OnDestroy {
  userId: string | null = null;
  private subscription?: Subscription;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.subscription = this.route.paramMap.subscribe((params) => {
      this.userId = params.get('id');
    });
  }

  ngOnDestroy() {
    this.subscription?.unsubscribe();
  }
}
```

**Correct (Signal input for route params):**

```typescript
// app.config.ts - Enable input binding
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes, withComponentInputBinding())
  ]
};

// Route: { path: 'users/:id', component: UserDetailComponent }
@Component({
  template: `<h1>User {{ id() }}</h1>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserDetailComponent {
  id = input.required<string>();  // Route param auto-bound
  userId = computed(() => parseInt(this.id(), 10));
}
```

**Why it matters:**

- No manual `ActivatedRoute` subscription management

- Route params, query params, and resolver data all become inputs

- Reactive updates when route changes

- Clean teardown handled automatically

Reference: [https://angular.dev/guide/routing](https://angular.dev/guide/routing)

### 0.11 Use Smart and Dumb Component Pattern

**Impact: MEDIUM (Separation of concerns improves testability, reusability, and maintainability)**

Separate components into "Smart" (container) components that handle logic/data and "Dumb" (presentational) components that only render UI. This improves testability, reusability, and makes change detection more efficient.

**Incorrect (God component doing everything):**

```typescript
// ❌ One component handles data, logic, AND presentation
@Component({
  selector: 'app-user-dashboard',
  template: `
    <div class="dashboard">
      <h1>Welcome, {{ user?.name }}</h1>
      @if (loading) {
        <div class="spinner">Loading...</div>
      }
      @for (order of orders; track order.id) {
        <div class="order-card" [class.urgent]="isUrgent(order)">
          <h3>Order #{{ order.id }}</h3>
          <p>{{ order.date | date }}</p>
          <p>{{ formatPrice(order.total) }}</p>
          <button (click)="cancelOrder(order)">Cancel</button>
          <button (click)="viewDetails(order)">Details</button>
        </div>
      }
      <form [formGroup]="filterForm" (ngSubmit)="applyFilters()">
        <!-- complex filter form -->
      </form>
    </div>
  `
})
export class UserDashboardComponent implements OnInit {
  user: User | null = null;
  orders: Order[] = [];
  loading = true;
  filterForm: FormGroup;

  constructor(
    private userService: UserService,
    private orderService: OrderService,
    private router: Router,
    private fb: FormBuilder,
    private analytics: AnalyticsService
  ) {
    this.filterForm = this.fb.group({...});
  }

  ngOnInit() {
    this.loadUser();
    this.loadOrders();
  }

  loadUser() { /* ... */ }
  loadOrders() { /* ... */ }
  isUrgent(order: Order): boolean { /* ... */ }
  formatPrice(price: number): string { /* ... */ }
  cancelOrder(order: Order) { /* ... */ }
  viewDetails(order: Order) { /* ... */ }
  applyFilters() { /* ... */ }
  // 500+ lines of mixed concerns
}
```

**Correct (Smart + Dumb separation):**

```typescript
// ✅ DUMB Component - single order card
@Component({
  selector: 'app-order-card',
  template: `
    <div class="order-card" [class.urgent]="isUrgent()">
      <h3>Order #{{ order().id }}</h3>
      <p>{{ order().date | date }}</p>
      <p>{{ order().total | currency }}</p>
      <button (click)="cancel.emit()">Cancel</button>
      <button (click)="viewDetails.emit()">Details</button>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OrderCardComponent {
  order = input.required<Order>();

  cancel = output<void>();
  viewDetails = output<void>();

  // Pure computation, no side effects
  isUrgent = computed(() => {
    const daysOld = this.getDaysOld(this.order().date);
    return this.order().status === 'pending' && daysOld > 3;
  });

  private getDaysOld(date: Date): number {
    return Math.floor((Date.now() - date.getTime()) / (1000 * 60 * 60 * 24));
  }
}
```

---

**Characteristics:**

| Aspect | Smart (Container) | Dumb (Presentational) |

|--------|-------------------|----------------------|

| Services | Injects services | No services |

| State | Manages state | Receives via @Input |

| Side effects | Makes HTTP calls, navigates | Emits events via @Output |

| Reusability | App-specific | Highly reusable |

| Testing | Integration tests | Unit tests (easy) |

| Change Detection | May use Default | Always use OnPush |

---

**File structure recommendation:**

```typescript
features/
└── orders/
    ├── containers/                  # Smart components
    │   └── order-dashboard/
    │       └── order-dashboard.component.ts
    ├── components/                  # Dumb components
    │   ├── order-list/
    │   │   └── order-list.component.ts
    │   ├── order-card/
    │   │   └── order-card.component.ts
    │   └── order-filters/
    │       └── order-filters.component.ts
    ├── services/
    │   └── order.service.ts
    └── orders.routes.ts
```

**Why it matters:**

- Dumb components are easy to unit test (no mocking services)

- Dumb components are reusable across features

- OnPush works perfectly with input-only components

- Clear data flow makes debugging easier

- Smart components are easier to integration test

Reference: [https://angular.dev/guide/components](https://angular.dev/guide/components)

---

## 1. Change Detection

**Impact: CRITICAL**

Change detection is the #1 performance factor in Angular. Using OnPush strategy, Signals, and proper zone management can dramatically reduce unnecessary checks.

### 1.1 Detach Change Detector for Heavy Operations

**Impact: CRITICAL (Eliminates change detection during computation)**

For components with heavy computations or animations, detaching the change detector excludes the component from change detection cycles. Reattach when updates are needed.

**Incorrect (Change detection runs during animation):**

```typescript
@Component({
  selector: 'app-animation',
  template: `<canvas #canvas></canvas>`
})
export class AnimationComponent implements OnInit {
  @ViewChild('canvas') canvas!: ElementRef<HTMLCanvasElement>;

  ngOnInit() {
    this.animate();
  }

  animate() {
    this.drawFrame();
    requestAnimationFrame(() => this.animate());
    // Each frame causes unnecessary change detection
  }
}
```

**Correct (Detach during animation):**

```typescript
@Component({
  selector: 'app-animation',
  template: `
    <canvas #canvas></canvas>
    <p>FPS: {{ fps }}</p>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AnimationComponent implements OnInit {
  @ViewChild('canvas') canvas!: ElementRef<HTMLCanvasElement>;
  fps = 0;

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.cdr.detach();  // Exclude from change detection
    this.animate();
    this.updateFps();
  }

  animate() {
    this.drawFrame();
    requestAnimationFrame(() => this.animate());
  }

  updateFps() {
    setInterval(() => {
      this.cdr.detectChanges();  // Manual update only when needed
    }, 1000);
  }
}
```

**Why it matters:**

- `detach()` excludes component from all automatic checks

- `detectChanges()` triggers manual check when needed

- Ideal for canvas animations, games, real-time visualizations

- Remember to `reattach()` in `ngOnDestroy` if needed

Reference: [https://angular.dev/api/core/ChangeDetectorRef](https://angular.dev/api/core/ChangeDetectorRef)

### 1.2 Run Non-UI Code Outside NgZone

**Impact: CRITICAL (Prevents unnecessary change detection triggers)**

NgZone patches async APIs to trigger change detection. For code that doesn't affect the UI, running outside the zone prevents unnecessary cycles.

**Incorrect (Event listener triggers change detection):**

```typescript
@Component({
  selector: 'app-scroll-tracker',
  template: `<div>Scroll position logged to console</div>`
})
export class ScrollTrackerComponent implements OnInit {
  ngOnInit() {
    // Every scroll event triggers change detection
    window.addEventListener('scroll', this.onScroll);
  }

  onScroll = () => {
    console.log('Scroll:', window.scrollY);  // No UI update needed
  };
}
```

**Correct (Run outside zone, enter for UI updates):**

```typescript
@Component({
  selector: 'app-scroll-tracker',
  template: `<div>Scroll position: {{ scrollPosition }}</div>`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ScrollTrackerComponent implements OnInit {
  scrollPosition = 0;

  constructor(
    private ngZone: NgZone,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.ngZone.runOutsideAngular(() => {
      window.addEventListener('scroll', this.onScroll);
    });
  }

  onScroll = () => {
    const newPosition = window.scrollY;
    if (Math.abs(newPosition - this.scrollPosition) > 100) {
      this.ngZone.run(() => {
        this.scrollPosition = newPosition;
        this.cdr.markForCheck();
      });
    }
  };
}
```

**Why it matters:**

- `runOutsideAngular()` prevents change detection triggers

- `run()` re-enters the zone for UI updates

- Use for scroll/resize/mousemove listeners

- Use for WebSocket connections and polling

Reference: [https://angular.dev/api/core/NgZone](https://angular.dev/api/core/NgZone)

### 1.3 Use Angular Signals for Reactive State

**Impact: CRITICAL (Fine-grained reactivity, automatic optimization)**

Signals provide fine-grained reactivity where only components reading a signal are updated when it changes. This eliminates the need for manual `ChangeDetectorRef` calls.

**Incorrect (Manual change detection with OnPush):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <p>Count: {{ count }}</p>
    <p>Double: {{ count * 2 }}</p>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  count = 0;

  constructor(private cdr: ChangeDetectorRef) {}

  increment() {
    this.count++;
    this.cdr.markForCheck(); // Manual trigger required
  }
}
```

**Correct (Signals with automatic change detection):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <p>Count: {{ count() }}</p>
    <p>Double: {{ doubleCount() }}</p>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
    // No markForCheck needed - signals handle it automatically
  }
}
```

**Why it matters:**

- Signals automatically notify Angular when values change

- `computed()` creates derived values that update reactively

- No manual `ChangeDetectorRef` management needed

- Works seamlessly with OnPush change detection

Reference: [https://angular.dev/guide/signals](https://angular.dev/guide/signals)

### 1.4 Use OnPush Change Detection Strategy

**Impact: CRITICAL (2-10x fewer change detection cycles)**

By default, Angular checks every component on each change detection cycle. OnPush limits checks to when inputs change by reference, events occur, or async pipes emit.

**Incorrect (Default checks on every cycle):**

```typescript
@Component({
  selector: 'app-user-list',
  template: `
    @for (user of users; track user.id) {
      <!-- formatDate called on EVERY change detection cycle -->
      <span>{{ formatDate(user.created) }}</span>
    }
  `
})
export class UserListComponent {
  @Input() users: User[] = [];

  formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US').format(date);
  }
}
```

**Correct (OnPush limits checks):**

```typescript
@Component({
  selector: 'app-user-list',
  template: `
    @for (user of users; track user.id) {
      <span>{{ user.created | date }}</span>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  @Input() users: User[] = [];
  // Component only checks when users reference changes
  // Use pure pipes instead of methods in templates
}
```

**Why it matters:**

- Component only re-renders when inputs change by reference

- Events within the component trigger checks

- Async pipe emissions trigger checks

- Must update inputs immutably (new array, not mutation)

Reference: [https://angular.dev/best-practices/skipping-subtrees](https://angular.dev/best-practices/skipping-subtrees)

---

## 2. Bundle & Lazy Loading

**Impact: CRITICAL**

Standalone components, @defer blocks, and lazy loading improve Time to Interactive. Angular 20+ defaults to standalone.

### 2.1 Avoid Barrel File Imports

**Impact: HIGH (Direct imports enable tree-shaking, reducing bundle size up to 30%)**

Barrel files (index.ts) re-export multiple modules from a single entry point. While convenient, they prevent effective tree-shaking and increase bundle size significantly.

**Incorrect (Barrel imports):**

```typescript
// Even worse - wildcard imports
import * as Services from './services';

// Using only one service, but entire barrel is included
constructor(private userService: Services.UserService) {}
```

**Correct (Direct imports):**

```typescript
// For commonly used utilities, create small focused barrels
// utils/date/index.ts - small, focused barrel (OK)
export { formatDate } from './format-date';
export { parseDate } from './parse-date';

// utils/string/index.ts - separate barrel for strings
export { capitalize } from './capitalize';
export { truncate } from './truncate';

// Instead of one massive utils/index.ts
```

**Correct (Package exports for libraries):**

```typescript
// Consumer code - tree-shakeable imports
import { Button } from '@myorg/ui-components/button';
// Only button code is bundled
```

**Project structure recommendation:**

```typescript
// ❌ Avoid: One massive barrel
src/
├── services/
│   ├── index.ts         // exports 30 services
│   ├── user.service.ts
│   └── ...

// ✅ Better: No barrels, direct imports
src/
├── services/
│   ├── user.service.ts      // import directly
│   ├── auth.service.ts      // import directly
│   └── ...

// ✅ Also OK: Feature-based small barrels
src/
├── features/
│   ├── user/
│   │   ├── index.ts         // only user-related exports
│   │   ├── user.service.ts
│   │   └── user.component.ts
│   └── auth/
│       ├── index.ts         // only auth-related exports
│       └── auth.service.ts
```

**IDE tip - auto-imports:**

```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  // Prevents IDE from auto-importing from barrels
  "typescript.preferences.autoImportFileExcludePatterns": [
    "**/index.ts",
    "**/index"
  ]
}
```

**Why it matters:**

- Barrel files create complex dependency graphs that confuse bundlers

- `export *` syntax is especially problematic for tree-shaking

- Real-world impact: 30% bundle size reduction by switching to direct imports

- Build times also improve (15-70% faster) with simpler module graphs

**Exceptions where barrels are OK:**

- Published npm packages with explicit `exports` in package.json

- Small, cohesive feature modules (under 5 exports)

- Public API boundaries that rarely change

Reference: [https://webpack.js.org/guides/tree-shaking/](https://webpack.js.org/guides/tree-shaking/)

### 2.2 Defer Non-Critical Third-Party Scripts

**Impact: MEDIUM (Loads analytics/tracking after hydration for faster TTI)**

Analytics, error tracking, chat widgets, and other non-critical third-party scripts don't need to block initial render. Use `@defer` to load them after hydration completes.

**Incorrect (blocks initial bundle):**

```typescript
// ❌ Analytics component loads in main bundle
import { AnalyticsComponent } from './analytics.component';
import { ChatWidgetComponent } from './chat-widget.component';
import { ErrorTrackingComponent } from './error-tracking.component';

@Component({
  selector: 'app-root',
  template: `
    <app-header />
    <router-outlet />
    <app-footer />

    <!-- These load immediately, blocking TTI -->
    <app-analytics />
    <app-chat-widget />
    <app-error-tracking />
  `,
  imports: [
    AnalyticsComponent,      // Included in main bundle
    ChatWidgetComponent,     // Included in main bundle
    ErrorTrackingComponent   // Included in main bundle
  ]
})
export class AppComponent {}
```

**Correct (defer with @defer):**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <app-header />
    <router-outlet />
    <app-footer />

    <!-- ✅ Loads AFTER hydration completes -->
    @defer (on idle) {
      <app-analytics />
    }

    @defer (on idle) {
      <app-chat-widget />
    }

    @defer (on idle) {
      <app-error-tracking />
    }
  `,
  imports: [HeaderComponent, FooterComponent]
  // Analytics, ChatWidget, ErrorTracking NOT in imports - loaded dynamically
})
export class AppComponent {}
```

**With timer delay:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <router-outlet />

    <!-- Load after 3 seconds idle time -->
    @defer (on idle; when isHydrated) {
      <app-analytics />
      <app-intercom-chat />
    } @placeholder {
      <!-- Nothing shown while waiting -->
    }
  `
})
export class AppComponent {
  isHydrated = signal(false);

  constructor() {
    afterNextRender(() => {
      this.isHydrated.set(true);
    });
  }
}
```

**For heavy libraries (charts, maps):**

```typescript
@Component({
  selector: 'app-dashboard',
  template: `
    <div class="metrics">
      <app-kpi-cards [data]="kpiData()" />
    </div>

    <!-- Heavy chart library deferred until visible -->
    @defer (on viewport) {
      <app-revenue-chart [data]="chartData()" />
    } @placeholder {
      <div class="chart-skeleton">
        <div class="skeleton-bar"></div>
      </div>
    } @loading (minimum 200ms) {
      <app-spinner />
    }

    <!-- Map only loads when user scrolls to it -->
    @defer (on viewport) {
      <app-location-map [markers]="locations()" />
    } @placeholder {
      <div class="map-placeholder">
        <img src="assets/map-preview.webp" alt="Map preview" />
      </div>
    }
  `
})
export class DashboardComponent {}
```

**Third-party script loading pattern:**

```typescript
// Service to load third-party scripts on demand
@Injectable({ providedIn: 'root' })
export class ThirdPartyService {
  private loaded = new Map<string, Promise<void>>();

  loadScript(src: string): Promise<void> {
    if (this.loaded.has(src)) {
      return this.loaded.get(src)!;
    }

    const promise = new Promise<void>((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Failed to load ${src}`));
      document.body.appendChild(script);
    });

    this.loaded.set(src, promise);
    return promise;
  }
}

// Analytics component that loads external script
@Component({
  selector: 'app-analytics',
  template: ``,
  standalone: true
})
export class AnalyticsComponent {
  private thirdParty = inject(ThirdPartyService);

  constructor() {
    afterNextRender(async () => {
      await this.thirdParty.loadScript('https://analytics.example.com/script.js');
      window.analytics?.init({ key: environment.analyticsKey });
    });
  }
}
```

**SSR hydration-aware loading:**

```typescript
@Component({
  selector: 'app-root',
  template: `
    <router-outlet />

    <!-- Only load on client, after hydration -->
    @defer (on idle; hydrate never) {
      <app-client-only-widget />
    }

    <!-- Prefetch during idle, hydrate on interaction -->
    @defer (on interaction; prefetch on idle; hydrate on interaction) {
      <app-feedback-widget />
    }
  `
})
export class AppComponent {}
```

**Priority guidelines:**

| Third-party | Priority | Defer Strategy |

|-------------|----------|----------------|

| Analytics | Low | `@defer (on idle)` after 2-3s |

| Error tracking | Low | `@defer (on idle)` |

| Chat widget | Low | `@defer (on idle)` or `(on viewport)` |

| Social embeds | Low | `@defer (on viewport)` |

| Maps | Medium | `@defer (on viewport)` |

| Video players | Medium | `@defer (on viewport)` |

| A/B testing | High | Load in main bundle (affects content) |

| Auth providers | High | Load in main bundle (blocks UX) |

**Why it matters:**

- Third-party scripts often add 100KB+ to initial bundle

- Analytics don't affect user experience - defer them

- Faster Time to Interactive (TTI) improves Core Web Vitals

- Users can interact sooner with the critical UI

Reference: [https://angular.dev/guide/defer](https://angular.dev/guide/defer)

### 2.3 Lazy Load Routes with loadComponent

**Impact: CRITICAL (40-70% initial bundle reduction)**

Lazy loading splits your application into smaller chunks loaded on demand. Use `loadComponent` for standalone components to reduce initial bundle size.

**Incorrect (Eagerly loaded routes):**

```typescript
import { DashboardComponent } from './dashboard/dashboard.component';
import { SettingsComponent } from './settings/settings.component';
import { ReportsComponent } from './reports/reports.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'settings', component: SettingsComponent },
  { path: 'reports', component: ReportsComponent }
  // All components loaded upfront, even if never visited
];
```

**Correct (Lazy loaded routes):**

```typescript
export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'settings',
    loadComponent: () =>
      import('./settings/settings.component').then(m => m.SettingsComponent)
  },
  {
    path: 'reports',
    loadChildren: () =>
      import('./reports/reports.routes').then(m => m.REPORTS_ROUTES)
  }
];
```

**Why it matters:**

- Initial bundle only includes code for first route

- Other routes downloaded on navigation

- `loadComponent` for single components

- `loadChildren` for route groups

Reference: [https://angular.dev/guide/routing/common-router-tasks#lazy-loading](https://angular.dev/guide/routing/common-router-tasks#lazy-loading)

### 2.4 Use @defer for Lazy Loading Components

**Impact: CRITICAL (Defers loading until needed, reduces initial bundle)**

`@defer` delays loading of heavy components until a trigger condition is met, reducing initial bundle size without route changes.

**Incorrect (Heavy components loaded immediately):**

```typescript
@Component({
  selector: 'app-dashboard',
  imports: [HeavyChartComponent, DataTableComponent],
  template: `
    <h1>Dashboard</h1>

    <!-- Chart library loaded even if user never scrolls down -->
    <app-heavy-chart [data]="chartData" />

    <!-- Large table always in initial bundle -->
    <app-data-table [rows]="tableData" />
  `
})
export class DashboardComponent {}
```

**Correct (Defer loading until needed):**

```typescript
@Component({
  selector: 'app-dashboard',
  imports: [HeavyChartComponent, DataTableComponent],
  template: `
    <h1>Dashboard</h1>

    @defer (on viewport) {
      <app-heavy-chart [data]="chartData" />
    } @placeholder {
      <div class="chart-skeleton">Loading chart...</div>
    }

    @defer (on interaction) {
      <app-data-table [rows]="tableData" />
    } @placeholder {
      <button>Click to load data table</button>
    }
  `
})
export class DashboardComponent {}
```

**Why it matters:**

- `on viewport` - Loads when element enters viewport (scroll-triggered)

- `on interaction` - Loads on click/focus (user-triggered)

- `on idle` - Loads when browser is idle (background loading)

- `@placeholder` shows fallback content until loaded

Reference: [https://angular.dev/guide/defer](https://angular.dev/guide/defer)

### 2.5 Use Preload Strategies for Lazy Modules

**Impact: CRITICAL (Improves navigation performance)**

Preloading downloads lazy-loaded modules in the background after initial load, making subsequent navigation instant.

**Incorrect (No preloading causes navigation delay):**

```typescript
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes)
    // No preloading - modules load on demand
    // User experiences delay on first navigation
  ]
};
```

**Correct (Preload all modules after initial load):**

```typescript
import { provideRouter, withPreloading, PreloadAllModules } from '@angular/router';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withPreloading(PreloadAllModules)
    )
  ]
};
```

**Why it matters:**

- `PreloadAllModules` loads all routes after initial render

- Navigation to lazy routes becomes instant

- Initial load is not affected (preloading happens after)

- Custom strategies can preload selectively

Reference: [https://angular.dev/guide/routing/common-router-tasks#preloading](https://angular.dev/guide/routing/common-router-tasks#preloading)

### 2.6 Use Standalone Components

**Impact: CRITICAL (Better tree-shaking, simpler architecture)**

Standalone components don't require NgModules, enabling better tree-shaking and granular lazy loading. In Angular v19+, components are standalone by default.

**Incorrect (NgModule-based with implicit dependencies):**

```typescript
@NgModule({
  declarations: [UserListComponent, UserDetailComponent],
  imports: [CommonModule, SharedModule],
  exports: [UserListComponent]
})
export class UserModule {}

@Component({
  selector: 'app-user-list',
  template: `...`
})
export class UserListComponent {}
// Dependencies come from module - not explicit
```

**Correct (Standalone with explicit imports):**

```typescript
@Component({
  selector: 'app-user-list',
  // No standalone: true needed in v19+
  imports: [RouterLink, UserAvatarComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (user of users(); track user.id) {
      <app-user-avatar [user]="user" />
      <a [routerLink]="['/users', user.id]">{{ user.name }}</a>
    }
  `
})
export class UserListComponent {
  private userService = inject(UserService);
  users = toSignal(this.userService.getUsers(), { initialValue: [] });
}
```

**Why it matters:**

- Dependencies explicit in component's `imports` array

- Better tree-shaking (unused components excluded)

- No NgModule boilerplate needed

- Components are standalone by default in v19+

Reference: [https://angular.dev/guide/components/importing](https://angular.dev/guide/components/importing)

---

## 3. RxJS Optimization

**Impact: HIGH**

Proper RxJS usage with takeUntilDestroyed, async pipe, and efficient operators prevents memory leaks and reduces computations.

### 3.1 Avoid Nested Subscriptions

**Impact: HIGH (Nested subscribes cause memory leaks, callback hell, and missed errors)**

Nesting subscribe() calls inside other subscribe() callbacks creates callback hell, memory leaks, and makes error handling difficult. Use RxJS operators to compose streams instead.

**Incorrect (Nested subscriptions):**

```typescript
// ❌ Callback hell, inner subscription never cleaned up
@Component({...})
export class OrderDetailsComponent implements OnInit {
  ngOnInit() {
    this.route.params.subscribe(params => {
      this.orderService.getOrder(params['id']).subscribe(order => {
        this.order = order;
        this.userService.getUser(order.userId).subscribe(user => {
          this.user = user;
          this.addressService.getAddress(user.addressId).subscribe(address => {
            this.address = address;
            // 4 levels deep, impossible to maintain
            // Memory leak: inner subscriptions never unsubscribed
          });
        });
      });
    });
  }
}
```

**Correct (Use operators to compose):**

```typescript
// ✅ Flat, readable, properly managed
@Component({...})
export class OrderDetailsComponent implements OnDestroy {
  private destroy$ = new Subject<void>();

  order$ = this.route.params.pipe(
    map(params => params['id']),
    switchMap(id => this.orderService.getOrder(id)),
    takeUntil(this.destroy$)
  );

  user$ = this.order$.pipe(
    switchMap(order => this.userService.getUser(order.userId))
  );

  address$ = this.user$.pipe(
    switchMap(user => this.addressService.getAddress(user.addressId))
  );

  // Or combine all data into one stream
  vm$ = this.route.params.pipe(
    map(params => params['id']),
    switchMap(id => this.orderService.getOrder(id)),
    switchMap(order => forkJoin({
      order: of(order),
      user: this.userService.getUser(order.userId)
    })),
    switchMap(({ order, user }) => forkJoin({
      order: of(order),
      user: of(user),
      address: this.addressService.getAddress(user.addressId)
    })),
    takeUntil(this.destroy$)
  );

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**Even better (Angular 16+ with takeUntilDestroyed):**

```typescript
// ✅ Cleanest approach with modern Angular
@Component({...})
export class OrderDetailsComponent {
  private destroyRef = inject(DestroyRef);

  vm$ = this.route.params.pipe(
    map(params => params['id']),
    switchMap(id => this.loadOrderWithDetails(id)),
    takeUntilDestroyed(this.destroyRef)
  );

  private loadOrderWithDetails(orderId: string) {
    return this.orderService.getOrder(orderId).pipe(
      switchMap(order =>
        combineLatest({
          order: of(order),
          user: this.userService.getUser(order.userId),
          address: this.getAddressForOrder(order)
        })
      )
    );
  }
}
```

---

**Incorrect (Nested subscribe for conditional logic):**

```typescript
// ❌ Nested subscribe for conditional fetch
this.authService.currentUser$.subscribe(user => {
  if (user) {
    this.userService.getProfile(user.id).subscribe(profile => {
      this.profile = profile;
    });
  }
});
```

**Correct (Use filter and switchMap):**

```typescript
// ✅ Operators handle the conditional
this.authService.currentUser$.pipe(
  filter((user): user is User => user !== null),
  switchMap(user => this.userService.getProfile(user.id)),
  takeUntilDestroyed()
).subscribe(profile => {
  this.profile = profile;
});
```

---

**Incorrect (Subscribe to trigger side effects):**

```typescript
// ❌ Subscribe just to call another method
this.items$.subscribe(items => {
  this.processItems(items).subscribe(result => {
    this.saveResult(result).subscribe(() => {
      console.log('Done');
    });
  });
});
```

**Correct (Chain with operators):**

```typescript
// ✅ Single subscription with operator chain
this.items$.pipe(
  concatMap(items => this.processItems(items)),
  concatMap(result => this.saveResult(result)),
  takeUntilDestroyed()
).subscribe({
  next: () => console.log('Done'),
  error: (err) => console.error('Pipeline failed:', err)
});
```

---

**Common operator patterns:**

```typescript
// Sequential dependent calls
a$.pipe(
  switchMap(a => b$(a)),
  switchMap(b => c$(b))
)

// Parallel independent calls
forkJoin({ a: a$, b: b$, c: c$ })

// Parallel then combine
combineLatest([a$, b$]).pipe(
  map(([a, b]) => ({ ...a, ...b }))
)

// Conditional based on value
source$.pipe(
  switchMap(value =>
    value.needsExtra
      ? fetchExtra(value).pipe(map(extra => ({ ...value, extra })))
      : of(value)
  )
)
```

**Why it matters:**

- Inner subscriptions don't auto-unsubscribe when outer completes

- Error in inner stream doesn't propagate to outer

- Impossible to cancel/retry the whole chain

- Code becomes unreadable and untestable

Reference: [https://blog.angular-university.io/rxjs-error-handling/](https://blog.angular-university.io/rxjs-error-handling/)

### 3.2 Share Observables to Avoid Duplicate Requests

**Impact: HIGH (Eliminates redundant HTTP calls)**

When multiple subscribers consume the same observable, each subscription triggers a new execution. Use `shareReplay` to share results among subscribers.

**Incorrect (Each async pipe triggers separate request):**

```typescript
@Component({
  template: `
    <!-- 3 async pipes = 3 HTTP requests! -->
    <h1>{{ (user$ | async)?.name }}</h1>
    <p>{{ (user$ | async)?.email }}</p>
    <img [src]="(user$ | async)?.avatar" />
  `
})
export class UserProfileComponent {
  user$ = this.http.get<User>('/api/user');
}
```

**Correct (Share observable among subscribers):**

```typescript
@Component({
  template: `
    @if (user$ | async; as user) {
      <h1>{{ user.name }}</h1>
      <p>{{ user.email }}</p>
      <img [src]="user.avatar" />
    }
  `
})
export class UserProfileComponent {
  user$ = this.http.get<User>('/api/user').pipe(
    shareReplay({ bufferSize: 1, refCount: true })
  );
}
```

**Why it matters:**

- `bufferSize: 1` caches the latest value

- `refCount: true` unsubscribes when no subscribers remain

- Single HTTP request shared among all async pipes

- Alternative: use `@if (obs | async; as value)` pattern

Reference: [https://rxjs.dev/api/operators/shareReplay](https://rxjs.dev/api/operators/shareReplay)

### 3.3 Use Async Pipe Instead of Manual Subscribe

**Impact: HIGH (Automatic cleanup, better change detection)**

The async pipe automatically subscribes and unsubscribes from observables, preventing memory leaks and working seamlessly with OnPush change detection.

**Incorrect (Manual subscription with leak potential):**

```typescript
@Component({
  template: `
    @if (user) {
      <h1>{{ user.name }}</h1>
    }
  `
})
export class UserProfileComponent implements OnInit, OnDestroy {
  user: User | null = null;
  private subscription!: Subscription;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.subscription = this.userService.getCurrentUser()
      .subscribe(user => this.user = user);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();  // Easy to forget
  }
}
```

**Correct (Async pipe handles lifecycle):**

```typescript
@Component({
  imports: [AsyncPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @if (user$ | async; as user) {
      <h1>{{ user.name }}</h1>
    }
  `
})
export class UserProfileComponent {
  user$ = inject(UserService).getCurrentUser();
  // No manual subscribe/unsubscribe needed
}
```

**Why it matters:**

- No manual `Subscription` management

- No `ngOnDestroy` cleanup needed

- Works perfectly with OnPush change detection

- Declarative and testable

Reference: [https://angular.dev/api/common/AsyncPipe](https://angular.dev/api/common/AsyncPipe)

### 3.4 Use Correct RxJS Mapping Operators

**Impact: HIGH (Wrong operator causes race conditions, memory leaks, or dropped requests)**

Choosing the wrong higher-order mapping operator (switchMap, exhaustMap, concatMap, mergeMap) causes race conditions, duplicate requests, or lost data. Each has a specific use case.

**Quick Reference:**

| Operator | Behavior | Use When |

|----------|----------|----------|

| `switchMap` | Cancels previous, uses latest | Search, typeahead, GET requests |

| `exhaustMap` | Ignores new until current completes | Form submit, prevent double-click |

| `concatMap` | Queues in order, sequential | Ordered operations, writes |

| `mergeMap` | All run in parallel | Independent parallel tasks |

---

**Incorrect (Wrong operator for search):**

```typescript
// ❌ mergeMap - All requests run parallel, results arrive out of order
searchControl.valueChanges.pipe(
  mergeMap(query => this.searchService.search(query))
).subscribe(results => {
  this.results = results; // May show stale results from slow old request!
});

// ❌ concatMap - Queues all requests, user waits for old queries
searchControl.valueChanges.pipe(
  concatMap(query => this.searchService.search(query))
).subscribe(results => {
  this.results = results; // Slow - waits for each request sequentially
});
```

**Correct (switchMap for search):**

```typescript
// ✅ switchMap - Cancels previous request, only latest matters
searchControl.valueChanges.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap(query => this.searchService.search(query))
).subscribe(results => {
  this.results = results; // Always shows results for latest query
});
```

---

**Incorrect (Wrong operator for form submit):**

```typescript
// ❌ switchMap - User double-clicks, first submit is cancelled!
submitForm$.pipe(
  switchMap(() => this.orderService.placeOrder(this.form.value))
).subscribe();
// First order never placed if user clicks twice quickly

// ❌ mergeMap - Both submits go through, duplicate orders!
submitForm$.pipe(
  mergeMap(() => this.orderService.placeOrder(this.form.value))
).subscribe();
// User gets charged twice
```

**Correct (exhaustMap for form submit):**

```typescript
// ✅ exhaustMap - Ignores clicks while request is pending
submitForm$.pipe(
  exhaustMap(() => {
    this.isSubmitting = true;
    return this.orderService.placeOrder(this.form.value).pipe(
      finalize(() => this.isSubmitting = false)
    );
  })
).subscribe({
  next: (order) => this.router.navigate(['/order', order.id]),
  error: (err) => this.showError(err)
});
// Double-clicks ignored, only one order placed
```

---

**Incorrect (Wrong operator for sequential writes):**

```typescript
// ❌ switchMap - Later items cancel earlier ones!
itemsToSave$.pipe(
  switchMap(item => this.saveItem(item))
).subscribe();
// Only last item gets saved

// ❌ mergeMap - Order not guaranteed, race conditions
itemsToSave$.pipe(
  mergeMap(item => this.saveItem(item))
).subscribe();
// Items may save out of order, causing data inconsistency
```

**Correct (concatMap for sequential writes):**

```typescript
// ✅ concatMap - Each completes before next starts
itemsToSave$.pipe(
  concatMap(item => this.saveItem(item))
).subscribe({
  complete: () => console.log('All items saved in order')
});
// Guaranteed order: item1 saved, then item2, then item3...
```

---

**Correct (mergeMap for parallel independent operations):**

```typescript
// ✅ mergeMap - When order doesn't matter and parallel is faster
notificationIds$.pipe(
  mergeMap(
    id => this.markAsRead(id),
    5 // Optional: limit concurrent requests to 5
  )
).subscribe();
// All notifications marked as read in parallel, fastest completion
```

---

**Real-world patterns:**

```typescript
// Autocomplete with loading state
@Component({...})
export class SearchComponent {
  searchControl = new FormControl('');
  results$ = this.searchControl.valueChanges.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    filter(query => query.length >= 2),
    switchMap(query => this.search(query).pipe(
      startWith(null) // Emit null to show loading
    )),
    share()
  );
}

// Save with optimistic UI
saveItem(item: Item): Observable<Item> {
  return of(item).pipe( // Optimistic: return immediately
    tap(() => this.updateLocalState(item)),
    concatMap(() => this.api.save(item)), // Then persist
    catchError(err => {
      this.rollbackLocalState(item);
      return throwError(() => err);
    })
  );
}
```

**Why it matters:**

- `switchMap` + form submit = lost transactions

- `mergeMap` + search = race conditions showing wrong results

- `concatMap` + search = slow UX waiting for old requests

- `exhaustMap` + search = ignored user input

Reference: [https://blog.angular-university.io/rxjs-higher-order-mapping/](https://blog.angular-university.io/rxjs-higher-order-mapping/)

### 3.5 Use Efficient RxJS Operators

**Impact: HIGH (Prevents race conditions and unnecessary work)**

Choosing the right operator prevents race conditions and unnecessary work. Use `switchMap` for cancellable requests, `debounceTime` for user input.

**Incorrect (mergeMap causes race conditions):**

```typescript
@Component({...})
export class SearchComponent {
  searchControl = new FormControl('');

  results$ = this.searchControl.valueChanges.pipe(
    // mergeMap doesn't cancel previous requests
    // Results can arrive out of order
    mergeMap(query => this.searchService.search(query))
  );
}
```

**Correct (switchMap cancels previous, debounce reduces calls):**

```typescript
@Component({
  template: `
    <input [formControl]="searchControl" />
    @for (result of results$ | async; track result.id) {
      <div>{{ result.title }}</div>
    }
  `
})
export class SearchComponent {
  searchControl = new FormControl('');

  results$ = this.searchControl.valueChanges.pipe(
    debounceTime(300),                // Wait for typing to stop
    distinctUntilChanged(),            // Skip if same value
    filter(query => query.length > 2), // Min length
    switchMap(query =>                 // Cancel previous request
      this.searchService.search(query).pipe(
        catchError(() => of([]))
      )
    )
  );
}
```

**Why it matters:**

- `switchMap` - Only latest matters (search, autocomplete)

- `exhaustMap` - Ignore new until current completes (form submit)

- `concatMap` - Order matters, queue requests

- `mergeMap` - All results matter, order doesn't

Reference: [https://rxjs.dev/guide/operators](https://rxjs.dev/guide/operators)

### 3.6 Use takeUntilDestroyed for Cleanup

**Impact: HIGH (Prevents memory leaks automatically)**

`takeUntilDestroyed()` automatically unsubscribes when the component is destroyed, eliminating manual cleanup boilerplate.

**Incorrect (Manual Subject-based cleanup):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => this.processData(data));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
    // Boilerplate, easy to forget
  }
}
```

**Correct (takeUntilDestroyed handles cleanup):**

```typescript
@Component({...})
export class DataComponent {
  constructor() {
    // In constructor, DestroyRef is auto-injected
    this.dataService.getData()
      .pipe(takeUntilDestroyed())
      .subscribe(data => this.processData(data));
  }
}

// Or outside constructor:
export class DataComponent implements OnInit {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(data => this.processData(data));
  }
}
```

**Why it matters:**

- No `ngOnDestroy` boilerplate needed

- No manual `Subject` management

- Works with `DestroyRef` outside constructor

- `toSignal()` is even cleaner when possible

Reference: [https://angular.dev/api/core/rxjs-interop/takeUntilDestroyed](https://angular.dev/api/core/rxjs-interop/takeUntilDestroyed)

---

## 4. Template Performance

**Impact: HIGH**

New control flow (@for with track, @if) and pure pipes optimize rendering. NgOptimizedImage improves Core Web Vitals.

### 4.1 Avoid Function Calls in Templates

**Impact: CRITICAL (Functions run on every change detection cycle, causing severe performance issues)**

Calling functions directly in templates forces Angular to execute them on every change detection cycle, even if inputs haven't changed. This can cause hundreds of unnecessary executions per second.

**Incorrect (Function called on every cycle):**

```typescript
@Component({
  selector: 'app-user-card',
  template: `
    <div class="user">
      <!-- getFullName() runs 100+ times on scroll, clicks, any event -->
      <h2>{{ getFullName() }}</h2>
      <span>{{ calculateAge(user.birthDate) }}</span>
      <p>{{ formatAddress(user.address) }}</p>
    </div>
  `
})
export class UserCardComponent {
  @Input() user!: User;

  getFullName(): string {
    console.log('getFullName called'); // Logs hundreds of times!
    return `${this.user.firstName} ${this.user.lastName}`;
  }

  calculateAge(birthDate: Date): number {
    const today = new Date();
    return today.getFullYear() - birthDate.getFullYear();
  }

  formatAddress(address: Address): string {
    return `${address.street}, ${address.city}`;
  }
}
```

**Correct (Use pipes or computed values):**

```typescript
// Option 1: Pure Pipe (recommended for reusable transformations)
@Pipe({ name: 'fullName', standalone: true, pure: true })
export class FullNamePipe implements PipeTransform {
  transform(user: User): string {
    return `${user.firstName} ${user.lastName}`;
  }
}

@Pipe({ name: 'age', standalone: true, pure: true })
export class AgePipe implements PipeTransform {
  transform(birthDate: Date): number {
    return new Date().getFullYear() - birthDate.getFullYear();
  }
}

@Component({
  selector: 'app-user-card',
  template: `
    <div class="user">
      <!-- Pipes only run when input changes -->
      <h2>{{ user | fullName }}</h2>
      <span>{{ user.birthDate | age }}</span>
      <p>{{ user.address.street }}, {{ user.address.city }}</p>
    </div>
  `,
  imports: [FullNamePipe, AgePipe],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  @Input() user!: User;
}

// Option 2: Computed signal (Angular 16+)
@Component({
  selector: 'app-user-card',
  template: `
    <div class="user">
      <h2>{{ fullName() }}</h2>
      <span>{{ age() }}</span>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  user = input.required<User>();

  fullName = computed(() =>
    `${this.user().firstName} ${this.user().lastName}`
  );

  age = computed(() =>
    new Date().getFullYear() - this.user().birthDate.getFullYear()
  );
}
```

**Why it matters:**

- Pure pipes are memoized - only re-execute when inputs change by reference

- Computed signals track dependencies automatically

- Without this, a list of 100 items with 3 functions = 300+ calls per change detection

- Common symptom: app feels "janky" or slow during scrolling/typing

**When functions ARE acceptable:**

- Event handlers: `(click)="handleClick()"` - only called on actual events

- Template reference variables: `#input` with `input.value`

Reference: [https://angular.dev/guide/pipes](https://angular.dev/guide/pipes)

### 4.2 Use @for with track for Loops

**Impact: HIGH (Prevents unnecessary DOM recreation)**

`@for` requires a `track` expression, enforcing efficient DOM reuse. Without tracking, Angular recreates all DOM elements when the array changes.

**Incorrect (No tracking causes full DOM recreation):**

```typescript
@Component({
  template: `
    <!-- All items re-render when array changes -->
    <div *ngFor="let user of users">
      <app-user-card [user]="user" />
    </div>
  `
})
export class UserListComponent {
  users: User[] = [];
}
```

**Correct (@for with required track):**

```typescript
@Component({
  template: `
    @for (user of users(); track user.id) {
      <app-user-card [user]="user" />
    } @empty {
      <p>No users found</p>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  users = signal<User[]>([]);
}
```

**Why it matters:**

- `track user.id` identifies items for DOM reuse

- Only changed items are re-rendered, not the entire list

- `@empty` block handles empty array case

- Required `track` prevents accidental performance issues

Reference: [https://angular.dev/guide/templates/control-flow](https://angular.dev/guide/templates/control-flow)

### 4.3 Use NgOptimizedImage for Images

**Impact: HIGH (LCP improvement, automatic lazy loading)**

`NgOptimizedImage` enforces image best practices: automatic lazy loading, priority hints for LCP images, and prevents layout shift.

**Incorrect (Native img without optimization):**

```html
<!-- No lazy loading, no priority hints, potential CLS -->
<img src="/assets/hero.jpg" alt="Hero image">

<!-- May cause layout shift without dimensions -->
<img src="{{ user.avatar }}" alt="User avatar">
```

**Correct (NgOptimizedImage with best practices):**

```typescript
@Component({
  imports: [NgOptimizedImage],
  template: `
    <!-- Priority image (above fold, LCP candidate) -->
    <img
      ngSrc="/assets/hero.jpg"
      alt="Hero image"
      width="1200"
      height="600"
      priority
    />

    <!-- Lazy loaded by default (below fold) -->
    <img
      [ngSrc]="user().avatar"
      alt="User avatar"
      width="64"
      height="64"
    />
  `
})
export class ProductComponent {
  user = input.required<User>();
}
```

**Why it matters:**

- `priority` attribute for above-fold images (LCP)

- Automatic lazy loading for below-fold images

- Required `width`/`height` prevents layout shift

- `fill` mode available for dynamic containers

Reference: [https://angular.dev/guide/image-optimization](https://angular.dev/guide/image-optimization)

### 4.4 Use Pure Pipes for Data Transformation

**Impact: HIGH (Memoized computation, called only when input changes)**

Pure pipes are only executed when inputs change by reference. They're memoized, unlike template methods which run on every change detection cycle.

**Incorrect (Method called on every change detection):**

```typescript
@Component({
  template: `
    @for (product of products; track product.id) {
      <!-- formatPrice called on EVERY change detection cycle -->
      <span>{{ formatPrice(product.price) }}</span>
    }
  `
})
export class ProductListComponent {
  formatPrice(price: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  }
}
```

**Correct (Pure pipe only runs when input changes):**

```typescript
@Pipe({ name: 'price' })
export class PricePipe implements PipeTransform {
  transform(value: number, currency = 'USD'): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency
    }).format(value);
  }
}

@Component({
  imports: [PricePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @for (product of products; track product.id) {
      <span>{{ product.price | price }}</span>
    }
  `
})
export class ProductListComponent {
  products = signal<Product[]>([]);
}
```

**Why it matters:**

- Pure pipes are memoized by Angular

- Only recalculate when input reference changes

- Methods in templates run on every change detection

- Significant performance gain in loops

Reference: [https://angular.dev/guide/pipes](https://angular.dev/guide/pipes)

### 4.5 Use Virtual Scrolling for Large Lists

**Impact: HIGH (Renders only visible items, reducing DOM nodes from 1000s to ~20)**

Rendering thousands of items creates thousands of DOM nodes, causing slow initial render, high memory usage, and janky scrolling. Virtual scrolling renders only visible items.

**Incorrect (Renders all items):**

```typescript
@Component({
  selector: 'app-product-list',
  template: `
    <!-- 10,000 products = 10,000 DOM nodes = slow & memory hungry -->
    <div class="product-list">
      @for (product of products; track product.id) {
        <app-product-card [product]="product" />
      }
    </div>
  `
})
export class ProductListComponent {
  products: Product[] = []; // 10,000 items loaded
}
```

**Correct (Virtual scrolling):**

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  selector: 'app-product-list',
  template: `
    <!-- Only ~10-20 visible items rendered at a time -->
    <cdk-virtual-scroll-viewport
      itemSize="80"
      class="product-list"
    >
      <app-product-card
        *cdkVirtualFor="let product of products; trackBy: trackById"
        [product]="product"
      />
    </cdk-virtual-scroll-viewport>
  `,
  styles: [`
    .product-list {
      height: 600px; /* Fixed height required */
      width: 100%;
    }
  `],
  imports: [ScrollingModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductListComponent {
  products: Product[] = []; // 10,000 items - no problem!

  trackById(index: number, product: Product): number {
    return product.id;
  }
}
```

**For variable height items:**

```typescript
@Component({
  selector: 'app-infinite-list',
  template: `
    <cdk-virtual-scroll-viewport
      itemSize="50"
      (scrolledIndexChange)="onScroll($event)"
      class="list-container"
    >
      <div *cdkVirtualFor="let item of items; trackBy: trackById">
        {{ item.name }}
      </div>
      @if (loading) {
        <div class="loader">Loading more...</div>
      }
    </cdk-virtual-scroll-viewport>
  `,
  imports: [ScrollingModule]
})
export class InfiniteListComponent {
  items: Item[] = [];
  loading = false;

  @ViewChild(CdkVirtualScrollViewport) viewport!: CdkVirtualScrollViewport;

  onScroll(index: number): void {
    const end = this.viewport.getRenderedRange().end;
    const total = this.viewport.getDataLength();

    if (end >= total - 5 && !this.loading) {
      this.loadMore();
    }
  }

  private loadMore(): void {
    this.loading = true;
    // Fetch next page...
  }
}
```

**Advanced: Infinite scroll with virtual scrolling:**

**Why it matters:**

- 10,000 items without virtual scroll: ~500MB memory, 5+ seconds render

- 10,000 items with virtual scroll: ~50MB memory, instant render

- Only visible items + small buffer are in DOM at any time

- `templateCacheSize` reuses DOM nodes for better performance

**When NOT to use virtual scrolling:**

- Lists under 100 items (overhead not worth it)

- Items need to be fully rendered for SEO

- Complex item heights that can't be estimated

Reference: [https://material.angular.io/cdk/scrolling/overview](https://material.angular.io/cdk/scrolling/overview)

---

## 5. Dependency Injection

**Impact: MEDIUM-HIGH**

Proper DI with providedIn, InjectionToken, and factory providers enables tree-shaking and testability.

### 5.1 Use Factory Providers for Complex Setup

**Impact: MEDIUM-HIGH (Conditional logic, dependency injection in factories)**

Factory providers allow conditional service creation with access to other dependencies via `inject()` inside the factory function.

**Incorrect (Complex logic in constructor):**

```typescript
@Injectable({ providedIn: 'root' })
export class StorageService {
  private storage: Storage;

  constructor() {
    // Complex logic in constructor - hard to test
    if (typeof window !== 'undefined' && window.localStorage) {
      this.storage = window.localStorage;
    } else {
      this.storage = new MemoryStorage();
    }
  }
}
```

**Correct (Factory with inject()):**

```typescript
export abstract class StorageService {
  abstract getItem(key: string): string | null;
  abstract setItem(key: string, value: string): void;
}

export class LocalStorageService extends StorageService {
  getItem(key: string) { return localStorage.getItem(key); }
  setItem(key: string, value: string) { localStorage.setItem(key, value); }
}

export class MemoryStorageService extends StorageService {
  private store = new Map<string, string>();
  getItem(key: string) { return this.store.get(key) ?? null; }
  setItem(key: string, value: string) { this.store.set(key, value); }
}

// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: StorageService,
      useFactory: () => {
        const platformId = inject(PLATFORM_ID);
        return isPlatformBrowser(platformId)
          ? new LocalStorageService()
          : new MemoryStorageService();
      }
    }
  ]
};
```

**Why it matters:**

- Use `inject()` inside factory for dependencies

- Conditional service creation based on environment

- Clean separation of implementations

- Easy to test each implementation independently

Reference: [https://angular.dev/guide/di/dependency-injection-providers](https://angular.dev/guide/di/dependency-injection-providers)

### 5.2 Use InjectionToken for Type-Safe Configuration

**Impact: MEDIUM-HIGH (Type safety, better testability)**

`InjectionToken` provides type-safe dependency injection for non-class values like configuration objects and feature flags.

**Incorrect (String tokens lose type safety):**

```typescript
providers: [
  { provide: 'API_URL', useValue: 'https://api.example.com' }
]

@Injectable({ providedIn: 'root' })
export class ApiService {
  private apiUrl = inject('API_URL' as any);  // No type safety
}
```

**Correct (InjectionToken with inject()):**

```typescript
// tokens.ts
export interface AppConfig {
  apiUrl: string;
  timeout: number;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.example.com', timeout: 5000 }
    }
  ]
};

// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  private config = inject(APP_CONFIG);  // Fully typed as AppConfig
}
```

**Why it matters:**

- Full type safety with `inject()`

- Compile-time checking for configuration values

- Easy to test by providing mock tokens

- Self-documenting code

Reference: [https://angular.dev/api/core/InjectionToken](https://angular.dev/api/core/InjectionToken)

### 5.3 Use providedIn root for Tree-Shaking

**Impact: MEDIUM-HIGH (Enables automatic tree-shaking of unused services)**

Services with `providedIn: 'root'` are tree-shakeable - if no component injects them, they're excluded from the bundle.

**Incorrect (Service always in bundle):**

```typescript
@Injectable()
export class UserService {}

@NgModule({
  providers: [UserService]  // Always in bundle, even if unused
})
export class UserModule {}
```

**Correct (Tree-shakeable with inject()):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}

// No providers array needed - just inject where used
@Component({...})
export class UserListComponent {
  private userService = inject(UserService);
  users = toSignal(this.userService.getUsers(), { initialValue: [] });
}
```

**Why it matters:**

- Unused services excluded from bundle

- No need to add to providers arrays

- Use `inject()` function for cleaner dependency injection

- Works with signals and OnPush change detection

Reference: [https://angular.dev/guide/di](https://angular.dev/guide/di)

---

## 6. HTTP & Caching

**Impact: MEDIUM**

Functional interceptors, HTTP cache transfer for SSR, and caching strategies reduce network requests.

### 6.1 Use Functional HTTP Interceptors

**Impact: MEDIUM (Cleaner code, better tree-shaking)**

Functional interceptors are simpler functions that replace class-based interceptors, with better tree-shaking and no boilerplate.

**Incorrect (Class-based interceptor):**

```typescript
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    if (token) {
      req = req.clone({
        setHeaders: { Authorization: `Bearer ${token}` }
      });
    }
    return next.handle(req);
  }
}

// Registration requires verbose provider config
providers: [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
]
```

**Correct (Functional interceptor):**

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(req);
};

// app.config.ts - Clean registration
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([authInterceptor])
    )
  ]
};
```

**Why it matters:**

- Just a function, no class boilerplate

- Use `inject()` to get dependencies

- Clean array-based registration

- Automatically applies to `httpResource()` calls

Reference: [https://angular.dev/guide/http/interceptors](https://angular.dev/guide/http/interceptors)

### 6.2 Use httpResource for Signal-Based HTTP

**Impact: HIGH (Automatic loading states, reactive data fetching)**

`httpResource()` provides automatic loading/error states and reactive refetching when dependencies change, eliminating manual state management boilerplate.

**Incorrect (Manual loading state management):**

```typescript
@Component({
  template: `
    @if (loading) {
      <p>Loading...</p>
    } @else if (error) {
      <p>Error: {{ error }}</p>
    } @else {
      <p>{{ user?.name }}</p>
    }
  `
})
export class UserComponent implements OnInit {
  user: User | null = null;
  loading = false;
  error: string | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loading = true;
    this.http.get<User>('/api/users/1').subscribe({
      next: (user) => {
        this.user = user;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
      }
    });
  }
}
```

**Correct (httpResource with automatic state):**

```typescript
@Component({
  template: `
    @if (userResource.isLoading()) {
      <p>Loading...</p>
    } @else if (userResource.error()) {
      <p>Error: {{ userResource.error()?.message }}</p>
      <button (click)="userResource.reload()">Retry</button>
    } @else if (userResource.hasValue()) {
      <h1>{{ userResource.value().name }}</h1>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserComponent {
  userId = signal('123');

  // Auto-refetches when userId changes
  userResource = httpResource<User>(() => `/api/users/${this.userId()}`);
}
```

**Why it matters:**

- Eliminates loading/error state boilerplate

- Automatically refetches when signal dependencies change

- Built-in `reload()` for retry functionality

- Type-safe access via `value()`, `error()`, `isLoading()`

Reference: [https://angular.dev/guide/http](https://angular.dev/guide/http)

### 6.3 Use TransferState for SSR Hydration

**Impact: MEDIUM (Eliminates duplicate requests on hydration)**

Without TransferState, HTTP requests made on the server are repeated on the client during hydration. TransferState transfers server responses to the client, avoiding duplicates.

**Incorrect (Duplicate requests during hydration):**

```typescript
@Component({...})
export class ProductListComponent implements OnInit {
  products$!: Observable<Product[]>;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Runs on server AND client = 2 identical requests
    this.products$ = this.http.get<Product[]>('/api/products');
  }
}
```

**Correct (Enable HTTP cache transfer):**

```typescript
// app.config.ts
import { provideClientHydration, withHttpTransferCacheOptions } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withFetch()),
    provideClientHydration(
      withHttpTransferCacheOptions({
        includePostRequests: true
      })
    )
  ]
};

// component.ts - No changes needed
@Component({...})
export class ProductListComponent {
  products$ = inject(HttpClient).get<Product[]>('/api/products');
  // Response transferred from server to client automatically
}
```

**Why it matters:**

- Server response cached and transferred to client

- No duplicate HTTP requests during hydration

- Faster initial page interactivity

- Works automatically with HttpClient

Reference: [https://angular.dev/guide/ssr](https://angular.dev/guide/ssr)

---

## 7. Forms Optimization

**Impact: MEDIUM**

Typed reactive forms with NonNullableFormBuilder provide compile-time safety and better DX.

### 7.1 Use Reactive Forms for Complex Forms

**Impact: MEDIUM (Better testability, synchronous access)**

Reactive forms provide synchronous access to form state, making them easier to test and offering better control over validation.

**Incorrect (Template-driven with complex validation):**

```typescript
@Component({
  template: `
    <form #userForm="ngForm" (ngSubmit)="onSubmit()">
      <input [(ngModel)]="user.email" name="email" required email />
      <input [(ngModel)]="user.password" name="password" required />
      <input [(ngModel)]="user.confirmPassword" name="confirmPassword" />

      <!-- Complex validation in template -->
      @if (userForm.controls['password']?.value !== userForm.controls['confirmPassword']?.value) {
        <div>Passwords don't match</div>
      }
    </form>
  `
})
export class RegisterComponent {
  user = { email: '', password: '', confirmPassword: '' };
}
```

**Correct (Reactive form with typed controls):**

```typescript
@Component({
  imports: [ReactiveFormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      <input type="password" formControlName="password" />
      <input type="password" formControlName="confirmPassword" />

      @if (form.errors?.['passwordMismatch']) {
        <span class="error">Passwords don't match</span>
      }

      <button [disabled]="form.invalid">Submit</button>
    </form>
  `
})
export class RegisterComponent {
  private fb = inject(NonNullableFormBuilder);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    confirmPassword: ['', Validators.required]
  }, {
    validators: [this.passwordMatchValidator]
  });

  passwordMatchValidator(group: FormGroup): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }

  onSubmit() {
    if (this.form.valid) {
      const { email, password } = this.form.getRawValue();
    }
  }
}
```

**Why it matters:**

- Typed form values with `NonNullableFormBuilder`

- Cross-field validation in component logic

- Synchronous access to form state

- Easy to test without template

Reference: [https://angular.dev/guide/forms/reactive-forms](https://angular.dev/guide/forms/reactive-forms)

---

## 8. General Performance

**Impact: LOW-MEDIUM**

Web Workers and additional optimization patterns for specific use cases.

### 8.1 Offload Heavy Computation to Web Workers

**Impact: LOW-MEDIUM (Keeps UI responsive during intensive tasks)**

Heavy computations on the main thread block the UI. Web Workers run in a separate thread, keeping the UI responsive.

**Incorrect (Heavy computation blocks UI):**

```typescript
@Component({
  template: `
    <button (click)="processData()">Process</button>
    <div>Result: {{ result }}</div>
    <!-- UI freezes while processing -->
  `
})
export class DataProcessorComponent {
  result = '';

  processData() {
    // Blocks main thread for seconds
    const data = this.generateLargeDataset();
    this.result = this.heavyComputation(data);
  }
}
```

**Correct (Web Worker keeps UI responsive):**

```typescript
// ng generate web-worker data-processor

// data-processor.worker.ts
addEventListener('message', ({ data }) => {
  const result = heavyComputation(data);
  postMessage(result);
});

// data-processor.component.ts
@Component({
  template: `
    <button (click)="processData()" [disabled]="isProcessing()">
      {{ isProcessing() ? 'Processing...' : 'Process' }}
    </button>
    <div>Result: {{ result() }}</div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DataProcessorComponent {
  result = signal('');
  isProcessing = signal(false);
  private worker = new Worker(
    new URL('./data-processor.worker', import.meta.url)
  );

  constructor() {
    this.worker.onmessage = ({ data }) => {
      this.result.set(data);
      this.isProcessing.set(false);
    };
  }

  processData() {
    this.isProcessing.set(true);
    this.worker.postMessage(this.generateLargeDataset());
  }
}
```

**Why it matters:**

- UI remains responsive during computation

- Use for data parsing, image processing, encryption

- Generate with `ng generate web-worker <name>`

- Consider Comlink library for easier communication

Reference: [https://angular.dev/guide/web-worker](https://angular.dev/guide/web-worker)

### 8.2 Prevent Memory Leaks

**Impact: HIGH (Uncleaned subscriptions, timers, and listeners cause app slowdown and crashes)**

Memory leaks occur when resources aren't released after component destruction. Common sources: subscriptions, timers, event listeners, and DOM references. Over time, leaks cause slowdown and crashes.

**Incorrect (Subscription not cleaned up):**

```typescript
// ❌ Subscription lives forever after component destroyed
@Component({...})
export class DashboardComponent implements OnInit {
  ngOnInit() {
    // This subscription NEVER gets cleaned up
    this.dataService.getData().subscribe(data => {
      this.data = data;
    });

    // Interval runs forever, even after navigation
    setInterval(() => this.refresh(), 5000);

    // Event listener never removed
    window.addEventListener('resize', this.onResize);
  }

  onResize = () => {
    this.width = window.innerWidth;
  };
}
```

**Correct (Proper cleanup):**

```typescript
// ✅ Modern approach: takeUntilDestroyed (Angular 16+)
@Component({...})
export class DashboardComponent {
  private destroyRef = inject(DestroyRef);

  data$ = this.dataService.getData().pipe(
    takeUntilDestroyed(this.destroyRef)
  );

  constructor() {
    // Auto-cleaned up when component destroys
    interval(5000).pipe(
      takeUntilDestroyed(this.destroyRef)
    ).subscribe(() => this.refresh());
  }
}

// ✅ Classic approach: Subject + takeUntil
@Component({...})
export class DashboardComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData().pipe(
      takeUntil(this.destroy$)
    ).subscribe(data => this.data = data);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

---

**Incorrect (Timer/Interval not cleared):**

```typescript
// ❌ setInterval runs forever
@Component({...})
export class PollingComponent implements OnInit {
  ngOnInit() {
    setInterval(() => {
      this.fetchData(); // Runs even after component destroyed!
    }, 3000);
  }
}
```

**Correct (Clear timers):**

```typescript
// ✅ Option 1: Use RxJS interval with takeUntilDestroyed
@Component({...})
export class PollingComponent {
  private destroyRef = inject(DestroyRef);

  constructor() {
    interval(3000).pipe(
      takeUntilDestroyed(this.destroyRef),
      switchMap(() => this.dataService.fetch())
    ).subscribe(data => this.data = data);
  }
}

// ✅ Option 2: Manual cleanup with clearInterval
@Component({...})
export class PollingComponent implements OnInit, OnDestroy {
  private intervalId?: ReturnType<typeof setInterval>;

  ngOnInit() {
    this.intervalId = setInterval(() => this.fetchData(), 3000);
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }
}

// ✅ Option 3: setTimeout with recursive call
@Component({...})
export class PollingComponent implements OnDestroy {
  private timeoutId?: ReturnType<typeof setTimeout>;
  private isDestroyed = false;

  ngOnInit() {
    this.poll();
  }

  private poll() {
    if (this.isDestroyed) return;

    this.fetchData();
    this.timeoutId = setTimeout(() => this.poll(), 3000);
  }

  ngOnDestroy() {
    this.isDestroyed = true;
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  }
}
```

---

**Incorrect (Event listener not removed):**

```typescript
// ❌ Window listener persists forever
@Component({...})
export class ResponsiveComponent implements OnInit {
  ngOnInit() {
    window.addEventListener('resize', this.handleResize);
    document.addEventListener('click', this.handleClick);
  }

  handleResize = () => { /* ... */ };
  handleClick = () => { /* ... */ };
}
```

**Correct (Remove listeners):**

```typescript
// ✅ Option 1: Manual cleanup
@Component({...})
export class ResponsiveComponent implements OnInit, OnDestroy {
  // Must use arrow function or bind to keep 'this' reference
  private handleResize = () => {
    this.width = window.innerWidth;
  };

  ngOnInit() {
    window.addEventListener('resize', this.handleResize);
  }

  ngOnDestroy() {
    window.removeEventListener('resize', this.handleResize);
  }
}

// ✅ Option 2: RxJS fromEvent (recommended)
@Component({...})
export class ResponsiveComponent {
  private destroyRef = inject(DestroyRef);

  width$ = fromEvent(window, 'resize').pipe(
    debounceTime(100),
    map(() => window.innerWidth),
    startWith(window.innerWidth),
    takeUntilDestroyed(this.destroyRef)
  );
}

// ✅ Option 3: Renderer2 for SSR compatibility
@Component({...})
export class ResponsiveComponent implements OnInit, OnDestroy {
  private renderer = inject(Renderer2);
  private unlistenFn?: () => void;

  ngOnInit() {
    this.unlistenFn = this.renderer.listen('window', 'resize', () => {
      this.width = window.innerWidth;
    });
  }

  ngOnDestroy() {
    this.unlistenFn?.();
  }
}
```

---

**Incorrect (Holding references to destroyed elements):**

```typescript
// ❌ Service holds reference to destroyed component
@Injectable({ providedIn: 'root' })
export class ModalService {
  private openModals: ModalComponent[] = [];

  register(modal: ModalComponent) {
    this.openModals.push(modal);
    // Never removed - component reference held forever!
  }
}
```

**Correct (Clean up references):**

```typescript
// ✅ Properly manage references
@Injectable({ providedIn: 'root' })
export class ModalService {
  private openModals = new Set<ModalComponent>();

  register(modal: ModalComponent) {
    this.openModals.add(modal);
  }

  unregister(modal: ModalComponent) {
    this.openModals.delete(modal);
  }
}

@Component({...})
export class ModalComponent implements OnDestroy {
  private modalService = inject(ModalService);

  constructor() {
    this.modalService.register(this);
  }

  ngOnDestroy() {
    this.modalService.unregister(this);
  }
}
```

**Memory leak detection checklist:**

- [ ] All subscriptions use `takeUntilDestroyed` or `takeUntil`

- [ ] All `setInterval`/`setTimeout` cleared in `ngOnDestroy`

- [ ] All `addEventListener` has matching `removeEventListener`

- [ ] No component references stored in long-lived services

- [ ] Use Chrome DevTools Memory tab to detect leaks

Reference: [https://angular.dev/best-practices/runtime-performance](https://angular.dev/best-practices/runtime-performance)

---

## References

1. [https://angular.dev](https://angular.dev)
2. [https://angular.dev/guide/signals](https://angular.dev/guide/signals)
3. [https://angular.dev/guide/defer](https://angular.dev/guide/defer)
4. [https://angular.dev/guide/templates/control-flow](https://angular.dev/guide/templates/control-flow)
5. [https://angular.dev/guide/image-optimization](https://angular.dev/guide/image-optimization)
