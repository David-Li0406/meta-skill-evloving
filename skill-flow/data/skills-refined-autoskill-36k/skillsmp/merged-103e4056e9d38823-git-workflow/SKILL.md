---
name: git-workflow
description: Use this skill for managing Git branches, commits, and pull requests, including creating feature branches, following commit conventions, and ensuring proper PR workflows.
---

# Git Workflow Management

## Branch Naming

Format: `type/description`

| Type     | Use For            | Example                |
| -------- | ------------------ | ---------------------- |
| feat     | New features       | `feat/add-user-auth`   |
| fix      | Bug fixes          | `fix/login-redirect`   |
| chore    | Maintenance        | `chore/update-deps`    |
| docs     | Documentation      | `docs/api-reference`   |
| refactor | Code restructuring | `refactor/auth-module` |

## Branch Operations

```bash
# Check current branch
git branch --show-current

# Create feature branch from main
git checkout main && git pull origin main
git checkout -b <branch-name>

# Check for existing branch
git branch -a | grep -i "<branch-name>"
```

## Commit Convention

Format: `#<issue>: <type>(<scope>): <description>`

### Types

| Type       | Description                               |
| ---------- | ----------------------------------------- |
| `feat`     | New features                              |
| `fix`      | Bug fixes                                 |
| `docs`     | Documentation changes                     |
| `style`    | Code style (formatting, no logic changes) |
| `refactor` | Code changes (neither fix nor feature)    |
| `perf`     | Performance improvements                  |
| `test`     | Adding or correcting tests                |
| `chore`    | Dependencies, tooling, build              |
| `ci`       | CI configuration changes                  |
| `revert`   | Revert a previous commit                  |

### Examples

```bash
# Simple commit
git commit -m "#<issue>: feat(auth): add user authentication endpoint"

# Multi-line commit
git commit -m "$(cat <<'EOF'
#<issue>: feat(auth): add user authentication

- Implement JWT token generation
- Add password hashing

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Pull Request Creation

```bash
# Push branch
git push -u origin <branch-name>

# Create PR
gh pr create --title "#<issue>: <title>" --body "$(cat <<'EOF'
## Summary
[Brief description]

Closes #<issue>

## Changes
- [Change 1]

## Testing
- [How tested]

---
Generated with Claude Code
EOF
)" --reviewer <reviewer>
```

## Full Workflow

```bash
# 1. Create branch from main
git checkout main
git pull
git checkout -b <branch-name>

# 2. Make changes
# ... edit files ...

# 3. Stage and commit
git add <files>
git commit -m "#<issue>: feat(scope): add feature description"

# 4. Push to remote
git push -u origin <branch-name>

# 5. Create PR
gh pr create --title "#<issue>: <title>" --body "..."

# 6. After review, merge
gh pr merge --squash
```

## Safety Rules

- NEVER commit directly to `main`
- NEVER force push to shared branches
- NEVER skip pre-commit hooks without approval
- Always create PRs for code review

## Common Mistakes

| Mistake                    | Correct Pattern                       |
| -------------------------- | ------------------------------------- |
| `Fix bug`                  | `fix(scope): correct bug description` |
| `feat: Added feature`      | `feat: add feature` (imperative mood) |
| `feat(ui): Fix button.`    | `feat(ui): fix button` (no period)    |
| `FEAT: add feature`        | `feat: add feature` (lowercase)       |
| Committing without staging | `git add <files>` first               |
| Pushing to main directly   | Create feature branch first           |

## Delegation

- **Branch strategy questions**: Ask user for preferences
- **Merge conflicts**: Use `git mergetool` or resolve manually
- **PR reviews**: Use `code-reviewer` agent