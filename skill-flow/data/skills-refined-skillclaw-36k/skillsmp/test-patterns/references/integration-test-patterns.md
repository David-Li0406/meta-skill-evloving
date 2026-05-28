# Integration Test Patterns

Patterns for testing components working together, APIs, and external integrations.

## API Testing Patterns

### Request/Response Testing

```python
def test_create_user_endpoint(client):
    response = client.post("/api/users", json={
        "email": "new@example.com",
        "name": "New User"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"
    assert "id" in response.json()
```

### Authentication Testing

```python
@pytest.fixture
def auth_headers(user):
    token = create_token(user)
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint_requires_auth(client):
    response = client.get("/api/profile")
    assert response.status_code == 401

def test_protected_endpoint_with_auth(client, auth_headers):
    response = client.get("/api/profile", headers=auth_headers)
    assert response.status_code == 200
```

### Error Response Testing

```python
def test_validation_error_response(client, auth_headers):
    response = client.post("/api/orders",
        json={"items": []},  # Invalid: empty items
        headers=auth_headers
    )

    assert response.status_code == 422
    errors = response.json()["errors"]
    assert any(e["field"] == "items" for e in errors)
```

### Pagination Testing

```python
def test_pagination(client, auth_headers, create_items):
    # Create 25 items
    create_items(25)

    # First page
    response = client.get("/api/items?page=1&per_page=10", headers=auth_headers)
    assert len(response.json()["data"]) == 10
    assert response.json()["total"] == 25
    assert response.json()["has_next"] == True

    # Last page
    response = client.get("/api/items?page=3&per_page=10", headers=auth_headers)
    assert len(response.json()["data"]) == 5
    assert response.json()["has_next"] == False
```

## Database Integration Patterns

### Transaction Rollback

```python
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### Database State Verification

```python
def test_order_creates_audit_log(db_session):
    order = Order.create(db_session, user_id=1, items=[item])

    # Verify audit log was created
    log = db_session.query(AuditLog).filter_by(
        entity_type="Order",
        entity_id=order.id,
        action="create"
    ).first()

    assert log is not None
    assert log.user_id == 1
```

### Seed Data Fixtures

```python
@pytest.fixture
def seed_data(db_session):
    """Create standard test data"""
    admin = User.create(db_session, email="admin@test.com", role="admin")
    user = User.create(db_session, email="user@test.com", role="user")

    category = Category.create(db_session, name="Electronics")
    product = Product.create(db_session,
        name="Widget",
        category=category,
        price=99.99
    )

    return {
        "admin": admin,
        "user": user,
        "category": category,
        "product": product
    }
```

## External Service Integration

### Contract Testing

```python
def test_payment_service_contract():
    """Verify our code matches payment service expectations"""
    # Record actual response (run once against real service)
    # Then use as contract
    expected_response = {
        "id": str,  # UUID
        "status": ["pending", "completed", "failed"],
        "amount": int,
        "currency": str
    }

    response = payment_client.create_charge(amount=1000)

    assert isinstance(response["id"], str)
    assert response["status"] in expected_response["status"]
```

### Mock External Services

```python
@pytest.fixture
def mock_payment_service(requests_mock):
    requests_mock.post(
        "https://api.payment.com/charges",
        json={"id": "ch_123", "status": "completed"}
    )
    return requests_mock

def test_checkout_with_payment(client, mock_payment_service):
    response = client.post("/checkout", json={"cart_id": "cart_1"})

    assert response.status_code == 200
    assert mock_payment_service.called
```

### Retry Testing

```python
def test_retries_on_transient_failure(requests_mock):
    # First two calls fail, third succeeds
    requests_mock.post(
        "https://api.service.com/data",
        [
            {"status_code": 503},
            {"status_code": 503},
            {"json": {"success": True}}
        ]
    )

    result = resilient_client.post_data({"key": "value"})

    assert result["success"] == True
    assert requests_mock.call_count == 3
```

## End-to-End Patterns

### User Journey Testing

```python
def test_complete_purchase_flow(client):
    # Register user
    register_response = client.post("/auth/register", json={
        "email": "buyer@test.com",
        "password": "secure123"
    })
    token = register_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Add item to cart
    client.post("/cart/items",
        json={"product_id": 1, "quantity": 2},
        headers=headers
    )

    # Checkout
    checkout_response = client.post("/checkout",
        json={"payment_method": "card_123"},
        headers=headers
    )

    assert checkout_response.status_code == 200
    order_id = checkout_response.json()["order_id"]

    # Verify order
    order_response = client.get(f"/orders/{order_id}", headers=headers)
    assert order_response.json()["status"] == "confirmed"
```

### State Machine Testing

```python
@pytest.mark.parametrize("initial,action,expected", [
    ("pending", "approve", "approved"),
    ("pending", "reject", "rejected"),
    ("approved", "ship", "shipped"),
    ("shipped", "deliver", "delivered"),
])
def test_order_state_transitions(initial, action, expected, db_session):
    order = create_order(status=initial)

    getattr(order, action)()

    assert order.status == expected
```

## Performance Integration Tests

### Load Testing

```python
@pytest.mark.performance
def test_api_response_time(client, auth_headers):
    import time

    start = time.time()
    response = client.get("/api/dashboard", headers=auth_headers)
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.5, f"Response took {duration}s, expected < 0.5s"
```

### Concurrent Request Testing

```python
import asyncio
import aiohttp

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with aiohttp.ClientSession() as session:
        tasks = [
            session.get(f"http://localhost:8000/api/items/{i}")
            for i in range(100)
        ]
        responses = await asyncio.gather(*tasks)

        success_count = sum(1 for r in responses if r.status == 200)
        assert success_count == 100
```

## Test Environment Management

### Docker Compose for Tests

```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"

  test-redis:
    image: redis:7
    ports:
      - "6380:6379"
```

```python
@pytest.fixture(scope="session")
def docker_services():
    """Start required services for integration tests"""
    subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "up", "-d"])
    wait_for_services()
    yield
    subprocess.run(["docker-compose", "-f", "docker-compose.test.yml", "down"])
```

### Environment Isolation

```python
@pytest.fixture
def isolated_env(monkeypatch):
    """Ensure tests don't affect real environment"""
    monkeypatch.setenv("DATABASE_URL", "postgresql://test:test@localhost:5433/test_db")
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6380")
    monkeypatch.setenv("EXTERNAL_API_URL", "http://localhost:8080/mock")
```
