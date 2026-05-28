---
name: test-driven-development
description: TDD workflows, Red-Green-Refactor, and testing frameworks (PHPUnit, Jest).
---

# Test-Driven Development (TDD)

## When to use this skill
- Starting a new complex feature.
- Fixing a bug (write test to reproduce first).
- Refactoring critical paths.

## 1. The Cycle (Red-Green-Refactor)
1.  **Red**: Write a failing test that defines the desired behavior.
2.  **Green**: Write the *minimum* code to pass the test.
3.  **Refactor**: Clean up the code while keeping tests green.

## 2. Tools & Config
- **PHP**: Use Pest or PHPUnit.
  - `php artisan test` (Laravel).
- **JS/TS**: Use Jest or Vitest.
  - `npm test`.

## 3. Best Practices
- **Arrangement**: Arrange-Act-Assert structure in every test.
- **Naming**: `it_should_validate_email` or `test_email_validation`.
- **Speed**: Unit tests must run in milliseconds. Mock external services (Stripe, DB) if they are slow.
