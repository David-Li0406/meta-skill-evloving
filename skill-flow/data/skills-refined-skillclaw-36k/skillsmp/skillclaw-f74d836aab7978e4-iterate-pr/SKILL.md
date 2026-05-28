---
name: iterate-pr
description: Use this skill when you need to fix CI failures, address review feedback, or continuously push fixes until all checks are green. It automates the feedback-fix-push-wait cycle for pull requests.
---

# Iterate on PR Until CI Passes

Continuously iterate on the current branch until all CI checks pass and review feedback is addressed.

**Requires**: GitHub CLI (`gh`) authenticated and available.

## Process

### Step 1: Identify the PR

```bash
gh pr view --json number,url,headRefName,baseRefName
```
If no PR exists for the current branch, stop and inform the user.

### Step 2: Check CI Status First

Always check CI/GitHub Actions status before looking at review feedback:

```bash
gh pr checks --json name,state,bucket,link,workflow
```
The `bucket` field categorizes state into: `pass`, `fail`, `pending`, `skipping`, or `cancel`.

**Important:** If any of these checks are still `pending`, wait before proceeding:
- `sentry` / `sentry-io`
- `codecov`
- `cursor` / `bugbot` / `seer`
- Any linter or code analysis checks

These bots may post additional feedback comments once their checks complete. Waiting avoids duplicate work.

### Step 3: Gather Review Feedback

Once CI checks have completed (or at least the bot-related checks), gather human and bot feedback:

**Review Comments and Status:**
```bash
gh pr view --json reviews,comments,reviewDecision
```

**Inline Code Review Comments:**
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

**PR Conversation Comments (includes bot comments):**
```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments
```
Look for bot comments from: Sentry, Codecov, Cursor, Bugbot, Seer, and other automated tools.

### Step 4: Investigate Failures

For each CI failure, get the actual logs:

```bash
# List recent runs for this branch
gh run list --branch $(git branch --show-current) --limit 5 --json databaseId,name,status,conclusion

# View failed logs for a specific run
gh run view <run-id> --log-failed
```
Do NOT assume what failed based on the check name alone. Always read the actual logs.

### Step 5: Validate Feedback

For each piece of feedback (CI failure or review comment):

1. **Read the relevant code** - Understand the context before making changes.
2. **Verify the issue is real** - Not all feedback is correct; reviewers and bots can be wrong.
3. **Check if already addressed** - The issue may have been fixed in a subsequent commit.
4. **Skip invalid feedback** - If the feedback is not applicable, disregard it.