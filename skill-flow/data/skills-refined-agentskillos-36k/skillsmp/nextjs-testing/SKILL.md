---
name: nextjs-testing
description: Testing patterns for Next.js projects using Jest, React Testing Library, and Playwright. Use when writing tests, setting up test infrastructure, or testing Next.js components, pages, API routes, or server actions.
---

# Next.js Testing Guidelines

## Testing Stack

- **Jest** - Unit and integration tests
- **React Testing Library** - Component testing
- **Playwright** - End-to-end testing
- **@testing-library/jest-dom** - DOM matchers

## Component Testing

### Server Components

Test Server Components by testing their rendered output:

```tsx
// app/components/ProductCard.test.tsx
import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

describe('ProductCard', () => {
  it('renders product information', async () => {
    const product = { id: '1', name: 'Test Product', price: 99.99 };
    const { container } = render(await ProductCard({ product }));
    
    expect(screen.getByText('Test Product')).toBeInTheDocument();
    expect(screen.getByText('$99.99')).toBeInTheDocument();
  });
});
```

### Client Components

Test interactive behavior:

```tsx
'use client';

import { render, screen, fireEvent } from '@testing-library/react';
import Counter from './Counter';

describe('Counter', () => {
  it('increments count on button click', () => {
    render(<Counter />);
    const button = screen.getByRole('button', { name: /count/i });
    
    expect(screen.getByText('0')).toBeInTheDocument();
    fireEvent.click(button);
    expect(screen.getByText('1')).toBeInTheDocument();
  });
});
```

## Page Testing

### Server Pages

```tsx
// app/products/page.test.tsx
import { render, screen } from '@testing-library/react';
import ProductsPage from './page';

// Mock data fetching
jest.mock('@/lib/api', () => ({
  getProducts: jest.fn(() => Promise.resolve([
    { id: '1', name: 'Product 1' },
  ])),
}));

describe('ProductsPage', () => {
  it('renders products', async () => {
    const page = await ProductsPage();
    render(page);
    
    expect(screen.getByText('Product 1')).toBeInTheDocument();
  });
});
```

## API Route Testing

### Route Handlers

```tsx
// app/api/posts/route.test.ts
import { GET, POST } from './route';
import { NextRequest } from 'next/server';

describe('/api/posts', () => {
  it('GET returns posts', async () => {
    const request = new NextRequest('http://localhost/api/posts');
    const response = await GET(request);
    const data = await response.json();
    
    expect(response.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
  });

  it('POST creates post', async () => {
    const request = new NextRequest('http://localhost/api/posts', {
      method: 'POST',
      body: JSON.stringify({ title: 'Test' }),
    });
    const response = await POST(request);
    
    expect(response.status).toBe(201);
  });
});
```

## Server Actions Testing

```tsx
// app/actions.test.ts
import { createPost } from './actions';

describe('createPost', () => {
  it('creates post and revalidates', async () => {
    const formData = new FormData();
    formData.set('title', 'Test Post');
    
    const result = await createPost(formData);
    
    expect(result).toEqual({ success: true });
  });
});
```

## E2E Testing with Playwright

### Page Tests

```tsx
// e2e/products.spec.ts
import { test, expect } from '@playwright/test';

test('navigates to products page', async ({ page }) => {
  await page.goto('/products');
  await expect(page.locator('h1')).toContainText('Products');
});

test('filters products', async ({ page }) => {
  await page.goto('/products');
  await page.fill('[name="search"]', 'laptop');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('.product-card')).toHaveCount(3);
});
```

### API E2E Tests

```tsx
test('API endpoint returns data', async ({ request }) => {
  const response = await request.get('/api/posts');
  expect(response.ok()).toBeTruthy();
  
  const data = await response.json();
  expect(Array.isArray(data)).toBe(true);
});
```

## Mocking Patterns

### Mock Next.js Modules

```tsx
// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
    };
  },
  usePathname() {
    return '/current-path';
  },
  useSearchParams() {
    return new URLSearchParams();
  },
}));

// Mock next/image
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props: any) => {
    // eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text
    return <img {...props} />;
  },
}));
```

### Mock Fetch

```tsx
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ data: 'test' }),
  })
) as jest.Mock;
```

## Testing Utilities

### Custom Render Function

```tsx
// lib/test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

## Best Practices

1. **Test user behavior, not implementation** - Focus on what users see and do
2. **Use semantic queries** - Prefer `getByRole`, `getByLabelText` over `getByTestId`
3. **Test async behavior** - Use `waitFor` and `findBy*` queries
4. **Mock external dependencies** - Mock API calls, database, etc.
5. **Keep tests isolated** - Each test should be independent
6. **Test error states** - Verify error handling and edge cases
7. **Use data-testid sparingly** - Only when semantic queries aren't possible
8. **Test accessibility** - Verify ARIA attributes and keyboard navigation

## Test File Organization

```
app/
  components/
    Button/
      Button.tsx
      Button.test.tsx
  api/
    posts/
      route.ts
      route.test.ts
e2e/
  products.spec.ts
  auth.spec.ts
```

## Common Patterns

### Testing Forms

```tsx
test('submits form with valid data', async () => {
  render(<ContactForm />);
  
  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/message/i), 'Hello');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));
  
  await waitFor(() => {
    expect(screen.getByText(/success/i)).toBeInTheDocument();
  });
});
```

### Testing Loading States

```tsx
test('shows loading state', async () => {
  render(<ProductList />);
  
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));
  expect(screen.getByText(/products/i)).toBeInTheDocument();
});
```
