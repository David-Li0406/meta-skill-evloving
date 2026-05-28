---
name: biome-tooling
description: Use this skill when you need a fast, all-in-one toolchain for linting and formatting JavaScript/TypeScript code with Biome.
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

## Quick Start

### Initialize Biome

```bash
npx @biomejs/biome init
```

### Basic Usage

#### Format Files

```bash
# Format all files
npx @biomejs/biome format --write .

# Check formatting without modifying
npx @biomejs/biome format .
```

#### Lint Files

```bash
# Lint all files
npx @biomejs/biome lint .

# Lint and fix
npx @biomejs/biome lint --write .
```

#### All-in-One Check

```bash
# Format, lint, and organize imports
npx @biomejs/biome check --write .

# Check without modifying (for CI)
npx @biomejs/biome check .
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
  "organizeImports": {
    "enabled": true
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

## Best Practices

- Always run `biome check --write` before committing.
- Keep `biome.json` configuration synchronized across all services.
- Use the VS Code Biome extension and set it as the default formatter.
- Never push lint errors to main; rely on `npm run lint` in CI/CD pipelines.