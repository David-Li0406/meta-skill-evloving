# Design Patterns Reference

Quick reference for design patterns with decision guidance.

## Pattern Selection Decision Trees

### Creational Patterns

```
Q: How should objects be created?
    │
    ├─ "Complex object with many parameters" ──────────────────────────────────┐
    │   → Builder Pattern                                                      │
    │   Example: QueryBuilder, RequestBuilder                                  │
    │
    ├─ "Object family that varies" ────────────────────────────────────────────┐
    │   → Abstract Factory                                                     │
    │   Example: UI toolkit (Windows/Mac components)                           │
    │
    ├─ "Single creation point, type varies" ───────────────────────────────────┐
    │   → Factory Method                                                       │
    │   Example: PaymentProcessor factory                                      │
    │
    ├─ "Expensive object, reuse instances" ────────────────────────────────────┐
    │   → Prototype (clone)                                                    │
    │   Example: Game object spawning                                          │
    │
    └─ "Only one instance ever" ───────────────────────────────────────────────┐
        → Singleton (use sparingly)                                            │
        Example: Configuration, Logger                                         │
```

### Structural Patterns

```
Q: How should objects be composed?
    │
    ├─ "Incompatible interface" ───────────────────────────────────────────────┐
    │   → Adapter                                                              │
    │   Example: Legacy API wrapper                                            │
    │
    ├─ "Multiple implementations, multiple abstractions" ──────────────────────┐
    │   → Bridge                                                               │
    │   Example: Notification (Email/SMS) × (Urgent/Normal)                    │
    │
    ├─ "Tree structure, uniform treatment" ────────────────────────────────────┐
    │   → Composite                                                            │
    │   Example: File system (files + folders)                                 │
    │
    ├─ "Add behavior dynamically" ─────────────────────────────────────────────┐
    │   → Decorator                                                            │
    │   Example: Middleware, stream wrappers                                   │
    │
    ├─ "Simplify complex subsystem" ───────────────────────────────────────────┐
    │   → Facade                                                               │
    │   Example: Payment service (hides card, fraud, ledger)                   │
    │
    ├─ "Many similar objects, share state" ────────────────────────────────────┐
    │   → Flyweight                                                            │
    │   Example: Character rendering in text editor                            │
    │
    └─ "Control access to object" ─────────────────────────────────────────────┐
        → Proxy                                                                │
        Example: Lazy loading, access control, caching                         │
```

### Behavioral Patterns

```
Q: How should objects communicate?
    │
    ├─ "Vary algorithm at runtime" ────────────────────────────────────────────┐
    │   → Strategy                                                             │
    │   Example: Sorting, payment methods, discount calculations               │
    │
    ├─ "Notify multiple objects of changes" ───────────────────────────────────┐
    │   → Observer                                                             │
    │   Example: Event system, pub/sub                                         │
    │
    ├─ "Encapsulate request as object" ────────────────────────────────────────┐
    │   → Command                                                              │
    │   Example: Undo/redo, job queues                                         │
    │
    ├─ "Object behavior changes with state" ───────────────────────────────────┐
    │   → State                                                                │
    │   Example: Order status, media player                                    │
    │
    ├─ "Pass request along chain" ─────────────────────────────────────────────┐
    │   → Chain of Responsibility                                              │
    │   Example: Middleware, validation chain                                  │
    │
    ├─ "Define skeleton, defer steps" ─────────────────────────────────────────┐
    │   → Template Method                                                      │
    │   Example: Test framework lifecycle                                      │
    │
    └─ "Traverse collection uniformly" ────────────────────────────────────────┐
        → Iterator                                                             │
        Example: Database cursors, pagination                                  │
```

---

## Architectural Patterns

### Layered Architecture

```
┌─────────────────────────────────┐
│      Presentation Layer         │  Controllers, Views
├─────────────────────────────────┤
│      Application Layer          │  Use Cases, Services
├─────────────────────────────────┤
│        Domain Layer             │  Entities, Business Logic
├─────────────────────────────────┤
│     Infrastructure Layer        │  DB, External APIs, Cache
└─────────────────────────────────┘

When to use:
- Traditional web applications
- Clear separation of concerns needed
- Team familiarity

Dependencies: Top → Bottom only
```

### Clean Architecture

```
                  ┌──────────────────────┐
                  │   External Systems   │  DB, UI, Web, Devices
                  ├──────────────────────┤
                  │  Interface Adapters  │  Controllers, Gateways, Presenters
                  ├──────────────────────┤
                  │    Use Cases         │  Application-specific rules
                  ├──────────────────────┤
                  │     Entities         │  Business objects, domain rules
                  └──────────────────────┘

When to use:
- Long-lived applications
- Complex business logic
- Testability is priority

Dependencies: Outer → Inner only (Dependency Inversion)
```

### Hexagonal Architecture (Ports & Adapters)

```
                    ┌─────────────┐
       ┌────────────┤   Adapter   ├────────────┐
       │            └──────┬──────┘            │
       │                   │                   │
   ┌───┴───┐          ┌────┴────┐         ┌───┴───┐
   │ Port  │          │  Core   │         │ Port  │
   │ (in)  │◄────────►│ Domain  │◄───────►│ (out) │
   └───┬───┘          └────┬────┘         └───┬───┘
       │                   │                   │
       │            ┌──────┴──────┐            │
       └────────────┤   Adapter   ├────────────┘
                    └─────────────┘

When to use:
- Multiple entry points (REST, GraphQL, CLI)
- Multiple data sources
- Heavy testing requirements

Ports: Interfaces defining how to interact with core
Adapters: Implementations of ports (e.g., PostgresAdapter)
```

---

## Distributed System Patterns

### Circuit Breaker

```
States:
┌────────┐         failure threshold        ┌────────┐
│ CLOSED │ ────────────────────────────────►│  OPEN  │
└────────┘                                  └────────┘
    ▲                                           │
    │                                           │ timeout
    │              ┌───────────┐                │
    └──────────────┤ HALF-OPEN │◄───────────────┘
       success     └───────────┘

Implementation:
- CLOSED: Normal operation, count failures
- OPEN: Reject calls immediately, return fallback
- HALF-OPEN: Allow limited calls to test recovery
```

### Saga Pattern

```
Orchestration (centralized):
┌───────────────┐
│  Orchestrator │
└───────┬───────┘
        │
   ┌────┴────┬────────┬────────┐
   ▼         ▼        ▼        ▼
Service A  Service B  Service C  ...
   │         │        │
   └─────────┴────────┴──── Compensating transactions on failure

Choreography (event-driven):
Service A ──event──► Service B ──event──► Service C
    ◄──compensation──    ◄──compensation──

When to use:
- Distributed transactions across services
- Need eventual consistency
- Long-running business processes
```

### CQRS (Command Query Responsibility Segregation)

```
              Commands (write)
                   │
                   ▼
            ┌─────────────┐
            │   Write     │
            │   Model     │────► Write Database
            └─────────────┘           │
                                      │ Events
                                      ▼
            ┌─────────────┐    Read Database
            │   Read      │◄──────────┘
            │   Model     │
            └─────────────┘
                   │
                   ▼
              Queries (read)

When to use:
- Read/write patterns differ significantly
- Need to scale reads/writes independently
- Complex querying requirements
- Event sourcing
```

### Event Sourcing

```
Instead of storing current state:
┌─────────────────────────────────┐
│ Order: { status: "delivered" }  │
└─────────────────────────────────┘

Store sequence of events:
┌─────────────────────────────────┐
│ 1. OrderCreated { items: [...] }│
│ 2. PaymentReceived { amount: X }│
│ 3. OrderShipped { tracking: Y } │
│ 4. OrderDelivered { date: Z }   │
└─────────────────────────────────┘

When to use:
- Need complete audit trail
- Complex domain with time-based logic
- Need to replay/rebuild state
- Debugging historical issues
```

---

## Data Patterns

### Repository Pattern

```python
# Interface
class UserRepository:
    def find_by_id(self, id: str) -> User
    def find_by_email(self, email: str) -> User
    def save(self, user: User) -> None
    def delete(self, id: str) -> None

# Implementation
class PostgresUserRepository(UserRepository):
    def find_by_id(self, id: str) -> User:
        row = self.db.query("SELECT * FROM users WHERE id = ?", id)
        return User.from_row(row)

When to use:
- Decouple domain from data access
- Enable testing with in-memory repositories
- Abstract data source details
```

### Unit of Work

```python
class UnitOfWork:
    def __enter__(self):
        self.transaction = self.db.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.transaction.rollback()
        else:
            self.transaction.commit()

# Usage
with unit_of_work as uow:
    uow.users.save(user)
    uow.orders.save(order)
    # Commits both or rolls back both

When to use:
- Multiple repository operations in one transaction
- Ensure atomicity across aggregates
```

### Outbox Pattern

```
┌─────────────────────────────────────────────┐
│            Single Transaction               │
│  1. Update business data                    │
│  2. Insert event to outbox table            │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│     Background Worker (separate process)    │
│  1. Read unpublished events from outbox     │
│  2. Publish to message broker               │
│  3. Mark as published                       │
└─────────────────────────────────────────────┘

When to use:
- Need reliable event publishing
- At-least-once delivery guarantee
- Avoid dual-write problem (DB + message broker)
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **God Object** | Class does everything | Split by responsibility |
| **Spaghetti Code** | No clear structure | Apply layered architecture |
| **Distributed Monolith** | Microservices tightly coupled | Define clear boundaries |
| **Big Ball of Mud** | No architecture | Incremental refactoring |
| **Golden Hammer** | Same solution for everything | Choose pattern by context |
| **Premature Optimization** | Complexity without proof | Measure first, optimize later |

---

*Design Patterns Reference v1.0*
