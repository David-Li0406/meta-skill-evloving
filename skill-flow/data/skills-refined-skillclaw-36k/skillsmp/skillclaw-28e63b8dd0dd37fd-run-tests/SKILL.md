---
name: run-tests
description: Use this skill to run appropriate tests based on code changes, ensuring quality and efficiency in your development workflow.
---

# Skill body

## When to Use

- After making code changes
- Before committing changes
- Verifying implementation quality
- CI/CD pipeline execution
- Investigating test failures

## What This Skill Does

1. **Detects which app was modified** (API, web, or packages) using git status or file paths.
2. **Runs appropriate tests** based on the detected changes:
   - **API Changes**: Runs unit tests with `node:test` and integration tests with Testcontainers.
   - **Web Changes**: Runs E2E tests with Playwright.
   - **Package Changes**: Runs tests for apps that import the package.
3. **Reports coverage metrics** and provides detailed failure reports.
4. **Suggests fixes for failures** based on error messages.

## Testing Workflow

1. **Detect which app was modified**:
   - Check git status or file paths to determine if it's API, web, or a package.

2. **Run appropriate tests**:
   - For API changes: 
     ```bash
     pnpm run test:api
     ```
   - For Web changes:
     ```bash
     pnpm run test:web:e2e
     ```

3. **Fix failures**:
   - Analyze error messages, fix the issue, and re-run the specific test.

## Test Technologies

| Layer        | Technology                         |
| ------------ | ---------------------------------- |
| Backend Unit | node:test (built-in)              |
| Backend E2E  | Testcontainers (PostgreSQL, Redis) |
| Frontend E2E | Playwright                         |

## Important Notes

- **Targeted Testing Only**: Never run all tests at once to ensure fast feedback and CI/CD efficiency.
- **Test Standards**:
  - Unit tests: 80% coverage minimum.
  - Integration tests: Mandatory for all database operations.
  - E2E tests: Critical user paths only.

## Common Commands

- Run tests for my API changes
- Run tests for the web app
- Verify the API tests pass
- Investigate test failures

## Output Format

1. **Test Summary** - Total tests, passed, failed, duration.
2. **Coverage Report** - Percentage by module.
3. **Failure Details** - Stack traces, error messages.
4. **Performance Metrics** - Slow tests identified.
5. **Suggestions** - How to fix failures or improve tests.