# Vite

**Category**: developer-tools/bundlers
**Description**: Vite - next generation frontend build tool with fast HMR and optimized builds
**Homepage**: https://vitejs.dev

## Package Detection

### NPM
- `vite`
- `@vitejs/plugin-react`
- `@vitejs/plugin-vue`
- `@vitejs/plugin-react-swc`
- `@vitejs/plugin-legacy`
- `vite-plugin-pwa`
- `vitest` (testing)

## Configuration Files

- `vite.config.js`
- `vite.config.ts`
- `vite.config.mjs`
- `vite.config.cjs`
- `vitest.config.js`
- `vitest.config.ts`

## Environment Variables

- `VITE_*` (client-side env vars)

## Detection Notes

- Look for vite.config.js/ts in repository root
- Check for vite in dependencies/devDependencies
- Uses esbuild for dev and Rollup for production
- Modern alternative to webpack

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
