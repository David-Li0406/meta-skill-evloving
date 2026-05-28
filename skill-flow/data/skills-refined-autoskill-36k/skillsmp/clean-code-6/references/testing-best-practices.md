# Testing Best Practices (Vitest + Playwright + Maestro)

## Unit & Integration Tests (Vitest + Testing Library)

### Test Principles

- **Test Behavior**: Focus on what code does, not how
- **Clear Names**: Descriptive names explaining what's tested and expected outcome
- **Independent**: Each test runs independently without shared state
- **AAA Pattern**: Arrange, Act, Assert
- **One Concept**: Test one behavior per test
- **User Workflows**: Validate from user's perspective

### Test Structure

```typescript
describe("UserCard", () => {
  it("displays the user name and email", () => {
    // Arrange
    const user = { name: "John", email: "john@example.com" };

    // Act
    render(<UserCard user={user} />);

    // Assert
    expect(screen.getByText("John")).toBeVisible();
    expect(screen.getByText("john@example.com")).toBeVisible();
  });
});
```

### Rules

- **Assertions in Blocks**: Write assertions inside `it()` blocks only
- **Async Tests**: Use async/await instead of done callbacks
- **No .only/.skip**: Never commit tests with `.only` or `.skip`
- **Flat Structure**: Keep test suites flat - avoid excessive `describe` nesting

### Testing Library APIs

- Use `render` for components, `renderHook` for hooks
- Keep unit tests fast (milliseconds)
- Apply same code quality standards to test code

### Query Priority (Most Accessible First)

1. `getByRole` - buttons, links, headings
2. `getByLabelText` - form inputs
3. `getByText` - non-interactive elements
4. `getByTestId` - last resort only

### Interactions

- **User Events**: Use `userEvent` over `fireEvent`
- **Visibility**: Use `toBeVisible()` for displayed UI

```typescript
import { userEvent } from "@testing-library/user-event";

it("submits the form on button click", async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<Form onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText("Email"), "test@example.com");
  await user.click(screen.getByRole("button", { name: "Submit" }));

  expect(onSubmit).toHaveBeenCalledWith({ email: "test@example.com" });
});
```

### Mocking

- **Edge Cases**: Include boundary conditions, empty inputs, null values, errors
- **External Dependencies**: Mock databases, APIs, file systems for unit tests
- **Avoid Internal Mocking**: Don't mock sub-components in integration tests

### Coverage

- **Minimum Threshold**: 80% baseline
- **Critical Paths**: 90%+ on business logic, auth, payments
- **Quality Over Quantity**: Focus on behavior and edge cases
- **Track Trends**: Monitor to catch regressions
- **Exclude**: Don't count generated code, test files, config

---

## E2E Tests - Playwright (Web)

### Test Structure & Style

- **User-centric scenarios**: Describe behavior from user's point of view
- **Accessible selectors first**: `getByRole` → `getByLabelText` → `getByText` → `getByTestId`
- **Short, intention-revealing tests**: Follow Arrange–Act–Assert
- **Use `test.step`**: When it clarifies flow
- **Isolated specs**: No cross-test state; each spec is order-independent

### Assertions & Interactions

```typescript
import { test, expect } from "@playwright/test";

test("user can log in", async ({ page }) => {
  await test.step("navigate to login", async () => {
    await page.goto("/login");
  });

  await test.step("fill credentials", async () => {
    await page.getByLabel("Email").fill("user@example.com");
    await page.getByLabel("Password").fill("password123");
  });

  await test.step("submit and verify redirect", async () => {
    await page.getByRole("button", { name: "Sign in" }).click();
    await expect(page).toHaveURL("/dashboard");
  });
});
```

### Best Practices

- **No sleeps**: Never use `waitForTimeout`; rely on auto-wait
- **Assert end state**: Always verify with `expect(...)`
- **Stable locators**: Avoid brittle CSS/XPath/`nth-of-type`
- **Use `locator()`**: With `{ has, hasText }` for filtering
- **Don't interact with hidden elements**

### Assertions to Prefer

| Assertion         | Use Case                   |
| ----------------- | -------------------------- |
| `toBeVisible`     | Element is shown           |
| `toHaveText`      | Text content matches       |
| `toHaveURL`       | Navigation completed       |
| `toBeEnabled`     | Button/input is active     |
| `toBeChecked`     | Checkbox/radio is selected |
| `toHaveAttribute` | Attribute value matches    |

### Non-DOM Conditions

Use `expect.poll` for conditions not tied to DOM:

```typescript
await expect
  .poll(async () => {
    const response = await fetch("/api/status");
    return response.json();
  })
  .toEqual({ status: "ready" });
```

### Configuration

- **`webServer`**: Configure server start in config, not specs
- **`use.baseURL`**: Navigate with `page.goto('/')`
- **Retries**: Keep low; enable tracing on first retry
- **Headless**: CI runs headless
- **Viewport**: Standard `1280x720`
- **TypeScript**: Write tests in TypeScript

### Database & Auth

- Use Prisma for database operations
- Use auth utilities for authentication testing

---

## E2E Tests - Maestro (Mobile)

### Test Structure & Style

- **User journeys**: Focus each flow on a single feature
- **testID selectors first**: Always use `testID` attributes on React Native components
- **Reusable flows**: Extract common sequences into shared flows
- **Compose with `runFlow`**
- **Isolated flows**: `launchApp: clearState: true` to start clean
- **Platform handling**: Use `when: platform:` for iOS/Android differences

### Example Flow

```yaml
appId: com.example.app
---
- launchApp:
    clearState: true

- tapOn:
    id: "login-button"

- inputText:
    id: "email-input"
    text: "user@example.com"

- inputText:
    id: "password-input"
    text: "password123"

- tapOn:
    id: "submit-button"

- assertVisible:
    id: "dashboard-header"
```

### Best Practices

- **No unnecessary waits**: Trust Maestro's auto-wait
- **Use `waitForAnimationToEnd`**: When animations need to complete
- **Stable selectors**: Prefer `testID` over text that changes with translations
- **Avoid `point(x, y)` coordinates**
- **Flexible matching**: Use regex patterns in assertions
- **Meaningful messages**: Add assertion messages

### Parametrization

```yaml
env:
  EMAIL: user@example.com
  PASSWORD: password123
---
- inputText:
    id: "email-input"
    text: ${EMAIL}
```

### Configuration & Project Structure

```
.maestro/
├── common/          # Shared flows (login, navigation)
├── features/        # Feature-specific tests
├── smoke/           # Smoke tests
└── config.yaml      # Global configuration
```

### Tagging Strategy

- Tag by purpose: `smoke`, `regression`
- Tag by context: `pr`, `nightly`
- Use `includeTags`/`excludeTags` to filter

### Development Tools

- `maestro studio`: Interactive debugging
- `maestro record`: Capture test executions

### CI Integration

- GitHub Actions: `mobile-dev-inc/action-maestro-cloud`
- EAS workflows in `.eas/workflows/`
- Dedicated EAS profile for E2E
- APK for Android, simulator for iOS
- Test against development builds

---

## Anti-Patterns

| Pattern                 | Problem             | Solution                    |
| ----------------------- | ------------------- | --------------------------- |
| Testing implementation  | Brittle tests       | Test behavior               |
| Shared test state       | Flaky tests         | Isolate each test           |
| `waitForTimeout`        | Slow, unreliable    | Auto-wait + assertions      |
| Text-based selectors    | Breaks with i18n    | Use testID/accessible roles |
| `.only`/`.skip` commits | Skipped tests in CI | Remove before commit        |
| Mocking internals       | False confidence    | Integration tests           |
| No error cases          | Missed edge cases   | Test error paths            |
