# Class Diagram Templates

Class diagrams show the structure of a system using object-oriented design concepts. They display classes, interfaces, attributes, methods, and relationships like inheritance, composition, and association.

---

## Template 1: E-Commerce Domain Model

**Purpose**: Show core domain classes and their relationships

```
┌────────────────────────────────────────────────────────────┐
│             E-Commerce Domain Model                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ <<interface>>                                       │ │
│  │ Payable                                             │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │ + processPayment(amount): boolean                   │ │
│  │ + refund(transactionId): boolean                    │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       ▲                                    │
│                       │ implements                         │
│                       │                                    │
│  ┌────────────────────┴─────────────────────────────────┐ │
│  │                                                       │ │
│  ▼                                                       ▼ │
│  ┌──────────────────────┐                ┌──────────────────┐
│  │ CreditCard           │                │ PayPalAccount    │
│  ├──────────────────────┤                ├──────────────────┤
│  │ - cardNumber: string │                │ - email: string  │
│  │ - expiryDate: Date   │                │ - accountId: int │
│  │ - cvv: string        │                │                  │
│  ├──────────────────────┤                ├──────────────────┤
│  │ + getCardHolder()    │                │ + getEmail()     │
│  │ + isExpired()        │                │ + verify()       │
│  └──────────────────────┘                └──────────────────┘
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Order                             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ - orderId: int                                       │  │
│  │ - customer: Customer                                 │  │
│  │ - items: OrderItem[]                                 │  │
│  │ - status: OrderStatus enum                           │  │
│  │ - createdAt: DateTime                                │  │
│  │ - totalAmount: decimal                               │  │
│  │ - paymentMethod: Payable                             │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ + addItem(product, quantity): void                   │  │
│  │ + removeItem(itemId): void                           │  │
│  │ + calculateTotal(): decimal                          │  │
│  │ + process(): boolean                                 │  │
│  │ + getStatus(): OrderStatus                           │  │
│  └──────────────────────────────────────────────────────┘  │
│         ▲        ▲                  ▲         ▲             │
│         │        │ 1 uses          │         │             │
│         │        │                 1         │             │
│    uses │        │                 │         │             │
│    0..* │        │                 │    has  │             │
│         │        │              1..*       0..1            │
│         │        │                 │         │             │
│  ┌──────┴───┐    │            ┌────┴────────┴───┐          │
│  │          │    └────────────┤                 │          │
│  ▼          ▼                  ▼                 ▼          │
│  ┌──────────────────┐    ┌──────────────────┐ ┌──────────┐
│  │   Customer       │    │  OrderItem       │ │ Product  │
│  ├──────────────────┤    ├──────────────────┤ ├──────────┤
│  │ - customerId: int│    │ - itemId: int    │ │- id: int │
│  │ - name: string   │    │ - product: Prod. │ │- name    │
│  │ - email: string  │    │ - quantity: int  │ │- price   │
│  │ - address: Addr. │    │ - unitPrice: dec │ │- stock   │
│  │ - phone: string  │    │ - subtotal: dec  │ │- category│
│  ├──────────────────┤    ├──────────────────┤ ├──────────┤
│  │ + getOrders()    │    │ + getSubtotal()  │ │+ inStock │
│  │ + getTotalSpent()│    │ + applyDiscount()│ │+ getPrice│
│  │ + register()     │    │                  │ │          │
│  └──────────────────┘    └──────────────────┘ └──────────┘
│           │
│           │ has
│           1
│           │
│  ┌────────┴──────────┐
│  │                   │
│  ▼                   ▼
│  ┌────────────────────────┐  ┌────────────────────────┐
│  │   ShippingAddress      │  │   BillingAddress       │
│  ├────────────────────────┤  ├────────────────────────┤
│  │ - street: string       │  │ - street: string       │
│  │ - city: string         │  │ - city: string         │
│  │ - state: string        │  │ - state: string        │
│  │ - zipCode: string      │  │ - zipCode: string      │
│  │ - country: string      │  │ - country: string      │
│  ├────────────────────────┤  ├────────────────────────┤
│  │ + isValid(): boolean   │  │ + isValid(): boolean   │
│  │ + format(): string     │  │ + format(): string     │
│  └────────────────────────┘  └────────────────────────┘
│           ▲                              ▲
│           │ extends                      │ extends
│           │                              │
│           └──────────────────┬───────────┘
│                              │
│                   ┌──────────┴──────────┐
│                   │                     │
│                   ▼                     ▼
│           ┌───────────────┐      ┌──────────────┐
│           │  Address      │      │  <<enum>>    │
│           ├───────────────┤      │ OrderStatus  │
│           │ - type: string│      ├──────────────┤
│           │ - timestamp   │      │ PENDING      │
│           ├───────────────┤      │ CONFIRMED    │
│           │ + update()    │      │ SHIPPED      │
│           │ + verify()    │      │ DELIVERED    │
│           └───────────────┘      │ CANCELLED    │
│                                  └──────────────┘
│
└────────────────────────────────────────────────────────────┘

Legend:
- Solid line with arrow (→): Association
- Dashed line with arrow (⇢): Implementation
- Triangle (△): Inheritance/Extension
- Label: 0..*, 1, 1..* = Cardinality
```

### Key Relationships
- **Association**: Customer has multiple Orders (1..*)
- **Composition**: Order contains OrderItems (1..*)
- **Inheritance**: Address is parent of ShippingAddress and BillingAddress
- **Interface Implementation**: Order uses Payable interface
- **Aggregation**: Order uses Product (weak ownership)

---

## Template 2: Repository Pattern Architecture

**Purpose**: Show data access layer with repositories and models

```
┌────────────────────────────────────────────────────────────┐
│            Repository Pattern - Data Access                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ <<interface>>                                       │ │
│  │ IRepository<T>                                      │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │ + getAll(): T[]                                     │ │
│  │ + getById(id): T                                    │ │
│  │ + create(entity: T): T                              │ │
│  │ + update(id, entity: T): boolean                    │ │
│  │ + delete(id): boolean                               │ │
│  │ + find(predicate): T[]                              │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       │ implements                        │
│        ┌──────────────┼──────────────┬────────────────┐  │
│        │              │              │                │  │
│        ▼              ▼              ▼                ▼  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │  │
│  │ Customer     │ │ Product      │ │ Order        │ │  │
│  │ Repository   │ │ Repository   │ │ Repository   │ │  │
│  ├──────────────┤ ├──────────────┤ ├──────────────┤ │  │
│  │ - dbContext  │ │ - dbContext  │ │ - dbContext  │ │  │
│  │ - cache      │ │ - cache      │ │ - cache      │ │  │
│  ├──────────────┤ ├──────────────┤ ├──────────────┤ │  │
│  │ + getByEmail │ │ + findByName │ │ + findByDate │ │  │
│  │ + getByPhone │ │ + findByCatg │ │ + findByUser │ │  │
│  │ + search()   │ │ + inStock()  │ │ + findByStatus │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ │  │
│        │              │              │                │  │
│        └──────────────┴──────────────┴────────────────┘  │
│                       │                                  │
│             Uses (Dependency Injection)                 │
│                       │                                  │
│  ┌────────────────────▼──────────────────────────────┐  │
│  │           DatabaseContext                         │  │
│  ├──────────────────────────────────────────────────┤  │
│  │ - connectionString: string                        │  │
│  │ - customers: DbSet<Customer>                      │  │
│  │ - products: DbSet<Product>                        │  │
│  │ - orders: DbSet<Order>                            │  │
│  ├──────────────────────────────────────────────────┤  │
│  │ + saveChanges(): void                             │  │
│  │ + beginTransaction(): Transaction                 │  │
│  │ + rollback(): void                                │  │
│  │ + executeQuery(sql): DataTable                    │  │
│  └──────────────────────────────────────────────────┘  │
│        │        │        │         │                    │
│        ▼        ▼        ▼         ▼                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │  <<entities>>                                    │  │
│  │                                                  │  │
│  │  ┌──────────────┐  ┌──────────────┐             │  │
│  │  │ Customer     │  │ Product      │ ┌─────────┐ │  │
│  │  ├──────────────┤  ├──────────────┤ │ Order   │ │  │
│  │  │ + Id: int    │  │ + Id: int    │ ├─────────┤ │  │
│  │  │ + Name       │  │ + Name       │ │ + Id    │ │  │
│  │  │ + Email      │  │ + Price      │ │ + Items │ │  │
│  │  │ + Phone      │  │ + Stock      │ │ + Total │ │  │
│  │  └──────────────┘  └──────────────┘ └─────────┘ │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Key Elements
- **Generic Interface**: IRepository<T> defines contract for all repositories
- **Concrete Repositories**: Implement specific queries for each entity
- **DbContext**: Central point for database operations
- **Entity Models**: Plain data objects (POCOs/DTOs)
- **Dependency Injection**: Repositories injected into services

---

## Template 3: Service Layer with Dependency Injection

**Purpose**: Show business logic layer and how services collaborate

```
┌────────────────────────────────────────────────────────────┐
│            Service Layer Architecture                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ <<interface>>                                       │ │
│  │ IOrderService                                       │ │
│  ├─────────────────────────────────────────────────────┤ │
│  │ + createOrder(request): OrderDto                    │ │
│  │ + getOrder(id): OrderDto                            │ │
│  │ + processPayment(orderId, payment): boolean         │ │
│  │ + trackOrder(id): TrackingDto                       │ │
│  └────────────────────┬────────────────────────────────┘ │
│                       │ implements                        │
│                       │                                   │
│  ┌────────────────────▼────────────────────────────────┐ │
│  │ OrderService                                        │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ - orderRepository: IRepository<Order>              │ │
│  │ - productRepository: IRepository<Product>          │ │
│  │ - paymentService: IPaymentService                  │ │
│  │ - notificationService: INotificationService        │ │
│  │ - logger: ILogger                                  │ │
│  │                                                    │ │
│  │ Constructor (Dependency Injection):                │ │
│  │ + OrderService(orderRepo, productRepo,            │ │
│  │               paymentSvc, notificationSvc, logger) │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ + createOrder(request): OrderDto                   │ │
│  │   1. Validate request                              │ │
│  │   2. Check product availability                    │ │
│  │   3. Calculate total                               │ │
│  │   4. Create Order entity                           │ │
│  │   5. Save to repository                            │ │
│  │   6. Notify customer                               │ │
│  │   7. Return OrderDto                               │ │
│  │                                                    │ │
│  │ + processPayment(orderId, payment): boolean        │ │
│  │   1. Get order from repository                     │ │
│  │   2. Validate payment                              │ │
│  │   3. Call paymentService.charge()                  │ │
│  │   4. Update order status                           │ │
│  │   5. Save changes                                  │ │
│  │   6. Return success status                         │ │
│  │                                                    │ │
│  └──────────────────────────────────────────────────┘  │
│         ▲                    ▲                          │
│         │ uses               │ uses                     │
│         │                    │                          │
│  ┌──────┴───────────┐ ┌──────┴──────────────┐          │
│  │                  │ │                     │          │
│  ▼                  ▼ ▼                     ▼          │
│  ┌──────────────────────────┐  ┌──────────────────┐  │
│  │ <<interface>>            │  │ <<interface>>    │  │
│  │ IPaymentService          │  │ INotificationSvc │  │
│  ├──────────────────────────┤  ├──────────────────┤  │
│  │ + charge(amount): Tx     │  │ + sendEmail()    │  │
│  │ + refund(txId): boolean  │  │ + sendSMS()      │  │
│  │ + verify(): boolean      │  │ + sendPush()     │  │
│  └──────────────────────────┘  └──────────────────┘  │
│         ▲                              ▲              │
│         │ implements                   │ implements  │
│         │                              │              │
│  ┌──────┴──────────────┐      ┌────────┴────────────┐ │
│  │                     │      │                     │ │
│  ▼                     ▼      ▼                     ▼ │
│  ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
│  │ StripePayment  │ │ PayPalPayment│ │NotificationHub │
│  │ Service        │ │ Service      │ │ Service        │
│  ├────────────────┤ ├──────────────┤ ├────────────────┤
│  │ - apiKey       │ │ - clientId   │ │ - smtpClient   │
│  │ - apiSecret    │ │ - secret     │ │ - twilioClient │
│  ├────────────────┤ ├──────────────┤ ├────────────────┤
│  │ + charge()     │ │ + charge()   │ │ + sendEmail()  │
│  │ + refund()     │ │ + refund()   │ │ + sendSMS()    │
│  │ + verify()     │ │ + verify()   │ │ + sendPush()   │
│  └────────────────┘ └──────────────┘ └────────────────┘
│
└────────────────────────────────────────────────────────────┘

Dependency Injection Container:
┌─────────────────────────────────────┐
│ services.Register<IOrderService,    │
│        new OrderService(             │
│          orderRepository,            │
│          productRepository,          │
│          new StripePaymentService(), │
│          new NotificationHub(),      │
│          logger)                     │
└─────────────────────────────────────┘
```

### Key Patterns
- **Dependency Injection**: Dependencies passed via constructor
- **Interface Segregation**: Small, focused interfaces
- **Strategy Pattern**: Multiple payment/notification implementations
- **Single Responsibility**: Each service has one reason to change
- **Loose Coupling**: Services depend on abstractions, not concrete classes

---

## Template 4: State Machine Pattern (Order Workflow)

**Purpose**: Show allowed state transitions in a workflow

```
┌────────────────────────────────────────────────────┐
│     Order State Machine (Workflow)                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ┌──────────────────────────┐                    │
│  │                          │                    │
│  ▼                          │                    │
│  ┌─────────────┐            │                    │
│  │   DRAFT     │◄───────────┼──── cancel()      │
│  │ (Initial)   │            │                    │
│  └──────┬──────┘            │                    │
│         │                   │                    │
│         │ submit()          │                    │
│         ▼                   │                    │
│  ┌──────────────────┐       │                    │
│  │   PENDING        │       │                    │
│  │ (Awaiting        │       │                    │
│  │  payment)        │       │                    │
│  └──────┬───┬──────┘       │                    │
│         │   │              │                    │
│    pay()│   │abandon()     │                    │
│         │   │              │                    │
│         ▼   ▼              │                    │
│  ┌──────────────────┐  ┌───┴──────────────┐   │
│  │   CONFIRMED      │  │   CANCELLED      │   │
│  │ (Payment         │  │ (Order rejected) │   │
│  │  received)       │  └──────────────────┘   │
│  └──────┬───┬──────┘                          │
│         │   │                                 │
│    ship()   │ refund()                        │
│         │   │                                 │
│         ▼   ▼                                 │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │   SHIPPED        │  │   REFUNDED       │  │
│  │ (In transit)     │  │ (Payment back)   │  │
│  └──────┬───┬──────┘  └──────────────────┘  │
│         │   │                                │
│  deliver() │ return()                        │
│         │   │                                │
│         ▼   ▼                                │
│  ┌──────────────────┐  ┌──────────────────┐ │
│  │  DELIVERED       │  │   RETURNED       │ │
│  │ (Complete)       │  │ (Items back)     │ │
│  └──────────────────┘  └──────────────────┘ │
│          │                      │            │
│          └──────────┬───────────┘            │
│                     │                       │
│                     ▼                       │
│          ┌──────────────────┐               │
│          │   COMPLETED      │               │
│          │ (Final state)    │               │
│          └──────────────────┘               │
│                                             │
│  State Transitions Table:                   │
│  ┌───────────┬──────────┬─────────┐        │
│  │From State │Event     │To State │        │
│  ├───────────┼──────────┼─────────┤        │
│  │DRAFT      │submit()  │PENDING  │        │
│  │PENDING    │pay()     │CONFIRMED       │        │
│  │PENDING    │abandon() │CANCELLED       │        │
│  │CONFIRMED  │ship()    │SHIPPED │        │
│  │SHIPPED    │deliver() │DELIVERED       │        │
│  │SHIPPED    │return()  │RETURNED        │        │
│  │DELIVERED  │(timeout) │COMPLETED       │        │
│  │CANCELLED  │none      │(END)   │        │
│  │REFUNDED   │none      │(END)   │        │
│  │COMPLETED  │none      │(END)   │        │
│  └───────────┴──────────┴─────────┘        │
│                                             │
│  Rules:                                     │
│  - Only valid transitions allowed           │
│  - Invalid transitions throw exception      │
│  - Each state has allowed operations        │
│  - Events change state atomically           │
│                                             │
└────────────────────────────────────────────────┘
```

### Key Concepts
- **States**: Discrete conditions an order can be in
- **Events**: Actions that trigger transitions
- **Transitions**: Valid movements between states
- **Guards**: Conditions that must be met for transitions
- **Final States**: COMPLETED, CANCELLED, REFUNDED

---

## Best Practices

### Do's ✓
- Use clear class names (PascalCase for classes, camelCase for methods)
- Show attributes with types and visibility (+, -, #)
- Include method signatures with parameters and return types
- Show relationships with appropriate symbols (→, -|>, ◇)
- Group related classes together
- Use inheritance for shared behavior
- Show cardinality on associations (0..1, 1..*,etc.)
- Include <<interface>>, <<abstract>>, <<enum>> stereotypes

### Don'ts ✗
- Overcomplicate with implementation details
- Show private methods unless they're important
- Mix design and structural concerns
- Use ambiguous class names
- Create too many classes on one diagram (max 8-10)
- Forget to label relationships
- Show every method (focus on public API)
- Make diagram too wide (hard to read)

---

## Tips for Effective Class Diagrams

1. **Identify Key Classes**: Focus on domain entities first
2. **Show Relationships**: Association, inheritance, composition, aggregation
3. **Keep It Focused**: One diagram per bounded context
4. **Use Stereotypes**: Clearly mark interfaces, abstract classes, enums
5. **Include Cardinality**: Show how many of each type exist
6. **Method Signatures**: Include parameters and return types
7. **Organize Layout**: Group related classes, minimize line crossings

---

**Template Version**: 1.0
**Best for**: Domain modeling, object-oriented design, API contracts, code structure documentation
