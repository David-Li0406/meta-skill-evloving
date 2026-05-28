# Example Output

A completed critique for a hypothetical e-commerce codebase.

## Architectural Inventory (Phase 1 Summary)

**Project Overview**
- Language/Framework: Python 3.11 + FastAPI
- Build System: uv, Makefile
- Key Dependencies: SQLAlchemy, redis-py, stripe, httpx

**Entry Points**
| Type | Location | Count |
|------|----------|-------|
| HTTP Routes | `api/*.py` | 24 endpoints |
| Background Workers | `workers/*.py` | 3 Celery tasks |
| Cron Jobs | `tasks/daily.py` | 2 scheduled tasks |

**Services**
| Service | Location | Dependencies |
|---------|----------|--------------|
| UserService | `services/user.py` | UserRepo, EmailService |
| OrderService | `services/order.py` | OrderRepo, PaymentService, InventoryService |
| PaymentService | `services/payment.py` | Stripe client |

**Infrastructure**
| Component | Type | Access Pattern |
|-----------|------|----------------|
| PostgreSQL | Database | SQLAlchemy ORM, direct connection |
| Redis | Cache | redis-py client, no abstraction |
| Stripe | Payment API | Direct SDK calls in PaymentService |
| SendGrid | Email | httpx transport in EmailService |

**Domain Model**
| Entity | Location | Relationships |
|--------|----------|---------------|
| User | `models/user.py` | has_many Orders |
| Order | `models/order.py` | belongs_to User, has_many LineItems |
| Product | `models/product.py` | has_many LineItems |
| Cart | `models/cart.py` | belongs_to User, has_many CartItems |

**Observed Patterns**: Active Record via SQLAlchemy, service classes for orchestration, no repository layer, direct infrastructure access from services.

## Assessment (Phase 2 Summary)

**Executive Summary**

This e-commerce codebase has a solid foundation with clear service boundaries and proper separation of background jobs from request handling. The team has established reasonable conventions that have served them well.

However, the architecture shows signs of organic growth without consistent application of dependency inversion principles. Domain logic has leaked into infrastructure concerns—pricing calculations live inside ORM event hooks, and payment processing is tightly coupled to Stripe's SDK. These issues don't cause immediate pain, but they're accumulating technical debt that will slow feature development and make testing increasingly difficult.

The thesis: *This codebase handles feature organization well, but struggles with clean separation between domain logic and infrastructure dependencies.*

**What's Working Well**
- Clear feature folder organization
- Service layer exists for complex operations
- Background jobs properly separated from HTTP handlers

**Detailed Findings**

### Finding 1: Pricing Logic Embedded in ORM Events

**Category**: Boundary Violation

**The Problem**
The `Order` model contains pricing calculation logic inside SQLAlchemy event listeners. When an order is saved, the `before_flush` event recalculates totals, applies discounts, and computes tax. This mixes pure business rules with persistence mechanics.

**Why It Matters**
- Cannot unit test pricing without a database connection
- Pricing rules are invisible—hidden inside ORM events rather than explicit domain code
- Changing pricing logic requires understanding SQLAlchemy event execution order

**Evidence**
- `models/order.py:45-78` - `before_flush` listener with 30+ lines of pricing logic
- `models/order.py:82` - Tax calculation references `os.environ["TAX_RATE"]` directly

**Suggested Direction**
Extract a pure `PricingCalculator` class that takes order data and returns computed totals. Event simply calls calculator and assigns results.

---

### Finding 2: Direct Payment Provider Coupling

**Category**: Boundary Violation

**The Problem**
`CartService` directly instantiates and calls Stripe SDK methods. Payment intent creation, charge capture, and refund logic all reference Stripe-specific types and error codes.

**Why It Matters**
- Switching payment providers requires rewriting business logic
- Cannot test checkout flow without Stripe test mode
- Stripe version upgrades have unbounded blast radius

**Evidence**
- `services/cart.py:112-145` - Direct `stripe.PaymentIntent.create()` calls
- `services/cart.py:167` - Catches `stripe.error.CardError` specifically

**Suggested Direction**
Introduce `PaymentGateway` port interface. Current Stripe logic becomes `StripePaymentAdapter`.

## Roadmap (Phase 3 Summary)

**Executive Summary**

This roadmap contains 2 quick wins, 2 medium-term improvements, and 2 long-term projects. Start with the `PricingCalculator` extraction—it's the lowest-risk change with immediate testability benefits, and it establishes a pattern the team can follow for subsequent extractions.

The quick wins are independent and can be tackled in any order. Medium-term items should follow quick wins, as they build on the patterns established. Long-term items require the foundation laid by earlier work.

**Quick Wins**

### 1. Extract PricingCalculator from Order Model

**Problem**: Pricing logic buried in ORM events makes testing require database setup.
**Impact**: Enables unit testing of pricing rules; makes pricing logic explicit and auditable.

**Implementation Approach**

1. Create the pricing domain module:
   ```python
   # domain/pricing/calculator.py
   from dataclasses import dataclass
   from decimal import Decimal

   @dataclass
   class OrderLineItem:
       unit_price: Decimal
       quantity: int
       discount_percent: Decimal = Decimal("0")

   @dataclass
   class PricingResult:
       subtotal: Decimal
       discount: Decimal
       tax: Decimal
       total: Decimal

   def calculate_order_total(
       items: list[OrderLineItem],
       tax_rate: Decimal
   ) -> PricingResult:
       subtotal = sum(
           item.unit_price * item.quantity for item in items
       )
       # ... rest of logic extracted from event
   ```

2. Update the Order model event:
   ```python
   # models/order.py
   from domain.pricing.calculator import calculate_order_total

   @event.listens_for(Order, "before_flush")
   def calculate_totals(mapper, connection, order):
       result = calculate_order_total(order.line_items, config.tax_rate)
       order.subtotal = result.subtotal
       order.tax = result.tax
       order.total = result.total
   ```

**Files to Modify**
- `domain/pricing/calculator.py` (new)
- `models/order.py:45-78` (simplify event)

**Verification**
- Add unit tests for `calculate_order_total` with various scenarios
- Existing integration tests should pass unchanged

---

### 2. Create PaymentGateway Interface

**Problem**: Direct Stripe coupling prevents testing and locks in vendor.
**Impact**: Enables mock payment testing; prepares for potential provider switch.

**Implementation Approach**

1. Define the port:
   ```python
   # domain/ports/payment_gateway.py
   from typing import Protocol
   from dataclasses import dataclass
   from decimal import Decimal

   @dataclass
   class PaymentIntent:
       id: str
       client_secret: str

   @dataclass
   class PaymentResult:
       success: bool
       charge_id: str

   @dataclass
   class RefundResult:
       success: bool
       refund_id: str

   class PaymentGateway(Protocol):
       def create_payment_intent(
           self, amount: Decimal, currency: str
       ) -> PaymentIntent: ...

       def capture_payment(self, intent_id: str) -> PaymentResult: ...

       def refund(
           self, charge_id: str, amount: Decimal | None = None
       ) -> RefundResult: ...
   ```

2. Implement Stripe adapter:
   ```python
   # infrastructure/stripe_adapter.py
   import stripe
   from domain.ports.payment_gateway import (
       PaymentGateway, PaymentIntent, PaymentResult, RefundResult
   )

   class StripePaymentAdapter(PaymentGateway):
       def __init__(self, api_key: str):
           self._client = stripe
           self._client.api_key = api_key

       def create_payment_intent(
           self, amount: Decimal, currency: str
       ) -> PaymentIntent:
           intent = self._client.PaymentIntent.create(
               amount=int(amount * 100), currency=currency
           )
           return PaymentIntent(
               id=intent.id, client_secret=intent.client_secret
           )
       # ... other methods
   ```

3. Inject into CartService constructor and update calls.

**Files to Modify**
- `domain/ports/payment_gateway.py` (new)
- `infrastructure/stripe_adapter.py` (new)
- `services/cart.py:112-167` (use injected gateway)

**Medium-term**

3. Introduce repository pattern for data access
4. Implement dependency injection container

**Long-term**

5. Separate read models for reporting queries
6. Extract order fulfillment bounded context
