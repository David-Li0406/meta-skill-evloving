---
name: test
description: Run tests for the Guidr React Native application. Includes Jest commands, coverage reports, watch mode, and test structure overview with current test counts across entities, services, and screens.
---

# Test Skill

Run tests for the Guidr React Native application.

## Commands

```bash
# Run all tests
npm test

# Run tests in watch mode (useful during development)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run specific test file
npm test -- Category.test.ts

# Run tests matching pattern
npm test -- --testNamePattern="should create"
```

## Test Structure

- **Entity Tests**: `src/domain/entities/*.test.ts`
- **Service Tests**: `src/domain/services/*.test.ts`
- **Storage Tests**: `src/infrastructure/storage/*.test.ts`
- **Screen Tests**: `src/presentation/screens/*.test.tsx`

## Current Test Count

171 tests passing across:
- 8 tests: Signal (common/Signal.test.ts)
- 6 tests: DependencyInjection (common/DependencyInjection.test.ts)
- 10 tests: Category entity
- 15 tests: Guide entity
- 19 tests: Step entity
- 34 tests: Session entity
- 13 tests: CategoryService
- 21 tests: GuideService
- 24 tests: SessionService
- 12 tests: ServerConfigStorage
- 9 tests: ServerSetupScreen

## Test Output

Tests run with Jest. Output shows:
- Pass/fail status per test
- Test suite summary
- Coverage information (with --coverage flag)
- Error stack traces for failures
