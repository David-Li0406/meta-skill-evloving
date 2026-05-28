---
name: pr-feedback-resolver
description: Use this skill when you need to address feedback on a pull request in an isolated worktree and push fixes.
---

# Skill body

## Invocation

`/pr-feedback-resolver <pr-number>`

- `<pr-number>` - the pull request number to address comments on.

## Prerequisites

- **Repo context**: Run from the repo root where the PR exists.
- **Not tracked as ba task**: This skill is ephemeral - it responds to feedback on an existing PR, not a new work item.

## Flow

1. Read dive context (if available) for project background:
   ```bash
   cat .wm/dive_context.md 2>/dev/null || echo "No dive context"
   ```

2. Get PR branch info and create worktree:
   ```bash
   # Save original directory for cleanup
   ORIGINAL_DIR=$(pwd)

   # Get the PR branch name
   BRANCH=$(gh pr view <pr-number> --json headRefName -q .headRefName)

   # Fetch and create worktree tracking the remote branch
   git fetch origin
   git worktree add .worktrees/pr-<pr-number> -B $BRANCH origin/$BRANCH
   cd .worktrees/pr-<pr-number>
   sg init
   ```
   Note: `-B $BRANCH` creates/resets the local branch to track origin.

3. Fetch PR comments (both top-level and inline review comments):
   ```bash
   gh pr view <pr-number> --json comments,reviews
   gh api repos/{owner}/{repo}/pulls/<pr-number>/comments
   ```

4. Identify unresolved comments:
   - Focus on actionable feedback requiring code changes.
   - Ignore resolved/outdated comments.
   - Skip non-actionable noise (e.g., "Thanks for the PR!").

5. For each unresolved comment:
   a. Understand the feedback.
   b. Make the fix.
   c. Stage changes (`git add`).
   d. Run `sg review` on staged changes.
   e. Handle review findings:
      - P1-P3 trivial (one-liner fix): fix inline, re-stage, re-review.
      - P1-P3 non-trivial (significant change): create GitHub issue as descendant.
      - P4: discard (nitpick).

6. **Complete ALL descendant tasks before commit.**
   Any `ba create` during this session = descendant that blocks push.

   Note: If feedback requires significant architectural changes, consider escalating back to the original task author rather than creating many descendant tasks.

   While ANY unclosed tasks created in this session:
   - `ba claim <next-task>`
   - Work until complete.
   - Stage changes.
   - Run `sg review` (each task gets its own review!).
   - Handle findings (may spawn more descendants).
   - `ba finish`, commit code + `.ba/`.
   - Loop until zero unclosed.