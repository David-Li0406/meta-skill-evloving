# Changelog Analysis

Reading and interpreting dependency changelogs for safe updates.

## Finding Changelogs

### Common Locations

```bash
# In package directory
node_modules/package/CHANGELOG.md
node_modules/package/HISTORY.md
node_modules/package/CHANGES.md

# On GitHub
https://github.com/owner/repo/releases
https://github.com/owner/repo/blob/main/CHANGELOG.md

# On npm
https://www.npmjs.com/package/package?activeTab=versions
```

### Automated Lookup

```bash
# Open package homepage
npm docs package-name

# View package info (includes repo link)
npm view package-name repository.url

# Check for changelog in package
npm pack package-name --dry-run | grep -i change
```

## Reading Changelogs

### Common Format (Keep a Changelog)

```markdown
## [Unreleased]

## [2.0.0] - 2024-01-15

### Added
- New feature X

### Changed
- Modified behavior of Y (BREAKING)

### Deprecated
- Method Z is deprecated, use W instead

### Removed
- Removed support for Node 16 (BREAKING)

### Fixed
- Fixed bug in feature A

### Security
- Fixed CVE-2024-XXXXX
```

### What to Look For

```markdown
## Changelog Review Checklist

### Breaking Changes
- [ ] "BREAKING" or "Breaking Change" labels
- [ ] Removed features/APIs
- [ ] Changed default behaviors
- [ ] Modified function signatures
- [ ] Dropped platform support

### Migration Requirements
- [ ] "Migration" or "Upgrade" sections
- [ ] "Deprecated" warnings (future breaking)
- [ ] Changed configuration options
- [ ] New required dependencies

### Security Fixes
- [ ] CVE references
- [ ] "Security" sections
- [ ] Vulnerability patches

### New Features
- [ ] Features we might use
- [ ] Performance improvements
- [ ] New APIs available
```

## Analyzing Breaking Changes

### Impact Assessment

```markdown
## Breaking Change Analysis: Package v2.0.0

### Change: Removed `legacyMethod()`

**Our Usage:**
```bash
grep -rn "legacyMethod" src/
# src/utils/helper.ts:45: package.legacyMethod()
# src/services/data.ts:78: await package.legacyMethod(config)
```

**Files Affected:** 2
**Effort:** Low (simple replacement)

**Migration:**
```javascript
// Before
package.legacyMethod(options)

// After
package.newMethod(options)
```

### Change: Changed return type of `fetchData()`

**Our Usage:**
```bash
grep -rn "fetchData" src/
# 15 occurrences
```

**Files Affected:** 8
**Effort:** Medium (type changes needed)

**Migration:**
```typescript
// Before
const result: string = await fetchData()

// After
const result: DataResult = await fetchData()
const value: string = result.value
```
```

## Version Comparison

### Comparing Multiple Versions

```markdown
## Version Comparison: Package 1.x → 2.x

### Changes Between Versions

| Feature | v1.5.0 | v2.0.0 | Impact |
|---------|--------|--------|--------|
| legacyMethod | ✅ | ❌ Removed | Need migration |
| newFeature | ❌ | ✅ Added | Optional |
| config.old | ✅ | ⚠️ Deprecated | Plan migration |
| Node 16 | ✅ | ❌ Dropped | Update CI |

### Migration Path

1. **v1.5 → v1.9:** Update to latest v1
2. **v1.9:** Fix all deprecation warnings
3. **v1.9 → v2.0:** Apply breaking changes
```

### Incremental Update Strategy

```markdown
## Update Path: React 16 → 18

### Step 1: 16.8 → 16.14 (Latest v16)
- Fix all deprecation warnings
- Adopt hooks if not already

### Step 2: 16.14 → 17.0.2
- Update react-dom
- Fix UNSAFE_ lifecycle methods
- Test thoroughly

### Step 3: 17.0.2 → 18.2.0
- Update to new root API
- Handle Strict Mode changes
- Adopt concurrent features
```

## Extracting Migration Steps

### From Changelog to Actions

```markdown
## Changelog Entry:
> ### Changed
> - The `connect` function now requires explicit options object.
>   Previously: `connect(host, port)`
>   Now: `connect({ host, port })`

## Extracted Action:
**Task:** Update all `connect()` calls to use options object

**Find:**
```bash
grep -rn "connect(" src/ --include="*.ts"
```

**Replace:**
```typescript
// Before
client.connect(host, port)

// After
client.connect({ host, port })
```

**Estimated Effort:** 1 hour
**Files:** 5
```

## Creating Update Summary

### Template

```markdown
# Dependency Update Summary: [Package] [Old] → [New]

## Overview
- **Package:** [name]
- **Old Version:** [x.y.z]
- **New Version:** [a.b.c]
- **Changelog:** [link]

## Breaking Changes
1. [Change description and impact]
2. [Change description and impact]

## Deprecations to Address
1. [Deprecated feature and replacement]

## Security Fixes
1. [CVE if applicable]

## New Features Available
1. [Optional features to consider]

## Migration Steps
1. [ ] [Step 1]
2. [ ] [Step 2]
3. [ ] [Step 3]

## Testing Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Build succeeds
- [ ] Manual testing complete

## Estimated Effort
- **Low:** Minor changes, < 1 hour
- **Medium:** Several file changes, 1-4 hours
- **High:** Significant refactoring, 1+ days

## Decision
- [ ] Proceed with update
- [ ] Defer update (reason: ___)
- [ ] Skip version (reason: ___)
```

## Tracking Changelog Reviews

```markdown
## Changelog Review Log

| Package | Version | Reviewed | Reviewer | Decision |
|---------|---------|----------|----------|----------|
| lodash | 4.17.21 | 2024-01-15 | @dev | Update |
| react | 18.2.0 | 2024-01-10 | @lead | Plan migration |
| prisma | 5.8.0 | 2024-01-12 | @dev | Update |
```
