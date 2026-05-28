---
name: pr-comment-resolution
description: Use this skill to address feedback on pull requests, resolve comments, and push fixes in an isolated worktree.
---

# PR Comment Resolution

This skill is designed to help you address feedback on a pull request (PR) by working in an isolated worktree, resolving comments, and pushing the necessary fixes.

## Invocation

`/pr-comment-resolution <pr-number>`

- `<pr-number>` - the pull request number to address comments on.

## Prerequisites

- **Repo context**: Run from the repo root where the PR exists.
- **Not tracked as a new task**: This skill is ephemeral and responds to feedback on an existing PR.

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
      - P1-P3 non-trivial (significant change): create a descendant issue or task.
      - P4: discard (nitpick).

6. **Complete ALL descendant issues or tasks before commit.**
   Any issue or task created during this session blocks the push.

   While ANY unclosed issues or tasks created in this session:
   - Work on the fix (same worktree, same branch).
   - Stage changes.
   - Run `sg review` (each issue/task gets its own review!).
   - Handle findings (may spawn more descendants).
   - Commit with "Fixes #<issue-number>" to auto-close.
   - Loop until zero unclosed descendants.

7. Commit all fixes:
   ```bash
   git commit -m "address PR #<pr-number> feedback

   - <summary of each addressed comment>"
   ```

8. Push changes:
   ```bash
   git push
   ```

9. Reply to addressed comments (optional but helpful):
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
     -f body="Fixed in $(git rev-parse --short HEAD)"
   ```

10. Cleanup worktree:
    ```bash
    cd $ORIGINAL_DIR
    git worktree remove .worktrees/pr-<pr-number>
    ```

11. Exit and report:
   - List addressed comments.
   - Note any unresolved items that need human decision.
   - Provide PR URL.

## Comment Handling

### Actionable Comments (address)
- "This should handle null case."
- "Missing error handling."
- "Variable name is confusing."
- "Add test for edge case."

### Non-Actionable (skip, report)
- Questions without clear ask: "Why did you do it this way?" (can address with code comment if helpful).
- Design debates: "Have you considered X approach?"
- Requests requiring human decision: "Should we use A or B?"

When in doubt, address it. Better to over-fix than under-fix.

## Review Handling

- **P1-P3 findings**: Create as issues or tasks, work them in this session.
- **P4 findings**: Discard as nitpicks (don't create issues/tasks).

## Exit Conditions

- **Success**: All actionable comments addressed, changes pushed.
- **Blocked**: Comment requires human decision - report and stop.
- **Safety**: Max 10 issue/task iterations (prevent runaway).

## Completion Signaling (MANDATORY)

**CRITICAL: You MUST signal completion when done.** This is the LAST thing you do.

```bash
# On success:
curl -sS -X POST "http://localhost:${MIRANDA_PORT}/complete" \
  -H "Content-Type: application/json" \
  -d "{\"session\": \"$TMUX_SESSION\", \"status\": \"success\", \"pr\": \"<PR-URL>\"}"

# On blocked (needs human):
curl -sS -X POST "http://localhost:${MIRANDA_PORT}/complete" \
  -H "Content-Type: application/json" \
  -d "{\"session\": \"$TMUX_SESSION\", \"status\": \"blocked\", \"blocker\": \"<reason>\"}"

# On error:
curl -sS -X POST "http://localhost:${MIRANDA_PORT}/complete" \
  -H "Content-Type: application/json" \
  -d "{\"session\": \"$TMUX_SESSION\", \"status\": \"error\", \"error\": \"<reason>\"}"
```

**If you don't signal, Miranda won't know you're done and the session becomes orphaned.**

## Example

```
$ /pr-comment-resolution 42

Getting PR #42 info...
Branch: issue/123

Creating worktree .worktrees/pr-42 on branch issue/123
Initializing superego...

Fetching comments...
Found 4 comments:
  1. "Add null check before accessing user.email" (line 45)
  2. "This error message could be clearer" (line 72)
  3. [coderabbit] "Consider using optional chaining" (line 45)
  4. "Why not use the existing validate() function?" → needs decision

Addressing comment 1: Add null check...
Staging changes...
Running sg review...
No issues found.

Addressing comment 2: Improve error message...
Staging changes...
Running sg review...
No issues found.

Addressing comment 3: Use optional chaining...
Staging changes...
Running sg review...
No issues found.

Skipping comment 4: Requires human decision
  (Unsure whether to refactor to use validate() or keep current approach)

Committing fixes...
[issue/123 a1b2c3d] address PR #42 feedback

  - Add null check before accessing user.email
  - Improve error message clarity
  - Use optional chaining per CodeRabbit suggestion

Pushing...
To github.com:org/repo.git
   f1e2d3c..a1b2c3d  issue/123 -> issue/123

Cleaning up worktree...
Signaling blocked (comment 4 needs decision)...

Done.
  Addressed: 3 comments
  Blocked: 1 (comment about validate() function)

PR: https://github.com/org/repo/pull/42
```

### Success Example (no blockers)

```console
$ /pr-comment-resolution 43

Getting PR #43 info...
Branch: feature/add-caching

Creating worktree .worktrees/pr-43 on branch feature/add-caching
Initializing superego...

Fetching comments...
Found 2 comments:
  1. "Fix typo in variable name" (line 12)
  2. "Add logging here" (line 45)

Addressing comment 1: Fix typo...
Addressing comment 2: Add logging...
Committing fixes...
Pushing...

Cleaning up worktree...
Signaling success...

Done.
  Addressed: 2 comments
  Blocked: 0

PR: https://github.com/org/repo/pull/43
```