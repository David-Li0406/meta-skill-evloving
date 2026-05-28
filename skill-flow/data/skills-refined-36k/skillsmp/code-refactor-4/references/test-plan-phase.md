# Test Plan Phase: Design Patterns

## Table of Contents

1. [Test Audit Process](#test-audit-process)
2. [Integration Test Patterns](#integration-test-patterns)
3. [When Mocks Are Acceptable](#when-mocks-are-acceptable)
4. [Test Infrastructure Setup](#test-infrastructure-setup)

---

## Test Audit Process

### Step 1: Inventory Existing Tests

Create a table of all tests touching the component:

| File | Test Name | Type | What It Tests | Mocks Used |
|------|-----------|------|---------------|------------|
| `order.test.ts` | creates order | Unit | Order creation | DB, Payment |
| `order.integration.ts` | checkout flow | Integration | Full flow | Stripe only |

### Step 2: Map Coverage to Behavior

For each component method, check test coverage:

| Method | Happy Path | Error Cases | Edge Cases | Concurrent |
|--------|------------|-------------|------------|------------|
| `processPayment()` | Yes | Partial | No | No |
| `refundPayment()` | Yes | No | No | No |

### Step 3: Identify Gaps

Common gaps to look for:
- Error handling paths
- Boundary conditions (empty arrays, null values, max limits)
- Concurrent access scenarios
- Timeout and retry behavior
- State transitions (especially invalid ones)

---

## Integration Test Patterns

### Database Integration

Test with real database, isolated per test:

```typescript
describe('OrderRepository', () => {
  let db: TestDatabase;
  let repo: OrderRepository;

  beforeEach(async () => {
    db = await TestDatabase.create();  // Fresh DB
    repo = new OrderRepository(db.connection);
  });

  afterEach(async () => {
    await db.destroy();  // Cleanup
  });

  it('persists and retrieves order', async () => {
    const order = new Order({ total: 100 });
    await repo.save(order);

    const found = await repo.findById(order.id);
    expect(found.total).toBe(100);
  });
});
```

### Service Integration

Test services with real dependencies:

```typescript
describe('OrderService integration', () => {
  let service: OrderService;
  let db: TestDatabase;

  beforeEach(async () => {
    db = await TestDatabase.create();

    // Real dependencies, test database
    const orderRepo = new OrderRepository(db.connection);
    const inventoryRepo = new InventoryRepository(db.connection);

    service = new OrderService(orderRepo, inventoryRepo);
  });

  it('reserves inventory when creating order', async () => {
    // Setup: Add inventory
    await db.insert('inventory', { productId: 'p1', quantity: 10 });

    // Act
    await service.createOrder({
      items: [{ productId: 'p1', quantity: 2 }]
    });

    // Assert: Inventory decreased
    const inventory = await db.query('SELECT quantity FROM inventory WHERE productId = $1', ['p1']);
    expect(inventory.quantity).toBe(8);
  });
});
```

### API Integration

Test HTTP handlers with real routing:

```typescript
describe('Order API', () => {
  let app: Express;
  let db: TestDatabase;

  beforeEach(async () => {
    db = await TestDatabase.create();
    app = createApp({ database: db.connection });
  });

  it('POST /orders creates order and returns 201', async () => {
    const response = await request(app)
      .post('/orders')
      .send({ items: [{ productId: 'p1', quantity: 1 }] });

    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();

    // Verify in database
    const order = await db.query('SELECT * FROM orders WHERE id = $1', [response.body.id]);
    expect(order).toBeDefined();
  });
});
```

---

## When Mocks Are Acceptable

### External Payment APIs

```typescript
// Mock Stripe to avoid real charges and latency
const mockStripe = {
  paymentIntents: {
    create: jest.fn().mockResolvedValue({
      id: 'pi_test',
      status: 'succeeded'
    })
  }
};

it('processes payment through gateway', async () => {
  const service = new PaymentService(mockStripe);
  const result = await service.charge(1000);

  expect(mockStripe.paymentIntents.create).toHaveBeenCalledWith({
    amount: 1000,
    currency: 'usd'
  });
});
```

### Email/SMS Services

```typescript
// Mock email to avoid sending real emails
const mockEmailer = {
  send: jest.fn().mockResolvedValue({ messageId: 'test' })
};

it('sends confirmation email', async () => {
  const service = new NotificationService(mockEmailer);
  await service.sendOrderConfirmation(order);

  expect(mockEmailer.send).toHaveBeenCalledWith(
    expect.objectContaining({
      to: order.customerEmail,
      subject: expect.stringContaining('Order Confirmation')
    })
  );
});
```

### Simulating Failures

```typescript
// Mock to test error handling
it('handles payment failure gracefully', async () => {
  const failingStripe = {
    paymentIntents: {
      create: jest.fn().mockRejectedValue(new Error('Card declined'))
    }
  };

  const service = new PaymentService(failingStripe);

  await expect(service.charge(1000)).rejects.toThrow('Payment failed');
});
```

---

## Test Infrastructure Setup

### Test Database Utilities

```typescript
// tests/utils/test-database.ts
export class TestDatabase {
  private connection: Connection;

  static async create(): Promise<TestDatabase> {
    const db = new TestDatabase();
    db.connection = await createConnection({
      database: `test_${randomUUID()}`,  // Unique per test
      synchronize: true
    });
    return db;
  }

  async destroy(): Promise<void> {
    await this.connection.dropDatabase();
    await this.connection.close();
  }

  // Convenience methods
  async insert(table: string, data: object): Promise<void> { /* ... */ }
  async query(sql: string, params: any[]): Promise<any> { /* ... */ }
}
```

### Test Fixtures

```typescript
// tests/fixtures/orders.ts
export const validOrder = {
  customerId: 'cust_123',
  items: [
    { productId: 'prod_1', quantity: 2, unitPrice: 1000 }
  ],
  shippingAddress: {
    street: '123 Test St',
    city: 'Testville',
    zip: '12345'
  }
};

export const orderWithDiscount = {
  ...validOrder,
  discountCode: 'SAVE10'
};
```

### Contract Tests for Interfaces

When introducing new interfaces, verify all implementations:

```typescript
// tests/contract/payment-gateway.contract.ts
export function testPaymentGatewayContract(
  name: string,
  createGateway: () => PaymentGateway
) {
  describe(`${name} implements PaymentGateway`, () => {
    let gateway: PaymentGateway;

    beforeEach(() => {
      gateway = createGateway();
    });

    it('charge returns result with id and status', async () => {
      const result = await gateway.charge(1000, 'usd');
      expect(result.id).toBeDefined();
      expect(['succeeded', 'pending', 'failed']).toContain(result.status);
    });

    it('refund returns result with id', async () => {
      const charge = await gateway.charge(1000, 'usd');
      const refund = await gateway.refund(charge.id);
      expect(refund.id).toBeDefined();
    });
  });
}

// Use in test files:
testPaymentGatewayContract('StripeAdapter', () => new StripeAdapter(testClient));
testPaymentGatewayContract('MockAdapter', () => new MockPaymentAdapter());
```
