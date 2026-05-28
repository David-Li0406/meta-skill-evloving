---
name: git-workflow
description: Use when managing Git branches, creating commits, or preparing pull requests
---

# Git Workflow

Guidelines for branches, conventional commits, and pull requests.

## When to Use

- Creating feature branches
- Writing commit messages
- Preparing pull requests
- Managing Git history

## Golden Rules

1. **Always branch from updated main**
2. **One change per branch**
3. **Conventional commits for automation**
4. **Keep PRs small and focused**
5. **Explain WHY, not WHAT**

## Branching Strategy

### Branch Creation
```bash
git checkout main
git pull origin main          # CRITICAL - always pull first
git checkout -b type/description
```

### Branch Naming
```
<type>/<description>
feat/oauth-login
fix/memory-leak-parser
refactor/auth-module
docs/api-guide
```

### Common Mistakes
- ❌ Branching from outdated main
- ❌ Reusing branches for multiple changes
- ❌ Branching from feature branches
- ❌ Not syncing before starting work

## Conventional Commits

### Format
```
<type>[scope]: <description>

[body explaining WHY]

[footers: Fixes #123]
```

### Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| feat | New feature | MINOR |
| fix | Bug fix | PATCH |
| docs | Documentation | None |
| style | Formatting | None |
| refactor | Code restructuring | None |
| perf | Performance | PATCH |
| test | Tests | None |
| build | Build system | None |
| ci | CI/CD config | None |
| chore | Maintenance | None |

### Breaking Changes
Add `!` after type or `BREAKING-CHANGE:` footer → MAJOR bump

### Rules
- Imperative mood: "add" not "added"
- Lowercase after colon
- No period at end
- 50 char subject limit
- Body explains WHY

### Examples

**Feature**:
```
feat(auth): add OAuth2 login support

Implements OAuth2 flow with Google, GitHub, Microsoft.
Users can now authenticate without passwords.

Closes: #123
```

**Bug Fix**:
```
fix(parser): handle malformed JSON gracefully

Previously crashed on invalid JSON. Now returns
clear error and continues processing.

Fixes: #456
```

**Breaking Change**:
```
feat!: redesign authentication API

Redesigned auth flow for better security.

BREAKING-CHANGE: AuthProvider requires clientId parameter.
```

## Pull Requests

### PR Title
Follow conventional commit format:
```
feat(auth): add OAuth2 login support
```

### PR Template
```markdown
## Summary
Brief overview (1-2 sentences).

## Changes
- Added OAuth2 authentication flow
- Implemented token refresh mechanism
- Added login UI components

## Motivation
Why this change is needed.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing performed

## Related Issues
- Fixes #123
```

### Size Guidelines

| Size | Lines | Files | Verdict |
|------|-------|-------|---------|
| ✅ | <500 | <10 | Easy to review |
| ⚠️ | <1000 | <20 | Needs structure |
| ❌ | >1000 | >20 | Split it |

## Quality Gates

### Before Committing
- [ ] Tests passing
- [ ] Linting clean
- [ ] Conventional commit format
- [ ] Body explains WHY
- [ ] Issues referenced

### Before PR
- [ ] Branch from updated main
- [ ] All commits conventional
- [ ] PR title conventional
- [ ] Description complete
- [ ] Tests passing
- [ ] No debug code

## Scope Selection

### Finding Scopes
1. Check `.commitlintrc.json` for allowed scopes
2. Analyze recent commits: `git log --format="%s" -50`
3. Infer from file paths: `src/auth/*` → "auth"
4. Use module/component names

### Naming
- Use kebab-case: `auth-service`, `api-gateway`
- Avoid file-level granularity
- Keep scope count manageable (5-20)

## Common Operations

### Edit Last Commit
```bash
git commit --amend
```

### Squash Commits
```bash
git rebase -i HEAD~3
# Change 'pick' to 'squash'
```

### Sync with Main
```bash
# Rebase (cleaner history)
git checkout main && git pull
git checkout feat/branch
git rebase main
git push --force-with-lease

# Merge (preserves history)
git checkout feat/branch
git merge origin/main
git push
```

### Fix Merge Conflicts
```bash
git checkout main && git pull
git checkout your-branch
git rebase main
# Resolve conflicts
git rebase --continue
git push --force-with-lease
```

## Release Automation

Conventional commits enable:
- Automatic version bumps
- Changelog generation
- Release notes

| Type | Version |
|------|---------|
| feat | MINOR (1.2.0 → 1.3.0) |
| fix | PATCH (1.2.0 → 1.2.1) |
| BREAKING | MAJOR (1.2.0 → 2.0.0) |

Tools: release-please, semantic-release, changesets
