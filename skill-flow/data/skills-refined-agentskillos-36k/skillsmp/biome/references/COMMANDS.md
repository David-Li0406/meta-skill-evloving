# Biome Commands

Reference for Biome CLI commands in projects.

## Overview

Biome provides fast command-line tools for linting, formatting, and checking code. Commands are typically run in each project directory.

## Basic Commands

### Check All Files

```bash
# Run linter and formatter check
npx biome check ./src

# Check specific file
npx biome check ./src/services/user.service.ts

# Check with verbose output
npx biome check ./src --verbose
```

### Apply Fixes

```bash
# Lint and format (safe auto-fix)
npx biome check --write ./src

# Format only
npx biome format --write ./src

# Lint only
npx biome lint --write ./src
```

### Lint Commands

```bash
# Run linter
npx biome lint ./src

# Lint with auto-fix
npx biome lint --write ./src

# Lint specific file
npx biome lint ./src/services/user.service.ts

# Lint with error-level only
npx biome lint ./src --diagnostic-level=error
```

### Format Commands

```bash
# Format files
npx biome format ./src

# Format with write
npx biome format --write ./src

# Check formatting without changes
npx biome format --check ./src

# Format specific file
npx biome format --write ./src/services/user.service.ts
```

## NPM Scripts

Common NPM scripts found in projects:

```json
{
  "scripts": {
    "lint": "biome lint ./src",
    "lint:fix": "biome lint --write ./src",
    "format": "biome format --write ./src",
    "format:check": "biome format --check ./src"
  }
}
```

### Usage

```bash
# Run lint (check only)
npm run lint

# Run lint with fixes
npm run lint:fix

# Format all files
npm run format

# Check formatting
npm run format:check
```

## Advanced Commands

### Output Formats

```bash
# JSON output (for CI/CD)
npx biome check ./src --reporter=json

# GitHub Actions output
npx biome check ./src --reporter=github

# JUnit output
npx biome check ./src --reporter=junit
```

### File Filtering

```bash
# Include specific file patterns
npx biome check ./src --files-max-size=1048576

# Ignore specific files
npx biome check ./src --ignore=v1/deprecated.ts

# Include only TS files
npx biome check ./src/**/*.ts
```

### Severity Levels

```bash
# Show only errors
npx biome check ./src --diagnostic-level=error

# Show errors and warnings
npx biome check ./src --diagnostic-level=warn

# Show all diagnostics (including info)
npx biome check ./src --diagnostic-level=info
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Check code with Biome
  run: npx biome check ./src

- name: Format code with Biome
  run: npx biome format --write ./src
  if: failure()
```

### Pre-commit Hook Example

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Lint and format staged files
npx biome lint --write ./src

# Add formatted files back to staging
git add -u
```

## Configuration Options

### Using Custom Config

```bash
# Use specific biome.json file
npx biome check ./src --config=path/to/biome.json

# Use custom config file
npx biome check ./src --config=biome.prod.json
```

### Working Directory

```bash
# Run from project root
cd GGA Team.this project.WebApi
npx biome check ./src

# Run with explicit working directory
npx biome check ./src --working-directory=GGA Team.this project.WebApi
```

## Common Workflows

### 1. Development Workflow

```bash
# 1. Write code

# 2. Format and lint
npm run lint:fix

# 3. Review changes
git diff

# 4. Commit
git commit -m "feat: add new feature"
```

### 2. Pre-commit Workflow

```bash
# Before committing
npm run lint

# If errors found, fix them
npm run lint:fix

# Stage and commit
git add .
git commit -m "fix: resolve lint issues"
```

### 3. CI/CD Pipeline

```bash
# In CI: Check only, don't fix
npx biome check ./src

# In local: Fix issues
npx biome check --write ./src
```

### 4. Migration from ESLint

```bash
# Check Biome vs ESLint differences
npx biome check ./src
npx eslint ./src

# Convert ESLint config (if needed)
npx @biomejs/biome migrate eslint

# Verify migration
npm run lint
```

## Performance Tips

### Parallel Execution

```bash
# Run in parallel for faster results
npx biome check ./src --threads=4

# Auto-detect threads
npx biome check ./src --threads=true
```

### File Size Limits

```bash
# Skip large files
npx biome check ./src --files-max-size=5242880  # 5MB limit

# Show max file size warning
npx biome check ./src --files-ignore-unknown=false
```

## Troubleshooting

### Biome Not Found

```bash
# Install locally
npm install --save-dev @biomejs/biome

# Or run directly with npx
npx @biomejs/biome check ./src
```

### Configuration Not Loading

```bash
# Verify biome.json exists
cat biome.json

# Check JSON syntax
npx biome check ./src --verbose

# Use explicit config
npx biome check ./src --config=biome.json
```

### Format Conflicts

```bash
# Check what would change
npx biome format --check ./src

# Preview changes (dry run)
npx biome format --write-dry-run ./src

# Force format
npx biome format --write ./src --unsafe
```

## Finding Commands

```bash
# Show all available commands
npx biome --help

# Show command help
npx biome check --help
npx biome lint --help
npx biome format --help

# Check package.json scripts
grep '"lint"' package.json
grep '"format"' package.json

# Find Biome usage in project
grep -r "biome" package.json
```

## Related Skills

- **`biome`** - Biome lint rules and format configuration
- **`webapi`** - Backend code linting
- **`testing`** - Test file linting
- **`git-commit`** - Pre-commit hooks with Biome
