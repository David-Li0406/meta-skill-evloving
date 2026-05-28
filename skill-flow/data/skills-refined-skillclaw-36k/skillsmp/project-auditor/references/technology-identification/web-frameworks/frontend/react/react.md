# React

**Category**: web-frameworks/frontend
**Description**: A JavaScript library for building user interfaces
**Homepage**: https://react.dev

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `react` - Core React library
- `react-dom` - React DOM renderer

#### YARN
- `react` - Core React library
- `react-dom` - React DOM renderer

#### PNPM
- `react` - Core React library
- `react-dom` - React DOM renderer

### Related Packages (Not for detection - informational only)
These packages are commonly used with React but should not trigger React detection on their own:
- react-router
- react-router-dom
- react-redux
- react-query
- @tanstack/react-query
- react-hook-form
- react-native
- next (see Next.js patterns)
- gatsby

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions may indicate React usage*

- `.jsx` - React JavaScript files
- `.tsx` - React TypeScript files

### Configuration Files
*Known configuration files commonly used with React*

- `vite.config.js` - Vite configuration (common React bundler)
- `vite.config.ts` - Vite TypeScript configuration
- `next.config.js` - Next.js configuration (React framework)
- `next.config.mjs` - Next.js ES module configuration
- `gatsby-config.js` - Gatsby configuration (React framework)
- `craco.config.js` - Create React App Configuration Override
- `.babelrc` - Babel configuration
- `.babelrc.json` - Babel configuration
- `babel.config.js` - Babel configuration
- `babel.config.json` - Babel configuration

### Import Patterns

#### JavaScript
Extensions: `.js`, `.jsx`, `.mjs`

**Pattern**: `import\s+React\s+from\s+['"]react['"]`
- Default React import (ES6)
- Example: `import React from 'react';`

**Pattern**: `import\s+\{[^}]+\}\s+from\s+['"]react['"]`
- Named imports from React
- Example: `import { useState, useEffect } from 'react';`

**Pattern**: `import\s+\*\s+as\s+React\s+from\s+['"]react['"]`
- Namespace import
- Example: `import * as React from 'react';`

**Pattern**: `const\s+React\s*=\s*require\(['"]react['"]\)`
- CommonJS require
- Example: `const React = require('react');`

**Pattern**: `from\s+['"]react-dom['"]`
- React DOM imports
- Example: `import ReactDOM from 'react-dom';`

**Pattern**: `from\s+['"]react-dom/client['"]`
- React 18 client import
- Example: `import { createRoot } from 'react-dom/client';`

#### TypeScript
Extensions: `.ts`, `.tsx`

**Pattern**: `import\s+React\s+from\s+['"]react['"]`
- Default React import
- Example: `import React from 'react';`

**Pattern**: `import\s+type\s+\{[^}]+\}\s+from\s+['"]react['"]`
- Type-only imports
- Example: `import type { FC, ReactNode } from 'react';`

**Pattern**: `import\s+\{[^}]+\}\s+from\s+['"]react['"]`
- Named imports
- Example: `import { useState, useEffect } from 'react';`

### Code Patterns
*React-specific code patterns*

**Pattern**: `React\.createElement\(`
- React createElement call
- Example: `React.createElement('div', null, 'Hello')`

**Pattern**: `<[A-Z][a-zA-Z]*`
- JSX component usage (uppercase indicates component)
- Example: `<MyComponent />`

**Pattern**: `useState\s*\(`
- React useState hook
- Example: `const [count, setCount] = useState(0);`

**Pattern**: `useEffect\s*\(`
- React useEffect hook
- Example: `useEffect(() => { ... }, []);`

**Pattern**: `useRef\s*\(`
- React useRef hook
- Example: `const ref = useRef(null);`

**Pattern**: `useMemo\s*\(`
- React useMemo hook
- Example: `const memoized = useMemo(() => ..., []);`

**Pattern**: `useCallback\s*\(`
- React useCallback hook
- Example: `const callback = useCallback(() => ..., []);`

**Pattern**: `useContext\s*\(`
- React useContext hook
- Example: `const value = useContext(MyContext);`

**Pattern**: `createContext\s*\(`
- React context creation
- Example: `const MyContext = createContext(defaultValue);`

**Pattern**: `React\.Component`
- Class component
- Example: `class MyComponent extends React.Component`

**Pattern**: `React\.PureComponent`
- Pure class component
- Example: `class MyComponent extends React.PureComponent`

---

## Environment Variables

- `REACT_APP_*` - Create React App environment variables
- `NEXT_PUBLIC_*` - Next.js public environment variables
- `GATSBY_*` - Gatsby environment variables
- `VITE_*` - Vite environment variables

## Detection Notes

- Presence of both `react` and `react-dom` packages is strong indicator
- `.jsx` and `.tsx` file extensions are specific to React (and similar libraries)
- React hooks (useState, useEffect, etc.) are definitive React patterns
- JSX syntax with uppercase component names indicates React
- Modern React doesn't require importing React in every file (React 17+)
