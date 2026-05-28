---
name: test-report
description: Open and analyze Playwright HTML test reports. Use when user asks to see test results, check test report, view test output, or analyze test failures.
allowed-tools: Bash(npx:*), Bash(open:*), Bash(xdg-open:*), Read, Grep, Glob
---

# Test Report Viewer

## Instructions

### 1. Open HTML Report
```bash
# Open Playwright HTML report
npx playwright show-report
```

The report will open in the default browser showing:
- Test results summary
- Failed test details
- Screenshots and videos
- Test traces

### 2. Analyze Report Files (if needed)

**Check for report existence:**
```bash
ls -la playwright-report/
```

**Check recent test results:**
```bash
# List recent test runs
ls -lt playwright-report/ | head -10

# Check for failures
grep -r "failed" playwright-report/ 2>/dev/null || echo "No failures found"
```

### 3. Provide Summary

If analyzing results, provide:
- Total tests: passed/failed/skipped
- Failed test names
- Common failure patterns
- Screenshots/traces available

### 4. Troubleshooting

**If report doesn't exist:**
```bash
# Run tests first
npx playwright test

# Then show report
npx playwright show-report
```

**Alternative: Direct file access**
```bash
# Open report HTML directly (macOS)
open playwright-report/index.html

# Linux
xdg-open playwright-report/index.html
```

## Tips

- The report includes interactive filtering by status, browser, file
- Click on failed tests to see detailed error messages and traces
- Screenshots are embedded for visual verification
- Trace viewer allows step-by-step debugging
