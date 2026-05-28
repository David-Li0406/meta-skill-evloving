# Example: Changed Files Only Verification

## Scenario
Large codebase with 500+ tests. Only run tests for changed files.

## Verification Output

```
Running Verification Pipeline (Changed Files Only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Changed files detected:
  - src/components/UserForm.tsx
  - src/components/UserForm.test.tsx
  - src/utils/validation.ts

Step 1: Type Check (changed files)
$ npx tsc --noEmit src/components/UserForm.tsx src/utils/validation.ts
✓ PASS (0.8s)

Step 2: Lint (changed files)
$ npx eslint src/components/UserForm.tsx src/utils/validation.ts
✓ PASS (0.5s)

Step 3: Test (changed files only)
$ npm test -- --changedSince=HEAD~1
✓ PASS (2.1s)
  Tests: 8 passed (of 8 related)
  Full suite: 524 tests (skipped)

Step 4: Build (validation only)
$ npm run build -- --dry-run
✓ PASS (1.2s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verification Results:
  Typecheck: ✅ passed (changed files)
  Lint:      ✅ passed (changed files)
  Tests:     ✅ 8 passed (related tests)
  Build:     ✅ valid (dry run)

Total time: 4.6s (vs ~45s for full suite)
Status: CHANGED FILES PASSED ✓

Note: Full suite recommended before merge.
```

## When to Use Changed-Only

| Scenario | Use Changed-Only |
|----------|------------------|
| During TDD cycle | ✅ Yes |
| After each small fix | ✅ Yes |
| Before signaling READY_FOR_QA | ❌ No (full suite) |
| Final verification | ❌ No (full suite) |

## Commands

```bash
# TypeScript - changed only
npx tsc --noEmit $(git diff --name-only HEAD~1 | grep '\.tsx\?$')

# ESLint - changed only
npx eslint $(git diff --name-only HEAD~1 | grep '\.tsx\?$')

# Jest - changed since last commit
npm test -- --changedSince=HEAD~1

# Jest - related to changed files
npm test -- --findRelatedTests $(git diff --name-only HEAD~1)
```

## Filtered Summary

```
✓ VERIFICATION PASSED (changed files)
─────────────────────
Changed: 3 files
Typecheck: passed
Lint: passed
Tests: 8 related passed
─────────────────────
Time: 4.6s (10x faster than full)
```
