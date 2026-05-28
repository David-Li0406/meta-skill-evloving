# esbuild

**Category**: developer-tools/bundlers
**Description**: esbuild - extremely fast JavaScript and TypeScript bundler and minifier
**Homepage**: https://esbuild.github.io

## Package Detection

### NPM
- `esbuild`
- `esbuild-register`
- `esbuild-loader`

## Configuration Files

- `esbuild.config.js`
- `esbuild.config.mjs`
- `esbuild.config.ts`

## Detection Notes

- Look for esbuild in dependencies
- Often used programmatically without config file
- Check for esbuild in build scripts
- Used by Vite for development server
- ~100x faster than webpack/rollup

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Configuration File Detection**: 90% (HIGH)
