---
name: git-commit
description: Git commit standards, conventions, and commit message formatting
license: MIT
metadata:
  author: GGA Team
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "commit"
    - "git"
    - "versioning"
    - "changelog"
    - "release"
allowed-tools: []
---

## When to Use It

- When creating commits in the repository
- When preparing a new version or release (SemVer)
- When updating the project `CHANGELOG.md`

## Critical Patterns

- **ALWAYS** follow the **Conventional Commits** format: `type(scope): subject`
- **NEVER** write subjects in past tense ("fixed", "added"); use imperative mood ("fix", "add")
- **ALWAYS** keep the title at **50 characters** or fewer
- **ALWAYS** add a `BREAKING CHANGE:` footer for backward-incompatible changes
- **NEVER** bundle multiple logical changes into one commit; keep them atomic and focused
- **ALWAYS** reference GitHub issues in the body via `Fixes #123`

## Convenciones de Commit (Commit Conventions)

### Conventional Commits

This project uses **Conventional Commits** for structured commit messages:

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semi colons, etc.)
- `refactor`: Code refactoring without adding features or fixing bugs
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, build process, dependency updates
- `ci`: CI/CD configuration changes

**Scopes** (common examples):
- `api`: API changes
- `backend`: Backend changes
- `frontend`: Frontend changes
- `domain`: Domain layer changes
- `infrastructure`: Infrastructure changes
- `migration`: Database migrations
- `docs`: Documentation changes
- `tests`: Test changes

## Commit Message Examples

### Feature Commit

```bash
feat(agents): add agent versioning support

- Implement agent version tracking
- Add version comparison endpoint
- Add version restoration functionality

Co-authored-by: John Doe <john@example.com>
```

### Bug Fix Commit

```bash
fix(webapi): resolve NaN flowId in metrics

- Validate flowId before processing
- Add error logging for invalid IDs
- Fix metrics aggregation

Fixes #123
```

### Refactor Commit

```bash
refactor(agents): simplify agent creation flow

- Remove duplicate validation logic
- Consolidate versioning service
- Improve error handling

BREAKING CHANGE: Agent creation API now requires version parameter
```

### Documentation Commit

```bash
docs: update agent skill documentation

- Add integration patterns section
- Update examples
- Fix typos in README
```

## Commit Standards

### Title Guidelines

- Use imperative mood: "add" not "added" or "adds"
- Don't end with period
- Limit to 50 characters (including type/scope)

### Body Guidelines

- Wrap at 72 characters
- Use imperative mood
- Explain **what** and **why** (not **how**)
- Reference issues with `Fixes #123`

### Footer Guidelines

- **Breaking changes**: Start with `BREAKING CHANGE:`
- **References**: `Fixes #123`, `Closes #456`
- **Co-authors**: For multiple authors

## Git Hooks

### Pre-commit Hook

Configured in `lefthook.yml`:

```yaml
pre-commit:
  commands:
    lint:
      run: npm run lint:fix
    typecheck:
      run: npm run typecheck
    test:
      run: npm run test:unit
```

### Commit Message Hook

Configured in `lefthook.yml`:

```yaml
commit-msg:
  commands:
    validate:
      run: |
        PATTERN="^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?: "
        if ! grep -qE "$PATTERN" {1}; then
          echo "Commit message must follow conventional format"
          exit 1
        fi
        
        # Check subject length
        subject=$(head -n1 {1} | cut -d':' -f2 | sed 's/^\s*//')
        if [ ${#subject} -gt 50 ]; then
          echo "Commit subject must be 50 characters or less"
          exit 1
        fi
```

## Versioning

### Semantic Versioning

This project uses **Semantic Versioning** (SemVer):

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Example**: `1.5.0` → `2.0.0` (breaking)
**Example**: `1.5.0` → `1.6.0` (new feature)
**Example**: `1.5.0` → `1.5.1` (bug fix)

### Version Bumping

When to increment:

| Change | Type | Example |
|--------|------|---------|
| Breaking change | MAJOR | `1.5.0` → `2.0.0` |
| New feature (backward compatible) | MINOR | `1.5.0` → `1.6.0` |
| Bug fix (backward compatible) | PATCH | `1.5.0` → `1.5.1` |

### Release Branches

**Naming**: `release/vX.Y.Z`

```bash
# Create release branch
git checkout -b release/v1.6.0

# Make release commits
git commit -m "chore(release): prepare for v1.6.0 release"

# Merge to main
git checkout main
git merge release/v1.6.0

# Tag release
git tag -a v1.6.0 -m "Release v1.6.0"
```

## Changelog

### Changelog Format

Based on conventional commits, maintain `CHANGELOG.md`:

```markdown
# Changelog

## [2.0.0] - 2024-01-15

### Added
- Agent versioning support
- Agent comparison endpoint
- Version restoration functionality

### Changed
- Improved agent creation flow
- Simplified validation logic

### Deprecated
- Legacy agent API (use agents/v2)

### Removed
- Old agent caching mechanism

### Fixed
- NaN flowId in metrics
- Agent dirty state tracking

### Security
- Added input validation for agent names
- Updated JWT token handling
```

## Finding Related Code

### Search Git Configuration

```bash
# Find lefthook configuration
find . -name "lefthook.yml"
cat lefthook.yml

# Find commitlint configuration
find . -name "commitlint*"
grep -r "commitlint" package.json

# Find version configuration
grep -r "version" package.json
```

### Search Commit Patterns

```bash
# Find recent commits
git log --oneline -20

# Find commit messages by type
git log --grep="^feat:" --oneline
git log --grep="^fix:" --oneline

# Find breaking changes
git log --grep="BREAKING CHANGE:" --oneline
```

## Common Patterns

### Feature Addition

```bash
# Make changes
git add .

# Commit with proper format
git commit -m "feat(agents): add agent tools configuration

- Add tool input/output mapping
- Support integration and piece tool types
- Add custom description support"

# Push to remote
git push origin feature/agent-tools

# Create PR from feature/agent-tools to main
```

### Bug Fix

```bash
# Make changes
git add .

# Commit with reference
git commit -m "fix(webapi): handle missing agent ID

- Add null check for agentId parameter
- Return 400 Bad Request instead of 500 error
- Add error logging

Fixes #456"

# Push
git push origin fix/missing-agent-id
```

### Breaking Change

```bash
# Update code to breaking API
git add .

# Commit with BREAKING CHANGE footer
git commit -m "feat(agents): restructure agent configuration model

BREAKING CHANGE: Agent configuration now uses new model
- Old agent format no longer supported
- Migration required for existing agents
- See migration guide in docs/migration.md

Migrates #123"
```

### Release Preparation

```bash
# Update version in package.json
npm version minor --no-git-tag-version

# Update CHANGELOG.md
git add CHANGELOG.md
git commit -m "chore(release): update CHANGELOG for v1.6.0"

# Create release branch
git checkout -b release/v1.6.0

# Update any additional files
vim version.ts
git commit -am "chore(release): bump version to 1.6.0"

# Merge and tag
git checkout main
git merge release/v1.6.0
git tag -a v1.6.0 -m "Release v1.6.0"

# Push tags and main
git push origin main --tags
```

## Troubleshooting

### Commit Hook Failed

**Error**: Commit message doesn't follow format

**Solution**:
1. Use conventional format: `type(scope): subject`
2. Keep subject under 50 characters
3. Use valid types: feat, fix, docs, style, refactor, perf, test, chore, ci
4. Don't end subject with period

### Pre-commit Hook Failed

**Error**: Linting or tests failed

**Solution**:
1. Run `npm run lint:fix` to auto-fix issues
2. Run `npm run typecheck` to check types
3. Run `npm run test` to verify tests pass
4. Fix remaining issues manually
5. Commit again

### Merge Conflicts

**Error**: Git merge conflict

**Solution**:
```bash
# Start merge
git merge feature/branch

# Resolve conflicts in conflicted files
# Edit and save files

# Mark as resolved
git add <resolved-files>

# Complete merge
git commit -m "chore: resolve merge conflicts with feature/branch"
```

## Best Practices

### Small, Focused Commits

- One logical change per commit
- Keep changes atomic and testable
- Avoid bundling unrelated changes

### Descriptive Messages

- Explain **what** changed and **why**
- Include context for future maintainers
- Reference related issues or PRs

### Consistent Formatting

- Use same format across all commits
- Follow conventional commits specification
- Use proper line wrapping (72 characters)

### Test Before Commit

- Run unit tests: `npm run test:unit`
- Run integration tests: `npm run test:integration`
- Run linting: `npm run lint`
- Run type checking: `npm run typecheck`

### Atomic Changes

- Each commit should pass all tests
- Never commit broken code
- Use branches for work-in-progress

## Referencias (References)
- [BRANCHING.md](references/BRANCHING.md)
- [COMMIT-MESSAGE-FORMAT.md](references/COMMIT-MESSAGE-FORMAT.md)
- [GIT-HOOKS.md](references/GIT-HOOKS.md)

## Assets
- `assets/scripts/commit.sh` - Commit automation script
- `assets/scripts/release.sh` - Release automation script
