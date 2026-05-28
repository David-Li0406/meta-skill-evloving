---
name: git-workflow
description: Git workflow, branching, commits, and PRs for Pricing App
license: MIT
metadata:
  author: pricing-app
  version: "1.0.0"
  scope: [root]
  auto_invoke:
    - "Creating git commits"
    - "Creating branches"
    - "Opening pull requests"
    - "Git workflow questions"
allowed-tools: Bash
---

# Git Workflow - Pricing App

---

## BRANCH STRATEGY

### Main Branches
- **`main`** - Production (NEVER commit directly)
- **`develop`** - Development (default for PRs)

### Working Branches
- **`feature/*`** - New features
- **`fix/*`** - Bug fixes
- **`refactor/*`** - Code improvements
- **`hotfix/*`** - Emergency production fixes

---

## DAILY WORKFLOW

### 1. Start New Work

```bash
# Sync develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/short-description
```

**Naming:**
- `feature/agregar-dashboard`
- `fix/corregir-calculo-markup`
- `refactor/migrate-pydantic-v2`

### 2. Make Changes & Commit

```bash
# Stage changes
git add .

# Commit with conventional commits
git commit -m "feat: add dashboard de ventas"
```

### 3. Push & Create PR

```bash
# Push branch
git push origin feature/short-description

# Open PR to develop in GitHub
# Title: same as commit message
# Description: what, why, how to test
```

### 4. After Merge

```bash
# Delete local branch
git branch -d feature/short-description

# Sync develop
git checkout develop
git pull origin develop
```

---

## COMMIT MESSAGE FORMAT

Use **Conventional Commits**:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat** - New feature
- **fix** - Bug fix
- **refactor** - Code refactor (no bug/feature)
- **docs** - Documentation only
- **style** - Formatting, semicolons (no logic change)
- **test** - Adding tests
- **chore** - Build, dependencies, tools
- **perf** - Performance improvement

### Examples

```bash
# Good
git commit -m "feat: agregar filtro por categoría en productos"
git commit -m "fix: corregir cálculo de markup en rebate ML"
git commit -m "refactor: extraer lógica de pricing a service"
git commit -m "docs: actualizar README con nuevas features"

# Bad
git commit -m "changes"
git commit -m "fix stuff"
git commit -m "wip"
```

### Multi-line Commits

```bash
git commit -m "fix: corregir validación de JWT en login

El token expiraba antes de tiempo por timezone incorrecto.
Ahora usa datetime.now(UTC) en lugar de utcnow().

Closes #42"
```

---

## COMMON TASKS

### Create Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-descriptivo
# ... work ...
git add .
git commit -m "feat: descripción"
git push origin feature/nombre-descriptivo
# PR to develop
```

### Quick Fix

```bash
git checkout develop
git pull origin develop
git checkout -b fix/nombre-bug
# ... fix ...
git add .
git commit -m "fix: descripción del fix"
git push origin fix/nombre-bug
# PR to develop
```

### Update Branch with Latest develop

```bash
# If your branch is behind develop
git checkout feature/mi-branch
git merge develop
# or
git rebase develop
```

### Hotfix (Emergency Production Fix)

```bash
# ONLY for critical production bugs
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug
# ... fix ...
git add .
git commit -m "hotfix: descripción crítica"
git push origin hotfix/critical-bug
# PR to main (urgent)
# Then merge main back to develop
```

---

## PULL REQUEST RULES

### Title
- Use same format as commit: `feat: add dashboard`
- Be specific and descriptive

### Description Template

```markdown
## Description
Brief explanation of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Documentation

## Testing
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Tested functionality manually
- [ ] No console errors

## Screenshots (if applicable)
[Add screenshots for UI changes]
```

### Target Branch
- ✅ **Default:** `develop`
- ❌ **NEVER:** `main` (except for hotfixes or releases)

---

## MERGE STRATEGIES

### When to Use Each

**Squash and Merge** (recommended for features)
- Combines all commits into one
- Clean history
- Use for: feature branches with many WIP commits

**Merge Commit** (recommended for releases)
- Keeps all commits
- Full history preserved
- Use for: develop → main releases

**Rebase and Merge** (advanced)
- Linear history
- Use if you know what you're doing

---

## RELEASE TO PRODUCTION

### Create Release

```bash
# 1. Ensure develop is stable
# 2. Create PR: develop → main
# Title: "Release v1.x.0"
# 3. Review and merge
# 4. Tag the release

git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release v1.2.0: description"
git push origin v1.2.0
```

### Semantic Versioning

- **MAJOR (v2.0.0)** - Breaking changes
- **MINOR (v1.1.0)** - New features (backward compatible)
- **PATCH (v1.0.1)** - Bug fixes

---

## COMMON PITFALLS

### ❌ DON'T

- Don't commit directly to `main` or `develop`
- Don't commit without testing locally
- Don't use vague commit messages ("fix", "changes")
- Don't include secrets (.env, credentials)
- Don't commit node_modules, __pycache__, etc
- Don't force push to shared branches

### ✅ DO

- Create feature branch for each change
- Write descriptive commit messages
- Test before pushing
- Review your own diff before PR
- Keep commits atomic (one logical change)
- Use .gitignore properly

---

## GITIGNORE ESSENTIALS

**Already configured, but verify:**

```gitignore
# Python
__pycache__/
*.pyc
venv/
.env

# Node
node_modules/
.env

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## TROUBLESHOOTING

### Committed to Wrong Branch

```bash
# If not pushed yet
git reset --soft HEAD~1  # undo commit, keep changes
git stash
git checkout correct-branch
git stash pop
git commit -m "..."
```

### Accidentally Pushed to main

```bash
# Contact maintainer immediately
# They can revert or force push
# Don't try to fix yourself
```

### Merge Conflicts

```bash
# Update your branch
git checkout feature/mi-branch
git merge develop

# Fix conflicts in files
# Look for <<<<<<< markers
# Keep what you need, remove markers

git add .
git commit -m "merge: resolve conflicts with develop"
git push
```

### Forgot to Create Branch

```bash
# If you haven't committed yet
git stash
git checkout develop
git checkout -b feature/correct-branch
git stash pop

# If you already committed (not pushed)
git checkout -b feature/correct-branch
# Your commit is now in the new branch
```

---

## QUICK REFERENCE

```bash
# Check status
git status

# See diff
git diff

# See commit history
git log --oneline -10

# See branches
git branch -a

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name

# Undo last commit (not pushed)
git reset --soft HEAD~1

# Discard local changes
git restore .
```

---

## WHEN TO ASK FOR HELP

- Force push needed (usually bad)
- Pushed sensitive data (.env, keys)
- Broke main branch somehow
- Complex merge conflicts
- Lost commits

**Don't try to fix main alone. Ask maintainer.**

---

## REFERENCES

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [BRANCHING.md](../../BRANCHING.md) - Full Git Flow documentation
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contributor guide
