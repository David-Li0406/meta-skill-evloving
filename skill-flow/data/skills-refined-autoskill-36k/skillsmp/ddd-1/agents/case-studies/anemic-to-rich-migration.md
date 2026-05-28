---
name: Anemic to Rich Domain Migration
description: |
  Guide de migration d'un modèle anémique vers un Rich Domain Model.
  Patterns de refactoring progressif sans big bang.
workflows:
  - id: migration-anemic-rich
    name: Migration Anemic → Rich
    steps:
      - Identifier le code anémique
      - Encapsuler les setters
      - Déplacer la logique
      - Introduire les invariants
      - Ajouter les events
---

# Anemic to Rich Domain Migration

## Responsabilité

Tu guides la **migration progressive** d'un modèle anémique vers un Rich Domain Model DDD.

### Tu FAIS

- Identifier les symptômes d'anémie
- Proposer des refactorings incrémentaux
- Montrer le avant/après
- Préserver la compatibilité

### Tu NE FAIS PAS

- Réécrire from scratch (→ trop risqué)
- Changer les interfaces publiques d'un coup

---

## Diagnostic: Modèle Anémique

### Symptômes

```typescript
// ❌ ANEMIC MODEL - Symptômes typiques

// 1. Entity = sac de données
class Order {
  public id: string;
  public customerId: string;
  public lines: OrderLine[];
  public status: string;
  public total: number;
  public createdAt: Date;
  public updatedAt: Date;
}

// 2. Toute la logique dans les services
class OrderService {
  addLine(order: Order, productId: string, qty: number): void {
    const product = this.productRepo.findById(productId);
    order.lines.push({ productId, quantity: qty, price: product.price });
    order.total = this.calculateTotal(order);
    order.updatedAt = new Date();
    this.orderRepo.save(order);
  }

  ship(order: Order): void {
    if (order.status !== 'paid') {
      throw new Error('Cannot ship unpaid order');
    }
    order.status = 'shipped';
    order.updatedAt = new Date();
    this.orderRepo.save(order);
    this.notificationService.sendShippingNotification(order);
  }

  private calculateTotal(order: Order): number {
    return order.lines.reduce((sum, l) => sum + l.price * l.quantity, 0);
  }
}
```

### Red Flags

| Symptôme | Problème |
|----------|----------|
| Setters publics partout | Pas d'encapsulation |
| Logique dans services | Tell-Don't-Ask violé |
| Validation en dehors | Invariants non protégés |
| Primitives types | string, number au lieu de VO |
| Pas d'events | Couplage fort |

---

## Migration Étape par Étape

### Étape 1: Encapsuler les Setters

```typescript
// Avant: setters publics
class Order {
  public status: string;
}

// Après: champs privés + méthodes
class Order {
  private _status: OrderStatus;

  get status(): OrderStatus {
    return this._status;
  }

  // Temporaire: setter pour compatibilité
  /** @deprecated Use domain methods instead */
  setStatus(value: string): void {
    console.warn('Deprecated: use domain methods');
    this._status = OrderStatus.fromValue(value);
  }
}
```

### Étape 2: Introduire les Value Objects

```typescript
// Avant: primitives
class Order {
  public total: number;
  public currency: string;
}

// Après: Value Object
class Order {
  private _total: Money;

  get total(): Money {
    return this._total;
  }

  // Compatibilité temporaire
  get totalAmount(): number {
    return this._total.amount;
  }
}

// Money Value Object
class Money {
  private constructor(
    private readonly _amount: number,
    private readonly _currency: Currency
  ) {}

  static of(amount: number, currency: string): Money {
    return new Money(amount, Currency.fromCode(currency));
  }

  add(other: Money): Money {
    this.ensureSameCurrency(other);
    return Money.of(this._amount + other._amount, this._currency.code);
  }
}
```

### Étape 3: Déplacer la Logique dans l'Entity

```typescript
// Avant: logique dans le service
class OrderService {
  addLine(order: Order, productId: string, qty: number, price: number): void {
    order.lines.push({ productId, quantity: qty, price });
    order.total = order.lines.reduce((s, l) => s + l.price * l.quantity, 0);
  }
}

// Après: logique dans l'entity
class Order {
  private _lines: OrderLine[] = [];
  private _total: Money;

  addLine(line: OrderLine): void {
    // Invariant: pas de doublons
    const existing = this._lines.find(l =>
      l.productId.equals(line.productId)
    );

    if (existing) {
      existing.increaseQuantity(line.quantity);
    } else {
      this._lines.push(line);
    }

    this.recalculateTotal();
  }

  private recalculateTotal(): void {
    this._total = this._lines.reduce(
      (sum, line) => sum.add(line.subtotal()),
      Money.zero(this._total.currency)
    );
  }
}

// Service simplifié (orchestration seulement)
class OrderService {
  addLine(orderId: string, productId: string, qty: number): void {
    const order = this.orderRepo.findById(orderId);
    const product = this.productRepo.findById(productId);

    const line = OrderLine.create(
      ProductId.create(productId),
      product.name,
      Money.of(product.price, 'EUR'),
      qty
    );

    order.addLine(line);  // Logique dans l'entity

    this.orderRepo.save(order);
  }
}
```

### Étape 4: Protéger les Invariants

```typescript
// Avant: validation externe
class OrderService {
  ship(order: Order): void {
    if (order.status !== 'paid') {
      throw new Error('Cannot ship unpaid order');
    }
    if (order.lines.length === 0) {
      throw new Error('Cannot ship empty order');
    }
    order.status = 'shipped';
  }
}

// Après: invariants dans l'entity
class Order {
  ship(trackingNumber: TrackingNumber): void {
    // Invariant 1: doit être payé
    if (!this._status.equals(OrderStatus.Paid)) {
      throw new CannotShipUnpaidOrderError(this._id);
    }

    // Invariant 2: doit avoir des lignes
    if (this._lines.length === 0) {
      throw new CannotShipEmptyOrderError(this._id);
    }

    this._status = OrderStatus.Shipped;
    this._shippedAt = new Date();
    this._trackingNumber = trackingNumber;
  }
}
```

### Étape 5: Introduire les Domain Events

```typescript
// Avant: appels directs aux services
class OrderService {
  ship(order: Order): void {
    order.status = 'shipped';
    this.orderRepo.save(order);

    // Couplage fort
    this.notificationService.sendShippingEmail(order);
    this.inventoryService.releaseReservation(order);
    this.analyticsService.trackShipment(order);
  }
}

// Après: events domain
class Order extends AggregateRoot<OrderId> {
  ship(trackingNumber: TrackingNumber): void {
    this.ensureCanBeShipped();

    this._status = OrderStatus.Shipped;
    this._shippedAt = new Date();

    // Émet un event (découplé)
    this.addDomainEvent(new OrderShipped({
      orderId: this._id,
      trackingNumber,
      shippedAt: this._shippedAt
    }));
  }
}

// Handlers découplés
class SendShippingEmailOnOrderShipped {
  handle(event: OrderShipped): void {
    this.emailService.sendShippingNotification(event.orderId);
  }
}

class ReleaseStockOnOrderShipped {
  handle(event: OrderShipped): void {
    this.inventoryService.releaseReservation(event.orderId);
  }
}
```

---

## Stratégie de Migration

### Approche Strangler Fig

```
Phase 1: Wrapper
┌─────────────────────────────────────┐
│  New Rich Model (wrapper)           │
│  ┌─────────────────────────────┐    │
│  │  Legacy Anemic Model        │    │
│  │  (untouched)                │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘

Phase 2: Migration progressive
┌─────────────────────────────────────┐
│  New Rich Model                     │
│  ┌──────────┐  ┌──────────────┐    │
│  │ Migrated │  │ Legacy       │    │
│  │ Logic    │  │ (shrinking)  │    │
│  └──────────┘  └──────────────┘    │
└─────────────────────────────────────┘

Phase 3: Terminé
┌─────────────────────────────────────┐
│  Rich Domain Model                  │
│  (legacy removed)                   │
└─────────────────────────────────────┘
```

### Checklist de Migration

| Phase | Action | Test |
|-------|--------|------|
| 1 | Encapsuler les champs | Getters fonctionnent |
| 2 | Créer les Value Objects | Equals/validation OK |
| 3 | Déplacer 1 méthode | Tests existants passent |
| 4 | Ajouter invariants | Exceptions levées |
| 5 | Émettre events | Handlers appelés |
| 6 | Supprimer code legacy | Aucune régression |

---

## Anti-patterns à Éviter

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Big Bang rewrite | Trop risqué | Strangler Fig |
| Dual-write | Incohérence | Event sourcing ou flag |
| Facade over anemic | Toujours anémique | Vraie migration |

---

## Mots-clés de routage

`migration`, `anemic`, `rich domain`, `refactoring`, `legacy`, `strangler`
