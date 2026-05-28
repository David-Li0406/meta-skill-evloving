---
name: playwright-test
description: Writing Playwright E2E tests following project patterns and fixtures. Use when creating new E2E tests, debugging test failures, or setting up test helpers and page objects.
license: MIT
compatibility: Requires Node.js and Playwright. Tests run in playwright/ directory.
metadata:
  author: shipitsmarter
  version: "1.2"
---

# Playwright Test Skill

Guidelines for writing Playwright E2E tests in this project.

> **Detailed patterns**: See [reference/patterns.md](reference/patterns.md) for locator strategies, waiting patterns, and common issues.

---

## Quick Reference

### Common Commands

```bash
cd playwright

# Fast dev cycle (RECOMMENDED - skips teardown, ~15-20s)
npx playwright test tests/app-tests/{feature}/{feature}.spec.ts --no-deps --project=chromium

# Run specific test by name
npx playwright test tests/app-tests/{feature}/{feature}.spec.ts --grep "01. Create" --no-deps

# Full run with traces
npx playwright test tests/app-tests/{feature}/{feature}.spec.ts --trace=on

# View traces (start viewer, then open http://localhost:9400)
cd trace-viewer && node trace-viewer.js &
```

### Key Paths

| Path | Purpose |
|------|----------|
| `playwright/tests/app-tests/{feature}/` | Feature test files |
| `playwright/tests/helpers/` | Shared fixtures, functions, constants |
| `playwright/test-results/` | Traces, screenshots, videos |
| `playwright/.auth/user.json` | Stored auth state |

### Critical Rules

- Use `data-testid` for element selection (add to Vue components if missing)
- Tests must be **functional** (Create/Update/Delete), NOT navigational
- Test names: `'01. Create entity'` (two-digit prefix, <25 chars)
- **Entity references MUST start with `PW_ENTITY_PREFIX` (`pwtest-`)** - enables automatic cleanup
- **Add teardown section** in `entities.teardown.ts` to delete all `pwtest-` prefixed entities
- Use `--no-deps` during development (skip teardown)
- Always run on **both** Chromium and Firefox before committing

---

## 13-Step Implementation Workflow

**When asked to create tests, follow these steps in order:**

| Step | Action | Output |
|------|--------|--------|
| **0. Verify dev server** | Check Docker containers and Vite dev server are running | Prerequisites confirmed |
| **1. Explore** | Search codebase for views, routes, services, data-testids, API endpoints | Understanding of UI structure |
| **2. Create PLAN.md** | Document test plan following Standard PLAN.md Structure below | `playwright/tests/app-tests/{feature}/PLAN.md` |
| **3. Create mock data** | Define test fixtures and constants using `PW_ENTITY_PREFIX` | `mock-data.ts` |
| **4. Create test helpers** | Build navigation, form filling, verification, and cleanup helpers | `{feature}-helpers.ts` |
| **5. Implement tests** | Write test specifications using helpers | `{feature}.spec.ts` |
| **6. Add teardown** | Add cleanup section to `entities.teardown.ts` for `pwtest-` prefixed entities | Safety net cleanup |
| **7. Run & verify** | Execute tests on Chromium with `--no-deps --trace=on` | Test results |
| **8. Fix & iterate** | Debug failures, fix selectors/timing, update helpers | Passing tests |
| **9. Review locators** | Replace fragile CSS/index selectors with `data-testid` or robust alternatives | Maintainable selectors |
| **10. Review helpers** | Identify generic helpers and move to `~/helpers/functions.ts` if reusable | Organized codebase |
| **11. Cross-browser test** | Run on Firefox and Chromium, fix browser-specific issues | Both browsers passing |
| **12. Show traces** | Start trace viewer and display results | http://localhost:9400 |

**Do NOT skip steps. Each builds on the previous one.**

---

## Workflow: Write, Run, Iterate

**CRITICAL:** When writing Playwright tests, you MUST follow this complete workflow:

1. **Write the tests** - Follow all conventions and patterns
2. **Run tests on Chromium first** (faster iteration):
   ```bash
   cd playwright && npx playwright test <path-to-test-file> --project=chromium --no-deps
   ```
3. **Iterate until all tests pass on Chromium**
4. **Run tests on Firefox**:
   ```bash
   npx playwright test <path-to-test-file> --project=firefox --no-deps
   ```
5. **Iterate until all tests pass on Firefox**

**DO NOT consider the task complete until tests pass on BOTH Chromium and Firefox.**

---

## Project Structure

```
playwright/
├── tests/
│   ├── app-tests/           # Feature tests organized by domain
│   │   ├── address/
│   │   ├── carrier-integration/
│   │   ├── configuration/
│   │   ├── consignment/
│   │   ├── shipment/
│   │   └── tokens/
│   ├── helpers/              # Shared utilities
│   │   ├── fixtures.ts       # Custom test fixtures
│   │   ├── functions.ts      # Helper functions
│   │   ├── consts.ts         # Constants
│   │   ├── TestId.ts         # Test ID helpers
│   │   └── wrappers/         # Page object wrappers
│   ├── users/                # User management tests
│   ├── onboarding/           # Onboarding flow tests
│   └── *.login.ts, *.logout.ts, *.setup.ts, *.teardown.ts
├── playwright.config.ts
└── package.json
```

---

## Test File Structure

```typescript
import { BASE_URL } from '~/auth-consts';
import { expect, test } from '~/helpers/fixtures';
import { navigateToHome } from '~/helpers/functions';
import MultiselectWrapper from '~/helpers/wrappers/MultiselectWrapper';

test.describe.serial('feature name', () => {
  test('01. Test case description', async ({ page }) => {
    // Arrange
    await navigateToHome(page);
    
    // Act
    await page.getByTestId('some-button').click();
    
    // Assert
    await expect(page.getByText('Expected text')).toBeVisible();
  });

  test('02. Another test case', async ({ adminRolePage }) => {
    const { page } = adminRolePage;
    // Use adminRolePage fixture for authenticated tests
  });
});
```

---

## Fixtures

The project provides custom fixtures in `tests/helpers/fixtures.ts`:

```typescript
import { expect, test } from '~/helpers/fixtures';

// Available fixtures:
test('with admin role', async ({ adminRolePage }) => {
  const { page } = adminRolePage;
  // Pre-authenticated as admin user
});

test('with new role', async ({ newRolePage }) => {
  const { page } = newRolePage;
  // Fresh context without authentication
});
```

---

## Test Entity Naming

**Entity references MUST start with `PW_ENTITY_PREFIX` (`pwtest-`)** to enable automatic cleanup:

```typescript
// mock-data.ts
import { PW_ENTITY_PREFIX } from '~/helpers/consts';
import { TestId } from '~/helpers/TestId';

export const ENTITY_DATA = { name: `${PW_ENTITY_PREFIX}Test Entity` } as const;

// Fixture generator - always use PW_ENTITY_PREFIX + feature-specific suffix
export const getFixture = () => TestId.getFixtureId(8, PW_ENTITY_PREFIX + 'entity-');
// Result example: "pwtest-entity-a1b2c3d4"
```

---

## Environment Variables

Tests require these environment variables:

| Variable | Description |
|----------|-------------|
| `PLAYWRIGHT_BASE_URL` | Base URL (e.g., `https://preview.viya.me`) |
| `PLAYWRIGHT_ORY_USERNAME` | Login username |
| `PLAYWRIGHT_ORY_PASSWORD` | Login password |
| `PLAYWRIGHT_ORY_PAT` | Ory API token |
| `PLAYWRIGHT_ADMIN_MAILBOX` | Admin mailbox URL |
| `PLAYWRIGHT_ADMIN_MAILBOX_USER` | Mailbox basic auth user |
| `PLAYWRIGHT_ADMIN_MAILBOX_PASSWORD` | Mailbox basic auth password |

Local setup: Copy `.env.example` to `.env.local` and fill in values.

---

## Debugging Tests

> **For CI failure investigation:** Use the **browser-debug** skill for trace analysis and Chrome DevTools MCP usage.

```bash
npx playwright test --ui      # UI mode (recommended for development)
npx playwright test --debug   # Debug mode with breakpoints
```

```typescript
// Add console logging
page.on('console', (msg) => console.log(msg.text()));

// Pause execution
await page.pause(); // Opens Playwright Inspector

// Take screenshots
await page.screenshot({ path: 'debug-screenshot.png' });
```

---

## Trace Viewer

**Start:** `cd playwright/trace-viewer && node trace-viewer.js &`
**Open:** http://localhost:9400

Features: dashboard with browser grouping, one-click trace viewing, arrow key navigation.

---

## Checklist for New Tests

- [ ] Test file in correct `app-tests/<feature>/` directory
- [ ] Uses `test.describe.serial` for dependent tests
- [ ] Tests numbered for clarity (`01.`, `02.`, etc.)
- [ ] Uses `data-testid` selectors where possible
- [ ] Entity references start with `PW_ENTITY_PREFIX` (`pwtest-`)
- [ ] Includes cleanup helper (`deleteAllTestEntities`)
- [ ] Waits for API responses when needed
- [ ] Includes meaningful assertions
- [ ] Cleans up test data in teardown if needed
- [ ] Works on both Chromium and Firefox
- [ ] Works in CI environment (no local dependencies)
- [ ] **Tests have been run and pass successfully** (most important!)

---

## Related Documentation

- [Testing Strategy Research](../../../research/testing-strategy/2026-01-16-modern-testing-strategy.md) - When to write E2E vs unit tests

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **browser-debug** | Investigating CI test failures with traces and Chrome DevTools |
| **pr-review** | Test coverage evaluation during PR review |
| **vue-component** | Component conventions when adding test IDs |
