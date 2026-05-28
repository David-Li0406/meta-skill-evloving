---
name: nextjs-testing
description: Use this skill when writing tests, debugging test failures, or setting up test infrastructure for Next.js applications using Jest, React Testing Library, and Playwright.
---

# Next.js Testing Guidelines

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
    // Add assertions for the response data
  });
});
```

## Playwright E2E Tests

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
    await page.fill('input[name="email"]', 'invalid@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')
    await expect(page.getByText('Invalid credentials')).toBeVisible()
  });
});
```