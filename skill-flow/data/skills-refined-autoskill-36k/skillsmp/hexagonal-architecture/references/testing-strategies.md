# Testing Strategies for Hexagonal Architecture

## Test Pyramid by Layer

```
                    ┌─────────────────┐
                    │   E2E Tests     │  Few, slow, verify wiring
                    └────────┬────────┘
               ┌─────────────┴─────────────┐
               │   Integration Tests       │  Adapters against real infra
               └─────────────┬─────────────┘
          ┌──────────────────┴──────────────────┐
          │      Application Service Tests      │  Mocked ports
          └──────────────────┬──────────────────┘
     ┌───────────────────────┴───────────────────────┐
     │              Domain Unit Tests                │  No dependencies
     └───────────────────────────────────────────────┘
```

## Domain Layer Tests

Domain tests verify business rules with zero infrastructure. If a test needs a database, network, or filesystem, the architecture has leaked.

### Entity Tests

```python
class TestOrder:
    def test_new_order_is_pending(self):
        order = Order.create(
            customer_id=CustomerId("cust-1"),
            items=[OrderItem(sku=SKU("WIDGET"), quantity=2, unit_price=Money(10))],
            created_at=datetime(2024, 1, 15, tzinfo=timezone.utc),
        )
        assert order.status == OrderStatus.PENDING
    
    def test_cannot_cancel_shipped_order(self):
        order = self._shipped_order()
        with pytest.raises(InvalidOrderStateError):
            order.cancel()
    
    def test_total_sums_line_items(self):
        order = Order.create(
            customer_id=CustomerId("cust-1"),
            items=[
                OrderItem(sku=SKU("A"), quantity=2, unit_price=Money(10)),
                OrderItem(sku=SKU("B"), quantity=1, unit_price=Money(25)),
            ],
            created_at=datetime.now(timezone.utc),
        )
        assert order.total == Money(45)
```

### Value Object Tests

```python
class TestMoney:
    def test_addition(self):
        assert Money(10) + Money(5) == Money(15)
    
    def test_cannot_be_negative(self):
        with pytest.raises(ValueError):
            Money(-5)
    
    def test_different_currencies_cannot_add(self):
        usd = Money(10, Currency.USD)
        eur = Money(10, Currency.EUR)
        with pytest.raises(CurrencyMismatchError):
            usd + eur
```

### Domain Service Tests

```python
class TestPricingService:
    def test_bulk_discount_applied(self):
        pricing = PricingService(bulk_threshold=10, bulk_discount_pct=15)
        
        price = pricing.calculate(
            base_price=Money(100),
            quantity=15,
        )
        
        # 15 * 100 = 1500, less 15% = 1275
        assert price == Money(1275)
```

## Application Layer Tests

Application service tests verify orchestration. Mock all ports—these tests should not hit real infrastructure.

### Use Case Tests with Mocked Ports

```python
class TestPlaceOrderUseCase:
    def setup_method(self):
        self.order_repo = Mock(spec=OrderRepository)
        self.inventory = Mock(spec=InventoryService)
        self.payments = Mock(spec=PaymentGateway)
        self.clock = FixedClock(datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc))
        
        self.use_case = PlaceOrderUseCase(
            order_repository=self.order_repo,
            inventory_service=self.inventory,
            payment_gateway=self.payments,
            clock=self.clock,
        )
    
    def test_successful_order_placement(self):
        # Arrange
        self.inventory.check_availability.return_value = AvailabilityResult(all_available=True)
        self.payments.charge.return_value = PaymentResult(
            success=True,
            transaction_id=TransactionId("txn-123"),
            failure_reason=None,
        )
        
        command = PlaceOrderCommand(
            customer_id=CustomerId("cust-1"),
            items=[OrderItem(sku=SKU("WIDGET"), quantity=1, unit_price=Money(50))],
            payment_method=PaymentMethodToken("pm-abc"),
        )
        
        # Act
        result = self.use_case.execute(command)
        
        # Assert
        assert result.success
        self.order_repo.save.assert_called_once()
        saved_order = self.order_repo.save.call_args[0][0]
        assert saved_order.status == OrderStatus.CONFIRMED
    
    def test_payment_failure_does_not_persist_order(self):
        self.inventory.check_availability.return_value = AvailabilityResult(all_available=True)
        self.payments.charge.return_value = PaymentResult(
            success=False,
            transaction_id=None,
            failure_reason=PaymentFailureReason.CARD_DECLINED,
        )
        
        result = self.use_case.execute(self._valid_command())
        
        assert not result.success
        assert result.failure_reason == PaymentFailureReason.CARD_DECLINED
        self.order_repo.save.assert_not_called()
```

### Fakes vs Mocks

**Use mocks when:**
- Verifying interactions (was this method called with these arguments?)
- Port behaviour is straightforward
- Test focuses on orchestration logic

**Use fakes when:**
- Port has complex state
- Multiple interactions build on each other
- Realistic behaviour improves test clarity

```python
class InMemoryOrderRepository(OrderRepository):
    """Fake for tests requiring stateful repository behaviour."""
    
    def __init__(self):
        self._orders: dict[OrderId, Order] = {}
    
    def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order
    
    def find_by_customer(self, customer_id: CustomerId) -> list[Order]:
        return [o for o in self._orders.values() if o.customer_id == customer_id]
```

## Adapter Layer Tests

Adapter tests verify that adapters correctly implement port contracts against real infrastructure.

### Repository Adapter Tests

```python
@pytest.mark.integration
class TestPostgresOrderRepository:
    @pytest.fixture
    def repository(self, postgres_session):
        return PostgresOrderRepository(session=postgres_session)
    
    def test_save_and_retrieve(self, repository):
        order = Order.create(
            customer_id=CustomerId("cust-1"),
            items=[OrderItem(sku=SKU("W"), quantity=1, unit_price=Money(10))],
            created_at=datetime.now(timezone.utc),
        )
        
        repository.save(order)
        retrieved = repository.find_by_id(order.id)
        
        assert retrieved is not None
        assert retrieved.id == order.id
        assert retrieved.customer_id == order.customer_id
        assert retrieved.total == order.total
    
    def test_find_missing_returns_none(self, repository):
        result = repository.find_by_id(OrderId("nonexistent"))
        assert result is None
```

### External Service Adapter Tests

Use contract tests or recorded responses:

```python
@pytest.mark.integration
class TestStripePaymentAdapter:
    @pytest.fixture
    def adapter(self):
        return StripePaymentAdapter(api_key=os.environ["STRIPE_TEST_KEY"])
    
    def test_successful_charge(self, adapter):
        result = adapter.charge(
            amount=Money(100),
            payment_method=PaymentMethodToken("pm_card_visa"),  # Stripe test token
        )
        assert result.success
        assert result.transaction_id is not None
    
    def test_declined_card(self, adapter):
        result = adapter.charge(
            amount=Money(100),
            payment_method=PaymentMethodToken("pm_card_declined"),
        )
        assert not result.success
        assert result.failure_reason == PaymentFailureReason.CARD_DECLINED
```

For external services without test modes, use recorded responses:

```python
@pytest.mark.integration
class TestWeatherApiAdapter:
    def test_fetch_forecast(self, vcr_cassette):
        # VCR records/replays HTTP interactions
        adapter = WeatherApiAdapter(api_key="test")
        
        forecast = adapter.get_forecast(Location(lat=51.5, lon=-0.1))
        
        assert forecast is not None
        assert len(forecast.daily) == 7
```

## Contract Tests

Verify that fake implementations match real adapter behaviour:

```python
class OrderRepositoryContract:
    """Shared tests that both real and fake repos must pass."""
    
    @pytest.fixture
    def repository(self) -> OrderRepository:
        raise NotImplementedError
    
    def test_save_and_retrieve_roundtrip(self, repository):
        order = self._sample_order()
        repository.save(order)
        retrieved = repository.find_by_id(order.id)
        assert retrieved == order
    
    def test_find_nonexistent_returns_none(self, repository):
        assert repository.find_by_id(OrderId("missing")) is None
    
    def test_save_updates_existing(self, repository):
        order = self._sample_order()
        repository.save(order)
        
        order.cancel()
        repository.save(order)
        
        retrieved = repository.find_by_id(order.id)
        assert retrieved.status == OrderStatus.CANCELLED

class TestInMemoryOrderRepository(OrderRepositoryContract):
    @pytest.fixture
    def repository(self):
        return InMemoryOrderRepository()

class TestPostgresOrderRepository(OrderRepositoryContract):
    @pytest.fixture
    def repository(self, postgres_session):
        return PostgresOrderRepository(session=postgres_session)
```

## E2E Tests

Verify full system integration through driving adapters:

```python
@pytest.mark.e2e
class TestOrderAPI:
    def test_place_order_flow(self, test_client, seeded_inventory):
        # Create order
        response = test_client.post("/orders", json={
            "customer_id": "cust-1",
            "items": [{"sku": "WIDGET", "quantity": 2}],
            "payment_method_token": "pm_card_visa",
        })
        assert response.status_code == 201
        order_id = response.json()["order_id"]
        
        # Verify persisted
        get_response = test_client.get(f"/orders/{order_id}")
        assert get_response.status_code == 200
        assert get_response.json()["status"] == "confirmed"
```

## Architecture Tests

Verify dependency rules at build time:

```python
# tests/architecture/test_dependencies.py
import ast
from pathlib import Path

DOMAIN_PATH = Path("src/domain")
ADAPTER_PATH = Path("src/adapters")

def test_domain_does_not_import_adapters():
    """Domain layer must not depend on adapter layer."""
    forbidden = {"adapters", "sqlalchemy", "requests", "flask", "fastapi"}
    
    for py_file in DOMAIN_PATH.rglob("*.py"):
        tree = ast.parse(py_file.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module = alias.name.split(".")[0]
                    assert module not in forbidden, f"{py_file}: imports {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module = node.module.split(".")[0]
                    assert module not in forbidden, f"{py_file}: imports from {node.module}"
```

For larger projects, use dedicated tools like `import-linter` or `deptry`.
