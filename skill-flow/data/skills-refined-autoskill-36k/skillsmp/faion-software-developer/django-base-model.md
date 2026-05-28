---
id: django-base-model
name: "Django Base Model Pattern"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Base Model Pattern

## Overview

The Base Model pattern provides a consistent foundation for all Django models with common fields (UUID, timestamps) and behaviors. This ensures data integrity, audit trails, and consistent API responses across the application.

## When to Use

- Starting a new Django project
- Creating any new model that represents a domain entity
- Refactoring legacy models to add tracking fields
- Building APIs that expose model data
- Systems requiring audit trails

## Key Principles

1. **UUID for external references** - Never expose auto-increment IDs in APIs
2. **Automatic timestamps** - Created and updated times for all records
3. **Consistent interface** - All models have the same base fields
4. **Abstract base** - No database table for the base model itself
5. **Immutable identifiers** - UUID cannot be changed after creation

## Best Practices

### Base Model Implementation

```python
# core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model with UUID and timestamps.

    All domain models should inherit from this class.
    """
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.uid})"
```

### Model Implementation

```python
# apps/users/models.py
from django.db import models
from core.models import BaseModel
from apps.users import constants


class User(BaseModel):
    """User account model."""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(
        max_length=20,
        choices=constants.UserType.choices,
        default=constants.UserType.REGULAR,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type', 'is_active']),
        ]

    def __str__(self) -> str:
        return self.email
```

### ForeignKey Patterns

```python
# apps/orders/models.py
from django.db import models
from core.models import BaseModel


class Order(BaseModel):
    """Order model with proper FK patterns."""

    # PROTECT - prevent deletion if orders exist
    user = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='orders',
    )

    # CASCADE - delete items with order (careful!)
    # Only use when child has no meaning without parent

    # SET_NULL - preserve order if handler deleted
    handled_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_orders',
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices)

    class Meta:
        db_table = 'orders'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
```

### Soft Delete Extension

```python
# core/models.py
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(BaseModel):
    """Base model with soft delete support."""

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Include deleted

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete instead of hard delete."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at', 'updated_at'])

    def hard_delete(self):
        """Actually delete from database."""
        super().delete()

    def restore(self):
        """Restore soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at', 'updated_at'])

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

### Django 5.0+ Features

```python
# Using db_default for database-computed defaults
from django.db.models.functions import Now, Lower


class Article(BaseModel):
    """Article with Django 5.0 features."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_default=Lower('title'))
    published_at = models.DateTimeField(null=True, blank=True)

    # GeneratedField for computed columns
    is_published = models.GeneratedField(
        expression=models.Q(published_at__isnull=False),
        output_field=models.BooleanField(),
        db_persist=True,
    )
```

### API Serialization

```python
# serializers/users.py
from rest_framework import serializers
from apps.users.models import User


class UserResponse(serializers.ModelSerializer):
    """Response serializer - uses uid, not id."""

    class Meta:
        model = User
        fields = ['uid', 'email', 'name', 'user_type', 'created_at']
        read_only_fields = fields


# Usage in views - never expose internal ID
class UserDetailView(APIView):
    def get(self, request, uid):
        user = get_object_or_404(User, uid=uid)  # Lookup by UUID
        return Response(UserResponse(user).data)
```

## Anti-patterns

### Avoid: Exposing Auto-Increment IDs

```python
# BAD - exposes internal ID
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']  # id leaks info

# GOOD - use uid
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'email', 'name']
```

### Avoid: Missing Indexes

```python
# BAD - no index on frequently queried fields
class Order(BaseModel):
    status = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

# GOOD - add composite index
class Order(BaseModel):
    status = models.CharField(max_length=20, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'status', 'created_at']),
        ]
```

### Avoid: CASCADE Without Consideration

```python
# BAD - deleting user deletes all orders (data loss!)
user = models.ForeignKey(User, on_delete=models.CASCADE)

# GOOD - protect important data
user = models.ForeignKey(User, on_delete=models.PROTECT)
```

## References

- [Django Model Field Reference](https://docs.djangoproject.com/en/5.0/ref/models/fields/)
- [Django Model Meta Options](https://docs.djangoproject.com/en/5.0/ref/models/options/)
- [UUID Best Practices](https://www.percona.com/blog/uuids-are-popular-but-bad-for-performance/)
- [Django 5.0 Release Notes](https://docs.djangoproject.com/en/5.0/releases/5.0/)
