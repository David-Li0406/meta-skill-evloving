# E2E Testing Guide - MediApp

Playwright-based end-to-end testing for the mediapp monorepo with Bun runtime.

## Prerequisites

- **API running** on port 5300 with test routes enabled
- **Database seeded** with test data
- **Test user credentials** configured

## Quick Start

```bash
# 1. Start API with test routes
cd packages/api
ENABLE_TEST_ROUTES=true bun run dev

# 2. Seed database (once)
curl -X POST http://localhost:5300/api/test/seed

# 3. Run tests
cd packages/web
bun run test
```

## Test Structure

```
packages/web/tests/
├── fixtures.ts                          # Global fixtures (auth + DB)
└── e2e/
    ├── config/
    │   ├── profile.spec.ts             # Profile settings tests
    │   ├── settings.spec.ts            # Settings tests
    │   └── profile-seed.spec.ts        # Seed verification
    ├── fixtures/
    │   └── test-data.ts                # Test constants
    └── utils/
        ├── auth.helper.ts              # Authentication helper
        └── db.helper.ts                # Database helper
```

## Fixtures

### Main Fixtures (`fixtures.ts`)

```typescript
export const test = base.extend<{
  auth: ReturnType<typeof createAuthHelper>;
  db: ReturnType<typeof createDatabaseHelper>;
  authenticatedPage: {
    page: Page;
    auth: ReturnType<typeof createAuthHelper>;
    db: ReturnType<typeof createDatabaseHelper>;
  };
}>({
  // Auth fixture - automatically logs in before each test
  auth: [
    async ({ page }, use) => {
      const auth = createAuthHelper(page);
      await auth.login();
      await use(auth);
      await auth.logout();
    },
    { scope: "test" },
  ],

  // Combined fixture - logs in without automatic seeding
  authenticatedPage: [
    async ({ page }, use) => {
      const auth = createAuthHelper(page);
      const db = createDatabaseHelper(page);

      await auth.login();
      await use({ page, auth, db });
      await auth.logout();
    },
    { scope: "test" },
  ],
});
```

### Usage

```typescript
test("should update profile", async ({ authenticatedPage }) => {
  const { page } = authenticatedPage;
  await page.goto("/dashboard/profile");
});
```

## Test Data

### `e2e/fixtures/test-data.ts`

```typescript
// Test credentials
export const TEST_CREDENTIALS = {
  email: "test@wellness.com",
  password: "test123456",
} as const;

// Test profile data
export const TEST_PROFILE_DATA = {
  displayName: "Dra. E2E Test",
  username: "e2e-test-doctor",
  title: "Médica General",
  bio: "Médica general con especialización en wellness.",
  whatsappNumber: "+1234567890",
} as const;

// App URLs
export const APP_URLS = {
  home: "/",
  login: "/auth/login",
  dashboard: "/dashboard",
  profile: "/dashboard/profile",
  settings: "/settings",
  themes: "/dashboard/themes",
  social: "/dashboard/social",
} as const;

// Wait intervals
export const WAIT_INTERVALS = {
  short: 500,
  medium: 1000,
  long: 3000,
} as const;
```

## Helpers

### Auth Helper

```typescript
class AuthHelper {
  async login(credentials?: { email: string; password: string }): Promise<void>;
  async logout(): Promise<void>;
  async expectAuthenticated(): Promise<void>;
  async expectUnauthenticated(): Promise<void>;
  async expectErrorMessage(): Promise<void>;
  async expectSuccessMessage(): Promise<void>;
}
```

**Features:**

- Auto-detects pre-filled fields in DEV mode
- Multiple logout button selectors for resilience
- Spinner detection for loading states

### Database Helper

```typescript
class DatabaseHelper {
  async resetDatabase(): Promise<boolean>;
  async seedTestData(): Promise<boolean>;
  async cleanupTestData(): Promise<boolean>;
  async getDatabaseStatus(): Promise<Record<string, unknown> | null>;
}
```

## Writing Tests

### Test Template

```typescript
import { test, expect } from "../../fixtures";
import { WAIT_INTERVALS, APP_URLS } from "../fixtures/test-data";

test.describe("Feature Name", () => {
  test.beforeEach(async ({ authenticatedPage: { page } }) => {
    await page.goto(APP_URLS.feature);
    await page.waitForLoadState("networkidle");
  });

  test("should perform action", async ({ authenticatedPage: { page } }) => {
    // Arrange
    const element = page.locator("selector");

    // Act
    await element.click();

    // Assert
    await expect(element).toHaveAttribute("expected", "value");
  });
});
```

### Best Practices

1. **Use fixtures:** Always use `authenticatedPage` for authenticated tests
2. **Add timeouts:** Use `WAIT_INTERVALS` for consistent waits
3. **Handle missing elements:** Use conditional checks for optional features
4. **Use semantic selectors:** Prefer `data-testid`, `name`, `role` over CSS classes
5. **Keep tests independent:** Each test should work in isolation

## Running Tests

### Commands

```bash
# All tests
bun run test

# With UI
bun run test:ui

# Specific file
bun run test tests/e2e/config/profile.spec.ts

# Headed mode
bun run test --headed
```

### Environment Variables

```bash
# Enable test routes (required for seeding)
ENABLE_TEST_ROUTES=true bun run dev

# API URL (default: http://localhost:5300)
export API_URL=http://localhost:5300
```

## Security

Test routes are **disabled by default**:

```bash
# Development (enabled)
ENABLE_TEST_ROUTES=true bun run dev

# Production (disabled - default)
bun run dev
```

**Protected endpoints (only with flag):**

- `POST /api/test/seed`
- `POST /api/test/reset-db`
- `POST /api/test/cleanup`
- `GET /api/test/status`

## Current Coverage

| Category               | Tests  | Status      |
| ---------------------- | ------ | ----------- |
| Profile Settings       | 15     | ✅ Passing  |
| Settings               | 13     | ✅ Passing  |
| Profile with Seed Data | 5      | ✅ Passing  |
| **Total**              | **34** | **✅ 100%** |

## CI/CD

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - name: Start API
        run: |
          cd packages/api
          ENABLE_TEST_ROUTES=true bun run dev &
          sleep 5
          curl -X POST http://localhost:5300/api/test/seed
      - name: Run tests
        run: |
          cd packages/web
          bun run test
```

## Troubleshooting

### Port Conflicts

```bash
# Check ports
lsof -i :5176  # Web
lsof -i :5300  # API

# Kill process
kill -9 <PID>
```

### Database Issues

```bash
# Reset and seed
cd packages/api
bun run db:reset
bun run db:seed
```

### Test Failures

```bash
# Run with trace for debugging
bun run test --trace on

# Run single test
bun run test tests/e2e/config/profile.spec.ts --reporter=line
```
