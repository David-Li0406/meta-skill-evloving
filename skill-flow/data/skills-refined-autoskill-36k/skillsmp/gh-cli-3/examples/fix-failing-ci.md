# Example: Fix Failing CI Workflow

Complete real-world scenario for diagnosing and fixing a failing GitHub Actions workflow.

## Scenario

You've pushed changes to a PR, and the CI workflow is failing. You need to:
1. Identify what's failing
2. Download and analyze logs
3. Fix the problem
4. Verify the fix

## Step 1: Identify the Failing Run

```bash
$ gh run list --limit 5
```

**Expected Output:**
```
✓  feat: Add user authentication   CI       main  push  3m ago
✓  fix: Update dependencies        CI       main  push  1h ago
X  feat: Add export feature        CI       feat-export  push  5m ago  ← This one failed
✓  docs: Update README             CI       main  push  2h ago
✓  chore: Bump version             CI       main  push  3h ago
```

Get the failing run ID:

```bash
$ FAILED_RUN=$(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')
$ echo $FAILED_RUN
```

**Expected Output:**
```
7890123456
```

## Step 2: View Run Summary

```bash
$ gh run view $FAILED_RUN
```

**Expected Output:**
```
X feat: Add export feature · 7890123456
Triggered via push about 5 minutes ago

JOBS
X test (16.10s)
X lint (8.22s)
✓ build (23.45s)

ANNOTATIONS
X test: Process completed with exit code 1.
X lint: Process completed with exit code 1.

For more information about this run, view the logs:
  gh run view 7890123456 --log

To rerun this run, run:
  gh run rerun 7890123456
```

The `test` and `lint` jobs failed. Let's investigate.

## Step 3: Download Failed Logs

```bash
$ gh run view $FAILED_RUN --log-failed > failed-logs.txt
$ ls -lh failed-logs.txt
```

**Expected Output:**
```
-rw-r--r--  1 user  staff   24K Jan 19 10:30 failed-logs.txt
```

## Step 4: Analyze Test Failures

```bash
$ grep -A 5 "FAILED\|Error:" failed-logs.txt
```

**Expected Output:**
```
test/export.test.js:42:15
  FAILED: test should export data in CSV format
    Error: Expected CSV header to include "email" field
    Expected: "name,email,created_at"
    Received: "name,created_at"

test/export.test.js:67:20
  FAILED: test should handle empty datasets
    TypeError: Cannot read property 'length' of undefined
    at exportToCSV (src/export.js:23:15)
```

Two issues found:
1. Missing "email" field in CSV export header
2. Crash when dataset is empty (null/undefined handling)

## Step 5: Analyze Lint Failures

```bash
$ grep -A 3 "error\|warning" failed-logs.txt | grep -v "test/"
```

**Expected Output:**
```
src/export.js:23:5
  error: 'data' is possibly 'undefined'  @typescript-eslint/no-unsafe-member-access

src/export.js:45:10
  error: Missing return type on function  @typescript-eslint/explicit-function-return-type
```

Lint issues:
1. No null check on `data` parameter
2. Missing return type annotation

## Step 6: Examine the Code

```bash
$ cat src/export.js
```

**Current Code:**
```javascript
export function exportToCSV(data) {
  // Missing null check!
  const header = `name,created_at\n`;  // Email field missing!

  const rows = data.map(item => {
    return `${item.name},${item.created_at}`;
  }).join('\n');

  return header + rows;
}
```

## Step 7: Fix the Issues

**Fix 1: Add email field to header and data**

```javascript
export function exportToCSV(data): string {
  // Add null check
  if (!data || data.length === 0) {
    return 'name,email,created_at\n';
  }

  // Include email field
  const header = `name,email,created_at\n`;

  const rows = data.map(item => {
    return `${item.name},${item.email},${item.created_at}`;
  }).join('\n');

  return header + rows;
}
```

Save the fix:

```bash
$ cat > src/export.js << 'EOF'
export function exportToCSV(data): string {
  if (!data || data.length === 0) {
    return 'name,email,created_at\n';
  }

  const header = `name,email,created_at\n`;

  const rows = data.map(item => {
    return `${item.name},${item.email},${item.created_at}`;
  }).join('\n');

  return header + rows;
}
EOF
```

## Step 8: Run Tests Locally (Optional but Recommended)

```bash
$ npm test src/export.test.js
```

**Expected Output:**
```
PASS test/export.test.js
  ✓ should export data in CSV format (12ms)
  ✓ should handle empty datasets (3ms)
  ✓ should include all required fields (8ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
```

## Step 9: Commit and Push the Fix

```bash
$ git add src/export.js
$ git commit -m "fix: Add email field to CSV export and handle empty datasets

- Include email field in CSV header and data rows
- Add null check to prevent crash on undefined data
- Add TypeScript return type annotation

Fixes the failing test and lint checks in CI."

$ git push
```

**Expected Output:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 456 bytes | 456.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/user/repo.git
   abc1234..def5678  feat-export -> feat-export
```

## Step 10: Check if Workflow Triggers Automatically

```bash
$ EVENT=$(gh run view $FAILED_RUN --json event --jq '.event')
$ echo "Workflow triggered by: $EVENT"
```

**Expected Output:**
```
Workflow triggered by: push
```

Since this is a `push` event, the new commit will automatically trigger the workflow. No manual rerun needed!

## Step 11: Watch the New Run

```bash
# Get the latest run
$ sleep 10  # Give it a moment to start
$ NEW_RUN=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')
$ echo "New run ID: $NEW_RUN"

# Watch it in real-time
$ gh run watch $NEW_RUN
```

**Expected Output:**
```
Refreshing run status every 3 seconds. Press Ctrl+C to quit.

✓ feat: Add export feature · 7890123457 · 12s
✓ test (15.23s)
✓ lint (7.89s)
✓ build (22.11s)

Run completed with 'success' status
```

Success! The CI is now passing.

## Alternative: Manual Rerun (if needed)

If the workflow doesn't auto-trigger (e.g., scheduled or workflow_dispatch events), manually rerun:

```bash
# Check if rerun is needed
$ EVENT=$(gh run view $FAILED_RUN --json event --jq '.event')

if [ "$EVENT" != "push" ] && [ "$EVENT" != "pull_request" ]; then
  echo "Manual rerun needed for event type: $EVENT"
  gh run rerun $FAILED_RUN
else
  echo "New commit will trigger automatically"
fi
```

## Full Automation Script

Combine everything into a reusable script:

```bash
#!/bin/bash
# fix-ci-failures.sh - Diagnose and report CI failures

set -euo pipefail

# Get most recent failed run
FAILED_RUN=$(gh run list --status failure --limit 1 --json databaseId --jq '.[0].databaseId')

if [ -z "$FAILED_RUN" ] || [ "$FAILED_RUN" = "null" ]; then
  echo "No failed runs found!"
  exit 0
fi

echo "Analyzing failed run: $FAILED_RUN"
echo ""

# Show summary
echo "=== Run Summary ==="
gh run view "$FAILED_RUN"
echo ""

# Download failed logs
echo "=== Failed Job Logs ==="
gh run view "$FAILED_RUN" --log-failed > /tmp/failed-logs.txt

# Extract key errors
echo "=== Test Failures ==="
grep -A 3 "FAILED\|Error:" /tmp/failed-logs.txt | head -20 || echo "No test failures found"
echo ""

echo "=== Lint Errors ==="
grep -A 2 "error:" /tmp/failed-logs.txt | grep -v "test/" | head -20 || echo "No lint errors found"
echo ""

echo "=== Full logs saved to: /tmp/failed-logs.txt ==="
echo ""
echo "After fixing issues, commit and push:"
echo "  git add ."
echo "  git commit -m 'fix: Resolve CI failures'"
echo "  git push"
echo ""
echo "To watch the new run:"
echo "  sleep 10 && gh run watch \$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')"
```

**Usage:**
```bash
$ chmod +x fix-ci-failures.sh
$ ./fix-ci-failures.sh
```

## Summary of Workflow

1. ✅ List recent runs, identify failures
2. ✅ View run summary to see which jobs failed
3. ✅ Download failed logs for analysis
4. ✅ Extract error messages and identify root cause
5. ✅ Fix code issues (missing fields, null handling, type annotations)
6. ✅ Verify fix with local tests
7. ✅ Commit with descriptive message
8. ✅ Push changes (auto-triggers workflow)
9. ✅ Watch new run to confirm fix

**Key Insights:**
- Always download logs first - web UI can be slow
- Use `grep` to extract relevant errors quickly
- Test locally before pushing when possible
- Push events auto-trigger workflows, no manual rerun needed
- Descriptive commit messages help track fixes

## Common CI Failure Patterns

**Test failures:**
- Missing test data
- API changes breaking tests
- Async timing issues
- Environment differences (local vs CI)

**Lint failures:**
- Missing type annotations
- Unused variables
- Formatting issues
- Import order

**Build failures:**
- Missing dependencies
- Version mismatches
- Environment variable configuration
- Build tool updates

**Solution strategy:**
1. Read the error message carefully
2. Check recent changes that might have caused it
3. Reproduce locally if possible
4. Fix the specific issue (don't fix unrelated things)
5. Verify the fix
6. Push and confirm in CI
