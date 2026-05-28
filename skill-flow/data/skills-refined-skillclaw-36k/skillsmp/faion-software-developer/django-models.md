# Models Reference

## Base Model Pattern

```python
import uuid
from django.db import models

class BaseModel(models.Model):
    """Abstract base with UUID and timestamps."""
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Order(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self) -> str:
        return f"Order {self.uid}"
```

## ForeignKey Patterns

```python
# PROTECT - prevent deletion if related exists
user = models.ForeignKey('users.User', on_delete=models.PROTECT)

# CASCADE - delete together (use carefully!)
items = models.ForeignKey('Item', on_delete=models.CASCADE)

# SET_NULL - set to NULL on delete
last_handler = models.ForeignKey(
    'Handler',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
)
```

## Django 5.0+ Features

### Database-computed defaults

```python
from django.db.models.functions import Now, Lower

class Article(models.Model):
    created_at = models.DateTimeField(db_default=Now())
    slug = models.CharField(max_length=100, db_default=Lower('title'))
```

## Constants

Every app should have constants.py:

```python
# apps/users/constants.py

# TextChoices (recommended)
from django.db import models

class UserType(models.TextChoices):
    REGULAR = 'regular', 'Regular'
    PREMIUM = 'premium', 'Premium'
    ADMIN = 'admin', 'Administrator'

# Limits
DEFAULT_PAGE_SIZE = 20
MAX_ITEMS_PER_USER = 100
```

Usage:

```python
from apps.users import constants as user_constants

class User(BaseModel):
    user_type = models.CharField(
        max_length=20,
        choices=user_constants.UserType.choices,
        default=user_constants.UserType.REGULAR,
    )
```

## Project Structure

```
project/
├── config/                 # Project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── celery.py
├── apps/                   # Domain applications
│   ├── users/
│   ├── orders/
│   └── catalog/
├── core/                   # Shared code
│   ├── models.py
│   └── exceptions.py
└── tests/
    └── conftest.py
```

### Domain Application Structure

```
users/
├── models/
│   ├── __init__.py
│   └── user.py
├── services/
├── utils/
├── tasks/
├── admin/
├── serializers/
├── views/
├── filters/
├── migrations/
├── constants.py
├── apps.py
├── urls.py
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```
