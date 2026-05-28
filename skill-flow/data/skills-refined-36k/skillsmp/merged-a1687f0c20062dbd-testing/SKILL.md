---
name: testing
description: Use this skill when implementing features, fixing bugs, or adding test coverage by following TDD principles. Covers e2e, integration, and unit testing patterns.
---

# Testing Guidelines

Follow TDD (Test-Driven Development) for all features and bug fixes. **Always write failing tests first.**

## TDD Workflow

1. **Write a failing test** that describes the expected behavior.
2. **Run the test** to confirm it fails (red).
3. **Write the minimum code** to make the test pass.
4. **Run the test** to confirm it passes (green).
5. **Refactor** while keeping tests green.

### When to Apply TDD

- **Bug fix**: Write a test that reproduces the bug first.
- **New feature**: Write a test showing the feature doesn't exist yet.
- **Refactoring**: Ensure tests exist before changing code.

## Test Types

| When                    | Test Type   | Framework  | Location                              |
| ----------------------- | ----------- | ---------- | ------------------------------------- |
| Apps/UI features        | E2E         | Playwright | `apps/{app}/e2e/`                     |
| Data functions (Prisma) | Integration | Vitest     | `apps/{app}/src/data/` or `packages/` |
| Utils/helpers           | Unit        | Vitest     | `packages/{pkg}/*.test.ts`            |

## E2E Testing (Playwright)

### Core Principle: Test User Behavior

Test what users see and do, not implementation details. If your test breaks when you refactor CSS or rename a class, it's testing the wrong thing.

### Preventing Flaky Tests

**CRITICAL: Run new tests multiple times before considering them done.** Flaky tests often pass 90% of the time but fail intermittently. After writing a new E2E test:

```bash
# Run the test 5+ times to catch flakiness
for i in {1..5}; do pnpm e2e -- -g "test name" --reporter=line; done
```

**High-risk scenarios that commonly cause flakiness:**

| Scenario                         | Risk                          | Prevention                                         |
| -------------------------------- | ----------------------------- | -------------------------------------------------- |
| Clicking dropdown/menu items     | Animations cause instability  | Wait for item visibility, use `force: true`        |
| Actions that trigger navigation  | Page reload detaches elements | Use `waitForLoadState` or `waitForURL` after click |
| Form submissions                 | Async save operations         | Wait for success indicator before next action      |
| Clicking items in lists          | List may still be loading     | Wait for specific item with `toBeVisible()` first  |
| Keyboard navigation              | Focus state transitions       | Wait for focused element before next key press     |
| Inputs with debounced validation | State changes between actions | Use `waitForLoadState("networkidle")` after fill   |

### Defensive Patterns for Common Interactions

```typescript
// RISKY: Dropdown item click without animation handling
await page.getByRole("menuitem", { name: /settings/i }).click();
await page.getByRole("menuitem", { name: "Dark mode" }).click();

// SAFE: Wait for submenu, then force click
await page.getByRole("menuitem", { name: /settings/i }).click();
await expect(page.getByRole("menuitem", { name: "Dark mode" })).toBeVisible();
await page.getByRole("menuitem", { name: "Dark mode" }).click({ force: true });
```

### Avoid Redundant Tests

**Don't write separate tests when a higher-level test already covers the behavior.** If a test proves the final outcome, intermediate steps are implicitly verified.

### Query Priority

Use semantic queries that reflect how users interact with the page:

```typescript
// GOOD: Semantic queries (in order of preference)
page.getByRole("button", { name: "Submit" });
page.getByRole("heading", { name: "Welcome" });
page.getByLabel("Email address");
page.getByText("Sign up for free");
page.getByPlaceholder("Search...");
```

### Fix Accessibility First, Then Test

When a component lacks semantic markup, fix the component before writing tests.

### Wait Patterns

```typescript
// GOOD: Wait for visible state with timeout
await expect(page.getByRole("heading")).toBeVisible();
await expect(page.getByText("Success")).toBeVisible();
```

### Verify Destination Content, Not Just URLs

**Never rely solely on `toHaveURL` for navigation tests.** Always verify the destination page renders expected content.

## Integration Testing (Vitest + Prisma)

### Using Fixtures

```typescript
import { prisma } from "@/lib/db";
import { postFixture, memberFixture, signInAs } from "@/tests/fixtures";

describe("createComment", () => {
  describe("unauthenticated users", () => {
    test("returns unauthorized error", async () => {
      const result = await createComment({
        headers: new Headers(),
        postId: 1,
        content: "Test",
      });

      expect(result.error?.message).toBe(ErrorCode.unauthorized);
    });
  });

  describe("admin users", () => {
    let organization: Organization;
    let post: Post;
    let headers: Headers;

    beforeAll(async () => {
      const { organization, user } = await memberFixture({
        role: "admin",
      });

      post = await postFixture({ organizationId: organization.id });
      headers = await signInAs(user.email, user.password);
    });

    test("creates comment successfully", async () => {
      const result = await createComment({
        headers,
        postId: post.id,
        content: "New Comment",
      });

      expect(result.data?.content).toBe("New Comment");

      // Verify in database
      const comment = await prisma.comment.findFirst({
        where: { postId: post.id },
      });

      expect(comment?.content).toBe("New Comment");
    });
  });
});
```

## Unit Testing (Vitest)

### Pure Functions

```typescript
import { removeAccents } from "./string";

describe("removeAccents", () => {
  test("removes diacritics from string", () => {
    expect(removeAccents("café")).toBe("cafe");
    expect(removeAccents("São Paulo")).toBe("Sao Paulo");
  });
});
```

### When to Add Unit Tests

- Edge cases not covered by e2e tests.
- Complex utility functions.
- Error boundary conditions.

## Commands

```bash
# Unit/Integration tests using Vitest
pnpm test                    # Run all tests once

# Run specific test file
pnpm test -- --run src/data/posts/create-post.test.ts

# E2E tests using Playwright
pnpm e2e                     # Run all e2e tests
```