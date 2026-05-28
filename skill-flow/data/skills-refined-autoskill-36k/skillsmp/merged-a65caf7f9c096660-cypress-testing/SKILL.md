---
name: cypress-testing
description: Use this skill for implementing reliable end-to-end and component testing in web applications using Cypress, focusing on best practices for selectors, waits, and network control.
---

# Cypress Testing Best Practices

You are an expert in Cypress end-to-end and component testing.

## Overview

Cypress runs browser automation with first-class network control, time-travel debugging, and a strong local dev workflow. Use it for critical path E2E tests and for component tests when browser-level rendering matters.

## Quick Start

### Install and Open

```bash
npm i -D cypress
npx cypress open
```

### Minimal Spec

```ts
// cypress/e2e/health.cy.ts
describe("health", () => {
  it("loads", () => {
    cy.visit("/");
    cy.contains("Hello").should("be.visible");
  });
});
```

## Core Principles

### Test Structure
- Use descriptive test names that clearly explain expected behavior.
- Organize tests by feature or user flow.
- Keep tests focused on critical user paths.
- Follow the Given-When-Then pattern for clarity.

### Stable Selectors
- Prefer `data-testid` or `data-cy` attributes for test selectors.
- Avoid brittle selectors like CSS classes or tag hierarchies.

```html
<button data-testid="save-user">Save</button>
```

```ts
cy.get('[data-testid="save-user"]').click();
```

### Deterministic Waiting
- Wait on app-visible conditions or network aliases rather than using fixed sleeps.

```ts
cy.intercept("GET", "/api/users/*").as("getUser");
cy.visit("/users/1");
cy.wait("@getUser");
cy.get('[data-testid="user-email"]').should("not.be.empty");
```

### Network Control
- Use `cy.intercept()` to mock or wait for network requests.

```ts
cy.intercept("GET", "/api/users/1", {
  statusCode: 200,
  body: { id: "1", email: "a@example.com" },
}).as("getUser");
```

### Authentication Strategies
- Prefer `cy.session` to cache login for speed and stability.

```ts
// cypress/support/commands.ts
Cypress.Commands.add("login", () => {
  cy.session("user", () => {
    cy.request("POST", "/api/auth/login", {
      email: "test@example.com",
      password: "password",
    });
  });
});
```

### Test Isolation
- Each test should be independent and repeatable.
- Use `beforeEach` hooks for setup.

### Anti-Patterns to Avoid
- Using `cy.wait(5000)` with arbitrary timeouts.
- Testing third-party sites you don't control.
- Writing overly long tests that test multiple features.
- Relying on the state from previous tests.

## Component Testing

Run component tests to validate UI behavior in isolation while keeping browser rendering.

```bash
npx cypress open --component
```

```ts
// cypress/component/Button.cy.tsx
import React from "react";
import Button from "../../src/Button";

describe("<Button />", () => {
  it("clicks", () => {
    cy.mount(<Button onClick={cy.stub().as("onClick")}>Save</Button>);
    cy.contains("Save").click();
    cy.get("@onClick").should("have.been.calledOnce");
  });
});
```

## CI Patterns

### Artifacts (Videos/Screenshots)
Store artifacts for failed runs and keep videos optional to reduce storage.

```ts
// cypress.config.ts
import { defineConfig } from "cypress";

export default defineConfig({
  video: false,
  screenshotOnRunFailure: true,
  retries: { runMode: 2, openMode: 0 },
});
```

### Parallelization
Parallelize long E2E suites via Cypress Cloud when runtime dominates feedback loops.

## Troubleshooting

### Flaky Click or Element Not Found
- Add a `data-testid` hook for the element.
- Assert visibility before interaction (`should("be.visible")`).
- Wait on network alias for the data that renders the element.

### Tests Fail Only in CI
- Increase run-mode retries and record screenshots on failure.
- Verify viewport and baseUrl config match CI environment.
- Eliminate reliance on local-only seed data; create data via API calls.

## Resources
- Cypress docs: https://docs.cypress.io/
- Best practices: https://docs.cypress.io/guides/references/best-practices