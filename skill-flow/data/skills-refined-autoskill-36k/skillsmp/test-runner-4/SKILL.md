---
name: test-runner
description: Run appropriate tests based on changes using node:test, Testcontainers, and Playwright
allowed-tools:
  - Bash
  - Grep
  - Read
---

# Test Runner

## Purpose

Run appropriate tests based on changes and ensure code quality through comprehensive testing.

## When to Invoke

- After making code changes
- Before committing changes
- Verifying implementation quality
- CI/CD pipeline execution
- Investigating test failures

## Capabilities

### Test Detection

- Detects affected apps using Nx affected detection
- Identifies which tests to run based on changes
- Determines test type (unit, integration, E2E)

### Test Execution

- Runs unit tests (Jest)
- Runs integration tests with Jest + Testcontainers
- Runs E2E tests (Jest + Testcontainers for backend, Playwright for frontend)
- Runs tests in parallel for speed
- Provides detailed failure reports

### Quality Checks

- Test coverage metrics
- Test performance analysis
- Flaky test detection
- Test quality assessment

### Testcontainers Support

- Spins up PostgreSQL container for integration tests
- Spins up Redis container when needed
- Spins up RabbitMQ container when needed
- Cleans up containers after tests

## How to Use

### Run All Tests

```
"Run all tests"
```

### Run Affected Tests

```
"Run tests for my changes"
"Run affected tests"
```

### Run Specific Test Type

```
"Run unit tests for the api app"
"Run integration tests for the auth module"
"Run E2E tests"
```

### Investigate Failures

```
"The tests are failing, help me fix them"
```

## Test Types

### Unit Tests

- Fast execution
- No external dependencies
- Mock external services
- Focus on business logic

### Integration Tests

- Testcontainers for real databases
- Test repository implementations
- Test CQRS handlers
- Test API endpoints

### E2E Tests

- Playwright for frontend
- Test user flows
- Test authentication
- Test critical paths

## Test Standards

- **Unit tests**: 80% coverage minimum
- **Integration tests**: Mandatory for all database operations
- **E2E tests**: Critical user paths only
- **Testcontainers**: Required for all integration tests

## Output Format

1. **Test Summary** - Total tests, passed, failed, duration
2. **Coverage Report** - Percentage by module
3. **Failure Details** - Stack traces, error messages
4. **Performance Metrics** - Slow tests identified
5. **Suggestions** - How to fix failures or improve tests

## Common Issues

### Testcontainers Issues

- Docker not running
- Port conflicts
- Resource limits

### Fix Commands

```bash
# Reset test database
pnpm db:reset --env=test

# Clean Testcontainers cache
docker system prune -af

# Run tests with debug output
pnpm test --debug
```
