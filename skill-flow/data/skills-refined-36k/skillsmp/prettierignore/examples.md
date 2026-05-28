# Prettier Ignore Examples

**Last Updated**: December 17, 2025

**⚠️ DEPRECATION CHECK**: Before using, verify patterns are compatible with Prettier version in use.

---

## Standard Configuration (Minimal Essential Exclusions)

```
# Build outputs
dist/
build/

# Dependencies
node_modules/

# Test coverage
coverage/

# Minified/bundled files
*.min.js
*.bundle.js
```

---

## Pattern Explanations

**Build Outputs**:
- `dist/` - Vite default output directory (check `vite.config.ts` for custom paths)
- `build/` - Alternative build output name (some projects use this)

**Dependencies**:
- `node_modules/` - Third-party packages (never format, performance critical)

**Test Coverage**:
- `coverage/` - Jest/Vitest coverage reports (auto-generated HTML/JSON)

**Minified Files**:
- `*.min.js` - Minified JavaScript (already compressed, formatting breaks it)
- `*.bundle.js` - Webpack/Rollup bundles (generated code, don't format)

**Why Minimal**: Only exclude files that:
1. Are auto-generated (build outputs, coverage)
2. Are third-party code (node_modules)
3. Are already minified/optimized (*.min.js)
4. Cause performance issues (large directories)

---

## Detection Logic

### Build Output Detection

**Check `vite.config.ts` or `vite.config.js`**:
```typescript
// If this exists:
export default defineConfig({
  build: {
    outDir: 'custom-dist' // Use this value
  }
})

// Then use: custom-dist/
// Default: dist/
```

### Coverage Directory Detection

**Check `jest.config.js` or `vitest.config.ts`**:
```javascript
// Jest:
module.exports = {
  coverageDirectory: 'test-coverage' // Use this value
}

// Vitest:
export default defineConfig({
  test: {
    coverage: {
      reportsDirectory: './coverage' // Use this value
    }
  }
})

// Default: coverage/
```

---

## Verification Commands

**Test ignore patterns**:
```bash
# Check what files Prettier will process
prettier --check "**/*" --ignore-path .prettierignore

# List ignored files (verbose)
prettier --check "**/*" --ignore-path .prettierignore --debug-check

# Verify specific file is ignored
prettier --check dist/index.js --ignore-path .prettierignore
# Should output: (ignored)
```

**Performance comparison**:
```bash
# Without ignore file (slower)
time prettier --check "**/*"

# With ignore file (faster)
time prettier --check "**/*" --ignore-path .prettierignore
```

---

## Common Mistakes to Avoid

❌ **Don't exclude source code**:
```
# WRONG - Never do this
src/
components/
```

❌ **Don't exclude config files**:
```
# WRONG - Config files should be formatted
package.json
tsconfig.json
vite.config.ts
```

❌ **Don't exclude lock files** (not applicable to Prettier):
```
# UNNECESSARY - Lock files aren't formatted by Prettier
package-lock.json
yarn.lock
pnpm-lock.yaml
```

✅ **Only exclude generated/third-party files**:
```
# CORRECT - Minimal essential exclusions
dist/
node_modules/
coverage/
*.min.js
*.bundle.js
```

---

## Integration with Other Tools

**Lint-Staged** (in `.lintstagedrc`):
```javascript
{
  '**/*.{js,jsx,ts,tsx,vue,json,css,scss,md}': 'prettier --write'
}
// Prettier automatically respects .prettierignore
```

**VSCode Settings** (`.vscode/settings.json`):
```json
{
  "prettier.ignorePath": ".prettierignore",
  "editor.formatOnSave": true
}
```

**Package.json Scripts**:
```json
{
  "scripts": {
    "format": "prettier --write \"**/*\" --ignore-path .prettierignore",
    "format:check": "prettier --check \"**/*\" --ignore-path .prettierignore"
  }
}
```

---

## Troubleshooting

**Issue**: Prettier still formatting excluded files
- **Solution**: Check glob pattern syntax, ensure paths use forward slashes `/`
- **Verify**: Run `prettier --check dist/index.js` - should show `(ignored)`

**Issue**: Prettier running slowly
- **Solution**: Ensure `node_modules/` is excluded, check for missing directory patterns
- **Benchmark**: Compare execution time with/without ignore file

**Issue**: Ignore patterns not working in CI/CD
- **Solution**: Verify `.prettierignore` is committed to git, not in `.gitignore`
- **Check**: `git ls-files .prettierignore` should list the file

---

## Version Compatibility

**Prettier 3.x** (Latest as of Dec 2025):
- Supports `.prettierignore` file
- Standard gitignore-style glob patterns
- Respects `--ignore-path` CLI flag

**Format Stability**: `.prettierignore` has been stable since Prettier 1.x, unlikely to change.

**Breaking Changes**: Check https://prettier.io/docs/en/ignore.html for any updates.