---
id: e2e-testing
name: "E2E Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# E2E Testing

## Overview

End-to-end (E2E) testing validates complete user workflows through the entire application stack, simulating real user interactions with browsers, APIs, and databases. E2E tests ensure critical business flows work correctly from the user's perspective.

## When to Use

- Critical user journeys (signup, checkout, payment)
- Smoke tests for deployment verification
- Cross-browser compatibility testing
- Testing complex multi-step workflows
- Regression testing for major releases

## Key Principles

- **Test user journeys**: Focus on complete workflows, not features
- **Minimize E2E tests**: They're slow and brittle, test happy paths
- **Use stable selectors**: data-testid attributes, not CSS classes
- **Handle async properly**: Wait for elements, not arbitrary timeouts
- **Independent tests**: Each test should work in isolation

## Best Practices

### Playwright Setup and Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### Page Object Model

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByTestId('login-email');
    this.passwordInput = page.getByTestId('login-password');
    this.submitButton = page.getByTestId('login-submit');
    this.errorMessage = page.getByTestId('login-error');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password?' });
  }

  async goto() {
    await this.page.goto('/login');
    await expect(this.emailInput).toBeVisible();
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}

// e2e/pages/DashboardPage.ts
export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.getByTestId('welcome-message');
    this.userMenu = page.getByTestId('user-menu');
    this.logoutButton = page.getByRole('button', { name: 'Logout' });
  }

  async expectWelcomeMessage(name: string) {
    await expect(this.welcomeMessage).toContainText(`Welcome, ${name}`);
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
    await expect(this.page).toHaveURL('/login');
  }
}
```

### E2E Test Examples

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { createTestUser, deleteTestUser } from './helpers/api';

test.describe('Authentication Flow', () => {
  let testUser: { email: string; password: string; id: string };

  test.beforeEach(async () => {
    testUser = await createTestUser({
      email: `test-${Date.now()}@example.com`,
      password: 'TestPass123!',
      name: 'Test User',
    });
  });

  test.afterEach(async () => {
    if (testUser?.id) {
      await deleteTestUser(testUser.id);
    }
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login(testUser.email, testUser.password);

    await loginPage.expectLoggedIn();
    await dashboardPage.expectWelcomeMessage('Test User');
  });

  test('invalid credentials show error message', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('wrong@example.com', 'wrongpassword');

    await loginPage.expectError('Invalid email or password');
  });

  test('logout returns to login page', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login(testUser.email, testUser.password);
    await loginPage.expectLoggedIn();

    await dashboardPage.logout();
    await expect(page).toHaveURL('/login');
  });
});
```

### Complete User Journey Test

```typescript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { HomePage } from './pages/HomePage';
import { ProductPage } from './pages/ProductPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { OrderConfirmationPage } from './pages/OrderConfirmationPage';

test.describe('Checkout Flow', () => {
  test('complete purchase journey', async ({ page }) => {
    const homePage = new HomePage(page);
    const productPage = new ProductPage(page);
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);
    const confirmationPage = new OrderConfirmationPage(page);

    // Step 1: Browse to product
    await homePage.goto();
    await homePage.searchProduct('wireless headphones');
    await homePage.selectFirstProduct();

    // Step 2: Add to cart
    await productPage.selectVariant('Black');
    await productPage.setQuantity(2);
    await productPage.addToCart();
    await expect(productPage.cartNotification).toBeVisible();

    // Step 3: View cart
    await productPage.goToCart();
    await cartPage.expectItemCount(1);
    await cartPage.expectProductInCart('Wireless Headphones', 2);

    // Step 4: Proceed to checkout
    await cartPage.proceedToCheckout();

    // Step 5: Fill shipping info
    await checkoutPage.fillShippingAddress({
      firstName: 'John',
      lastName: 'Doe',
      address: '123 Test Street',
      city: 'Test City',
      zipCode: '12345',
      country: 'United States',
    });
    await checkoutPage.selectShippingMethod('Express');
    await checkoutPage.continueToPayment();

    // Step 6: Fill payment info (test card)
    await checkoutPage.fillPaymentDetails({
      cardNumber: '4242424242424242',
      expiry: '12/25',
      cvc: '123',
    });

    // Step 7: Place order
    await checkoutPage.placeOrder();

    // Step 8: Verify confirmation
    await confirmationPage.expectOrderConfirmed();
    await expect(confirmationPage.orderNumber).toBeVisible();
    await confirmationPage.expectEmailSent('john@example.com');
  });

  test('handles out of stock during checkout', async ({ page }) => {
    const cartPage = new CartPage(page);
    const checkoutPage = new CheckoutPage(page);

    // Setup: Add product that will become out of stock
    await page.goto('/cart?test=out-of-stock-scenario');

    await cartPage.proceedToCheckout();
    await checkoutPage.fillShippingAddress({ /* ... */ });
    await checkoutPage.continueToPayment();
    await checkoutPage.placeOrder();

    // Should show error and redirect to cart
    await expect(page.getByText('Some items are no longer available')).toBeVisible();
    await expect(page).toHaveURL('/cart');
  });
});
```

### API Testing with Playwright

```typescript
// e2e/api/users.spec.ts
import { test, expect, request } from '@playwright/test';

test.describe('Users API', () => {
  let apiContext;

  test.beforeAll(async () => {
    apiContext = await request.newContext({
      baseURL: process.env.API_URL || 'http://localhost:8000',
      extraHTTPHeaders: {
        'Accept': 'application/json',
      },
    });
  });

  test.afterAll(async () => {
    await apiContext.dispose();
  });

  test('create user and retrieve', async () => {
    // Create user
    const createResponse = await apiContext.post('/api/users', {
      data: {
        email: `api-test-${Date.now()}@example.com`,
        password: 'TestPass123!',
        name: 'API Test User',
      },
    });

    expect(createResponse.ok()).toBeTruthy();
    const user = await createResponse.json();
    expect(user.email).toContain('api-test');

    // Retrieve user
    const getResponse = await apiContext.get(`/api/users/${user.id}`, {
      headers: {
        'Authorization': `Bearer ${await getAuthToken(apiContext)}`,
      },
    });

    expect(getResponse.ok()).toBeTruthy();
    const retrieved = await getResponse.json();
    expect(retrieved.id).toBe(user.id);
  });

  test('validation errors return 400', async () => {
    const response = await apiContext.post('/api/users', {
      data: {
        email: 'invalid-email',
        password: '123', // Too short
      },
    });

    expect(response.status()).toBe(400);
    const errors = await response.json();
    expect(errors.errors).toBeDefined();
  });
});
```

### Visual Regression Testing

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixelRatio: 0.01,
    });
  });

  test('product card component', async ({ page }) => {
    await page.goto('/products');

    const productCard = page.getByTestId('product-card').first();
    await expect(productCard).toHaveScreenshot('product-card.png');
  });

  test('responsive design - mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    await expect(page).toHaveScreenshot('homepage-mobile.png', {
      fullPage: true,
    });
  });
});
```

### Test Data Management

```typescript
// e2e/helpers/testData.ts
import { APIRequestContext } from '@playwright/test';

interface TestUser {
  id: string;
  email: string;
  password: string;
}

const createdResources: { type: string; id: string }[] = [];

export async function createTestUser(
  api: APIRequestContext,
  overrides: Partial<TestUser> = {}
): Promise<TestUser> {
  const userData = {
    email: `e2e-${Date.now()}-${Math.random().toString(36).slice(2)}@test.com`,
    password: 'TestPassword123!',
    name: 'E2E Test User',
    ...overrides,
  };

  const response = await api.post('/api/test/users', { data: userData });
  const user = await response.json();

  createdResources.push({ type: 'user', id: user.id });

  return { ...user, password: userData.password };
}

export async function createTestProduct(
  api: APIRequestContext,
  overrides: Partial<any> = {}
): Promise<any> {
  const productData = {
    name: `Test Product ${Date.now()}`,
    price: 99.99,
    stock: 100,
    ...overrides,
  };

  const response = await api.post('/api/test/products', { data: productData });
  const product = await response.json();

  createdResources.push({ type: 'product', id: product.id });

  return product;
}

export async function cleanupTestData(api: APIRequestContext): Promise<void> {
  for (const resource of createdResources.reverse()) {
    try {
      await api.delete(`/api/test/${resource.type}s/${resource.id}`);
    } catch (e) {
      console.warn(`Failed to cleanup ${resource.type} ${resource.id}`);
    }
  }
  createdResources.length = 0;
}
```

### Fixtures for Common Scenarios

```typescript
// e2e/fixtures.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { createTestUser, cleanupTestData } from './helpers/testData';

type TestFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
  testUser: { email: string; password: string; id: string };
};

export const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  testUser: async ({ request }, use) => {
    const user = await createTestUser(request);
    await use(user);
    await cleanupTestData(request);
  },

  authenticatedPage: async ({ page, testUser }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(testUser.email, testUser.password);
    await expect(page).toHaveURL('/dashboard');
    await use(page);
  },
});

export { expect };

// Usage in tests
test('authenticated user can view profile', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  await expect(authenticatedPage.getByTestId('profile-name')).toBeVisible();
});
```

## Anti-patterns

- **Too many E2E tests**: Slow suite, high maintenance
- **Flaky selectors**: Using CSS classes or dynamic IDs
- **Hard-coded waits**: `sleep(5000)` instead of proper assertions
- **Testing UI details**: Checking CSS properties instead of behavior
- **No test isolation**: Tests depending on other tests' state
- **Testing through UI for API logic**: Use integration tests instead
- **Missing cleanup**: Test data accumulating in test environment

## References

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Cypress Documentation](https://docs.cypress.io/)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Google Testing Blog - Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
