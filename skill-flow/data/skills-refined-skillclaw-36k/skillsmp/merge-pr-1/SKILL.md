---
name: merge-pr
description: |
  Watch CI checks, auto-fix failures, and squash-merge the PR when all checks pass.
---
# Merge PR When CI Passes

Wait for CI checks to pass, then merge the specified PR with squash.

## Usage
```
/merge-pr <pr-number>
```

If no PR number is provided, use the current branch's PR.

## Instructions

1. **Determine target PR and branch**:
   - Record the current branch: `git branch --show-current`
   - If `$ARGUMENTS` is provided (PR number specified):
     - Get the PR's head branch: `gh pr view <pr-number> --json headRefName -q .headRefName`
     - Compare with current branch
     - If different branch:
       - Stash all local changes (including untracked): `git stash push -u -m "merge-pr: stashing for PR #<pr-number>"`
       - Switch to PR branch: `git checkout <pr-branch>`
       - Set `SWITCHED_BRANCH=true` and `ORIGINAL_BRANCH=<current-branch>`
   - If no `$ARGUMENTS`, use the current branch's PR

2. **Check uncommitted changes**: Run `git status` to check for uncommitted changes:
   - If there are uncommitted changes, inform the user and ask if they want to commit
   - If yes, invoke the `commit-changes` skill to create a proper commit

3. **Check unpushed commits**: Run `git log origin/<branch>..HEAD --oneline` to check for unpushed commits:
   - If there are unpushed commits, inform the user and push them: `git push`

4. **Check for existing PR**: Run `gh pr view --json number,url -q '.number' 2>/dev/null` to check if a PR exists for the current branch:
   - If no PR exists and no `$ARGUMENTS` provided, ask the user if they want to create a PR
   - If yes, invoke the `pr-push` skill to create the PR, then continue
   - If no, inform the user that a PR is required and stop

5. **Get PR number**: If `$ARGUMENTS` is provided, use it as the PR number. Otherwise, get the PR for the current branch:
   ```bash
   gh pr view --json number -q .number
   ```

6. **Watch CI status**: Monitor the CI checks for the PR:
   ```bash
   gh pr checks <pr-number> --watch
   ```

7. **Handle CI failures**: If any check fails:
   - Get the failed check details:
     ```bash
     gh pr checks <pr-number>
     ```
   - For each failed check, fetch the logs to understand the error:
     ```bash
     gh run view <run-id> --log-failed
     ```
   - Analyze the error and attempt to fix it
   - Push the fix and repeat from step 6

8. **Prepare commit message**: Before merging, consolidate commit messages:
   - Get all commits in the PR:
     ```bash
     gh pr view <pr-number> --json commits -q '.commits[].messageHeadline'
     ```
   - Create a consolidated commit message that:
     - Uses the PR title as the main message
     - Removes duplicate/redundant commit messages
     - Keeps unique meaningful changes as bullet points in the body

9. **Merge the PR**: Once all checks pass, merge with squash:
   ```bash
   gh pr merge <pr-number> --squash --delete-branch --body "<consolidated-message>"
   ```

10. **Restore original state or switch to main**:
    - If `SWITCHED_BRANCH=true` (was working on a different branch):
      - Switch back to original branch: `git checkout <ORIGINAL_BRANCH>`
      - Restore stashed changes: `git stash pop`
      - Inform the user that original branch and changes have been restored
    - If `SWITCHED_BRANCH=false` (was on the PR branch itself):
      - The PR branch has been deleted, switch to main and pull:
        ```bash
        git checkout main && git pull
        ```

11. **Report result**: Show the merge commit and confirm success.

## Commit Messages Examples

### Example 1: Feature Commit

```
feat: add JWT token refresh mechanism

Changes:
- Implement automatic token refresh before expiration
- Add refresh token storage in secure cookie
- Include retry logic for failed refresh attempts
```

### Example 2: Bug Fix Commit

```
fix: prevent null pointer on empty response

Changes:
Handle case where API returns empty body instead of
throwing unhandled exception in response parser.
```

### Example 3: Refactor Commit

```
refactor: extract common mock to shared helper

Changes:
- Move mockGRPCStreamClient to mock_query.go
- Consolidate 4 duplicate mock implementations
- Reduce test file coupling
```
