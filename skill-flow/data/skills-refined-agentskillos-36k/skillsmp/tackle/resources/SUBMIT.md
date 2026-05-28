# Submit Phase

Mark the draft PR as ready for review after gate-submit approval.

> **IMPORTANT: Never reference local beads issue IDs (gt-xxx, hq-xxx) in upstream PRs.**
> Local beads are internal tracking - they mean nothing to upstream maintainers.
> Only reference GitHub issue numbers if they exist on the upstream repo.

## Pre-Submit Checklist

Before this phase, verify:
1. gate-submit step is closed (was approved)
2. **CI completed successfully** (checked via ci-status-check.sh in gate-submit)

**⚠️ NEVER mark a PR ready if CI is still running or has new failures.**

If you're unsure about CI status, check it now:
```bash
gh pr view $PR_NUMBER --repo $ORG_REPO --json statusCheckRollup --jq '.statusCheckRollup[] | "\(.name): \(.conclusion // "PENDING")"'
```

All checks must show SUCCESS or be known pre-existing failures. If any show PENDING, wait.

## Mark PR Ready

The draft PR was created during gate-submit (see SKILL.md for idempotent PR check).
Now we mark it ready for maintainer review.

### 1. Get PR Number

PR info should be available from gate-submit (via `pr-check-idempotent.sh`). If resuming:

```bash
# Use pr-check-idempotent.sh which correctly handles fork owner detection
source "$SKILL_DIR/resources/scripts/pr-check-idempotent.sh"
# Sets: PR_NUMBER, IS_DRAFT, PR_URL, BRANCH, FORK_OWNER
```

### 2. Mark Draft as Ready

```bash
gh pr ready $PR_NUMBER --repo $ORG_REPO
```

### 3. Verify PR is Ready

```bash
source "$SKILL_DIR/resources/scripts/verify-pr-ready.sh"
# Sets: IS_DRAFT, PR_STATE, PR_URL
# Exits 1 if still draft
```

### 4. PR URL

`PR_URL` is set by the scripts above.

## PR Title and Body Reference

If you need to update the PR before marking ready:

```bash
# Update title
gh pr edit $PR_NUMBER --repo $ORG_REPO --title "<new-title>"

# Update body
gh pr edit $PR_NUMBER --repo $ORG_REPO --body "<new-body>"
```

### Title Format

From cached `research.yaml`:
```yaml
pull_requests:
  title_format: null  # or specific format
```

Default format: `<type>(<scope>): <description>`

Examples:
- `fix(doctor): correct indentation in database check`
- `feat(sync): add progress indicator`
- `docs(readme): update installation instructions`

### Body Format

Use template if available, otherwise:

```markdown
## Summary

<Brief description of what this PR does>

## Changes

- <Change 1>
- <Change 2>

## Test Plan

- [ ] <How to test change 1>
- [ ] <How to test change 2>

## Checklist

- [x] Tests pass
- [x] Linter passes
- [x] Rebased on upstream default branch
- [x] Single concern (isolation verified)
```

## Update Molecule

```yaml
phase: "record"
pr:
  url: "https://github.com/org/repo/pull/123"
  number: 123
  submitted_at: "2026-01-19T12:00:00Z"
```

## Record Phase

After PR submission:

### What Gets Closed When?

**Molecule vs Issue - they're separate:**

| Thing | When to Close | Why |
|-------|---------------|-----|
| **Molecule** (gt-mol-xxx) | After reflect step | Workflow complete, PR submitted |
| **Issue/task bead** (hq-xxx) | After PR outcome | Work not done until fix is in upstream |

- Closing the molecule does NOT close the issue
- Issue gets `pr-submitted` label and `deferred` status until PR outcome is known
- PR outcomes are checked in step 6 (Check Pending PR Outcomes) on future tackle invocations

This separation allows tracking issues through the full lifecycle, even if PRs need revisions or take time to merge.

### 1. Update Local Issue

```bash
source "$SKILL_DIR/resources/scripts/record-pr-stats.sh"
# Requires: ISSUE_ID, PR_URL, UPSTREAM_REF
# Sets: FILES_CHANGED, LINES_CHANGED
# Updates issue with pr-submitted label, deferred status, and PR info
```

The molecule and issue history provide the audit trail for learning.

### 2. Final Output

```
## PR Submitted

Issue:    hq-1234 - Fix doctor indentation
PR:       https://github.com/steveyegge/beads/pull/123
Status:   Awaiting review

To check PR status later:
  gh pr view 123 --repo steveyegge/beads
```

**⚠️ WORKFLOW NOT COMPLETE** - You must still complete the reflect step before you are done.

### 3. Advance to Reflect

```bash
bd close <record-step-id> --continue
```

Use `bd ready` to find the reflect step.

## Error Handling

### Push Fails

```
Error: Failed to push branch

Possible causes:
- No push access to origin
- Branch already exists remotely

Solutions:
- Verify remote: git remote -v
- Force push if needed: git push -f origin <branch>
- Use different branch name
```

### PR Ready Fails

```
Error: gh pr ready failed

Possible causes:
- PR doesn't exist
- Network issue
- Permission denied

Solutions:
- Check PR exists: gh pr view $PR_NUMBER --repo <upstream>
- Retry: gh pr ready $PR_NUMBER --repo <upstream>
```

