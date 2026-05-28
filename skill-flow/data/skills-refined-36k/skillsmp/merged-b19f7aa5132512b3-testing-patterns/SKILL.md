---
name: testing-patterns
description: Use this skill when writing tests, including unit tests with Vitest and E2E tests with Playwright, as well as for mocking and coverage requirements.
---

# Testing Patterns

## Purpose

Guide for writing unit tests (Vitest) and E2E tests (Playwright) following project conventions.

## Test Stack

| Tool                  | Purpose                | Config                 |
| --------------------- | ---------------------- | ---------------------- |
| Vitest                | Unit/integration tests | `vitest.config.ts`     |
| React Testing Library | Component tests        | Via Vitest             |
| Playwright            | E2E tests              | `playwright.config.ts` |
| jsdom                 | DOM environment        | Vitest config          |

## Commands

```bash
# Run Playwright E2E tests
npm run test

# Run Playwright in headed mode
npm run test:headed

# Run Playwright with UI
npm run test:ui

# Run specific browser
npm run test:chrome
npm run test:firefox
npm run test:mobile

# Run Vitest unit tests
npm run test:unit

# Run Vitest in watch mode
npm run test:unit:watch

# Run Vitest with coverage
npm run test:unit:coverage
```

## Unit Test Location & Naming

- Location: `test/**/*.{test,spec}.{ts,tsx}`
- Naming: `<feature>.test.ts` or `<component>.spec.tsx`

## Writing Unit Tests

### Basic Structure

```typescript
import { describe, it, expect, vi } from "vitest";

describe("featureName", () => {
  describe("functionName", () => {
    it("should do something specific", () => {
      // Arrange
      const input = "test";

      // Act
      const result = functionName(input);

      // Assert
      expect(result).toBe("expected");
    });
  });
});
```

### Testing Utilities/Functions

```typescript
import { describe, it, expect } from "vitest";
import { buildCanonicalUrlDynamic } from "@utils/url-filters";

describe("buildCanonicalUrlDynamic", () => {
  it("should omit tots for date and category", () => {
    expect(buildCanonicalUrlDynamic("barcelona", "tots", "tots")).toBe(
      "/barcelona"
    );
  });

  it("should include date when not tots", () => {
    expect(buildCanonicalUrlDynamic("barcelona", "avui", "tots")).toBe(
      "/barcelona/avui"
    );
  });
});
```

### Mocking with Vitest

```typescript
import { vi, describe, it, expect, beforeEach } from "vitest";

// Mock a module
vi.mock("@utils/api-helpers", () => ({
  fetchWithHmac: vi.fn(),
}));

import { fetchWithHmac } from "@utils/api-helpers";

describe("myFunction", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should call fetchWithHmac", async () => {
    vi.mocked(fetchWithHmac).mockResolvedValue({ data: [] });

    await myFunction();

    expect(fetchWithHmac).toHaveBeenCalledWith(
      expect.stringContaining("/api/events")
    );
  });
});
```

### Testing React Components

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MyComponent } from "@components/ui/MyComponent";

describe("MyComponent", () => {
  it("should render title", () => {
    render(<MyComponent title="Hello" />);

    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  it("should handle click", async () => {
    const onClick = vi.fn();
    render(<MyComponent onClick={onClick} />);

    await userEvent.click(screen.getByRole("button"));

    expect(onClick).toHaveBeenCalled();
  });
});
```

## Writing E2E Tests

### E2E Test Structure

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature Name", () => {
  test("should do something", async ({ page }) => {
    await page.goto("/barcelona");

    await expect(
      page.getByRole("heading", { name: "Barcelona" })
    ).toBeVisible();
  });
});
```

### Common Patterns

```typescript
// Wait for navigation
await page.waitForURL(/\/barcelona\/avui/);

// Click and wait
await page.getByRole("link", { name: "Events" }).click();
await page.waitForLoadState("networkidle");

// Fill form
await page.getByLabel("Search").fill("concert");
await page.getByRole("button", { name: "Search" }).click();

// Assert element count
const cards = page.locator('[data-testid="event-card"]');
await expect(cards).toHaveCount(10);

// Check URL params
expect(page.url()).toContain("search=concert");
```

### Testing Forms

```typescript
test("should submit contact form", async ({ page }) => {
  await page.goto("/contact");

  // Fill form
  await page.getByLabel("Name").fill("John Doe");
  await page.getByLabel("Email").fill("john@example.com");
  await page.getByLabel("Message").fill("Test message");

  // Submit
  await page.getByRole("button", { name: "Submit" }).click();

  // Verify success
  await expect(page.getByText("Message sent successfully")).toBeVisible();
});
```

### Visual Testing

```typescript
test("should match visual snapshot", async ({ page }) => {
  await page.goto("/landing");
  await expect(page).toHaveScreenshot("landing-page.png");
});
```

## Test Setup

The `test/setup.ts` file:

- Seeds `HMAC_SECRET` for HMAC utilities
- Sets up global test environment

## Coverage Requirements

- Aim for meaningful coverage on new code
- Run `npm run test:unit:coverage` to check
- Focus on critical paths (filters, URLs, API calls)

## Testing Checklist

- [ ] E2E tests cover critical user flows
- [ ] Authentication tests verify protected routes
- [ ] Forms are tested with valid and invalid input
- [ ] Page objects used for complex pages
- [ ] Unit tests for utility functions
- [ ] Mocks used for external services
- [ ] Tests run in CI/CD pipeline
- [ ] Test data is isolated between tests
- [ ] Visual snapshots for critical pages
- [ ] Coverage reports generated