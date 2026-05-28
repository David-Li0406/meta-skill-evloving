---
name: e2e-test-loop
description: |
  This skill should be used when the user asks for "browser tests", "playwright
  tests", "end-to-end testing", "test user flows", "E2E coverage", "integration
  tests for UI", "page object pattern", "/e2e command", or discusses automated
  browser testing. Covers the E2E test loop workflow, Playwright patterns, page
  objects, and selector strategies.
version: 1.0.0
---

# E2E Test Loop - Browser Automation Testing

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`

The E2E test loop systematically adds end-to-end tests for user flows using
Playwright, with page objects for maintainable test code.

## State Management

**Single Source of Truth**: `.claude/e2e-state-{session}.json` stores all state including
the embedded progress log. No separate progress.txt file.

**What Hook Updates:**
- Appends to state.json's `log` array automatically
- Iteration markers are optional (hook auto-detects from git)

## When to Use E2E Test Loop

- Need to test critical user flows
- Adding browser automation tests
- Ensuring features work end-to-end
- Integration testing across components

## Starting the Loop

```bash
/e2e "Cover checkout flow"                           # Basic
/e2e "Test auth" --max-iterations 5                  # Limited
/e2e "Add E2E" --test-command "npx playwright test"  # Custom command
```

## Iteration Workflow

Each iteration follows this sequence:

1. **Identify flow** - Find user flow lacking E2E coverage
2. **Create page object** - `*.e2e.page.ts` for reusable locators/actions
3. **Write ONE test** - `*.e2e.ts` using page objects
4. **Run linters** - Ensure code quality
5. **Verify passing** - Run the E2E test
6. **Run reviewers** - code-simplifier + kieran reviewer (MANDATORY)
7. **Commit** - `test(e2e): describe user flow`

## File Naming Convention

```
e2e/
├── checkout.e2e.page.ts    # Page object (locators, setup, actions)
├── checkout.e2e.ts         # Test file (concise tests)
├── auth.e2e.page.ts
└── auth.e2e.ts
```

## Playwright Patterns

### Locator Priority (Semantic First)

| Priority | Locator | Example |
|----------|---------|---------|
| 1 | `getByRole` | `page.getByRole('button', { name: 'Submit' })` |
| 2 | `getByLabel` | `page.getByLabel('Email address')` |
| 3 | `getByText` | `page.getByText('Welcome back')` |
| 4 | `getByTestId` | `page.getByTestId('submit-btn')` - last resort |

### Page Object Pattern

```typescript
// checkout.e2e.page.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  // Locators
  readonly emailInput = this.page.getByLabel('Email')
  readonly submitButton = this.page.getByRole('button', { name: 'Complete' })

  // Actions
  async fillEmail(email: string) {
    await this.emailInput.fill(email)
  }

  async submit() {
    await this.submitButton.click()
  }
}
```

```typescript
// checkout.e2e.ts
test('user can complete checkout', async ({ page }) => {
  const checkout = new CheckoutPage(page)
  await checkout.fillEmail('user@example.com')
  await checkout.submit()
  await expect(page.getByText('Order confirmed')).toBeVisible()
})
```

### Waiting Patterns

```typescript
// Auto-waiting (built into actions)
await page.getByRole('button').click()  // Waits until clickable

// Explicit wait for state
await expect(page.getByText('Loaded')).toBeVisible()

// Wait for network
await page.waitForResponse('**/api/data')
```

## Quality Standards

- **ONE test per iteration** - Focused, reviewable commits
- **Test user-visible behavior** - Not implementation details
- **Tests must be independent** - No shared state between tests
- **Use page objects** - Keep test files concise

## Completion

Output when critical user flows are covered:

```xml
<promise>E2E COMPLETE</promise>
```

Only output when genuinely complete - do not exit prematurely.

## Task Integration (Optional)

### On Flow Identification

For each user flow to test:
```
TaskCreate({
  subject: "E2E: {flow_name}",
  description: "Test: {flow_description}",
  activeForm: "Testing {flow_name} flow",
  metadata: { loop: "e2e", flow_name: "{name}" }
})
```

Set `blockedBy` for dependent flows (checkout depends on login).

### On Flow Test Complete

`TaskUpdate(task_id, status: "completed")`

## Command Reference

```bash
/e2e "prompt"                                      # Basic loop
/e2e "prompt" --max-iterations 10                  # Limit iterations
/e2e "prompt" --test-command "npx playwright test" # Custom command
/cancel-e2e                                        # Cancel loop
```

## Additional Resources

### Reference Files

- **`references/playwright-patterns.md`** - Advanced Playwright patterns
