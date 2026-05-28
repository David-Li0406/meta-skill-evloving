# Proposal Phase: Common Patterns

## Table of Contents

1. [Quick Win Patterns](#quick-win-patterns)
2. [Medium Change Patterns](#medium-change-patterns)
3. [Large Restructuring Patterns](#large-restructuring-patterns)
4. [Code Sample Guidelines](#code-sample-guidelines)

---

## Quick Win Patterns

### Extract Interface

**When**: Direct dependency on concrete class limits testability.

```typescript
// Before
class OrderService {
  constructor() {
    this.payment = new StripePayment();
  }
}

// After
interface PaymentGateway {
  charge(amount: number): Promise<Result>;
}

class OrderService {
  constructor(private payment: PaymentGateway) {}
}
```

### Inject Dependency

**When**: Class creates its own dependencies.

```typescript
// Before
class ReportGenerator {
  generate() {
    const db = new Database(process.env.DB_URL);
    // ...
  }
}

// After
class ReportGenerator {
  constructor(private db: Database) {}
  generate() {
    // use this.db
  }
}
```

### Extract Pure Function

**When**: Business logic mixed with side effects.

```typescript
// Before
class PricingService {
  calculateTotal(order) {
    const subtotal = order.items.reduce((s, i) => s + i.price * i.qty, 0);
    const tax = subtotal * 0.1;
    this.logger.log(`Calculated: ${subtotal + tax}`);  // side effect
    return subtotal + tax;
  }
}

// After
function calculateOrderTotal(items: LineItem[], taxRate: number): number {
  const subtotal = items.reduce((s, i) => s + i.price * i.qty, 0);
  return subtotal * (1 + taxRate);
}

class PricingService {
  calculateTotal(order) {
    const total = calculateOrderTotal(order.items, 0.1);
    this.logger.log(`Calculated: ${total}`);
    return total;
  }
}
```

### Remove Hidden Global

**When**: Function relies on global state.

```typescript
// Before
function sendEmail(to, subject, body) {
  const config = Config.getInstance();  // hidden global
  const client = new EmailClient(config.smtp);
  // ...
}

// After
function sendEmail(client: EmailClient, to, subject, body) {
  // client is explicit dependency
}
```

---

## Medium Change Patterns

### Introduce Repository

**When**: Data access scattered across services.

```typescript
// Before: SQL in service
class UserService {
  async getUser(id) {
    return await db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}

// After: Repository abstraction
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  async findById(id) {
    const row = await this.db.query('SELECT * FROM users WHERE id = $1', [id]);
    return row ? this.mapToUser(row) : null;
  }
}

class UserService {
  constructor(private users: UserRepository) {}
  async getUser(id) {
    return this.users.findById(id);
  }
}
```

### Split Service by Responsibility

**When**: Service does too many things.

```typescript
// Before: God service
class OrderService {
  createOrder() { /* ... */ }
  processPayment() { /* ... */ }
  sendConfirmation() { /* ... */ }
  generateInvoice() { /* ... */ }
  updateInventory() { /* ... */ }
}

// After: Focused services
class OrderService {
  constructor(
    private payments: PaymentService,
    private notifications: NotificationService,
    private inventory: InventoryService
  ) {}

  async createOrder(data) {
    const order = new Order(data);
    await this.payments.process(order);
    await this.inventory.reserve(order.items);
    await this.notifications.sendConfirmation(order);
    return order;
  }
}
```

### Introduce Domain Events

**When**: Services tightly coupled through direct calls.

```typescript
// Before: Direct coupling
class OrderService {
  async complete(orderId) {
    const order = await this.orders.findById(orderId);
    order.complete();
    await this.orders.save(order);

    // Tight coupling
    await this.inventory.release(order.items);
    await this.notifications.sendComplete(order);
    await this.analytics.trackConversion(order);
  }
}

// After: Event-driven
class OrderService {
  async complete(orderId) {
    const order = await this.orders.findById(orderId);
    order.complete();
    await this.orders.save(order);

    this.events.emit(new OrderCompleted(order));
  }
}

// Handlers subscribed elsewhere
class InventoryHandler {
  @OnEvent(OrderCompleted)
  handle(event) {
    this.inventory.release(event.order.items);
  }
}
```

---

## Large Restructuring Patterns

### Extract Bounded Context

**When**: Module has grown too large with distinct sub-domains.

Steps:
1. Identify natural boundaries (entities that cluster together)
2. Define context interfaces (API between contexts)
3. Move code to new structure
4. Replace internal calls with context API calls

### Strangler Fig Migration

**When**: Replacing legacy component incrementally.

```
Phase 1: Introduce facade
┌─────────────────────────────────┐
│           Facade                │
│    ┌─────────┬─────────┐       │
│    │  Legacy │   New   │       │
│    │  100%   │   0%    │       │
│    └─────────┴─────────┘       │
└─────────────────────────────────┘

Phase 2: Migrate feature by feature
┌─────────────────────────────────┐
│           Facade                │
│    ┌─────────┬─────────┐       │
│    │  Legacy │   New   │       │
│    │   60%   │   40%   │       │
│    └─────────┴─────────┘       │
└─────────────────────────────────┘

Phase 3: Complete migration
┌─────────────────────────────────┐
│           Facade                │
│    ┌─────────┬─────────┐       │
│    │  Legacy │   New   │       │
│    │    0%   │  100%   │       │
│    └─────────┴─────────┘       │
└─────────────────────────────────┘
```

---

## Code Sample Guidelines

### Before/After Clarity

Always show:
- File path and line numbers
- Enough context to understand the change
- Both removed and added code

```typescript
// Before: src/services/order.ts:45-52
class OrderService {
  private db = new Database();  // Line to change

  async save(order) {
    await this.db.insert('orders', order);
  }
}

// After: src/services/order.ts:45-55
class OrderService {
  constructor(private db: Database) {}  // Now injected

  async save(order) {
    await this.db.insert('orders', order);
  }
}

// Also update: src/composition-root.ts:23
const orderService = new OrderService(database);  // Wire dependency
```

### Impact Completeness

List ALL files that need changes:

```markdown
**Impact**
- `src/services/order.ts:45` - Add constructor parameter
- `src/services/order.ts:12` - Remove direct instantiation
- `src/composition-root.ts:23` - Wire new dependency
- `tests/order.test.ts:15` - Update test setup
- `src/types/index.ts` - Export new interface (if applicable)
```
