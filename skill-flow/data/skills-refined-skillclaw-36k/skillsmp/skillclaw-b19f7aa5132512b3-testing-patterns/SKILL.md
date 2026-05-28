---
name: testing-patterns
description: Use this skill when writing unit tests with Vitest and E2E tests with Playwright, following best practices for test structure, naming conventions, and mocking.
---

# Skill body

## Purpose

Guide for writing unit tests (Vitest) and E2E tests (Playwright) following project conventions.

## Test Stack

| Tool                  | Purpose                | Config                 |
| --------------------- | ---------------------- | ---------------------- |
| Vitest                | Unit/integration tests | `vitest.config.ts`     |
| Playwright            | E2E tests              | `playwright.config.ts` |

## Commands

```bash
yarn test              # Run all unit tests
yarn test:watch        # Watch mode
yarn test:coverage     # With coverage report
yarn test:e2e          # Playwright E2E tests
```

## Unit Test Location & Naming

- **Location**: `test/**/*.{test,spec}.{ts,tsx}`
- **Naming**: `<feature>.test.ts` or `<component>.spec.tsx`

## E2E Test Location

- **Location**: `e2e/**/*.spec.ts`
- **Naming**: `<feature>.flow.spec.ts` or `<feature>.spec.ts`

## Writing Unit Tests

### Basic Structure

```typescript
import { describe, it, expect } from "vitest";

describe("featureName", () => {
  it("should do something specific", () => {
    // Arrange
    const input = "test";

    // Act
    const result = functionName(input);

    // Assert
    expect(result).toBe("expected");
  });
});
```

### Mocking with Vitest

```typescript
import { vi, describe, it, expect } from "vitest";

// Mock a module
vi.mock("@utils/api-helpers", () => ({
  fetchWithHm: vi.fn(),
}));
```

## Playwright E2E Testing

### Test Structure

```typescript
import { test, expect } from "@playwright/test";

test.describe("Courses", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/courses");
  });

  test("should display course list", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Courses" })).toBeVisible();
    await expect(page.getByTestId("course-card")).toHaveCount.greaterThan(0);
  });
});
```

### Authentication in Tests

```typescript
import { test as setup, expect } from "@playwright/test";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("test@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign In" }).click();
  await expect(page).toHaveURL("/dashboard");
  await page.context().storageState({ path: authFile });
});
```

### Testing Protected Routes

```typescript
test.describe("Admin Dashboard", () => {
  test.use({ storageState: "playwright/.auth/admin.json" });

  test("should access admin dashboard", async ({ page }) => {
    await page.goto("/admin");
    await expect(page.getByRole("heading", { name: "Admin Dashboard" })).toBeVisible();
  });
});
```

### Page Object Pattern

```typescript
// tests/pages/CoursePage.ts
import { Page, Locator } from "@playwright/test";

export class CoursePage {
  readonly page: Page;
  readonly title: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.locator("h1");
  }

  async navigateTo() {
    await this.page.goto("/courses");
  }
}
```