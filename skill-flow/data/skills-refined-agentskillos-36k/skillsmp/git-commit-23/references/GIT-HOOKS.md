# Git Hooks

Guide for Git hooks using lefthook.

## Overview

This project uses **lefthook** to manage Git hooks for:
- Validating commit messages
- Running code quality checks before commits
- Ensuring code formatting
- Preventing broken code from being committed

## Hook Location

Git hooks are configured in `lefthook.yml` file at the project root:

```yaml
# lefthook.yml
pre-commit:
  commands:
    lint:
      glob: "*.{ts,tsx,js,jsx}"
      run: npx biome check --write {staged_files}
    
commit-msg:
  commands:
    validate:
      run: |
        PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert|merge)(\(.+\))?: .{1,}"
        if ! grep -qE "$PATTERN" {1}; then
          echo "❌ Invalid commit message format"
          exit 1
        fi

pre-push:
  commands:
    test:
      run: npm test
```

## Commit Message Hook (`commit-msg`)

### Purpose

Validates that commit messages follow Conventional Commits format.

### Location

Configured in `lefthook.yml` under `commit-msg` section

### Validation Pattern

```bash
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert|merge)(\(.+\))?: .{1,}"
```

### Accepted Commit Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, etc.) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `perf` | Performance improvements |
| `ci` | CI/CD changes |
| `build` | Build system changes |
| `revert` | Revert previous commit |
| `merge` | Merge branches |

### Hook Behavior

```bash
# When you commit:
git commit -m "invalid message"

# If invalid, hook shows:
❌ ERROR: Commit message doesn't follow Conventional Commits format

Expected format: type(scope): description

Valid types:
  feat:     New feature
  fix:      Bug fix
  docs:     Documentation changes
  ...

Your message: invalid message

# And exits with code 1 (commit blocked)
```

### Valid Commit Examples

```
feat: add user authentication
fix(api): resolve null pointer exception
docs: update README with setup instructions
refactor: simplify agent execution flow
test: add unit tests for UserService
```

## Pre-commit Hook (`pre-commit`)

### Purpose

Runs code quality checks before allowing commit.

### Checks Performed

1. **Biome Lint & Format**: Runs `biome check --write` on staged files
2. **File Type Filter**: Only checks `.ts` files in `src/` directories
3. **Auto-fix**: Automatically applies Biome fixes
4. **Restage Files**: Re-stages files modified by Biome

### Supported Projects

The hook runs Biome on configured file patterns (typically `.ts`, `.tsx`, `.js`, `.jsx` files)

### Hook Behavior

```bash
# When you commit:
git add src/services/user.service.ts
git commit -m "feat: add user service"

# Hook runs:
🔍 Running Biome check on WebApi...

# If errors found, Biome auto-fixes and re-stages:
✅ Formatted 1 file

# Then commit continues
[main abc1234] feat: add user service
```

### If Biome Fails

```bash
# If Biome finds unfixable errors:
❌ Lint errors found

Fix errors and commit again.

# Commit is blocked
```

## Pre-push Hook (`pre-push`)

### Purpose

Runs tests before pushing to remote repository.

### Checks Performed

1. **Run Tests**: Executes test suite
2. **Build Verification**: Ensures project builds successfully
3. **Coverage Check**: Verifies test coverage meets requirements

### Hook Behavior

```bash
# When you push:
git push origin feature/new-feature

# Hook runs:
🧪 Running tests...

# If tests fail:
❌ Tests failed
Fix failing tests before pushing.

# Push is blocked
```

## Installing Hooks

### Initial Setup (Automatic)

```bash
# Hooks are installed via npm
npm install

# lefthook installs hooks automatically
```
Install lefthook
npm install lefthook --save-dev

# Or with Go
go install github.com/evilmartians/lefthook@latest

# Install hooks
npx lefthook install
```

### Manual Installation

```bash
# If hooks aren't installed:
lefthook install

# Verify hooks configuration:
cat lefthook.ymlxisting Hook

```bash
Edit the `lefthook.yml` file:

```yaml
pre-commit:
  commands:
    custom-check:
      run: ./scripts/custom-check.sh
```

### Add New Hook

```yaml
# Add to lefthook.yml
pre-push:
  commands:
    security-scan:
      run: npm audit

## Common Hook Tasks

### Running Linting

```bash
#!/bin/bash
# Run Biome on staged files
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.ts$')

if [ -n "$FILES" ]; then
  npx biome check --write $FILES
  git add $FILES
fi
```yaml
# In lefthook.yml
pre-commit:
  commands:
    lint:
      glob: "*.{ts,tsx}"
      run: npx biome check --write {staged_files}
if [ $? -ne 0 ]; then
  eyaml
# In lefthook.yml
pre-commit:
  commands:
    test:
      run: npm test
      fail_text: "❌ Tests failed. Commit blocked."/bin/bash
# Enforce branch naming convention
BRANCH_NAME=$(git symbolic-ref --short HEAD)
PATTERN="^(feature|bugfix|hotfix)\/.+$"

if ! [[ $BRANCH_NAME =~ $PATTERN ]]; then
  echo "❌ Invalid branch name: $BRANCH_NAME"
  eyaml
# In lefthook.yml
pre-commit:
  commands:
    branch-name:
      run: |
        BRANCH=$(git symbolic-ref --short HEAD)
        if ! [[ $BRANCH =~ ^(feature|bugfix|hotfix)/ ]]; then
          echo "❌ Invalid branch name: $BRANCH"
          exit 1
        # Skip commit-msg validation
git commit --no-verify -m "your message"

# Skip pre-commit checks
git commit --no-verify

# Skip pre-push checks
git push --no-verify
```

⚠️ **Warning**: Use `--no-verify` only in emergencies. It bypasses all quality checks.

## Troubleshooting

### Hooks Not Running

```bash
# Check if lefthook is installed
git config core.hooksPath

# Should show: .lefthook

# If not, reinstall:
npx lefthook install
```

### Hook Not Executable

```bash
# On Linux/lefthook is installed
lefthook version

# Reinstall hooks
lefthook install

# Run hooks manually to test
lefthook run pre-commit
### Biome Errors in Pre-commit

```bash
# Run Biome manually to see details
npx biome check --write ./src

# Check Biome configuration
cat biome.json
```

## Finding Hooks

```bash
# View lefthook configuration
cat lefthook.yml

# List all configured hooks
lefthook dump

# Check lefthook version
lefthook version

# Run specific hook manually
lefthook run pre-commit
```

## Related Skills

- **`biome`** - Biome configuration and commands
- **`git-commit`** - Commit message format and branching
- **`testing`** - Test execution in hooks
