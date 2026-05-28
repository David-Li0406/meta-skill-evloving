---
name: playwright-testing
description: Generates Playwright BDD end-to-end tests using playwright-bdd framework with pure Page Object Model pattern. Use when creating Gherkin feature files, step definitions, POMs, fixtures, or running Playwright tests.
metadata:
  author: test-implementation-agent
  version: "1.0"
---

# Playwright BDD Testing Skill

Generate and maintain Playwright BDD tests using playwright-bdd framework.

## Architecture Principles

### 1. POMs are Pure (No Decorators, No Assertions)

```typescript
// ✅ CORRECT: Pure POM
class LoginPage {
  readonly errorAlert: Locator;
  
  constructor(page: Page) {
    this.errorAlert = page.getByRole('alert');
  }
  
  async login(email: string, password: string) {
    // Actions only, no assertions
  }
}

// ❌ WRONG: Decorators or assertions in POM
class LoginPage {
  @Given('I am on login page')  // NO decorators
  async goto() { }
  
  async verifyError() {
    await expect(this.errorAlert).toBeVisible();  // NO assertions
  }
}
```

### 2. Assertions Belong in Step Definitions

```typescript
Then('I should see a login error', async ({ loginPage }) => {
  await expect(loginPage.errorAlert).toBeVisible();
});
```

### 3. Behavior-Focused Steps (Not Data-Focused)

```gherkin
# ✅ GOOD: Behavior-focused
When I login with valid credentials

# ❌ BAD: Exposes test data
When I login with email "test@example.com" and password "secret123"
```

### 4. Parameterize Only When Value IS the Requirement

| ✅ Parameterize | ❌ Don't Parameterize |
|-----------------|----------------------|
| User roles | Credentials |
| Prices, calculations | Generic error messages |
| Compliance-required text | Implementation details |

## Project Structure

```
project/
├── features/           # Gherkin feature files
├── steps/              # Step definitions (assertions here)
│   ├── fixtures.ts     # Fixtures, TEST_USERS, createBdd
│   └── *.steps.ts      # Feature-specific steps
├── page-objects/       # Pure POMs
├── .features-gen/      # Generated (git-ignored)
└── playwright.config.ts
```

## Templates

Use these templates when generating code:

- [Page Object Template](assets/page-object-template.ts)
- [Fixtures Template](assets/fixtures-template.ts)
- [Feature Template](assets/feature-template.feature)
- [Playwright Config](assets/playwright.config.ts)

## Quick Patterns

### Fixtures Setup

```typescript
import { test as base, createBdd } from 'playwright-bdd';
import { LoginPage } from '../page-objects/login.page';

export const TEST_USERS = {
  valid: { email: 'user@example.com', password: 'pass123' },
  invalid: { email: 'wrong@example.com', password: 'bad' },
};

export const test = base.extend<{ loginPage: LoginPage }>({
  loginPage: async ({ page }, use) => use(new LoginPage(page)),
});

export const { Given, When, Then } = createBdd(test);
```

### Step Definition Pattern

```typescript
// Behavior-focused action
When('I login with valid credentials', async ({ loginPage }) => {
  const { email, password } = TEST_USERS.valid;
  await loginPage.login(email, password);
});

// Assertion using POM locator
Then('I should see a login error', async ({ loginPage }) => {
  await expect(loginPage.errorAlert).toBeVisible();
});
```

### Locator Priority

1. `getByTestId()` - Most reliable
2. `getByRole()` - Semantic
3. `getByLabel()` - Form fields
4. `getByText()` - Static content
5. `locator()` - CSS (last resort)

## Common Commands

```bash
# Generate and run tests
npx bddgen && npx playwright test

# Run by tag
npx bddgen && npx playwright test --grep "@smoke"

# Debug mode
npx bddgen && npx playwright test --debug
```

## References

Detailed examples loaded on demand:

- [Page Objects](references/page-objects.md) - Complete POM examples
- [Step Definitions](references/step-definitions.md) - Behavior-focused steps
- [Fixtures](references/fixtures.md) - createBdd, hooks, TEST_USERS
- [Features](references/features.md) - Gherkin scenario examples
- [Locators](references/locators.md) - Locator strategy guide
- [Commands](references/commands.md) - CLI quick reference
- [Troubleshooting](references/troubleshooting.md) - Common issues

## Tag Organization

- `@smoke` - Critical path tests
- `@negative` - Error scenarios
- `@compliance` - Specific text requirements
- `@wip` - Work in progress
