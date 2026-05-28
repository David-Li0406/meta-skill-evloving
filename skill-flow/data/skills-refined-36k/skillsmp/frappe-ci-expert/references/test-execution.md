# Test Execution

This reference covers running tests in CI environments, including parallel tests, UI tests, and test output handling.

## Server Tests

### Enabling Tests

Before running tests, ensure tests are enabled on the site:

```bash
# Set allow_tests config (required for some apps)
bench --site test_site set-config allow_tests true
```

Some official apps (like CRM) require this configuration before running tests.

### Parallel Test Execution

The standard way to run Frappe tests in CI:

```bash
bench --site test_site run-parallel-tests --app your_app_name
```

### Test Orchestrator (Advanced)

ERPNext uses a test orchestrator for distributed testing:

```bash
bench --site test_site run-parallel-tests \
  --app erpnext \
  --total-builds 4 \
  --build-number ${{ matrix.container }}
```

With environment variables:
```yaml
env:
  CI_BUILD_ID: ${{ github.run_id }}
  ORCHESTRATOR_URL: http://test-orchestrator.frappe.io
```

This distributes tests across multiple CI runners for faster execution.

### What This Does

1. Discovers all test files in the app
2. Splits tests across multiple processes
3. Runs tests in parallel for speed
4. Aggregates results and reports failures

### Options and Flags

```bash
# Basic usage
bench --site test_site run-parallel-tests --app your_app_name

# With orchestrator
bench --site test_site run-parallel-tests --app your_app_name --total-builds 4 --build-number 1

# With specific test pattern
bench --site test_site run-parallel-tests --app your_app_name --pattern "test_*.py"

# Verbose output
bench --site test_site run-parallel-tests --app your_app_name --verbose

# With coverage
bench --site test_site run-parallel-tests --app your_app_name --with-coverage

# Failfast (stop on first failure)
bench --site test_site run-parallel-tests --app your_app_name --failfast
```

### Alternative: run-tests (Non-Parallel)

Some apps use `run-tests` instead of `run-parallel-tests`:

```bash
# Standard test execution
bench --site test_site run-tests --app your_app_name

# With coverage
bench --site test_site run-tests --app your_app_name --coverage
```

### In Workflow

```yaml
- name: Set Config
  run: bench --site test_site set-config allow_tests true
  working-directory: /home/runner/frappe-bench

- name: Run Tests
  run: bench --site test_site run-parallel-tests --app your_app_name
  working-directory: /home/runner/frappe-bench
```

Note the `working-directory` - bench commands must run from the bench directory.

## Running Specific Tests

### Single Test Module

```bash
bench --site test_site run-tests --module your_app.module.test_file
```

Example:
```bash
bench --site test_site run-tests --module myapp.myapp.doctype.item.test_item
```

### Specific Test Class

```bash
bench --site test_site run-tests \
    --module your_app.module.test_file \
    --test-case TestClassName
```

### Specific Test Method

```bash
bench --site test_site run-tests \
    --module your_app.module.test_file \
    --test-case TestClassName.test_method_name
```

### Why Use Specific Tests in CI?

Usually you don't - run the full suite. But specific tests are useful for:
- Debugging specific failures
- Testing only changed modules
- Quick feedback during development

## UI Tests (Cypress)

### Basic UI Test Execution

```bash
bench --site test_site run-ui-tests your_app_name --headless
```

### Parallel UI Tests

For faster execution with multiple containers:

```yaml
strategy:
  matrix:
    container: [1, 2, 3]

steps:
  # ... setup steps ...
  
  - name: UI Tests
    run: |
      cd ~/frappe-bench/
      bench --site test_site run-ui-tests your_app_name \
        --headless \
        --parallel \
        --ci-build-id $GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT
```

### UI Test Options

```bash
# Headless mode (no browser UI)
bench --site test_site run-ui-tests your_app --headless

# With parallel execution
bench --site test_site run-ui-tests your_app --headless --parallel

# Specific spec file
bench --site test_site run-ui-tests your_app --headless --spec "cypress/integration/test.js"

# With CI build ID for Cypress Dashboard
bench --site test_site run-ui-tests your_app \
  --headless \
  --parallel \
  --ci-build-id $GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT
```

### Setup for UI Tests

Before running UI tests, complete setup wizard:

```yaml
- name: Site Setup
  run: |
    cd ~/frappe-bench/
    bench --site test_site execute frappe.utils.install.complete_setup_wizard
    bench --site test_site execute frappe.tests.ui_test_helpers.create_test_user
```

This creates necessary user accounts and configures the site.

## Code Coverage

### Server Test Coverage

```bash
# Run with coverage
bench --site test_site run-parallel-tests --app your_app_name --with-coverage
```

This generates:
- `coverage.xml` - Machine-readable coverage report
- `.coverage` - Raw coverage data
- `htmlcov/` - HTML coverage report (if configured)

### UI Test Coverage

For UI tests, enable coverage in Procfile:

```bash
sed -i 's/^web: bench serve/web: bench serve --with-coverage/g' Procfile
```

Then run UI tests normally. Backend coverage is collected automatically.

### Uploading Coverage

#### Simple Upload

Upload to Codecov or similar services:

```yaml
- name: Upload Coverage
  uses: codecov/codecov-action@v4
  with:
    file: ~/frappe-bench/apps/your_app_name/coverage.xml
    flags: server
    name: Server Tests
```

#### Multi-Job Coverage Pattern (Recommended)

Official apps like Helpdesk use a multi-job pattern for coverage:

```yaml
jobs:
  tests:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      # ... setup and test steps ...
      
      - name: Run Tests
        run: bench --site test_site run-tests --app your_app_name --coverage
      
      - name: Upload coverage data
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.container }}
          path: /home/runner/frappe-bench/sites/coverage.xml

  coverage:
    name: Coverage Wrap Up
    needs: tests
    runs-on: ubuntu-latest
    steps:
      - name: Clone
        uses: actions/checkout@v6

      - name: Download artifacts
        uses: actions/download-artifact@v4

      - name: Upload coverage data
        uses: codecov/codecov-action@v4
        with:
          name: MariaDB
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true
          verbose: true
```

This pattern:
1. Runs tests and saves coverage as artifacts
2. Separate job downloads all coverage artifacts
3. Uploads combined coverage to Codecov

Benefits:
- Works with matrix strategies
- Combines coverage from multiple test runs
- Cleaner separation of concerns

## Test Output and Logging

### Capturing Test Output

Tests run in workflow automatically capture stdout/stderr.

### Bench Logs

Always collect bench logs, especially on failure:

```yaml
- name: Show bench output
  if: ${{ always() }}
  run: |
    cd ~/frappe-bench
    cat bench_start.log || true
    cd logs
    for f in ./*.log*; do
      echo "Printing log: $f";
      cat $f
    done
```

The `always()` condition ensures logs are shown even if tests fail.

### What Logs Are Available?

- `bench_start.log` - Output from bench start command
- `logs/web.error.log` - Web server errors
- `logs/web.log` - Web server access logs
- `logs/worker.log` - Background worker logs
- `logs/frappe.log` - General Frappe logs

## Test Failures

### Exit Codes

Tests return non-zero exit codes on failure, which fails the workflow step.

### Failure Output

```
FAILED tests/test_something.py::TestClass::test_method - AssertionError: ...
```

The workflow will show:
- Which tests failed
- Assertion errors
- Tracebacks
- Relevant logs

### Debugging Failed Tests

1. **Check the test output** in workflow logs
2. **Review bench logs** for server errors
3. **Reproduce locally** with same setup
4. **Use tmate** for interactive debugging

## Testing Multiple Apps

### Install Multiple Apps

```bash
# Install dependencies first
bench --site test_site install-app erpnext
bench --site test_site install-app hrms

# Install your app
bench --site test_site install-app your_app_name
```

### Run Tests for Specific App

```bash
# Only your app
bench --site test_site run-parallel-tests --app your_app_name

# All installed apps
bench --site test_site run-parallel-tests
```

### Matrix Testing Against Versions

Test your app against multiple versions of dependencies:

```yaml
strategy:
  matrix:
    frappe-version: [version-14, version-15]
    erpnext-version: [version-14, version-15]

steps:
  - name: Get Frappe
    run: |
      cd ~/frappe-bench/apps/frappe
      git fetch origin ${{ matrix.frappe-version }}
      git checkout ${{ matrix.frappe-version }}

  - name: Get ERPNext
    run: |
      cd ~/frappe-bench
      bench get-app erpnext --branch ${{ matrix.erpnext-version }}
      bench --site test_site install-app erpnext
```

## Performance Considerations

### Parallel Test Performance

Parallel tests are significantly faster:
- Sequential: ~15-30 minutes
- Parallel: ~5-10 minutes

Adjust the number of processes based on your test suite size.

### UI Test Performance

UI tests are slower due to browser automation:
- Single container: ~20-30 minutes
- 3 containers (parallel): ~8-12 minutes

Use matrix strategy to parallelize across containers.

### Caching for Speed

Cache these between runs:

```yaml
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt') }}

- name: Get yarn cache directory path
  id: yarn-cache-dir-path
  run: echo "dir=$(yarn cache dir)" >> $GITHUB_OUTPUT

- uses: actions/cache@v3
  with:
    path: ${{ steps.yarn-cache-dir-path.outputs.dir }}
    key: ${{ runner.os }}-yarn-${{ hashFiles('**/yarn.lock') }}
```

## Test Environment Variables

### Standard Variables

Set in workflow environment:

```yaml
env:
  CI: 1
  NODE_ENV: production
```

### App-Specific Variables

If your app needs specific configuration:

```yaml
env:
  YOUR_APP_API_KEY: test_key
  YOUR_APP_DEBUG: 1
```

Access in tests:

```python
import os
api_key = os.getenv('YOUR_APP_API_KEY')
```

## Test Database

### Fresh Database Per Run

Each workflow run gets a fresh database:
1. Database created in setup
2. Site installed from scratch
3. Tests run on clean state
4. Database destroyed after run

### Restoring Production Data

For migration tests, restore a production backup:

```bash
wget https://example.com/backup.sql.gz
bench --site test_site --force restore backup.sql.gz
bench --site test_site migrate
```

### Multiple Test Sites

Create multiple sites if needed:

```bash
# Create second site
bench new-site test_site_2 --db-root-password travis --admin-password admin
bench --site test_site_2 install-app your_app_name

# Run tests on specific site
bench --site test_site_2 run-tests --app your_app_name
```

## Test Artifacts

### Saving Test Results

Save test results for later analysis:

```yaml
- name: Archive test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: |
      ~/frappe-bench/apps/your_app_name/test_results.xml
      ~/frappe-bench/apps/your_app_name/coverage.xml
```

### Saving Screenshots (UI Tests)

Cypress automatically saves screenshots on failure:

```yaml
- name: Archive screenshots
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: cypress-screenshots
    path: ~/frappe-bench/apps/your_app_name/cypress/screenshots
```

## Conditional Test Execution

### Run Tests Only on Changes

Use path filters:

```yaml
on:
  pull_request:
    paths:
      - '**.py'
      - '**.js'
      - '**/test_*.py'
```

### Skip Tests on Documentation Changes

```yaml
on:
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

### Matrix Conditional Execution

Run different tests based on matrix:

```yaml
- name: Run Server Tests
  if: matrix.test-type == 'server'
  run: bench --site test_site run-parallel-tests --app your_app_name

- name: Run UI Tests
  if: matrix.test-type == 'ui'
  run: bench --site test_site run-ui-tests your_app_name --headless
```

## Test Timeouts

### Global Timeout

Set on the job:

```yaml
jobs:
  test:
    timeout-minutes: 30  # Fail if tests take longer
```

### Per-Step Timeout

```yaml
- name: Run Tests
  timeout-minutes: 20
  run: bench --site test_site run-parallel-tests --app your_app_name
```

## Debugging Test Execution

### Verbose Test Output

```bash
bench --site test_site run-parallel-tests --app your_app_name --verbose
```

### Interactive Debugging with tmate

Add to workflow:

```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: ${{ failure() || contains(github.event.pull_request.labels.*.name, 'debug-gha') }}
```

This gives SSH access to the runner when tests fail or when `debug-gha` label is present.

### Print Test Discovery

See what tests will run:

```bash
bench --site test_site run-tests --app your_app_name --dry-run
```

## Common Test Issues

### Issue: Import Errors

**Cause**: App not installed or not in apps.txt

**Solution**:
```bash
bench --site test_site install-app your_app_name
cat ~/frappe-bench/sites/apps.txt  # Verify app is listed
```

### Issue: Database Connection Errors

**Cause**: Site config incorrect or database not created

**Solution**:
```bash
cat ~/frappe-bench/sites/test_site/site_config.json
mariadb -h 127.0.0.1 -u test_frappe -ptest_frappe test_frappe -e "SHOW TABLES;"
```

### Issue: Tests Timeout

**Cause**: Tests hanging or taking too long

**Solution**:
- Increase timeout
- Check for infinite loops in tests
- Verify database and Redis are running

### Issue: UI Tests Fail

**Cause**: Various Cypress-related issues

**Solution**:
- Check Cypress binary is cached correctly
- Verify bench serve is running
- Check test user was created
- Review Cypress screenshots/videos

## Best Practices

1. **Always run parallel tests** for speed
2. **Collect logs on all runs** (use `always()`)
3. **Set reasonable timeouts** (30-60 minutes)
4. **Cache dependencies** (pip, yarn, Cypress)
5. **Use fresh database** per run
6. **Clean up test data** in tearDown methods
7. **Mock external services** in tests
8. **Use fixtures** for common test data
9. **Tag slow tests** and optionally skip in CI
10. **Monitor test execution time** and optimize slow tests
