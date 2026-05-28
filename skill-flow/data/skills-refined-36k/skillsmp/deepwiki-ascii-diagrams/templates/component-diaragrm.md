# Component Diagram Templates

Component diagrams show the organization and dependencies of software components within a container or system. They reveal internal structure, interfaces, and how components interact.

---

## Template 1: Monolithic Application Architecture

**Purpose**: Show internal structure of a single application

```
┌───────────────────────────────────────────────────────────┐
│              Web Application (Node.js)                     │
├───────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ HTTP Server (Express)                                │ │
│  │                                                      │ │
│  │  ┌─────────────────────────────────────────────┐   │ │
│  │  │ Route Handlers                              │   │ │
│  │  │ - GET /api/products                         │   │ │
│  │  │ - POST /api/orders                          │   │ │
│  │  │ - POST /api/auth/login                      │   │ │
│  │  │ - DELETE /api/cart/:id                      │   │ │
│  │  └─────────────────────────────────────────────┘   │ │
│  │           ▲          ▲            ▲                  │ │
│  │           │          │            │                  │ │
│  └───────────┼──────────┼────────────┼──────────────────┘ │
│              │          │            │                     │
│  ┌───────────┴────┐ ┌───┴─────┐ ┌──┴────────┐           │
│  │                │ │         │ │           │           │
│  ▼                ▼ ▼         ▼ ▼           ▼           │
│┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
││ Product ├──┤ Business │◄─┤  Order   │  │   Auth   │   │
││ Service │  │  Logic   │  │ Service  │  │ Service  │   │
│└────┬────┘  └──────────┘  └──────────┘  └──────────┘   │
│     │           ▲              │                        │
│     │           │              │                        │
│     └───────────┼──────────────┘                        │
│                 │                                       │
│  ┌──────────────┴───────────────────────────────────┐  │
│  │ Data Access Layer (Repository Pattern)          │  │
│  │                                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │
│  │  │ Product  │  │  Order   │  │  User    │      │  │
│  │  │Repository│  │Repository│  │Repository│      │  │
│  │  └─────┬────┘  └─────┬────┘  └─────┬────┘      │  │
│  │        │             │             │            │  │
│  └────────┼─────────────┼─────────────┼────────────┘  │
│           │             │             │               │
│           ▼             ▼             ▼               │
│  ┌────────────────────────────────────────────────┐  │
│  │ Database Connection Pool                       │  │
│  │ (MySQL/PostgreSQL)                            │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│  ┃ Utility Services                              ┃  │
│  ┃ - Logger                                      ┃  │
│  ┃ - Config Manager                             ┃  │
│  ┃ - Error Handler                              ┃  │
│  ┃ - JWT Token Manager                          ┃  │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│                                                       │
└───────────────────────────────────────────────────────┘

[Monolithic app shows services, repositories, and shared utilities]
```

---

## Template 2: Microservices Component Structure

**Purpose**: Show internal structure of microservices

```
┌──────────────────────────────────────────────────────────┐
│           Order Service (Node.js/Express)                │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ API Layer                                          │  │
│  │ ┌──────────────────────────────────────────────┐  │  │
│  │ │ Order Controller                            │  │  │
│  │ │ - POST /orders (create)                     │  │  │
│  │ │ - GET /orders/:id (retrieve)                │  │  │
│  │ │ - PATCH /orders/:id (update status)        │  │  │
│  │ │ - GET /orders (list)                        │  │  │
│  │ └──────────────────────────────────────────────┘  │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │ Business Logic Layer                             │  │
│  │ ┌──────────────────────────────────────────────┐ │  │
│  │ │ Order Service (Orchestration)               │ │  │
│  │ │ - Validate order                            │ │  │
│  │ │ - Calculate totals                          │ │  │
│  │ │ - Orchestrate payment & shipping            │ │  │
│  │ │ - Publish events                            │ │  │
│  │ └──────────────────────────────────────────────┘ │  │
│  │ ┌──────────────────────────────────────────────┐ │  │
│  │ │ Order Domain Logic                          │ │  │
│  │ │ - Order entity rules                        │ │  │
│  │ │ - State machine (pending→paid→shipped)     │ │  │
│  │ │ - Business rules validation                 │ │  │
│  │ └──────────────────────────────────────────────┘ │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │ Data Access Layer                                │  │
│  │ ┌──────────────────────────────────────────────┐ │  │
│  │ │ Order Repository                            │ │  │
│  │ │ - save(order)                               │ │  │
│  │ │ - findById(id)                              │ │  │
│  │ │ - findByStatus(status)                      │ │  │
│  │ │ - update(id, data)                          │ │  │
│  │ └──────────────────────────────────────────────┘ │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐  │
│  │ Persistence Layer                                │  │
│  │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │  │
│  │ ┃ PostgreSQL Database                        ┃ │  │
│  │ ┃ - orders table                             ┃ │  │
│  │ ┃ - order_items table                        ┃ │  │
│  │ ┃ - order_history table                      ┃ │  │
│  │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │  │
│  └──────────────────────────────────────────────────┘  │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ External Integrations                              │ │
│  │                                                     │ │
│  │  ┌──────────────┐    ┌──────────────┐             │ │
│  │  │ Event Bus    │    │ Payment API  │             │ │
│  │  │ Client       │    │ Client       │             │ │
│  │  └──────────────┘    └──────────────┘             │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                            │
└──────────────────────────────────────────────────────────┘

[Service layer shows controller-service-repository pattern]
```

---

## Template 3: React Component Structure

**Purpose**: Show component hierarchy and data flow

```
┌──────────────────────────────────────────────────────────┐
│              App Component (React)                        │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ State Management (Context/Redux)                  │  │
│  │ - products: Product[]                             │  │
│  │ - cart: CartItem[]                                │  │
│  │ - user: User | null                               │  │
│  │ - filters: { category, price, material }         │  │
│  └────────────────────────────────────────────────────┘  │
│           │          │           │          │            │
│           ▼          ▼           ▼          ▼            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Page Components                                  │  │
│  │                                                  │  │
│  │  ┌────────────────┐      ┌────────────────┐    │  │
│  │  │ ProductPage    │      │ CartPage       │    │  │
│  │  │ ├─ Filters     │      │ ├─ CartList    │    │  │
│  │  │ ├─ ProductList │      │ ├─ CartSummary │    │  │
│  │  │ └─ ProductCard │      │ └─ Checkout    │    │  │
│  │  └────────────────┘      └────────────────┘    │  │
│  │                                                  │  │
│  │  ┌────────────────┐      ┌────────────────┐    │  │
│  │  │ LoginPage      │      │ ProfilePage    │    │  │
│  │  │ ├─ LoginForm   │      │ ├─ UserInfo    │    │  │
│  │  │ └─ SignupForm  │      │ └─ OrderHistory│    │  │
│  │  └────────────────┘      └────────────────┘    │  │
│  └──────────────────────────────────────────────────┘  │
│           │          │          │           │          │
│           ▼          ▼          ▼           ▼          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Reusable Components                              │  │
│  │                                                  │  │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │ │ Button   │ │ Modal    │ │ Loading  │         │  │
│  │ │ Component│ │ Component│ │ Spinner  │         │  │
│  │ └──────────┘ └──────────┘ └──────────┘         │  │
│  └──────────────────────────────────────────────────┘  │
│           │          │          │                      │
│  ┌────────┴──────────┴──────────┴──────────────────┐  │
│  │ Utility Hooks & Services                        │  │
│  │                                                  │  │
│  │ ┌──────────────┐    ┌─────────────────────┐    │  │
│  │ │ Hooks        │    │ API Services        │    │  │
│  │ │ - useCart()  │    │ - fetchProducts()   │    │  │
│  │ │ - useUser()  │    │ - createOrder()     │    │  │
│  │ │ - useFilters()│   │ - loginUser()       │    │  │
│  │ └──────────────┘    └─────────────────────┘    │  │
│  └──────────────────────────────────────────────────┘  │
│                                                        │
└──────────────────────────────────────────────────────┘

[React hierarchy shows page components, reusable components, and hooks]
```

---

## Template 4: Data Processing Pipeline

**Purpose**: Show components in a data transformation pipeline

```
┌──────────────────────────────────────────────────────────┐
│              Data Processing Pipeline                     │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Data Source                                         │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Raw Data Input                               │  │ │
│  │ │ - CSV files                                  │  │ │
│  │ │ - Database records                           │  │ │
│  │ │ - API responses                              │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │                                          │
│  ┌─────────────▼───────────────────────────────────────┐ │
│  │ Data Extraction                                     │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Parser Component                             │  │ │
│  │ │ - Parse CSV/JSON                             │  │ │
│  │ │ - Extract fields                             │  │ │
│  │ │ - Handle encoding                            │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │                                          │
│  ┌─────────────▼───────────────────────────────────────┐ │
│  │ Data Validation                                     │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Validator Component                          │  │ │
│  │ │ - Type checking                              │  │ │
│  │ │ - Range validation                           │  │ │
│  │ │ - Required fields check                      │  │ │
│  │ │ - Reject invalid rows                        │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │                                          │
│  ┌─────────────▼───────────────────────────────────────┐ │
│  │ Data Transformation                                │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Transformer Component                        │  │ │
│  │ │ - Normalize values                           │  │ │
│  │ │ - Calculate derived fields                   │  │ │
│  │ │ - Join related data                          │  │ │
│  │ │ - Enrich with external data                  │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │                                          │
│  ┌─────────────▼───────────────────────────────────────┐ │
│  │ Data Aggregation                                    │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Aggregator Component                         │  │ │
│  │ │ - Group by category                          │  │ │
│  │ │ - Calculate statistics                       │  │ │
│  │ │ - Create summaries                           │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └─────────────┬───────────────────────────────────────┘ │
│                │                                          │
│  ┌─────────────▼───────────────────────────────────────┐ │
│  │ Data Output                                         │ │
│  │ ┌───────────────────────────────────────────────┐  │ │
│  │ │ Writer Component                             │  │ │
│  │ │ - Write to database                          │  │ │
│  │ │ - Export to files                            │  │ │
│  │ │ - Publish events                             │  │ │
│  │ └───────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Error Handling & Logging                            │ │
│  │ - Log failed records                                │ │
│  │ - Track processing metrics                          │ │
│  │ - Alert on anomalies                                │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
└──────────────────────────────────────────────────────────┘

[Pipeline shows sequential processing with validation and error handling]
```

---

## Template 5: Backend API Component Structure

**Purpose**: Show how components handle API requests

```
┌──────────────────────────────────────────────────────────┐
│            API Backend (FastAPI/Express)                 │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ HTTP Server / Framework                          │   │
│  └──────────────────────────────────────────────────┘   │
│           │              │              │               │
│           ▼              ▼              ▼               │
│  ┌──────────────┐  ┌──────────────┐ ┌──────────────┐  │
│  │ Auth Handler │  │ Validation   │ │ Error        │  │
│  │              │  │ Middleware   │ │ Handler      │  │
│  │ - JWT Verify │  │              │ │              │  │
│  │ - Authorize  │  │ - Schema val │ │ - Exception  │  │
│  │              │  │ - Rules check│ │ - Format err │  │
│  └──────────────┘  └──────────────┘ └──────────────┘  │
│           ▲              ▲              ▲               │
│           │              │              │               │
│  ┌────────┴──────────────┴──────────────┴────────────┐ │
│  │          Router & Controller Layer                 │ │
│  │                                                   │ │
│  │  ┌───────────┐  ┌───────────┐  ┌────────────┐   │ │
│  │  │ GET       │  │ POST      │  │ PATCH/DEL  │   │ │
│  │  │ Handlers  │  │ Handlers  │  │ Handlers   │   │ │
│  │  └─────┬─────┘  └─────┬─────┘  └────┬───────┘   │ │
│  └────────┼───────────────┼─────────────┼──────────┘ │
│           │               │             │            │
│  ┌────────▼───────────────▼─────────────▼──────────┐ │
│  │         Service Layer (Business Logic)          │ │
│  │                                                 │ │
│  │  ┌──────────────────────────────────────────┐  │ │
│  │  │ Service Classes                          │  │ │
│  │  │ - Process requests                       │  │ │
│  │  │ - Implement business rules               │  │ │
│  │  │ - Orchestrate database queries           │  │ │
│  │  │ - Manage transactions                    │  │ │
│  │  └──────────────────────────────────────────┘  │ │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │         Repository/Data Access Layer         │  │
│  │                                              │  │
│  │  ┌──────────────────────────────────────┐   │  │
│  │  │ Query Builders                       │   │  │
│  │  │ - Build SQL/NoSQL queries            │   │  │
│  │  │ - Handle parameterization            │   │  │
│  │  │ - Manage connections                 │   │  │
│  │  └──────────────────────────────────────┘   │  │
│  └──────────────┬───────────────────────────────┘  │
│                 │                                   │
│  ┌──────────────▼───────────────────────────────┐  │
│  │         Database Connection Pool             │  │
│  │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │  │
│  │ ┃ PostgreSQL / MySQL                     ┃ │  │
│  │ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
└──────────────────────────────────────────────────┘

[API components show middleware, handlers, services, and data access]
```

---

## Design Patterns for Components

### Layered Architecture
```
┌──────────────────┐
│ Presentation     │ (UI, Controllers)
├──────────────────┤
│ Business Logic   │ (Services, Handlers)
├──────────────────┤
│ Data Access      │ (Repositories, Queries)
├──────────────────┤
│ Persistence      │ (Database)
└──────────────────┘
```

### Model-View-Controller
```
┌──────┐      ┌──────┐      ┌──────┐
│Model │◄────►│View  │◄────►│Controller│
└──────┘      └──────┘      └──────┘
```

### Service Locator Pattern
```
┌──────────────────────────┐
│ Service Container        │
│ - Service Registry       │
│ - Dependency Injection   │
└──────────────────────────┘
```

---

## Best Practices

### Do's ✓
- Show clear component boundaries
- Include responsibilities for each component
- Show dependencies between components
- Use consistent naming conventions
- Group related components together
- Show external dependencies

### Don'ts ✗
- Create too many small components
- Show implementation details
- Cross arrows without reason
- Use unclear naming
- Mix abstraction levels
- Forget to label connections

---

**Template Version**: 1.0
**Best for**: Architecture documentation, component design, integration guides, code organization
