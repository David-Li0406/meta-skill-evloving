# Example: Successful Verification Run

## Scenario
Running full verification pipeline after implementing a feature.

## Verification Output

```
Running Verification Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Type Check
$ npm run typecheck
✓ PASS (2.1s)

Step 2: Lint
$ npm run lint
✓ PASS (1.8s)
  Auto-fixed: 2 issues

Step 3: Test
$ npm test -- --changedSince=HEAD~1
✓ PASS (4.2s)
  Tests: 12 passed, 0 failed

Step 4: Build
$ npm run build
✓ PASS (8.3s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verification Results:
  Typecheck: ✅ passed
  Lint:      ✅ passed (2 auto-fixed)
  Tests:     ✅ 12 passed, 0 failed
  Build:     ✅ success

Total time: 16.4s
Status: ALL PASSED ✓
```

## Filtered Output (Anthropic Best Practice)

Instead of full output (~500 tokens), filtered output (~50 tokens):

```
✓ VERIFICATION PASSED
─────────────────────
Typecheck: passed
Lint: passed (2 auto-fixed)
Tests: 12 passed, 0 failed
Build: success (8.3s)
─────────────────────
Total: 16.4s
```

## Progress Update

```yaml
# Update to .claude/auto-progress.yaml
verification:
  last_run: "2025-01-18T10:15:00Z"
  status: passed
  results:
    typecheck: passed
    lint: passed
    test: "12 passed, 0 failed"
    build: passed
  duration: 16.4
```
