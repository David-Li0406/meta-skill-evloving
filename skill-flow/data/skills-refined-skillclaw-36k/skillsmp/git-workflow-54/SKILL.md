---
name: git-workflow
description: Git workflow for branches, commits, and PRs. Use for commit, branch, pr, pull request, conventional, push, feat, fix, chore, merge, rebase
---

# Git Workflow

## Quick Start

```bash
# Create feature branch
git checkout -b feat/add-user-auth

# Make changes and commit
git add src/auth/
git commit -m "feat(auth): add user authentication"

# Push and create PR
git push -u origin feat/add-user-auth
gh pr create --title "feat(auth): add user authentication" --body "..."
```

## Branch Naming

```text
type/description
```

| Type     | Use For            | Example                |
| -------- | ------------------ | ---------------------- |
| feat     | New features       | `feat/add-user-auth`   |
| fix      | Bug fixes          | `fix/login-redirect`   |
| chore    | Maintenance        | `chore/update-deps`    |
| docs     | Documentation      | `docs/api-reference`   |
| refactor | Code restructuring | `refactor/auth-module` |

## Conventional Commits

```text
type(scope): subject

body (optional)

footer (optional)
```

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

### Scopes

| Category | Scopes                                                                   |
| -------- | ------------------------------------------------------------------------ |
| Apps     | `web`                                                                    |
| Packages | `auth`, `config`, `database`, `ui`, `eslint-config`, `typescript-config` |
| Tooling  | `deps`, `ci`                                                             |

Custom scopes allowed. Scope is optional.

### Rules

- Subject: imperative mood, no period, lowercase
- Header max length: 200 characters
- Body: optional, use `|` for line breaks in interactive mode

### Examples

```bash
# Feature
git commit -m "feat(auth): add password reset flow"

# Bug fix
git commit -m "fix(ui): correct button alignment on mobile"

# Chore
git commit -m "chore(deps): update react to v19"

# With scope
git commit -m "refactor(database): simplify user queries"

# Without scope
git commit -m "docs: update README installation steps"
```

## PR Creation

```bash
gh pr create --title "feat(auth): add user authentication" --body "$(cat <<'EOF'
## Summary
- Add login/logout functionality
- Add session management
- Add auth middleware

## Test plan
- [ ] Verify login flow works
- [ ] Verify logout clears session
- [ ] Verify protected routes redirect
EOF
)"
```

### PR Template

```markdown
## Summary

<1-3 bullet points describing the change>

## Test plan

- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] Edge cases verified
```

## Full Workflow

```bash
# 1. Create branch from main
git checkout main
git pull
git checkout -b feat/my-feature

# 2. Make changes
# ... edit files ...

# 3. Stage and commit
git add src/
git commit -m "feat(scope): add feature description"

# 4. Push to remote
git push -u origin feat/my-feature

# 5. Create PR
gh pr create --title "feat(scope): add feature description" --body "..."

# 6. After review, merge
gh pr merge --squash
```

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
