# rails

**Category**: web-frameworks/backend
**Homepage**: https://www.npmjs.com/package/rails

## Package Detection

### NPM
*Core rails package*

- `rails`

### YARN
*Core rails package via Yarn*

- `rails`

### PNPM
*Core rails package via pnpm*

- `rails`

## Import Detection

### Javascript
File extensions: .js, .mjs

**Pattern**: `import\s+.*\s+from\s+['"]rails['"]`
- ES6 import from rails
- Example: `import rails from 'rails';`

**Pattern**: `require\(['"]rails['"]\)`
- CommonJS require
- Example: `const rails = require('rails');`

## Detection Notes

- Check for rails in dependencies or devDependencies
- Look for import/require statements
- Verify with configuration files

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
