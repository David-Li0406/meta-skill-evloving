---
name: e2e
description: Tests end-to-end - parcours utilisateur
workflows:
  - id: e2e-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests E2E
    duration: 2-3 jours
---

# Tests End-to-End

Tu es expert en **tests end-to-end** pour valider les parcours utilisateurs complets.

## Mission

> Valider que l'application fonctionne de bout en bout comme un utilisateur réel.

## Tu NE fais PAS

- ❌ Configurer Cypress/Playwright → `frontend-developer/testing/e2e-testing`
- ❌ Écrire les tests → Développeurs avec skills techniques
- ❌ Tests unitaires → `types/unit`
- ❌ Tests de performance → `performance/`

## Philosophie E2E

```
┌─────────────────────────────────────────────────────────────┐
│                    Tests End-to-End                         │
│                                                             │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐     │
│  │ Browser│───▶│Frontend│───▶│  API   │───▶│Database│     │
│  └────────┘    └────────┘    └────────┘    └────────┘     │
│                                                             │
│  Simule un utilisateur réel avec une vraie stack           │
└─────────────────────────────────────────────────────────────┘
```

## Outils Principaux

| Outil | Forces | Usage |
|-------|--------|-------|
| **Playwright** | Multi-browser, auto-wait | Recommandé 2024+ |
| **Cypress** | DX excellent, debugging | Apps classiques |
| **Puppeteer** | Chrome/Edge, léger | Scripts simples |

## Playwright - Configuration

```javascript
// playwright.config.js
import { defineConfig, devices } from '@playwright/test';

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
    video: 'retain-on-failure'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
});
```

## Patterns de Test E2E

### Page Object Model

```javascript
// pages/LoginPage.js
export class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="submit"]');
    this.errorMessage = page.locator('[data-testid="error"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getError() {
    return this.errorMessage.textContent();
  }
}

// pages/DashboardPage.js
export class DashboardPage {
  constructor(page) {
    this.page = page;
    this.welcomeMessage = page.locator('[data-testid="welcome"]');
  }

  async isLoaded() {
    await this.welcomeMessage.waitFor();
    return true;
  }
}
```

### Tests avec Page Objects

```javascript
// e2e/auth.spec.js
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

test.describe('Authentication', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    const dashboard = new DashboardPage(page);

    await loginPage.goto();
    await loginPage.login('user@test.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
    expect(await dashboard.isLoaded()).toBe(true);
  });

  test('invalid credentials shows error', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login('user@test.com', 'wrongpassword');

    const error = await loginPage.getError();
    expect(error).toContain('Invalid credentials');
  });
});
```

## Parcours Critiques

### Identifier les Parcours Clés

```
🔴 CRITIQUE (toujours tester)
├── Inscription / Connexion
├── Parcours d'achat complet
├── Paiement
└── Fonctionnalités core business

🟡 IMPORTANT (tester si possible)
├── Édition de profil
├── Recherche
└── Notifications

🟢 NICE TO HAVE
├── Dark mode
├── Préférences
└── Features secondaires
```

### Exemple Parcours Achat

```javascript
test('complete purchase flow', async ({ page }) => {
  // 1. Connexion
  await page.goto('/login');
  await page.fill('[name="email"]', 'buyer@test.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/');

  // 2. Recherche et sélection produit
  await page.fill('[placeholder="Search"]', 'iPhone');
  await page.press('[placeholder="Search"]', 'Enter');
  await page.click('text=iPhone 15 Pro');
  await expect(page).toHaveURL(/\/products\/\d+/);

  // 3. Ajout au panier
  await page.click('button:has-text("Add to Cart")');
  await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

  // 4. Checkout
  await page.click('[data-testid="cart-icon"]');
  await page.click('text=Checkout');

  // 5. Paiement
  await page.fill('[name="card"]', '4242424242424242');
  await page.fill('[name="expiry"]', '12/25');
  await page.fill('[name="cvc"]', '123');
  await page.click('button:has-text("Pay")');

  // 6. Confirmation
  await expect(page).toHaveURL(/\/orders\/\d+/);
  await expect(page.locator('h1')).toHaveText('Order Confirmed');
});
```

## Gestion des Données

### Fixtures et Seeding

```javascript
// fixtures/auth.fixture.js
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Login avant le test
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@test.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page);

    // Cleanup après le test (optionnel)
  }
});

// Utilisation
test('dashboard shows user data', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('h1')).toContainText('Welcome');
});
```

### API Setup

```javascript
test.beforeEach(async ({ request }) => {
  // Reset test data via API
  await request.post('/api/test/reset');

  // Seed specific data
  await request.post('/api/test/seed', {
    data: {
      users: [{ email: 'test@test.com', name: 'Test User' }],
      products: [{ name: 'Test Product', price: 100 }]
    }
  });
});
```

## Bonnes Pratiques

### DO

- Tester les parcours critiques uniquement
- Utiliser des sélecteurs stables (data-testid)
- Attendre les éléments explicitement
- Isoler les tests (reset data)
- Capturer screenshots/videos en cas d'échec

### DON'T

- Tester chaque fonctionnalité en E2E
- Utiliser des sélecteurs CSS fragiles
- Dépendre de l'ordre des tests
- Ignorer les tests flaky
- Tester en parallèle sans isolation

## Sélecteurs Recommandés

```javascript
// ❌ Fragile
page.locator('.btn-primary.submit-form');
page.locator('#root > div > form > button');

// ✅ Stable
page.locator('[data-testid="submit-button"]');
page.getByRole('button', { name: 'Submit' });
page.getByLabel('Email');
page.getByText('Sign in');
```

## Debugging

### Mode Debug

```bash
# Lancer en mode headed avec debug
npx playwright test --headed --debug

# Lancer un test spécifique
npx playwright test login.spec.js -g "successful login"

# Générer le code
npx playwright codegen localhost:3000
```

### Traces et Screenshots

```javascript
test('with trace', async ({ page }, testInfo) => {
  // Démarrer une trace
  await page.context().tracing.start({ screenshots: true, snapshots: true });

  // ... test ...

  // Sauvegarder la trace
  await page.context().tracing.stop({ path: `trace-${testInfo.title}.zip` });
});
```

## CI Configuration

```yaml
# .github/workflows/e2e.yml
e2e:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npx playwright install --with-deps
    - run: npm run test:e2e
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: playwright-report
        path: playwright-report/
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests E2E | Parcours critiques couverts |
| Page Objects | Abstractions réutilisables |
| CI config | Pipeline avec artifacts |
| Documentation | Parcours testés et sélecteurs |
