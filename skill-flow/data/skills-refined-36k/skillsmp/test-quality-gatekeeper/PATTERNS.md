# Test Patterns & Anti-Patterns

Examples of tests that give false confidence vs tests that actually protect.

---

## Anti-Pattern: Testing Happy Path Only

### :x: Bad Test
```typescript
test('createOrder creates an order', async () => {
  const order = await createOrder({
    userId: 'user-1',
    items: [{ productId: 'prod-1', quantity: 1 }],
    total: 100,
  });

  expect(order.id).toBeDefined();
  expect(order.status).toBe('created');
});
// What if quantity is 0? Negative? userId doesn't exist?
```

### :white_check_mark: Good Test
```typescript
describe('createOrder', () => {
  test('creates order with valid input', async () => {
    const order = await createOrder(validOrderInput);
    expect(order.id).toBeDefined();
    expect(order.status).toBe('created');
  });

  test('rejects order with zero quantity', async () => {
    await expect(createOrder({ ...validOrderInput, items: [{ productId: 'p1', quantity: 0 }] }))
      .rejects.toThrow('Quantity must be positive');
  });

  test('rejects order with non-existent user', async () => {
    await expect(createOrder({ ...validOrderInput, userId: 'non-existent' }))
      .rejects.toThrow('User not found');
  });

  test('rejects order with insufficient inventory', async () => {
    await expect(createOrder({ ...validOrderInput, items: [{ productId: 'p1', quantity: 9999 }] }))
      .rejects.toThrow('Insufficient inventory');
  });
});
```

---

## Anti-Pattern: No Assertions

### :x: Bad Test
```typescript
test('processPayment works', async () => {
  const result = await processPayment(paymentData);
  // No assertions! Test passes even if processPayment is broken
});
```

### :white_check_mark: Good Test
```typescript
test('processPayment charges card and returns confirmation', async () => {
  const result = await processPayment(paymentData);

  expect(result.success).toBe(true);
  expect(result.transactionId).toMatch(/^txn_[a-z0-9]+$/);
  expect(result.amount).toBe(paymentData.amount);
  expect(mockPaymentGateway.charge).toHaveBeenCalledWith({
    cardToken: paymentData.cardToken,
    amount: paymentData.amount,
    currency: paymentData.currency,
  });
});
```

---

## Anti-Pattern: Testing Implementation, Not Behavior

### :x: Bad Test
```typescript
test('UserService calls repository', async () => {
  const mockRepo = { findById: jest.fn().mockResolvedValue(user) };
  const service = new UserService(mockRepo);

  await service.getUser('123');

  // Testing HOW, not WHAT
  expect(mockRepo.findById).toHaveBeenCalledWith('123');
});
```

### :white_check_mark: Good Test
```typescript
test('getUser returns user data', async () => {
  const service = new UserService(testRepo);
  await testRepo.save(testUser);

  const result = await service.getUser(testUser.id);

  // Testing WHAT - the behavior
  expect(result).toEqual({
    id: testUser.id,
    name: testUser.name,
    email: testUser.email,
  });
});

test('getUser throws when user not found', async () => {
  const service = new UserService(testRepo);

  await expect(service.getUser('non-existent'))
    .rejects.toThrow('User not found');
});
```

---

## Anti-Pattern: Over-Mocking

### :x: Bad Test
```typescript
test('order flow works', async () => {
  const mockOrderService = { createOrder: jest.fn().mockResolvedValue({ id: '1' }) };
  const mockPaymentService = { charge: jest.fn().mockResolvedValue({ success: true }) };
  const mockInventoryService = { reserve: jest.fn().mockResolvedValue(true) };
  const mockEmailService = { send: jest.fn().mockResolvedValue(true) };

  const result = await processOrder(order, {
    orderService: mockOrderService,
    paymentService: mockPaymentService,
    inventoryService: mockInventoryService,
    emailService: mockEmailService,
  });

  expect(result.success).toBe(true);
  // This test will pass even if the real integration is broken!
});
```

### :white_check_mark: Good Test
```typescript
// Integration test with real services, only mock external boundaries
test('order flow charges payment and reserves inventory', async () => {
  // Use real services, mock only external payment gateway
  const mockPaymentGateway = createMockPaymentGateway();

  const result = await processOrder(order);

  // Verify actual database state
  const savedOrder = await orderRepo.findById(result.orderId);
  expect(savedOrder.status).toBe('confirmed');

  // Verify inventory actually decremented
  const product = await inventoryRepo.findById(order.productId);
  expect(product.quantity).toBe(initialQuantity - order.quantity);

  // Verify payment was attempted
  expect(mockPaymentGateway.charge).toHaveBeenCalled();
});
```

---

## Anti-Pattern: Flaky Time-Dependent Test

### :x: Bad Test
```typescript
test('token expires after 1 hour', async () => {
  const token = createToken();

  // Wait for real time - flaky!
  await new Promise(resolve => setTimeout(resolve, 100));

  // This might fail depending on timing
  expect(isTokenValid(token)).toBe(true);
});
```

### :white_check_mark: Good Test
```typescript
test('token expires after 1 hour', () => {
  jest.useFakeTimers();

  const token = createToken();

  // Token valid immediately
  expect(isTokenValid(token)).toBe(true);

  // Advance time by 59 minutes - still valid
  jest.advanceTimersByTime(59 * 60 * 1000);
  expect(isTokenValid(token)).toBe(true);

  // Advance past 1 hour - expired
  jest.advanceTimersByTime(2 * 60 * 1000);
  expect(isTokenValid(token)).toBe(false);

  jest.useRealTimers();
});
```

---

## Anti-Pattern: Test Without Error Cases

### :x: Bad Test
```typescript
test('API returns data', async () => {
  const response = await request(app).get('/api/users/123');
  expect(response.status).toBe(200);
  expect(response.body.name).toBe('John');
});
// What if the API is down? What if the user doesn't exist?
```

### :white_check_mark: Good Test
```typescript
describe('GET /api/users/:id', () => {
  test('returns user for valid id', async () => {
    const response = await request(app).get('/api/users/123');
    expect(response.status).toBe(200);
    expect(response.body).toMatchObject({
      id: '123',
      name: expect.any(String),
    });
  });

  test('returns 404 for non-existent user', async () => {
    const response = await request(app).get('/api/users/non-existent');
    expect(response.status).toBe(404);
    expect(response.body.error).toBe('User not found');
  });

  test('returns 400 for invalid id format', async () => {
    const response = await request(app).get('/api/users/!!!invalid!!!');
    expect(response.status).toBe(400);
    expect(response.body.error).toContain('Invalid user ID');
  });

  test('returns 401 when not authenticated', async () => {
    const response = await request(app)
      .get('/api/users/123')
      .set('Authorization', ''); // No auth

    expect(response.status).toBe(401);
  });
});
```

---

## Anti-Pattern: Shared Mutable State

### :x: Bad Test
```typescript
// Tests depend on shared state - order matters!
let testUser: User;

beforeAll(async () => {
  testUser = await createUser({ name: 'Test' });
});

test('user can be updated', async () => {
  testUser.name = 'Updated';
  await updateUser(testUser);
  // Modifies shared state!
});

test('user has original name', async () => {
  expect(testUser.name).toBe('Test');
  // FAILS because previous test modified it!
});
```

### :white_check_mark: Good Test
```typescript
describe('user operations', () => {
  let testUser: User;

  beforeEach(async () => {
    // Fresh user for each test
    testUser = await createUser({ name: 'Test' });
  });

  afterEach(async () => {
    // Clean up
    await deleteUser(testUser.id);
  });

  test('user can be updated', async () => {
    const updated = await updateUser(testUser.id, { name: 'Updated' });
    expect(updated.name).toBe('Updated');
  });

  test('user has original name', async () => {
    const fetched = await getUser(testUser.id);
    expect(fetched.name).toBe('Test');
    // Works because each test gets fresh user
  });
});
```

---

## Good Pattern: Testing Invariants

### :white_check_mark: Property-Based Test
```typescript
import fc from 'fast-check';

test('transfer never creates or destroys money', () => {
  fc.assert(
    fc.property(
      fc.integer({ min: 0, max: 1000000 }),  // amount
      fc.integer({ min: 0, max: 1000000 }),  // fromBalance
      fc.integer({ min: 0, max: 1000000 }),  // toBalance
      (amount, fromBalance, toBalance) => {
        const totalBefore = fromBalance + toBalance;

        const result = transfer(
          { balance: fromBalance },
          { balance: toBalance },
          Math.min(amount, fromBalance), // Can't transfer more than balance
        );

        const totalAfter = result.from.balance + result.to.balance;

        // Invariant: money is never created or destroyed
        expect(totalAfter).toBe(totalBefore);
      },
    ),
  );
});
```

---

## Good Pattern: Contract Tests

### :white_check_mark: Consumer-Driven Contract
```typescript
// Consumer side (frontend or calling service)
describe('UserAPI Contract', () => {
  test('GET /users/:id returns expected schema', async () => {
    const response = await userApi.getUser('123');

    // Contract: these fields MUST exist with these types
    expect(response).toMatchObject({
      id: expect.any(String),
      email: expect.stringMatching(/@/),
      createdAt: expect.any(String),
    });

    // Verify date is valid ISO string
    expect(new Date(response.createdAt).toISOString()).toBe(response.createdAt);
  });

  test('error response follows standard format', async () => {
    const response = await userApi.getUser('non-existent').catch(e => e.response);

    expect(response.status).toBe(404);
    expect(response.data).toMatchObject({
      error: expect.any(String),
      code: expect.any(String),
    });
  });
});
```

---

## Good Pattern: Smart Contract Invariant Test

### :white_check_mark: Foundry Invariant Test
```solidity
// Invariant: total supply equals sum of all balances
function invariant_totalSupply() public {
    uint256 sumOfBalances = 0;
    for (uint256 i = 0; i < holders.length; i++) {
        sumOfBalances += token.balanceOf(holders[i]);
    }
    assertEq(token.totalSupply(), sumOfBalances);
}

// Invariant: no individual balance exceeds total supply
function invariant_noBalanceExceedsTotalSupply() public {
    for (uint256 i = 0; i < holders.length; i++) {
        assertLe(token.balanceOf(holders[i]), token.totalSupply());
    }
}
```

---

## Quick Reference: Test Smells

| Smell | Problem | Fix |
|-------|---------|-----|
| `test('it works')` | Unclear what's tested | Describe behavior in name |
| No `expect`/`assert` | Test always passes | Add meaningful assertions |
| `sleep(1000)` | Flaky, slow | Mock time |
| Shared `let` variable | Tests not isolated | Use `beforeEach` |
| 50+ line test | Hard to understand | Extract setup, split tests |
| Mock everything | Tests implementation | Use real objects, mock boundaries |
| `skip`/`xit` | Dead test | Delete or fix |
| Random failures | Flaky | Fix isolation, timing, or delete |
