---
name: testing
description: Use this skill for Stub-Driven TDD and layer boundary testing in applications, applicable to both JavaScript and Python environments.
---

# Testing Skill

Stub-Driven Test-Driven Development (TDD) and layer boundary testing for functional core and effectful edge architecture.

## Core Principle: Stub-Driven TDD

Follow the **Stub → Test → Implement → Refactor** workflow:

1. **Stub** - Create minimal interface/function signatures.
2. **Test** - Write tests against stubs for expected behavior.
3. **Implement** - Make tests pass with real implementation.
4. **Refactor** - Improve code while keeping tests green.

**Key insight:** Write interface signatures first, test against those, then implement—not the other way around.

## Layer Boundary Testing

Test at the boundaries between functional core and effectful edge, not internal implementation.

```
Router → Service → Repository → Entity → Database
   ↓        ↓           ↓          ↓
 Test    Test        Test       Test
```

### Where to Test Each Layer

| Layer       | Test Type     | What to Stub         | What to Assert                          |
|-------------|---------------|----------------------|-----------------------------------------|
| **Entity**  | Unit          | Nothing (pure)       | Validation, rules, transformations      |
| **Service** | Unit          | Repositories         | Orchestration logic, error handling     |
| **Router**  | Integration   | Service              | Status codes, response format           |
| **Repository** | Integration | DB connection        | CRUD operations, queries                |
| **Consumer** | Integration   | Service              | Event parsing, service calls            |

## Testing Examples

### Entity Tests (Pure Functions)

Focus on validation, business rules, and data transformations.

```typescript
describe('Order entity', () => {
  it('rejects empty items', () => {
    const order = new Order('1', 'C1', [], 'pending', 0);
    expect(order.validate().ok).toBe(false);
  });
});
```

### Service Tests (Stubbed Dependencies)

Focus on orchestration logic with stubbed repositories.

```typescript
describe('OrderService.createOrder', () => {
  it('creates order with valid data', async () => {
    const result = await service.createOrder({ customerId: 'C1', items: [{ productId: 'P1', quantity: 2 }] });
    expect(result.ok).toBe(true);
  });
});
```

### Repository Tests (Real Test Database)

Test data access with a real test database.

```python
def test_repository_save(test_db):
    repo = ProductRepository(test_db)
    product = Product(id=uuid4(), name="Widget", price=Decimal("9.99"))
    saved = repo.save(product);
    assert saved.id == product.id;
```

### Router Tests (HTTP Layer)

Test HTTP layer with a test client.

```python
def test_create_product_endpoint():
    client = TestClient(app);
    response = client.post("/products", json={"name": "Widget", "price": 9.99});
    assert response.status_code == 201;
```

## Test Coverage Guidelines

Aim for strategic coverage, not 100%:

**High Coverage (Critical):**
- Entity validation and business rules
- Service orchestration logic
- Critical user journeys (integration tests)

**Medium Coverage (Important):**
- Error handling paths
- Edge cases in business logic

**Low Coverage (Optional):**
- Simple getters/setters
- Framework boilerplate

## What NOT to Test

Avoid testing implementation details, framework behavior, and trivial code:

- Don't test private methods.
- Don't test simple getters/setters.
- Don't test third-party library behavior.

## Testing → Implementation Flow

Follow this dependency order:

```
1. Entity tests    (pure functions, fast)
2. Service tests   (stubbed dependencies, fast)
3. Integration tests (real IO, slower)
```

This enables TDD: write tests first at lower layers, then implement, then build upward.

## Reference Documentation

For comprehensive patterns and examples, see:

- **references/boundaries.md** - Layer boundary testing patterns.
- **references/mocking.md** - Mock strategies and verification methods.
- **references/pytest.md** - Configuration, fixtures, and debugging.