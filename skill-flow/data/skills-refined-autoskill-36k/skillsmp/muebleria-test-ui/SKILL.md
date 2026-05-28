---
name: muebleria-test-ui
description: >
  Frontend testing patterns for MuebleriaIris UI components.
  Trigger: When writing tests for Astro pages or React components.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Writing frontend tests"
    - "Testing React components"
    - "E2E testing with Playwright"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Writing unit tests for React components
- Testing Astro pages
- E2E testing with Playwright
- Testing API integration
- Ensuring UI functionality

---

## Testing Strategy

### Test Types

```
Unit Tests     → Individual components (React Testing Library)
Integration    → Component + API interaction
E2E Tests      → Full user workflows (Playwright)
Visual Tests   → Screenshot comparison
```

---

## Critical Patterns

### Pattern 1: React Component Test

```tsx
// src/components/ui/__tests__/ProductCard.test.tsx
import { render, screen } from '@testing-library/react';
import { ProductCard } from '../ProductCard';

describe('ProductCard', () => {
  it('renders product information', () => {
    render(
      <ProductCard 
        nombre="Sofá 3 Cuerpos"
        precio={1500}
        imagen_principal="/sofá.jpg"
      />
    );
    
    expect(screen.getByText('Sofá 3 Cuerpos')).toBeInTheDocument();
    expect(screen.getByText('$1500')).toBeInTheDocument();
  });
  
  it('calls onAddToCart when button clicked', () => {
    const mockHandler = jest.fn();
    render(<ProductCard {...props} onAddToCart={mockHandler} />);
    
    fireEvent.click(screen.getByText('Agregar al Carrito'));
    expect(mockHandler).toHaveBeenCalledTimes(1);
  });
});
```

### Pattern 2: E2E Test (Playwright)

```typescript
// tests/e2e/products.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Product Catalog', () => {
  test('displays product list', async ({ page }) => {
    await page.goto('http://localhost:4321/productos');
    
    // Wait for API response
    await page.waitForSelector('[data-testid="product-card"]');
    
    // Check products are displayed
    const products = page.locator('[data-testid="product-card"]');
    await expect(products).toHaveCount(await products.count());
  });
  
  test('filters products by category', async ({ page }) => {
    await page.goto('http://localhost:4321/productos');
    
    // Click category filter
    await page.click('text=Sofás');
    
    // Verify filtered results
    await expect(page.locator('text=Sofá')).toBeVisible();
  });
});
```

### Pattern 3: Mock API Calls

```tsx
// Mock fetch in tests
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve([
      { id: 1, nombre: 'Producto 1', precio: 100 }
    ])
  })
) as jest.Mock;

// In test
test('fetches and displays products', async () => {
  render(<ProductList />);
  
  await waitFor(() => {
    expect(screen.getByText('Producto 1')).toBeInTheDocument();
  });
  
  expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api/productos');
});
```

---

## Test Structure

```
src/
├── components/
│   └── ui/
│       ├── ProductCard.tsx
│       └── __tests__/
│           └── ProductCard.test.tsx
└── tests/
    └── e2e/
        ├── products.spec.ts
        ├── cart.spec.ts
        └── checkout.spec.ts
```

---

## Commands

```bash
# Install testing dependencies
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @playwright/test

# Run unit tests
npm test

# Run E2E tests
npx playwright test

# Run E2E with UI
npx playwright test --ui

# Generate test report
npx playwright show-report
```

---

## Best Practices

```typescript
// ✅ DO: Use data-testid for stable selectors
<button data-testid="add-to-cart">Agregar</button>
await page.click('[data-testid="add-to-cart"]');

// ❌ DON'T: Use text content (fragile)
await page.click('text=Agregar');  // Breaks if text changes

// ✅ DO: Wait for network idle
await page.goto(url, { waitUntil: 'networkidle' });

// ✅ DO: Test user-visible behavior
expect(screen.getByRole('button', { name: 'Agregar' })).toBeEnabled();

// ❌ DON'T: Test implementation details
expect(component.state.count).toBe(1);  // Internal state
```

---

## QA Checklist

- [ ] Tests cover happy path + error cases
- [ ] Mock API calls don't hit real backend
- [ ] Tests are independent (no shared state)
- [ ] Use semantic queries (getByRole, getByLabelText)
- [ ] Clean up after tests (unmount, clear mocks)
- [ ] Test accessibility (ARIA, keyboard)
- [ ] E2E tests wait for async operations

---

## Resources

- **React Testing Library**: https://testing-library.com/react
- **Playwright**: https://playwright.dev
