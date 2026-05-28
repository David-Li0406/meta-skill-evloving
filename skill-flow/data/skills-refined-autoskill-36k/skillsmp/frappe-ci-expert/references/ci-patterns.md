# CI Patterns and Best Practices

This reference covers best practices, common patterns, optimization strategies, and troubleshooting for Frappe CI setups.

## Caching Strategies

### Python Package Caching

Cache pip packages to speed up dependency installation:

```yaml
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt', '**/pyproject.toml', '**/setup.py') }}
    restore-keys: |
      ${{ runner.os }}-pip-
      ${{ runner.os }}-
```

**Key components**:
- Uses hash of requirements files as cache key
- Falls back to OS-level cache if exact match not found
- Saves 2-5 minutes per run

### Node Package Caching

Cache yarn packages:

```yaml
- name: Get yarn cache directory path
  id: yarn-cache-dir-path
  run: echo "dir=$(yarn cache dir)" >> $GITHUB_OUTPUT

- uses: actions/cache@v3
  id: yarn-cache
  with:
    path: ${{ steps.yarn-cache-dir-path.outputs.dir }}
    key: ${{ runner.os }}-yarn-${{ hashFiles('**/yarn.lock') }}
    restore-keys: |
      ${{ runner.os }}-yarn-
```

**Benefits**:
- Speeds up `yarn install` by 1-3 minutes
- Uses yarn.lock hash for cache invalidation

### Cypress Binary Caching

For UI tests, cache Cypress binary:

```yaml
- name: Cache cypress binary
  uses: actions/cache@v3
  with:
    path: ~/.cache/Cypress
    key: ${{ runner.os }}-cypress
```

Cypress is large (~100MB), caching saves significant time.

### Cache Best Practices

1. **Use specific cache keys** - Include file hashes
2. **Provide restore-keys** - Fall back to partial matches
3. **Don't cache too much** - GitHub has cache size limits (10GB per repo)
4. **Invalidate when needed** - Change key when dependencies change significantly
5. **Monitor cache hits** - Check if caches are being used effectively

## Performance Optimization

### Parallel Test Execution

**Always use parallel tests** for server tests:

```yaml
- name: Run Tests
  run: bench --site test_site run-parallel-tests --app your_app_name
```

**Speedup**: 3-5x faster than sequential tests

### Matrix Strategy for UI Tests

Run UI tests across multiple containers:

```yaml
strategy:
  fail-fast: false
  matrix:
    container: [1, 2, 3]
```

**Speedup**: 2-3x faster than single container

### Background Asset Building

Start asset building while installing site:

```bash
CI=Yes bench build --app frappe &
build_pid=$!

bench --site test_site reinstall --yes

wait $build_pid
```

**Speedup**: Saves 2-3 minutes by overlapping operations

### Skip Unnecessary Steps

For server tests, skip frontend setup:

```bash
if [ "$TYPE" == "server" ]
then
  # Skip node requirements
  # Skip Cypress installation
  # Disable socketio
fi
```

### Concurrent Workflows

Limit concurrent runs to save resources:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.event.number }}
  cancel-in-progress: true
```

This cancels old runs when new commits are pushed.

## Debugging Failures

### Interactive Debugging with tmate

SSH into the runner when tests fail:

```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
  if: ${{ failure() || contains(github.event.pull_request.labels.*.name, 'debug-gha') }}
```

**Usage**:
1. Add `debug-gha` label to PR, or
2. Let workflow fail, then SSH will be available
3. Access link shown in workflow logs

### Always Collect Logs

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

The `always()` ensures logs are shown even on failure.

### Artifact Upload

Save important files for debugging:

```yaml
- name: Upload logs
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: logs
    path: |
      ~/frappe-bench/bench_start.log
      ~/frappe-bench/logs/*.log*
```

### Enable Debug Output

Add debug flags:

```bash
set -ex  # Print commands and exit on error
bench -v ...  # Verbose bench output
```

### Check Service Health

Verify database is running:

```yaml
- name: Check Services
  if: failure()
  run: |
    mysqladmin ping -h 127.0.0.1 -u root -ptravis
    redis-cli ping
    docker ps -a
```

## Common Pitfalls and Solutions

### Pitfall 1: Tests Pass Locally but Fail in CI

**Common causes**:
- Different Python/Node versions
- Missing system dependencies
- Timing issues (tests run faster/slower)
- Environment variables not set

**Solutions**:
- Pin versions in workflow
- Document all system dependencies
- Add timeouts to async operations
- Set all required environment variables

### Pitfall 2: Flaky Tests

**Symptoms**: Tests intermittently pass/fail

**Common causes**:
- Race conditions
- Timing-dependent assertions
- External service dependencies
- Shared state between tests

**Solutions**:
- Use proper waiting mechanisms
- Add retry logic for network calls
- Mock external services
- Ensure test isolation

### Pitfall 3: Slow Tests

**Symptoms**: Workflow takes >30 minutes

**Solutions**:
- Use parallel test execution
- Cache dependencies
- Skip unnecessary setup steps
- Profile slow tests and optimize
- Use matrix strategy for UI tests

### Pitfall 4: Cache Not Working

**Symptoms**: Dependencies reinstall every time

**Solutions**:
- Check cache key includes file hashes
- Verify restore-keys are correct
- Check cache size limits not exceeded
- Ensure cache path is correct

### Pitfall 5: Database Connection Issues

**Symptoms**: "Connection refused" or "Access denied"

**Solutions**:
- Verify service health check passes
- Check credentials match in config
- Ensure database was created
- Wait for service to be ready

## Security Considerations

### Secrets Management

Never hardcode secrets in workflows:

```yaml
# Bad
env:
  API_KEY: sk_live_1234567890

# Good
env:
  API_KEY: ${{ secrets.API_KEY }}
```

Store secrets in GitHub Settings → Secrets.

### Database Credentials

For CI, use standard test credentials (safe to be public):
- root password: `travis`
- test user: `test_frappe:test_frappe`

Never use production credentials in CI.

### Access Tokens

For private dependencies, use:
- Personal Access Tokens stored as secrets
- Deploy keys for specific repositories
- Never commit tokens to code

## Multi-App Testing

### Testing Your App with Dependencies

```yaml
- name: Setup Dependencies
  run: |
    cd ~/frappe-bench
    bench get-app erpnext --branch version-14
    bench get-app hrms --branch version-14
    bench --site test_site install-app erpnext
    bench --site test_site install-app hrms

- name: Install Your App
  run: |
    cd ~/frappe-bench
    bench get-app ${GITHUB_WORKSPACE}
    bench --site test_site install-app your_app_name

- name: Run Tests
  run: bench --site test_site run-parallel-tests --app your_app_name
```

### Testing Multiple Apps Together

```yaml
- name: Run All Tests
  run: |
    bench --site test_site run-parallel-tests --app erpnext
    bench --site test_site run-parallel-tests --app hrms
    bench --site test_site run-parallel-tests --app your_app_name
```

### Version Matrix Testing

Test against multiple versions:

```yaml
strategy:
  matrix:
    frappe-version: [version-14, version-15, develop]
    include:
      - frappe-version: version-14
        erpnext-version: version-14
      - frappe-version: version-15
        erpnext-version: version-15
      - frappe-version: develop
        erpnext-version: develop
```

## Workflow Optimization Patterns

### Conditional Job Execution

Skip tests when only docs change:

```yaml
on:
  pull_request:
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - 'README*'
```

### Required Status Checks

For skipped jobs, use a faux-test job:

```yaml
faux-test:
  name: Unit Tests
  runs-on: ubuntu-latest
  needs: checkrun
  if: ${{ needs.checkrun.outputs.build != 'strawberry' }}
  steps:
    - name: Pass skipped tests unconditionally
      run: "echo Skipped"
```

This ensures GitHub's required status checks pass.

### Scheduled Testing

Run full test suite on schedule:

```yaml
on:
  schedule:
    - cron: "0 0 * * *"  # Daily at midnight UTC
```

Benefits:
- Catch integration issues early
- Test against latest dependencies
- Verify production data migrations

### Multiple Database Testing

Test both MariaDB and PostgreSQL:

```yaml
strategy:
  fail-fast: false
  matrix:
    db: [mariadb, postgres]

services:
  mariadb:
    # ... mariadb config
  postgres:
    # ... postgres config

steps:
  # ... setup steps
  - name: Install Dependencies
    env:
      DB: ${{ matrix.db }}
    run: |
      bash ${GITHUB_WORKSPACE}/.github/helper/install.sh
```

## Monitoring and Reporting

### Test Result Reporting

Use test reporter actions:

```yaml
- name: Test Report
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Test Results
    path: ~/frappe-bench/apps/your_app_name/test_results.xml
    reporter: java-junit
```

### Coverage Reporting

Upload to Codecov:

```yaml
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    file: ~/frappe-bench/apps/your_app_name/coverage.xml
    flags: server
    name: ${{ matrix.db }}-server-tests
```

### Slack Notifications

Notify team on failure:

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Tests failed: ${{ github.repository }} - ${{ github.ref }}"
      }
```

## Custom App Setup

### Minimal Setup for Custom App

```yaml
name: Tests

on: [pull_request, push]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    services:
      mariadb:
        image: mariadb:10.6.24
        env:
          MARIADB_ROOT_PASSWORD: travis
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping" --health-interval=5s

    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - uses: actions/setup-node@v3
        with:
          node-version: 24
      
      - name: Setup
        run: |
          sudo apt update
          sudo apt install libcups2-dev redis-server mariadb-client
          pip install frappe-bench
          cd ~
          bench init frappe-bench --skip-assets --python "$(which python)" --frappe-branch version-14
          cd frappe-bench
          bench get-app ${GITHUB_WORKSPACE}
          bench setup requirements --dev
          
      - name: Create Site
        run: |
          cd ~/frappe-bench
          bench new-site test_site --db-root-password travis --admin-password admin
          bench --site test_site install-app your_app_name
          
      - name: Run Tests
        run: |
          cd ~/frappe-bench
          bench --site test_site run-parallel-tests --app your_app_name
```

### Advanced Setup with Caching

Add caching to the minimal setup:

```yaml
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/*requirements.txt') }}

- name: Cache yarn
  uses: actions/cache@v3
  with:
    path: ~/.cache/yarn
    key: ${{ runner.os }}-yarn-${{ hashFiles('**/yarn.lock') }}
```

## Troubleshooting Checklist

When tests fail, check:

1. **Service health**:
   ```bash
   mysqladmin ping -h 127.0.0.1 -u root -ptravis
   redis-cli ping
   ```

2. **Database created**:
   ```bash
   mariadb -h 127.0.0.1 -u root -ptravis -e "SHOW DATABASES;"
   ```

3. **Site config exists**:
   ```bash
   cat ~/frappe-bench/sites/test_site/site_config.json
   ```

4. **App installed**:
   ```bash
   cat ~/frappe-bench/sites/apps.txt
   bench --site test_site list-apps
   ```

5. **Bench running**:
   ```bash
   ps aux | grep bench
   cat ~/frappe-bench/bench_start.log
   ```

6. **Python/Node versions**:
   ```bash
   python --version
   node --version
   ```

7. **Dependencies installed**:
   ```bash
   pip list | grep frappe
   ls ~/frappe-bench/env/lib/python*/site-packages/
   ```

## Best Practices Summary

1. **Use caching** for pip, yarn, and Cypress
2. **Run parallel tests** for speed
3. **Always collect logs** with `if: always()`
4. **Set reasonable timeouts** (30-60 minutes)
5. **Use matrix strategies** for multiple configurations
6. **Cache dependencies** between runs
7. **Pin versions** of Python, Node, and databases
8. **Use health checks** for services
9. **Provide restore-keys** for caches
10. **Test locally first** before pushing to CI
11. **Use secrets** for sensitive data
12. **Monitor test execution time** and optimize
13. **Add debug steps** for troubleshooting
14. **Use standard credentials** for test environments
15. **Keep workflows DRY** with reusable scripts

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [Bench CLI Documentation](https://frappeframework.com/docs/user/en/bench)
- [Cypress Documentation](https://docs.cypress.io)
