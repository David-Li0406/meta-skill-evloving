---
id: django-coding-standards
name: "Django Coding Standards"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Coding Standards

## Overview

Django coding standards ensure consistent, maintainable code across projects. These patterns cover project structure, import conventions, service layer architecture, and view patterns that separate concerns and improve testability.

## When to Use

- Starting a new Django project
- Refactoring existing Django codebase
- Onboarding new team members to Django conventions
- Code review checklist for Django PRs
- Establishing team coding guidelines

## Key Principles

1. **Fat models, thin views** - Business logic in services, views handle HTTP only
2. **Explicit imports** - Use aliases for cross-app imports to prevent circular dependencies
3. **Separation of concerns** - Services for DB writes, utils for pure functions
4. **Type hints everywhere** - All function parameters and returns are typed
5. **Constants over magic strings** - Use TextChoices and constants.py

## Best Practices

### Project Structure

```
project/
├── config/                    # Django settings
│   ├── settings/
│   │   ├── base.py           # Common settings
│   │   ├── development.py    # Dev overrides
│   │   └── production.py     # Prod overrides
│   ├── urls.py
│   └── celery.py
├── apps/                      # Domain applications
│   ├── users/
│   ├── orders/
│   └── catalog/
├── core/                      # Shared code
│   ├── models.py             # BaseModel
│   └── exceptions.py
└── tests/
    └── conftest.py
```

### Import Conventions

```python
# Cross-app imports - ALWAYS use alias
from apps.orders import models as order_models
from apps.users import services as user_services
from apps.catalog import constants as catalog_constants

# Own app imports (relative)
from .models import User
from . import constants
from .services import create_user

# Standard library
import uuid
from datetime import datetime
from typing import Optional

# Third-party
from django.db import models
from rest_framework import status
```

### Service Layer Pattern

```python
# services/user_activation.py
from django.db import transaction
from apps.users.models import User
from apps.items.models import Item


def activate_user_item(
    user: User,
    item_code: str,
    *,  # Keyword-only arguments after
    activated_by: User | None = None,
    send_notification: bool = True,
) -> Item:
    """
    Activate an item for a user.

    Args:
        user: The user receiving the item
        item_code: Unique code identifying the item
        activated_by: Admin who performed activation (optional)
        send_notification: Whether to send email notification

    Returns:
        The activated Item instance

    Raises:
        Item.DoesNotExist: If item with code not found
        ValidationError: If item already activated
    """
    item = Item.objects.get(code=item_code)

    if item.is_active:
        raise ValidationError("Item already activated")

    item.user = user
    item.is_active = True
    item.activated_by = activated_by
    item.activated_at = timezone.now()
    item.save(update_fields=['user', 'is_active', 'activated_by', 'activated_at', 'updated_at'])

    if send_notification:
        send_activation_email.delay(user.id, item.id)

    return item
```

### Thin Views

```python
# views/activation.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users import services
from .serializers import ItemActivationRequest, ItemResponse


class ItemActivationView(APIView):
    """Activate item for authenticated user."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Validate input
        serializer = ItemActivationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Call service (business logic)
        item = services.activate_user_item(
            user=request.user,
            item_code=serializer.validated_data['item_code'],
            activated_by=request.user if request.user.is_staff else None,
        )

        # 3. Return response
        return Response(
            ItemResponse(item).data,
            status=status.HTTP_200_OK
        )
```

### Constants Pattern

```python
# constants.py
from django.db import models


class UserType(models.TextChoices):
    REGULAR = 'regular', 'Regular User'
    PREMIUM = 'premium', 'Premium User'
    ADMIN = 'admin', 'Administrator'


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


# Limits and thresholds
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MAX_ITEMS_PER_USER = 50
ACTIVATION_CODE_LENGTH = 12
```

## Anti-patterns

### Avoid: Business Logic in Views

```python
# BAD - Logic in view
class OrderView(APIView):
    def post(self, request):
        order = Order.objects.create(user=request.user)
        order.items.set(request.data['items'])
        order.total = sum(i.price for i in order.items.all())
        order.save()
        send_email(order)  # Side effect in view
        return Response(...)
```

### Avoid: Bare Except

```python
# BAD
try:
    obj = Model.objects.get(pk=pk)
except:
    pass

# GOOD - Specific exception
try:
    obj = Model.objects.get(pk=pk)
except Model.DoesNotExist:
    raise NotFoundError(f"Object {pk} not found")
```

### Avoid: Direct Cross-App Imports

```python
# BAD - Circular import risk
from apps.orders.models import Order

# GOOD - Use alias
from apps.orders import models as order_models
order = order_models.Order.objects.get(pk=pk)
```

## References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
