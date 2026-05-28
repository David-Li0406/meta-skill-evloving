# remix

**Category**: web-frameworks/frontend
**Homepage**: https://www.npmjs.com/package/@remix-run/react

## Package Detection

### NPM
*Core remix package*

- `@remix-run/react`

### YARN
*Core remix package via Yarn*

- `@remix-run/react`

### PNPM
*Core remix package via pnpm*

- `@remix-run/react`

## Import Detection

### Javascript
File extensions: .js, .mjs

**Pattern**: `import\s+.*\s+from\s+['"]@remix-run/react['"]`
- ES6 import from @remix-run/react
- Example: `import remix from '@remix-run/react';`

**Pattern**: `require\(['"]@remix-run/react['"]\)`
- CommonJS require
- Example: `const remix = require('@remix-run/react');`

## Detection Notes

- Check for @remix-run/react in dependencies or devDependencies
- Look for import/require statements
- Verify with configuration files

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
