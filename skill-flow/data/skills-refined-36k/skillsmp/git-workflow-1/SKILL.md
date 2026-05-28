---
name: git-workflow
description: Git workflow standards. Apply when committing changes, creating pull requests, or managing branches.
---

# Git Workflow Standards

## Commit Message Format

Follow Conventional Commits strictly:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change without fixing bug or adding feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

**Examples**:
```
feat(auth): add OAuth2 login flow

Implements authorization code flow with PKCE.
Supports Google and GitHub providers.

Closes #123
```

```
fix(payment): handle Stripe webhook retries

Previous implementation didn't handle duplicate
webhook events, causing duplicate charge attempts.

Fixes #456
```

## Commit Rules

1. **Subject line max 50 chars**
2. **Imperative mood**: "Add feature" not "Added feature" or "Adds feature"
3. **No period at end of subject**
4. **Body explains WHY**, not WHAT (code shows what)
5. **Reference issues**: Use `Closes #123` or `Refs #456`

## Branch Strategy

```
main (protected)
  ├─ feature/<feature-name>
  ├─ fix/<bug-description>
  ├─ hotfix/<urgent-fix>
  └─ refactor/<description>
```

**Rules**:
- **main**: Only via merge PR, direct push forbidden
- **feature branches**: Delete after merge
- **branch naming**: Lowercase, kebab-case, descriptive
- **branch lifespan**: Max 2 weeks, else split or abandon

## Pull Request Standards

### PR Title
Follow commit format, include PR number:
```
feat(auth): add OAuth2 login flow (#42)
```

### PR Description Template

```markdown
## Summary
[Bullet points, 2-3 lines max]

## Changes
- File A: What changed
- File B: What changed

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done

## Breaking Changes
[List any breaking changes or "None"]

## Screenshots (if applicable)
```

### PR Review Rules

1. **At least 1 reviewer approval** before merge
2. **All checks must pass** (CI/CD, tests, linting)
3. **Address all review comments** before requesting re-review
4. **Squash commits** when merging to main

## Git Best Practices

- **Amend only**: If commit not pushed, use `--amend` to fix typos
- **Never force push to main**
- **Use .gitignore religiously**: Never commit:
  - `.env`, `.env.local`
  - `node_modules/`, `dist/`, `build/`
  - IDE files (`.vscode/`, `.idea/`)
  - OS files (`.DS_Store`, `Thumbs.db`)
- **Rebase before PR**: Keep branch up-to-date with main
- **Atomic commits**: Each commit should be a logical unit, can be reverted independently
