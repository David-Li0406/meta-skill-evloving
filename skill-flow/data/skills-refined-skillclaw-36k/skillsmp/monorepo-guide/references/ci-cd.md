# CI/CD Configuration

## Table of Contents
- [GitHub Actions Workflows](#github-actions-workflows)
- [Lovable Cloud Deployment](#lovable-cloud-deployment)
- [Common CI Issues](#common-ci-issues)

## GitHub Actions Workflows

### CI Workflow (`.github/workflows/ci.yml`)
**Trigger:** Push to main, Pull requests

**Steps:**
1. Checkout code
2. Setup Node.js 20
3. `npm ci` (install from lockfile)
4. TypeScript check (`npx tsc --noEmit`)
5. Biome lint check
6. Build (`npm run build`)

### Tests Workflow (heavy)
**Trigger:** Push to main, Pull requests

**Steps:**
1. Unit tests (`npm test`)
2. Playwright smoke tests
3. Coverage reporting

### Security Deep Scan
**Trigger:** Push to main

**Steps:**
1. Trivy vulnerability scan
2. npm audit
3. CodeQL analysis

### Supabase Sync
**Trigger:** Push to main

**Steps:**
1. Generate TypeScript types
2. Validate schema
3. Commit type updates if changed

## Lovable Cloud Deployment

### Requirements
- Root-level `src/` directory with entry point
- Root `package.json` with build scripts
- Shell frontend delegates to main app

### Build Process
```bash
npm ci
npm run build
```

### Entry Point
`src/main.tsx` → `src/App.tsx` → `apps/raamattu-nyt/`

### Environment Variables
Set in Lovable Cloud dashboard:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

## Common CI Issues

### "npm ci" Fails: Lockfile Out of Sync
**Error:** `npm ERR! ... packages not in sync`

**Solution:**
```bash
npm install
git add package-lock.json
git commit -m "Sync package-lock.json"
git push
```

### TypeScript Errors in CI but Not Locally
**Cause:** `tsconfig.ci.json` includes more files

**Solution:**
```bash
# Run same check locally
npx tsc --noEmit -p tsconfig.ci.json
```

### Biome Lint Failures
**Solution:**
```bash
npx @biomejs/biome check --write --unsafe .
git add -A
git commit -m "Fix lint issues"
```

### Test Failures
**Cause:** Missing test environment setup

**Solution:**
Ensure `vitest.config.ts` has proper setup:
```typescript
export default defineConfig({
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

### Build Size Warnings
**Warning:** "Some chunks are larger than 500kb"

**Not blocking** - optimization suggestions only. Consider:
- Dynamic imports for large dependencies
- Manual chunk configuration in Vite
- Tree-shaking unused code

## Workflow Configuration Example

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npx @biomejs/biome lint .
      - run: npm run build
```

## Local CI Simulation

Run all CI checks locally before pushing:

```bash
# Full CI simulation
npm ci
npx tsc --noEmit
npx @biomejs/biome lint .
npm run build
npm test
```
