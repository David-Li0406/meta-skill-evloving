# Testing Reference

## pytest with model_bakery

```python
import pytest
from model_bakery import baker

from apps.inventory import models as inventory_models
from apps.inventory import services as inventory_services


@pytest.fixture
def user(db):
    """Create test user."""
    return baker.make('users.User')


@pytest.fixture
def item(db, user):
    """Create inactive item."""
    return baker.make(
        inventory_models.Item,
        user=None,
        is_active=False,
    )


@pytest.mark.django_db
def test_activate_item_success(user, item):
    """Test successful item activation."""
    result = inventory_services.activate_user_item(
        user=user,
        item_code=item.code,
    )

    assert result.is_active is True
    assert result.user == user


@pytest.mark.django_db
def test_activate_item_not_found(user):
    """Test activation with invalid code."""
    with pytest.raises(inventory_models.Item.DoesNotExist):
        inventory_services.activate_user_item(
            user=user,
            item_code='invalid-code',
        )
```

## pytest with factory_boy

```python
import factory
from factory.django import DjangoModelFactory

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    is_active = True


# Usage
@pytest.mark.django_db
def test_user_creation():
    user = UserFactory()
    assert user.is_active is True

    admin = UserFactory(is_staff=True, is_superuser=True)
```

## Parametrized Tests

```python
@pytest.mark.django_db
@pytest.mark.parametrize('amount,expected_status', [
    pytest.param(Decimal('100.00'), 'success', id='valid'),
    pytest.param(Decimal('0.00'), 'error', id='zero'),
    pytest.param(Decimal('-10.00'), 'error', id='negative'),
])
def test_order_validation(user, amount, expected_status):
    result = validate_order(user=user, amount=amount)
    assert result.status == expected_status
```

## Test Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

## API Testing

```python
@pytest.mark.django_db
def test_user_detail_api(api_client, user):
    response = api_client.get(f'/api/users/{user.id}/')

    assert response.status_code == 200
    assert response.data['email'] == user.email
    assert 'password' not in response.data
```

## Test Quality Checklist

- [ ] Test calls real code (not just mocks)
- [ ] Has assertions that check results
- [ ] Assertions verify specific values
- [ ] Edge cases covered (None, empty list, negative)
- [ ] Test will fail if code breaks
