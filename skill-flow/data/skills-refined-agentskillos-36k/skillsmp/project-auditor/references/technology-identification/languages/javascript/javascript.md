# JavaScript

**Category**: languages
**Description**: JavaScript programming language - the language of the web, used for frontend, backend (Node.js), and mobile development
**Homepage**: https://developer.mozilla.org/en-US/docs/Web/JavaScript

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
*Any NPM package indicates JavaScript/Node.js usage, but these are core indicators*

- `node` - Node.js runtime
- `npm` - Node package manager
- `yarn` - Alternative package manager
- `pnpm` - Performant package manager

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions indicates JavaScript usage*

- `.js` - JavaScript source files
- `.mjs` - ES module JavaScript files
- `.cjs` - CommonJS JavaScript files
- `.jsx` - React JSX files

### Configuration Files
*Known configuration files that indicate JavaScript/Node.js*

- `package.json` - NPM package manifest (strong indicator)
- `package-lock.json` - NPM lock file
- `yarn.lock` - Yarn lock file
- `pnpm-lock.yaml` - pnpm lock file
- `.npmrc` - NPM configuration
- `.yarnrc` - Yarn v1 configuration
- `.yarnrc.yml` - Yarn v2+ configuration
- `.pnpmrc` - pnpm configuration
- `.nvmrc` - Node Version Manager config
- `.node-version` - Node version specification
- `jsconfig.json` - JavaScript project configuration
- `.eslintrc` - ESLint configuration
- `.eslintrc.js` - ESLint JS configuration
- `.eslintrc.json` - ESLint JSON configuration
- `.eslintrc.yml` - ESLint YAML configuration
- `eslint.config.js` - ESLint flat config
- `.prettierrc` - Prettier configuration
- `.prettierrc.js` - Prettier JS configuration
- `.prettierrc.json` - Prettier JSON configuration
- `.babelrc` - Babel configuration
- `.babelrc.json` - Babel JSON configuration
- `babel.config.js` - Babel JS configuration
- `babel.config.json` - Babel JSON configuration
- `webpack.config.js` - Webpack configuration
- `webpack.config.ts` - Webpack TypeScript configuration
- `rollup.config.js` - Rollup configuration
- `rollup.config.mjs` - Rollup ES module configuration
- `vite.config.js` - Vite configuration
- `vite.config.ts` - Vite TypeScript configuration
- `esbuild.config.js` - esbuild configuration
- `turbo.json` - Turborepo configuration
- `.swcrc` - SWC compiler configuration
- `jest.config.js` - Jest test configuration
- `jest.config.ts` - Jest TypeScript configuration
- `vitest.config.js` - Vitest configuration
- `vitest.config.ts` - Vitest TypeScript configuration

### Configuration Directories
*Known directories that indicate JavaScript/Node.js*

- `node_modules/` - NPM packages directory (usually gitignored)
- `.npm/` - NPM cache directory

### Import Patterns

#### JavaScript
Extensions: `.js`, `.mjs`, `.cjs`, `.jsx`

**Pattern**: `import\s+.*\s+from\s+['"]`
- ES module import
- Example: `import React from 'react';`

**Pattern**: `import\s+['"]`
- Side-effect import
- Example: `import './styles.css';`

**Pattern**: `import\s*\(`
- Dynamic import
- Example: `const module = await import('./module.js');`

**Pattern**: `require\(['"]`
- CommonJS require
- Example: `const fs = require('fs');`

**Pattern**: `module\.exports\s*=`
- CommonJS module export
- Example: `module.exports = myFunction;`

**Pattern**: `exports\.\w+\s*=`
- CommonJS named export
- Example: `exports.myFunction = myFunction;`

**Pattern**: `export\s+(default\s+)?(function|class|const|let|var)`
- ES module export
- Example: `export default function App() {}`

**Pattern**: `export\s+\{`
- ES named exports
- Example: `export { foo, bar };`

### Code Patterns
*JavaScript-specific code patterns*

**Pattern**: `^\s*"use strict";?$`
- Strict mode declaration
- Example: `"use strict";`

**Pattern**: `^#!/usr/bin/env node`
- Node.js shebang
- Example: `#!/usr/bin/env node`

**Pattern**: `async\s+function\s+\w+`
- Async function declaration
- Example: `async function fetchData() {}`

**Pattern**: `const\s+\w+\s*=\s*async\s*\(`
- Async arrow function
- Example: `const fetchData = async () => {}`

**Pattern**: `await\s+`
- Await expression
- Example: `const data = await fetch(url);`

**Pattern**: `=>\s*\{`
- Arrow function
- Example: `const fn = (x) => { return x * 2; }`

**Pattern**: `\?\?`
- Nullish coalescing operator (ES2020)
- Example: `const value = a ?? 'default';`

**Pattern**: `\?\.\w+`
- Optional chaining (ES2020)
- Example: `const name = user?.profile?.name;`

**Pattern**: `\.\.\.`
- Spread operator
- Example: `const arr = [...items, newItem];`

**Pattern**: `\$\{[^}]+\}`
- Template literal interpolation
- Example: ``const msg = `Hello ${name}`;``

---

## Environment Variables

- `NODE_ENV` - Node environment (development, production, test)
- `NODE_PATH` - Additional module search paths
- `NODE_OPTIONS` - Node.js CLI options
- `NPM_TOKEN` - NPM authentication token
- `NPM_CONFIG_REGISTRY` - NPM registry URL
- `YARN_ENABLE_IMMUTABLE_INSTALLS` - Yarn immutable mode
- `PORT` - Common HTTP port variable

## Detection Notes

- `package.json` is the strongest indicator of JavaScript/Node.js
- `.js` files are ubiquitous but could be from other sources
- ES modules use `import`/`export`, CommonJS uses `require`/`module.exports`
- Modern projects may use `.mjs` (ES) or `.cjs` (CommonJS) extensions
- Lock files (`package-lock.json`, `yarn.lock`) indicate active development
- Bundler configs (webpack, vite, rollup) indicate frontend projects
- Node.js specific code may include `process`, `Buffer`, `__dirname`
