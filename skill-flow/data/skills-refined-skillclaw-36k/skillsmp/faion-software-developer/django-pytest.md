---
id: django-pytest
name: "Django Testing with pytest"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Django Testing with pytest

## Overview

pytest is the preferred testing framework for Django projects, offering powerful fixtures, parametrization, and a cleaner syntax than Django's built-in TestCase. This methodology covers test organization, fixtures, mocking, and integration testing patterns.

## When to Use

- Writing unit tests for services and utils
- Integration testing API endpoints
- Testing models and database operations
- Mocking external services
- Setting up test data factories

## Key Principles

1. **Arrange-Act-Assert** - Clear test structure
2. **One assertion per test** - Focused, debuggable tests
3. **Factory pattern** - Flexible test data creation
4. **Fixtures for setup** - Reusable test configuration
5. **Test behavior, not implementation** - Tests survive refactoring

## Best Practices

### Project Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]
```

### Test Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── factories.py             # Model factories
├── unit/
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_views.py
└── fixtures/
    ├── users.py
    └── orders.py
```

### Shared Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client() -> APIClient:
    """DRF API test client."""
    return APIClient()


@pytest.fixture
def user(db) -> User:
    """Create a basic test user."""
    return User.objects.create(
        email="test@example.com",
        name="Test User",
    )


@pytest.fixture
def admin_user(db) -> User:
    """Create an admin user."""
    return User.objects.create(
        email="admin@example.com",
        name="Admin User",
        user_type="admin",
        is_staff=True,
    )


@pytest.fixture
def authenticated_client(api_client, user) -> APIClient:
    """API client with authenticated user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user) -> APIClient:
    """API client with admin user."""
    api_client.force_authenticate(user=admin_user)
    return api_client
```

### Factory Pattern

```python
# tests/factories.py
import pytest
from faker import Faker
from apps.users.models import User
from apps.orders.models import Order

fake = Faker()


@pytest.fixture
def user_factory(db):
    """Factory for creating users with custom attributes."""
    def create_user(
        email: str | None = None,
        name: str | None = None,
        user_type: str = "regular",
        **kwargs,
    ) -> User:
        return User.objects.create(
            email=email or fake.email(),
            name=name or fake.name(),
            user_type=user_type,
            **kwargs,
        )
    return create_user


@pytest.fixture
def order_factory(db, user_factory):
    """Factory for creating orders."""
    def create_order(
        user: User | None = None,
        amount: Decimal | None = None,
        status: str = "pending",
        **kwargs,
    ) -> Order:
        return Order.objects.create(
            user=user or user_factory(),
            amount=amount or Decimal("99.99"),
            status=status,
            **kwargs,
        )
    return create_order
```

### Unit Testing Services

```python
# tests/unit/test_services.py
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from apps.orders import services
from apps.orders.models import Order


@pytest.mark.django_db
class TestCreateOrder:
    """Tests for order creation service."""

    def test_creates_order_with_valid_data(self, user, product):
        """Order is created with correct attributes."""
        order = services.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 2}],
        )

        assert order.user == user
        assert order.status == "pending"
        assert order.items.count() == 1

    def test_calculates_total_correctly(self, user, product):
        """Order total is sum of item prices."""
        product.price = Decimal("25.00")
        product.save()

        order = services.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 3}],
        )

        assert order.total == Decimal("75.00")

    def test_raises_error_for_insufficient_stock(self, user, product):
        """ValueError raised when stock is insufficient."""
        product.stock = 1
        product.save()

        with pytest.raises(ValueError, match="Insufficient stock"):
            services.create_order(
                user=user,
                items=[{"product_id": product.id, "quantity": 10}],
            )

    @patch("apps.orders.services.send_order_confirmation")
    def test_sends_confirmation_email(self, mock_send, user, product):
        """Confirmation email is sent after order creation."""
        order = services.create_order(
            user=user,
            items=[{"product_id": product.id, "quantity": 1}],
        )

        mock_send.delay.assert_called_once_with(order.id)
```

### Integration Testing APIs

```python
# tests/integration/test_api.py
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestUserAPI:
    """Tests for User API endpoints."""

    def test_list_users_requires_auth(self, api_client):
        """Unauthenticated request returns 401."""
        response = api_client.get("/api/v1/users/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_users_returns_users(self, authenticated_client, user_factory):
        """Authenticated request returns user list."""
        user_factory(email="user1@example.com")
        user_factory(email="user2@example.com")

        response = authenticated_client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) >= 2

    def test_create_user_with_valid_data(self, admin_client):
        """Admin can create new user."""
        response = admin_client.post("/api/v1/users/", {
            "email": "new@example.com",
            "name": "New User",
        })

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "new@example.com"

    def test_create_user_validates_email(self, admin_client):
        """Invalid email returns validation error."""
        response = admin_client.post("/api/v1/users/", {
            "email": "invalid-email",
            "name": "Test",
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_get_user_by_uid(self, authenticated_client, user):
        """Can retrieve user by UID."""
        response = authenticated_client.get(f"/api/v1/users/{user.uid}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["uid"] == str(user.uid)
```

### Parametrized Tests

```python
# tests/unit/test_validators.py
import pytest
from apps.users.validators import validate_password


class TestPasswordValidation:
    """Tests for password validation."""

    @pytest.mark.parametrize("password,expected", [
        ("ValidPass123!", True),
        ("AnotherGood1@", True),
        ("short1!", False),  # Too short
        ("nouppercase1!", False),
        ("NOLOWERCASE1!", False),
        ("NoDigits!!", False),
        ("NoSpecial123", False),
    ])
    def test_password_validation(self, password, expected):
        """Password validation with various inputs."""
        result = validate_password(password)
        assert result.is_valid == expected

    @pytest.mark.parametrize("password,error_code", [
        ("short", "too_short"),
        ("nouppercase123!", "no_uppercase"),
        ("NOLOWERCASE123!", "no_lowercase"),
        ("NoDigitsHere!!", "no_digit"),
    ])
    def test_password_error_codes(self, password, error_code):
        """Validation returns correct error codes."""
        result = validate_password(password)
        assert error_code in result.error_codes
```

### Mocking External Services

```python
# tests/unit/test_integrations.py
import pytest
from unittest.mock import patch, MagicMock
import responses

from apps.payments.services import process_payment


class TestPaymentProcessing:
    """Tests for payment service."""

    @patch("apps.payments.services.stripe")
    def test_creates_stripe_charge(self, mock_stripe, user, order):
        """Stripe charge is created with correct amount."""
        mock_stripe.Charge.create.return_value = MagicMock(id="ch_123")

        result = process_payment(order, token="tok_visa")

        mock_stripe.Charge.create.assert_called_once_with(
            amount=int(order.total * 100),
            currency="usd",
            source="tok_visa",
            metadata={"order_id": str(order.uid)},
        )

    @responses.activate
    def test_webhook_external_api(self):
        """Test external API call with responses library."""
        responses.add(
            responses.POST,
            "https://api.external.com/notify",
            json={"status": "ok"},
            status=200,
        )

        result = services.notify_external_system({"event": "order_created"})

        assert result["status"] == "ok"
        assert len(responses.calls) == 1
```

## Anti-patterns

### Avoid: Testing Implementation Details

```python
# BAD - testing internal method calls
def test_create_order_calls_private_method(self, user):
    with patch.object(services, '_validate_items') as mock:
        services.create_order(user, items=[])
        mock.assert_called_once()  # Breaks if internal refactored

# GOOD - test observable behavior
def test_create_order_validates_items(self, user):
    with pytest.raises(ValidationError):
        services.create_order(user, items=[])  # Test the outcome
```

### Avoid: Shared Mutable State

```python
# BAD - tests affect each other
class TestOrders:
    orders = []  # Shared state!

    def test_create(self):
        self.orders.append(Order())

# GOOD - use fixtures
@pytest.fixture
def orders(order_factory):
    return [order_factory() for _ in range(3)]
```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)
- [responses](https://github.com/getsentry/responses)
