---
name: Git Workflow & CI/CD
description: Git conventions, branch strategy, commit messages, Husky hooks, and GitHub Actions.
---

# Git Workflow & CI/CD

## Context

Lumira V2 uses a structured Git workflow with automated CI/CD via GitHub Actions.

---

## Branch Strategy

```
main
├── develop          # Integration branch
│   ├── feature/*    # New features
│   ├── fix/*        # Bug fixes
│   └── refactor/*   # Code improvements
└── release/*        # Production releases
```

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/[ticket]-description` | `feature/LP-123-user-onboarding` |
| Bug Fix | `fix/[ticket]-description` | `fix/LP-456-login-error` |
| Refactor | `refactor/description` | `refactor/mission-service` |
| Release | `release/vX.Y.Z` | `release/v2.1.0` |
| Hotfix | `hotfix/description` | `hotfix/critical-auth-bug` |

---

## Commit Messages

### Conventional Commits Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code change, no new feature |
| `test` | Adding tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvement |

### Examples

```bash
feat(missions): add filtering by location
fix(auth): resolve token refresh loop
docs(readme): update deployment instructions
refactor(api): extract mission service
chore(deps): update prisma to 5.7
```

---

## Husky Git Hooks

### Configuration

```bash
# Install husky
pnpm prepare

# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
npx lint-staged
```

### Lint-Staged

```json
// package.json
{
  "lint-staged": {
    "**/*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "**/*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

---

## Pull Request Workflow

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation

## Testing
- [ ] Unit tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing done

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process

1. Create PR from feature branch to `develop`
2. Automated checks run (lint, test, build)
3. Request review from team member
4. Address feedback
5. Squash merge when approved

---

## GitHub Actions CI/CD

### CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build

  e2e:
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Coolify Deployment
        run: |
          curl -X POST ${{ secrets.COOLIFY_WEBHOOK_URL }}
```

---

## Release Process

### Semantic Versioning

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └── Bug fixes
  │     └──────── New features (backward compatible)
  └────────────── Breaking changes
```

### Release Checklist

1. Create `release/vX.Y.Z` branch from `develop`
2. Update version in `package.json`
3. Update CHANGELOG.md
4. Create PR to `main`
5. Merge and tag release
6. Deploy to production

```bash
# Create tag
git tag -a v2.1.0 -m "Release v2.1.0"
git push origin v2.1.0
```

---

## Common Commands

```bash
# Create feature branch
git checkout -b feature/LP-123-new-feature develop

# Rebase on develop
git fetch origin
git rebase origin/develop

# Squash commits before PR
git rebase -i HEAD~3

# Amend last commit
git commit --amend

# Cherry-pick to hotfix
git cherry-pick <commit-hash>
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Write descriptive commits | Use "fix" or "update" alone |
| Squash before merging | Merge with 50+ commits |
| Keep PRs small (<400 lines) | Create massive PRs |
| Run tests before pushing | Push broken code |
| Update branch regularly | Let branch get stale |
