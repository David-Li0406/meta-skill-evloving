# Rollup

**Category**: developer-tools/bundlers
**Description**: Rollup - JavaScript module bundler optimized for ES modules and tree-shaking
**Homepage**: https://rollupjs.org

## Package Detection

### NPM
- `rollup`
- `@rollup/plugin-node-resolve`
- `@rollup/plugin-commonjs`
- `@rollup/plugin-typescript`
- `@rollup/plugin-babel`
- `@rollup/plugin-terser`
- `@rollup/plugin-json`

## Configuration Files

- `rollup.config.js`
- `rollup.config.mjs`
- `rollup.config.ts`
- `rollup.config.cjs`

## Detection Notes

- Look for rollup.config.js in repository root
- Check for rollup in dependencies
- Often used for library bundling
- Vite uses Rollup for production builds

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
