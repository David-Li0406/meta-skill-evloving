---
name: test-planning
description: |
  Plan and design tests with a UX-first approach. Use this skill when: (1) Adding new features that need test coverage, (2) Fixing bugs and need to prevent regression, (3) Reviewing or improving existing test coverage, (4) The test suite failed to catch a production issue. Forces a conversation about what user experience we're protecting before writing any test code.
---

# Test Planning Skill

## Core Philosophy

**Tests exist to protect user experiences, not to hit coverage metrics.**

Before writing any test, you MUST be able to answer:
1. What user experience are we protecting?
2. How would a user know if this broke?
3. What does "working" look like from the user's perspective?

## When to Invoke This Skill

Use `/test-planning` when:
- Adding a new feature (what UX should tests verify?)
- Fixing a bug (how do we prevent this regression?)
- A production issue escaped the test suite (what did we miss?)
- Reviewing test coverage for a component or flow
- Planning a testing strategy for a new area

---

## Mandatory Conversation: UX Discovery

**Before ANY test code is written**, we must discuss:

### 1. User Experience Definition

Ask the user:
- "What is the user trying to accomplish?"
- "What does success look like from the user's perspective?"
- "What would frustrate or confuse the user if it broke?"

### 2. Failure Scenarios

Ask the user:
- "How would a user discover this is broken?"
- "What's the worst-case failure mode?"
- "Are there silent failures that users wouldn't notice immediately?"

### 3. Test Layer Selection

Determine together:
| If the answer is... | Use this test layer |
|---------------------|---------------------|
| "User can't log in" | Smoke test (blocks all others) |
| "User can't complete a workflow" | E2E test |
| "Page looks broken/unstyled" | Smoke test + visual verification |
| "Data isn't saved correctly" | Integration test |
| "Calculation is wrong" | Unit test |
| "Error message is unclear" | E2E test with assertion on message |

---

## Test Hierarchy (Pyramid + Smoke Layer)

```
        ┌─────────────┐
        │   SMOKE     │  ← Blocks everything if it fails
        │  (6 tests)  │     "Is the app alive?"
        └─────────────┘
       ┌───────────────┐
       │     E2E       │  ← User journeys
       │  (17 suites)  │     "Can users do things?"
       └───────────────┘
      ┌─────────────────┐
      │  INTEGRATION    │  ← API contracts
      │  (backend API)  │     "Do systems talk correctly?"
      └─────────────────┘
     ┌───────────────────┐
     │      UNIT         │  ← Business logic
     │  (services/utils) │     "Is the math right?"
     └───────────────────┘
```

### Smoke Tests (The Gatekeeper)

Location: `e2e/tests/smoke/app-health.spec.ts`

Smoke tests verify the app is fundamentally functional:
- Frontend loads and React mounts
- CSS loads and applies (not browser defaults)
- Backend API responds
- Login flow works end-to-end (API returns 200, token is valid)
- Authenticated requests succeed
- Unauthenticated users are redirected

**Rule:** If smoke tests fail, no other tests run. This saves CI time and immediately surfaces catastrophic failures.

---

## Reference Documentation

Read these before planning tests:

| Document | Purpose | Location |
|----------|---------|----------|
| Testing Guide | Test infrastructure, patterns, commands | [docs/TESTING.md](docs/TESTING.md) |
| E2E Testing Guide | Playwright setup, page objects, debugging | [docs/E2E_TESTING.md](docs/E2E_TESTING.md) |
| UI Test Checklist | Manual visual verification checklist | [docs/UI_TEST_CHECKLIST.md](docs/UI_TEST_CHECKLIST.md) |

---

## Test Design Principles

### 1. Test Behavior, Not Implementation

```typescript
// BAD: Tests implementation details
expect(component.state.isLoading).toBe(true);

// GOOD: Tests user-visible behavior
await expect(page.locator('text=Loading...')).toBeVisible();
```

### 2. Verify API Responses, Not Just URLs

```typescript
// BAD: Only checks if URL changed (can pass when login is broken)
await loginPage.login(username, password);
await expect(page).toHaveURL(/\/recipes/);

// GOOD: Verifies the API actually succeeded
const responsePromise = page.waitForResponse(
  resp => resp.url().includes('/users/login') && resp.status() === 200
);
await loginPage.login(username, password);
await responsePromise;
await expect(page).toHaveURL(/\/recipes/);
```

### 3. Check Computed Styles for Visual Verification

```typescript
// BAD: Only checks element exists (passes even with no CSS)
await expect(button).toBeVisible();

// GOOD: Verifies CSS actually loaded and applied
const styles = await button.evaluate(el => {
  const computed = window.getComputedStyle(el);
  return { backgroundColor: computed.backgroundColor };
});
expect(styles.backgroundColor).not.toBe('rgba(0, 0, 0, 0)');
```

### 4. Use Specific Locators

```typescript
// BAD: Ambiguous, matches multiple elements
page.locator('text=My Recipes')

// GOOD: Specific to the element type
page.locator('h1:has-text("My Recipes")')
```

---

## Test Planning Workflow

### Step 1: UX Interview (MANDATORY)

Before writing tests, ask:

```
1. What user action or experience are we testing?
   Example: "User can create a new recipe and see it in their list"

2. What does success look like?
   Example: "Recipe appears in the list with correct title, time shows in the UI"

3. What failure would a user notice?
   Example: "Recipe doesn't appear, or appears with wrong data, or page crashes"

4. What failure might be SILENT to users but critical?
   Example: "Recipe saves but isn't searchable, or isn't persisted after refresh"
```

### Step 2: Map to Test Layers

Based on the UX interview, decide:

| User Experience | Test Type | Why |
|-----------------|-----------|-----|
| "App loads at all" | Smoke | Blocks everything else |
| "User can complete workflow X" | E2E | Full stack verification |
| "API returns correct data" | Integration | Contract verification |
| "Calculation produces right result" | Unit | Isolated logic test |

### Step 3: Write Test Specification

Before coding, document:

```markdown
## Test: [Name]

**User Experience Protected:**
[What breaks if this test would have failed?]

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Test Type:** [Smoke / E2E / Integration / Unit]

**Key Assertions:**
1. [What we check]
2. [What we check]
```

### Step 4: Implement & Verify

Write the test, then verify:
- [ ] Test fails when the feature is broken (try breaking it!)
- [ ] Test passes when the feature works
- [ ] Test is not flaky (run 3x)
- [ ] Test provides clear failure message

---

## Common Test Patterns

### Pattern: Login Flow Verification

```typescript
test('login works end-to-end', async ({ page }) => {
  // 1. Intercept API response BEFORE action
  const loginResponse = page.waitForResponse(
    resp => resp.url().includes('/users/login')
  );

  // 2. Perform action
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill(password);
  await page.locator('button[type="submit"]').click();

  // 3. Verify API succeeded (not just redirect)
  const response = await loginResponse;
  expect(response.status()).toBe(200);

  // 4. Verify token is valid
  const body = await response.json();
  expect(body.access_token).toBeTruthy();

  // 5. Verify UI state reflects login
  await expect(page).toHaveURL(/\/recipes/);
});
```

### Pattern: CSS Loading Verification

```typescript
test('CSS loads correctly', async ({ page }) => {
  await page.goto('/login');

  const button = page.locator('button[type="submit"]');
  const styles = await button.evaluate(el => {
    const computed = window.getComputedStyle(el);
    return {
      backgroundColor: computed.backgroundColor,
      fontFamily: computed.fontFamily,
      borderRadius: computed.borderRadius,
    };
  });

  // Not browser defaults
  expect(styles.backgroundColor).not.toBe('rgba(0, 0, 0, 0)');
  expect(styles.fontFamily.toLowerCase()).not.toContain('times');
  expect(styles.borderRadius).not.toBe('0px');
});
```

### Pattern: Protected Route Verification

```typescript
test('unauthenticated users redirected to login', async ({ page }) => {
  // Clear any auth state
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());

  // Try to access protected route
  await page.goto('/recipes');

  // Should redirect to login
  await expect(page).toHaveURL(/\/login/);
});
```

---

## Running Tests

```bash
# Smoke tests only (quick sanity check)
npx playwright test --project=smoke

# Full E2E suite
npm run test:e2e

# Specific test file
npx playwright test e2e/tests/auth/login.spec.ts

# With visible browser (debugging)
npm run test:e2e:headed

# Interactive UI mode
npm run test:e2e:ui
```

---

## Checklist Before Merging Tests

- [ ] UX interview completed - we know what user experience we're protecting
- [ ] Test fails when feature is broken (verified by temporarily breaking it)
- [ ] Test uses appropriate layer (smoke vs E2E vs integration vs unit)
- [ ] API responses are verified, not just URL changes
- [ ] Visual elements are verified with computed styles where appropriate
- [ ] Locators are specific (no ambiguous matches)
- [ ] Test is not flaky (ran 3+ times successfully)
- [ ] Test provides clear, actionable failure message

---

## Anti-Patterns to Avoid

### 1. "Element Exists" Testing

```typescript
// WRONG: Passes even if login is completely broken
await expect(page.locator('button')).toBeVisible();
await button.click();
await expect(page).toHaveURL(/\/recipes/);  // Could redirect without auth!
```

### 2. Coverage-Driven Testing

```typescript
// WRONG: Written just to hit coverage, doesn't protect real UX
test('should render component', () => {
  render(<MyComponent />);
  expect(screen.getByTestId('container')).toBeInTheDocument();
});
```

### 3. Implementation-Coupled Tests

```typescript
// WRONG: Tests internal state, breaks on refactor
expect(component.instance().state.items).toHaveLength(3);
```

### 4. Missing API Verification

```typescript
// WRONG: Network could fail silently
await form.submit();
await expect(page).toHaveURL(/\/success/);  // What if API returned 500?
```

---

## Summary

**Before writing tests, always ask:**

1. What user experience breaks if this test would have caught it?
2. How would a real user discover this failure?
3. Am I testing behavior (good) or implementation (bad)?
4. Am I verifying the API response, not just the URL?
5. Would this test catch the CSS-not-loading or login-broken scenarios?

**Remember:** A test suite with 90% coverage that misses "the app doesn't load" is worthless. Smoke tests first, coverage second.
