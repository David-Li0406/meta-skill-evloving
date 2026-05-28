---
name: e2e-testing
description: Tests end-to-end avec Playwright
workflows:
  - id: e2e-testing-nextjs
    template: wf-creation
    phase: Production
    name: Setup tests E2E Playwright
    duration: 1 jour
---

# E2E Testing

Tu es l'agent responsable des **tests end-to-end** avec Playwright.

## Ta Responsabilité Unique

Configurer et écrire des tests E2E pour les parcours utilisateur.

## Tu NE fais PAS

- ❌ Tests unitaires → `unit-testing.md`
- ❌ Tests composants → `integration-testing.md`
- ❌ Mocking → `mocking.md`
- ❌ CI/CD → `deployment/ci-cd`

## Input Attendu

- Parcours utilisateur critiques
- Scénarios de test
- Navigateurs cibles

## Output Produit

- Configuration Playwright
- Tests E2E
- Scripts de test

## Configuration Playwright

### Installation

```bash
npm init playwright@latest

# Ou manuellement
npm install -D @playwright/test
npx playwright install
```

### playwright.config.ts

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
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  // Démarrer le serveur Next.js avant les tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

## Scripts package.json

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:headed": "playwright test --headed"
  }
}
```

## Tests E2E Basiques

### Navigation

```typescript
// e2e/navigation.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Navigation', () => {
  test('navigue vers la page about', async ({ page }) => {
    await page.goto('/')

    await page.click('text=À propos')

    await expect(page).toHaveURL('/about')
    await expect(page.locator('h1')).toContainText('À propos')
  })

  test('le logo ramène à l\'accueil', async ({ page }) => {
    await page.goto('/about')

    await page.click('[data-testid="logo"]')

    await expect(page).toHaveURL('/')
  })
})
```

### Authentification

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentification', () => {
  test('connexion réussie', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'password123')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('text=Bienvenue')).toBeVisible()
  })

  test('affiche erreur si identifiants incorrects', async ({ page }) => {
    await page.goto('/login')

    await page.fill('input[name="email"]', 'user@example.com')
    await page.fill('input[name="password"]', 'wrongpassword')
    await page.click('button[type="submit"]')

    await expect(page.locator('text=Identifiants incorrects')).toBeVisible()
    await expect(page).toHaveURL('/login')
  })

  test('redirige vers login si non connecté', async ({ page }) => {
    await page.goto('/dashboard')

    await expect(page).toHaveURL('/login')
  })
})
```

### Formulaire CRUD

```typescript
// e2e/posts.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Gestion des posts', () => {
  test.beforeEach(async ({ page }) => {
    // Login avant chaque test
    await page.goto('/login')
    await page.fill('input[name="email"]', 'admin@example.com')
    await page.fill('input[name="password"]', 'admin123')
    await page.click('button[type="submit"]')
    await page.waitForURL('/dashboard')
  })

  test('crée un nouveau post', async ({ page }) => {
    await page.goto('/posts/new')

    await page.fill('input[name="title"]', 'Mon nouveau post')
    await page.fill('textarea[name="content"]', 'Contenu du post')
    await page.click('button[type="submit"]')

    await expect(page).toHaveURL(/\/posts\/[\w-]+/)
    await expect(page.locator('h1')).toContainText('Mon nouveau post')
  })

  test('modifie un post existant', async ({ page }) => {
    await page.goto('/posts/existing-post')

    await page.click('text=Modifier')
    await page.fill('input[name="title"]', 'Titre modifié')
    await page.click('button[type="submit"]')

    await expect(page.locator('h1')).toContainText('Titre modifié')
  })

  test('supprime un post', async ({ page }) => {
    await page.goto('/posts/post-to-delete')

    await page.click('text=Supprimer')
    await page.click('text=Confirmer')

    await expect(page).toHaveURL('/posts')
    await expect(page.locator('text=post-to-delete')).not.toBeVisible()
  })
})
```

## Fixtures et Setup

### Auth State

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test'

const authFile = 'playwright/.auth/user.json'

setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.fill('input[name="email"]', 'user@example.com')
  await page.fill('input[name="password"]', 'password123')
  await page.click('button[type="submit"]')

  await page.waitForURL('/dashboard')

  // Sauvegarder l'état d'auth
  await page.context().storageState({ path: authFile })
})

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
})
```

### Page Object Model

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly page: Page
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator
  readonly errorMessage: Locator

  constructor(page: Page) {
    this.page = page
    this.emailInput = page.locator('input[name="email"]')
    this.passwordInput = page.locator('input[name="password"]')
    this.submitButton = page.locator('button[type="submit"]')
    this.errorMessage = page.locator('[role="alert"]')
  }

  async goto() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}

// e2e/login.spec.ts
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'

test('login with Page Object', async ({ page }) => {
  const loginPage = new LoginPage(page)

  await loginPage.goto()
  await loginPage.login('user@example.com', 'password123')

  await expect(page).toHaveURL('/dashboard')
})
```

## Assertions

```typescript
// Assertions de page
await expect(page).toHaveURL('/dashboard')
await expect(page).toHaveTitle(/Dashboard/)

// Assertions d'élément
await expect(page.locator('h1')).toBeVisible()
await expect(page.locator('button')).toBeEnabled()
await expect(page.locator('input')).toHaveValue('test')
await expect(page.locator('.list')).toHaveCount(3)
await expect(page.locator('p')).toContainText('Hello')

// Assertions visuelles
await expect(page).toHaveScreenshot('dashboard.png')
```

## Debugging

```typescript
// Pause le test
await page.pause()

// Screenshot manuel
await page.screenshot({ path: 'debug.png' })

// Console logs
page.on('console', msg => console.log(msg.text()))

// Trace viewer
// npx playwright show-trace trace.zip
```

## Bonnes Pratiques

```
✅ Tester les parcours critiques (happy path)
✅ Page Object Model pour pages complexes
✅ Fixtures pour état partagé
✅ Tests indépendants et isolés
✅ Locators stables (data-testid, role)

❌ Ne pas tester tout en E2E (coûteux)
❌ Éviter les waits arbitraires
❌ Ne pas dépendre de l'ordre des tests
❌ Éviter les sélecteurs CSS fragiles
```

## Escalades

| Situation | Action |
|-----------|--------|
| Tests unitaires | → `unit-testing.md` |
| Tests composants | → `integration-testing.md` |
| Mocking API | → `mocking.md` |
| CI/CD | → `deployment/ci-cd` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration E2E | Setup Playwright/Cypress pour Next.js |
| Suite de tests E2E | Tests des parcours utilisateur |
| Documentation | Guide des tests E2E |
