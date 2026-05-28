---
name: test
description: Run Playwright tests with various options (specific file, all UI tests, debug mode, headed browser, tagged tests). Use when user asks to run tests, execute tests, test something, or debug tests.
allowed-tools: Bash(npx:*), Bash(playwright:*), Read, Grep
---

# Test Execution

## Usage Patterns

### 1. Run Specific Test File
```bash
# Single spec file
npx playwright test tests/ui/basket.spec.ts

# With specific test name
npx playwright test tests/ui/basket.spec.ts -g "Remove product from cart"
```

### 2. Run All UI Tests
```bash
# All tests in ui directory
npx playwright test tests/ui/

# All tests
npx playwright test
```

### 3. Run Tagged Tests
```bash
# Run P1 priority tests
npx playwright test --grep @P1

# Run P2 priority tests
npx playwright test --grep @P2
```

### 4. Debug Mode
```bash
# Debug specific test (opens Playwright Inspector)
npx playwright test tests/ui/basket.spec.ts --debug

# Debug with specific test name
npx playwright test tests/ui/basket.spec.ts -g "Add product" --debug
```

### 5. Headed Mode (See Browser)
```bash
# Run with visible browser
npx playwright test tests/ui/basket.spec.ts --headed

# Slow down execution for visibility
npx playwright test tests/ui/basket.spec.ts --headed --slow-mo=1000
```

### 6. Run on Specific Browser
```bash
# Chromium only
npx playwright test --project=chromium

# Run setup manually
npx playwright test --project=setup
```

### 7. Update Snapshots
```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update specific test snapshots
npx playwright test tests/ui/basket.spec.ts --update-snapshots
```

## Common Options

| Option | Description |
|--------|-------------|
| `--headed` | Show browser window |
| `--debug` | Open Playwright Inspector |
| `--ui` | Open Playwright UI mode (interactive) |
| `-g "pattern"` | Run tests matching pattern |
| `--grep @P1` | Run tests with @P1 tag |
| `--project=chromium` | Run on specific browser |
| `--workers=1` | Run tests serially (for debugging) |
| `--reporter=list` | Use list reporter (verbose) |
| `--trace on` | Record trace for all tests |

## Interactive UI Mode
```bash
# Open Playwright UI (best for development)
npx playwright test --ui
```

## After Test Execution

1. **Check results** in console output
2. **If failures occur:**
   - Read error messages
   - Check screenshots in `playwright-report/`
   - Offer to open HTML report: `npx playwright show-report`
3. **Summarize:** passed/failed/skipped counts

## Troubleshooting

**If auth setup fails:**
```bash
# Run setup separately
npx playwright test tests/auth.setup.ts
```

**If parallel execution causes issues:**
```bash
# Run serially
npx playwright test --workers=1
```

**Clear test artifacts:**
```bash
# Remove auth files
rm -rf .auth/

# Remove reports
rm -rf playwright-report/ test-results/
```

## Best Practices

- Use `--headed` for visual debugging
- Use `--debug` to step through test actions
- Use `--ui` for interactive test development
- Run with `--workers=1` when debugging race conditions
- Check HTML report after failures for detailed diagnostics
