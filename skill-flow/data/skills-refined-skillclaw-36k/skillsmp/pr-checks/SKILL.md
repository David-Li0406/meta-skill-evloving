---
name: pr-checks
description: Wait for CI checks to pass, address automated feedback from Copilot, and mark PR ready for human review
---

## What I do

1. Poll CI check status until all checks complete
2. If checks pass, assign GitHub Copilot as a reviewer
3. Wait for Copilot's review feedback
4. Address any feedback or issues that come up
5. If an unrelated test fails, re-run it (do not attempt to fix it)
6. Once all feedback is addressed, mark PR as ready and assign human reviewers

## Workflow

### Step 1: Wait for CI checks

Poll the PR checks until they complete:

```bash
gh pr checks <PR_NUMBER> 2>&1
```

If checks are still pending, wait 60-120 seconds and poll again. Continue until all checks have a final status (pass/fail).

### Step 2: Handle check failures

- **Related test failure**: Investigate and fix the issue, then push the fix
- **Unrelated test failure**: Re-run the failed job:
  ```bash
  gh run rerun <RUN_ID> --failed
  ```
- **Lint/typecheck failure**: Fix the issues and push

### Step 3: Assign Copilot reviewer (on success)

Once all checks pass:

```bash
gh pr edit <PR_NUMBER> --add-reviewer @copilot-pull-request-reviewer
```

### Step 4: Wait for Copilot review

Poll for review status:

```bash
gh pr view <PR_NUMBER> --json reviews
```

Wait until Copilot's review appears (usually 1-3 minutes).

### Step 5: Address feedback

Fetch Copilot's review comments:

```bash
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/reviews
```

For each piece of feedback:
- If it's a valid suggestion, implement the change
- If it's incorrect or not applicable, explain why in a reply
- Push any changes and wait for checks again (repeat from Step 1)

### Step 6: Mark PR ready and assign human reviewers

Once all Copilot feedback has been addressed and checks pass:

```bash
gh pr ready <PR_NUMBER>
gh pr edit <PR_NUMBER> --add-reviewer @chartmogul/delta
```

## When to use me

Use this skill when asked to:
- "Wait for checks and get Copilot review"
- "Monitor PR and address feedback"
- "Get the PR reviewed"
- "Finalize the PR"

## Notes

- Always use `--failed` flag when re-running jobs to only re-run failed ones
- Be patient with polling - CI can take several minutes
- If Copilot reviewer is not available, inform the user
- Only mark PR as ready after ALL automated feedback has been addressed
