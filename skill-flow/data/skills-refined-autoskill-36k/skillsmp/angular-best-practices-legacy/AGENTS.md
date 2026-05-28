# Angular Best Practices (Angular 12-16)

**Version 1.0.0**  
Community  
January 2026

> **Note:**  
> This document is for AI agents and LLMs to follow when maintaining,  
> generating, or refactoring Angular codebases. Optimized for Angular 12-16.

---

## Abstract

Performance optimization guide for Angular 12-16 applications using NgModule-based architecture, RxJS state management, and classic template syntax (*ngIf, *ngFor). Contains rules prioritized by impact for AI-assisted code generation and refactoring of legacy Angular codebases.

---

## Table of Contents

0. [Section 0](#0-section-0) — **MEDIUM**
   - 0.1 [Combine Multiple Array Iterations](#01-combine-multiple-array-iterations)
   - 0.2 [Use CSS content-visibility for Off-Screen Content](#02-use-css-content-visibility-for-off-screen-content)
   - 0.3 [Use Set/Map for O(1) Lookups](#03-use-setmap-for-o1-lookups)
   - 0.4 [Use Smart and Dumb Component Pattern](#04-use-smart-and-dumb-component-pattern)
1. [Change Detection](#1-change-detection) — **CRITICAL**
   - 1.1 [Detach Change Detector for Heavy Operations](#11-detach-change-detector-for-heavy-operations)
   - 1.2 [Run Non-UI Code Outside NgZone](#12-run-non-ui-code-outside-ngzone)
   - 1.3 [Use BehaviorSubject for Reactive State](#13-use-behaviorsubject-for-reactive-state)
   - 1.4 [Use OnPush Change Detection Strategy](#14-use-onpush-change-detection-strategy)
2. [Bundle & Lazy Loading](#2-bundle--lazy-loading) — **CRITICAL**
   - 2.1 [Avoid Barrel File Imports](#21-avoid-barrel-file-imports)
   - 2.2 [Lazy Load Feature Modules](#22-lazy-load-feature-modules)
   - 2.3 [Organize Code with Feature Modules](#23-organize-code-with-feature-modules)
   - 2.4 [Use Preload Strategies for Lazy Modules](#24-use-preload-strategies-for-lazy-modules)
   - 2.5 [Use SCAM Pattern Instead of Shared Modules](#25-use-scam-pattern-instead-of-shared-modules)
3. [RxJS Optimization](#3-rxjs-optimization) — **HIGH**
   - 3.1 [Avoid Nested Subscriptions](#31-avoid-nested-subscriptions)
   - 3.2 [Share Observables to Avoid Duplicate Requests](#32-share-observables-to-avoid-duplicate-requests)
   - 3.3 [Use Async Pipe Instead of Manual Subscribe](#33-use-async-pipe-instead-of-manual-subscribe)
   - 3.4 [Use Correct RxJS Mapping Operators](#34-use-correct-rxjs-mapping-operators)
   - 3.5 [Use Efficient RxJS Operators](#35-use-efficient-rxjs-operators)
   - 3.6 [Use Subject with takeUntil for Cleanup](#36-use-subject-with-takeuntil-for-cleanup)
4. [Template Performance](#4-template-performance) — **HIGH**
   - 4.1 [Avoid Function Calls in Templates](#41-avoid-function-calls-in-templates)
   - 4.2 [Use NgOptimizedImage for Images (v15+)](#42-use-ngoptimizedimage-for-images-v15)
   - 4.3 [Use Pure Pipes for Data Transformation](#43-use-pure-pipes-for-data-transformation)
   - 4.4 [Use trackBy with *ngFor](#44-use-trackby-with-ngfor)
   - 4.5 [Use Virtual Scrolling for Large Lists](#45-use-virtual-scrolling-for-large-lists)
5. [Dependency Injection](#5-dependency-injection) — **MEDIUM-HIGH**
   - 5.1 [Use Factory Providers for Complex Setup](#51-use-factory-providers-for-complex-setup)
   - 5.2 [Use InjectionToken for Type-Safe Configuration](#52-use-injectiontoken-for-type-safe-configuration)
   - 5.3 [Use providedIn root for Tree-Shaking](#53-use-providedin-root-for-tree-shaking)
6. [HTTP & Caching](#6-http--caching) — **MEDIUM**
   - 6.1 [Use Class-Based HTTP Interceptors](#61-use-class-based-http-interceptors)
   - 6.2 [Use TransferState for SSR](#62-use-transferstate-for-ssr)
7. [Forms Optimization](#7-forms-optimization) — **MEDIUM**
   - 7.1 [Use Reactive Forms for Complex Forms](#71-use-reactive-forms-for-complex-forms)
   - 7.2 [Use Typed Reactive Forms (v14+)](#72-use-typed-reactive-forms-v14)
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

### 0.2 Use CSS content-visibility for Off-Screen Content

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

### 0.3 Use Set/Map for O(1) Lookups

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

### 0.4 Use Smart and Dumb Component Pattern

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

Change detection optimization with OnPush, NgZone, and RxJS-based reactive state management.

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

### 1.3 Use BehaviorSubject for Reactive State

**Impact: CRITICAL (Reactive state management without Signals)**

Before Angular Signals (v16+), BehaviorSubject provides reactive state management. Combined with OnPush change detection and async pipe, it offers efficient updates.

**Incorrect (Imperative state with manual change detection):**

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

**Correct (BehaviorSubject with async pipe):**

```typescript
@Component({
  selector: 'app-counter',
  template: `
    <ng-container *ngIf="vm$ | async as vm">
      <p>Count: {{ vm.count }}</p>
      <p>Double: {{ vm.double }}</p>
    </ng-container>
    <button (click)="increment()">+</button>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  private countSubject = new BehaviorSubject<number>(0);

  vm$ = this.countSubject.pipe(
    map(count => ({
      count,
      double: count * 2
    }))
  );

  increment() {
    this.countSubject.next(this.countSubject.value + 1);
    // No manual markForCheck needed - async pipe handles it
  }
}
```

**State service pattern:**

```typescript
@Injectable({ providedIn: 'root' })
export class CounterState {
  private countSubject = new BehaviorSubject<number>(0);

  readonly count$ = this.countSubject.asObservable();
  readonly double$ = this.count$.pipe(map(c => c * 2));

  increment() {
    this.countSubject.next(this.countSubject.value + 1);
  }

  decrement() {
    this.countSubject.next(this.countSubject.value - 1);
  }
}
```

Reference: [https://rxjs.dev/api/index/class/BehaviorSubject](https://rxjs.dev/api/index/class/BehaviorSubject)

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

NgModule-based lazy loading and preload strategies to reduce initial bundle size.

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

### 2.2 Lazy Load Feature Modules

**Impact: CRITICAL (40-70% initial bundle reduction)**

Lazy loading splits your application into smaller chunks loaded on demand. Use `loadChildren` to lazy load feature modules.

**Incorrect (Eagerly loaded modules):**

```typescript
import { UserModule } from './user/user.module';
import { AdminModule } from './admin/admin.module';

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    UserModule,   // Loaded immediately
    AdminModule   // Loaded even if user never visits
  ]
})
export class AppRoutingModule {}
```

**Correct (Lazy loaded modules):**

```typescript
const routes: Routes = [
  {
    path: 'users',
    loadChildren: () =>
      import('./user/user.module').then(m => m.UserModule)
  },
  {
    path: 'admin',
    loadChildren: () =>
      import('./admin/admin.module').then(m => m.AdminModule),
    canLoad: [AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
```

**Why it matters:**

- Initial bundle only includes core code

- Feature modules downloaded on navigation

- `canLoad` prevents loading if not authorized

- Use `forChild` in lazy-loaded routing modules

Reference: [https://v16.angular.io/guide/lazy-loading-ngmodules](https://v16.angular.io/guide/lazy-loading-ngmodules)

### 2.3 Organize Code with Feature Modules

**Impact: CRITICAL (Better code organization, enables lazy loading)**

Feature modules group related components, services, and pipes. They enable lazy loading and keep the codebase organized. Each feature should have its own module.

**Incorrect (Everything in AppModule):**

```typescript
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    UserListComponent,
    UserDetailComponent,
    ProductListComponent,
    ProductDetailComponent,
    CartComponent,
    CheckoutComponent,
    // ... 50 more components
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
// Everything loaded upfront, huge initial bundle
```

**Correct (Feature modules with lazy loading):**

```typescript
// user.module.ts
@NgModule({
  declarations: [
    UserListComponent,
    UserDetailComponent,
    UserAvatarComponent,
  ],
  imports: [
    CommonModule,
    UserRoutingModule,
    SharedModule,
  ]
})
export class UserModule {}

// product.module.ts
@NgModule({
  declarations: [
    ProductListComponent,
    ProductDetailComponent,
  ],
  imports: [
    CommonModule,
    ProductRoutingModule,
    SharedModule,
  ]
})
export class ProductModule {}

// app-routing.module.ts
const routes: Routes = [
  {
    path: 'users',
    loadChildren: () => import('./user/user.module').then(m => m.UserModule)
  },
  {
    path: 'products',
    loadChildren: () => import('./product/product.module').then(m => m.ProductModule)
  }
];

// app.module.ts - minimal
@NgModule({
  declarations: [AppComponent, HeaderComponent, FooterComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    CoreModule, // Singleton services
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
```

**SharedModule pattern:**

```typescript
@NgModule({
  declarations: [LoadingSpinnerComponent, ErrorMessageComponent],
  imports: [CommonModule],
  exports: [
    CommonModule,
    LoadingSpinnerComponent,
    ErrorMessageComponent,
  ]
})
export class SharedModule {}
```

Reference: [https://v16.angular.io/guide/feature-modules](https://v16.angular.io/guide/feature-modules)

### 2.4 Use Preload Strategies for Lazy Modules

**Impact: CRITICAL (Improves navigation performance)**

Preloading downloads lazy-loaded modules in the background after initial load, making subsequent navigation instant.

**Incorrect (No preloading causes navigation delay):**

```typescript
@NgModule({
  imports: [RouterModule.forRoot(routes)]
  // No preloading - modules load on demand with delay
})
export class AppRoutingModule {}
```

**Correct (Preload all modules):**

```typescript
import { PreloadAllModules } from '@angular/router';

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      preloadingStrategy: PreloadAllModules
    })
  ]
})
export class AppRoutingModule {}
```

**Why it matters:**

- `PreloadAllModules` loads all routes after initial render

- Navigation to lazy routes becomes instant

- Initial load is not affected

- Custom strategies can preload selectively

Reference: [https://v16.angular.io/guide/lazy-loading-ngmodules#preloading](https://v16.angular.io/guide/lazy-loading-ngmodules#preloading)

### 2.5 Use SCAM Pattern Instead of Shared Modules

**Impact: HIGH (Better tree-shaking and smaller bundles by avoiding shared module bloat)**

SCAM (Single Component as Module) pattern creates a dedicated NgModule for each component, directive, or pipe. This enables better tree-shaking and prevents importing unused code through shared modules.

**Incorrect (Shared module with many exports):**

```typescript
// shared.module.ts
@NgModule({
  declarations: [
    ButtonComponent,
    CardComponent,
    ModalComponent,
    TooltipDirective,
    DatePipe,
    CurrencyPipe,
    // 20+ more components...
  ],
  exports: [
    ButtonComponent,
    CardComponent,
    ModalComponent,
    TooltipDirective,
    DatePipe,
    CurrencyPipe,
    // All exported even if only one is used
  ]
})
export class SharedModule {}

// feature.module.ts
@NgModule({
  imports: [SharedModule] // Imports ALL shared components
})
export class FeatureModule {}
```

**Correct (SCAM pattern):**

```typescript
// button/button.component.module.ts
@NgModule({
  declarations: [ButtonComponent],
  imports: [CommonModule],
  exports: [ButtonComponent]
})
export class ButtonComponentModule {}

// card/card.component.module.ts
@NgModule({
  declarations: [CardComponent],
  imports: [CommonModule],
  exports: [CardComponent]
})
export class CardComponentModule {}

// modal/modal.component.module.ts
@NgModule({
  declarations: [ModalComponent],
  imports: [CommonModule, ButtonComponentModule],
  exports: [ModalComponent]
})
export class ModalComponentModule {}

// tooltip/tooltip.directive.module.ts
@NgModule({
  declarations: [TooltipDirective],
  exports: [TooltipDirective]
})
export class TooltipDirectiveModule {}

// feature.module.ts
@NgModule({
  imports: [
    ButtonComponentModule,  // Only import what you need
    CardComponentModule
  ]
})
export class FeatureModule {}
```

**File structure for SCAM:**

```typescript
shared/
├── button/
│   ├── button.component.ts
│   ├── button.component.html
│   ├── button.component.scss
│   ├── button.component.spec.ts
│   └── button.component.module.ts    # SCAM module
├── card/
│   ├── card.component.ts
│   ├── card.component.module.ts
├── modal/
│   ├── modal.component.ts
│   ├── modal.component.module.ts
└── index.ts                          # Barrel exports
```

**Barrel file for clean imports:**

```typescript
// shared/index.ts
export { ButtonComponentModule } from './button/button.component.module';
export { CardComponentModule } from './card/card.component.module';
export { ModalComponentModule } from './modal/modal.component.module';

// Usage in feature module
import { ButtonComponentModule, CardComponentModule } from '@shared';
```

**Benefits of SCAM:**

1. **Tree-shaking** - Unused components are excluded from bundle

2. **Explicit dependencies** - Each component declares its own imports

3. **Lazy loading ready** - Easy to lazy load individual components

4. **Migration path** - Simpler upgrade to standalone components in v17+

Reference: [https://v16.angular.io/guide/ngmodule-faq](https://v16.angular.io/guide/ngmodule-faq)

---

## 3. RxJS Optimization

**Impact: HIGH**

Proper RxJS patterns with async pipe, Subject-based cleanup, and efficient operators.

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

**Incorrect (Manual subscription):**

```typescript
@Component({
  template: `
    <div *ngIf="user">
      <h1>{{ user.name }}</h1>
    </div>
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
  template: `
    <div *ngIf="user$ | async as user">
      <h1>{{ user.name }}</h1>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserProfileComponent {
  user$ = this.userService.getCurrentUser();

  constructor(private userService: UserService) {}
  // No manual subscribe/unsubscribe needed
}
```

**Why it matters:**

- No manual `Subscription` management

- No `ngOnDestroy` cleanup needed

- Works perfectly with OnPush change detection

- Use `*ngIf="obs$ | async as value"` pattern for single subscription

Reference: [https://v16.angular.io/api/common/AsyncPipe](https://v16.angular.io/api/common/AsyncPipe)

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

### 3.6 Use Subject with takeUntil for Cleanup

**Impact: HIGH (Prevents memory leaks from subscriptions)**

When manually subscribing to observables, use a Subject with `takeUntil` to automatically unsubscribe when the component is destroyed.

**Incorrect (Manual subscription management):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private sub1!: Subscription;
  private sub2!: Subscription;

  ngOnInit() {
    this.sub1 = this.dataService.getData()
      .subscribe(data => this.processData(data));
    this.sub2 = this.eventService.events$
      .subscribe(event => this.handleEvent(event));
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();  // Easy to forget one
    this.sub2.unsubscribe();
  }
}
```

**Correct (Subject with takeUntil pattern):**

```typescript
@Component({...})
export class DataComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => this.processData(data));

    this.eventService.events$
      .pipe(takeUntil(this.destroy$))
      .subscribe(event => this.handleEvent(event));
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

**Why it matters:**

- Single cleanup point in `ngOnDestroy`

- Can't forget to unsubscribe individual subscriptions

- Works with any number of subscriptions

- Consider base class for reuse across components

Reference: [https://rxjs.dev/api/operators/takeUntil](https://rxjs.dev/api/operators/takeUntil)

---

## 4. Template Performance

**Impact: HIGH**

Optimizing templates with *ngFor trackBy, pure pipes, and NgOptimizedImage (v15+).

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

### 4.2 Use NgOptimizedImage for Images (v15+)

**Impact: HIGH (LCP improvement, automatic lazy loading)**

NgOptimizedImage (available from Angular 15) enforces best practices: automatic lazy loading, priority hints, srcset generation, and preconnect warnings.

**Incorrect (Native img):**

```html
<img src="/assets/hero.jpg" alt="Hero image">
<img src="{{ user.avatar }}" alt="User avatar">
```

**Correct (NgOptimizedImage):**

```typescript
// app.module.ts
import { NgOptimizedImage } from '@angular/common';

@NgModule({
  imports: [NgOptimizedImage]
})
export class AppModule {}

// component.ts
@Component({
  template: `
    <!-- Priority image (LCP candidate) -->
    <img
      ngSrc="/assets/hero.jpg"
      alt="Hero image"
      width="1200"
      height="600"
      priority
    />

    <!-- Lazy loaded (below fold) -->
    <img
      [ngSrc]="user.avatar"
      alt="User avatar"
      width="64"
      height="64"
    />

    <!-- Fill mode -->
    <div class="image-container">
      <img
        ngSrc="/assets/product.jpg"
        alt="Product"
        fill
        sizes="(max-width: 768px) 100vw, 50vw"
      />
    </div>
  `,
  styles: [`
    .image-container {
      position: relative;
      width: 100%;
      aspect-ratio: 4/3;
    }
  `]
})
export class ProductComponent {}
```

**With image loader:**

```typescript
// app.module.ts
import { NgOptimizedImage, provideImgixLoader } from '@angular/common';

@NgModule({
  imports: [NgOptimizedImage],
  providers: [
    provideImgixLoader('https://my-site.imgix.net/')
  ]
})
export class AppModule {}
```

**For Angular 12-14 (without NgOptimizedImage):**

```typescript
// Manual optimization
@Component({
  template: `
    <!-- Manual lazy loading -->
    <img
      [src]="imageSrc"
      [alt]="imageAlt"
      loading="lazy"
      width="400"
      height="300"
    />

    <!-- Intersection Observer for more control -->
    <img
      #lazyImage
      [attr.data-src]="imageSrc"
      [alt]="imageAlt"
      width="400"
      height="300"
    />
  `
})
export class ImageComponent implements AfterViewInit {
  @ViewChild('lazyImage') lazyImage!: ElementRef;

  ngAfterViewInit() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          img.src = img.dataset['src']!;
          observer.unobserve(img);
        }
      });
    });
    observer.observe(this.lazyImage.nativeElement);
  }
}
```

Reference: [https://v16.angular.io/guide/image-directive](https://v16.angular.io/guide/image-directive)

### 4.3 Use Pure Pipes for Data Transformation

**Impact: HIGH (Memoized computation, called only when input changes)**

Pure pipes are only executed when inputs change by reference. They're memoized, unlike template methods which run on every change detection cycle.

**Incorrect (Method called on every change detection):**

```typescript
@Component({
  template: `
    <div *ngFor="let product of products; trackBy: trackById">
      <span>{{ formatPrice(product.price) }}</span>
    </div>
  `
})
export class ProductListComponent {
  formatPrice(price: number): string {
    // Called on EVERY change detection cycle
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
  template: `
    <div *ngFor="let product of products; trackBy: trackById">
      <span>{{ product.price | price }}</span>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ProductListComponent {
  trackById = (index: number, product: Product) => product.id;
}
```

**Why it matters:**

- Pure pipes are memoized by Angular

- Only recalculate when input reference changes

- Methods run on every change detection cycle

- Declare pipes in NgModule and add to exports

Reference: [https://v16.angular.io/guide/pipes](https://v16.angular.io/guide/pipes)

### 4.4 Use trackBy with *ngFor

**Impact: HIGH (Prevents unnecessary DOM recreation)**

Without `trackBy`, Angular recreates all DOM elements when the array reference changes. `trackBy` tells Angular how to identify items for efficient DOM reuse.

**Incorrect (DOM recreated on every update):**

```typescript
@Component({
  template: `
    <div *ngFor="let user of users">
      <app-user-card [user]="user"></app-user-card>
    </div>
  `
})
export class UserListComponent {
  users: User[] = [];

  refresh() {
    // New array = all DOM destroyed and recreated
    this.users = [...this.fetchedUsers];
  }
}
```

**Correct (trackBy enables DOM reuse):**

```typescript
@Component({
  template: `
    <div *ngFor="let user of users; trackBy: trackById">
      <app-user-card [user]="user"></app-user-card>
    </div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserListComponent {
  users: User[] = [];

  trackById(index: number, user: User): number {
    return user.id;
  }
}
```

**Why it matters:**

- Same IDs = DOM elements reused

- Only changed items are re-rendered

- Significant performance gain in large lists

- Track by `index` only when items have no unique ID

Reference: [https://v16.angular.io/api/common/NgForOf](https://v16.angular.io/api/common/NgForOf)

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

Proper DI with providedIn, InjectionToken, and factory providers.

### 5.1 Use Factory Providers for Complex Setup

**Impact: MEDIUM-HIGH (Conditional logic, dependency injection in factories)**

Factory providers allow conditional service creation with dependencies specified via the `deps` array.

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

**Correct (Factory provider with deps array):**

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

// app.module.ts
@NgModule({
  providers: [
    {
      provide: StorageService,
      useFactory: (platformId: object) => {
        return isPlatformBrowser(platformId)
          ? new LocalStorageService()
          : new MemoryStorageService();
      },
      deps: [PLATFORM_ID]
    }
  ]
})
export class AppModule {}
```

**Why it matters:**

- Use `deps` array to inject dependencies

- Conditional service creation based on environment

- Clean separation of implementations

- Easy to test each implementation independently

Reference: [https://angular.dev/guide/di/dependency-injection-providers](https://angular.dev/guide/di/dependency-injection-providers)

### 5.2 Use InjectionToken for Type-Safe Configuration

**Impact: MEDIUM-HIGH (Type safety, better testability)**

`InjectionToken` provides type-safe dependency injection for non-class values like configuration objects and feature flags.

**Incorrect (String tokens lose type safety):**

```typescript
@NgModule({
  providers: [
    { provide: 'API_URL', useValue: 'https://api.example.com' }
  ]
})
export class AppModule {}

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(@Inject('API_URL') private apiUrl: any) {}  // No type safety
}
```

**Correct (InjectionToken with @Inject):**

```typescript
// tokens.ts
export interface AppConfig {
  apiUrl: string;
  timeout: number;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// app.module.ts
@NgModule({
  providers: [
    {
      provide: APP_CONFIG,
      useValue: { apiUrl: 'https://api.example.com', timeout: 5000 }
    }
  ]
})
export class AppModule {}

// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(@Inject(APP_CONFIG) private config: AppConfig) {}  // Typed!
}
```

**Why it matters:**

- Full type safety with `@Inject()` decorator

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

**Correct (Tree-shakeable with constructor injection):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}

// Inject in constructor
@Component({...})
export class UserListComponent implements OnInit {
  users$!: Observable<User[]>;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.users$ = this.userService.getUsers();
  }
}
```

**Why it matters:**

- Unused services excluded from bundle

- No need to add to providers arrays

- Constructor injection is the standard pattern

- Use BehaviorSubject for service state

Reference: [https://angular.dev/guide/di](https://angular.dev/guide/di)

---

## 6. HTTP & Caching

**Impact: MEDIUM**

Class-based interceptors, TransferState for SSR, and caching strategies.

### 6.1 Use Class-Based HTTP Interceptors

**Impact: MEDIUM (Centralized request/response handling)**

Class-based interceptors centralize cross-cutting concerns like authentication and error handling, eliminating duplicated logic across services.

**Incorrect (Duplicated auth logic in services):**

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient, private authService: AuthService) {}

  getUsers(): Observable<User[]> {
    // Auth header added manually in every method
    const headers = new HttpHeaders().set(
      'Authorization', `Bearer ${this.authService.getToken()}`
    );
    return this.http.get<User[]>('/api/users', { headers });
  }
}
```

**Correct (Class-based interceptor):**

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

// app.module.ts
@NgModule({
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ]
})
export class AppModule {}

// Services are now clean
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');  // No auth logic needed
  }
}
```

**Why it matters:**

- Centralized auth, logging, and error handling

- Services stay focused on business logic

- Use `multi: true` for multiple interceptors

- Interceptors run in order registered

Reference: [https://v16.angular.io/guide/http#intercepting-requests-and-responses](https://v16.angular.io/guide/http#intercepting-requests-and-responses)

### 6.2 Use TransferState for SSR

**Impact: MEDIUM (Eliminates duplicate requests on hydration)**

With Server-Side Rendering, HTTP requests run on the server. Without TransferState, the client repeats these requests during hydration. TransferState transfers server data to the client.

**Incorrect (Duplicate requests):**

```typescript
@Component({...})
export class ProductListComponent implements OnInit {
  products: Product[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit() {
    // Runs on server AND client = 2 requests
    this.http.get<Product[]>('/api/products')
      .subscribe(products => this.products = products);
  }
}
```

**Correct (Manual TransferState):**

```typescript
import { TransferState, makeStateKey } from '@angular/platform-browser';
import { isPlatformServer } from '@angular/common';

const PRODUCTS_KEY = makeStateKey<Product[]>('products');

@Component({
  template: `
    <div *ngFor="let product of products; trackBy: trackById">
      {{ product.name }}
    </div>
  `
})
export class ProductListComponent implements OnInit {
  products: Product[] = [];

  constructor(
    private http: HttpClient,
    private transferState: TransferState,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  ngOnInit() {
    // Check if data was transferred from server
    if (this.transferState.hasKey(PRODUCTS_KEY)) {
      this.products = this.transferState.get(PRODUCTS_KEY, []);
      this.transferState.remove(PRODUCTS_KEY);
    } else {
      this.http.get<Product[]>('/api/products').subscribe(products => {
        this.products = products;
        // Store on server for client
        if (isPlatformServer(this.platformId)) {
          this.transferState.set(PRODUCTS_KEY, products);
        }
      });
    }
  }

  trackById = (index: number, product: Product) => product.id;
}
```

**Reusable service pattern:**

```typescript
@Injectable({ providedIn: 'root' })
export class TransferStateService {
  constructor(
    private transferState: TransferState,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  fetch<T>(key: string, request: Observable<T>): Observable<T> {
    const stateKey = makeStateKey<T>(key);

    if (this.transferState.hasKey(stateKey)) {
      const data = this.transferState.get(stateKey, null as T);
      this.transferState.remove(stateKey);
      return of(data);
    }

    return request.pipe(
      tap(data => {
        if (isPlatformServer(this.platformId)) {
          this.transferState.set(stateKey, data);
        }
      })
    );
  }
}

// Usage
@Injectable({ providedIn: 'root' })
export class ProductService {
  constructor(
    private http: HttpClient,
    private transferStateService: TransferStateService
  ) {}

  getProducts(): Observable<Product[]> {
    return this.transferStateService.fetch(
      'products',
      this.http.get<Product[]>('/api/products')
    );
  }
}
```

Reference: [https://v16.angular.io/api/platform-browser/TransferState](https://v16.angular.io/api/platform-browser/TransferState)

---

## 7. Forms Optimization

**Impact: MEDIUM**

Reactive forms with typed controls (v14+) for better maintainability.

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

      <div *ngIf="userForm.controls['password']?.value !== userForm.controls['confirmPassword']?.value">
        Passwords don't match
      </div>
    </form>
  `
})
export class RegisterComponent {
  user = { email: '', password: '', confirmPassword: '' };
}
```

**Correct (Reactive form with FormBuilder):**

```typescript
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      <input type="password" formControlName="password" />
      <input type="password" formControlName="confirmPassword" />

      <div *ngIf="form.errors?.['passwordMismatch']" class="error">
        Passwords don't match
      </div>

      <button [disabled]="form.invalid">Submit</button>
    </form>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegisterComponent implements OnInit {
  form!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    }, {
      validators: [this.passwordMatchValidator]
    });
  }

  passwordMatchValidator(group: FormGroup): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }
}
```

**Why it matters:**

- Cross-field validation in component logic

- Synchronous access to form state

- Easy to test without template

- Works well with OnPush change detection

Reference: [https://v16.angular.io/guide/reactive-forms](https://v16.angular.io/guide/reactive-forms)

### 7.2 Use Typed Reactive Forms (v14+)

**Impact: MEDIUM (Compile-time type checking)**

Angular 14+ provides strictly typed reactive forms. Use `NonNullableFormBuilder` for non-nullable controls and explicit types for better IDE support.

**Incorrect (Untyped form):**

```typescript
@Component({...})
export class ProfileComponent {
  form = new FormGroup({
    name: new FormControl(''),
    email: new FormControl(''),
    age: new FormControl(0)
  });

  onSubmit() {
    const value = this.form.value;
    // value is Partial<{name: string | null, ...}>
    // Type is loose, nullable, and partial
    console.log(value.nmae); // Typo not caught
  }
}
```

**Correct (Typed form with NonNullableFormBuilder):**

```typescript
interface ProfileForm {
  name: FormControl<string>;
  email: FormControl<string>;
  age: FormControl<number>;
}

@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" />
      <input formControlName="email" type="email" />
      <input formControlName="age" type="number" />
      <button [disabled]="form.invalid">Save</button>
    </form>
  `
})
export class ProfileComponent {
  form: FormGroup<ProfileForm>;

  constructor(private fb: NonNullableFormBuilder) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      age: [0, [Validators.required, Validators.min(0)]]
    });
  }

  onSubmit() {
    // getRawValue() returns fully typed, non-nullable object
    const value = this.form.getRawValue();
    // Type: { name: string; email: string; age: number }

    // Compile error: Property 'nmae' does not exist
    // console.log(value.nmae);

    this.saveProfile(value);
  }

  // Safe typed access
  get nameControl() {
    return this.form.controls.name; // FormControl<string>
  }
}
```

**Typed FormArray:**

```typescript
interface OrderForm {
  customer: FormControl<string>;
  items: FormArray<FormGroup<{
    product: FormControl<string>;
    quantity: FormControl<number>;
  }>>;
}

@Component({...})
export class OrderComponent {
  form: FormGroup<OrderForm>;

  constructor(private fb: NonNullableFormBuilder) {
    this.form = this.fb.group({
      customer: ['', Validators.required],
      items: this.fb.array([this.createItemGroup()])
    });
  }

  get itemsArray() {
    return this.form.controls.items;
  }

  createItemGroup() {
    return this.fb.group({
      product: ['', Validators.required],
      quantity: [1, Validators.min(1)]
    });
  }

  addItem() {
    this.itemsArray.push(this.createItemGroup());
  }
}
```

Reference: [https://v16.angular.io/guide/typed-forms](https://v16.angular.io/guide/typed-forms)

---

## 8. General Performance

**Impact: LOW-MEDIUM**

Web Workers and additional optimization patterns.

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

1. [https://v16.angular.io](https://v16.angular.io)
2. [https://v16.angular.io/guide/lazy-loading-ngmodules](https://v16.angular.io/guide/lazy-loading-ngmodules)
3. [https://v16.angular.io/guide/reactive-forms](https://v16.angular.io/guide/reactive-forms)
4. [https://rxjs.dev](https://rxjs.dev)
5. [https://v16.angular.io/api/common/AsyncPipe](https://v16.angular.io/api/common/AsyncPipe)
