# nestjs

**Category**: web-frameworks/backend
**Homepage**: https://www.npmjs.com/package/@nestjs/core

## Package Detection

### NPM
*Core nestjs package*

- `@nestjs/core`

### YARN
*Core nestjs package via Yarn*

- `@nestjs/core`

### PNPM
*Core nestjs package via pnpm*

- `@nestjs/core`

## Import Detection

### Javascript
File extensions: .js, .mjs

**Pattern**: `import\s+.*\s+from\s+['"]@nestjs/core['"]`
- ES6 import from @nestjs/core
- Example: `import nestjs from '@nestjs/core';`

**Pattern**: `require\(['"]@nestjs/core['"]\)`
- CommonJS require
- Example: `const nestjs = require('@nestjs/core');`

## Detection Notes

- Check for @nestjs/core in dependencies or devDependencies
- Look for import/require statements
- Verify with configuration files

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
