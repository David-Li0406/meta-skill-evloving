---
name: E-Commerce Domain Case Study
description: |
  Case study complet d'un domaine e-commerce modélisé en DDD.
  Couvre discovery, bounded contexts, aggregates et events.
workflows:
  - id: ecommerce-study
    name: Étude E-Commerce
    steps:
      - Event Storming du domaine
      - Identification des Bounded Contexts
      - Modélisation des Aggregates
      - Définition des Domain Events
---

# E-Commerce Domain Case Study

## Responsabilité

Tu fournis un **exemple end-to-end** de modélisation DDD sur un domaine e-commerce.

### Tu FAIS

- Montrer le workflow complet DDD
- Illustrer chaque building block
- Fournir des exemples de code
- Expliquer les décisions de design

### Tu NE FAIS PAS

- Implémenter l'infrastructure (→ `backend-developer`)
- Détailler les tests (→ `testing-process`)

---

## 1. Event Storming Output

```
Timeline du processus de commande:
──────────────────────────────────────────────────────────────

[Customer]        [Catalog]         [Order]           [Payment]
    │                 │                 │                 │
    │  ProductViewed  │                 │                 │
    │────────────────>│                 │                 │
    │                 │                 │                 │
    │  ProductAddedToCart               │                 │
    │────────────────────────────────-->│                 │
    │                 │                 │                 │
    │  CartCheckedOut │                 │                 │
    │────────────────────────────────-->│                 │
    │                 │                 │  OrderPlaced    │
    │                 │                 │────────────────>│
    │                 │                 │                 │
    │                 │                 │  PaymentReceived│
    │                 │                 │<────────────────│
    │                 │                 │                 │
    │                 │  StockReserved  │                 │
    │                 │<────────────────│                 │
    │                 │                 │                 │
    │                 │                 │  OrderShipped   │
    │                 │                 │────────────────>│
```

### Domain Events Identifiés

| Event | Bounded Context | Trigger |
|-------|----------------|---------|
| ProductViewed | Catalog | User action |
| ProductAddedToCart | Shopping | User action |
| CartCheckedOut | Shopping | User action |
| OrderPlaced | Ordering | Command |
| PaymentReceived | Payment | External |
| StockReserved | Inventory | Event reaction |
| OrderShipped | Shipping | Command |

---

## 2. Bounded Contexts

```
┌─────────────────────────────────────────────────────────────────┐
│                        E-COMMERCE SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   CATALOG    │    │   SHOPPING   │    │   ORDERING   │       │
│  │   Context    │───>│   Context    │───>│   Context    │       │
│  │              │    │              │    │              │       │
│  │  • Product   │    │  • Cart      │    │  • Order     │       │
│  │  • Category  │    │  • CartItem  │    │  • OrderLine │       │
│  │  • Price     │    │              │    │  • Customer  │       │
│  └──────────────┘    └──────────────┘    └──────┬───────┘       │
│         │                                        │               │
│         │                                        ▼               │
│  ┌──────▼───────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  INVENTORY   │    │   PAYMENT    │    │   SHIPPING   │       │
│  │   Context    │<───│   Context    │<───│   Context    │       │
│  │              │    │              │    │              │       │
│  │  • Stock     │    │  • Payment   │    │  • Shipment  │       │
│  │  • Warehouse │    │  • Refund    │    │  • Tracking  │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Context Map

| Relation | Upstream | Downstream | Type |
|----------|----------|------------|------|
| Catalog → Shopping | Catalog | Shopping | Conformist |
| Shopping → Ordering | Shopping | Ordering | Customer-Supplier |
| Ordering → Payment | Ordering | Payment | Partnership |
| Ordering → Inventory | Ordering | Inventory | ACL |
| Ordering → Shipping | Ordering | Shipping | Published Language |

---

## 3. Core Domain: Ordering

### Ubiquitous Language

| Terme | Définition |
|-------|------------|
| **Order** | Demande d'achat validée par un client |
| **OrderLine** | Ligne de commande (produit + quantité) |
| **OrderStatus** | État du cycle de vie (Pending, Paid, Shipped, Delivered) |
| **PlaceOrder** | Acte de passer une commande |
| **ShipOrder** | Expédier physiquement la commande |

### Order Aggregate

```typescript
// domain/ordering/Order.ts

export class Order extends AggregateRoot<OrderId> {
  private _customerId: CustomerId;
  private _lines: OrderLine[];
  private _shippingAddress: Address;
  private _billingAddress: Address;
  private _status: OrderStatus;
  private _placedAt: Date;
  private _paidAt?: Date;
  private _shippedAt?: Date;

  // Factory: seul point d'entrée pour créer
  static place(props: PlaceOrderProps): Order {
    const order = new Order();
    order._id = props.orderId;
    order._customerId = props.customerId;
    order._lines = props.lines;
    order._shippingAddress = props.shippingAddress;
    order._billingAddress = props.billingAddress ?? props.shippingAddress;
    order._status = OrderStatus.Pending;
    order._placedAt = new Date();

    // Invariant: au moins une ligne
    order.ensureHasLines();

    // Invariant: montant positif
    order.ensurePositiveTotal();

    order.addDomainEvent(new OrderPlaced({
      orderId: order._id,
      customerId: order._customerId,
      lines: order._lines.map(l => l.toSnapshot()),
      totalAmount: order.totalAmount(),
      placedAt: order._placedAt
    }));

    return order;
  }

  // Behavior: marquer comme payé
  markAsPaid(paymentId: PaymentId): void {
    if (!this._status.equals(OrderStatus.Pending)) {
      throw new InvalidOrderStateError(
        `Cannot pay order in ${this._status} state`
      );
    }

    this._status = OrderStatus.Paid;
    this._paidAt = new Date();

    this.addDomainEvent(new OrderPaid({
      orderId: this._id,
      paymentId,
      paidAt: this._paidAt
    }));
  }

  // Behavior: expédier
  ship(shipmentId: ShipmentId, trackingNumber: TrackingNumber): void {
    if (!this._status.equals(OrderStatus.Paid)) {
      throw new InvalidOrderStateError(
        `Cannot ship unpaid order`
      );
    }

    this._status = OrderStatus.Shipped;
    this._shippedAt = new Date();

    this.addDomainEvent(new OrderShipped({
      orderId: this._id,
      shipmentId,
      trackingNumber,
      shippedAt: this._shippedAt
    }));
  }

  // Query
  totalAmount(): Money {
    return this._lines.reduce(
      (sum, line) => sum.add(line.subtotal()),
      Money.zero('EUR')
    );
  }

  // Invariants privés
  private ensureHasLines(): void {
    if (this._lines.length === 0) {
      throw new EmptyOrderError();
    }
  }

  private ensurePositiveTotal(): void {
    if (this.totalAmount().isZero()) {
      throw new ZeroTotalError();
    }
  }
}
```

### Value Objects

```typescript
// OrderStatus - Enum-style Value Object
export class OrderStatus extends ValueObject<string> {
  static readonly Pending = new OrderStatus('pending');
  static readonly Paid = new OrderStatus('paid');
  static readonly Shipped = new OrderStatus('shipped');
  static readonly Delivered = new OrderStatus('delivered');
  static readonly Cancelled = new OrderStatus('cancelled');

  private constructor(value: string) {
    super(value);
  }

  canTransitionTo(target: OrderStatus): boolean {
    const allowed: Record<string, string[]> = {
      pending: ['paid', 'cancelled'],
      paid: ['shipped', 'cancelled'],
      shipped: ['delivered'],
      delivered: [],
      cancelled: []
    };
    return allowed[this.value].includes(target.value);
  }
}

// Address Value Object
export class Address extends ValueObject<AddressProps> {
  get street(): string { return this.props.street; }
  get city(): string { return this.props.city; }
  get postalCode(): string { return this.props.postalCode; }
  get country(): string { return this.props.country; }

  format(): string {
    return `${this.street}\n${this.postalCode} ${this.city}\n${this.country}`;
  }
}
```

---

## 4. Application Layer

```typescript
// application/commands/PlaceOrderHandler.ts

export class PlaceOrderHandler {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly productReader: ProductReadModel,
    private readonly eventBus: DomainEventBus
  ) {}

  async handle(cmd: PlaceOrderCommand): Promise<OrderId> {
    // 1. Créer les OrderLines depuis le panier
    const lines = await Promise.all(
      cmd.cartItems.map(async item => {
        const product = await this.productReader.getById(item.productId);
        return new OrderLine(
          OrderLineId.generate(),
          ProductId.create(item.productId),
          product.name,
          Money.of(product.price, 'EUR'),
          item.quantity
        );
      })
    );

    // 2. Créer l'Order (factory method)
    const order = Order.place({
      orderId: this.orderRepo.nextId(),
      customerId: CustomerId.create(cmd.customerId),
      lines,
      shippingAddress: Address.create(cmd.shippingAddress)
    });

    // 3. Persister
    await this.orderRepo.save(order);

    // 4. Publier les events
    await this.eventBus.publishAll(order.pullDomainEvents());

    return order.id;
  }
}
```

---

## 5. Integration Events

```typescript
// Ordering → Inventory (via message broker)

// Event publié par Ordering
interface OrderPlacedIntegrationEvent {
  eventType: 'ordering.order.placed';
  orderId: string;
  lines: Array<{
    productId: string;
    quantity: number;
  }>;
  occurredAt: string;
}

// Handler dans Inventory (ACL)
class ReserveStockOnOrderPlaced {
  async handle(event: OrderPlacedIntegrationEvent): Promise<void> {
    // Traduire vers le langage d'Inventory
    for (const line of event.lines) {
      await this.stockService.reserve(
        SkuId.fromProductId(line.productId),  // ACL translation
        line.quantity,
        ReservationReason.CustomerOrder(event.orderId)
      );
    }
  }
}
```

---

## Résumé

| Aspect | Choix | Raison |
|--------|-------|--------|
| Core Domain | Ordering | Différenciateur business |
| Aggregate principal | Order | Invariants de cohérence |
| Eventual Consistency | Ordering ↔ Inventory | Scalabilité |
| ACL | Inventory | Langage différent (SKU vs ProductId) |

---

## Mots-clés de routage

`case study`, `e-commerce`, `exemple complet`, `end-to-end`, `ordering`, `commande`
