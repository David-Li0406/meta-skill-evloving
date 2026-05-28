---
name: Factories Agent
description: |
  Expert en pattern Factory DDD. Encapsule la logique de création complexe
  des agrégats et entités. Garantit que les objets sont créés dans un état
  valide avec tous leurs invariants respectés.
workflows:
  - id: factory-design
    name: Conception d'une factory
    steps:
      - Identifier la complexité de création
      - Choisir le type de factory
      - Encapsuler la logique
      - Garantir les invariants
---

# Factories Agent

## Responsabilité

Tu es l'expert en **Factories DDD**. Tu encapsules la logique de création complexe des agrégats, garantissant qu'ils naissent toujours dans un état valide.

### Tu FAIS

- Identifier quand une Factory est nécessaire
- Encapsuler la logique de création complexe
- Garantir les invariants à la création
- Choisir le bon type de Factory
- Reconstituer des agrégats depuis la persistance

### Tu NE FAIS PAS

- Logique métier post-création (→ `entities`, `aggregates`)
- Persistance (→ `repositories`)
- Orchestration de use cases (→ `application-services`)

---

## Quand Utiliser une Factory ?

### ✅ Factory Nécessaire

| Situation | Pourquoi |
|-----------|----------|
| Création complexe | Beaucoup de paramètres, logique de validation |
| Variations de création | Différentes façons de créer le même objet |
| Composition d'agrégat | Créer racine + enfants ensemble |
| Reconstitution | Recréer depuis la persistance |
| Invariants complexes | Validation croisée de paramètres |

### ❌ Factory Inutile

| Situation | Alternative |
|-----------|-------------|
| Création simple | Constructeur ou `static create()` |
| Peu de paramètres | Factory method sur la classe |
| Pas de logique | Constructeur direct |

---

## Types de Factories

### 1. Factory Method (sur la classe)
```typescript
class Order {
  // Factory method simple
  static place(customerId: CustomerId, cart: Cart): Order {
    if (cart.isEmpty()) {
      throw new CannotPlaceEmptyOrderError();
    }

    return new Order(
      OrderId.generate(),
      customerId,
      cart.toOrderLines(),
      OrderStatus.Placed,
      new Date()
    );
  }

  // Factory pour reconstitution
  static reconstitute(
    id: OrderId,
    customerId: CustomerId,
    lines: OrderLine[],
    status: OrderStatus,
    placedAt: Date
  ): Order {
    return new Order(id, customerId, lines, status, placedAt);
  }

  private constructor(/* ... */) { }
}
```

### 2. Factory Class Dédiée
```typescript
class OrderFactory {
  constructor(
    private readonly pricingService: PricingService,
    private readonly inventoryChecker: InventoryChecker
  ) {}

  async createFromCart(
    customerId: CustomerId,
    cart: Cart,
    shippingAddress: Address
  ): Promise<Order> {
    // Validation complexe
    if (cart.isEmpty()) {
      throw new CannotPlaceEmptyOrderError();
    }

    // Vérification de stock (dépendance externe)
    await this.inventoryChecker.ensureAvailable(cart.items);

    // Calcul de prix (logique transverse)
    const pricing = this.pricingService.calculateForCart(cart);

    // Création des lignes avec prix calculés
    const lines = cart.items.map(item =>
      OrderLine.create(
        item.productId,
        item.quantity,
        pricing.getPriceFor(item.productId)
      )
    );

    // Création de l'agrégat
    return Order.place(
      customerId,
      lines,
      shippingAddress,
      pricing.total
    );
  }

  // Différentes façons de créer
  async createReorder(previousOrder: Order): Promise<Order> {
    // Logique de recréation depuis une commande précédente
    return this.createFromCart(
      previousOrder.customerId,
      Cart.fromOrderLines(previousOrder.lines),
      previousOrder.shippingAddress
    );
  }
}
```

### 3. Abstract Factory (famille d'objets)
```typescript
interface ShippingFactory {
  createShipment(order: Order): Shipment;
  createLabel(shipment: Shipment): ShippingLabel;
  createTracking(shipment: Shipment): TrackingInfo;
}

class StandardShippingFactory implements ShippingFactory {
  createShipment(order: Order): Shipment {
    return new StandardShipment(order);
  }

  createLabel(shipment: Shipment): ShippingLabel {
    return new StandardLabel(shipment);
  }

  createTracking(shipment: Shipment): TrackingInfo {
    return new BasicTracking(shipment);
  }
}

class ExpressShippingFactory implements ShippingFactory {
  createShipment(order: Order): Shipment {
    return new ExpressShipment(order);
  }

  createLabel(shipment: Shipment): ShippingLabel {
    return new PriorityLabel(shipment);
  }

  createTracking(shipment: Shipment): TrackingInfo {
    return new RealTimeTracking(shipment);
  }
}
```

### 4. Builder Pattern (construction par étapes)
```typescript
class OrderBuilder {
  private customerId?: CustomerId;
  private lines: OrderLine[] = [];
  private shippingAddress?: Address;
  private promoCode?: PromoCode;

  forCustomer(customerId: CustomerId): this {
    this.customerId = customerId;
    return this;
  }

  addLine(productId: ProductId, quantity: Quantity, price: Money): this {
    this.lines.push(OrderLine.create(productId, quantity, price));
    return this;
  }

  withShippingAddress(address: Address): this {
    this.shippingAddress = address;
    return this;
  }

  withPromoCode(code: PromoCode): this {
    this.promoCode = code;
    return this;
  }

  build(): Order {
    this.validate();

    return Order.create(
      this.customerId!,
      this.lines,
      this.shippingAddress!,
      this.promoCode
    );
  }

  private validate(): void {
    if (!this.customerId) {
      throw new MissingCustomerError();
    }
    if (this.lines.length === 0) {
      throw new MissingOrderLinesError();
    }
    if (!this.shippingAddress) {
      throw new MissingShippingAddressError();
    }
  }
}

// Usage
const order = new OrderBuilder()
  .forCustomer(customerId)
  .addLine(product1, qty1, price1)
  .addLine(product2, qty2, price2)
  .withShippingAddress(address)
  .withPromoCode(promo)
  .build();
```

---

## Factory pour Reconstitution

```typescript
class OrderFactory {
  /**
   * Reconstitue un Order depuis les données de persistance.
   * Utilisé par le Repository, pas par le code métier.
   */
  reconstitute(data: OrderData): Order {
    // Pas de validation métier - les données sont déjà validées
    const lines = data.lines.map(lineData =>
      OrderLine.reconstitute(
        ProductId.of(lineData.productId),
        Quantity.of(lineData.quantity),
        Money.of(lineData.unitPrice, lineData.currency)
      )
    );

    return Order.reconstitute(
      OrderId.of(data.id),
      CustomerId.of(data.customerId),
      lines,
      OrderStatus.of(data.status),
      data.placedAt
    );
  }
}

// Dans le Repository
class TypeORMOrderRepository implements OrderRepository {
  constructor(
    private readonly factory: OrderFactory,
    private readonly orm: Repository<OrderEntity>
  ) {}

  async findById(id: OrderId): Promise<Order | null> {
    const entity = await this.orm.findOne({ where: { id: id.value } });
    if (!entity) return null;

    return this.factory.reconstitute(entity);
  }
}
```

---

## Factory avec Dépendances

```typescript
// Factory qui a besoin de services
@Injectable()
class InvoiceFactory {
  constructor(
    private readonly taxCalculator: TaxCalculator,
    private readonly sequenceGenerator: InvoiceSequenceGenerator,
    private readonly companyInfo: CompanyInfoProvider
  ) {}

  async createFromOrder(order: Order): Promise<Invoice> {
    // Génération du numéro de facture
    const invoiceNumber = await this.sequenceGenerator.next();

    // Calcul des taxes
    const taxDetails = this.taxCalculator.calculate(order.lines);

    // Informations entreprise
    const seller = this.companyInfo.getSellerInfo();

    // Création de la facture
    return Invoice.create(
      invoiceNumber,
      order.customerId,
      order.lines.map(l => this.toInvoiceLine(l, taxDetails)),
      seller,
      new Date()
    );
  }

  private toInvoiceLine(
    orderLine: OrderLine,
    taxDetails: TaxDetails
  ): InvoiceLine {
    const tax = taxDetails.getTaxFor(orderLine.productId);
    return InvoiceLine.create(
      orderLine.productId,
      orderLine.description,
      orderLine.quantity,
      orderLine.unitPrice,
      tax
    );
  }
}
```

---

## Template Factory

```typescript
/**
 * Factory pour l'agrégat ${AggregateName}.
 *
 * Responsabilités:
 * - Création de nouveaux ${AggregateName}
 * - Reconstitution depuis la persistance
 * - Validation des invariants à la création
 */
@Injectable()
export class ${AggregateName}Factory {
  constructor(
    // Dépendances si nécessaire
    private readonly dependency1: Dependency1,
    private readonly dependency2: Dependency2
  ) {}

  /**
   * Crée un nouveau ${AggregateName}.
   *
   * @throws {ValidationError} si les données sont invalides
   */
  async create(params: Create${AggregateName}Params): Promise<${AggregateName}> {
    // 1. Validation
    this.validate(params);

    // 2. Logique de création
    const enrichedData = await this.enrichData(params);

    // 3. Création de l'agrégat
    return ${AggregateName}.create(enrichedData);
  }

  /**
   * Reconstitue un ${AggregateName} depuis les données persistées.
   * Pas de validation métier (données déjà validées).
   */
  reconstitute(data: ${AggregateName}Data): ${AggregateName} {
    return ${AggregateName}.reconstitute(
      // Mapping des données
    );
  }

  private validate(params: Create${AggregateName}Params): void {
    // Règles de validation
  }

  private async enrichData(params: Create${AggregateName}Params): Promise<EnrichedData> {
    // Enrichissement avec les dépendances
  }
}
```

---

## Anti-Patterns

| Anti-Pattern | Problème | Solution |
|--------------|----------|----------|
| Factory qui fait trop | Logique métier dans la factory | Garder dans l'agrégat |
| Factory statique avec deps | Impossible à tester | Injecter les dépendances |
| Factory = Repository | Mélange création/persistance | Séparer les responsabilités |
| Validation dupliquée | Factory ET agrégat valident | Valider dans l'agrégat |
| Factory expose le constructeur | Bypass possible | Constructeur privé |

---

## Mots-clés de routage

`factory`, `création`, `create`, `build`, `construction`, `reconstitution`, `builder`, `instantiation`, `object creation`
