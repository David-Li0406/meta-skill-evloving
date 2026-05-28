# Profile Tailors E2E Testing Reference

Project-specific patterns for CVIX webapp E2E testing.

## Environment Variables

| Variable                 | Description             | Default              |
|--------------------------|-------------------------|----------------------|
| `USE_HAR`                | Enable HAR replay mode  | `false` (auto in CI) |
| `RECORD_HAR`             | Record new HAR files    | `false`              |
| `CI`                     | CI environment flag     | `false`              |
| `FORCE_HTTP`             | Force HTTP (skip HTTPS) | `false`              |
| `PLAYWRIGHT_BACKEND_URL` | Backend URL override    | Auto-detected        |

## Test User Credentials

```typescript
// From helpers.ts
export const TEST_USERS = {
    existingUser: {
        email: "john.doe@profiletailors.com",
        password: "S3cr3tP@ssw0rd*123",
    },
    newUser: {
        email: "jane.doe@profiletailors.com",
        password: "S3cr3tP@ssw0rd*123",
    },
};
```

## API Content Type

All API mocks use: `application/vnd.api.v1+json`

## Test ID Convention

Format: `{FEATURE}-E2E-{NUMBER}`

Examples:

- `LOGIN-E2E-001` - Login success flow
- `REGISTER-E2E-002` - Registration with existing email
- `LOGOUT-E2E-001` - Logout flow

## Project Structure

```markdown
e2e/
├── base-page.ts # Common page methods
├── helpers.ts # Mocking, data generation
├── login/
│ ├── login-page.ts # LoginPage class
│ ├── login.spec.ts # Login tests
│ └── login.md # Test documentation
├── register/
│ ├── register-page.ts # RegisterPage class
│ ├── register.spec.ts # Register tests
│ └── register.md # Test documentation
├── logout/
│ ├── home-page.ts # HomePage class (for logout)
│ ├── logout.spec.ts # Logout tests
│ └── logout.md # Test documentation
└── fixtures/
└── harFixture.ts # HAR replay (experimental)
```

## Running Tests

```bash
# All E2E tests
pnpm test:e2e

# Specific feature
pnpm test:e2e e2e/login/

# By tag
npx playwright test --grep "@critical"
npx playwright test --grep "@login"

# With UI
pnpm test:e2e:headed
npx playwright test --ui
```

## API Mocking Strategy

This project uses **manual API mocking** via Playwright's `page.route()`:

1. **Why manual over HAR?**
    - More reliable (no XSRF token matching issues)
    - Easier to customize per test scenario
    - Simpler to debug

2. **Setup functions:**
    - `setupBasicMocks(page)` - Health check + unauthenticated account
    - `setupLoginMocks(page)` - Full login flow mocking
    - `setupRegisterMocks(page)` - Full registration flow mocking

3. **Error mocking:**
    - `mockApiErrors.invalidCredentials(page)` - 401
    - `mockApiErrors.rateLimitExceeded(page)` - 429
    - `mockApiErrors.networkError(page)` - Connection failed
    - `mockApiErrors.emailAlreadyExists(page)` - 409

## Authentication Flow

```markdown
1. Login: POST /api/auth/login → Returns accessToken + user
2. Account: GET /api/account → Returns user profile (or 401)
3. Workspace: GET /api/workspace → Returns user workspaces
4. Refresh: POST /api/auth/token/refresh → Returns new accessToken
```

## Key Selectors

| Element        | Selector Strategy                                     |
|----------------|-------------------------------------------------------|
| Email input    | `getByLabel(/email/i)`                                |
| Password input | `getByLabel(/password/i)`                             |
| Sign in button | `getByRole("button", {name: /sign in/i})`             |
| Sign up button | `getByRole("button", {name: /create account/i})`      |
| Register link  | `getByRole("link", {name: /sign up or register/i})`   |
| Login link     | `getByRole("link", {name: /log in or sign in/i})`     |
| Logout button  | `getByRole("button", {name: /log out or sign out/i})` |
