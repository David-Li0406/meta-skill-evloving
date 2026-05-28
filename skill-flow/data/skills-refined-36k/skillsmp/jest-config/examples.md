# Jest Configuration Examples

## ⚠️ CRITICAL DEPRECATION WARNING

**Date**: December 2025
**Status**: This example may be outdated

**🚨 HIGH PRIORITY - DO NOT USE WITHOUT VERIFICATION**

**⚠️ JEST IS LEGACY FOR VUE 3**: Vitest is the officially recommended test framework for Vue 3 projects as of 2024+. Jest support for Vue 3 may be deprecated.

Before using this example:
1. ✅ **CRITICAL**: Verify `@vue/vue3-jest` is still maintained (check npm last publish date)
2. ✅ Verify `ts-jest` is compatible with current TypeScript and Jest versions
3. ✅ Check if `v8` coverage provider is still recommended over `babel`
4. ✅ Verify `jsdom` test environment compatibility with current version
5. ✅ Check which ESM packages in your project need `transformIgnorePatterns`
6. ✅ Verify Jest configuration options haven't been deprecated
7. ✅ Consider migrating to Vitest for better Vue 3 support

**If `@vue/vue3-jest` is unmaintained:**
- **STOP**: Strongly consider migrating to Vitest
- Consult Vue.js documentation for official testing recommendations
- Check for community forks or alternatives

---

## Example: jest.config.cjs (Preferred Format)

**Configuration Date**: December 2025
**Jest Version**: 29.x
**Format**: CommonJS
**Status**: Legacy for Vue 3 projects

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  collectCoverage: true,
  collectCoverageFrom: [
    '!**/tests/**',
    '!**/node_modules/**',
    '**/src/**/*.{ts,js,vue}',
    '!**/src/**/interfaces/*.ts',
    '!**/src/**/router/*.ts',
    '!**/src/**/services/**/*.ts',
    '!**/src/**/shared/constants/**/*.ts',
    '!**/src/**/shared/EnvConsts.ts',
    '!**/src/store/index.ts',
    '!**/src/App.vue',
    '!**/src/main.ts',
    '!**/src/shims-vue.d.ts',
  ],
  testMatch: [
    '**/src/**/**/*.spec.{ts,js,vue}',
    '**/tests/**/*.spec.{ts,js,vue}',
  ],
  moduleFileExtensions: ['ts', 'js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',  // ⚠️ Verify this package is still maintained!
    '^.+\\.tsx?$': 'ts-jest',
    '^.+\\.js$': 'babel-jest',
  },
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    'src/shared/EnvConsts.ts',
  ],
  transformIgnorePatterns: ['node_modules/(?!axios)'],  // ⚠️ Update based on your ESM packages
  setupFiles: ['<rootDir>/tests/unit/testSetup.ts'],
  moduleNameMapper: {
    '^@/shared/EnvConsts$': '<rootDir>/tests/unit/mockEnvConsts.ts',
    '\\.svg$': '<rootDir>/tests/unit/svgMock.cjs',
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/tests/unit/fileMock.cjs',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  coverageProvider: 'v8',  // ⚠️ Verify 'v8' is still recommended over 'babel'
};
```

---

## Configuration Option Explanations

### Essential Options

**`preset: 'ts-jest'`**
- Preset configuration for TypeScript support
- **Why**: Handles TypeScript transformation automatically
- **Verify**: Check `ts-jest` is compatible with current Jest version
- **Alternative**: Can be omitted if not using TypeScript

**`testEnvironment: 'jsdom'`**
- Simulates browser environment for DOM testing
- **Why**: Vue components require DOM APIs
- **Values**: `'jsdom'` (browser) | `'node'` (Node.js)
- **Verify**: Check jsdom version compatibility

**`coverageProvider: 'v8'`**
- Uses V8's native code coverage (faster, more accurate)
- **Why**: Better performance than Babel-based coverage
- **Default**: `'babel'` in older Jest versions
- **Values**: `'v8'` | `'babel'`
- **Verify**: Check if `'v8'` is still recommended

### Transform Configuration

**`transform`** - File transformers for different file types:
```javascript
{
  '^.+\\.vue$': '@vue/vue3-jest',    // Vue SFC files
  '^.+\\.tsx?$': 'ts-jest',          // TypeScript files
  '^.+\\.js$': 'babel-jest',         // JavaScript files
}
```

**⚠️ CRITICAL**: Verify `@vue/vue3-jest` maintenance status:
```bash
# Check last publish date
npm view @vue/vue3-jest time

# If last publish > 1 year ago, consider Vitest migration
```

### ESM Package Handling

**`transformIgnorePatterns`** - Packages to transform (not ignore):
```javascript
transformIgnorePatterns: ['node_modules/(?!axios)']
```

**Common ESM Packages** (as of December 2025 - verify current list):
- `axios` - HTTP client
- `lodash-es` - Lodash ES modules
- `uuid` - UUID generator
- `nanoid` - ID generator
- `date-fns` - Date utilities (if using ESM version)

**How to detect ESM packages in your project**:
```bash
# Check for "type": "module" in package
npm view axios type

# Or check exports field
npm view axios exports
```

**Example with multiple ESM packages**:
```javascript
transformIgnorePatterns: [
  'node_modules/(?!(axios|lodash-es|uuid|nanoid)/)'
]
```

### Coverage Configuration

**`collectCoverageFrom`** - Files to include in coverage:
```javascript
[
  '!**/tests/**',                     // Exclude test files
  '!**/node_modules/**',              // Exclude dependencies
  '**/src/**/*.{ts,js,vue}',          // Include all source files
  '!**/src/**/interfaces/*.ts',       // Exclude type definitions
  '!**/src/**/router/*.ts',           // Exclude router config
  '!**/src/**/services/**/*.ts',      // Exclude service layer
  '!**/src/**/shared/constants/**',   // Exclude constants
  '!**/src/main.ts',                  // Exclude entry point
  '!**/src/App.vue',                  // Exclude root component
]
```

**Why exclude these files**:
- **Interfaces/Types**: No runtime code to test
- **Router**: Configuration, tested through E2E
- **Services**: API calls, tested with mocks
- **Constants**: Static data, no logic
- **main.ts**: Application bootstrap, tested through E2E

### Module Name Mapper

**`moduleNameMapper`** - Resolve imports and mock assets:
```javascript
{
  '^@/(.*)$': '<rootDir>/src/$1',        // Path alias resolution
  '\\.svg$': '<rootDir>/tests/unit/svgMock.cjs',  // SVG mocks
  '\\.(css|less|scss|sass)$': 'identity-obj-proxy',  // Style mocks
  '\\.(jpg|jpeg|png)$': '<rootDir>/tests/unit/fileMock.cjs',  // Image mocks
}
```

---

## Coverage Provider Comparison

### V8 Coverage (`coverageProvider: 'v8'`)

**Pros**:
- ✓ Faster (native V8 instrumentation)
- ✓ More accurate (actual code execution paths)
- ✓ No transpilation overhead
- ✓ Better source map support

**Cons**:
- ✗ Requires Node.js 10.10.0+
- ✗ May have edge cases with complex builds

**Recommended**: **Yes** (as of December 2025 - verify current recommendation)

### Babel Coverage (`coverageProvider: 'babel'`)

**Pros**:
- ✓ Mature and stable
- ✓ Works with older Node.js versions
- ✓ Well-tested with complex transpilation

**Cons**:
- ✗ Slower (requires Babel transpilation)
- ✗ Less accurate (based on transpiled code)
- ✗ Higher memory usage

**Recommended**: **Legacy** (use v8 unless compatibility issues)

---

## How to Verify Current Standards

### Check Package Maintenance Status

**@vue/vue3-jest**:
```bash
# Check last publish date (CRITICAL)
npm view @vue/vue3-jest time

# Check current version
npm view @vue/vue3-jest version

# Check npm page for maintenance notices
open https://www.npmjs.com/package/@vue/vue3-jest
```

**If last publish > 1 year**: **Consider Vitest migration**

### Check Jest Version

```bash
npm view jest version
npx jest --version
```

### Check Transformer Compatibility

```bash
# ts-jest
npm view ts-jest peerDependencies

# @vue/vue3-jest
npm view @vue/vue3-jest peerDependencies
```

### Test Configuration

```bash
# Run tests with coverage
npm run test:unit -- --coverage

# Run specific test file
npm run test:unit -- path/to/test.spec.ts

# Debug Jest config
npx jest --showConfig
```

---

## Migration to Vitest (Recommended)

**Why**: Vitest is the official recommendation for Vue 3 projects (better performance, native ESM, maintained by Vue team)

**Consider migrating** if `@vue/vue3-jest` is unmaintained (check npm publish date)

---

## Common Issues and Solutions

**Issue**: `@vue/vue3-jest` fails to transform Vue files
- **Solution**: Verify package is still maintained, check version compatibility
- **Alternative**: Migrate to Vitest

**Issue**: ESM package transformation errors
- **Solution**: Add package to `transformIgnorePatterns` exclusion list
- **Check**: Verify package is actually ESM-only

**Issue**: Coverage shows 0% for all files
- **Solution**: Check `coverageProvider` setting, verify v8 compatibility
- **Alternative**: Try `babel` coverage provider

**Issue**: TypeScript type errors in tests
- **Solution**: Verify `ts-jest` version matches TypeScript version
- **Check**: Ensure `tsconfig.json` includes test files

**Issue**: `Cannot find module '@/...'` errors
- **Solution**: Verify `moduleNameMapper` includes `'^@/(.*)$': '<rootDir>/src/$1'`
- **Check**: Ensure paths match your project structure

---

## Important Reminders

1. **Always Research First**: Verify `@vue/vue3-jest` maintenance status before using
2. **Vitest Preferred**: For new Vue 3 projects, use Vitest instead of Jest
3. **ESM Detection**: Check which packages need `transformIgnorePatterns`
4. **Coverage Provider**: Use `v8` unless compatibility issues (verify current recommendation)
5. **Transformer Compatibility**: Ensure all transformers match current tool versions
6. **Legacy Status**: Jest is legacy for Vue 3; plan migration to Vitest
7. **Test Environment**: `jsdom` required for Vue component testing
8. **Module Mapping**: Ensure path aliases match vite.config.ts/tsconfig.json
