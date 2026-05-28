---
name: pr-completion
description: Ensure PR checks pass and conflicts are resolved before completing tasks. Use after creating a PR, when marking tasks as done, or when completing work that resulted in a PR.
---

# PR Completion Workflow

Before marking a task as done after creating a PR, verify:

1. All PR checks pass
2. No merge conflicts exist

## Check PR Status

```bash
# View PR checks
gh pr checks

# View PR status (includes mergeable state)
gh pr view --json state,mergeable,mergeStateStatus
```

## Wait for Checks

If checks are pending:

```bash
# Wait for checks to complete (blocking)
gh pr checks --watch
```

If checks fail:
1. Read check logs: `gh pr checks --json name,state,conclusion`
2. Fix failing checks
3. Push fixes
4. Re-verify with `gh pr checks --watch`

## Resolve Conflicts

If PR has conflicts (`mergeable: CONFLICTING`):

```bash
# Update branch from base
gh pr update-branch

# Or rebase locally
git fetch origin
git rebase origin/main
# Resolve conflicts
git add .
git rebase --continue
git push --force-with-lease
```

## Completion Checklist

Before `set_task_status --status=done`:

- [ ] `gh pr checks` shows all checks passing
- [ ] `gh pr view --json mergeable` shows `MERGEABLE`
