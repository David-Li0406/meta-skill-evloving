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

## Step 2.5: Generate Feature Notification (Optional)

If this PR includes user-facing changes (new features, bug fixes, or improvements), ask the user:
"Would you like to notify users about this change? (Run /broadcast)"

If yes, run the `/broadcast` skill to generate a notification migration, then continue.

Skip this step for:
- Internal refactoring
- Test changes
- Documentation updates
- CI/workflow changes

## Step 3: Run Tests

Run these checks and **ensure they pass**:

1. **Unit tests**: Execute `dotnet test` - expect 185+ tests, all must pass
2. **E2E tests**: Execute `cd tests/PraxisNote.E2E.Tests && npm test` - all tests must pass

**STOP if any tests fail.** Fix the failures and re-run until all tests pass. Do not proceed to PR creation with failing tests.

## Step 4: Create the PR

Once tests pass:

1. Push any remaining commits to the remote branch
2. Create the PR using `gh pr create`

## Step 5: Post-PR Review and Monitoring

After the PR is created, **actively monitor** and address feedback:

1. **Self code review**: Review the PR diff using `gh pr diff` and look for:
   - Code duplication that could be extracted (DRY principle)
   - Performance improvements without added complexity
   - Patterns that don't match existing codebase conventions
   - Missing null guards or error handling
   - Accessibility issues (missing aria-labels on icon-only buttons)

   **Apply good refactoring opportunities** you identify - don't defer them to future PRs unless they require significant architectural changes. Add comments for any issues found using `gh pr comment` or `gh api`
2. **Wait for CI**: Monitor GitHub Actions for completion using `gh pr checks`
3. **Check for warnings**: Review action logs AND annotations for any warnings (not just failures)
   - Use `gh api repos/{owner}/{repo}/check-runs/{job_id}/annotations` to fetch annotations
   - Common warnings: deprecation notices, bundle size budgets, artifact upload failures, EF Core model validation
   - **ALL warnings must be addressed** - either fix the issue or update the workflow if it's a false positive
4. **Monitor for AI reviews**: Actively poll for CodeRabbit and Copilot reviews to complete
   - **CodeRabbit**: Use `gh pr checks` - wait until CodeRabbit shows "Review completed"
   - **Copilot**: Use `gh api repos/{owner}/{repo}/pulls/{number}/reviews --jq '.[] | select(.user.login | contains("copilot")) | .state'` to check if Copilot has submitted a review (look for "COMMENTED" state)
   - Alternatively, use `gh pr view <number> --comments` and look for comments from `copilot-pull-request-reviewer[bot]`
   - Keep checking every 30-60 seconds until BOTH CodeRabbit AND Copilot reviews are complete
5. **Address all comments immediately**: When comments appear:
   - Read each comment carefully, including **high-level feedback** in comment bodies (not just line-specific suggestions)
   - **For line comments (have their own ID)**:
     - **If addressing**: Add a thumbs up reaction using `gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions -X POST -f content='+1'`, then make the fix
     - **If not addressing**: Reply to the comment explaining why (e.g., out of scope, matches existing patterns, deferred to follow-up)
   - **For high-level feedback in PR comments**: Reply to the comment addressing each suggestion - either confirm you'll fix it or explain why not
   - **Apply good refactoring suggestions**: When reviewers suggest refactoring (e.g., extracting duplicated code, improving efficiency), evaluate and apply them if they:
     - Reduce code duplication (DRY principle)
     - Improve performance without adding complexity
     - Follow existing patterns in the codebase
     - Are straightforward to implement
   - Do NOT defer refactoring suggestions to "future PRs" unless they are truly out of scope or require significant architectural changes
   - Commit, push, and verify the fix resolves the comment
6. **Verify CI passes**: After all fixes, ensure all checks pass (no warnings in annotations)

**Do not stop monitoring until**: All AI reviews are complete (both CodeRabbit AND Copilot have submitted reviews), all comments are addressed, and CI is green.

## Step 6: Manual Testing (Required Before Merge)

Once CI is green and all comments are addressed:

1. **Start the dev stack**: Run `docker compose --profile dev-stack up`
2. **Notify the user**: Tell them the app is running at http://localhost:4200 and ask them to test the changes
3. **Wait for approval**: Do NOT merge until the user explicitly approves or provides feedback
4. **If feedback given**: Make fixes, commit, push, and repeat from Step 5 (CI monitoring)
5. **If approved**: Proceed to merge with `gh pr merge --squash --delete-branch`

**Exception**: Skip this step for markdown-only PRs (`.md` files only) - merge immediately.