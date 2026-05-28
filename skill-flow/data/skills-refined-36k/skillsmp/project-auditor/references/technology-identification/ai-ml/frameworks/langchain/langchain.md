# langchain

**Category**: ai-ml/frameworks
**Homepage**: https://www.npmjs.com/package/langchain

## Package Detection

### NPM
*Core langchain package*

- `langchain`

### YARN
*Core langchain package via Yarn*

- `langchain`

### PNPM
*Core langchain package via pnpm*

- `langchain`

## Import Detection

### Javascript
File extensions: .js, .mjs

**Pattern**: `import\s+.*\s+from\s+['"]langchain['"]`
- ES6 import from langchain
- Example: `import langchain from 'langchain';`

**Pattern**: `require\(['"]langchain['"]\)`
- CommonJS require
- Example: `const langchain = require('langchain');`

## Detection Notes

- Check for langchain in dependencies or devDependencies
- Look for import/require statements
- Verify with configuration files

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
