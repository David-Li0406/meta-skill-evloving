---
name: umbraco-e2e-testing-playwright
description: Use this skill for end-to-end testing of Umbraco backoffice extensions with Playwright and the @umbraco/playwright-testhelpers package.
---

# Umbraco E2E Testing with Playwright

This skill provides a comprehensive framework for end-to-end (E2E) testing of Umbraco backoffice extensions using Playwright and the `@umbraco/playwright-testhelpers` package. It allows for testing against a real running Umbraco instance, validating complete user workflows, and ensuring the integrity of core operations.

## When to Use

- Testing complete user workflows
- Validating data persistence
- Ensuring authentication and authorization
- Conducting acceptance testing before release
- Performing integration testing with real API responses

## Installation

To get started, install the necessary packages:

```bash
npm install @umbraco/playwright-testhelpers @umbraco/json-models-builders --save-dev
```

## Critical: Use Testhelpers for Core Umbraco

Utilize `@umbraco/playwright-testhelpers` for core Umbraco operations, which include:

| Package | Purpose | Why Required |
|---------|---------|--------------|
| `@umbraco/playwright-testhelpers` | UI and API helpers | Handles authentication, navigation, and core entity CRUD operations |
| `@umbraco/json-models-builders` | Test data builders | Creates valid Umbraco entities with the correct structure |

### Example Usage

```typescript
import { test } from '@umbraco/playwright-testhelpers';

test('my test', async ({ umbracoApi, umbracoUi }) => {
  await umbracoUi.goToBackOffice();
  await umbracoUi.login.enterEmail('admin@example.com');
});
```

## Setup

### Dependencies

Add the following to your `package.json`:

```json
{
  "devDependencies": {
    "@playwright/test": "^1.56",
    "@umbraco/playwright-testhelpers": "^17.0.15",
    "@umbraco/json-models-builders": "^2.0.42",
    "dotenv": "^16.3.1"
  },
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

Then run:

```bash
npm install
npx playwright install chromium
```

### Configuration

Create a `playwright.config.ts` file:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  use: {
    baseURL: process.env.UMBRACO_URL || 'https://localhost:44325',
    trace: 'retain-on-failure',
    ignoreHTTPSErrors: true,
    testIdAttribute: 'data-mark',
  },
});
```

### Authentication Setup

Create `tests/e2e/auth.setup.ts`:

```typescript
import { test as setup } from '@playwright/test';
import { ConstantHelper, UiHelpers } from '@umbraco/playwright-testhelpers';

setup('authenticate', async ({ page }) => {
  const umbracoUi = new UiHelpers(page);
  await umbracoUi.goToBackOffice();
  await umbracoUi.login.enterEmail(process.env.UMBRACO_USER_LOGIN!);
  await umbracoUi.login.enterPassword(process.env.UMBRACO_USER_PASSWORD!);
  await umbracoUi.login.clickLoginButton();
});
```

### Environment Variables

Create a `.env` file (add to `.gitignore`):

```bash
UMBRACO_URL=https://localhost:44325
UMBRACO_USER_LOGIN=admin@example.com
UMBRACO_USER_PASSWORD=yourpassword
```

## Testing Patterns

### Test Fixtures

Use the following pattern for your tests:

```typescript
import { test } from '@umbraco/playwright-testhelpers';

test('my test', async ({ umbracoApi, umbracoUi }) => {
  // Arrange - Setup via API
  await umbracoApi.documentType.createDefaultDocumentType('TestDocType');

  // Act - Perform user actions via UI
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.content);
  await umbracoUi.content.clickActionsMenuAtRoot();

  // Assert - Verify results
  expect(await umbracoApi.document.doesNameExist('TestContent')).toBeTruthy();
});
```

### Idempotent Cleanup

Ensure cleanup after each test:

```typescript
test.afterEach(async ({ umbracoApi }) => {
  await umbracoApi.document.ensureNameNotExists('TestContent');
  await umbracoApi.documentType.ensureNameNotExists('TestDocType');
});
```

## Complete Examples

### Example Test

```typescript
import { expect } from '@playwright/test';
import { ConstantHelper, test } from '@umbraco/playwright-testhelpers';

test('can create content', async ({ umbracoApi, umbracoUi }) => {
  // Arrange
  await umbracoApi.documentType.createDefaultDocumentType('TestDocType');

  // Act
  await umbracoUi.goToBackOffice();
  await umbracoUi.content.goToSection(ConstantHelper.sections.content);
  await umbracoUi.content.clickActionsMenuAtRoot();
  await umbracoUi.content.clickCreateActionMenuOption();
  await umbracoUi.content.enterContentName('TestContent');
  await umbracoUi.content.clickSaveButton();

  // Assert
  expect(await umbracoApi.document.doesNameExist('TestContent')).toBeTruthy();
});
```

## Troubleshooting

- Ensure `testIdAttribute: 'data-mark'` is set in `playwright.config.ts`.
- Check `.env` credentials are correct.
- Increase timeouts in the config if tests timeout.

## Related Skills

- **umbraco-testing** - Master skill for testing overview
- **umbraco-playwright-testhelpers** - Full reference for the testhelpers package
- **umbraco-test-builders** - JsonModels.Builders for test data
- **umbraco-mocked-backoffice** - Test without real backend (faster)

## Documentation

- **Playwright**: [Playwright Documentation](https://playwright.dev/docs/intro)
- **Reference tests**: `Umbraco-CMS/tests/Umbraco.Tests.AcceptanceTest`