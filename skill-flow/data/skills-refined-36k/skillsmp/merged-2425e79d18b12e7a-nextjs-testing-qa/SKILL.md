---
name: nextjs-testing-qa
description: Use this skill when writing comprehensive tests for Next.js applications, including unit, integration, and end-to-end tests with Jest, React Testing Library, and Playwright.
---

# Next.js Testing & QA Guidelines

## Overview

This skill provides a comprehensive guide for testing Next.js applications using Playwright for end-to-end tests, Jest for unit tests, and React Testing Library for component tests.

## Testing Stack

- **Jest** - Unit and integration tests
- **React Testing Library** - Component testing
- **Playwright** - End-to-end testing
- **@testing-library/jest-dom** - DOM matchers

## Testing Philosophy

### Testing Pyramid
1. **E2E Tests (10%)**: Critical user journeys
2. **Integration Tests (30%)**: Component interactions
3. **Unit Tests (60%)**: Individual functions and utilities

### What to Test
- **DO**: Test behavior, not implementation
- **DO**: Test user interactions and outcomes
- **DO**: Test error states and edge cases
- **DO**: Test accessibility
- **DON'T**: Test internal implementation details
- **DON'T**: Test third-party libraries
- **DON'T**: Over-test simple presentational components

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

## E2E Testing with Playwright

### Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### Basic E2E Test

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication', () => {
  test('should sign up new user', async ({ page }) => {
    await page.goto('/signup')

    // Fill form
    await page.fill('input[name="email"]', 'test@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.fill('input[name="confirmPassword"]', 'password123')

    // Submit
    await page.click('button[type="submit"]')

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard')

    // Verify welcome message
    await expect(page.getByText('Welcome')).toBeVisible()
  })

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'wrong@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    // Verify error message
    await expect(page.getByText('Invalid credentials')).toBeVisible()
  })
})
```

## Best Practices

1. **Test user behavior, not implementation** - Focus on what users see and do.
2. **Use semantic queries** - Prefer `getByRole`, `getByLabelText` over `getByTestId`.
3. **Test async behavior** - Use `waitFor` and `findBy*` queries.
4. **Mock external dependencies** - Mock API calls, database, etc.
5. **Keep tests isolated** - Each test should be independent.
6. **Test error states** - Verify error handling and edge cases.
7. **Use data-testid sparingly** - Only when semantic queries aren't possible.
8. **Test accessibility** - Verify ARIA attributes and keyboard navigation.

## Common Testing Patterns

### Testing Forms

```typescript
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

```typescript
test('shows loading state', async () => {
  render(<ProductList />);
  
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));
  expect(screen.getByText(/products/i)).toBeInTheDocument();
});
```

## Debugging Tests

### Debug Output

```typescript
import { screen, render } from '@testing-library/react'

// Print component tree
render(<Component />);
screen.debug();
```

### Common Issues

**Element not found:**
- Check if element exists: `screen.getByText` vs `screen.queryByText`
- Use `findBy` for async elements: `screen.findByText`

**Timing issues:**
- Use `waitFor` for async updates
- Use `findBy` queries (built-in wait)

## Testing Checklist

### E2E Tests
- [ ] Test critical user journeys (signup, login, checkout)
- [ ] Test on multiple browsers
- [ ] Test on mobile viewport
- [ ] Test error states
- [ ] Test accessibility

### Component Tests
- [ ] Test rendering
- [ ] Test user interactions
- [ ] Test props
- [ ] Test conditional rendering
- [ ] Test error states

### Unit Tests
- [ ] Test pure functions
- [ ] Test edge cases
- [ ] Test error handling

## When to Use This Skill

Invoke this skill when:
- Writing new tests
- Debugging test failures
- Setting up test infrastructure
- Testing specific scenarios (forms, async, auth)
- Implementing E2E tests
- Testing accessibility
- Mocking dependencies
- Improving test coverage