# Step 6: CI Integration

**Duration**: ~1 minute
**Purpose**: Update GitHub Actions workflows and Playwright configuration.

---

## Actions

### 1. Analyze Current CI Configuration

Check existing workflow files:

```bash
ls .github/workflows/
cat .github/workflows/ci.yml
```

### 2. Determine If New Playwright Project Needed

**Create new project when**:
- Tests require different worker count
- Tests have unique dependencies
- Tests need separate retry configuration

**Use existing project when**:
- Tests fit existing category (e.g., `chrome-serial`)
- No special configuration needed

### 3. Update Playwright Configuration

If new project needed, add to `playwright.config.ts`:

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // Existing projects...

    // New project for feature
    {
      name: 'chrome-{feature}',
      testMatch: '**/{feature}/**/*.spec.ts',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 }
      },
      workers: 1,  // Serial execution
      retries: 2   // Auto-retry on failure
    }
  ]
})
```

### 4. Update GitHub Actions Workflow

Add test job to `.github/workflows/ci.yml`:

```yaml
jobs:
  test-{feature}:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'yarn'

      - name: Install dependencies
        run: yarn install --frozen-lockfile

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Run {feature} tests
        run: npx playwright test --project=chrome-{feature}

      - name: Upload test report
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-{feature}
          path: playwright-report/
          retention-days: 7
```

### 5. Commit Changes

```bash
git add playwright.config.ts .github/workflows/ci.yml
git commit -m "ci: add automated tests for {ticket-id}"
```

---

## Configuration Patterns

### Serial Test Project (Shared State)

```typescript
{
  name: 'chrome-serial',
  testMatch: '**/serial/**/*.spec.ts',
  workers: 1,
  fullyParallel: false,
  retries: 2
}
```

### Parallel Test Project (Independent)

```typescript
{
  name: 'chrome-parallel',
  testMatch: '**/parallel/**/*.spec.ts',
  workers: 4,
  fullyParallel: true,
  retries: 1
}
```

### API Test Project

```typescript
{
  name: 'api-tests',
  testMatch: '**/*-api.spec.ts',
  use: {
    baseURL: process.env.API_URL
  },
  workers: 4
}
```

---

## GitHub Actions Best Practices

### Caching

```yaml
- name: Cache Playwright browsers
  uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ hashFiles('**/yarn.lock') }}
```

### Sharding for Large Test Suites

```yaml
strategy:
  matrix:
    shard: [1/4, 2/4, 3/4, 4/4]

steps:
  - run: npx playwright test --shard=${{ matrix.shard }}
```

### Conditional Execution

```yaml
# Only run on specific paths
on:
  push:
    paths:
      - 'src/{feature}/**'
      - 'automation/playwright/tests/{feature}/**'
```

---

## Output

Updated configuration files:
- `playwright.config.ts` (if new project added)
- `.github/workflows/ci.yml` (new test job)

---

## Verification

After CI configuration:

```bash
# Verify Playwright config is valid
npx playwright test --list

# Dry run to check workflow syntax
act -n push  # Using 'act' for local testing
```
