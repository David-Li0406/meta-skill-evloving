# Optimization and Debugging for GitHub Actions

Performance optimization, caching strategies, debugging techniques, and troubleshooting patterns for CI/CD workflows.

---

## Workflow Optimization

### 1. Skip Redundant Runs

Use path filters to prevent unnecessary workflow runs:

```yaml
on:
  push:
    paths:
      - "src/**"
      - "!**.md"          # Exclude markdown
      - "!docs/**"        # Exclude docs
      - ".github/workflows/ci.yml"  # Include workflow itself
```

### 2. Fast Fail for Quick Feedback

Run fast checks first, expensive tests later:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make lint  # Fast check runs first

  test:
    needs: lint  # Expensive tests wait
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

### 3. Parallel Job Execution

Maximize parallelism:

```yaml
jobs:
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - run: make unit-test

  integration-test:
    runs-on: ubuntu-latest  # Runs parallel with unit-test
    steps:
      - run: make integration-test

  e2e-test:
    runs-on: ubuntu-latest  # Runs parallel with both
    steps:
      - run: make e2e-test
```

### 4. Matrix Optimization

Use matrix strategy efficiently:

```yaml
strategy:
  fail-fast: false  # See all failures, don't stop early
  matrix:
    os: [ubuntu-latest, macos-latest]
    go: ["1.21", "1.22"]
    exclude:
      - os: macos-latest  # Skip expensive combo
        go: "1.21"

runs-on: ${{ matrix.os }}
```

---

## Caching Strategies

### Effective Caching

Cache restore is fast; cache save is slow. Optimize both:

```yaml
- name: Cache Dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
    restore-keys: |
      ${{ runner.os }}-go-  # Fallback to partial match
```

### Cache Key Strategies

**Exact Match:**
```yaml
key: ${{ runner.os }}-deps-${{ hashFiles('package-lock.json') }}
```

**Partial Match (Fallback):**
```yaml
restore-keys: |
  ${{ runner.os }}-deps-
  ${{ runner.os }}-
```

**Multi-Level Keys:**
```yaml
key: v1-${{ runner.os }}-${{ hashFiles('**/*.go') }}-${{ github.sha }}
restore-keys: |
  v1-${{ runner.os }}-${{ hashFiles('**/*.go') }}-
  v1-${{ runner.os }}-
```

### Language-Specific Caching

**Go:**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
```

**Node.js:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Python:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

**Rust:**
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      ~/.cargo/git/db/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

### Cache Invalidation

Bust cache when needed:

```yaml
# Add version prefix to key
key: v2-${{ runner.os }}-deps-${{ hashFiles('lockfile') }}

# Or use workflow run number
key: ${{ github.run_number }}-${{ runner.os }}-deps
```

### Cache Size Limits

- Maximum cache size: 10 GB per repository
- Unused caches deleted after 7 days
- Keep caches small and targeted

---

## Debugging Workflows

### 1. Enable Debug Logging

Set repository secrets:
- `ACTIONS_RUNNER_DEBUG`: `true` (runner diagnostics)
- `ACTIONS_STEP_DEBUG`: `true` (step-level debug)

Or use workflow dispatch:

```yaml
on:
  workflow_dispatch:
    inputs:
      debug_enabled:
        type: boolean
        description: 'Enable debug logging'
        default: false

jobs:
  build:
    steps:
      - name: Enable Debug
        if: ${{ inputs.debug_enabled }}
        run: |
          echo "ACTIONS_RUNNER_DEBUG=true" >> $GITHUB_ENV
          echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
```

### 2. Debug Information Steps

Add debug output:

```yaml
- name: Debug Information
  run: |
    echo "--- Environment ---"
    env | sort
    echo ""
    echo "--- GitHub Context ---"
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "SHA: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    echo "Runner OS: ${{ runner.os }}"
    echo "Working Directory: $(pwd)"
    echo ""
    echo "--- Files ---"
    ls -la
```

### 3. Step Summaries

Add formatted output to job summary:

```yaml
- name: Generate Summary
  run: |
    echo "## 🚀 Build Summary" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "- **Commit**: ${{ github.sha }}" >> $GITHUB_STEP_SUMMARY
    echo "- **Branch**: ${{ github.ref_name }}" >> $GITHUB_STEP_SUMMARY
    echo "- **Status**: ✅ Success" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "### Build Stats" >> $GITHUB_STEP_SUMMARY
    echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
    du -sh dist/* >> $GITHUB_STEP_SUMMARY
    echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
```

### 4. Conditional Debugging

Add debug steps that only run on failure:

```yaml
- name: Run Tests
  run: make test

- name: Debug on Failure
  if: failure()
  run: |
    echo "Test failed, dumping logs..."
    cat logs/*.log
    echo ""
    echo "Environment:"
    env | sort
```

### 5. SSH Debugging (Last Resort)

Use [action-tmate](https://github.com/mxschmitt/action-tmate):

```yaml
- name: Setup tmate session
  if: failure()  # Only on failure
  uses: mxschmitt/action-tmate@v3
  timeout-minutes: 15  # Limit session time
```

---

## Performance Monitoring

### Timing Steps

```yaml
- name: Build
  run: |
    start_time=$(date +%s)
    make build
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "Build took ${duration}s"
    echo "build_duration=${duration}" >> $GITHUB_OUTPUT
```

### Job Duration Tracking

```yaml
- name: Job Summary
  if: always()
  run: |
    echo "## ⏱️ Performance" >> $GITHUB_STEP_SUMMARY
    echo "- **Job Duration**: ${{ job.status == 'success' && '✅' || '❌' }} $(date -u -d @$(($(date +%s) - ${{ github.event.created_at }})) +%M:%S)" >> $GITHUB_STEP_SUMMARY
```

---

## Common Issues and Solutions

### Issue: Workflow Not Triggering

**Causes:**
- Path filters exclude changed files
- Branch protection prevents workflow
- Workflow disabled in repository settings

**Solution:**
```yaml
on:
  push:
    branches:
      - main
      - develop
    paths:
      - "src/**"
      - ".github/workflows/ci.yml"  # Always include workflow file
```

### Issue: Cache Not Restoring

**Causes:**
- Key changed (expected)
- Cache expired (7 days)
- Cache size exceeded (10 GB)

**Solution:**
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache
    key: v1-${{ runner.os }}-${{ hashFiles('lockfile') }}
    restore-keys: |
      v1-${{ runner.os }}-  # Fallback
```

**Debug:**
```yaml
- name: Check Cache
  run: |
    echo "Cache key: v1-${{ runner.os }}-${{ hashFiles('lockfile') }}"
    ls -la ~/.cache || echo "Cache directory not found"
```

### Issue: Artifacts Not Found

**Causes:**
- Upload path incorrect
- Artifact expired (retention-days)
- Job failed before upload

**Solution:**
```yaml
- name: Upload Artifacts
  if: always()  # Upload even on failure
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: dist/
    if-no-files-found: error  # Fail if nothing to upload
```

### Issue: Permission Denied

**Causes:**
- Insufficient job permissions
- GITHUB_TOKEN lacks scope

**Solution:**
```yaml
permissions:
  contents: write  # Add needed permission
  pull-requests: write

jobs:
  job:
    steps:
      - name: Create Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Issue: Timeout

**Causes:**
- Default 6-hour timeout exceeded
- Hanging process

**Solution:**
```yaml
jobs:
  build:
    timeout-minutes: 30  # Set reasonable timeout
    steps:
      - name: Build
        run: timeout 300 make build  # Per-command timeout
```

---

## Conditional Execution Patterns

### By Event Type

```yaml
- name: Only on Push
  if: github.event_name == 'push'
  run: echo "Pushed!"

- name: Only on PR
  if: github.event_name == 'pull_request'
  run: echo "PR opened/updated!"
```

### By Branch

```yaml
- name: Only on Main
  if: github.ref == 'refs/heads/main'
  run: echo "Main branch!"

- name: Only on Tags
  if: startsWith(github.ref, 'refs/tags/')
  run: echo "Tag pushed!"
```

### By Matrix Value

```yaml
- name: macOS Only
  if: matrix.platform == 'macos'
  run: brew install tool

- name: Linux Only
  if: matrix.platform != 'macos'
  run: apt-get install tool
```

### By Previous Step Status

```yaml
- name: Always Run
  if: always()
  run: echo "Cleanup"

- name: On Success
  if: success()
  run: echo "Succeeded!"

- name: On Failure
  if: failure()
  run: cat error.log

- name: On Cancellation
  if: cancelled()
  run: echo "Cancelled"
```

### By File Changes

```yaml
- name: Check Changes
  id: changes
  run: |
    if git diff --name-only HEAD^ HEAD | grep '^src/'; then
      echo "src_changed=true" >> $GITHUB_OUTPUT
    fi

- name: If Source Changed
  if: steps.changes.outputs.src_changed == 'true'
  run: make build
```

---

## Working Directory

### Per-Step Working Directory

```yaml
- name: Build
  run: go build
  working-directory: installer

- name: Test
  run: go test ./...
  working-directory: installer
```

### Job-Level Default

```yaml
jobs:
  build:
    defaults:
      run:
        working-directory: installer
    steps:
      - run: go build    # Uses installer/
      - run: go test ./... # Uses installer/
```

---

## Environment Variables

### Job-Level Environment

```yaml
jobs:
  build:
    env:
      GO111MODULE: on
      CGO_ENABLED: 0
    steps:
      - run: go build  # Uses job env
```

### Step-Level Environment

```yaml
- name: Build
  run: make build
  env:
    CGO_ENABLED: 0
    GOOS: linux
    GOARCH: amd64
```

### Setting Environment for Subsequent Steps

```yaml
- name: Set Environment
  run: |
    echo "BUILD_VERSION=1.2.3" >> $GITHUB_ENV
    echo "BUILD_DATE=$(date +%Y-%m-%d)" >> $GITHUB_ENV

- name: Use Environment
  run: |
    echo "Version: $BUILD_VERSION"
    echo "Date: $BUILD_DATE"
```

---

## Best Practices Summary

1. **Use path filters** to skip unnecessary runs
2. **Run fast checks first** for quick feedback
3. **Maximize parallelism** with independent jobs
4. **Cache dependencies** with smart key strategies
5. **Set reasonable timeouts** to prevent hanging
6. **Add debug steps** conditional on failure
7. **Use step summaries** for better visibility
8. **Monitor job duration** to catch performance regressions
9. **Pin action versions** for reproducibility
10. **Keep caches small** and targeted
