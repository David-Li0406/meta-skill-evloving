---
name: web-testing
description: Testing patterns for React + GraphQL + Prisma stack
user-invocable: false
---

# Web Testing Skill

**Version:** 1.0
**Stack:** React Testing Library + Jest + Prisma

> Testing strategies for the full stack: components, hooks, resolvers, and services.

---

## Core Principles

1. **Test Behavior, Not Implementation** — Test what users see and do, not internal details.
2. **Pyramid Structure** — Many unit tests, fewer integration, minimal E2E.
3. **Fast Feedback** — Tests should run in seconds, not minutes.
4. **Deterministic** — Same input = same output. No flaky tests.
5. **Isolated** — Tests don't depend on each other or external state.

---

## Testing Pyramid

```
        /\
       /  \      E2E (5%)
      /----\     Critical user journeys only
     /      \
    /--------\   Integration (25%)
   /          \  API boundaries, database
  /------------\
 /              \ Unit (70%)
/________________\ Components, hooks, services, utils
```

| Level | Speed | Confidence | Volume |
|-------|-------|------------|--------|
| Unit | Fast (ms) | Lower | Many |
| Integration | Medium (s) | Medium | Some |
| E2E | Slow (10s+) | Highest | Few |

---

## React Component Testing

### Testing Library Philosophy

```typescript
// ❌ Bad - Testing implementation
expect(component.state.isOpen).toBe(true);
expect(component.find('.modal-class')).toHaveLength(1);

// ✅ Good - Testing behavior
expect(screen.getByRole('dialog')).toBeInTheDocument();
expect(screen.getByText('Modal content')).toBeVisible();
```

### Component Test Structure

```typescript
// components/ProductCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ProductCard } from './ProductCard';

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    name: 'Test Product',
    price: 1999,
    image: '/test.jpg',
  };

  it('displays product information', () => {
    render(<ProductCard product={mockProduct} onAddToCart={() => {}} />);

    expect(screen.getByRole('heading', { name: 'Test Product' })).toBeInTheDocument();
    expect(screen.getByText('$19.99')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'Test Product' })).toHaveAttribute('src', '/test.jpg');
  });

  it('calls onAddToCart when add button is clicked', async () => {
    const user = userEvent.setup();
    const mockAddToCart = jest.fn();

    render(<ProductCard product={mockProduct} onAddToCart={mockAddToCart} />);

    await user.click(screen.getByRole('button', { name: /add to cart/i }));

    expect(mockAddToCart).toHaveBeenCalledWith('1', 1);
  });

  it('updates quantity before adding to cart', async () => {
    const user = userEvent.setup();
    const mockAddToCart = jest.fn();

    render(<ProductCard product={mockProduct} onAddToCart={mockAddToCart} />);

    const quantityInput = screen.getByRole('spinbutton');
    await user.clear(quantityInput);
    await user.type(quantityInput, '3');
    await user.click(screen.getByRole('button', { name: /add to cart/i }));

    expect(mockAddToCart).toHaveBeenCalledWith('1', 3);
  });
});
```

### Query Priority

Use queries in this order (most to least preferred):

```typescript
// 1. Accessible by everyone
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText('Email');
screen.getByPlaceholderText('Search...');
screen.getByText('Welcome');

// 2. Semantic queries
screen.getByAltText('Product image');
screen.getByTitle('Close');

// 3. Test IDs (last resort)
screen.getByTestId('custom-element');
```

---

## Apollo/GraphQL Testing

### Mocking Apollo Client

```typescript
// test-utils/apollo.tsx
import { MockedProvider } from '@apollo/client/testing';
import { render } from '@testing-library/react';

export function renderWithApollo(
  ui: React.ReactElement,
  { mocks = [], ...options } = {}
) {
  return render(
    <MockedProvider mocks={mocks} addTypename={false}>
      {ui}
    </MockedProvider>,
    options
  );
}
```

### Testing Components with Queries

```typescript
// features/products/ProductList.test.tsx
import { screen, waitFor } from '@testing-library/react';
import { renderWithApollo } from '@/test-utils/apollo';
import { ProductList } from './ProductList';
import { GET_PRODUCTS } from './queries';

describe('ProductList', () => {
  const mockProducts = [
    { id: '1', name: 'Product 1', price: 999 },
    { id: '2', name: 'Product 2', price: 1999 },
  ];

  const successMock = {
    request: {
      query: GET_PRODUCTS,
      variables: { first: 20 },
    },
    result: {
      data: {
        products: {
          edges: mockProducts.map(p => ({ node: p, cursor: p.id })),
          pageInfo: { hasNextPage: false, endCursor: '2' },
        },
      },
    },
  };

  it('displays loading state initially', () => {
    renderWithApollo(<ProductList />, { mocks: [successMock] });

    expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument();
  });

  it('displays products after loading', async () => {
    renderWithApollo(<ProductList />, { mocks: [successMock] });

    await waitFor(() => {
      expect(screen.getByText('Product 1')).toBeInTheDocument();
      expect(screen.getByText('Product 2')).toBeInTheDocument();
    });
  });

  it('displays error message on failure', async () => {
    const errorMock = {
      request: { query: GET_PRODUCTS, variables: { first: 20 } },
      error: new Error('Network error'),
    };

    renderWithApollo(<ProductList />, { mocks: [errorMock] });

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/error/i);
    });
  });
});
```

### Testing Mutations

```typescript
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithApollo } from '@/test-utils/apollo';
import { AddToCartButton } from './AddToCartButton';
import { ADD_TO_CART } from './mutations';

describe('AddToCartButton', () => {
  it('adds item to cart on click', async () => {
    const user = userEvent.setup();

    const addToCartMock = {
      request: {
        query: ADD_TO_CART,
        variables: { productId: '123', quantity: 1 },
      },
      result: {
        data: {
          addToCart: {
            id: 'cart-item-1',
            productId: '123',
            quantity: 1,
          },
        },
      },
    };

    renderWithApollo(<AddToCartButton productId="123" />, {
      mocks: [addToCartMock],
    });

    await user.click(screen.getByRole('button', { name: /add to cart/i }));

    await waitFor(() => {
      expect(screen.getByText(/added/i)).toBeInTheDocument();
    });
  });
});
```

---

## Custom Hook Testing

```typescript
// hooks/useProductQuantity.test.ts
import { renderHook, act } from '@testing-library/react';
import { useProductQuantity } from './useProductQuantity';

describe('useProductQuantity', () => {
  it('starts with initial quantity', () => {
    const { result } = renderHook(() => useProductQuantity(5));

    expect(result.current.quantity).toBe(5);
  });

  it('defaults to 1 if no initial value', () => {
    const { result } = renderHook(() => useProductQuantity());

    expect(result.current.quantity).toBe(1);
  });

  it('increments quantity', () => {
    const { result } = renderHook(() => useProductQuantity());

    act(() => {
      result.current.increment();
    });

    expect(result.current.quantity).toBe(2);
  });

  it('does not decrement below 1', () => {
    const { result } = renderHook(() => useProductQuantity(1));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.quantity).toBe(1);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useProductQuantity(3));

    act(() => {
      result.current.increment();
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.quantity).toBe(3);
  });
});
```

---

## Service/Resolver Testing

### Unit Testing Services

```typescript
// services/product.service.test.ts
import { ProductService } from './product.service';
import { prismaMock } from '@/test-utils/prisma-mock';

describe('ProductService', () => {
  let service: ProductService;

  beforeEach(() => {
    service = new ProductService(prismaMock, null);
  });

  describe('findById', () => {
    it('returns product when found', async () => {
      const mockProduct = { id: '1', name: 'Test', price: 999 };
      prismaMock.product.findUnique.mockResolvedValue(mockProduct);

      const result = await service.findById('1');

      expect(result).toEqual(mockProduct);
      expect(prismaMock.product.findUnique).toHaveBeenCalledWith({
        where: { id: '1' },
      });
    });

    it('returns null when not found', async () => {
      prismaMock.product.findUnique.mockResolvedValue(null);

      const result = await service.findById('nonexistent');

      expect(result).toBeNull();
    });
  });

  describe('create', () => {
    it('creates product successfully', async () => {
      const input = { name: 'New Product', priceInCents: 1999, categoryId: 'cat1' };
      const created = { id: '1', ...input, price: 1999 };

      prismaMock.product.create.mockResolvedValue(created);

      const result = await service.create(input);

      expect(result.product).toEqual(created);
      expect(result.errors).toHaveLength(0);
    });

    it('returns error on duplicate name', async () => {
      const input = { name: 'Existing', priceInCents: 1999, categoryId: 'cat1' };

      prismaMock.product.create.mockRejectedValue({
        code: 'P2002',
        meta: { target: ['name'] },
      });

      const result = await service.create(input);

      expect(result.product).toBeNull();
      expect(result.errors).toContainEqual(
        expect.objectContaining({ code: 'CONFLICT' })
      );
    });
  });
});
```

### Prisma Mock Setup

```typescript
// test-utils/prisma-mock.ts
import { PrismaClient } from '@prisma/client';
import { mockDeep, DeepMockProxy } from 'jest-mock-extended';

export type MockPrismaClient = DeepMockProxy<PrismaClient>;

export const prismaMock = mockDeep<PrismaClient>();

// Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});
```

---

## Integration Testing with Real Database

### Test Database Setup

```typescript
// test-utils/db.ts
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

const prisma = new PrismaClient();

export async function setupTestDatabase() {
  // Use test database
  process.env.DATABASE_URL = process.env.TEST_DATABASE_URL;

  // Reset and migrate
  execSync('npx prisma migrate reset --force --skip-seed', {
    env: { ...process.env, DATABASE_URL: process.env.TEST_DATABASE_URL },
  });
}

export async function cleanupTestDatabase() {
  // Delete all data in reverse order of dependencies
  await prisma.orderItem.deleteMany();
  await prisma.order.deleteMany();
  await prisma.product.deleteMany();
  await prisma.category.deleteMany();
  await prisma.user.deleteMany();
}

export { prisma };
```

### Integration Test Example

```typescript
// features/orders/order.integration.test.ts
import { prisma, cleanupTestDatabase } from '@/test-utils/db';
import { OrderService } from './order.service';

describe('OrderService Integration', () => {
  let orderService: OrderService;
  let testUser: User;
  let testProduct: Product;

  beforeAll(async () => {
    // Create test data
    testUser = await prisma.user.create({
      data: { email: 'test@example.com', name: 'Test User' },
    });

    const category = await prisma.category.create({
      data: { name: 'Test Category' },
    });

    testProduct = await prisma.product.create({
      data: { name: 'Test Product', price: 999, categoryId: category.id, stock: 10 },
    });
  });

  beforeEach(() => {
    orderService = new OrderService(prisma, testUser);
  });

  afterAll(async () => {
    await cleanupTestDatabase();
  });

  it('creates order and decrements stock', async () => {
    const result = await orderService.create({
      items: [{ productId: testProduct.id, quantity: 2 }],
    });

    expect(result.order).toBeDefined();
    expect(result.errors).toHaveLength(0);

    // Verify stock was decremented
    const updatedProduct = await prisma.product.findUnique({
      where: { id: testProduct.id },
    });
    expect(updatedProduct?.stock).toBe(8);
  });

  it('fails when insufficient stock', async () => {
    const result = await orderService.create({
      items: [{ productId: testProduct.id, quantity: 100 }],
    });

    expect(result.order).toBeNull();
    expect(result.errors).toContainEqual(
      expect.objectContaining({ message: expect.stringContaining('stock') })
    );
  });
});
```

---

## File Organization

```
src/
├── components/
│   └── Button/
│       ├── Button.tsx
│       └── Button.test.tsx      # Co-located
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts          # Co-located
├── services/
│   ├── product.service.ts
│   └── product.service.test.ts  # Co-located
├── features/
│   └── products/
│       ├── ProductList.tsx
│       └── ProductList.test.tsx # Co-located
└── test-utils/                   # Shared test utilities
    ├── apollo.tsx
    ├── prisma-mock.ts
    └── db.ts

# Or separate __tests__ folders:
src/
├── components/
│   └── Button/
│       ├── Button.tsx
│       └── __tests__/
│           └── Button.test.tsx
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Testing implementation** | Brittle tests, false failures | Test behavior and output |
| **Snapshot overuse** | Large, meaningless diffs | Targeted assertions |
| **No async handling** | Race conditions, flaky tests | Use waitFor, findBy |
| **Shared mutable state** | Tests affect each other | Fresh setup per test |
| **Testing library internals** | Coupling to implementation | Mock at boundaries |
| **Too many E2E tests** | Slow, flaky, hard to debug | More unit/integration |
| **No error case tests** | False confidence | Test unhappy paths |
| **Manual DOM queries** | Fragile, not accessible | Use Testing Library queries |

---

## Checklist

### Component Tests
- [ ] Uses Testing Library queries (getByRole, getByText)
- [ ] Tests user interactions (click, type)
- [ ] Tests loading states
- [ ] Tests error states
- [ ] Uses userEvent for interactions

### Apollo Tests
- [ ] MockedProvider wraps components
- [ ] Tests loading → success path
- [ ] Tests error handling
- [ ] Tests mutation side effects

### Service Tests
- [ ] Prisma properly mocked
- [ ] Happy path tested
- [ ] Error cases tested
- [ ] Edge cases covered

### Integration Tests
- [ ] Uses test database
- [ ] Database cleaned between tests
- [ ] Tests real data flow
- [ ] Tests across service boundaries

---

## When to Consider Alternatives

| Situation | Consider |
|-----------|----------|
| Complex E2E flows | Playwright or Cypress |
| Visual regression | Storybook + Chromatic |
| API contract testing | Pact |
| Performance testing | k6 or Artillery |
| Accessibility testing | axe-core integration |
