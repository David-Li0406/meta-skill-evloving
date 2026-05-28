---
name: commit-helper
description: Guide conventional commit creation with mandatory pre-commit checks for the Shortcuts project. Use when: (1) Creating commits, (2) Running pre-commit checks, (3) Following conventional commit format, (4) Ensuring tests pass before commit, (5) Co-authoring with AI (Claude Code).
---

# Commit Helper

Guide for creating conventional commits with mandatory pre-commit checks.

## Pre-Commit Checklist

**Before every commit, you MUST:**

1. **Run unit tests**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```
   - All tests must pass
   - If any fail, fix them before committing

2. **Run integration tests** (if you modified integration points)
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Integration
   ```

3. **Verify linting** (runs automatically with tests)
   - PSScriptAnalyzer checks run with test suite
   - Fix any Error/Warning severity issues

**Never commit if:**
- Any unit test fails
- Any integration test fails
- You changed a function but didn't update its tests
- You're unsure if tests cover your changes

## Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Must be one of:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no feature change or bug fix)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, build, etc.)
- **ci**: CI/CD changes

### Scope (Optional)

Component affected:
- `pslib` - PowerShell library
- `wsl` - WSL-related changes
- `install` - Installation scripts
- `test` - Test infrastructure
- etc.

### Subject

- Imperative mood ("add feature" not "added feature")
- Lowercase
- No period at the end
- Max 50 characters

### Body (Optional)

- Explain what and why (not how)
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (Optional)

- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Closes #123`
- Co-authored commits: `Co-Authored-By: Name <email>`

## Examples

### Simple Feature

```
feat: add distribution validation function

Add Test-ValidDistroName to validate WSL distribution names.
Returns false for null or empty names.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Bug Fix

```
fix: handle WSL distribution names with spaces

Properly quote distribution name in wsl command to support
distributions like "Ubuntu 22.04 LTS".

Closes #42
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Refactoring

```
refactor: consolidate error handling in utils

Extract common error handling pattern into helper function.
No behavior change.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Multiple Changes

```
feat(pslib): add Silent parameter to Invoke-CommandLine

- Suppresses console output when -Silent is used
- Useful for background operations
- Tests updated to verify behavior

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Co-Authoring with AI

When AI assists with the code, add co-author:

```
feat: add new feature

Description of feature.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

For GitHub Copilot:
```
Co-Authored-By: GitHub Copilot <noreply@github.com>
```

## Pre-Commit Workflow

### 1. Stage Changes

```bash
git add file1.ps1 file1.Tests.ps1
```

**Important:** Stage tests and implementation together!

### 2. Run Pre-Commit Checks

```bash
# Unit tests
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# Integration tests (if needed)
pwsh -File ".\test\bin\testrunner.ps1" -Integration
```

### 3. Create Commit

Using heredoc for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
feat: add new feature

Detailed description of the feature.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

Or interactive:

```bash
git commit
# Opens editor for commit message
```

### 4. Verify Commit

```bash
git log -1 --pretty=format:"%h %s"
git show HEAD --stat
```

## Common Patterns

### Feature Addition

```bash
# 1. Write tests
# 2. Implement feature
# 3. Run tests
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# 4. Stage changes
git add tools/pslib/utils.ps1 tools/pslib/utils.Tests.ps1

# 5. Commit
git commit -m "$(cat <<'EOF'
feat(pslib): add input validation helper

Add Test-ValidInput function for common input validation patterns.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Bug Fix

```bash
# 1. Write test reproducing bug
# 2. Fix bug
# 3. Run tests
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# 4. Stage and commit
git add file.ps1 file.Tests.ps1
git commit -m "$(cat <<'EOF'
fix: handle null input in validation

Add null check before string operations to prevent NullReferenceException.

Closes #123
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Documentation Update

```bash
git add README.md
git commit -m "docs: update installation instructions"
```

### Test Updates

```bash
git add file.Tests.ps1
git commit -m "test: add coverage for edge cases"
```

## Commit Message Templates

See [commit-templates.md](references/commit-templates.md) for more examples.

## Best Practices

1. **Test before commit** - Always run tests
2. **Atomic commits** - One logical change per commit
3. **Descriptive subjects** - Clear, concise description
4. **Include context** - Explain why in body
5. **Reference issues** - Use `Closes #123` for fixes
6. **Co-author AI contributions** - Credit AI assistance
7. **Stage related files together** - Tests + implementation
8. **Keep subject short** - Max 50 characters
9. **Use imperative mood** - "add" not "added"
10. **Proofread** - Check for typos

## Troubleshooting

### Tests Failing Before Commit

```bash
# Run tests to see failures
pwsh -File ".\test\bin\testrunner.ps1" -Unit -Verbosity Detailed

# Fix failing tests
# Run tests again
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# Commit once all tests pass
```

### Forgot to Stage Tests

```bash
# Check what's staged
git status

# Stage missing test files
git add *.Tests.ps1

# Amend previous commit (if not pushed)
git commit --amend
```

### Forgot Co-Author

```bash
# Amend commit (if not pushed)
git commit --amend

# Add co-author line in editor
```

### Need to Run Integration Tests

```bash
# Run integration tests
pwsh -File ".\test\bin\testrunner.ps1" -Integration

# If they pass, commit
git commit -m "message"
```
