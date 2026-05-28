---
name: run-tests
description: Use this skill to run appropriate tests based on code changes, ensuring implementation quality and CI/CD efficiency.
---

# Run Tests

## When to Use This Skill

- After making code changes
- Before committing changes
- Verifying implementation quality
- CI/CD pipeline execution
- Investigating test failures

## What This Skill Does

1. Detects which app was modified (API, web, or packages).
2. Runs unit tests with `node:test` for backend code.
3. Runs integration tests with Testcontainers for backend E2E.
4. Runs Playwright tests for frontend E2E.
5. Reports coverage metrics and provides detailed failure reports.
6. Suggests fixes for failures.

## Targeted Testing Only

**IMPORTANT:** NEVER run all tests at once. Only run tests for the affected app.

### Test Commands by App

**API (NestJS Backend):**

```bash
# Unit tests with node:test
pnpm run test:api:unit
# Or from apps/api directory:
node --test src/**/*.test.ts
node --test --watch src/**/*.test.ts

# E2E tests with Testcontainers
pnpm run test:api:e2e
# Or:
nx e2e api

# All API tests
pnpm run test:api
```

**Web (Next.js Frontend):**

```bash
# E2E tests with Playwright
pnpm run test:web:e2e
# Or:
nx e2e web

# Playwright UI mode
pnpm run test:web:e2e:ui
# Or:
nx e2e web --ui

# All web tests
pnpm run test:web
```

### Testing Workflow

1. **Detect which app was modified:**
   - Check git status or file paths to determine if it's API, web, or a package.
   
2. **Run appropriate tests:**
   - API changes: `pnpm run test:api`
   - Web changes: `pnpm run test:web:e2e`
   - Package changes: Run tests for apps that import the package.

3. **Fix failures:**
   - Analyze error messages, fix the issue, and re-run the specific test.

## Test Technologies

| Layer        | Technology                         |
| ------------ | ---------------------------------- |
| Backend Unit | node:test (built-in)               |
| Backend E2E  | Testcontainers (PostgreSQL, Redis) |
| Frontend E2E | Playwright                         |

### Quality Checks

- Test coverage metrics
- Test performance analysis
- Flaky test detection
- Test quality assessment

### Common Issues

- **Testcontainers Issues:** Docker not running, port conflicts, resource limits.

### Fix Commands

```bash
# Reset test database
pnpm db:reset --env=test

# Clean Testcontainers cache
docker system prune -af

# Run tests with debug output
pnpm test --debug
```

## Output Format

1. **Test Summary** - Total tests, passed, failed, duration.
2. **Coverage Report** - Percentage by module.
3. **Failure Details** - Stack traces, error messages.
4. **Performance Metrics** - Slow tests identified.
5. **Suggestions** - How to fix failures or improve tests.

## Usage Examples

```
"Run tests for my API changes"
"Run tests for the web app"
"Verify the API tests pass"
"The tests are failing, help me fix them"
```