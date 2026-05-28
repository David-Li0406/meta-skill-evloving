# Step 5: Execution Loop (Auto-Healing)

**Duration**: ~4-8 minutes
**Purpose**: Execute tests with self-healing capability.

---

## Execution Algorithm

```
MAX_RETRIES = 3
attempt = 1

WHILE attempt <= MAX_RETRIES:
  1. Execute: npx playwright test --project={projectName}
  2. IF ALL PASS -> Break, proceed to Step 6
  3. IF FAIL -> Analyze, Heal, Retry
  4. IF attempt > 3 -> Mark as fixme, proceed
```

---

## Test Execution

### Run Tests

```bash
# Run specific test file
npx playwright test automation/playwright/tests/{feature}/{test}.spec.ts

# Run with specific project
npx playwright test --project=chrome-serial

# Run with UI mode for debugging
npx playwright test --ui
```

### Capture Results

```bash
# Generate HTML report
npx playwright test --reporter=html

# Generate JSON for analysis
npx playwright test --reporter=json
```

---

## Failure Analysis

### With Exolar MCP (Recommended)

Query detailed failure data:

```typescript
const failures = await mcp.exolar.query_exolar_data({
  dataset: "execution_failures",
  filters: { execution_id: executionId },
  view_mode: "detailed"
})
```

Classify each failure:

```typescript
const classification = await mcp.exolar.perform_exolar_action({
  action: "classify",
  params: { execution_id, test_name }
})
// Result: "FLAKE" | "BUG" | "ENVIRONMENT"
```

### Without Exolar (Fallback)

Parse local test output:

```bash
# Read failure details from report
cat playwright-report/results.json | jq '.suites[].specs[] | select(.ok == false)'
```

---

## Auto-Healing Rules

### Common Fixes

| Error Pattern | Auto-Fix |
|---------------|----------|
| `Locator resolved to 0 elements` | Add `:visible` filter |
| `Timeout of 30000ms exceeded` | Use `getTimeout()` helper |
| `strict mode violation: N elements` | Add `.first()` to chain |
| `401 Unauthorized` | Delete `.auth/`, recreate |
| `Element not interactable` | Add `.scrollIntoViewIfNeeded()` |
| `Navigation failed` | Use `waitUntil: 'domcontentloaded'` |

### Healing Process

1. **Identify failure type** from error message
2. **Locate failing line** in test file
3. **Apply fix** using test-healer agent:

```typescript
Task({
  subagent_type: 'playwright-test-healer',
  prompt: `Fix failing test:
    File: ${testFile}
    Error: ${errorMessage}
    Line: ${lineNumber}`
})
```

4. **Re-run test** to verify fix
5. **Commit fix** if successful

---

## Retry Logic

### Attempt 1: Initial Run
- Execute tests as generated
- Capture all failures

### Attempt 2: First Heal
- Apply auto-fixes for known patterns
- Retry with updated code

### Attempt 3: Deep Heal
- More aggressive fixes
- Add retry logic to flaky assertions
- Consider marking as `test.fixme()` if still failing

### After 3 Attempts
```typescript
test.fixme('Feature test - needs manual review', async () => {
  // Original test code
  // Failed after 3 auto-heal attempts
  // See PR comments for failure details
})
```

---

## Output

### Success
All tests passing, proceed to Step 6.

### Partial Success
- Passing tests proceed normally
- Failing tests marked with `test.fixme()`
- Documented in PR for manual review

### Failure Metrics
```markdown
## Execution Summary
- Total tests: 10
- Passed: 8
- Fixed (auto-healed): 1
- Fixme (needs review): 1

## Auto-Healing Applied
1. `login.spec.ts:45` - Added `:visible` filter
2. `checkout.spec.ts:78` - Used `getTimeout('navigation')`
```

---

## Debug Mode

For stubborn failures, run with debug output:

```bash
# Headed mode with slowMo
npx playwright test --headed --debug

# Trace on failure
npx playwright test --trace on

# Step through with inspector
PWDEBUG=1 npx playwright test
```
