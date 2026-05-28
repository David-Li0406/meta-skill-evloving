# JavaScript/TypeScript Unit Testing Patterns

## Jest Patterns

### Test Structure

```typescript
import { OrderService } from './order-service';
import { OrderRepository } from './order-repository';
import { PaymentGateway } from './payment-gateway';

jest.mock('./order-repository');
jest.mock('./payment-gateway');

describe('OrderService', () => {
  let service: OrderService;
  let mockRepository: jest.Mocked<OrderRepository>;
  let mockPaymentGateway: jest.Mocked<PaymentGateway>;

  beforeEach(() => {
    mockRepository = new OrderRepository() as jest.Mocked<OrderRepository>;
    mockPaymentGateway = new PaymentGateway() as jest.Mocked<PaymentGateway>;
    service = new OrderService(mockRepository, mockPaymentGateway);
    jest.clearAllMocks();
  });

  describe('createOrder', () => {
    it('creates order with valid input', async () => {
      // Arrange
      mockRepository.save.mockResolvedValue({ id: 'order-123' });

      // Act
      const result = await service.createOrder({ itemId: 'item-1', quantity: 2 });

      // Assert
      expect(result.id).toBe('order-123');
      expect(mockRepository.save).toHaveBeenCalledWith(
        expect.objectContaining({ itemId: 'item-1', quantity: 2 })
      );
    });

    it('throws error for negative quantity', async () => {
      await expect(
        service.createOrder({ itemId: 'item-1', quantity: -1 })
      ).rejects.toThrow('quantity must be positive');
    });
  });
});
```

### Naming Conventions

```
<method> <condition> <expected behavior>
```

Examples:
- `creates order with valid input`
- `returns zero for empty cart`
- `throws AuthError when token expired`

### Mocking

```typescript
// Mock module
jest.mock('./api-client');

// Mock return value
mockClient.fetch.mockReturnValue({ data: 'value' });
mockClient.fetch.mockReturnValueOnce({ data: 'first' });

// Mock resolved/rejected promises
mockClient.fetchAsync.mockResolvedValue({ data: 'async' });
mockClient.fetchAsync.mockRejectedValue(new Error('Network error'));

// Mock implementation
mockCalculator.add.mockImplementation((a, b) => a + b);

// Spy on existing method
const spy = jest.spyOn(console, 'error').mockImplementation(() => {});
// ... test code
spy.mockRestore();

// Mock timers
jest.useFakeTimers();
jest.advanceTimersByTime(1000);
jest.runAllTimers();
jest.useRealTimers();
```

### Assertions

```typescript
// Equality
expect(result).toBe(expected);           // strict equality
expect(result).toEqual(expected);        // deep equality
expect(result).toStrictEqual(expected);  // deep + type equality

// Truthiness
expect(result).toBeTruthy();
expect(result).toBeFalsy();
expect(result).toBeNull();
expect(result).toBeUndefined();
expect(result).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(10);
expect(floatValue).toBeCloseTo(0.3, 5);

// Strings
expect(message).toMatch(/pattern/);
expect(message).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('nested.key', 'value');
expect(obj).toMatchObject({ key: 'value' });
expect(obj).toEqual(expect.objectContaining({ key: 'value' }));

// Functions/Mocks
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(3);
expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
expect(mockFn).toHaveBeenLastCalledWith(lastArg);

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow(Error);
expect(() => fn()).toThrow('error message');
expect(() => fn()).toThrow(/pattern/);

// Async
await expect(asyncFn()).resolves.toBe(value);
await expect(asyncFn()).rejects.toThrow('error');
```

### Parameterized Tests

```typescript
describe.each([
  [0, 0],
  [1, 1],
  [5, 120],
  [10, 3628800],
])('factorial(%i)', (input, expected) => {
  it(`returns ${expected}`, () => {
    expect(calculator.factorial(input)).toBe(expected);
  });
});

it.each`
  status  | shouldRetry
  ${500}  | ${true}
  ${503}  | ${true}
  ${400}  | ${false}
  ${200}  | ${false}
`('returns $shouldRetry for status $status', ({ status, shouldRetry }) => {
  expect(client.shouldRetry(status)).toBe(shouldRetry);
});
```

## Vitest Patterns

Vitest is largely compatible with Jest. Key differences:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Use vi instead of jest
vi.mock('./api-client');
const mockFn = vi.fn();
vi.spyOn(object, 'method');
vi.useFakeTimers();

// Inline snapshots
expect(result).toMatchInlineSnapshot(`
  {
    "id": "123",
    "name": "Test"
  }
`);
```

## Testing Library Patterns

### Component Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits credentials when form is valid', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={onSubmit} />);
    
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
  
  it('shows validation error for invalid email', async () => {
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={jest.fn()} />);
    
    await user.type(screen.getByLabelText(/email/i), 'invalid');
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });
});
```

### Query Priority

Prefer queries in this order (most to least recommended):
1. `getByRole` - accessible queries
2. `getByLabelText` - form fields
3. `getByPlaceholderText` - when label not available
4. `getByText` - non-interactive elements
5. `getByTestId` - last resort

```typescript
// Preferred
screen.getByRole('button', { name: /submit/i });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('heading', { level: 1 });

// For form fields
screen.getByLabelText(/password/i);

// Avoid when possible
screen.getByTestId('submit-button');
```

### Async Testing

```typescript
it('loads and displays data', async () => {
  render(<UserProfile userId="123" />);
  
  // Wait for loading to complete
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  // Wait for data to appear
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });
  
  // Or use findBy (combines getBy + waitFor)
  const userName = await screen.findByText('John Doe');
  expect(userName).toBeInTheDocument();
});
```

## Test Data Builders

```typescript
interface Order {
  id: string;
  customerId: string;
  items: OrderItem[];
  status: OrderStatus;
}

class OrderBuilder {
  private order: Order = {
    id: `order-${crypto.randomUUID()}`,
    customerId: 'customer-1',
    items: [],
    status: 'pending',
  };

  static anOrder(): OrderBuilder {
    return new OrderBuilder();
  }

  withId(id: string): this {
    this.order.id = id;
    return this;
  }

  withStatus(status: OrderStatus): this {
    this.order.status = status;
    return this;
  }

  withItem(productId: string, quantity: number): this {
    this.order.items.push({ productId, quantity });
    return this;
  }

  build(): Order {
    return { ...this.order };
  }
}

// Usage
const order = OrderBuilder.anOrder()
  .withStatus('shipped')
  .withItem('product-1', 2)
  .build();
```

## MSW (Mock Service Worker)

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'Test User' }));
  }),
  
  rest.post('/api/orders', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({ id: 'new-order-123' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('handles server error', async () => {
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) => {
      return res(ctx.status(500));
    })
  );
  
  render(<UserProfile userId="123" />);
  
  await screen.findByText(/error loading user/i);
});
```

## Snapshot Testing

```typescript
// Basic snapshot
it('renders correctly', () => {
  const { container } = render(<Button label="Click me" />);
  expect(container).toMatchSnapshot();
});

// Inline snapshot
it('formats output correctly', () => {
  const result = formatUser({ name: 'John', age: 30 });
  expect(result).toMatchInlineSnapshot(`"John (30)"`);
});

// Update snapshots: jest --updateSnapshot or vitest -u
```
