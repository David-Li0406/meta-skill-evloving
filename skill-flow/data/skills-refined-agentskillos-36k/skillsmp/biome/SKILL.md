---
name: biome
description: Linting, formatting, and code quality using Biome
license: MIT
metadata:
  author: GGA Team
  version: "1.0"
  scope: [root, webapi, web-executor]
  auto_invoke:
    - "lint"
    - "format"
    - "biome"
    - "code quality"
    - "eslint"
    - "prettier"
allowed-tools: []
---

## When to Use It

- When running linting or formatting tasks in the project
- When migrating ESLint/Prettier configs to Biome
- When configuring Git hooks (lefthook) for code quality validation

## Critical Patterns

- **ALWAYS** run `biome check --write` before committing
- **NEVER** disable `correctness` or `suspicious` rules without a clear justification in comments
- **ALWAYS** use the VS Code Biome extension and set it as the default formatter
- **ALWAYS** keep `biome.json` configuration synchronized across all services
- **NEVER** push lint errors to main; rely on `npm run lint` in CI/CD pipelines

## Common Commands

```bash
# Check and auto-fix
npx @biomejs/biome check --write .

# Format files
npx @biomejs/biome format --write .

# Organize imports
npx @biomejs/biome organize-imports .
```

## Biome Configuration

### ESLint to Biome Migration

**Note**: If your project currently uses ESLint, to migrate to Biome:

1. Install Biome:
```bash
npm install --save-dev @biomejs/biome
```

2. Remove ESLint:
```bash
npm uninstall eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

3. Create Biome config:

**biome.json**:
```json
{
  "$schema": "https://biomejs.dev/schemas/1.7.0/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": [
      "node_modules",
      "dist",
      "coverage",
      "build"
    ]
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": "warn",
      "correctness": "warn",
      "complexity": "warn",
      "performance": "warn",
      "style": "warn",
      "suspicious": "warn"
    }
  },
  "organizeImports": {
    "enabled": true
  },
  "javascript": {
    "globals": []
  },
  "overrides": [
    {
      "include": ["*.ts"],
      "linter": {
        "rules": {
          "style": {
            "noDefaultExport": "off"
          }
        }
      }
    }
  ]
}
```

### Project Structure

**ESLint Locations** (current):
3. Remove ESLint config files from your project directories

## Biome Commands

### Check Configuration

```bash
# Validate Biome configuration
npx @biomejs/biome check --verbose

# Show configuration
npx @biomejs/biome migrate eslint
```

### Lint Code

```bash
# Check all files
npx @biomejs/biome check

# Check specific file
npx @biomejs/biome check src/app.component.ts

# Check specific directory
npx @biomejs/biome check src/

# Watch mode
npx @biomejs/biome check --watch

# Apply fixes
npx @biomejs/biome check --write
```

### Format Code

```bash
# Format all files
npx @biomejs/biome format

# Format specific file
npx @biomejs/biome format src/app.component.ts

# Format specific directory
npx @biomejs/biome format src/

# Check formatting without writing
npx @biomejs/biome format --write=false
```

### Organize Imports

```bash
# Organize imports in all files
npx @biomejs/biome check --apply-unsafe

# Or run separately
npx @biomejs/biome organize-imports
```

## ESLint Configuration (Current)

### ESLint Config Pattern

```javascript
module.exports = {
  parser: '@typescript-eslint/parser',
  extends: [
    'plugin:@typescript-eslint/recommended',
    'airbnb-base',
    'prettier'
  ],
  plugins: [
    '@typescript-eslint',
    'prettier'
  ],
  rules: {
    // Custom rules
    '@typescript-eslint/no-unused-vars': 'warn',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    'prettier/prettier': 'error'
  },
  settings: {
    'import/resolver': {
      'typescript': {}
    }
  }
};
```

### ESLint Rules Used

Based on common ESLint configurations:

| Rule | Severity | Description |
|------|----------|-------------|
| `@typescript-eslint/no-unused-vars` | warn | Warn about unused variables |
| `@typescript-eslint/explicit-module-boundary-types` | off | Disable boundary type requirement |
| `prettier/prettier` | error | Enforce Prettier formatting |

## Package.json Scripts

### Biome Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "format:check": "biome check . --write=false",
    "lint:watch": "biome check --watch",
    "organize": "biome organize-imports"
  }
}
```

### ESLint Scripts (Current)

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,scss}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,scss}\""
  }
}
```

## Finding Related Code

### Search Linting Configs

```bash
# Find ESLint configs
find . -name ".eslintrc.*"

# Find Prettier configs
find . -name ".prettierrc.*"

# Find Biome configs (if migrated)
find . -name "biome.json"
```

### Search Linting Scripts

```bash
# Find lint scripts
grep -r "\"lint\"" package.json

# Find format scripts
grep -r "\"format\"" package.json
```

## Common Patterns

### Fix Linting Errors

```bash
# Auto-fix all fixable errors
npm run lint:fix

# Fix specific file
npx @biomejs/biome check --write src/file.ts

# Check remaining errors
npm run lint
```

### Format Before Commit

```bash
# Format all changes
npm run format

# Organize imports
npm run organize

# Check for remaining errors
npm run lint:fix
```

### CI/CD Integration

**GitHub Actions** (`.github/workflows/lint.yml`):

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run Biome
        run: npm run lint
```

## Migration Guide

### Step 1: Install Biome

```bash
npm install --save-dev @biomejs/biome
```

### Step 2: Migrate ESLint Config

```bash
# Generate Biome config from ESLint
npx @biomejs/biome migrate eslint

# Review generated biome.json
```

### Step 3: Remove ESLint

```bash
npm uninstall eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin prettier eslint-config-prettier eslint-config-airbnb-base eslint-plugin-import eslint-plugin-prettier
```

### Step 4: Update Scripts

```bash
# Update package.json scripts
# See "Biome Scripts" section above
```

### Step 5: Update Git Hooks

Update `.lefthook/pre-commit`:

```bash
#!/bin/sh
. "$(dirname "$0")/_/lefthook.sh"

# Run Biome check and format
npx --no -- biome check --write
```

## Troubleshooting

### Biome Not Found

**Error**: `command not found: biome`

**Solution**:
```bash
# Install Biome locally
npm install --save-dev @biomejs/biome

# Or use npx
npx @biomejs/biome check
```

### Linting Errors

**Common Errors**:
- Unused variables
- Missing imports
- Type errors
- Formatting issues

**Solutions**:
1. Run `npm run lint:fix` to auto-fix
2. Review remaining errors manually
3. Check TypeScript configuration
4. Run TypeScript compiler: `npx tsc --noEmit`

### Format Conflicts

**Issue**: Biome and Prettier both formatting

**Solution**:
- Remove Prettier
- Use Biome formatter exclusively
- Update VS Code settings to use Biome

## Best Practices

### Always Lint Before Commit

```bash
# Pre-commit hook
git add -A
npm run lint:fix
git add -A
```

### Use Consistent Configuration

- Share Biome config across all projects
- Use `.gitignore` exclusions
- Follow project conventions for formatting

### Keep Dependencies Updated

```bash
# Update Biome regularly
npm update @biomejs/biome

# Check for new rules
npx @biomejs/biome migrate --help
```

### Configure IDE Integration

**VS Code Settings** (`.vscode/settings.json`):

```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.biomejs.biome": "explicit"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

## References

- [biome.json](biome.json) - Biome configuration file.
- [ESLINTRC.md](references/ESLINTRC.md) - ESLint patterns (current setup).
- [package.json](package.json) - Linting and formatting scripts.

## Assets

- `assets/scripts/lint.sh` - Linting automation script.
- `assets/scripts/format.sh` - Formatting automation script.
