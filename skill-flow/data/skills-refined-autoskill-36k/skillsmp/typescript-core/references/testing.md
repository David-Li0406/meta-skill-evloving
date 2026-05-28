# Testing Guidelines

Testing is crucial to ensure our TypeScript code works as intended and to prevent regressions. We use Vitest (or Jest in legacy cases) as our test runner, along with appropriate libraries for the environment (e.g., React Testing Library for React components, and MSW for API calls).

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Tools & Stack](#tools--stack)
- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [End-to-End (E2E) Testing](#end-to-end-e2e-testing)
- [Testing Best Practices](#testing-best-practices)
- [What Not to Test](#what-not-to-test)

## Testing Philosophy

- **Test Behavior, Not Implementation**: Write tests to verify what the code should do (outputs, UI rendered, side effects observed), not how it does it. Avoid testing internal function calls or private state.
- **Fast, Automated, Frequent**: Tests should be runnable quickly (ideally in watch mode during development and in CI). Aim to run the unit test suite on each commit or push.
- **Deterministic**: Tests must produce the same results every run. Avoid relying on external services or non-deterministic inputs (time can be controlled via faking timers, random values via seeding, etc.).
- **Isolated Units, Realistic Integration**: Unit tests isolate a single function or component (no external calls). Integration tests can use a more realistic environment (database, network stubs) to ensure parts work together.
- **BDD Mindset**: Think in terms of scenarios: given some setup, when an action happens, then expect a result. This helps write clear, descriptive tests (potentially using BDD libraries or simply structuring tests with arrange-act-assert sections).

## Tools & Stack

**Testing frameworks**:

- **Vitest** – our default unit test runner (fast, TS-native, Vite-compatible). It supports JSDOM for component testing and is very similar to Jest.
- **React Testing Library (RTL)** – for React components. Encourages testing UI by interacting as a user (queries by text, clicking, etc.), not testing implementation details.
- **MSW (Mock Service Worker)** – for simulating API calls in tests. MSW intercepts `fetch`/`XHR` and returns mocked responses, allowing integration-like testing without real network calls.
- **Playwright or Cypress** – for end-to-end tests if applicable (browser automation, not covered deeply here, but mention for completeness).
- **Supertest** (for Node/Express) – for simulating HTTP calls to our API in integration tests.

**Coverage**: We aim for ~80%+ code coverage, but value meaningful coverage over number. Critical logic should be thoroughly tested.

## Unit Testing

Unit tests target a single function, module, or component in isolation:

- For pure functions, this is straightforward: call function with various inputs, assert outputs.
- For functions with dependencies, use dependency injection or module-mocking to pass in fake dependencies. (Vitest can stub imports easily via `vi.mock()`).
- For React components:
  - Use RTL’s `render(<MyComponent props={...}/>)` in a test. Assert on the rendered output or behavior (query text, simulate user events using `userEvent`).
  - Avoid reaching into component internals (state, or DOM structure not visible to user). Test what a user would perceive: text on screen, button enabled/disabled, etc..
  - Each test should ideally cover one logical scenario or edge case.

**Example (function)**:

```ts
// Function to test
function toSlug(input: string): string { ... }

// Test
import { describe, it, expect } from 'vitest';
import { toSlug } from './string-utils';

describe('toSlug', () => {
  it('converts spaces to hyphens and lowercases', () => {
    expect(toSlug('Hello World')).toBe('hello-world');
  });
  it('trims and removes special chars', () => {
    expect(toSlug(' Test !!! ')).toBe('test');
  });
});
```

**Example (React)**:

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm';

test('submits user data when form is filled and submitted', async () => {
  render(<LoginForm onSubmit={jest.fn()} />);
  await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  userEvent.click(screen.getByRole('button', { name: /login/i }));

  expect(screen.queryByText(/logging in/i)).toBeInTheDocument();
});
```

This is testing the visible behavior: after clicking login, maybe a loading message appears, etc.

## Integration Testing

Integration tests cover multiple units interacting:

- Test an API endpoint by calling it (e.g., using Supertest to hit an Express route, with a test database or an in-memory DB).
- Test a complex React component that makes network calls by rendering it and using MSW to mock network responses. Verify that after the component mounts, it calls the API and correctly renders the results (using MSW to supply the response).
- Use Vitest or Jest to spin up needed background (perhaps a SQLite memory DB, or a fake Redis, etc.) if your code interacts with those.

**Key**: don’t call the real production services. Instead:

- Use a test database or transactions that get rolled back.
- Use MSW for external HTTP calls (or `nock`/`axios-mock` if MSW isn't applicable).
- Use Node’s ability to simulate environment (e.g., set `process.env.TEST=true` to alter certain behaviors, like shorter timeouts).

**Example: Testing an Express route**:

```ts
import request from 'supertest';
import app from '../src/server'; // Express app

test('GET /api/items returns list of items', async () => {
  // Insert some known data in test DB (or mock DB calls)
  await db.item.create({ name: 'TestItem' });
  const res = await request(app).get('/api/items');
  expect(res.status).toBe(200);
  expect(res.body).toEqual(
    expect.arrayContaining([ expect.objectContaining({ name: 'TestItem' }) ])
  );
});
```

This hits the real routing and checks integration with DB.

## End-to-End (E2E) Testing

End-to-end tests simulate user interaction in a fully running application (frontend and backend together):

- These tests are slower and run in a real browser or headless browser environment.
- We might use Playwright to launch the app (possibly against a test server or a deployed staging environment) and then script a user journey: e.g., "open page, login, see dashboard".
- Because our focus is on TypeScript code and integration, we typically keep E2E tests limited (just covering critical flows), relying more on unit/integration for most coverage.

If E2E tests are included:

- They should run in CI on merge to `main` or on release (not every commit, due to time).
- Use test accounts or seeded data.
- Clean up side effects (e.g. if creating a record via UI, ensure it’s deleted or use a dev environment that resets).

## Testing Best Practices

### Organizing Test Files

- Co-locate tests with implementation when possible, naming them `*.test.ts` or `*.spec.ts`. This makes it easy to find tests and encourages keeping tests updated with code changes.
- Alternatively, use a parallel structure under `src/__tests__/` mirroring the source files if co-location gets messy.
- For React, also consider Storybook interaction tests (which run in browser) for visual or behavioral tests of components in isolation, but that’s supplementary.

### Before/After Hooks

Use `beforeAll`, `beforeEach`, `afterEach`, `afterAll` for repetitive setup/teardown:

- Example: start a test server once before all tests in a file, close it after.
- Clean database or reset state before each test to avoid leakage between tests.

### Factories & Test Data

Generate test data using factory functions or libraries (e.g., `faker` for random but realistic values).

- This avoids repeating object literals in many tests and makes it easy to adjust if your model changes.
- Ensure randomness is controlled or at least not affecting the logic (random user name is fine; random number of items could cause flaky tests if logic not expecting extreme values, so be careful).

### Focus on Edge Cases

Write tests not only for the “happy path” but also:

- Empty inputs (e.g., empty array to a function).
- Boundary values (e.g., string at max length allowed).
- Error conditions (simulate a function throwing or API returning error and ensure our code handles it gracefully).

### Use TypeScript in Tests

Our tests are also TypeScript, so use that to your advantage:

- Define types for test data if complex.
- Leverage the compiler to catch wrong usage of tested APIs – e.g., if a function signature changes, tests using it will fail to compile, alerting you to update tests.

### Continuous Integration

All tests must pass in CI. Flaky tests are not acceptable – if a test is flaky, mark it as `skipped` and fix it ASAP.

- Run tests with `--runInBand` or similar if concurrency causes issues (or use proper test isolation).
- Use coverage reports to identify untested code.

## What Not to Test

- **Library Code**: Don’t test internal behavior of third-party libraries (e.g., that React `useState` works – assume library code works as documented).
- **Styling/CSS**: Don’t test exact CSS class names or styles (those can change without affecting behavior). Instead, test visual outcomes or presence of elements.
- **Trivial Code**: Simple getters/setters or value-object constructors that don’t contain logic don’t need dedicated tests (they’ll be exercised via other tests).
- **Console Output**: If using our logging, you generally don’t test that “`logger.info` was called” unless critical for logic. Focus on state changes, returns, UI output rather than logging side effects.
- **Timing Specifics**: Avoid tests that rely on real timers (use fake timers for waiting, or better yet design code to be testable without real time passing).

By following these guidelines, our test suite will be fast, reliable, and provide confidence in our codebase’s correctness. Remember, a well-tested codebase is easier to refactor and maintain, enabling us to move quickly with fewer bugs.
