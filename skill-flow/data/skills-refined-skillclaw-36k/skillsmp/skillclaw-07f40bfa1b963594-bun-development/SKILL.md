---
name: bun-development
description: Use this skill when you want to develop modern JavaScript/TypeScript applications with the Bun runtime, optimize development speed, or migrate from Node.js to Bun.
---

# Skill Body

## ⚡ Bun Development

Fast, modern JavaScript/TypeScript development with the Bun runtime, inspired by [oven-sh/bun](https://github.com/oven-sh/bun).

## When to Use This Skill

Use this skill when:

- Starting new JS/TS projects with Bun
- Migrating from Node.js to Bun
- Optimizing development speed
- Using Bun's built-in tools (bundler, test runner)
- Troubleshooting Bun-specific issues

---

## 1. Getting Started

### 1.1 Installation

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"

# Homebrew
brew tap oven-sh/bun
brew install bun

# npm (if needed)
npm install -g bun

# Upgrade
bun upgrade
```

### 1.2 Why Bun?

| Feature         | Bun            | Node.js                     |
| :-------------- | :------------- | :-------------------------- |
| Startup time    | ~25ms          | ~100ms+                     |
| Package install | 10-100x faster | Baseline                    |
| TypeScript      | Native         | Requires transpiler         |
| JSX             | Native         | Requires transpiler         |
| Test runner     | Built-in       | External (Jest, Vitest)     |
| Bundler         | Built-in       | External (Webpack, esbuild) |

---

## 2. Project Setup

### 2.1 Create New Project

```bash
# Initialize project
bun init

# Creates:
# ├── package.json
# ├── tsconfig.json
# ├── index.ts
# └── README.md

# With specific template
bun create <template> <project-name>

# Examples
bun create react my-app        # React app
bun create next my-app         # Next.js app
bun create vite my-app         # Vite app
bun create elysia my-api       # Elysia API
```

### 2.2 package.json

```json
{
  "name": "my-bun-project",
  "version": "1.0.0",
  "module": "index.ts",
  "type": "module",
  "scripts": {
    "dev": "bun run --watch index.ts",
    "start": "bun run index.ts",
    "test": "bun test",
    "build": "bun build ./index.ts --outdir ./dist",
    "lint": "bunx eslint ."
  },
  "devDependencies": {
    "@types/bun": "latest"
  },
  "peerDependencies": {
    "typescript": "^5.0.0"
  }
}
```

### 2.3 tsconfig.json (Bun-optimized)

```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "module": "esnext",
    ...
  }
}
```