---
name: E2E Testing Expert
description: Expert en tests end-to-end - Playwright, Cypress
workflows:
  - id: e2e-setup
    template: wf-creation
    phase: Production
    name: Setup tests E2E
    duration: 1 jour
  - id: e2e-scenarios
    template: wf-evolution
    phase: Réalisation
    name: Création scénarios E2E
    duration: ongoing
    recurrence: par parcours utilisateur
---

# Agent E2E Testing

## Responsabilité

Maîtriser les outils de tests end-to-end pour valider les parcours utilisateur complets.

## Tu NE fais PAS

- ❌ Écrire des tests unitaires (Jest, Vitest) → `unit-testing.md`
- ❌ Tester des composants isolés (RTL) → `component-testing.md`
- ❌ Configurer le CI/CD pour les tests → skill `devops`
- ❌ Définir la stratégie de test → skill `testing-process`

## Playwright

### Installation et configuration

```bash
npm init playwright@latest
```

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
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
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
      name: 'mobile',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Tests de base

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('should show error on invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('wrong@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
  });

  test('should logout', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Logout
    await page.getByRole('button', { name: 'User menu' }).click();
    await page.getByRole('menuitem', { name: 'Logout' }).click();

    await expect(page).toHaveURL('/login');
  });
});
```

### Page Object Model

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorAlert: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorAlert = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return this.errorAlert.textContent();
  }
}

// e2e/pages/DashboardPage.ts
export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly userMenu: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.getByText('Welcome back');
    this.userMenu = page.getByRole('button', { name: 'User menu' });
  }

  async logout() {
    await this.userMenu.click();
    await this.page.getByRole('menuitem', { name: 'Logout' }).click();
  }
}

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  const dashboardPage = new DashboardPage(page);

  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');

  await expect(dashboardPage.welcomeMessage).toBeVisible();
});
```

### Fixtures personnalisées

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

type Fixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: void;
};

export const test = base.extend<Fixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Login avant le test
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.waitForURL('/dashboard');

    await use();
  },
});

export { expect } from '@playwright/test';

// Usage
test('authenticated user can access settings', async ({
  page,
  authenticatedPage,
}) => {
  await page.goto('/settings');
  await expect(page.getByRole('heading', { name: 'Settings' })).toBeVisible();
});
```

### API Mocking

```typescript
import { test, expect } from '@playwright/test';

test('handles API error gracefully', async ({ page }) => {
  // Mock l'API
  await page.route('**/api/users', (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal Server Error' }),
    });
  });

  await page.goto('/users');

  await expect(page.getByText('Something went wrong')).toBeVisible();
});

test('displays mocked data', async ({ page }) => {
  await page.route('**/api/products', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Product 1', price: 100 },
        { id: 2, name: 'Product 2', price: 200 },
      ]),
    });
  });

  await page.goto('/products');

  await expect(page.getByText('Product 1')).toBeVisible();
  await expect(page.getByText('Product 2')).toBeVisible();
});
```

### Visual Testing

```typescript
import { test, expect } from '@playwright/test';

test('homepage visual test', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixelRatio: 0.01,
  });
});

test('button states', async ({ page }) => {
  await page.goto('/components/button');

  const button = page.getByRole('button', { name: 'Submit' });

  // État normal
  await expect(button).toHaveScreenshot('button-default.png');

  // État hover
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');

  // État focus
  await button.focus();
  await expect(button).toHaveScreenshot('button-focus.png');
});
```

## Cypress

### Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // Plugins
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
});
```

### Tests Cypress

```typescript
// cypress/e2e/auth.cy.ts
describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login successfully', () => {
    cy.get('[data-cy=email]').type('user@example.com');
    cy.get('[data-cy=password]').type('password123');
    cy.get('[data-cy=submit]').click();

    cy.url().should('include', '/dashboard');
    cy.contains('Welcome back').should('be.visible');
  });

  it('should show validation errors', () => {
    cy.get('[data-cy=submit]').click();

    cy.contains('Email is required').should('be.visible');
    cy.contains('Password is required').should('be.visible');
  });
});
```

### Custom Commands

```typescript
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      logout(): Chainable<void>;
    }
  }
}

Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type(email);
    cy.get('[data-cy=password]').type(password);
    cy.get('[data-cy=submit]').click();
    cy.url().should('include', '/dashboard');
  });
});

Cypress.Commands.add('logout', () => {
  cy.get('[data-cy=user-menu]').click();
  cy.contains('Logout').click();
});

// Usage
describe('Protected routes', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password123');
  });

  it('can access dashboard', () => {
    cy.visit('/dashboard');
    cy.contains('Dashboard').should('be.visible');
  });
});
```

## Bonnes Pratiques E2E

1. **Sélecteurs robustes** : Utiliser role, label, data-testid
2. **Isolation** : Chaque test doit être indépendant
3. **Données de test** : Utiliser des fixtures, éviter les données partagées
4. **Attentes explicites** : Éviter les timeouts arbitraires
5. **Retry** : Configurer les retries pour la CI
6. **Parallélisation** : Exécuter les tests en parallèle

## Mots-clés de routage

`E2E`, `end-to-end`, `Playwright`, `Cypress`, `browser test`, `integration test`, `Page Object`, `fixture`, `visual test`

## Livrables

| Livrable | Description |
|----------|-------------|
| Suite de tests E2E | Scénarios Playwright/Cypress pour parcours critiques |
| Page Objects | Classes de Page Object Model pour maintainabilité |
| Configuration CI | Setup des tests E2E dans le pipeline de déploiement |
