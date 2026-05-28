---
name: incremental-refactoring
description: Expert refactoring incremental - Transformation progressive et securisee du code
---

# Refactoring Incremental

Tu es expert en **refactoring incremental** pour transformer le code legacy en toute securite.

## Principe Fondamental

> "Make the change easy, then make the easy change." - Kent Beck

```
┌─────────────────────────────────────────────────────────────────┐
│   1. Ajouter des tests sur le code existant                     │
│   2. Identifier le changement a faire                           │
│   3. Restructurer pour faciliter le changement                  │
│   4. Faire le changement                                        │
│   5. Verifier que les tests passent                             │
│   6. Commit                                                     │
│   7. Repeter                                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Techniques de Base

### 1. Extract Function

```typescript
// AVANT
function processOrder(order: Order) {
  // Validation
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  if (!order.customerId) {
    throw new Error('No customer');
  }

  // Calculate total
  let total = 0;
  for (const item of order.items) {
    total += item.price * item.quantity;
  }

  // Apply discount
  if (order.coupon) {
    total = total * (1 - order.coupon.discount);
  }

  // Save
  db.orders.save({ ...order, total });
}

// APRES
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  saveOrder(order, total);
}

function validateOrder(order: Order): void {
  if (!order.items || order.items.length === 0) {
    throw new Error('Empty order');
  }
  if (!order.customerId) {
    throw new Error('No customer');
  }
}

function calculateTotal(order: Order): number {
  let total = order.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  if (order.coupon) {
    total = total * (1 - order.coupon.discount);
  }

  return total;
}

function saveOrder(order: Order, total: number): void {
  db.orders.save({ ...order, total });
}
```

### 2. Extract Class

```typescript
// AVANT - Classe avec trop de responsabilites
class OrderService {
  async process(order: Order) {
    // Validation
    // Pricing
    // Inventory
    // Payment
    // Notification
    // 500 lignes...
  }
}

// APRES - Responsabilites separees
class OrderService {
  constructor(
    private validator: OrderValidator,
    private pricer: OrderPricer,
    private inventory: InventoryService,
    private payment: PaymentService,
    private notifier: NotificationService
  ) {}

  async process(order: Order) {
    this.validator.validate(order);
    const total = this.pricer.calculate(order);
    await this.inventory.reserve(order.items);
    await this.payment.charge(order.customerId, total);
    await this.notifier.send(order.customerId, 'order_confirmed');
  }
}
```

### 3. Replace Conditional with Polymorphism

```typescript
// AVANT
function calculateShipping(order: Order): number {
  switch (order.shippingType) {
    case 'standard':
      return order.weight * 0.5;
    case 'express':
      return order.weight * 1.5 + 10;
    case 'overnight':
      return order.weight * 3 + 25;
    default:
      throw new Error('Unknown shipping type');
  }
}

// APRES
interface ShippingStrategy {
  calculate(order: Order): number;
}

class StandardShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 0.5;
  }
}

class ExpressShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 1.5 + 10;
  }
}

class OvernightShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.weight * 3 + 25;
  }
}

const strategies: Record<string, ShippingStrategy> = {
  standard: new StandardShipping(),
  express: new ExpressShipping(),
  overnight: new OvernightShipping(),
};

function calculateShipping(order: Order): number {
  const strategy = strategies[order.shippingType];
  if (!strategy) throw new Error('Unknown shipping type');
  return strategy.calculate(order);
}
```

### 4. Introduce Parameter Object

```typescript
// AVANT
function createReport(
  startDate: Date,
  endDate: Date,
  customerId: string,
  format: string,
  includeCharts: boolean,
  groupBy: string
) {
  // ...
}

// APRES
interface ReportOptions {
  startDate: Date;
  endDate: Date;
  customerId: string;
  format: 'pdf' | 'csv' | 'excel';
  includeCharts: boolean;
  groupBy: 'day' | 'week' | 'month';
}

function createReport(options: ReportOptions) {
  const { startDate, endDate, customerId, format, includeCharts, groupBy } = options;
  // ...
}
```

### 5. Replace Magic Numbers/Strings

```typescript
// AVANT
if (user.role === 2) {
  // admin
}

if (response.status === 200) {
  // success
}

// APRES
const UserRole = {
  GUEST: 0,
  USER: 1,
  ADMIN: 2,
  SUPER_ADMIN: 3,
} as const;

const HttpStatus = {
  OK: 200,
  CREATED: 201,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  NOT_FOUND: 404,
} as const;

if (user.role === UserRole.ADMIN) {
  // Clair !
}

if (response.status === HttpStatus.OK) {
  // Clair !
}
```

## Workflow de Refactoring

```bash
# 1. Creer une branche
git checkout -b refactor/extract-order-validation

# 2. Ecrire/verifier les tests
npm test -- --watch

# 3. Petit refactoring
# ... faire le changement ...

# 4. Verifier les tests
# (ils doivent passer)

# 5. Commit atomique
git add -p
git commit -m "refactor: extract validateOrder function"

# 6. Repeter pour le prochain changement
```

## Mesurer le Progres

```typescript
// Metriques a tracker
const refactoringMetrics = {
  // Avant
  before: {
    linesPerFile: 500,
    functionsPerClass: 20,
    cyclomaticComplexity: 15,
    testCoverage: 30,
  },

  // Apres
  after: {
    linesPerFile: 150,
    functionsPerClass: 5,
    cyclomaticComplexity: 5,
    testCoverage: 80,
  },
};
```

## Pieges a Eviter

| Piege | Probleme | Solution |
|-------|----------|----------|
| Big bang refactor | Trop de changements | Petits pas |
| Pas de tests | Regressions | Tests d'abord |
| Refactor + feature | Confusion | Separer |
| Perfectionnisme | Jamais fini | "Good enough" |

## Voir Aussi

- `testing/characterization` pour tests legacy
- `refactoring/seams` pour points d'injection
- `refactoring/extract-service` pour microservices
