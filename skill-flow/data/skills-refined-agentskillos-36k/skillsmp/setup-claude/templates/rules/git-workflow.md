# Git Workflow Rules

Version control conventions for consistent collaboration.

## Always Do

- **Write meaningful commit messages** - Explain why, not just what
- **Keep commits atomic** - One logical change per commit
- **Use feature branches** - Never commit directly to main
- **Pull before pushing** - Stay up to date with remote
- **Review before merging** - All code needs a second pair of eyes
- **Run tests before committing** - Don't break the build
- **Keep branches short-lived** - Merge within days, not weeks
- **Delete merged branches** - Keep the repo clean
- **Use .gitignore** - Don't commit generated/sensitive files
- **Sign commits** - Use GPG signing when possible

## Never Do

- ❌ **Force push to main** - Rewrites shared history
- ❌ **Commit secrets** - No API keys, passwords, .env files
- ❌ **Commit large binaries** - Use Git LFS or external storage
- ❌ **Use vague messages** - No "fix", "update", "wip"
- ❌ **Commit broken code** - Tests should pass
- ❌ **Mix unrelated changes** - Separate concerns into separate commits
- ❌ **Commit node_modules** - Use .gitignore
- ❌ **Rebase public branches** - Only rebase local work
- ❌ **Skip code review** - Even for "small" changes

## Commit Message Format

### Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `chore` | Maintenance, dependencies |
| `ci` | CI/CD changes |

### Examples

**Good**:
```
feat(auth): add password reset functionality

- Add reset password endpoint
- Create email template
- Add rate limiting

Closes #123
```

```
fix(cart): prevent negative quantities

Quantities below 1 were causing calculation errors.
Now validates and clamps to minimum of 1.

Fixes #456
```

```
refactor(api): extract validation logic to shared module

No functional changes. Improves reusability
and reduces duplication across endpoints.
```

**Bad**:
```
fix stuff
```

```
WIP
```

```
update code
```

## Branch Naming

### Format

```
<type>/<ticket>-<description>
```

### Examples

```
feat/AUTH-123-password-reset
fix/CART-456-negative-quantities
refactor/API-789-validation-module
docs/README-update
```

### Types for Branches

| Prefix | Purpose |
|--------|---------|
| `feat/` | New features |
| `fix/` | Bug fixes |
| `refactor/` | Code improvements |
| `docs/` | Documentation |
| `test/` | Test additions |
| `chore/` | Maintenance |

## Pull Request Process

### Creating a PR

1. **Ensure branch is up to date**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run all checks**:
   ```bash
   npm run lint
   npm run typecheck
   npm run test
   ```

3. **Write clear PR description**:
   ```markdown
   ## Summary
   [What does this PR do?]

   ## Changes
   - Change 1
   - Change 2

   ## Testing
   - [ ] Unit tests added
   - [ ] Tested manually

   ## Screenshots (if UI change)
   [Before/after images]
   ```

### Reviewing a PR

1. **Check the code**:
   - Does it follow conventions?
   - Are there security issues?
   - Is it well-tested?
   - Is it maintainable?

2. **Run it locally** if needed:
   ```bash
   git fetch origin
   git checkout feat/branch-name
   npm install
   npm run dev
   ```

3. **Provide constructive feedback**:
   - Be specific about issues
   - Suggest alternatives
   - Acknowledge good work

### Merging

1. **Squash or merge**:
   - Squash: Clean history, one commit per feature
   - Merge: Preserve commit history

2. **Delete the branch** after merging

3. **Verify deployment** if applicable

## Git Commands Reference

### Daily Workflow

```bash
# Start new feature
git checkout main
git pull
git checkout -b feat/TICKET-123-description

# Work on feature
git add .
git commit -m "feat(scope): description"

# Stay up to date
git fetch origin
git rebase origin/main

# Push and create PR
git push -u origin feat/TICKET-123-description
```

### Fixing Mistakes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Amend last commit message
git commit --amend -m "new message"

# Discard local changes
git checkout -- .

# Undo pushed commit (creates new commit)
git revert HEAD
```

### Useful Commands

```bash
# See what changed
git status
git diff
git log --oneline -10

# Stash work temporarily
git stash
git stash pop

# Interactive rebase (local only!)
git rebase -i HEAD~3
```

## Exceptions

1. **Hotfixes** - May bypass normal PR process with approval
2. **Documentation** - Minor typo fixes may be direct-committed
3. **Generated files** - May use automated commit messages
4. **Initial setup** - First commits don't need full format

## .gitignore Essentials

Always ignore:
```gitignore
# Dependencies
node_modules/
.pnpm-store/

# Environment
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
.next/

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test coverage
coverage/
```
