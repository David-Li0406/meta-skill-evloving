---
name: codex-pr-review-loop
description: "Use when managing Codex review iterations for a PR and you must enforce preflight risk-layer checks and post-merge learning capture."
---

# Codex PR Review Loop

## Overview
Run a 5-minute polling loop for PR review threads, but enforce a preflight Codex Context gate and capture post-merge learning when Codex churn occurs.

## Workflow (Preflight + Loop + Post-Merge)

### Preconditions
1. If the user asks for preflight, run Step -1 before PR submission.
2. If PR already exists, proceed to Step 0.
3. `gh` is authenticated.
4. You are allowed to push/merge as part of this explicit user-requested workflow.

### Step -1: Pre-PR Codex Readiness (only when requested)
- Open `.github/PULL_REQUEST_TEMPLATE.md`.
- If any **Risk Layer Trigger** applies, fill the **Risk Layer Addendum** (rules/invariants, boundary matrix >= 3, evidence).
- Ensure **Codex Context** lists delta, invariants, edge cases, tests, and known gaps.
- Run the minimal regression tests that cover the boundary matrix.
- Stop and ask the user to create the PR if it does not exist yet.

### Step 0: Identify PR
- Prefer current branch PR: `gh pr view --json number`.
- If ambiguous, ask for PR number.

### Step 1: Poll review threads, PR issue comments, and PR body reactions
Run:
```
GH_OWNER=<owner>
GH_REPO=<repo>
PR_NUMBER=<number>

gh api graphql -f owner="$GH_OWNER" -f name="$GH_REPO" -F number=$PR_NUMBER -f query='query($owner:String!,$name:String!,$number:Int!){repository(owner:$owner,name:$name){pullRequest(number:$number){reactionGroups{content users{totalCount}} reviewThreads(first:100){nodes{isResolved path line originalLine comments(first:50){nodes{author{login} body createdAt reactions(content: THUMBS_UP){totalCount}}}}} comments(first:100){nodes{author{login} body createdAt reactions(content: THUMBS_UP){totalCount}}}}}}}'
```

### Step 2: Wait for updates (repeat until update)
- **Do not proceed** unless review threads, PR issue comments, **or PR body reactions** have **new updates** since the last poll (new comments, new threads, updated timestamps, or reaction count changes).
- If no updates are found, **wait 5 minutes and poll again**. Continue doing this automatically until updates appear.

### Step 3: Decide
- **If any review thread comment OR PR issue comment contains** `Codex Review: Didn't find any major issues` **(exact phrase)** **OR** a thumbs-up signal:
  - thumbs-up signal = comment body includes `👍` or `:+1:` **OR** `reactions(content: THUMBS_UP).totalCount > 0` **OR** PR body `reactionGroups` has `content: THUMBS_UP` with `users.totalCount > 0`
  - You may merge to remote `main`, then pull locally. Proceed to Step 6.
- **Else:** treat updated review thread feedback as actionable. Proceed to Step 4.

### Step 4: Fix bugs or requested changes
- Apply fixes in code.
- Add/adjust tests for regressions.
- Run relevant verification commands.
- Commit changes locally.
- Push to update the PR.

### Step 5: Reply and wait
- Post a **separate PR issue comment** (not a thread reply) with **exactly** `@codex review`.
  - Use: `gh pr comment <PR_NUMBER> --body "@codex review"`
- After replying, immediately return to Step 2 (wait 5 minutes, poll again until updates appear).

### Step 6: Merge and sync
- Merge PR to `main` on remote (e.g., `gh pr merge --merge` or project-required strategy).
- Pull latest `main` locally.

### Step 7: Post-merge learning capture (when Codex churn occurred)
- If the PR required multiple @codex review cycles or post-merge fixes:
  - Run a retrospective using **pr-review-cycle-retro** on this PR.
  - Update `docs/retrospective/` entries if this repo uses them.
  - If a new cause category appears, update the churn skill taxonomy.

## Guardrails
- Do not merge until review thread content, PR issue comments, **or PR body reactions** explicitly include: `Codex Review: Didn't find any major issues` **or** a thumbs-up signal (see Step 3).
- Do not take any action (fix/respond/merge) unless review threads have new updates since the last poll.
- If no updates are found, you MUST keep waiting in 5-minute increments until updates appear.
- Do not request `@codex review` if a Risk Layer Trigger applies but the Addendum is incomplete.
- Always run tests appropriate to the change before pushing.
- Follow repo rules (e.g., no `git push` unless this skill is explicitly requested).
- If merging/pushing requires confirmation in the current environment, ask for explicit confirmation.

## Common Mistakes
- Triggering `@codex review` without filling Risk Layer Addendum when required.
- Treating Codex churn as a tooling issue instead of a stage/contract issue.

## Rationalization Table
| Excuse | Reality |
| --- | --- |
| "Preflight is optional" | If Risk Layer Trigger applies, the addendum is mandatory. |
| "Codex asked again, so we can skip context" | Missing context amplifies churn. |

## Red Flags - STOP
- Risk Layer Trigger checked but Addendum is missing.
- Multiple @codex reviews without any delta summary.
