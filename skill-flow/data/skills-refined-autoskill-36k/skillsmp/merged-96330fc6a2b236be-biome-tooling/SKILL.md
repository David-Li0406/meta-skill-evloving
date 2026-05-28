---
name: biome-tooling
description: Use this skill for fast, unified code formatting and linting in JavaScript/TypeScript projects using Biome, a modern alternative to ESLint and Prettier.
---

# Biome Tooling

This skill covers using Biome, a fast all-in-one toolchain for formatting and linting JavaScript/TypeScript code.

## What is Biome?

Biome is a performant toolchain that provides:
- **Formatting** (replaces Prettier)
- **Linting** (replaces ESLint)
- **Fast** (written in Rust, significantly faster than traditional tools)
- **Zero config** (sensible defaults)
- **Single tool** (no conflicts between tools)

## Installation

```bash
npm install --save-dev @biomejs/biome
```

## Configuration

Create `biome.json` in your project root:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["node_modules", "dist", "build", ".next"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded",
      "trailingCommas": "all"
    }
  }
}
```

## Package.json Scripts

Add the following scripts to your `package.json`:

```json
{
  "scripts": {
    "check": "biome check .",
    "check:write": "biome check --write .",
    "format": "biome format --write .",
    "lint": "biome lint .",
    "lint:fix": "biome lint --write ."
  }
}
```

## Basic Usage

### Check and Fix Issues

```bash
# Check all files and auto-fix
npx @biomejs/biome check --write .
```

### Format Files

```bash
# Format all files
npx @biomejs/biome format --write .
```

### Lint Files

```bash
# Lint all files
npx @biomejs/biome lint .
```

## Import Organization

Biome includes built-in import sorting:

```json
{
  "organizeImports": {
    "enabled": true
  }
}
```

## VS Code Integration

### Install Biome Extension

Install the "Biome" extension from the VSCode marketplace.

### VS Code Settings

```json
{
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  }
}
```

## Migration from ESLint and Prettier

### Remove Old Tools

```bash
npm uninstall eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### Migrate Configuration

Use Biome's migration tool:

```bash
npx @biomejs/biome migrate eslint
```

## CI/CD Integration

### GitHub Actions

```yaml
name: CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: npm ci
      - run: npm run check
```

## Best Practices

1. **Use `biome check`** instead of separate format/lint commands.
2. **Enable `--write`** flag for automatic fixes.
3. **Configure VS Code** for format-on-save.
4. **Add git hooks** to enforce quality before commits.

## Troubleshooting

### Biome Not Found

If you encounter a "command not found" error, ensure Biome is installed locally:

```bash
npm install --save-dev @biomejs/biome
```

### Linting Errors

Run `npm run lint:fix` to auto-fix any linting issues.

## Further Reading

- Biome Docs: [https://biomejs.dev/](https://biomejs.dev/)
- Biome GitHub: [https://github.com/biomejs/biome](https://github.com/biomejs/biome)