# Jest

**Category**: developer-tools/testing
**Homepage**: https://jestjs.io

## Package Detection

### NPM
*Jest testing framework*

- `jest`
- `@jest/core`
- `ts-jest`
- `@types/jest`
- `jest-environment-jsdom`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@jest/globals['"]`
- Type: esm_import

**Pattern**: `describe\(|test\(|it\(|expect\(`
- Type: api_usage

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
