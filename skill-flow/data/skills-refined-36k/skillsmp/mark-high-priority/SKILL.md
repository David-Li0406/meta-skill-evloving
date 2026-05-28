---
name: mark-high-priority
description: Add the high-priority label to a PR so merge-queue automation yields to it. Use when a PR needs to bypass normal queue yielding for urgent fixes or time-sensitive deployments.
---

# Mark High Priority

Add the `high-priority` label to a PR so other merge-queue sessions yield to it.

## Setup

Determine the repository for all `gh` commands:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Always pass `-R "$REPO"` to `gh` commands.

## Workflow

1. Get PR info:

   ```bash
   gh pr view --json number,labels -R "$REPO"
   ```

2. If the PR already has `high-priority`, report that and exit.

3. Add the label:

   ```bash
   gh pr edit <pr-number> --add-label "high-priority" -R "$REPO"
   ```

4. Confirm:

   ```bash
   gh pr view <pr-number> --json labels -R "$REPO"
   ```

## Notes

- The `high-priority` label must exist in the repository (create it if it doesn't).
- Use sparingly to keep the merge queue fair.
- To remove later: `gh pr edit <pr-number> --remove-label "high-priority" -R "$REPO"`.
