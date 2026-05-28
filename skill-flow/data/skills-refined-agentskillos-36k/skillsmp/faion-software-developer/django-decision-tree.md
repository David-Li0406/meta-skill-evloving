---
id: django-decision-tree
name: "Django Code Decision Tree"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Code Decision Tree

## Overview

A decision framework for determining where to place code in Django applications. This methodology eliminates ambiguity about code organization and ensures consistent architecture across the team.

## When to Use

- Deciding where to implement new functionality
- Refactoring existing code into proper locations
- Code review to verify proper placement
- Onboarding developers to project architecture
- Architectural discussions and documentation

## Key Principles

1. **Single responsibility** - Each module has one clear purpose
2. **Dependency direction** - Views depend on services, not vice versa
3. **Testability** - Pure functions in utils, side effects in services
4. **Explicit boundaries** - Clear separation between layers
5. **Predictable location** - Any team member can find any code

## Best Practices

### Primary Decision Tree

```
What does the function do?
│
├─► Changes database (CREATE/UPDATE/DELETE)?
│   └─► services/
│
├─► Makes external API calls?
│   └─► services/ or integrations/
│
├─► Pure function (validation, calculation)?
│   └─► utils/
│
├─► Data transformation (no side effects)?
│   └─► utils/
│
├─► Handles HTTP request/response?
│   └─► views/
│
├─► Defines data structure?
│   └─► models/
│
├─► Validates request data?
│   └─► serializers/
│
├─► Background/async task?
│   └─► tasks/
│
└─► Reusable across apps?
    └─► core/ or common/
```

### Layer Responsibilities

| Layer | Responsibility | Dependencies |
|-------|----------------|--------------|
| **views/** | HTTP handling, request validation | services, serializers |
| **services/** | Business logic, DB writes, external APIs | models, utils |
| **utils/** | Pure functions, helpers, transformations | None or stdlib |
| **models/** | Data structure, DB schema | Django ORM |
| **serializers/** | Input validation, output formatting | models |
| **tasks/** | Background jobs, async processing | services |
| **integrations/** | Third-party API wrappers | utils |

### Detailed Examples

**Services - Database Operations**

```python
# services/orders.py
from django.db import transaction
from apps.orders.models import Order
from apps.inventory import services as inventory_services


@transaction.atomic
def create_order(
    user: User,
    items: list[dict],
    *,
    shipping_address: Address,
) -> Order:
    """Create order and reserve inventory."""
    order = Order.objects.create(
        user=user,
        shipping_address=shipping_address,
        status=OrderStatus.PENDING,
    )

    for item in items:
        inventory_services.reserve_stock(item['product_id'], item['quantity'])
        order.items.create(**item)

    order.calculate_total()
    return order
```

**Utils - Pure Functions**

```python
# utils/pricing.py
from decimal import Decimal


def calculate_discount(
    subtotal: Decimal,
    discount_percent: int,
    *,
    max_discount: Decimal | None = None,
) -> Decimal:
    """
    Calculate discount amount.

    Pure function - no side effects, no DB access.
    """
    discount = subtotal * Decimal(discount_percent) / 100

    if max_discount is not None:
        discount = min(discount, max_discount)

    return discount.quantize(Decimal('0.01'))


def format_currency(amount: Decimal, currency: str = 'USD') -> str:
    """Format amount as currency string."""
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£'}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"
```

**Integrations - External APIs**

```python
# integrations/stripe.py
import stripe
from django.conf import settings


class StripeClient:
    """Wrapper for Stripe API."""

    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_payment_intent(
        self,
        amount: int,
        currency: str,
        *,
        customer_id: str | None = None,
        metadata: dict | None = None,
    ) -> stripe.PaymentIntent:
        """Create Stripe payment intent."""
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            customer=customer_id,
            metadata=metadata or {},
        )

    def refund_payment(self, payment_intent_id: str) -> stripe.Refund:
        """Refund a payment."""
        return stripe.Refund.create(payment_intent=payment_intent_id)
```

### Quick Reference Table

| Code Type | Location | Example |
|-----------|----------|---------|
| Create user | `services/users.py` | `create_user()` |
| Hash password | `utils/auth.py` | `hash_password()` |
| Login endpoint | `views/auth.py` | `LoginView` |
| User model | `models/user.py` | `class User` |
| User input validation | `serializers/users.py` | `CreateUserSerializer` |
| Send email | `tasks/notifications.py` | `send_welcome_email.delay()` |
| Stripe payment | `integrations/stripe.py` | `StripeClient` |
| Date formatting | `utils/formatting.py` | `format_date()` |
| Calculate tax | `utils/pricing.py` | `calculate_tax()` |
| Process payment | `services/payments.py` | `process_payment()` |

## Anti-patterns

### Avoid: Services in Utils

```python
# BAD - utils should not access DB
# utils/users.py
def get_active_users():
    return User.objects.filter(is_active=True)

# GOOD - move to services
# services/users.py
def get_active_users() -> QuerySet[User]:
    return User.objects.filter(is_active=True)
```

### Avoid: Business Logic in Views

```python
# BAD - business logic in view
class OrderView(APIView):
    def post(self, request):
        if request.user.orders.count() > 10:
            discount = 0.1
        # ... complex logic

# GOOD - delegate to service
class OrderView(APIView):
    def post(self, request):
        order = services.create_order(request.user, request.data)
        return Response(OrderSerializer(order).data)
```

### Avoid: Circular Dependencies

```python
# BAD - circular import
# apps/orders/services.py
from apps.users.services import update_user_stats  # users imports orders

# GOOD - use signals or tasks
# apps/orders/services.py
def create_order(...):
    order = Order.objects.create(...)
    update_user_stats_task.delay(order.user_id)  # async, no import
```

## References

- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [Clean Architecture in Django](https://www.cosmicpython.com/)
- [Domain-Driven Design with Django](https://djangostars.com/blog/django-ddd/)
