---
name: testing-patterns
description: Testing strategies and best practices
status: ✅ Working
last-validated: 2025-12-15
---

# Testing Patterns

## Purpose
Provides guidance on testing strategies, patterns, and best practices for comprehensive test coverage.

## Testing Pyramid
1. **Unit Tests** (70%) - Test individual functions/components
2. **Integration Tests** (20%) - Test component interactions
3. **E2E Tests** (10%) - Test user workflows

## Unit Testing
- Test behavior, not implementation
- One assertion per test (when possible)
- Use descriptive test names
- Arrange-Act-Assert pattern
- Mock external dependencies

## Integration Testing
- Test component interactions
- Verify data flow between modules
- Test API contracts
- Database integration tests

## E2E Testing
- Test critical user journeys
- Cover happy paths and edge cases
- Keep E2E tests minimal and stable
- Run in CI/CD pipeline

## Best Practices
- Write tests first (TDD)
- Aim for high coverage (>80%)
- Keep tests fast and independent
- Use fixtures and factories for test data
- Test error cases and edge cases

## Common Patterns
- AAA (Arrange-Act-Assert)
- Given-When-Then (BDD)
- Page Object Model (E2E)
- Test Data Builders
- Mock vs Stub vs Fake
