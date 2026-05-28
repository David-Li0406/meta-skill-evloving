---
name: javascript-typescript-development
description: Use this skill for fast JavaScript and TypeScript development, including bundling, package management, and optimization techniques.
---

# JavaScript and TypeScript Development

This skill provides comprehensive guidance on using modern tools like esbuild and Bun for efficient JavaScript and TypeScript development. It covers bundling, package management, build optimization, and runtime techniques.

## Core Principles

- Utilize esbuild for ultra-fast bundling and minification.
- Leverage Bun for package management and script execution.
- Focus on speed while maintaining code quality and type safety.

## Project Structure

```
project/
├── src/
│   ├── index.ts          # Main entry point
│   ├── components/       # UI components
│   └── utils/            # Utility functions
├── dist/                 # Build output
├── esbuild.config.mjs    # Build script (optional)
├── tsconfig.json         # TypeScript config
└── package.json
```

## esbuild Usage

### Basic Commands

```bash
# Basic bundle
esbuild src/index.ts --bundle --outfile=dist/bundle.js

# Production build
esbuild src/index.ts --bundle --minify --sourcemap --outfile=dist/bundle.js

# Watch mode
esbuild src/index.ts --bundle --watch --outfile=dist/bundle.js
```

### JavaScript API Example

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

## Bun Usage

### Package Management

- Use `bun install` for faster dependency resolution.
- Add dependencies with `bun add <package-name>`.
- Remove dependencies with `bun remove <package-name>`.
- Run scripts with `bun run <script-name>`.

### Build Optimization

- Leverage Bun's fast transpiler for development builds.
- Use Bun for production builds when possible to optimize performance.

## TypeScript Configuration

### tsconfig.json Best Practices

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
    "noEmit": true
  },
  "include": ["src/**/*"]
}
```

## Optimization Techniques

### Minification and Tree Shaking

```javascript
await esbuild.build({
  minify: true,
  treeShaking: true
});
```

### Performance Monitoring

- Monitor performance with Bun's built-in tools.
- Use esbuild's optimization features to reduce bundle sizes.

## Best Practices

- Prefer Bun over npm/yarn for package management when possible.
- Use `isolatedModules: true` in TypeScript config for compatibility with esbuild.
- Run type checking separately with `tsc --noEmit`.
- Optimize bundle sizes by tree-shaking unused dependencies.

## Common Patterns

### Library Build Example

```javascript
await esbuild.build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  external: ['react', 'react-dom'],
  format: 'esm',
  outfile: 'dist/index.js',
  sourcemap: true
});
```

### Application Build Example

```javascript
await esbuild.build({
  entryPoints: ['src/index.tsx'],
  bundle: true,
  splitting: true,
  format: 'esm',
  outdir: 'dist',
  minify: true,
  sourcemap: true
});
```

## Related Skills

- sveltekit-development: For building SvelteKit applications.
- frontend-design: For creating user interfaces.
- software-architecture: For overall application structure.