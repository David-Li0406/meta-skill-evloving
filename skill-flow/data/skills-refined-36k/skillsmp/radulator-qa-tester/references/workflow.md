# Radulator QA Workflow Guide

## Three-Branch Strategy

The Radulator repository follows a three-branch workflow:

```
dev1 (development) → test1 (staging) → main (production)
```

### Branch Purposes

- **dev1**: Active development branch where new calculators and features are built
- **test1**: Staging branch where code is tested before production deployment
- **main**: Production branch containing only fully tested, working code

## PR Testing Workflow

### 1. Development Phase (dev1)

Developer works on a calculator in `dev1` and creates a pull request into `test1`.

**Required PR Labels:**
- `qa`: Indicates the PR should trigger automated QA testing

### 2. Automated Testing Phase (PR into test1)

When a PR is opened from `dev1` → `test1`:

1. **Detect Changed Calculators**
   - Parse the PR diff to identify which calculator files changed
   - Look for changes in: `src/components/calculators/*.jsx`
   - Extract calculator name from filename

2. **Setup Test Environment**
   - Clone the PR branch
   - Run `npm install` to install dependencies
   - Start Vite dev server: `npm run dev` (typically on port 5173)
   - Wait for "ready" message in console

3. **Run Playwright Tests**
   - Use Playwright MCP to navigate to `http://localhost:PORT`
   - Select the changed calculator from sidebar
   - Fill inputs with predefined test values (from `references/test_cases.md`)
   - Click "Calculate" button
   - Capture output values

4. **Verify Results**
   - Run `scripts/verify_calculators.py` to compute expected values
   - Compare actual output vs. expected output
   - Check for discrepancies (tolerance: ±0.1 for percentages, ±0.01 for densities)

5. **Collect Diagnostics**
   - Call `browser_console_messages` to capture any JavaScript errors
   - Call `browser_network_requests` to verify no unexpected API calls
   - Call `browser_take_screenshot` to document the test state
   - Save all diagnostics for the report

6. **Generate Regression Tests**
   - Use `browser_generate_playwright_test` to create reusable test
   - Save generated test to `tests/<calculator-name>.spec.js`
   - Commit the test file to a branch: `qa/<calculator-name>`

7. **Report Results**
   - Create detailed test report with:
     - Test inputs used
     - Expected values (with formulas)
     - Actual values from web app
     - Any deviations or errors
     - Console logs (if errors present)
     - Screenshot of results
     - Recommended fixes (if tests failed)
   - Post report as comment on the PR using GitHub MCP

8. **Merge Decision**
   - **If all tests pass**: Merge PR into `test1`, add comment "✅ QA: All tests passed"
   - **If tests fail**: Do NOT merge, add comment with failure details, wait for fixes

### 3. Staging to Production (test1 → main)

After successful merge to `test1`:

1. **Create Production PR**
   - Open PR from `test1` → `main`
   - Add `qa` label

2. **Repeat Testing**
   - Run the same test suite against `test1` branch
   - Verify no regressions occurred during merge

3. **Production Merge**
   - **If tests pass**: Merge to `main`, deploy to production
   - **If tests fail**: Investigate regression, fix in `test1`

## MCP Tools Reference

### Playwright MCP Tools

- `browser_navigate`: Navigate to URL
- `browser_click`: Click elements by selector
- `browser_type`: Type into input fields
- `browser_console_messages`: Get console logs
- `browser_network_requests`: Get network activity
- `browser_take_screenshot`: Capture screenshot
- `browser_generate_playwright_test`: Generate test code

### GitHub MCP Tools

- `list_pull_requests`: Get PRs for repo
- `get_pull_request`: Get PR details and diff
- `create_comment`: Add comment to PR
- `merge_pull_request`: Merge PR if approved
- `create_pull_request`: Open new PR
- `list_files`: Get repo file list

## Test Coverage Goals

Each calculator should have:
- ✅ At least 2 test cases (normal + edge case)
- ✅ Automated Playwright regression test
- ✅ Formula verification script
- ✅ Console error monitoring
- ✅ Screenshot documentation

## Quality Gates

Before merging to `test1`:
- ✅ All calculations accurate within tolerance
- ✅ No console errors
- ✅ Results render in < 500ms
- ✅ UI elements properly labeled
- ✅ References section complete

Before merging to `main`:
- ✅ All `test1` quality gates passed
- ✅ No regressions detected
- ✅ Playwright tests committed to repo
- ✅ Documentation updated
