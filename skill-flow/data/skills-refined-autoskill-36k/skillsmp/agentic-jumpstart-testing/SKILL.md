---
name: agentic-jumpstart-testing
description: Testing patterns with Playwright for E2E tests and Vitest for unit tests. Use when writing tests, testing components, E2E testing, integration tests, mocking, or when the user mentions testing, Playwright, Vitest, test, or coverage.
---

# Testing Patterns

## Playwright E2E Testing

### Test Structure

```typescript
// tests/courses.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Courses", () => {
  test.beforeEach(async ({ page }) => {
    // Setup before each test
    await page.goto("/courses");
  });

  test("should display course list", async ({ page }) => {
    await expect(page.getByRole("heading", { name: "Courses" })).toBeVisible();
    await expect(page.getByTestId("course-card")).toHaveCount.greaterThan(0);
  });

  test("should navigate to course details", async ({ page }) => {
    await page.getByTestId("course-card").first().click();
    await expect(page).toHaveURL(/\/courses\/\d+/);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });
});
```

### Authentication in Tests

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from "@playwright/test";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  // Login flow
  await page.goto("/login");
  await page.getByLabel("Email").fill("test@example.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign In" }).click();

  // Wait for login to complete
  await expect(page).toHaveURL("/dashboard");

  // Save authentication state
  await page.context().storageState({ path: authFile });
});

// In playwright.config.ts
export default defineConfig({
  projects: [
    { name: "setup", testMatch: /.*\.setup\.ts/ },
    {
      name: "authenticated",
      testMatch: /.*\.spec\.ts/,
      dependencies: ["setup"],
      use: { storageState: authFile },
    },
  ],
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
  readonly enrollButton: Locator;
  readonly moduleList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.title = page.getByRole("heading", { level: 1 });
    this.enrollButton = page.getByRole("button", { name: "Enroll" });
    this.moduleList = page.getByTestId("module-list");
  }

  async goto(courseId: string) {
    await this.page.goto(`/courses/${courseId}`);
  }

  async enroll() {
    await this.enrollButton.click();
    await this.page.waitForURL(/\/checkout/);
  }

  async getModuleCount() {
    return this.moduleList.getByTestId("module-item").count();
  }
}

// Usage in test
test("should enroll in course", async ({ page }) => {
  const coursePage = new CoursePage(page);
  await coursePage.goto("1");
  await coursePage.enroll();
  await expect(page).toHaveURL(/\/checkout/);
});
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

### Testing Async Operations

```typescript
test("should load data", async ({ page }) => {
  await page.goto("/dashboard");

  // Wait for network request
  const responsePromise = page.waitForResponse("**/api/stats");
  await page.getByRole("button", { name: "Refresh" }).click();
  await responsePromise;

  // Verify data is displayed
  await expect(page.getByTestId("stats-card")).toBeVisible();
});
```

### Visual Testing

```typescript
test("should match visual snapshot", async ({ page }) => {
  await page.goto("/landing");
  await expect(page).toHaveScreenshot("landing-page.png");
});
```

## Vitest Unit Testing

### Testing Utility Functions

```typescript
// src/utils/format.test.ts
import { describe, it, expect } from "vitest";
import { formatCurrency, formatDate, truncate } from "./format";

describe("formatCurrency", () => {
  it("should format USD currency", () => {
    expect(formatCurrency(1234.56)).toBe("$1,234.56");
  });

  it("should handle zero", () => {
    expect(formatCurrency(0)).toBe("$0.00");
  });
});

describe("truncate", () => {
  it("should truncate long strings", () => {
    expect(truncate("Hello World", 5)).toBe("Hello...");
  });

  it("should not truncate short strings", () => {
    expect(truncate("Hi", 10)).toBe("Hi");
  });
});
```

### Testing Hooks

```typescript
// src/hooks/useDebounce.test.ts
import { describe, it, expect, vi } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useDebounce } from "./useDebounce";

describe("useDebounce", () => {
  it("should debounce value updates", async () => {
    vi.useFakeTimers();

    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: "initial" } }
    );

    expect(result.current).toBe("initial");

    rerender({ value: "updated" });
    expect(result.current).toBe("initial");

    act(() => {
      vi.advanceTimersByTime(500);
    });

    expect(result.current).toBe("updated");

    vi.useRealTimers();
  });
});
```

### Mocking

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { processPayment } from "./payment";

// Mock external module
vi.mock("stripe", () => ({
  default: vi.fn().mockImplementation(() => ({
    paymentIntents: {
      create: vi.fn().mockResolvedValue({ id: "pi_123", status: "succeeded" }),
    },
  })),
}));

describe("processPayment", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should process payment successfully", async () => {
    const result = await processPayment({ amount: 1000, currency: "usd" });
    expect(result.status).toBe("succeeded");
  });
});
```

### Testing React Components

```typescript
// src/components/Button.test.tsx
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("should render children", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button")).toHaveTextContent("Click me");
  });

  it("should call onClick handler", () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("should be disabled when loading", () => {
    render(<Button disabled>Loading</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
```

## Test Commands

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

## Test Data Setup

```typescript
// tests/setup/database.ts
import { database } from "~/db";
import { users, courses } from "~/db/schema";

export async function seedTestData() {
  // Clear existing data
  await database.delete(courses);
  await database.delete(users);

  // Insert test user
  const [testUser] = await database
    .insert(users)
    .values({
      email: "test@example.com",
      name: "Test User",
    })
    .returning();

  // Insert test courses
  await database.insert(courses).values([
    { title: "Test Course 1", authorId: testUser.id },
    { title: "Test Course 2", authorId: testUser.id },
  ]);

  return { testUser };
}
```

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
