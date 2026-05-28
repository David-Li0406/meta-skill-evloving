---
name: create-or-update-pull-request
description: Use this skill when you want to create or update a pull request, ensuring all necessary checks and documentation updates are completed.
---

# Skill body

## Step 1: Check for Uncommitted Changes

Run `git status` to check for uncommitted changes. If there are changes:
- Stage and commit them with a clear, descriptive message.
- Push to the remote branch.

## Step 2: Review and Update Documentation

Check if any changes in this PR require documentation updates:
- New features or commands.
- Changed setup/installation steps (e.g., Docker commands).
- New environment variables or configuration.
- Updated dev workflow.
- API changes that affect usage examples.

If updates are needed, make them and commit before proceeding.

## Step 3: Run Tests

Run these checks and **ensure they pass**:

1. **Unit tests**: Execute `dotnet test` - all tests must pass.
2. **E2E tests**: Execute `cd tests/<your-e2e-test-directory> && npm test` - all tests must pass.

**STOP if any tests fail.** Fix the failures and re-run until all tests pass. Do not proceed to PR creation with failing tests.

## Step 4: Create the Pull Request

Once tests pass:

1. Push any remaining commits to the remote branch.
2. Create the PR using `gh pr create`.

## Step 5: Continuous Monitoring and Review

After the PR is created, **continuously monitor** until ready to merge:

### 5a. Self Code Review
Review the PR diff using `gh pr diff` and look for:
- Code duplication that could be extracted (DRY principle).
- Performance improvements without added complexity.
- Patterns that don't match existing codebase conventions.
- Missing null guards or error handling.
- Accessibility issues (missing aria-labels on icon-only buttons).

**Apply good refactoring opportunities** you identify - don't defer them to future PRs unless they require significant architectural changes.

### 5b. Monitor CI Status
1. Check CI status: `gh pr checks`.
2. If checks are still running, wait and check again.
3. If checks fail:
   - Review the logs: `gh run view <run-id> --log-failed`.
   - Fix the issues, commit, push.
   - Return to monitoring loop.
4. Check for warnings in annotations:
   - Use `gh api repos/{owner}/{repo}/check-runs/{job_id}/annotations` to fetch annotations.
   - **ALL warnings must be addressed** - either fix or document why not.