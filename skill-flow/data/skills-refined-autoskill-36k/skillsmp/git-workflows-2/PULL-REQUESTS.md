# Pull Request Workflows

Comprehensive guide for creating, reviewing, and managing pull requests with Claude Code using the GitHub CLI.

## GitHub CLI (gh) Overview

Claude uses `gh` CLI for all GitHub operations. Never use raw git commands for GitHub-specific features.

### Authentication Check

```bash
gh auth status    # Verify authentication
gh auth login     # Login if needed
```

### Common gh Commands

| Command | Description |
|---------|-------------|
| `gh pr create` | Create pull request |
| `gh pr view <n>` | View PR details |
| `gh pr list` | List open PRs |
| `gh pr diff <n>` | View PR diff |
| `gh pr checks <n>` | View CI status |
| `gh pr merge <n>` | Merge PR |
| `gh pr close <n>` | Close without merge |
| `gh issue view <n>` | View issue |
| `gh api <path>` | Raw API calls |

## Creating Pull Requests

### Standard Workflow

When asked to create a PR, Claude follows this sequence:

#### Step 1: Gather Context (Parallel)

```bash
# Run simultaneously
git status                              # Current state
git diff main...HEAD                    # Full diff from base
git log main..HEAD --oneline            # All commits to include
git rev-parse --abbrev-ref HEAD         # Current branch name
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null  # Check upstream
```

#### Step 2: Analyze All Commits

Important: Look at ALL commits in the PR, not just the latest:
- Review each commit message
- Understand the complete change set
- Identify the overall purpose

#### Step 3: Push if Needed

```bash
# Push with upstream tracking
git push -u origin $(git branch --show-current)
```

#### Step 4: Create PR with Heredoc

```bash
gh pr create --title "feat(auth): implement OAuth2 login" --body "$(cat <<'EOF'
## Summary
- Add OAuth2 authentication flow
- Implement token refresh mechanism
- Add login/logout UI components

## Test plan
- [ ] Manual login flow with test OAuth provider
- [ ] Verify token refresh works after expiration
- [ ] Test logout clears all stored tokens
- [ ] Check error handling for failed auth
EOF
)"
```

### PR Description Template

```markdown
## Summary
<1-3 bullet points describing what changed and why>

## Test plan
<Bulleted checklist of testing steps>

## Notes (optional)
<Additional context for reviewers>

## Related (optional)
<Links to issues, other PRs, docs>
```

### Extended Template (Complex Changes)

```markdown
## Summary
Brief description of the change.

### What
- Bullet point of change 1
- Bullet point of change 2
- Bullet point of change 3

### Why
Explanation of motivation and context.

## Test plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing steps:
  - [ ] Step 1
  - [ ] Step 2

## Breaking changes
- List any breaking changes
- Migration steps if needed

## Screenshots (if UI change)
Before: [image]
After: [image]

## Related
- Fixes #123
- Related to #456
- Depends on #789
```

## PR Creation Options

### Basic PR

```bash
gh pr create --title "Fix login bug" --body "Fixes null pointer in auth flow"
```

### PR with Labels

```bash
gh pr create --title "..." --body "..." --label "bug,priority:high"
```

### PR with Reviewers

```bash
gh pr create --title "..." --body "..." --reviewer "username1,username2"
```

### PR with Assignee

```bash
gh pr create --title "..." --body "..." --assignee "@me"
```

### Draft PR

```bash
gh pr create --title "..." --body "..." --draft
```

### PR to Specific Base Branch

```bash
gh pr create --title "..." --body "..." --base develop
```

### Full Example

```bash
gh pr create \
  --title "feat(api): add rate limiting" \
  --body "$(cat <<'EOF'
## Summary
- Implement sliding window rate limiting
- Add configurable limits per endpoint
- Return appropriate 429 responses

## Test plan
- [ ] Unit tests for rate limiter
- [ ] Integration tests with mock time
- [ ] Manual testing with curl
EOF
)" \
  --label "enhancement" \
  --reviewer "lead-dev" \
  --assignee "@me"
```

## Viewing Pull Requests

### View PR Details

```bash
gh pr view 123              # View specific PR
gh pr view                  # View PR for current branch
gh pr view 123 --web        # Open in browser
```

### View PR Diff

```bash
gh pr diff 123              # View diff
gh pr diff 123 --patch      # Patch format
```

### View PR Checks

```bash
gh pr checks 123            # CI/CD status
gh pr checks 123 --watch    # Watch until complete
```

### View PR Comments

```bash
# Get all comments
gh api repos/{owner}/{repo}/pulls/123/comments

# Get review comments
gh api repos/{owner}/{repo}/pulls/123/reviews
```

### List PRs

```bash
gh pr list                  # Open PRs
gh pr list --state all      # All PRs
gh pr list --author @me     # Your PRs
gh pr list --label bug      # PRs with label
```

## Code Review Workflows

### Reviewing a PR

```bash
# 1. Fetch and checkout PR
gh pr checkout 123

# 2. View the changes
gh pr diff 123

# 3. Run tests locally
bun test

# 4. Leave review
gh pr review 123 --approve
# OR
gh pr review 123 --request-changes --body "Please fix X"
# OR
gh pr review 123 --comment --body "Consider changing Y"
```

### Adding Review Comments

```bash
# Comment on specific line (via API)
gh api repos/{owner}/{repo}/pulls/123/comments \
  -f body="This could be simplified" \
  -f commit_id="abc123" \
  -f path="src/file.ts" \
  -f line=42
```

### Requesting Review

```bash
gh pr edit 123 --add-reviewer "username"
```

## Addressing Review Feedback

### Workflow

1. **Read feedback**: `gh pr view 123` or `gh api repos/.../pulls/123/comments`
2. **Make changes**: Edit files as requested
3. **Commit fixes**: Use clear commit messages
4. **Push updates**: `git push`
5. **Reply to comments**: Via web UI or API

### Commit Messages for Fixes

```bash
git commit -m "$(cat <<'EOF'
fix: address review feedback

- Simplify error handling per reviewer suggestion
- Add missing null check
- Update tests for edge case
EOF
)"
```

### Marking Comments Resolved

Via gh API:
```bash
# Get comment ID first
gh api repos/{owner}/{repo}/pulls/123/comments

# Mark as resolved (graphQL needed for this)
# Usually done via web UI
```

## Merge Strategies

### Merge Commit (Default)

```bash
gh pr merge 123 --merge
```

Creates a merge commit preserving all history.

### Squash Merge

```bash
gh pr merge 123 --squash
```

Combines all commits into one. Good for:
- Feature branches with messy history
- WIP commits that shouldn't be preserved

### Rebase Merge

```bash
gh pr merge 123 --rebase
```

Applies commits on top of base branch. Good for:
- Linear history preference
- Clean commit history

### Auto-Merge

```bash
gh pr merge 123 --auto --squash
```

Merges automatically when:
- All checks pass
- Required reviews approved
- No conflicts

### Delete Branch After Merge

```bash
gh pr merge 123 --merge --delete-branch
```

## PR Status Updates

### Mark as Ready

```bash
gh pr ready 123           # Remove draft status
```

### Convert to Draft

```bash
gh pr ready 123 --undo    # Make draft again
```

### Close Without Merge

```bash
gh pr close 123           # Close PR
gh pr close 123 --comment "Closing: superseded by #456"
```

### Reopen

```bash
gh pr reopen 123
```

## Working with Forks

### Create PR from Fork

```bash
# From your fork
gh pr create --repo upstream/repo --title "..." --body "..."
```

### Checkout PR from Fork

```bash
gh pr checkout 123        # Works across forks
```

## Common PR Patterns

### Feature PR

```bash
gh pr create --title "feat(dashboard): add analytics widget" --body "$(cat <<'EOF'
## Summary
- Add real-time analytics widget to dashboard
- Display user engagement metrics
- Configurable time ranges

## Test plan
- [ ] Widget renders correctly
- [ ] Data updates in real-time
- [ ] Time range selector works
- [ ] Handles loading/error states

## Screenshots
[Add screenshots of widget]
EOF
)"
```

### Bug Fix PR

```bash
gh pr create --title "fix(auth): resolve session timeout issue" --body "$(cat <<'EOF'
## Summary
- Fix premature session expiration
- Extend token refresh window
- Add retry logic for failed refreshes

## Root cause
Token refresh was racing with expiration check.

## Test plan
- [ ] Sessions persist across expected duration
- [ ] Token refresh works reliably
- [ ] No regression in logout flow

Fixes #234
EOF
)"
```

### Documentation PR

```bash
gh pr create --title "docs: update API authentication guide" --body "$(cat <<'EOF'
## Summary
- Add OAuth2 flow documentation
- Include code examples for all languages
- Update authentication troubleshooting

## Test plan
- [ ] All code examples tested
- [ ] Links work correctly
- [ ] Renders properly in GitHub
EOF
)"
```

### Dependency Update PR

```bash
gh pr create --title "chore(deps): update dependencies" --body "$(cat <<'EOF'
## Summary
- Update React 18.2 -> 18.3
- Update TypeScript 5.3 -> 5.4
- Update testing-library packages

## Test plan
- [ ] All tests pass
- [ ] Build succeeds
- [ ] No runtime errors in dev

## Breaking changes
None expected - minor version updates only.
EOF
)"
```

## PR Checklist

Before creating a PR:

- [ ] All commits are included (`git log main..HEAD`)
- [ ] Changes reviewed (`git diff main...HEAD`)
- [ ] Branch pushed to remote
- [ ] Title follows conventional format
- [ ] Description explains "what" and "why"
- [ ] Test plan is actionable
- [ ] Sensitive data removed
- [ ] Related issues linked

After creating:

- [ ] PR URL returned to user
- [ ] Checks passing (or explained if failing)
- [ ] Reviewers assigned if needed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No commits between main and HEAD" | You're on main branch, create feature branch first |
| "gh: command not found" | Install GitHub CLI: `brew install gh` |
| "HTTP 401" | Run `gh auth login` |
| "No upstream configured" | `git push -u origin branch-name` |
| "PR already exists" | Use `gh pr view` to see existing PR |
| "Merge conflicts" | Resolve locally, push, then merge |
