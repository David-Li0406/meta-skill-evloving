---
name: error-handler
description: 'Standardized error responses for all failure scenarios. Always transparent, always provide next steps.'
---

## Purpose

Handle failures gracefully:
- Post clear error messages to issues
- Provide troubleshooting steps
- Preserve partial progress
- Never fail silently

## Usage

Include this file when handling errors:

```
Use lib/error-handler to handle [error type] gracefully
```

## Error Response Templates

### 1. Issue Validation Failed

**When:** Issue missing trigger label, closed, or not found

**Template:**
\`\`\`markdown
⚠️ **Cannot Process Issue**

This issue needs the \`claude:auto-fix\` label to be processed automatically.

**To enable automatic handling:**
\`\`\`bash
gh issue edit <issue-number> --add-label "claude:auto-fix"
\`\`\`

Then run: \`/handle-issue <issue-number>\`
\`\`\`

**Post to:** Issue comment
**Exit:** Gracefully (not a failure)

### 2. Code Exploration Found Nothing

**When:** Targeted search and deep analysis return no results

**Template:**
\`\`\`markdown
🔍 **Analysis Incomplete**

I searched the codebase but couldn't confidently locate code related to this issue.

**What I searched for:**
- Keywords: \`<keyword1>\`, \`<keyword2>\`, \`<keyword3>\`
- File patterns: \`**/*<pattern>*.{ts,js}\`
- Error traces: <extracted errors>

**Possible reasons:**
- Issue description may need more technical details (file names, function names, error messages)
- Code may be in a different location than expected
- Issue may require domain knowledge I don't have

**Next steps:**
- Add more technical details to the issue description
- Mention specific files or functions involved
- Run \`/handle-issue <issue-number>\` again after updating

Alternatively, this may require manual investigation.
\`\`\`

**Post to:** Issue comment
**Exit:** Gracefully (partial success)

### 3. Approval Check Failed

**When:** Can't access GitHub API, can't parse comments

**Template:**
\`\`\`markdown
⚠️ **Approval Check Failed**

I couldn't verify approval due to an error:
\`\`\`
<error message>
\`\`\`

**Manual verification:**
1. Ensure you've approved the plan (👍 or 'approve' comment)
2. Check GitHub CLI is authenticated: \`gh auth status\`
3. Try again: \`/continue-issue <issue-number>\`

If the error persists, you can implement the plan manually using the details above.
\`\`\`

**Post to:** Issue comment
**Exit:** Error (but actionable)

### 4. Worktree Creation Failed

**When:** Branch exists, directory conflicts, git errors

**Template:**
\`\`\`markdown
⚠️ **Worktree Setup Failed**

Couldn't create isolated workspace:
\`\`\`
<error message>
\`\`\`

**Common fixes:**
\`\`\`bash
# If branch exists from previous attempt
git worktree remove .worktrees/fix-issue-<number> --force
git branch -D fix/issue-<number>

# Then retry
/continue-issue <issue-number>
\`\`\`

**Manual alternative:**
\`\`\`bash
git checkout -b fix/issue-<number>
# Implement changes from plan above
\`\`\`
\`\`\`

**Post to:** Issue comment
**Exit:** Error (but recoverable)

### 5. Implementation Failed

**When:** Tests fail, compilation errors, execution issues

**Strategy:** Commit partial progress, create draft PR

**Step 1: Post issue comment:**
\`\`\`markdown
⚠️ **Implementation Completed with Issues**

PR created: #<pr-number> (draft)

The automated fix encountered some problems but progress has been committed. Please review the draft PR and complete remaining work.

**What worked:**
- ✅ <completed change 1>
- ✅ <completed change 2>

**What needs attention:**
- ❌ <failed test or error>
- ❌ <another issue>
\`\`\`

**Step 2: Create draft PR:**
\`\`\`bash
gh pr create \
  --title "[WIP] Fix: <issue title>" \
  --body "$(cat <<'EOF'
## ⚠️ Automated Fix - Needs Review

Fixes #<issue-number>

**Status:** Implementation partially completed but encountered errors.

### What Was Completed
- ✅ <change 1>
- ✅ <change 2>

### What Failed
- ❌ Tests failing: <test names>
- Error: \`<error message>\`

### Next Steps
This PR contains the attempted fix but requires manual review:
1. Review the implemented changes
2. Fix the failing tests
3. Complete any remaining work from the plan

---
*Automated implementation encountered issues. Manual review required.*
EOF
)" \
  --label "automated-fix,needs-work" \
  --draft
\`\`\`

**Exit:** Partial success (work preserved)

### 6. PR Creation Failed

**When:** GitHub API errors, permission issues

**Template:**
\`\`\`markdown
✅ **Implementation Complete**

The fix has been implemented in branch: \`fix/issue-<issue-number>\`

**However**, PR creation failed:
\`\`\`
<error message>
\`\`\`

**Create PR manually:**
\`\`\`bash
gh pr create --head fix/issue-<issue-number>
\`\`\`

Or visit: https://github.com/<owner>/<repo>/compare/fix/issue-<issue-number>

**Changes made:**
- <file 1>: <description>
- <file 2>: <description>

All changes have been committed and pushed.
\`\`\`

**Post to:** Issue comment
**Exit:** Partial success (code ready, manual PR needed)

## Error Posting Function

```bash
function post_error() {
  local issue_number=$1
  local error_template=$2
  local error_message=$3

  # Replace placeholders
  local formatted_message="${error_template//<error message>/$error_message}"
  formatted_message="${formatted_message//<issue-number>/$issue_number}"

  # Post to GitHub
  gh issue comment "$issue_number" --body "$formatted_message"

  # Log locally for debugging
  echo "[ERROR] Issue #$issue_number: $error_message" >> ~/.claude/errors.log
}
```

## Error Detection

### GitHub CLI Errors

```bash
gh issue view 999 --json title 2>&1
```

If output contains:
- `"could not resolve to an Issue"` → Issue not found
- `"HTTP 401"` → Authentication failed
- `"HTTP 403"` → Permission denied
- `"HTTP 404"` → Repository not found

### Git Errors

```bash
git worktree add .worktrees/test 2>&1
```

If output contains:
- `"already exists"` → Branch or worktree exists
- `"not a git repository"` → Not in git repo
- `"fatal: invalid reference"` → Invalid branch name

### Execution Errors

When spawning agents or executing commands:
- Timeout after 10 minutes
- Capture stdout and stderr
- Check exit codes

## Recovery Strategies

### 1. Retry with Backoff

For transient GitHub API errors:

```bash
function retry_gh_command() {
  local max_attempts=3
  local attempt=1
  local delay=5

  while [ $attempt -le $max_attempts ]; do
    if $@; then
      return 0
    fi

    echo "Attempt $attempt failed, retrying in ${delay}s..."
    sleep $delay
    delay=$((delay * 2))
    attempt=$((attempt + 1))
  done

  return 1
}

# Usage
retry_gh_command gh issue view 123 --json title
```

### 2. Partial Progress Preservation

Always commit work before failing:

```bash
# Before any risky operation
git add -A
git commit -m "wip: partial implementation before <operation>" || true

# Try operation
if ! risky_operation; then
  # Committed work is preserved
  post_error <issue> "implementation_failed" "$error"
fi
```

### 3. Graceful Degradation

If fancy features fail, fall back to basics:

```
Deep analysis fails → Use only targeted search
Worktree fails → Suggest manual branch creation
PR creation fails → Show manual commands
```

## Integration Points

### In handle-issue Command

```
Fetch issue → FAIL? → Error template #1
Parse issue → (always succeeds)
Search code → FAIL? → Error template #2
Generate plan → (always succeeds)
Post plan → FAIL? → Error template #3
```

### In continue-issue Command

```
Check approval → FAIL? → Error template #3
Create worktree → FAIL? → Error template #4
Implement fix → FAIL? → Error template #5
Create PR → FAIL? → Error template #6
```

## Logging

All errors logged to help debugging:

```bash
# ~/.claude/github-issue-handler.log

[2026-01-16 10:00:00] INFO: handle-issue 42 started
[2026-01-16 10:00:05] ERROR: gh CLI failed: HTTP 401
[2026-01-16 10:00:05] ERROR: Posted error template #3 to issue 42
[2026-01-16 10:00:05] EXIT: Graceful exit with code 1
```

## YAGNI Notes

**Not included:**
- Sentry/error tracking service
- Email notifications on errors
- Automatic retry loops (except for API rate limits)
- Error analytics/metrics

Keep it simple: post to GitHub, log locally, provide next steps.
