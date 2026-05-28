# Comprehensive jq Examples for CTRF Analysis

This document provides 24+ jq examples for analyzing CTRF test reports, organized by category. All examples assume CTRF files are in `/workspace/artifacts/test/`.

## Table of Contents

1. [Basic Queries](#basic-queries)
2. [Failure Analysis](#failure-analysis)
3. [Performance Analysis](#performance-analysis)
4. [Flaky Test Detection](#flaky-test-detection)
5. [Multi-Report Analysis](#multi-report-analysis)
6. [Advanced Filters](#advanced-filters)

---

## Basic Queries

### 1. Show complete summary object
```bash
jq '.results.summary' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output:
```json
{
  "tests": 415,
  "passed": 333,
  "failed": 81,
  "skipped": 1,
  "pending": 0,
  "other": 0,
  "start": 1768596014854,
  "stop": 1768596152016
}
```

### 2. One-line summary (compact)
```bash
jq -r '.results.summary | "Tests: \(.tests) | Passed: \(.passed) | Failed: \(.failed) | Skipped: \(.skipped)"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output: `Tests: 415 | Passed: 333 | Failed: 81 | Skipped: 1`

### 3. Pass rate percentage
```bash
jq -r '.results.summary | "Pass rate: \((.passed / .tests * 100) | floor)%"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output: `Pass rate: 80%`

### 4. Total test duration (calculated from start/stop)
```bash
jq -r '.results.summary | "Duration: \((.stop - .start) / 1000)s"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output: `Duration: 137.162s`

### 5. List all test names
```bash
jq -r '.results.tests[].name' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

---

## Failure Analysis

### 6. List failed test names only
```bash
jq -r '.results.tests[] | select(.status == "failed") | .name' /workspace/artifacts/test/*.ctrf.json
```

### 7. Failed tests with error messages (formatted)
```bash
jq -r '.results.tests[] | select(.status == "failed") | "❌ \(.name)\n   Error: \(.message // "No message")\n"' /workspace/artifacts/test/*.ctrf.json
```

Output:
```
❌ should execute CREATE tool sequence for new page
   Error: Expected status 200, got 403

❌ should handle placeholder replacement correctly
   Error: Timeout waiting for response
```

### 8. Failed tests with file locations
```bash
jq -r '.results.tests[] | select(.status == "failed") | "❌ \(.name)\n   File: \(.filePath // "N/A"):\(.line // "?")\n   Error: \(.message // "No message")\n"' /workspace/artifacts/test/*.ctrf.json
```

### 9. Group failures by error message (pattern analysis)
```bash
jq '[.results.tests[] | select(.status == "failed")] | group_by(.message) | map({
  error: .[0].message,
  count: length,
  tests: map(.name)
}) | sort_by(.count) | reverse' /workspace/artifacts/test/*.ctrf.json
```

Output:
```json
[
  {
    "error": "Expected status 200, got 403",
    "count": 15,
    "tests": ["test1", "test2", ...]
  },
  {
    "error": "Timeout waiting for response",
    "count": 8,
    "tests": ["test3", "test4", ...]
  }
]
```

### 10. Top 3 most common error patterns
```bash
jq '[.results.tests[] | select(.status == "failed")] | group_by(.message) | map({
  error: .[0].message,
  count: length
}) | sort_by(.count) | reverse | limit(3; .[])' /workspace/artifacts/test/*.ctrf.json
```

### 11. Extract unique file paths containing failures
```bash
jq -r '[.results.tests[] | select(.status == "failed") | .filePath] | unique | .[]' /workspace/artifacts/test/*.ctrf.json
```

### 12. Count failures per file
```bash
jq '[.results.tests[] | select(.status == "failed")] | group_by(.filePath) | map({
  file: .[0].filePath,
  failures: length
}) | sort_by(.failures) | reverse' /workspace/artifacts/test/*.ctrf.json
```

### 13. AI-friendly compact failure summary
```bash
jq -c '{
  summary: .results.summary,
  failures: [.results.tests[] | select(.status == "failed") | {
    name,
    suite,
    message,
    file: "\(.filePath // "N/A"):\(.line // "?")"
  }]
}' /workspace/artifacts/test/*.ctrf.json
```

---

## Performance Analysis

### 14. Slowest 10 tests
```bash
jq '.results.tests | sort_by(.duration) | reverse | limit(10; .[]) | {name, duration}' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 15. Slowest tests (formatted with milliseconds)
```bash
jq -r '.results.tests | sort_by(.duration) | reverse | limit(10; .[]) | "⏱️  \(.duration)ms - \(.name)"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output:
```
⏱️  3562ms - should handle DELETE_CHILD_BLOCKS correctly
⏱️  3419ms - should retrieve and verify sync database information
⏱️  2918ms - should find missing documents
```

### 16. Tests slower than threshold (e.g., 1000ms)
```bash
jq -r '.results.tests[] | select(.duration > 1000) | "\(.duration)ms - \(.name)"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 17. Average test duration
```bash
jq '.results.tests | (map(.duration) | add / length) | floor' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output: `330` (milliseconds)

### 18. Median test duration
```bash
jq '.results.tests | sort_by(.duration) | .[length / 2 | floor].duration' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 19. Performance percentiles (p50, p95, p99)
```bash
jq '.results.tests | sort_by(.duration) as $sorted | {
  p50: $sorted[($sorted | length) * 0.5 | floor].duration,
  p95: $sorted[($sorted | length) * 0.95 | floor].duration,
  p99: $sorted[($sorted | length) * 0.99 | floor].duration
}' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

---

## Flaky Test Detection

### 20. Tests with retries
```bash
jq -r '.results.tests[] | select(.retries > 0) | "⚠️  \(.name) (retries: \(.retries))"' /workspace/artifacts/test/*.ctrf.json
```

### 21. Tests marked as flaky
```bash
jq -r '.results.tests[] | select(.flaky == true) | "⚠️  \(.name)"' /workspace/artifacts/test/*.ctrf.json
```

### 22. Tests with retries AND flaky flag
```bash
jq -r '.results.tests[] | select(.retries > 0 or .flaky == true) | {
  name,
  retries: (.retries // 0),
  flaky: (.flaky // false)
}' /workspace/artifacts/test/*.ctrf.json
```

---

## Multi-Report Analysis

### 23. Cross-project failure summary
```bash
jq -s '{
  "notion-paper-sync": .[0].results.summary.failed,
  "rm-render-server": .[1].results.summary.failed,
  total: ((.[0].results.summary.failed // 0) + (.[1].results.summary.failed // 0))
}' /workspace/artifacts/test/notion-paper-sync.ctrf.json /workspace/artifacts/test/rm-render-server.ctrf.json
```

### 24. Aggregate stats across all projects
```bash
jq -s '{
  total_tests: (map(.results.summary.tests) | add),
  total_passed: (map(.results.summary.passed) | add),
  total_failed: (map(.results.summary.failed) | add),
  total_skipped: (map(.results.summary.skipped) | add)
}' /workspace/artifacts/test/*.ctrf.json
```

### 25. Combined failure pattern analysis (all projects)
```bash
jq -s '[
  .[].results.tests[] | select(.status == "failed")
] | group_by(.message) | map({
  error: .[0].message,
  count: length,
  affected_tests: map(.name)
}) | sort_by(.count) | reverse' /workspace/artifacts/test/*.ctrf.json
```

### 26. Per-project pass rates
```bash
jq -s 'map({
  project: (.reportId // "unknown"),
  tests: .results.summary.tests,
  passed: .results.summary.passed,
  pass_rate: ((.results.summary.passed / .results.summary.tests * 100) | floor)
})' /workspace/artifacts/test/*.ctrf.json
```

---

## Advanced Filters

### 27. Tests by status with counts
```bash
jq '.results.tests | group_by(.status) | map({
  status: .[0].status,
  count: length
})' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

Output:
```json
[
  { "status": "passed", "count": 333 },
  { "status": "failed", "count": 81 },
  { "status": "skipped", "count": 1 }
]
```

### 28. Tests by suite with stats
```bash
jq '[.results.tests[] | select(.suite)] | group_by(.suite) | map({
  suite: .[0].suite,
  total: length,
  passed: (map(select(.status == "passed")) | length),
  failed: (map(select(.status == "failed")) | length)
})' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 29. Failed tests in specific file
```bash
jq -r --arg file "src/composio.test.ts" '.results.tests[] | select(.status == "failed" and (.filePath | contains($file))) | .name' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 30. Tests containing specific text in name
```bash
jq -r --arg pattern "Composio" '.results.tests[] | select(.name | contains($pattern)) | "\(.status | ascii_upcase) - \(.name)"' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 31. Export failures as CSV
```bash
jq -r '.results.tests[] | select(.status == "failed") | [.name, .duration, .message // ""] | @csv' /workspace/artifacts/test/*.ctrf.json
```

Output:
```csv
"should execute CREATE tool sequence for new page",1038.5124999999998,"Expected status 200, got 403"
"should handle placeholder replacement correctly",1220.1826260000003,"Timeout waiting for response"
```

### 32. Full test details for debugging (pretty JSON)
```bash
jq '.results.tests[] | select(.name | contains("specific test name"))' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

---

## Utility Patterns

### 33. Count tests by pattern in name
```bash
jq -r --arg pattern "should" '[.results.tests[] | select(.name | contains($pattern))] | length' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 34. Tests without suite information
```bash
jq -r '.results.tests[] | select(.suite == null or .suite == "") | .name' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

### 35. Generate test inventory (all fields)
```bash
jq '.results.tests[] | {name, status, duration, suite, filePath}' /workspace/artifacts/test/notion-paper-sync.ctrf.json
```

---

## Tips & Tricks

### Using jq with multiple files
The `-s` (slurp) flag reads all files into an array:
```bash
jq -s '...' file1.ctrf.json file2.ctrf.json
```

### Using wildcards
Bash expands wildcards before passing to jq:
```bash
jq '...' /workspace/artifacts/test/*.ctrf.json
```

### Compact output (`-c`)
Remove whitespace for machine parsing:
```bash
jq -c '...' file.ctrf.json
```

### Raw output (`-r`)
Remove quotes from strings:
```bash
jq -r '...' file.ctrf.json
```

### Passing arguments to jq (`--arg`)
```bash
jq --arg myvar "value" '.results.tests[] | select(.name | contains($myvar))' file.ctrf.json
```

### Combining with shell tools
```bash
# Count lines
jq -r '.results.tests[] | select(.status == "failed") | .name' file.ctrf.json | wc -l

# Sort output
jq -r '.results.tests[].name' file.ctrf.json | sort

# Filter with grep
jq -r '.results.tests[].name' file.ctrf.json | grep "specific pattern"
```

---

## Common Use Cases

### Daily CI/CD Workflow
1. Check if any tests failed:
   ```bash
   jq '.results.summary.failed' /workspace/artifacts/test/*.ctrf.json
   ```

2. If failures > 0, get failure details:
   ```bash
   jq -r '.results.tests[] | select(.status == "failed") | "❌ \(.name)\n   Error: \(.message // "No message")\n"' /workspace/artifacts/test/*.ctrf.json
   ```

3. Identify slow tests for optimization:
   ```bash
   jq -r '.results.tests | sort_by(.duration) | reverse | limit(10; .[]) | "⏱️  \(.duration)ms - \(.name)"' /workspace/artifacts/test/*.ctrf.json
   ```

### Root Cause Analysis
1. Group failures by error message:
   ```bash
   jq '[.results.tests[] | select(.status == "failed")] | group_by(.message) | map({error: .[0].message, count: length, tests: map(.name)}) | sort_by(.count) | reverse' /workspace/artifacts/test/*.ctrf.json
   ```

2. Find which files contain the most failures:
   ```bash
   jq '[.results.tests[] | select(.status == "failed")] | group_by(.filePath) | map({file: .[0].filePath, failures: length}) | sort_by(.failures) | reverse' /workspace/artifacts/test/*.ctrf.json
   ```

3. Read the affected source files:
   ```bash
   # Extract file paths, then use Read tool
   jq -r '[.results.tests[] | select(.status == "failed") | .filePath] | unique | .[]' /workspace/artifacts/test/*.ctrf.json
   ```

### Performance Monitoring
1. Check p95 duration:
   ```bash
   jq '.results.tests | sort_by(.duration) as $sorted | $sorted[($sorted | length) * 0.95 | floor].duration' /workspace/artifacts/test/*.ctrf.json
   ```

2. Track duration over time (save to file, compare):
   ```bash
   jq '{timestamp: .timestamp, p95: (.results.tests | sort_by(.duration) as $sorted | $sorted[($sorted | length) * 0.95 | floor].duration)}' /workspace/artifacts/test/*.ctrf.json >> performance-history.jsonl
   ```

---

## References

- **CTRF Schema**: [ctrf-schema.json](./ctrf-schema.json)
- **CTRF Utilities**: [ctrf-utils.sh](./ctrf-utils.sh)
- **jq Manual**: https://jqlang.github.io/jq/manual/
- **CTRF Specification**: https://ctrf.io/docs/specification/overview
