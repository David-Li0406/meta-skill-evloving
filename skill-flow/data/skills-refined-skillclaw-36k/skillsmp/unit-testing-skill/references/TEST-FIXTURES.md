# Test Fixtures Reference

Common fixture patterns used across our test suite.

## Database Fixtures

### Session-Scoped Database

```python
@pytest.fixture(scope="session")
def db_engine():
    """Creates database engine once per test session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(db_engine):
    """Creates a new database session for each test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
```

## User Fixtures

```python
@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    def create(
        email="test@example.com",
        name="Test User",
        tier="standard",
        **kwargs
    ):
        user = User(email=email, name=name, tier=tier, **kwargs)
        db_session.add(user)
        db_session.commit()
        return user
    return create

@pytest.fixture
def authenticated_user(user_factory):
    """Pre-created authenticated user."""
    return user_factory(email="auth@example.com", tier="premium")
```

## Order Fixtures

```python
@pytest.fixture
def order_factory(db_session, authenticated_user):
    """Factory for creating test orders."""
    def create(
        user=None,
        items=None,
        status="pending",
        **kwargs
    ):
        user = user or authenticated_user
        items = items or [
            OrderItem(product_id="SKU-001", quantity=1, price=29.99)
        ]
        order = Order(user=user, items=items, status=status, **kwargs)
        db_session.add(order)
        db_session.commit()
        return order
    return create

@pytest.fixture
def sample_order(order_factory):
    """Pre-created sample order for simple tests."""
    return order_factory()
```

## API Client Fixtures

```python
@pytest.fixture
def api_client(app):
    """Test client for API endpoints."""
    return TestClient(app)

@pytest.fixture
def auth_headers(authenticated_user):
    """Authorization headers for authenticated requests."""
    token = create_token(authenticated_user)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def authenticated_client(api_client, auth_headers):
    """API client with authentication."""
    api_client.headers.update(auth_headers)
    return api_client
```

## Mock Fixtures

```python
@pytest.fixture
def mock_payment_gateway():
    """Mock for external payment gateway."""
    with patch('services.payment.gateway') as mock:
        mock.charge.return_value = PaymentResult(
            success=True,
            transaction_id="txn_123"
        )
        yield mock

@pytest.fixture
def mock_email_service():
    """Mock for email sending service."""
    with patch('services.notifications.email_client') as mock:
        mock.send.return_value = True
        yield mock
```

## Time Fixtures

```python
@pytest.fixture
def frozen_time():
    """Freeze time for deterministic tests."""
    with freeze_time("2025-01-15 10:30:00"):
        yield datetime(2025, 1, 15, 10, 30, 0)

@pytest.fixture
def mock_now(frozen_time):
    """Current time for comparisons."""
    return frozen_time
```

## Fixture Composition

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def complete_order_scenario(
    authenticated_user,
    order_factory,
    mock_payment_gateway,
    mock_email_service
):
    """Complete setup for order processing tests."""
    order = order_factory(user=authenticated_user)
    return {
        "user": authenticated_user,
        "order": order,
        "payment": mock_payment_gateway,
        "email": mock_email_service
    }
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use factories | Create entities dynamically, not statically |
| Scope appropriately | Session for slow setup, function for isolation |
| Clean up properly | Use yield, not return, for cleanup |
| Compose fixtures | Build complex scenarios from simple ones |
| Document fixtures | Add docstrings explaining purpose |
