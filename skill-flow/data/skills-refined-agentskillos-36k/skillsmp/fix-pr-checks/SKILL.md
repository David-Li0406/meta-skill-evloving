---
name: fix-pr-checks
description: Analyze and fix failing GitHub PR checks for the current branch. Use when CI is failing, builds are broken, tests are red, PR checks show errors, or the user mentions "fix CI", "fix checks", "fix pipeline", "failing tests", or "broken build".
allowed-tools:
  - Bash(gh:*)
  - Bash(git:*)
  - Read
  - Grep
  - Glob
  - Task
  - Skill
---

# Fix PR Checks

## Current Branch

!`git branch --show-current`

## PR Info

!`gh pr view --json number,state,title 2>&1`

## Check Status

!`gh pr checks --json name,bucket,state,description,link,workflow 2>&1`

---

## Instructions

### If No PR or All Checks Pass

- **No PR**: Tell user to create a PR first
- **All checks passing** (no `bucket: "fail"`): Report success, nothing to fix

### For Each Failing Check

1. Extract run ID from the check's `link` field (pattern: `/runs/<run-id>`)

2. Fetch failed logs:
   ```bash
   gh run view <run-id> --log-failed
   ```
   If empty, try `gh run view <run-id> --json jobs` to identify the failed job.

3. Spawn a **parallel** Task agent (`general-purpose`) for diagnosis:
   ```
   Diagnose this CI failure. DO NOT make changes—only analyze.

   Check: [name]
   Workflow: [workflow]

   Logs:
   [log output]

   Report:
   - Category: build | type | test | lint | security | other
   - Root Cause: [what's broken, file:line if visible]
   - Affected Files: [paths from error output]
   - Fix: [specific change needed]
   ```

   **Spawn all diagnostic agents in parallel** (single message, multiple Task calls).

4. Collect diagnoses. Look for shared causes—one fix may resolve multiple checks.

### Plan Fixes

After all diagnoses complete, invoke `tasks:plan-tasks` with a goal summarizing all failures:

```
Fix CI failures for PR #[number]:

[For each diagnosed failure:]
- [check-name] ([category]): [root cause]
  Files: [affected files]
  Fix: [specific change]

Fix order: [dependencies or "independent"]
```

### Execute Fixes

Invoke `tasks:do-all-tasks` to execute the planned fixes.

### Report

After execution completes:

```
Fixed X issues across Y files:
- [check-name]: [brief fix description]

Run `gh pr checks --watch` to verify.
```

If any tasks were blocked, explain what user needs to resolve.
