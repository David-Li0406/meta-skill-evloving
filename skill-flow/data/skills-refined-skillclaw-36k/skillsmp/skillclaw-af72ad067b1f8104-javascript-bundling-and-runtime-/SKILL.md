---
name: javascript-bundling-and-runtime-optimization
description: Use this skill when you need guidance on bundling JavaScript/TypeScript applications and optimizing runtime performance using esbuild or Bun.
---

# Skill body

## Overview

This skill provides comprehensive guidance on bundling JavaScript and TypeScript applications using esbuild and Bun, focusing on best practices for performance optimization and project structure.

## Core Principles

- **Speed**: Both esbuild and Bun are designed for high performance, significantly faster than traditional tools.
- **Simplicity**: Minimal configuration is required for most use cases, allowing for quick setup and development.
- **Native Support**: Both tools support TypeScript and modern JavaScript features out of the box.

## Project Structure

```
project/
├── src/
│   ├── index.ts          # Main entry point
│   ├── components/       # UI components
│   └── utils/            # Utility functions
├── dist/                 # Build output
├── esbuild.config.mjs    # esbuild configuration (optional)
├── bunfig.toml           # Bun configuration (optional)
├── tsconfig.json         # TypeScript configuration
└── package.json
```

## Using esbuild

### Basic Usage

#### Command Line

```bash
# Basic bundle
esbuild src/index.ts --bundle --outfile=dist/bundle.js

# Production build
esbuild src/index.ts --bundle --minify --sourcemap --outfile=dist/bundle.js

# Watch mode
esbuild src/index.ts --bundle --watch --outfile=dist/bundle.js
```

#### JavaScript API

```javascript
import * as esbuild from 'esbuild';

await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  minify: true,
  sourcemap: true,
  outfile: 'dist/bundle.js'
});
```

### TypeScript Configuration

#### tsconfig.json Best Practices

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "esModuleInterop": true,
    "isolatedModules": true,
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "verbatimModuleSyntax": true,
    "noUncheckedIndexedAccess": true
  },
  "include": ["src/**/*"]
}
```

## Using Bun

### Package Management

- Use `bun install` for faster dependency resolution.
- Add dependencies with `bun add package-name`.
- Run scripts with `bun run script-name`.

### Build Optimization

- Leverage Bun's fast transpiler for development builds.
- Use Bun for production builds to maximize performance.

### Example Usage

In a project, you might use Bun in the build process as follows:

```bash
# Production build with Bun
NODE_ENV=production bun run build
```

## Best Practices

- Prefer esbuild or Bun for bundling and package management to take advantage of their speed.
- Optimize bundle sizes by tree-shaking unused dependencies.
- Monitor performance using built-in tools provided by esbuild and Bun.

## Related Skills

- sveltekit-development: For building SvelteKit applications.
- frontend-design: For creating user interfaces.
- software-architecture: For overall application structure.