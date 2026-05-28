# Parallel Test Execution Guide

## Overview

The `run_tests_parallel.sh` script executes Terraform provider acceptance tests with file-level parallelism, allowing multiple test files to run concurrently for faster feedback.

## Basic Usage

### ✅ RECOMMENDED: Two-Step Process with Logging

**Step 1: Start tests with output redirected to log file**
```bash
# Create log file with timestamp
LOG_FILE="/tmp/terraform-tests-$(date +%Y%m%d-%H%M%S).log"

# Start tests in background with all environment variables
TF_ACC=1 BCM_ENDPOINT="${BCM_ENDPOINT}" BCM_USERNAME="${BCM_USERNAME}" \
BCM_PASSWORD="${BCM_PASSWORD}" \
./.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh \
  -c 21 -t 30m > "$LOG_FILE" 2>&1 &

# Save the process ID
TEST_PID=$!
echo "Tests running in background (PID: $TEST_PID)"
echo "Log file: $LOG_FILE"
```

**Step 2: Monitor test output with tail**
```bash
# Follow the log file in real-time
tail -f "$LOG_FILE"

# Press Ctrl+C to stop tailing (tests continue running)
```

**Why this approach?**
- ✅ Full control over environment variables
- ✅ Tests run in background (non-blocking)
- ✅ Complete log file preserved for later analysis
- ✅ Can disconnect and reconnect to tail
- ✅ Simple and transparent
- ✅ No wrapper complexity

### Alternative: Wrapper Script

**For convenience, use the wrapper script:**
```bash
# Run all tests - auto-logs and shows output
./.claude/skills/terraform-provider-tests/scripts/run_tests_with_log.sh -c 21 -t 30m

# Run only resource tests
./.claude/skills/terraform-provider-tests/scripts/run_tests_with_log.sh --resources-only -c 8
```

Note: Ensure all required environment variables are exported before using the wrapper.

### Quick Piped Output

**For direct control without logging:**
```bash
# View last 100 lines (quick feedback)
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100

# Save full log AND see output (CI/CD)
./run_tests_parallel.sh -c 21 2>&1 | tee test-results.log

# View full output in real-time
./run_tests_parallel.sh -c 4
```

## Command Options

### Concurrency Control
```bash
# Run with default concurrency (30 files at once)
./run_tests_parallel.sh

# Run all test files in parallel (21 files)
./run_tests_parallel.sh -c 21 2>&1 | tail -100

# Conservative parallelism (2 files)
./run_tests_parallel.sh -c 2
```

### Timeout Configuration
```bash
# Set 30-minute timeout per test file
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100

# Set 1-hour timeout for slow tests
./run_tests_parallel.sh -t 1h 2>&1 | tail -100
```

### Test Filtering
```bash
# Run only resource tests
./run_tests_parallel.sh --resources-only -c 8 2>&1 | tail -100

# Run only data source tests
./run_tests_parallel.sh --data-sources-only -c 10 2>&1 | tail -100

# Run specific test pattern
./run_tests_parallel.sh -p "Idempotency" 2>&1 | tail -100

# Run specific test file
./run_tests_parallel.sh -f resource_cmdevice_device_test.go
```

### Output Control
```bash
# Verbose mode - see detailed output
./run_tests_parallel.sh --verbose 2>&1 | tail -200

# Disable color output (for logs)
./run_tests_parallel.sh --no-color 2>&1 | tee clean.log
```

## Output Patterns

### Pattern 1: Interactive Development (Recommended)
```bash
# See last 100 lines - good for quick feedback
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100
```

**When to use:**
- Running tests locally
- Quick verification of fixes
- Debugging specific failures

### Pattern 2: Full Logging (CI/CD)
```bash
# Save complete log while watching progress
./run_tests_parallel.sh -c 21 2>&1 | tee test-results-$(date +%Y%m%d-%H%M%S).log
```

**When to use:**
- CI/CD pipelines
- Full test suite runs
- Need complete audit trail
- Investigating intermittent failures

### Pattern 3: Follow Progress (Real-time)
```bash
# Watch test progress in real-time
./run_tests_parallel.sh -c 4
```

**When to use:**
- Small test sets
- Need immediate feedback
- Debugging test hangs

## Understanding Output

### Test Execution Flow
```
===== Terraform Provider Parallel Test Execution =====
Test Directory: ./internal/provider
Test Pattern: TestAcc
Concurrency: 21
Timeout: 30m

Found 21 test file(s)

[START] bcm_client_test.go
[START] data_source_cmdevice_categories_test.go
...
[PASS] bcm_client_test.go (7s, passed: 13)
[PASS] data_source_cmdevice_categories_test.go (8s, passed: 4)
[FAIL] resource_cmdevice_device_test.go (149s, passed: 4, failed: 1)

===== Test Summary =====
Test Files: 21
Total Passed: 95
Total Failed: 5
Total Skipped: 0
Total Duration: 347s

Failed Files (5):
  - resource_cmdevice_device_test.go
  - resource_cmdevice_device_idempotency_test.go
  - resource_cmkube_cluster_test.go
```

### Status Indicators
- **[START]** - Test file execution started
- **[PASS]** - All tests in file passed
- **[FAIL]** - One or more tests in file failed
- **[SKIP]** - File skipped (no test functions)

## Performance Guidelines

### Concurrency Recommendations

| Test Count | Recommended -c | Notes |
|------------|----------------|-------|
| 1-5 files  | -c 4          | Default, balanced |
| 5-10 files | -c 8          | Moderate parallelism |
| 10-20 files| -c 15         | High parallelism |
| 20+ files  | -c 21         | Maximum parallelism |

### Resource Considerations

**CPU-bound tests:**
```bash
# Set concurrency to CPU count
./run_tests_parallel.sh -c $(nproc) 2>&1 | tail -100
```

**I/O-bound tests (API calls):**
```bash
# Higher concurrency - waiting on API responses
./run_tests_parallel.sh -c 20 2>&1 | tail -100
```

**Memory-intensive tests:**
```bash
# Lower concurrency to avoid OOM
./run_tests_parallel.sh -c 4 2>&1 | tail -100
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run Acceptance Tests
  env:
    TF_ACC: 1
    BCM_ENDPOINT: ${{ secrets.BCM_ENDPOINT }}
    BCM_USERNAME: ${{ secrets.BCM_USERNAME }}
    BCM_PASSWORD: ${{ secrets.BCM_PASSWORD }}
  run: |
    ./.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh \
      -c 21 -t 30m 2>&1 | tee test-results.log

- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: test-results.log
```

### GitLab CI
```yaml
test:
  script:
    - ./.claude/skills/terraform-provider-tests/scripts/run_tests_parallel.sh
        -c 21 -t 30m 2>&1 | tee test-results.log
  artifacts:
    when: always
    paths:
      - test-results.log
    expire_in: 7 days
```

## Troubleshooting

### Tests Hang
```bash
# Reduce timeout to fail faster
./run_tests_parallel.sh -c 4 -t 5m 2>&1 | tail -100

# Run specific hanging test file
./run_tests_parallel.sh -f resource_that_hangs_test.go --verbose
```

### Out of Memory
```bash
# Reduce concurrency
./run_tests_parallel.sh -c 2 2>&1 | tail -100

# Run resources sequentially
./run_tests_parallel.sh --resources-only -c 1 2>&1 | tail -100
```

### Connection Timeouts
```bash
# Increase timeout per test
./run_tests_parallel.sh -c 4 -t 1h 2>&1 | tail -100

# Reduce concurrency to avoid API rate limits
./run_tests_parallel.sh -c 2 2>&1 | tail -100
```

### Missing Output
```bash
# Use verbose mode
./run_tests_parallel.sh --verbose 2>&1 | tee debug.log

# Check if tests are actually running
ps aux | grep "go test"

# Check result files
ls -la /tmp/tmp.*/
cat /tmp/tmp.*/*.result
```

## Best Practices

### 1. Always Pipe Output
```bash
# ✅ Good - see output
./run_tests_parallel.sh -c 21 2>&1 | tail -100

# ❌ Bad - no visibility
./run_tests_parallel.sh -c 21 &
```

### 2. Save Logs in CI
```bash
# ✅ Good - logs preserved
./run_tests_parallel.sh -c 21 2>&1 | tee results.log

# ❌ Bad - logs lost
./run_tests_parallel.sh -c 21
```

### 3. Use Appropriate Concurrency
```bash
# ✅ Good - matches test count
./run_tests_parallel.sh -c 21 2>&1 | tail -100

# ❌ Bad - wasted parallelism
./run_tests_parallel.sh -c 100 2>&1 | tail -100
```

### 4. Set Reasonable Timeouts
```bash
# ✅ Good - allows completion
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100

# ❌ Bad - tests timeout prematurely
./run_tests_parallel.sh -c 21 -t 1m 2>&1 | tail -100
```

### 5. Filter When Debugging
```bash
# ✅ Good - focus on failures
./run_tests_parallel.sh -p "Idempotency" 2>&1 | tail -100

# ❌ Bad - run everything when debugging one thing
./run_tests_parallel.sh -c 21 2>&1 | tail -100
```

## Summary

**Key Takeaways:**
1. ✅ **Always use `| tail -100`** or `| tee logfile.log`
2. ❌ **Never run in background** - you need to see progress
3. 🚀 **Use high concurrency** for full test suites (`-c 21`)
4. 🎯 **Filter tests** when debugging (`-p`, `-f`, `--resources-only`)
5. 📝 **Save logs** in CI/CD pipelines (`| tee`)
6. ⏱️ **Set appropriate timeouts** based on test duration (`-t 30m`)

**Quick Reference:**
```bash
# Development (fast feedback)
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tail -100

# CI/CD (full logging)
./run_tests_parallel.sh -c 21 -t 30m 2>&1 | tee test-$(date +%s).log

# Debugging (focused)
./run_tests_parallel.sh -f specific_test.go --verbose
```
