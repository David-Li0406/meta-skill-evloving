---
name: git-workflow-skills
description: Provides standardized Git workflows, commit message conventions, branching strategies, and collaboration patterns for all agents performing Git operations. Use when creating commits, choosing branching strategies, creating PRs, performing git operations (merge vs rebase), or handling git collaboration workflows.
license: MIT
---

# Git Workflow Skills

## Overview

This skill provides comprehensive Git workflow guidance for agents performing version control operations. It covers commit message conventions (Conventional Commits), branching strategies (GitHub Flow, Git Flow, Trunk-based), PR best practices, git operation patterns (merge vs rebase vs squash), collaboration workflows, and security considerations.

Use this skill whenever performing git operations to ensure consistency, maintainability, and professional quality across all projects.

## Core Principles

1. **Clarity Over Cleverness**: Commit messages and branch names should be immediately understandable
2. **Atomic Commits**: One logical change per commit (enables easy revert, clear history)
3. **Safety First**: Never commit secrets, avoid force push to protected branches
4. **Team Consistency**: Follow project conventions, communicate through commits and PRs
5. **History Matters**: Clean, readable history is a project asset

## Commit Message Conventions

### Conventional Commits Format

Follow the Conventional Commits specification for all commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Components**:
- **type** (required): feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- **scope** (optional): Component/module affected (e.g., auth, api, ui, database)
- **subject** (required): Brief description (50 chars max, imperative mood, no period)
- **body** (optional): Detailed explanation (wrap at 72 chars)
- **footer** (optional): Breaking changes, issue references

### Commit Types

**feat**: New feature for the user
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.
Includes token refresh mechanism and session management.

Closes #142
```

**fix**: Bug fix for the user
```
fix(api): prevent race condition in user creation

Add database transaction lock to prevent duplicate user records
when multiple requests arrive simultaneously.

Fixes #238
```

**docs**: Documentation changes only
```
docs(readme): add installation instructions for Windows

Include troubleshooting section for common Windows-specific issues.
```

**style**: Code formatting, missing semicolons, whitespace (no logic change)
```
style(components): format with prettier, remove trailing whitespace
```

**refactor**: Code change that neither fixes bug nor adds feature
```
refactor(database): extract query builder into separate class

Improve code organization and testability by separating query
construction from execution logic.
```

**test**: Adding or updating tests
```
test(auth): add integration tests for OAuth flow
```

**chore**: Maintenance tasks, dependency updates, build configuration
```
chore(deps): upgrade React from 18.2.0 to 18.3.0
```

**perf**: Performance improvement
```
perf(api): add database indexes for user queries

Reduce user lookup time from 250ms to 15ms by indexing email column.
```

**ci**: CI/CD configuration changes
```
ci(github): add automated deployment to staging environment
```

**build**: Build system or external dependency changes
```
build(webpack): optimize bundle size with code splitting
```

**revert**: Reverts a previous commit
```
revert: feat(auth): add OAuth2 login support

This reverts commit a1b2c3d4. OAuth implementation needs rework
due to security concerns identified in code review.
```

### Breaking Changes

Indicate breaking changes with `!` after type/scope and in footer:

```
feat(api)!: change user endpoint response format

BREAKING CHANGE: User API now returns `userId` instead of `id`.
Clients must update to use new field name.

Migration guide: https://docs.example.com/migration-v2
```

### Good vs Bad Commit Messages

**❌ Bad Examples**:
```
Update files
Fix bug
WIP
asdf
Changed some stuff
Fixed it
```

**✅ Good Examples**:
```
feat(search): add fuzzy matching for product queries
fix(checkout): calculate tax correctly for international orders
docs(api): update authentication examples
refactor(utils): extract date formatting into helper function
```

### Multi-line Commit Messages

Use multi-line messages for non-trivial changes:

```
feat(notifications): implement real-time notification system

Add WebSocket-based notification delivery for user actions.
Includes:
- WebSocket server with connection pooling
- Client-side notification queue with retry logic
- Notification preferences UI
- Email fallback for offline users

Performance: Handles 10k concurrent connections with <100ms latency.

Closes #156, #187
```

### Integration with Claude Code

When agents create commits, always:
1. Analyze `git diff` to understand changes
2. Determine appropriate type (feat, fix, docs, etc.)
3. Identify scope from files changed
4. Write clear subject line (imperative mood)
5. Add body for non-trivial changes explaining "why"
6. Include Claude Code footer:
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

## Branching Strategies

### Strategy Selection Guide

**Choose GitHub Flow** (recommended for most projects):
- ✅ Continuous deployment
- ✅ Small to medium teams
- ✅ Web applications
- ✅ Simple release process

**Choose Git Flow**:
- ✅ Scheduled releases
- ✅ Multiple production versions
- ✅ Enterprise software
- ✅ Complex release management

**Choose Trunk-based Development**:
- ✅ Very frequent deployments
- ✅ Strong CI/CD pipeline
- ✅ Experienced team
- ✅ Feature flags in place

### GitHub Flow (Recommended)

**Branches**:
- `main`: Always deployable, protected
- `feature/*`: Short-lived feature branches

**Workflow**:
1. Create feature branch from `main`: `feature/add-user-search`
2. Commit changes with conventional commits
3. Push to remote and create PR
4. Code review and CI checks
5. Merge to `main` (squash or merge commit)
6. Deploy `main` to production
7. Delete feature branch

**Branch naming**:
```
feature/add-oauth-login
feature/user-profile-page
bugfix/fix-login-redirect
hotfix/patch-security-vulnerability
docs/update-api-documentation
```

**Example workflow**:
```bash
# Start feature
git checkout main
git pull origin main
git checkout -b feature/add-search-filter

# Work on feature
git add src/components/SearchFilter.tsx
git commit -m "feat(search): add category filter to search UI"

# Push and create PR
git push -u origin feature/add-search-filter
gh pr create --title "Add category filter to search" --body "..."

# After PR approval
# Merge via GitHub UI (squash recommended)
# Delete branch
git checkout main
git pull origin main
git branch -d feature/add-search-filter
```

### Git Flow

**Branches**:
- `main`: Production releases only
- `develop`: Integration branch
- `feature/*`: Feature development
- `release/*`: Release preparation
- `hotfix/*`: Production hotfixes

**Workflow**:
1. Feature: Branch from `develop`, merge back to `develop`
2. Release: Branch from `develop`, merge to `main` and `develop`
3. Hotfix: Branch from `main`, merge to `main` and `develop`

**Use when**: Managing multiple release versions, scheduled releases, complex projects

**Example**:
```bash
# Feature development
git checkout develop
git checkout -b feature/payment-integration
# ... work ...
git checkout develop
git merge --no-ff feature/payment-integration

# Release
git checkout -b release/1.2.0 develop
# ... version bump, changelog ...
git checkout main
git merge --no-ff release/1.2.0
git tag -a v1.2.0
git checkout develop
git merge --no-ff release/1.2.0
```

### Trunk-based Development

**Branches**:
- `main`: The trunk, always deployable
- `feature/*`: Very short-lived (< 1 day)

**Workflow**:
1. Create small feature branch
2. Commit frequently
3. Merge to `main` within hours/1 day
4. Use feature flags for incomplete features
5. Deploy `main` frequently (multiple times per day)

**Requirements**:
- Strong automated testing
- Feature flag system
- Mature CI/CD pipeline
- Team discipline

## PR/MR Best Practices

### PR Title Format

Use conventional commit format:
```
feat(auth): add OAuth2 login support
fix(api): prevent race condition in user creation
docs(readme): add installation instructions
```

### PR Description Template

```markdown
## Summary

Brief description of what this PR does and why.

## Changes

- Add OAuth2 authentication with Google and GitHub
- Implement token refresh mechanism
- Add session management
- Update user model to store OAuth tokens

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [x] Unit tests added/updated
- [x] Integration tests added/updated
- [x] Manual testing completed
- [ ] Performance testing completed

## Test Plan

1. Test Google OAuth login flow
2. Test GitHub OAuth login flow
3. Verify token refresh after expiry
4. Test session persistence across browser restarts

## Screenshots (if applicable)

[Add screenshots of UI changes]

## Breaking Changes

None

## Related Issues

Closes #142
Related to #156

## Checklist

- [x] Code follows project style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests pass locally
- [x] Dependent changes merged
```

### PR Size Guidelines

**Optimal PR size**: 200-400 lines changed
**Maximum recommended**: 800 lines changed

**When PR is too large**:
1. Split into multiple PRs (preferred)
2. Add detailed description and comments
3. Schedule synchronous review session
4. Break into reviewable sections

### Draft PRs

Create draft PR when:
- Seeking early feedback on approach
- Work in progress, not ready for review
- Demonstrating proof of concept
- Collaborating on complex feature

Mark as "Ready for review" when:
- All tests pass
- Code is self-reviewed
- Documentation is updated
- Ready for merge after approval

### Review Request Etiquette

1. **Self-review first**: Review your own PR before requesting review
2. **Provide context**: Explain the "why" in description
3. **Highlight concerns**: Point out areas needing special attention
4. **Request specific reviewers**: Tag domain experts
5. **Be responsive**: Address feedback promptly
6. **Be respectful**: Thank reviewers, engage constructively

### Addressing Review Comments

**When making changes**:
```bash
# Make requested changes
git add src/auth/oauth.ts
git commit -m "refactor(auth): extract token validation per review feedback"
git push origin feature/add-oauth-login
```

**When resolving comments**:
- ✅ "Done, updated in commit abc123"
- ✅ "Good point, refactored to use helper function"
- ✅ "Created issue #245 to track this separately"
- ❌ "Done" (without context)
- ❌ Resolving without making changes

## Git Operations Patterns

### Merge vs Rebase vs Squash

**Merge Commit** (`git merge --no-ff`):
- **When**: Preserving complete feature branch history
- **Pros**: Full history preserved, clear feature boundaries
- **Cons**: Cluttered history with many merge commits
- **Use for**: Long-lived feature branches, collaborative branches

```bash
git checkout main
git merge --no-ff feature/add-search
# Creates merge commit
```

**Rebase** (`git rebase`):
- **When**: Keeping feature branch up to date with main
- **Pros**: Clean linear history, no merge commits
- **Cons**: Rewrites history (don't rebase public branches)
- **Use for**: Updating feature branch, cleaning up local commits

```bash
# Update feature branch with latest main
git checkout feature/add-search
git rebase main

# Interactive rebase to clean up commits
git rebase -i HEAD~5
```

**Squash Merge** (`git merge --squash`):
- **When**: Merging feature branch with many commits
- **Pros**: Clean main history, one commit per feature
- **Cons**: Loses detailed feature development history
- **Use for**: Feature branches with many WIP commits

```bash
git checkout main
git merge --squash feature/add-search
git commit -m "feat(search): add advanced search functionality"
```

### Decision Matrix

| Scenario | Operation | Reasoning |
|----------|-----------|-----------|
| Update feature branch with main | Rebase | Keep linear history |
| Merge feature to main (GitHub Flow) | Squash | Clean main history |
| Merge feature to main (Git Flow) | Merge commit | Preserve feature history |
| Clean up local commits before PR | Interactive rebase | Present clean history |
| Integrate long-lived branch | Merge commit | Preserve collaboration history |
| Apply single commit from another branch | Cherry-pick | Selective integration |

### Keeping History Clean

**Before creating PR**:
```bash
# Interactive rebase to clean up commits
git rebase -i main

# In editor, squash/fixup WIP commits:
pick a1b2c3d feat(search): add search component
fixup e4f5g6h WIP: fix typo
fixup h7i8j9k WIP: update tests
pick k0l1m2n feat(search): add filters
```

**Commit message guidelines for clean history**:
1. Each commit should be self-contained and functional
2. Commit message should describe the complete change
3. Avoid "WIP", "temp", "fix typo" commits in final history
4. Group related changes into logical commits

### Force Push Safety

**❌ Never force push to**:
- `main` / `master`
- `develop`
- Any protected branch
- Any branch others are working on

**✅ Safe to force push to**:
- Your own feature branch (before PR review)
- After interactive rebase on personal branch

**When force push is needed**:
```bash
# After rebasing/amending on feature branch
git push --force-with-lease origin feature/add-search
```

**`--force-with-lease`**: Safer than `--force`, prevents overwriting others' work

### Cherry-pick Use Cases

**When to use cherry-pick**:
1. Apply hotfix to multiple branches
2. Selectively port features across branches
3. Recover commits from abandoned branch

**Example**:
```bash
# Apply specific commit to current branch
git cherry-pick a1b2c3d

# Apply multiple commits
git cherry-pick a1b2c3d..e4f5g6h

# Cherry-pick without committing (for editing)
git cherry-pick -n a1b2c3d
```

## Collaboration Workflows

### Fork vs Branch Workflow

**Branch Workflow** (recommended for teams):
- Team members have write access to repository
- Create feature branches directly in main repository
- Use for: Internal team projects, trusted contributors

**Fork Workflow**:
- Contributors fork repository to their account
- Create feature branches in fork
- Submit PR from fork to upstream
- Use for: Open source projects, external contributors

### Keeping Branch Up to Date

**Method 1: Rebase** (clean history):
```bash
git checkout feature/add-search
git fetch origin
git rebase origin/main

# If conflicts, resolve and continue
git add .
git rebase --continue

# Force push to update PR
git push --force-with-lease origin feature/add-search
```

**Method 2: Merge** (preserve history):
```bash
git checkout feature/add-search
git fetch origin
git merge origin/main

# Resolve conflicts if any
git add .
git commit -m "merge: resolve conflicts with main"

git push origin feature/add-search
```

**Recommendation**: Use rebase for feature branches, merge for long-lived branches

### Resolving Merge Conflicts

**Workflow**:
1. Identify conflicting files: `git status`
2. Open files and locate conflict markers:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Their changes
   >>>>>>> branch-name
   ```
3. Resolve conflicts by choosing correct code
4. Remove conflict markers
5. Test the resolved code
6. Stage and commit:
   ```bash
   git add src/conflicted-file.ts
   git commit -m "merge: resolve conflicts in user authentication"
   ```

**Best practices**:
- Understand both changes before resolving
- Test thoroughly after resolution
- Communicate with other developer if unclear
- Use merge tool if conflicts are complex: `git mergetool`

### Co-authored Commits

**When multiple people contribute to a commit**:
```
feat(auth): implement OAuth2 authentication

Add Google and GitHub OAuth providers with token refresh.

Co-authored-by: Jane Developer <jane@example.com>
Co-authored-by: Bob Engineer <bob@example.com>
```

**Claude Code integration**: Always include Claude as co-author:
```
Co-authored-by: Claude <noreply@anthropic.com>
```

### Atomic Commits

**Definition**: One logical change per commit

**✅ Good (atomic)**:
```bash
# Commit 1: Add feature
git commit -m "feat(search): add search bar component"

# Commit 2: Add tests
git commit -m "test(search): add search bar component tests"

# Commit 3: Update docs
git commit -m "docs(search): document search bar API"
```

**❌ Bad (non-atomic)**:
```bash
# One commit with multiple unrelated changes
git commit -m "Add search, fix login bug, update README"
```

**Benefits of atomic commits**:
- Easy to revert specific changes
- Clear history and blame
- Simpler code review
- Enables selective cherry-picking

## Git Hooks

### Hook Types

**pre-commit**: Run before commit is created
- Linting (ESLint, Pylint)
- Code formatting (Prettier, Black)
- Type checking
- Unit tests (fast only)

**commit-msg**: Validate commit message
- Conventional commit format
- Message length
- Required patterns

**pre-push**: Run before push to remote
- Full test suite
- Build verification
- Integration tests

### Pre-commit Hook Example

**Using Husky (JavaScript projects)**:
```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "commit-msg": "commitlint -E HUSKY_GIT_PARAMS"
    }
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

**Using pre-commit framework (Python projects)**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Commit Message Validation Hook

**Using commitlint**:
```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf', 'ci', 'build', 'revert']
    ],
    'subject-max-length': [2, 'always', 50],
    'body-max-line-length': [2, 'always', 72]
  }
};
```

### Hooks vs CI/CD

**Use hooks for**:
- Fast checks (< 10 seconds)
- Formatting and linting
- Commit message validation
- Pre-push quick tests

**Use CI/CD for**:
- Full test suite
- Integration tests
- Deployment
- Security scans
- Performance tests

**Reason**: Hooks should be fast to not slow down development workflow

## Security and Safety

### Never Commit Secrets

**Common secrets to avoid**:
- API keys and tokens
- Database passwords
- Private keys (SSH, TLS, JWT)
- OAuth client secrets
- AWS/cloud credentials
- `.env` files with secrets

**Prevention with .gitignore**:
```gitignore
# Environment files
.env
.env.local
.env.*.local

# Credentials
credentials.json
secrets.yaml
*.key
*.pem

# Cloud provider
.aws/credentials
.gcloud/credentials

# IDE
.vscode/settings.json (if contains secrets)
```

### Removing Accidentally Committed Secrets

**If secret committed but not pushed**:
```bash
# Remove file from staging
git reset HEAD secrets.env

# Amend last commit
git commit --amend

# Or reset to previous commit
git reset --soft HEAD~1
```

**If secret already pushed**:
1. **Rotate the secret immediately** (most important!)
2. Remove from history:
   ```bash
   # Using git filter-repo (recommended)
   git filter-repo --path secrets.env --invert-paths

   # Or using BFG Repo-Cleaner
   bfg --delete-files secrets.env

   # Force push (coordinate with team!)
   git push --force-with-lease origin main
   ```
3. Verify secret removed: `git log --all --full-history -- secrets.env`
4. Notify team about force push

**Important**: Removing from git doesn't invalidate the secret. Always rotate!

### Signed Commits (GPG)

**Why sign commits**:
- Verify commit author identity
- Prevent impersonation
- Required for some organizations

**Setup GPG signing**:
```bash
# Generate GPG key
gpg --full-generate-key

# List keys
gpg --list-secret-keys --keyid-format=long

# Configure git
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Sign individual commit
git commit -S -m "feat(auth): add OAuth login"
```

**GitHub verification**:
1. Export public key: `gpg --armor --export YOUR_KEY_ID`
2. Add to GitHub: Settings → SSH and GPG keys → New GPG key
3. Commits show "Verified" badge

### Protected Branches

**Recommended protections for `main`**:
- ✅ Require pull request reviews (1-2 approvals)
- ✅ Require status checks (CI tests pass)
- ✅ Require signed commits (optional)
- ✅ Require linear history (optional)
- ✅ Include administrators (enforce for all)
- ✅ Restrict who can push
- ✅ Require conversation resolution

**GitHub branch protection setup**:
Repository Settings → Branches → Add rule → `main`

### Required Reviews

**Review requirements**:
- Minimum 1 approval for small teams
- Minimum 2 approvals for production code
- Code owner approval for critical paths
- Dismiss stale reviews on new commits

**CODEOWNERS file**:
```
# .github/CODEOWNERS
# Require review from team leads
/src/auth/* @auth-team
/src/api/* @backend-team
/src/ui/* @frontend-team

# Require multiple reviews for critical files
/deploy/* @devops-team @tech-leads
```

## Workflow Examples

### Example 1: Feature Development Workflow (GitHub Flow)

**Scenario**: Add user profile page

```bash
# 1. Start from updated main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-profile-page

# 3. Develop incrementally with atomic commits
git add src/pages/UserProfile.tsx
git commit -m "feat(profile): add user profile page component"

git add src/api/user.ts
git commit -m "feat(profile): add API endpoint for user data"

git add src/pages/UserProfile.test.tsx
git commit -m "test(profile): add user profile component tests"

git add docs/user-profile.md
git commit -m "docs(profile): document user profile feature"

# 4. Keep branch updated with main
git fetch origin
git rebase origin/main

# 5. Push and create PR
git push -u origin feature/user-profile-page
gh pr create \
  --title "feat(profile): add user profile page" \
  --body "$(cat <<'EOF'
## Summary
Implements user profile page with avatar, bio, and settings.

## Changes
- Add UserProfile component with responsive design
- Add API endpoint for fetching user data
- Add unit and integration tests
- Update documentation

## Test Plan
1. Navigate to /profile
2. Verify profile information displays correctly
3. Test on mobile and desktop viewports
4. Verify edit functionality

Closes #156
EOF
)"

# 6. Address review feedback
git add src/pages/UserProfile.tsx
git commit -m "refactor(profile): extract avatar component per review"
git push origin feature/user-profile-page

# 7. After PR approval and merge
git checkout main
git pull origin main
git branch -d feature/user-profile-page
```

### Example 2: Hotfix Workflow (Production Bug)

**Scenario**: Critical security vulnerability in production

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/patch-auth-vulnerability

# 2. Fix the issue
git add src/auth/oauth.ts
git commit -m "fix(auth)!: patch token validation vulnerability

BREAKING CHANGE: OAuth tokens now require signature validation.
Invalid tokens will be rejected immediately.

Security: Prevents token forgery attack (CVE-2024-XXXXX)
Closes #489"

# 3. Add tests for the fix
git add src/auth/oauth.test.ts
git commit -m "test(auth): add security tests for token validation"

# 4. Push and create urgent PR
git push -u origin hotfix/patch-auth-vulnerability
gh pr create \
  --title "fix(auth)!: patch token validation vulnerability [SECURITY]" \
  --label "security,hotfix" \
  --body "$(cat <<'EOF'
## Summary
🚨 SECURITY: Patches critical token validation vulnerability.

## Vulnerability
OAuth tokens were not properly validated, allowing token forgery.

## Fix
- Add signature validation for all OAuth tokens
- Reject invalid tokens immediately
- Add comprehensive security tests

## Breaking Change
Invalid tokens that were previously accepted will now be rejected.

## Testing
- [x] Security tests added
- [x] Manual testing with valid tokens
- [x] Manual testing with forged tokens
- [x] Backward compatibility verified

## Deployment
Requires immediate deployment to production.

Fixes #489
EOF
)"

# 5. After expedited review and merge
git checkout main
git pull origin main
git branch -d hotfix/patch-auth-vulnerability

# 6. Tag the release
git tag -a v1.2.1 -m "Hotfix: patch auth vulnerability"
git push origin v1.2.1
```

### Example 3: Refactoring Workflow (Large Code Changes)

**Scenario**: Refactor database layer for better performance

```bash
# 1. Create refactoring branch
git checkout main
git pull origin main
git checkout -b refactor/database-layer-optimization

# 2. Make incremental, atomic commits
git add src/db/connection.ts
git commit -m "refactor(db): extract connection pool configuration"

git add src/db/queries/user.ts
git commit -m "refactor(db): optimize user queries with prepared statements"

git add src/db/queries/product.ts
git commit -m "refactor(db): add database indexes for product queries

Performance improvement: Product search reduced from 250ms to 15ms"

git add src/db/transaction.ts
git commit -m "refactor(db): implement transaction helper utility"

# 3. Keep tests passing after each commit
git add src/db/queries/user.test.ts
git commit -m "test(db): update user query tests for new implementation"

# 4. Update integration tests
git add tests/integration/db.test.ts
git commit -m "test(db): add integration tests for transaction handling"

# 5. Document performance improvements
git add docs/database-optimization.md
git commit -m "docs(db): document database optimization approach and results"

# 6. Rebase onto main to stay current
git fetch origin
git rebase origin/main

# 7. Review commits are atomic and well-organized
git log --oneline origin/main..HEAD

# 8. Create PR with detailed context
git push -u origin refactor/database-layer-optimization
gh pr create \
  --title "refactor(db): optimize database layer for performance" \
  --body "$(cat <<'EOF'
## Summary
Refactors database layer to improve query performance and code organization.

## Changes
- Extract connection pool configuration for better reusability
- Optimize user and product queries with prepared statements
- Add database indexes for common query patterns
- Implement transaction helper utility
- Update all tests for new implementation

## Performance Impact
- User lookup: 180ms → 12ms (93% improvement)
- Product search: 250ms → 15ms (94% improvement)
- Checkout flow: 450ms → 85ms (81% improvement)

## Testing
- [x] All existing tests pass
- [x] Added integration tests for transactions
- [x] Performance benchmarks completed
- [x] Load testing with 1000 concurrent users

## Migration
No database migrations required. Changes are backward compatible.

## Breaking Changes
None

Related to #234
EOF
)"
```

### Example 4: Documentation Update Workflow

**Scenario**: Update API documentation for new endpoints

```bash
# 1. Create docs branch
git checkout main
git pull origin main
git checkout -b docs/update-api-documentation

# 2. Update documentation files
git add docs/api/authentication.md
git commit -m "docs(api): update OAuth authentication examples"

git add docs/api/users.md
git commit -m "docs(api): add user profile endpoint documentation"

git add docs/api/search.md
git commit -m "docs(api): document new search filters API"

git add README.md
git commit -m "docs(readme): update API reference links"

# 3. Verify documentation builds correctly
npm run docs:build

# 4. Push and create PR
git push -u origin docs/update-api-documentation
gh pr create \
  --title "docs(api): update API documentation for v2.0" \
  --body "$(cat <<'EOF'
## Summary
Updates API documentation to reflect v2.0 changes.

## Changes
- Update OAuth authentication examples
- Add user profile endpoint documentation
- Document new search filters API
- Update README with correct API reference links

## Verification
- [x] Documentation builds without errors
- [x] All links are valid
- [x] Code examples tested and working
- [x] Screenshots updated

Related to #298
EOF
)"

# 5. After review and merge
git checkout main
git pull origin main
git branch -d docs/update-api-documentation
```

### Example 5: Multi-commit Feature Workflow

**Scenario**: Implement search functionality (complex feature)

```bash
# 1. Create feature branch
git checkout main
git pull origin main
git checkout -b feature/advanced-search

# 2. Build feature incrementally with atomic commits

# Add search infrastructure
git add src/search/index.ts src/search/types.ts
git commit -m "feat(search): add search infrastructure and types"

# Add search parser
git add src/search/parser.ts
git commit -m "feat(search): implement query parser with boolean operators"

# Add search indexer
git add src/search/indexer.ts
git commit -m "feat(search): add document indexer with full-text support"

# Add search API
git add src/api/search.ts
git commit -m "feat(search): add search API endpoints"

# Add search UI component
git add src/components/SearchBar.tsx
git commit -m "feat(search): add search bar component"

# Add filters
git add src/components/SearchFilters.tsx
git commit -m "feat(search): add category and date filters"

# Add tests for each component
git add src/search/parser.test.ts
git commit -m "test(search): add query parser tests"

git add src/search/indexer.test.ts
git commit -m "test(search): add indexer tests"

git add src/components/SearchBar.test.tsx
git commit -m "test(search): add search bar component tests"

# Add integration tests
git add tests/integration/search.test.ts
git commit -m "test(search): add end-to-end search integration tests"

# Add documentation
git add docs/search.md
git commit -m "docs(search): document search API and query syntax"

# 3. Review commit history
git log --oneline origin/main..HEAD

# 4. Optionally clean up history with interactive rebase
git rebase -i origin/main
# Squash related commits if needed

# 5. Create detailed PR
git push -u origin feature/advanced-search
gh pr create \
  --title "feat(search): implement advanced search functionality" \
  --body "$(cat <<'EOF'
## Summary
Implements advanced search with boolean operators, filters, and full-text indexing.

## Features
- Full-text search with boolean operators (AND, OR, NOT)
- Category and date range filters
- Real-time search suggestions
- Search result highlighting
- Performance: <50ms for typical queries

## Changes
- Add search infrastructure (parser, indexer)
- Add search API endpoints
- Add search UI components (SearchBar, SearchFilters)
- Add comprehensive test coverage (unit + integration)
- Add documentation for search API

## Testing
- [x] Unit tests for all components
- [x] Integration tests for search flow
- [x] Performance benchmarks
- [x] Manual testing with various queries

## Screenshots
[Add screenshots of search UI]

Closes #187, #234
EOF
)"
```

## Integration with Claude Code Workflows

### When Agents Should Create Commits

Agents should create commits when:

1. **User explicitly requests**: "Create a commit", "Commit these changes"
2. **After completing task**: When deliverable is complete and tests pass
3. **Before creating PR**: When preparing to create pull request
4. **After code review changes**: When addressing review feedback

Agents should NOT automatically commit when:
- Changes are incomplete or experimental
- Tests are failing
- User hasn't reviewed the changes
- Working in interactive exploration mode

### When to Use git-expert Agent

Delegate to `git-expert` agent for:
- Complex git history manipulation (rebasing, cherry-picking)
- Resolving merge conflicts
- Git repository diagnostics
- Advanced branching strategy implementation
- Git configuration and setup
- Repository migration or cleanup

Use `git-workflow-skills` (this skill) for:
- Standard commit creation
- Following commit conventions
- Creating PRs with proper format
- Choosing merge strategy
- Applying collaboration workflows

### Commit Message Generation from Changes

**Workflow for agents creating commits**:

1. **Analyze changes**:
   ```bash
   git status
   git diff --cached
   ```

2. **Determine commit type**:
   - New files/features → `feat`
   - Bug fixes → `fix`
   - Documentation → `docs`
   - Refactoring → `refactor`
   - Tests → `test`

3. **Identify scope**:
   - From file paths: `src/auth/` → `auth`
   - Component name: `SearchBar.tsx` → `search`
   - Module name: `api/users.ts` → `api`

4. **Write subject line**:
   - Imperative mood: "add", "fix", "update" (not "added", "fixes")
   - 50 characters max
   - No period at end
   - Describe what the code does (not what you did)

5. **Add body if needed**:
   - Why the change was made
   - What problem it solves
   - Any important context
   - Wrap at 72 characters

6. **Add footer**:
   - Issue references: `Closes #123`
   - Breaking changes: `BREAKING CHANGE: ...`
   - Co-authors: `Co-authored-by: Claude <noreply@anthropic.com>`
   - Claude Code attribution

**Example agent workflow**:
```bash
# Agent analyzes changes
git diff --cached

# Changes show:
# - New file: src/components/SearchBar.tsx
# - Modified: src/api/search.ts
# - Modified: src/types/search.ts

# Agent determines:
# Type: feat (new component)
# Scope: search (from file paths)
# Subject: add search bar component with autocomplete

# Agent creates commit:
git commit -m "$(cat <<'EOF'
feat(search): add search bar component with autocomplete

Implement search bar with real-time autocomplete suggestions.
Includes debouncing for performance and keyboard navigation support.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### PR Description Generation

**Workflow for agents creating PRs**:

1. **Analyze all commits** in branch:
   ```bash
   git log origin/main..HEAD
   git diff origin/main...HEAD
   ```

2. **Summarize changes**:
   - What features were added?
   - What bugs were fixed?
   - What was refactored?
   - What documentation was updated?

3. **Identify related issues**:
   - Look for issue references in commits
   - Check commit messages for "Closes", "Fixes", "Related to"

4. **Create test plan**:
   - List manual testing steps
   - Identify automated tests
   - Highlight edge cases tested

5. **Generate PR using template** (see PR/MR Best Practices section)

## Resources

### scripts/

This skill includes validation and generation scripts for git workflows:

- **validate_commit_msg.py**: Validates commit messages against Conventional Commits specification
- **generate_commit_msg.py**: Generates commit messages from git diff output

See `scripts/README.md` for usage details.

### references/

Additional reference documentation:

- **conventional-commits-examples.md**: Extensive examples of good and bad commit messages
- **branching-strategy-comparison.md**: Detailed comparison of GitHub Flow, Git Flow, and Trunk-based Development
- **pr-templates.md**: PR description templates for different types of changes

These references provide additional context and examples without cluttering the main skill document.

## Quality Checklist

Before completing any git workflow operation, verify:

- ✅ Commit messages follow Conventional Commits format
- ✅ Commit type is appropriate (feat, fix, docs, etc.)
- ✅ Subject line is ≤50 characters, imperative mood
- ✅ Body wraps at 72 characters (if present)
- ✅ Breaking changes are clearly indicated
- ✅ Commits are atomic (one logical change each)
- ✅ No secrets or sensitive data committed
- ✅ Branch name follows convention (feature/, bugfix/, etc.)
- ✅ PR title follows commit message format
- ✅ PR description is complete and clear
- ✅ Tests pass before committing
- ✅ Code is self-reviewed
- ✅ Appropriate git operation chosen (merge vs rebase vs squash)
- ✅ Protected branches are not force-pushed
- ✅ Claude Code attribution included in commits

## Summary

This skill provides comprehensive guidance for professional git workflows. Key takeaways:

1. **Commit Messages**: Always use Conventional Commits format with clear type, scope, and subject
2. **Branching**: Choose strategy based on project needs (GitHub Flow for most, Git Flow for complex releases)
3. **PRs**: Write detailed descriptions with context, testing, and checklists
4. **Operations**: Understand merge vs rebase vs squash trade-offs
5. **Collaboration**: Keep branches updated, resolve conflicts carefully, use atomic commits
6. **Security**: Never commit secrets, use protected branches, consider signed commits
7. **Integration**: Agents should create commits when requested or after completing tasks

Refer to the reference documents for detailed examples and comparisons.
