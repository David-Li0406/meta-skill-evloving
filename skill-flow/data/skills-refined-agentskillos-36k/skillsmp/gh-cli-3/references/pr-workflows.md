# Pull Request Workflows

Comprehensive patterns for working with pull requests using GitHub CLI.

## Quick Reference

```bash
gh pr create           # Create PR (interactive or with flags)
gh pr list             # List PRs with filters
gh pr view [number]    # View PR details
gh pr checkout [number]# Checkout PR branch locally
gh pr review [number]  # Review PR (approve, comment, request changes)
gh pr merge [number]   # Merge PR
gh pr close [number]   # Close PR
gh pr reopen [number]  # Reopen closed PR
gh pr comment [number] # Add comment to PR
gh pr diff [number]    # View PR diff
gh pr checks [number]  # View CI/CD status
```

**Remember:** Use `gh pr <subcommand> --help` for detailed options and examples.

## Creating Pull Requests

### Basic PR Creation

**Interactive mode** (prompts for all details):
```bash
gh pr create
```

**Non-interactive with flags:**
```bash
gh pr create \
  --title "feat: Add user authentication" \
  --body "Implements OAuth2 login flow with session management" \
  --base main \
  --head feature-auth
```

**From template:**
```bash
gh pr create --template bug_fix.md
```

### Advanced PR Creation

**Draft PR for work in progress:**
```bash
gh pr create --draft \
  --title "WIP: Refactor database layer" \
  --body "Early draft for feedback"
```

**Link to issues:**
```bash
gh pr create \
  --title "fix: Resolve memory leak" \
  --body "Fixes #123, #124" \
  --base main
```

**Assign reviewers and labels:**
```bash
gh pr create \
  --title "feat: New dashboard" \
  --body "..." \
  --reviewer alice,bob \
  --label enhancement,needs-review \
  --assignee @me
```

**Push current branch if needed:**
```bash
# Check if branch exists on remote
git ls-remote --heads origin $(git branch --show-current)

# If not, push first
git push -u origin $(git branch --show-current)

# Then create PR
gh pr create --fill  # Uses commit messages for title/body
```

### Creating PRs with JSON Output

Get the PR URL programmatically:
```bash
PR_URL=$(gh pr create --title "..." --body "..." --json url --jq '.url')
echo "Created PR: $PR_URL"
```

## Listing and Filtering PRs

### Basic Listing

```bash
gh pr list                    # Open PRs in current repo
gh pr list --state all        # All PRs (open, closed, merged)
gh pr list --state closed     # Only closed PRs
gh pr list --state merged     # Only merged PRs
```

### Filtering PRs

**By author:**
```bash
gh pr list --author username
gh pr list --author @me       # Your PRs
```

**By assignee:**
```bash
gh pr list --assignee username
gh pr list --assignee @me
```

**By label:**
```bash
gh pr list --label bug
gh pr list --label "needs review,priority-high"
```

**By base branch:**
```bash
gh pr list --base main
gh pr list --base develop
```

**By search query:**
```bash
gh pr list --search "in:title authentication"
gh pr list --search "is:draft"
gh pr list --search "review:approved"
```

### Listing with JSON

**Get structured data for processing:**
```bash
gh pr list \
  --json number,title,author,state,createdAt,updatedAt \
  --limit 50
```

**Extract specific information:**
```bash
# Get PR numbers for all open PRs
gh pr list --json number --jq '.[].number'

# Find PRs by specific author
gh pr list --json number,title,author --jq '.[] | select(.author.login == "username")'

# Get PRs updated in last 24 hours
gh pr list --json number,title,updatedAt \
  --jq '.[] | select(.updatedAt > (now - 86400 | todate))'
```

## Viewing PR Details

### Basic View

```bash
gh pr view 123                # View in terminal
gh pr view 123 --web          # Open in browser
```

### Detailed Information

```bash
# View with comments
gh pr view 123 --comments

# View with JSON output
gh pr view 123 --json title,body,author,state,reviews,comments

# Get specific fields
gh pr view 123 --json title --jq '.title'
gh pr view 123 --json reviews --jq '.reviews[].state'
```

### Check CI/CD Status

```bash
gh pr checks 123              # View all checks
gh pr checks 123 --watch      # Watch checks in real-time
gh pr checks 123 --json name,status,conclusion
```

### View PR Diff

```bash
gh pr diff 123                # View diff in terminal
gh pr diff 123 --patch        # Git patch format
```

## Reviewing Pull Requests

### Adding Reviews

**Approve PR:**
```bash
gh pr review 123 --approve
gh pr review 123 --approve --body "LGTM! Great work on the tests."
```

**Request changes:**
```bash
gh pr review 123 --request-changes \
  --body "Please address the following concerns:
- Add error handling in line 45
- Update tests to cover edge case"
```

**Comment without explicit approval:**
```bash
gh pr review 123 --comment \
  --body "Looks good overall, just some minor suggestions"
```

### Inline Comments

**Comment on specific files/lines:**
```bash
gh pr review 123 \
  --comment \
  --body "Consider extracting this to a helper function" \
  --file src/auth.js \
  --line 42
```

### Batch Review Comments

For complex reviews, use a comment file:

```bash
# Create review-comments.md with your review
gh pr review 123 --comment --body-file review-comments.md
```

## Commenting on PRs

### Simple Comments

```bash
gh pr comment 123 --body "Thanks for the quick fix!"

gh pr comment 123 --body "Could you add a test case for the error scenario?"
```

### Comments from Files

```bash
gh pr comment 123 --body-file comment.md
```

### React to Comments

```bash
# Get comment IDs first
gh pr view 123 --json comments --jq '.comments[].id'

# React to specific comment
gh api --method POST /repos/{owner}/{repo}/issues/comments/COMMENT_ID/reactions \
  -f content='+1'
```

## Merging Pull Requests

### Merge Strategies

**Default merge (merge commit):**
```bash
gh pr merge 123
```

**Squash and merge:**
```bash
gh pr merge 123 --squash
```

**Rebase and merge:**
```bash
gh pr merge 123 --rebase
```

**Auto-merge when checks pass:**
```bash
gh pr merge 123 --auto --squash
```

### Delete Branch After Merge

```bash
gh pr merge 123 --squash --delete-branch
```

### Merge with Body/Title Override

```bash
gh pr merge 123 --squash \
  --subject "feat: Add user authentication" \
  --body "Complete implementation of OAuth2 flow"
```

### Dry-Run Merge Check

**Check if PR can be merged:**
```bash
gh pr view 123 --json mergeable,mergeStateStatus

# Parse result
MERGEABLE=$(gh pr view 123 --json mergeable --jq '.mergeable')
if [ "$MERGEABLE" = "MERGEABLE" ]; then
  echo "PR can be merged"
else
  echo "PR cannot be merged yet"
fi
```

## Checking Out PRs Locally

### Basic Checkout

```bash
gh pr checkout 123            # Checkout by number
gh pr checkout branch-name    # Checkout by branch name
```

### Checkout and Review

**Typical workflow:**
```bash
# Checkout PR
gh pr checkout 123

# Review changes locally
git log --oneline HEAD~5..HEAD
git diff main...HEAD

# Run tests
npm test

# Leave review
gh pr review 123 --approve --body "Tested locally, works great!"
```

### Checkout from Fork

```bash
gh pr checkout 123  # Automatically handles fork remotes
```

## Closing and Reopening PRs

### Close PR

```bash
gh pr close 123
gh pr close 123 --comment "Closing due to duplicate of #124"
```

### Reopen PR

```bash
gh pr reopen 123
gh pr reopen 123 --comment "Reopening after discussion"
```

## Working with Draft PRs

### Create Draft

```bash
gh pr create --draft --title "WIP: Feature X"
```

### Convert Draft to Ready

```bash
gh pr ready 123
```

### Mark Ready as Draft

```bash
gh pr ready 123 --undo
```

## PR Workflows

### Complete PR Creation Workflow

```bash
# 1. Verify repository context
gh repo view

# 2. Ensure changes are committed
git status

# 3. Push branch if needed
BRANCH=$(git branch --show-current)
git push -u origin "$BRANCH"

# 4. Create PR with details
gh pr create \
  --title "feat: Add user dashboard" \
  --body "$(cat << 'EOF'
## Summary
Implements new user dashboard with analytics.

## Changes
- Added dashboard component
- Integrated with analytics API
- Added tests for dashboard logic

## Testing
- Unit tests pass
- Manual testing completed
- Screenshots in PR comments

Closes #456
EOF
)" \
  --base main \
  --reviewer alice,bob \
  --label enhancement

# 5. Get PR URL
PR_URL=$(gh pr view --json url --jq '.url')
echo "Created PR: $PR_URL"
```

### PR Review Cycle

```bash
# 1. List PRs needing review
gh pr list --search "review-requested:@me"

# 2. View PR details
gh pr view 123 --comments

# 3. Checkout and test locally
gh pr checkout 123
npm test

# 4. Leave review
gh pr review 123 --approve --body "Looks great! Tests pass locally."

# 5. Merge if you have permissions
gh pr merge 123 --squash --delete-branch
```

### Responding to PR Comments

```bash
# 1. View PR with comments
gh pr view 123 --comments

# 2. Read review comments
gh pr view 123 --json reviews,comments \
  --jq '.reviews[].body, .comments[].body'

# 3. Make requested changes
# ... edit files ...

# 4. Commit and push
git add .
git commit -m "fix: Address review comments"
git push

# 5. Reply to review
gh pr comment 123 --body "Thanks for the review! I've addressed all the comments."

# 6. Re-request review if needed
gh pr review 123 --request-changes --body "Please review the updates"
```

### Batch Processing PRs

**Close stale PRs:**
```bash
# Get PRs older than 30 days
gh pr list --json number,updatedAt \
  --jq '.[] | select(.updatedAt < (now - 2592000 | todate)) | .number' \
  | while read pr; do
    gh pr close "$pr" --comment "Closing due to inactivity. Please reopen if still relevant."
  done
```

**Auto-approve PRs from specific users:**
```bash
gh pr list --author dependabot --json number \
  | jq -r '.[].number' \
  | while read pr; do
    gh pr review "$pr" --approve --body "Auto-approved dependency update"
  done
```

## Error Handling

### Common Issues

**PR already exists:**
```
! pull request create failed: a pull request for branch "feature-x" into branch "main" already exists
```
**Solution:** Find existing PR with `gh pr list --head feature-x`

**No commits between branches:**
```
! pull request create failed: no commits between main and feature-x
```
**Solution:** Ensure branch has unique commits, check with `git log main..feature-x`

**Authentication required:**
```
! error: HTTP 401: Unauthorized
```
**Solution:** See `troubleshooting.md` for authentication guidance

**Branch not pushed:**
```
! error: branch not found on remote
```
**Solution:** Push branch first with `git push -u origin branch-name`

### Verification Before Operations

**Check if PR exists:**
```bash
gh pr view 123 &>/dev/null && echo "PR exists" || echo "PR not found"
```

**Verify PR is mergeable:**
```bash
STATUS=$(gh pr view 123 --json mergeable --jq '.mergeable')
if [ "$STATUS" != "MERGEABLE" ]; then
  echo "Cannot merge: conflicts or failing checks"
fi
```

**Check review status:**
```bash
gh pr view 123 --json reviewDecision --jq '.reviewDecision'
# Returns: APPROVED, CHANGES_REQUESTED, REVIEW_REQUIRED, or null
```

## Best Practices

1. **Always verify repository context** before creating PRs
2. **Use `--draft` for work in progress** to signal incomplete work
3. **Link issues** in PR body with "Fixes #123" or "Closes #456"
4. **Request specific reviewers** familiar with the code area
5. **Use appropriate labels** to categorize PRs
6. **Check CI status** before requesting review
7. **Squash commits** for cleaner history on merge
8. **Delete branches** after merging to keep repository clean
9. **Use templates** for consistent PR descriptions
10. **Comment on your own PR** to guide reviewers

## Related Commands

- `gh issue` - Link issues to PRs
- `gh workflow` - Trigger CI/CD workflows
- `gh api` - Custom PR operations
- `git` - Local branch and commit management

See `api-usage.md` for advanced PR operations using `gh api`.
