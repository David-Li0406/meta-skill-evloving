# ESLint Configuration Examples

## ⚠️ CRITICAL DEPRECATION WARNING

**Date**: December 2025
**Status**: This example may be outdated

**🚨 HIGH PRIORITY - DO NOT USE WITHOUT VERIFICATION**

Before using this example:
1. ✅ Verify ESLint is still on version 9+ with flat config format
2. ✅ Check all plugin versions for compatibility with current ESLint
3. ✅ Verify `eslint-plugin-prettier` is still recommended (or run Prettier separately)
4. ✅ Check if parser configuration syntax has changed
5. ✅ Verify rule names haven't been deprecated or renamed
6. ✅ Check if test framework globals syntax has changed (Jest vs Vitest)
7. ✅ Review ESLint migration guide if major version changed

**If ESLint has released version 10+ or made breaking changes:**
- Consult official ESLint documentation for current flat config format
- Check migration guides for rule changes
- Verify plugin compatibility matrices

---

## Example: eslint.config.cjs (Preferred Format)

**Configuration Date**: December 2025
**ESLint Version**: 9.x
**Format**: Flat Config (CommonJS)

```javascript
const globals = require('globals');
const vuePlugin = require('eslint-plugin-vue');
const vueParser = require('vue-eslint-parser');
const tsPlugin = require('@typescript-eslint/eslint-plugin');
const prettierPlugin = require('eslint-plugin-prettier');
const tsParser = require('@typescript-eslint/parser');

const browserNode = { ...globals.browser, ...globals.node };

module.exports = [
  {
    files: ['**/*.{js,ts,vue}'],
    ignores: ['node_modules', 'dist'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
      globals: browserNode,
    },
    plugins: {
      vue: vuePlugin,
      '@typescript-eslint': tsPlugin,
      prettier: prettierPlugin,
    },
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        { argsIgnorePattern: '^_', caughtErrors: 'none' },
      ],
      '@typescript-eslint/ban-types': 'off',
      '@typescript-eslint/no-explicit-any': 'warn',
      'prettier/prettier': ['error', { endOfLine: 'auto' }],
    },
  },
  {
    files: ['**/__tests__/*.{j,t}s?(x)', '**/*.spec.{j,t}s?(x)'],
    languageOptions: { globals: { ...globals.jest, ...globals.node } },
    // Note: Replace globals.jest with globals.vitest if using Vitest
    // This should be auto-detected from package.json dependencies
  },
  {
    files: ['**/*.d.ts'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-empty-interface': 'off',
      '@typescript-eslint/no-empty-object-type': 'off',
    },
  },
];
```

---

## Configuration Explanations

### File Matching
- `files: ['**/*.{js,ts,vue}']` - Applies to all JS/TS/Vue files
- `ignores: ['node_modules', 'dist']` - Excludes build output and dependencies

### Language Options
- `ecmaVersion: 'latest'` - Use latest ECMAScript features
- `sourceType: 'module'` - Treat files as ES modules
- `parser: vueParser` - Primary parser for Vue files
- `parserOptions.parser: tsParser` - Secondary parser for TypeScript in Vue

### Plugins
- `vue` - Vue 3 specific linting rules
- `@typescript-eslint` - TypeScript linting rules
- `prettier` - Prettier formatting as ESLint rules

### Rules
- `no-console/no-debugger` - Warn in production, allow in development
- `@typescript-eslint/no-unused-vars` - Warn on unused variables (ignore `_` prefix)
- `prettier/prettier` - Enforce Prettier formatting

### Test Files Configuration
- Separate configuration for test files (`*.spec.*`, `__tests__/*`)
- Includes test framework globals (Jest or Vitest)
- **Auto-Detection**: Check package.json for `jest` or `vitest` dependency

### Declaration Files
- Relaxed rules for `.d.ts` files
- Allow `any` type and empty interfaces (common in type declarations)

---

## Test Framework Global Detection

**Vitest Example** (Modern, preferred):
```javascript
{
  files: ['**/__tests__/*.{j,t}s?(x)', '**/*.spec.{j,t}s?(x)'],
  languageOptions: { 
    globals: { 
      ...globals.vitest,  // or globals.node if vitest globals not available
      ...globals.node 
    } 
  },
}
```

**Jest Example** (Legacy, still common):
```javascript
{
  files: ['**/__tests__/*.{j,t}s?(x)', '**/*.spec.{j,t}s?(x)'],
  languageOptions: { 
    globals: { 
      ...globals.jest, 
      ...globals.node 
    } 
  },
}
```

**Detection Logic**:
1. Check `package.json` for `"vitest"` in dependencies/devDependencies → Use `globals.vitest` or `globals.node`
2. Check `package.json` for `"jest"` in dependencies/devDependencies → Use `globals.jest`
3. If both or neither found → Prompt user for test framework choice

---

## Migration from Legacy Config

If migrating from `.eslintrc.*` format:

### Legacy Format (Deprecated)
```javascript
// .eslintrc.js (ESLint 8 and earlier)
module.exports = {
  extends: ['plugin:vue/vue3-recommended', 'prettier'],
  parser: 'vue-eslint-parser',
  parserOptions: {
    parser: '@typescript-eslint/parser',
  },
  // ... rest of config
};
```

### Modern Flat Config (Current)
```javascript
// eslint.config.cjs (ESLint 9+)
module.exports = [
  {
    files: ['**/*.{js,ts,vue}'],
    languageOptions: { parser: vueParser, /* ... */ },
    // ... rest of config
  },
];
```

**Migration Steps**:
1. Remove all `.eslintrc.*` files
2. Create `eslint.config.cjs` with flat config format
3. Convert `extends` to explicit plugin configurations
4. Update parser configuration to `languageOptions.parser`
5. Test with `npx eslint .`

---

## How to Verify Current Standards

**Check ESLint Version and Format**:
```bash
npm view eslint version
npx eslint --version
```

**Check Plugin Compatibility**:
```bash
npm view eslint-plugin-vue version
npm view @typescript-eslint/eslint-plugin version
npm view eslint-plugin-prettier version
```

**Verify Flat Config Support**:
```bash
# ESLint 9+ should use flat config by default
npx eslint --print-config eslint.config.cjs
```

**Test Configuration**:
```bash
npx eslint . --debug
```

---

## Important Reminders

1. **Always Research First**: Verify current ESLint version and plugin compatibility
2. **Check for Breaking Changes**: ESLint major versions may change config format
3. **Plugin Versions Matter**: Ensure all plugins support current ESLint version
4. **Test Framework Detection**: Auto-detect from package.json, prompt if unclear
5. **Prettier Integration**: Verify if `eslint-plugin-prettier` is still recommended or if Prettier should run separately
6. **No Legacy Configs**: Remove `.eslintrc.*` files when using flat config
7. **Format Selection**: Use `.cjs` for maximum compatibility unless project requires ESM
