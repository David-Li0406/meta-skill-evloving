---
name: run-tests
description: Run appropriate tests based on changes using node:test, Testcontainers, and Playwright
allowed-tools: [Bash, Grep, Glob]
---

# Run Tests

When to use this skill:

- After making code changes
- Before committing changes
- Verifying implementation quality
- CI/CD pipeline execution

What this skill does:

1. Detects which app was modified (api, web, or packages)
2. Runs unit tests with node:test for backend code
3. Runs integration tests with Testcontainers for backend E2E
4. Runs Playwright tests for frontend E2E
5. Reports coverage metrics
6. Suggests fixes for failures

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
   - Check git status or file paths
   - Determine if it's API, web, or a package

2. **Run appropriate tests:**
   - API changes: `pnpm run test:api`
   - Web changes: `pnpm run test:web:e2e`
   - Package changes: Run tests for apps that import the package

3. **Fix failures:**
   - Analyze error messages
   - Fix the issue
   - Re-run the specific test

### Test Technologies

| Layer        | Technology                         |
| ------------ | ---------------------------------- |
| Backend Unit | node:test (built-in)               |
| Backend E2E  | Testcontainers (PostgreSQL, Redis) |
| Frontend E2E | Playwright                         |

### NO "Test All" Script

There is intentionally NO script that runs all tests. This ensures:

- Fast feedback (only run relevant tests)
- CI/CD efficiency (test affected apps only)
- Clear ownership (each app has its own tests)

Usage:

```
"Run tests for my API changes"
"Run tests for the web app"
"Verify the API tests pass"
```
