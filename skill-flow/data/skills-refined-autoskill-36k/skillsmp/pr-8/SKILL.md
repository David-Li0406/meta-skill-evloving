---
name: pr
description: Create or update a pull request. Use when the user wants to create a PR, submit changes for review, or merge their work. Handles git operations, tests, CI monitoring, and PR creation.
---

# Create Pull Request

You are creating or updating a pull request. Follow these steps in order.

## Step 1: Check for Uncommitted Changes

Run `git status` to check for uncommitted changes. If there are changes:
- Stage and commit them with a clear, descriptive message
- Push to the remote branch

## Step 2: Review and Update README.md

Check if any changes in this PR require documentation updates:
- New features or commands
- Changed setup/installation steps (e.g., Docker commands)
- New environment variables or configuration
- Updated dev workflow
- API changes that affect usage examples

If updates are needed, make them and commit before proceeding.

## Step 3: Run Tests

Run these checks and **ensure they pass**:

1. **Unit tests**: Execute `dotnet test src/FlatRate.slnx` - all tests must pass
2. **E2E tests**: Execute `cd tests/FlatRate.E2E.Tests && npm test` - all tests must pass

**STOP if any tests fail.** Fix the failures and re-run until all tests pass. Do not proceed to PR creation with failing tests.

## Step 4: Create the PR

Once tests pass:

1. Push any remaining commits to the remote branch
2. Create the PR using `gh pr create`

## Step 5: Continuous CI and Review Monitoring Loop

After the PR is created, **continuously monitor** until ready to merge:

### 5a. Self Code Review
Review the PR diff using `gh pr diff` and look for:
- Code duplication that could be extracted (DRY principle)
- Performance improvements without added complexity
- Patterns that don't match existing codebase conventions
- Missing null guards or error handling
- Accessibility issues (missing aria-labels on icon-only buttons)

**Apply good refactoring opportunities** you identify - don't defer them to future PRs unless they require significant architectural changes.

### 5b. Monitor CI Status
1. Check CI status: `gh pr checks`
2. If checks are still running, wait 30 seconds and check again
3. If checks fail:
   - Review the logs: `gh run view <run-id> --log-failed`
   - Fix the issues, commit, push
   - Return to monitoring loop
4. Check for warnings in annotations:
   - Use `gh api repos/{owner}/{repo}/check-runs/{job_id}/annotations` to fetch annotations
   - **ALL warnings must be addressed** - either fix or document why not

### 5c. Monitor for AI Reviews
Poll for CodeRabbit and Copilot reviews:
1. **CodeRabbit**: Use `gh pr checks` - wait until CodeRabbit shows "Review completed"
2. **Copilot/Sourcery**: Check `gh pr view <number> --comments` for bot comments
3. If reviews not yet complete, wait 30 seconds and check again
4. **Keep monitoring** - reviews may come in multiple rounds

### 5d. Address All Comments
When comments appear from reviewers (human or AI):
1. Read each comment carefully, including **high-level feedback**
2. **For line comments**:
   - **If addressing**: React with thumbs up, then make the fix
   - **If not addressing**: Reply explaining why
3. **Apply good refactoring suggestions** when they:
   - Reduce code duplication (DRY principle)
   - Improve performance without adding complexity
   - Follow existing patterns in the codebase
4. Commit, push, and **return to Step 5b** (CI monitoring loop)

### 5e. Loop Completion Criteria
Continue the monitoring loop until ALL of these are true:
- [ ] All CI checks pass (green)
- [ ] No warnings in CI annotations
- [ ] CodeRabbit review is complete
- [ ] Copilot/Sourcery review is complete (or confirmed not enabled)
- [ ] All review comments have been addressed

## Step 6: Automatic Merge

Once the monitoring loop is complete (all CI checks pass, all reviews complete, all comments addressed):

**Merge automatically**:
```bash
gh pr merge --squash --delete-branch
```

Then notify the user the PR was merged and ask what to work on next.

## Post-Merge

After merging:
1. Confirm the PR was merged successfully
2. Check if there's an associated GitHub issue to close
3. Ask the user what to work on next (e.g., next issue in the backlog)
