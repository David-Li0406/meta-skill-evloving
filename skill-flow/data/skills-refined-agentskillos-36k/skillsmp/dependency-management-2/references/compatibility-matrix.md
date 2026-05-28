# Compatibility Matrix

Tracking and managing dependency compatibility constraints.

## Compatibility Documentation

### Matrix Format

```markdown
## Compatibility Matrix

| Package | Min Version | Max Version | Notes |
|---------|-------------|-------------|-------|
| node | 18.0.0 | - | LTS required |
| typescript | 5.0.0 | - | For decorator support |
| react | 18.0.0 | - | Uses new root API |
| prisma | 5.0.0 | 5.x | Database migrations |

### Peer Dependencies
| Package | Requires | Version |
|---------|----------|---------|
| @testing-library/react | react | >=18.0.0 |
| eslint-plugin-react | react | >=16.8.0 |
```

### Tracking File

```json
// .compatibility.json
{
  "runtime": {
    "node": {
      "minimum": "18.0.0",
      "recommended": "20.x",
      "reason": "LTS support, native fetch"
    }
  },
  "frameworks": {
    "react": {
      "current": "18.2.0",
      "minimum": "18.0.0",
      "constraints": [
        "@testing-library/react requires react >=18",
        "Using new concurrent features"
      ]
    }
  },
  "buildTools": {
    "typescript": {
      "current": "5.3.0",
      "minimum": "5.0.0",
      "constraints": [
        "Using decorator metadata",
        "Bundler module resolution"
      ]
    }
  }
}
```

## Detecting Compatibility Issues

### Peer Dependency Warnings

```bash
# Show peer dependency issues
npm ls 2>&1 | grep "peer dep"

# Or with npm 7+
npm install  # Shows peer dep warnings

# Fix peer dependencies
npm install --legacy-peer-deps  # Ignore (not recommended)
npm install package@compatible-version  # Proper fix
```

### Version Conflict Resolution

```markdown
## Conflict: Multiple React Versions

### Problem
```
npm ls react
├── react@18.2.0
└── legacy-component
    └── react@16.14.0  # Conflict!
```

### Solutions

#### Option 1: Update legacy-component
```bash
npm install legacy-component@latest
# Check if it supports React 18
```

#### Option 2: Use resolutions/overrides
```json
// package.json
{
  "overrides": {
    "legacy-component": {
      "react": "18.2.0"
    }
  }
}
```

#### Option 3: Replace package
Find alternative that supports React 18
```

## Engine Requirements

### Package.json Engines

```json
{
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "engineStrict": true
}
```

### Enforcing Engine Requirements

```bash
# .npmrc
engine-strict=true

# Or in CI
if [[ $(node -v) < "v18" ]]; then
  echo "Node 18+ required"
  exit 1
fi
```

## Cross-Package Compatibility

### Testing Compatibility

```markdown
## Compatibility Test: TypeScript 5.3

### Packages to Test
- [ ] ts-node
- [ ] @types/node
- [ ] tsconfig-paths
- [ ] jest (ts-jest)

### Test Process
1. Create branch: `test/typescript-5.3`
2. Update typescript
3. Run: `npx tsc --version`
4. Run: `npm test`
5. Run: `npm run build`
6. Document results
```

### Compatibility Table

```markdown
## TypeScript Compatibility

| TS Version | ts-node | jest | webpack | Status |
|------------|---------|------|---------|--------|
| 5.3 | 10.9+ | 29+ | 5.89+ | ✅ Tested |
| 5.2 | 10.9+ | 29+ | 5.88+ | ✅ Tested |
| 5.1 | 10.9+ | 29+ | 5.87+ | ✅ Tested |
| 5.0 | 10.9+ | 29+ | 5.82+ | ✅ Tested |
| 4.9 | 10.0+ | 28+ | 5.75+ | ⚠️ Legacy |
```

## Breaking Change Detection

### Automated Checks

```yaml
# .github/workflows/compat-check.yml
name: Compatibility Check

on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check engine requirements
        run: |
          node scripts/check-engines.js

      - name: Check peer dependencies
        run: npm ls 2>&1 | grep -i "peer" && exit 1 || exit 0

      - name: Run compatibility tests
        run: npm run test:compat
```

### Manual Compatibility Check

```markdown
## Compatibility Checklist for PR

### Before Merge
- [ ] No unmet peer dependencies
- [ ] Engine requirements satisfied
- [ ] All tests pass
- [ ] Build succeeds
- [ ] No conflicting versions

### After Merge
- [ ] Monitor error rates
- [ ] Check build times
- [ ] Verify bundle size
```

## Documentation

### When to Update Matrix

Update compatibility documentation when:

1. **Adding new dependency** - Document constraints
2. **Major version update** - Update minimum versions
3. **Dropping support** - Document in CHANGELOG
4. **New platform support** - Add to matrix

### Change Log Entry

```markdown
## Compatibility Changes

### 2024-01-15

#### Added
- Support for Node.js 21.x

#### Changed
- Minimum TypeScript version: 5.0 → 5.1

#### Removed
- Support for Node.js 16.x (EOL)

#### Migration
Users on Node 16 must upgrade to Node 18+ before updating.
```
