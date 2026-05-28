---
name: cypress-testing-best-practices
description: Use this skill when you need to write reliable end-to-end and component tests for web applications using Cypress, focusing on best practices for selectors, waits, and test structure.
---

# Cypress Testing Best Practices

You are an expert in Cypress end-to-end and component testing.

## Overview

Cypress runs browser automation with first-class network control, time-travel debugging, and a strong local dev workflow. Use it for critical path E2E tests and for component tests when browser-level rendering matters.

## Quick Start

### Install and Open Cypress

```bash
npm i -D cypress
npx cypress open
```

### Minimal Spec Example

```typescript
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

### Selecting Elements
- Prefer `data-testid` or `data-cy` attributes for test selectors.
- Avoid brittle selectors like CSS classes or tag hierarchies.

```javascript
// Recommended
cy.get('[data-testid="submit-button"]').click();
cy.contains('Submit').click();

// Avoid
cy.get('.btn-primary').click();
```

### Commands and Assertions
- Chain commands fluently for readability.
- Use built-in retry-ability; avoid explicit waits.
- Prefer `.should()` assertions over `.then()` for automatic retries.
- Use `.within()` to scope commands to a specific element.

### Handling Async Operations
- Use `cy.intercept()` to mock or wait for network requests.
- Avoid mixing Cypress commands with async/await.

```javascript
cy.intercept('GET', '/api/users').as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').should('be.visible');
```

### Authentication Strategies
- Prefer `cy.session()` to cache login for speed and stability.

```javascript
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type(email);
    cy.get('[data-testid="password"]').type(password);
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

### Test Isolation
- Each test should be independent and repeatable.
- Use `beforeEach` hooks for setup.

### Anti-Patterns to Avoid
- Avoid using `cy.wait(5000)` with arbitrary timeouts.
- Do not test third-party sites you don't control.
- Avoid writing overly long tests that test multiple features.
- Do not rely on the state from previous tests.