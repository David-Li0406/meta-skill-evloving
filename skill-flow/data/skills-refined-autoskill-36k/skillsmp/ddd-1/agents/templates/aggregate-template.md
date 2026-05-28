---
name: Aggregate Template
description: |
  Template de scaffolding pour créer un Aggregate DDD.
  Génère la structure complète avec racine, entités, value objects,
  invariants et domain events.
workflows:
  - id: scaffold-aggregate
    name: Scaffolding Aggregate
    steps:
      - Définir la racine d'agrégat
      - Identifier les entités internes
      - Extraire les value objects
      - Définir les invariants
      - Identifier les domain events
---

# Aggregate Template

## Responsabilité

Tu génères des **templates d'Aggregates DDD** prêts à l'emploi, avec tous les building blocks nécessaires.

### Tu FAIS

- Générer la structure complète d'un aggregate
- Inclure les invariants et validations
- Proposer les domain events associés
- Adapter au langage/framework cible

### Tu NE FAIS PAS

- Implémenter la persistance (→ `repositories`)
- Gérer les use cases (→ `application-services`)
- Définir les bounded contexts (→ `bounded-contexts`)

---

## Template Structure

```
[AggregateName]/
├── [AggregateName].ts          # Aggregate Root
├── [AggregateName]Id.ts        # Identity (Value Object)
├── entities/
│   └── [EntityName].ts         # Child Entities
├── value-objects/
│   ├── [VOName].ts             # Value Objects
│   └── ...
├── events/
│   ├── [AggregateName]Created.ts
│   ├── [AggregateName]Updated.ts
│   └── ...
└── specifications/
    └── [RuleName]Specification.ts
```

---

## Template: Aggregate Root

### TypeScript

```typescript
// ============================================
// Order Aggregate - E-commerce Domain
// ============================================

import { AggregateRoot } from '@core/ddd';
import { OrderId } from './OrderId';
import { OrderLine } from './entities/OrderLine';
import { Money } from './value-objects/Money';
import { Address } from './value-objects/Address';
import { OrderStatus } from './value-objects/OrderStatus';
import { OrderPlaced } from './events/OrderPlaced';
import { OrderShipped } from './events/OrderShipped';

export class Order extends AggregateRoot<OrderId> {
  private _customerId: CustomerId;
  private _lines: OrderLine[];
  private _shippingAddress: Address;
  private _status: OrderStatus;
  private _placedAt: Date;

  private constructor(
    id: OrderId,
    customerId: CustomerId,
    lines: OrderLine[],
    shippingAddress: Address
  ) {
    super(id);
    this._customerId = customerId;
    this._lines = lines;
    this._shippingAddress = shippingAddress;
    this._status = OrderStatus.Pending;
    this._placedAt = new Date();
  }

  // ========== Factory Method ==========

  static place(
    id: OrderId,
    customerId: CustomerId,
    lines: OrderLine[],
    shippingAddress: Address
  ): Order {
    // Invariant: Order must have at least one line
    if (lines.length === 0) {
      throw new EmptyOrderError();
    }

    // Invariant: All lines must have positive quantities
    if (lines.some(line => line.quantity <= 0)) {
      throw new InvalidQuantityError();
    }

    const order = new Order(id, customerId, lines, shippingAddress);

    order.addDomainEvent(new OrderPlaced({
      orderId: id,
      customerId,
      totalAmount: order.totalAmount(),
      placedAt: order._placedAt
    }));

    return order;
  }

  // ========== Behavior ==========

  addLine(line: OrderLine): void {
    this.ensureNotShipped();

    const existingLine = this._lines.find(l =>
      l.productId.equals(line.productId)
    );

    if (existingLine) {
      existingLine.increaseQuantity(line.quantity);
    } else {
      this._lines.push(line);
    }

    this.addDomainEvent(new OrderLineAdded({
      orderId: this.id,
      productId: line.productId,
      quantity: line.quantity
    }));
  }

  removeLine(productId: ProductId): void {
    this.ensureNotShipped();

    const index = this._lines.findIndex(l =>
      l.productId.equals(productId)
    );

    if (index === -1) {
      throw new LineNotFoundError(productId);
    }

    this._lines.splice(index, 1);

    // Invariant: Order cannot become empty
    if (this._lines.length === 0) {
      throw new CannotRemoveLastLineError();
    }
  }

  ship(trackingNumber: TrackingNumber): void {
    // Invariant: Can only ship pending orders
    if (!this._status.equals(OrderStatus.Pending)) {
      throw new InvalidOrderStateError(
        `Cannot ship order in ${this._status.value} state`
      );
    }

    this._status = OrderStatus.Shipped;

    this.addDomainEvent(new OrderShipped({
      orderId: this.id,
      trackingNumber,
      shippedAt: new Date()
    }));
  }

  cancel(reason: CancellationReason): void {
    this.ensureNotShipped();

    this._status = OrderStatus.Cancelled;

    this.addDomainEvent(new OrderCancelled({
      orderId: this.id,
      reason,
      cancelledAt: new Date()
    }));
  }

  // ========== Queries ==========

  totalAmount(): Money {
    return this._lines.reduce(
      (total, line) => total.add(line.subtotal()),
      Money.zero(this._lines[0].unitPrice.currency)
    );
  }

  get status(): OrderStatus {
    return this._status;
  }

  get lines(): readonly OrderLine[] {
    return [...this._lines];
  }

  // ========== Invariants (private) ==========

  private ensureNotShipped(): void {
    if (this._status.equals(OrderStatus.Shipped)) {
      throw new OrderAlreadyShippedError();
    }
  }
}
```

### Java

```java
// ============================================
// Order Aggregate - E-commerce Domain (Java)
// ============================================

public class Order extends AggregateRoot<OrderId> {

    private final CustomerId customerId;
    private final List<OrderLine> lines;
    private Address shippingAddress;
    private OrderStatus status;
    private final Instant placedAt;

    private Order(
        OrderId id,
        CustomerId customerId,
        List<OrderLine> lines,
        Address shippingAddress
    ) {
        super(id);
        this.customerId = customerId;
        this.lines = new ArrayList<>(lines);
        this.shippingAddress = shippingAddress;
        this.status = OrderStatus.PENDING;
        this.placedAt = Instant.now();
    }

    // Factory method
    public static Order place(
        OrderId id,
        CustomerId customerId,
        List<OrderLine> lines,
        Address shippingAddress
    ) {
        Preconditions.checkArgument(!lines.isEmpty(),
            "Order must have at least one line");

        Preconditions.checkArgument(
            lines.stream().allMatch(l -> l.getQuantity() > 0),
            "All lines must have positive quantities"
        );

        Order order = new Order(id, customerId, lines, shippingAddress);

        order.registerEvent(new OrderPlaced(
            id, customerId, order.totalAmount(), order.placedAt
        ));

        return order;
    }

    public void ship(TrackingNumber trackingNumber) {
        if (status != OrderStatus.PENDING) {
            throw new InvalidOrderStateException(
                "Cannot ship order in " + status + " state"
            );
        }

        this.status = OrderStatus.SHIPPED;
        registerEvent(new OrderShipped(id, trackingNumber, Instant.now()));
    }

    public Money totalAmount() {
        return lines.stream()
            .map(OrderLine::subtotal)
            .reduce(Money.ZERO, Money::add);
    }

    public List<OrderLine> getLines() {
        return Collections.unmodifiableList(lines);
    }
}
```

---

## Template: Value Object

```typescript
// ============================================
// Money Value Object
// ============================================

export class Money {
  private constructor(
    private readonly _amount: number,
    private readonly _currency: Currency
  ) {
    if (_amount < 0) {
      throw new NegativeAmountError();
    }
  }

  static of(amount: number, currency: Currency): Money {
    return new Money(amount, currency);
  }

  static zero(currency: Currency): Money {
    return new Money(0, currency);
  }

  add(other: Money): Money {
    this.ensureSameCurrency(other);
    return new Money(this._amount + other._amount, this._currency);
  }

  subtract(other: Money): Money {
    this.ensureSameCurrency(other);
    const result = this._amount - other._amount;
    if (result < 0) {
      throw new InsufficientFundsError();
    }
    return new Money(result, this._currency);
  }

  multiply(factor: number): Money {
    return new Money(this._amount * factor, this._currency);
  }

  equals(other: Money): boolean {
    return this._amount === other._amount
      && this._currency.equals(other._currency);
  }

  private ensureSameCurrency(other: Money): void {
    if (!this._currency.equals(other._currency)) {
      throw new CurrencyMismatchError(this._currency, other._currency);
    }
  }

  get amount(): number { return this._amount; }
  get currency(): Currency { return this._currency; }
}
```

---

## Template: Domain Event

```typescript
// ============================================
// OrderPlaced Domain Event
// ============================================

export class OrderPlaced extends DomainEvent {
  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly totalAmount: Money,
    public readonly placedAt: Date
  ) {
    super();
  }

  get eventType(): string {
    return 'order.placed';
  }

  get aggregateId(): string {
    return this.orderId.value;
  }

  toPayload(): Record<string, unknown> {
    return {
      orderId: this.orderId.value,
      customerId: this.customerId.value,
      totalAmount: {
        amount: this.totalAmount.amount,
        currency: this.totalAmount.currency.code
      },
      placedAt: this.placedAt.toISOString()
    };
  }
}
```

---

## Template: Entity (Child)

```typescript
// ============================================
// OrderLine Entity (part of Order Aggregate)
// ============================================

export class OrderLine extends Entity<OrderLineId> {
  private _quantity: number;

  constructor(
    id: OrderLineId,
    private readonly _productId: ProductId,
    private readonly _productName: string,
    private readonly _unitPrice: Money,
    quantity: number
  ) {
    super(id);
    this.setQuantity(quantity);
  }

  increaseQuantity(amount: number): void {
    this.setQuantity(this._quantity + amount);
  }

  decreaseQuantity(amount: number): void {
    const newQuantity = this._quantity - amount;
    if (newQuantity <= 0) {
      throw new InvalidQuantityError('Quantity must be positive');
    }
    this._quantity = newQuantity;
  }

  subtotal(): Money {
    return this._unitPrice.multiply(this._quantity);
  }

  private setQuantity(value: number): void {
    if (value <= 0) {
      throw new InvalidQuantityError('Quantity must be positive');
    }
    this._quantity = value;
  }

  get productId(): ProductId { return this._productId; }
  get quantity(): number { return this._quantity; }
  get unitPrice(): Money { return this._unitPrice; }
}
```

---

## Checklist de Création

Avant de valider ton aggregate, vérifie :

| Check | Description |
|-------|-------------|
| [ ] **Identité** | L'aggregate a un ID typé (Value Object) |
| [ ] **Factory** | Création via factory method, pas new public |
| [ ] **Invariants** | Toutes les règles métier sont protégées |
| [ ] **Immutabilité** | Pas de setters publics, mutations contrôlées |
| [ ] **Events** | Chaque changement d'état émet un event |
| [ ] **Encapsulation** | Collections retournées en readonly |
| [ ] **Taille** | < 5 entités internes (sinon découper) |

---

## Mots-clés de routage

`template`, `scaffolding`, `générer`, `créer aggregate`, `structure aggregate`, `boilerplate`, `starter`
