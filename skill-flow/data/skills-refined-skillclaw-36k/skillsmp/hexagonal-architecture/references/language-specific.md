# Language-Specific Implementation Notes

## Python

### Port Definitions

**Protocol classes (structural typing, Python 3.8+):**

```python
from typing import Protocol, Optional

class OrderRepository(Protocol):
    def find_by_id(self, order_id: OrderId) -> Optional[Order]: ...
    def save(self, order: Order) -> None: ...
```

Protocols enable structural typing—any class with matching methods satisfies the protocol without explicit inheritance. Useful when you don't control the implementing class.

**ABC (nominal typing):**

```python
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        ...
    
    @abstractmethod
    def save(self, order: Order) -> None:
        ...
```

ABCs require explicit inheritance. Prefer when you want compile-time enforcement and clearer intent.

**Recommendation:** Use ABC for ports you define and control. Use Protocol when adapting third-party code or when structural typing aids testing.

### Dependency Injection

**Manual injection (simple projects):**

```python
# config/dependencies.py
def create_place_order_use_case(settings: Settings) -> PlaceOrderUseCase:
    session = create_session(settings.database_url)
    return PlaceOrderUseCase(
        order_repository=PostgresOrderRepository(session),
        payment_gateway=StripePaymentAdapter(settings.stripe_key),
        clock=SystemClock(),
    )
```

**Container-based (larger projects):**

```python
# Using dependency-injector
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    db_session = providers.Singleton(
        create_session,
        url=config.database_url,
    )
    
    order_repository = providers.Factory(
        PostgresOrderRepository,
        session=db_session,
    )
    
    place_order_use_case = providers.Factory(
        PlaceOrderUseCase,
        order_repository=order_repository,
        payment_gateway=providers.Factory(StripePaymentAdapter, api_key=config.stripe_key),
        clock=providers.Singleton(SystemClock),
    )
```

### Value Objects

```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True, slots=True)
class Money:
    amount: int  # Store as cents to avoid float issues
    currency: str = "GBP"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money cannot be negative")
    
    def __add__(self, other: Self) -> Self:
        if self.currency != other.currency:
            raise CurrencyMismatchError(self.currency, other.currency)
        return Money(self.amount + other.amount, self.currency)
    
    @classmethod
    def pounds(cls, pounds: int, pence: int = 0) -> Self:
        return cls(pounds * 100 + pence, "GBP")
```

### Project Structure

```
src/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── order.py
│   │   └── customer.py
│   ├── services/
│   │   └── pricing.py
│   └── ports/
│       ├── __init__.py
│       └── repositories.py
├── application/
│   ├── __init__.py
│   └── use_cases/
│       └── place_order.py
├── adapters/
│   ├── __init__.py
│   ├── inbound/
│   │   └── http/
│   │       └── orders.py
│   └── outbound/
│       └── persistence/
│           └── postgres.py
└── config/
    ├── __init__.py
    └── dependencies.py
```

## TypeScript

### Port Definitions

```typescript
// domain/ports/order-repository.ts
export interface OrderRepository {
  findById(orderId: OrderId): Promise<Order | null>;
  save(order: Order): Promise<void>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
}

// With branded types for type safety
declare const brand: unique symbol;
type Brand<T, B> = T & { [brand]: B };

export type OrderId = Brand<string, 'OrderId'>;
export type CustomerId = Brand<string, 'CustomerId'>;

export function orderId(value: string): OrderId {
  return value as OrderId;
}
```

### Dependency Injection

**Constructor injection (simple):**

```typescript
// application/use-cases/place-order.ts
export class PlaceOrderUseCase {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly paymentGateway: PaymentGateway,
    private readonly clock: Clock,
  ) {}

  async execute(command: PlaceOrderCommand): Promise<PlaceOrderResult> {
    // ...
  }
}
```

**With tsyringe (container-based):**

```typescript
import { injectable, inject } from 'tsyringe';

@injectable()
export class PlaceOrderUseCase {
  constructor(
    @inject('OrderRepository') private orderRepository: OrderRepository,
    @inject('PaymentGateway') private paymentGateway: PaymentGateway,
    @inject('Clock') private clock: Clock,
  ) {}
}

// Registration
container.register('OrderRepository', { useClass: PostgresOrderRepository });
container.register('Clock', { useValue: new SystemClock() });
```

### Value Objects

```typescript
// domain/model/money.ts
export class Money {
  private constructor(
    readonly amountCents: number,
    readonly currency: Currency,
  ) {
    if (amountCents < 0) {
      throw new Error('Money cannot be negative');
    }
  }

  static of(amountCents: number, currency: Currency = 'GBP'): Money {
    return new Money(amountCents, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new CurrencyMismatchError(this.currency, other.currency);
    }
    return Money.of(this.amountCents + other.amountCents, this.currency);
  }

  equals(other: Money): boolean {
    return this.amountCents === other.amountCents && this.currency === other.currency;
  }
}
```

## Go

### Port Definitions

Go interfaces are implicitly satisfied—no explicit `implements` declaration needed.

```go
// domain/ports/repository.go
package ports

type OrderRepository interface {
    FindByID(ctx context.Context, id OrderID) (*Order, error)
    Save(ctx context.Context, order *Order) error
    FindByCustomer(ctx context.Context, customerID CustomerID) ([]*Order, error)
}

type Clock interface {
    Now() time.Time
}
```

### Dependency Injection

Go typically uses constructor functions with explicit dependencies:

```go
// application/place_order.go
package application

type PlaceOrderUseCase struct {
    orders   ports.OrderRepository
    payments ports.PaymentGateway
    clock    ports.Clock
}

func NewPlaceOrderUseCase(
    orders ports.OrderRepository,
    payments ports.PaymentGateway,
    clock ports.Clock,
) *PlaceOrderUseCase {
    return &PlaceOrderUseCase{
        orders:   orders,
        payments: payments,
        clock:    clock,
    }
}

func (uc *PlaceOrderUseCase) Execute(ctx context.Context, cmd PlaceOrderCommand) (*PlaceOrderResult, error) {
    // ...
}
```

**Wire composition root:**

```go
// cmd/server/wire.go
//go:build wireinject

package main

func InitializeServer(cfg *config.Config) (*Server, error) {
    wire.Build(
        config.NewDB,
        postgres.NewOrderRepository,
        stripe.NewPaymentAdapter,
        infrastructure.NewSystemClock,
        application.NewPlaceOrderUseCase,
        http.NewOrderHandler,
        NewServer,
    )
    return nil, nil
}
```

### Package Organisation

```
/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   │   ├── order.go
│   │   ├── customer.go
│   │   └── money.go
│   ├── ports/
│   │   ├── repository.go
│   │   └── payment.go
│   ├── application/
│   │   └── place_order.go
│   └── adapters/
│       ├── postgres/
│       │   └── order_repository.go
│       ├── stripe/
│       │   └── payment_adapter.go
│       └── http/
│           └── orders.go
└── pkg/  # Shared utilities (if any)
```

## Rust

### Port Definitions

Use traits for ports:

```rust
// domain/ports/repository.rs
use async_trait::async_trait;

#[async_trait]
pub trait OrderRepository: Send + Sync {
    async fn find_by_id(&self, id: &OrderId) -> Result<Option<Order>, RepositoryError>;
    async fn save(&self, order: &Order) -> Result<(), RepositoryError>;
}

#[async_trait]
pub trait Clock: Send + Sync {
    fn now(&self) -> DateTime<Utc>;
}
```

### Dependency Injection

Rust typically uses generics or trait objects:

**Generics (zero-cost, monomorphised):**

```rust
pub struct PlaceOrderUseCase<R, P, C>
where
    R: OrderRepository,
    P: PaymentGateway,
    C: Clock,
{
    orders: R,
    payments: P,
    clock: C,
}

impl<R, P, C> PlaceOrderUseCase<R, P, C>
where
    R: OrderRepository,
    P: PaymentGateway,
    C: Clock,
{
    pub fn new(orders: R, payments: P, clock: C) -> Self {
        Self { orders, payments, clock }
    }

    pub async fn execute(&self, command: PlaceOrderCommand) -> Result<PlaceOrderResult, UseCaseError> {
        // ...
    }
}
```

**Trait objects (dynamic dispatch, simpler signatures):**

```rust
pub struct PlaceOrderUseCase {
    orders: Arc<dyn OrderRepository>,
    payments: Arc<dyn PaymentGateway>,
    clock: Arc<dyn Clock>,
}
```

### Value Objects

```rust
// domain/model/money.rs
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Money {
    amount_cents: i64,
    currency: Currency,
}

impl Money {
    pub fn new(amount_cents: i64, currency: Currency) -> Result<Self, MoneyError> {
        if amount_cents < 0 {
            return Err(MoneyError::NegativeAmount);
        }
        Ok(Self { amount_cents, currency })
    }

    pub fn add(&self, other: &Money) -> Result<Money, MoneyError> {
        if self.currency != other.currency {
            return Err(MoneyError::CurrencyMismatch);
        }
        Money::new(self.amount_cents + other.amount_cents, self.currency)
    }
}
```

### Module Organisation

```
src/
├── main.rs
├── lib.rs
├── domain/
│   ├── mod.rs
│   ├── model/
│   │   ├── mod.rs
│   │   ├── order.rs
│   │   └── money.rs
│   ├── services/
│   │   └── pricing.rs
│   └── ports/
│       ├── mod.rs
│       └── repository.rs
├── application/
│   ├── mod.rs
│   └── place_order.rs
├── adapters/
│   ├── mod.rs
│   ├── postgres/
│   │   └── order_repository.rs
│   └── http/
│       └── orders.rs
└── config/
    └── mod.rs
```
