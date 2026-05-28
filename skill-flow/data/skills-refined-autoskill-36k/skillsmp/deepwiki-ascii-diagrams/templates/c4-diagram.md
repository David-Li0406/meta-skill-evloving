# C4 Model Diagram Templates

C4 Model diagrams show system architecture at different levels of abstraction:
- **Level 1 (System)**: High-level overview of the entire system
- **Level 2 (Container)**: Major building blocks and technologies
- **Level 3 (Component)**: Internal structure of containers
- **Level 4 (Code)**: Details of individual components

---

## Template 1: System Level (C1)

**Purpose**: Show how the system fits into the broader landscape

```
┌────────────────────────────────────────────────────────────────┐
│                      External Systems                           │
├──────────────────────────┬──────────────────────────────────────┤
│ ╔════════════════════╗   │   ╔═════════════════════════════╗   │
│ ║  Payment System    ║   │   ║  Email Service              ║   │
│ ║  (Stripe API)      ║   │   ║  (SendGrid)                 ║   │
│ ╚════════════════════╝   │   ╚═════════════════════════════╝   │
└────────────────────────────────────────────────────────────────┘
        ▲ payment      ◄──────────────── email notifications
        │
        │
┌────────────────────────────────────────────────────────────────┐
│                    E-Commerce System                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  Web Application (Frontend)                              │  │
│  │  ├─ React                                                │  │
│  │  ├─ Responsive Design                                   │  │
│  │  └─ Shopping Cart                                       │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────┘  │
│           ▲                                                    │
│           │ HTTP/HTTPS (REST API)                            │
│           ▼                                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │   Backend API Server                                     │  │
│  │   ├─ Product Management                                 │  │
│  │   ├─ Order Processing                                   │  │
│  │   └─ User Authentication                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

[This C1 diagram shows the main system and its external dependencies]
```

### Key Elements
- **Boxes**: Major systems or applications
- **Arrows**: Communication flows between systems
- **Labels**: Protocols used (HTTP, HTTPS, gRPC, etc.)
- **Double-line boxes**: External systems outside your control

---

## Template 2: Container Level (C2)

**Purpose**: Show major building blocks within a system

```
┌─────────────────────────────────────────────────────────────────┐
│                    E-Commerce System                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        Web Browser Container                             │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  React SPA                                         │  │   │
│  │  │  - Product Catalog                                │  │   │
│  │  │  - Shopping Cart                                  │  │   │
│  │  │  - Checkout Flow                                 │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│           ▲                                                       │
│           │ JSON/REST                                           │
│           ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │      API Gateway Container (Node.js/Express)            │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  Routes:                                           │  │   │
│  │  │  - GET /api/products                              │  │   │
│  │  │  - POST /api/orders                               │  │   │
│  │  │  - POST /api/auth/login                           │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│      ▲          ▲          ▲                                     │
│      │          │          │                                     │
│      ▼          ▼          ▼                                     │
│  ┌────────┐ ┌────────┐ ┌────────────────┐                       │
│  │Product │ │ Order  │ │ User Database  │                       │
│  │  DB    │ │  DB    │ │ (PostgreSQL)   │                       │
│  │(MySQL) │ │(MongoDB)│ │                │                       │
│  └────────┘ └────────┘ └────────────────┘                       │
│                                                                   │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃  Cache Layer (Redis)                                     ┃  │
│  ┃  - Session Storage                                      ┃  │
│  ┃  - Product Cache                                        ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

[Container level shows major application building blocks and data stores]
```

### Key Elements
- **Containers**: Applications, databases, caches, services
- **Different box types**: Different purposes (apps, databases, caches)
- **Communication**: Direct connections between containers
- **Responsibility**: Each container has clear purpose

---

## Template 3: Component Level (C3)

**Purpose**: Show internal structure of a container

```
┌───────────────────────────────────────────────────────────────┐
│            API Gateway Container (Node.js)                    │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Request Router                                        │  │
│  │  - Route matching                                      │  │
│  │  - Method handling                                     │  │
│  └────────┬───────────────────────────────────────────────┘  │
│           │                                                   │
│       ┌───┴────┬───────────┬──────────────┐                  │
│       │        │           │              │                  │
│       ▼        ▼           ▼              ▼                  │
│  ┌────────┐┌────────┐┌──────────┐┌────────────┐             │
│  │Product │││ Order  ││ Auth     ││ Payment    │             │
│  │Handler ││Handler ││ Handler  ││ Handler    │             │
│  └────┬───┘└───┬────┘└────┬─────┘└────┬───────┘             │
│       │        │          │           │                     │
│       └────┬───┴────┬─────┴─────┬─────┘                     │
│            │        │           │                           │
│            ▼        ▼           ▼                           │
│        ┌──────────────────────────┐                        │
│        │  Database Access Layer   │                        │
│        │  - Query builder         │                        │
│        │  - Connection pooling    │                        │
│        └──────────────────────────┘                        │
│                  ▲                                          │
│                  │ SQL/NoSQL                              │
│                  ▼                                          │
│        ┌──────────────────────────┐                        │
│        │  Data Models             │                        │
│        │  - User, Product, Order  │                        │
│        └──────────────────────────┘                        │
│                                                             │
└───────────────────────────────────────────────────────────┘

[Component view shows how the API Gateway is internally organized]
```

### Key Elements
- **Components**: Logical modules within a container
- **Responsibility**: Each component has specific role
- **Internal communication**: How components interact
- **External dependencies**: Databases, external services

---

## Template 4: Class Level (C4)

**Purpose**: Show detailed code structure (for complex components)

```
┌─────────────────────────────────────────────────────────────┐
│              Order Handler Component (Detailed)              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ OrderController                                        │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ - orders: Order[]                                      │ │
│  │ - db: Database                                         │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │ + createOrder(data): Order                            │ │
│  │ + getOrderById(id): Order                             │ │
│  │ + updateOrderStatus(id, status): void                │ │
│  └────────────────────────────────────────────────────────┘ │
│            ▲                    ▲                             │
│   uses     │                    │ depends on                 │
│            │                    │                             │
│  ┌─────────┴──────┐   ┌─────────┴─────────────────────┐     │
│  │ OrderValidator  │   │ PaymentService               │     │
│  ├─────────────────┤   ├──────────────────────────────┤     │
│  │ - rules: Rule[] │   │ - gateway: PaymentGateway    │     │
│  ├─────────────────┤   ├──────────────────────────────┤     │
│  │ + validate()    │   │ + charge(amount): Response   │     │
│  │ + checkInventory│   │ + refund(transactionId): ... │     │
│  └─────────────────┘   └──────────────────────────────┘     │
│                                                               │
└─────────────────────────────────────────────────────────────┘

[Class diagram shows the structure of components and their relationships]
```

### Key Elements
- **Classes**: Code structures (classes, types, interfaces)
- **Attributes**: Data members of the class
- **Methods**: Functions/operations available
- **Relationships**: Inheritance, composition, dependencies

---

## Tips for C4 Diagrams

### C1 Best Practices
- Include external systems and their purpose
- Show user/customer interactions
- Keep it simple and understandable to non-technical stakeholders

### C2 Best Practices
- Use container types consistently (app, database, cache)
- Show technology choices in labels
- Limit to 5-10 containers for clarity

### C3 Best Practices
- Focus on one container at a time
- Show component responsibilities
- Keep components at similar abstraction level

### C4 Best Practices
- Use for complex components only
- Show key classes and relationships
- Include method signatures for clarity

---

**Template Version**: 1.0
**Best for**: System architecture documentation, onboarding, design documentation
