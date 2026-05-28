---
name: shopify-testing
description: Use this skill when you need to test Shopify Apps, covering unit testing, mocking Shopify context, and end-to-end testing.
---

# Shopify App Testing

Reliable testing is crucial for ensuring your app handles Shopify's authentication and API quirks correctly.

## 1. Unit & Integration Testing (Vitest + Remix)

Use **Vitest** for running unit and integration tests in the Remix environment.

### Setup
Install dependencies:
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

### Mocking `shopify.server.ts`
Creating a mock for the `authenticate` object is critical for testing loaders and actions without hitting real Shopify APIs.

```typescript
// test/mocks/shopify.ts
import { vi } from 'vitest';

export const mockShopify = {
  authenticate: {
    admin: vi.fn(),
    public: vi.fn(),
    webhook: vi.fn(),
  },
};

// Usage in test file:
vi.mock('../app/shopify.server', () => mockShopify);

test('loader returns data for authenticated shop', async () => {
    mockShopify.authenticate.admin.mockResolvedValue({
        currentShop: 'test-shop.myshopify.com',
        session: { shop: 'test-shop.myshopify.com', accessToken: 'fake_token' },
        admin: {
             graphql: vi.fn().mockResolvedValue({ /* mock response */ })
        }
    });

    const response = await loader({ request: new Request('http://localhost/') });
    // Assertions...
});
```

## 2. Testing Loaders & Actions

Using Remix's `createRemixStub` or calling loaders/actions directly is the best way to test backend logic.

### Direct Function Call (Preferred for logic)
You can import the `loader` or `action` and call it directly with a mock Request.

```typescript
import { loader } from '../app/routes/app.dashboard';

test('dashboard loader returns stats', async () => {
   // Setup mocks...
   const response = await loader({ 
       request: new Request('http://localhost/app/dashboard'), 
       params: {} 
   });
   const data = await response.json();
   expect(data.stats).toBeDefined();
});
```

## 3. End-to-End (E2E) Testing (Playwright)

For E2E tests, you need to handle the OAuth flow or bypass it using session tokens.

### Bypassing Auth (Session Token)
The most stable way to E2E test embedded apps is to generate a valid session token (or mock the validation) so you don't have to automate the Login screen interaction which often triggers captchas.

### Basic Playwright Test
```typescript
import { test, expect } from '@playwright/test';

test('E2E test for Shopify app', async ({ page }) => {
    // Setup and navigate to the app
    await page.goto('http://localhost:3000');
    // Perform actions and assertions...
});
```