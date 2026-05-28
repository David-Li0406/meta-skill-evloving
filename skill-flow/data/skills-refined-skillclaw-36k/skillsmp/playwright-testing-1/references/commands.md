# Common Commands

Quick reference for running Playwright BDD tests.

## Generate and Run

```bash
# Generate and run all tests
npx bddgen && npx playwright test

# Run specific feature
npx bddgen && npx playwright test --grep "User Login"

# Run by tag
npx bddgen && npx playwright test --grep "@smoke"

# Exclude tags
npx bddgen && npx playwright test --grep-invert "@wip"
```

## Debug Mode

```bash
# Debug mode (step through)
npx bddgen && npx playwright test --debug

# UI mode (interactive)
npx bddgen && npx playwright test --ui

# Headed browser
npx bddgen && npx playwright test --headed
```

## Reports

```bash
# Show HTML report
npx playwright show-report

# Generate with trace
npx bddgen && npx playwright test --trace on
```

## Specific Tests

```bash
# Single file
npx bddgen && npx playwright test login.feature

# Specific line
npx bddgen && npx playwright test login.feature:15

# Specific project
npx bddgen && npx playwright test --project=chromium
```

## CI Commands

```bash
# CI mode (no retries locally)
CI=true npx bddgen && npx playwright test

# With retries
npx bddgen && npx playwright test --retries=2
```
