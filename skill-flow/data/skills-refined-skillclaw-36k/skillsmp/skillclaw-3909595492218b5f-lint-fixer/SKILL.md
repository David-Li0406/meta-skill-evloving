---
name: lint-fixer
description: Use this skill when analyzing and fixing linting and formatting issues in TypeScript projects using Biome, especially for resolving lint errors and improving code quality.
---

# Lint Fixer

## Context Files (Read First)

For project conventions, read from `Docs/context/`:
- `Docs/context/conventions.md` - Code style and patterns
- `Docs/context/repo-structure.md` - File organization

## Quick Commands

```bash
npx @biomejs/biome check --write .  # Auto-fix lint + format
npx tsc --noEmit                    # Type checking
npm run typecheck:ci                # CI type check
```

## Workflow

1. **Assess** - Run `npx @biomejs/biome lint .` to check for lint issues.
2. **Auto-fix** - Execute `npx @biomejs/biome check --write .` to auto-fix safe linting issues.
3. **Manual fixes** - Address issues in the following priority: errors → warnings → infos.
4. **Verify** - Confirm fixes by running `npx tsc --noEmit && npx @biomejs/biome check .`.

## Common Linting Issues and Fixes

### 1. Template Literals (useTemplate)
**Issue:** String concatenation should use template literals.

**Before:**
```javascript
alert('Error: ' + err.message);
const url = baseUrl + '/' + endpoint;
```

**After:**
```javascript
alert(`Error: ${err.message}`);
const url = `${baseUrl}/${endpoint}`;
```

### 2. Const Declarations (useConst)
**Issue:** Variables that are never reassigned should use `const`.

**Before:**
```javascript
let value = 10;
let result = calculate();
```

**After:**
```javascript
const value = 10;
const result = calculate();
```

### 3. Unused Variables (noUnusedVariables)
**Issue:** Variables declared but never used.

**Fix:**
```typescript
// Remove if truly unused
// const unused = value;

// Or prefix with _ if intentionally unused
const _intentionallyUnused = value;
```

### 4. Console Statements (noConsole)
**Issue:** Console statements in production code.

**Fix:**
```typescript
// Remove or conditionally include
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info');
}

// Or use proper logging
logger.debug('Debug info');
```

### 5. Any Type (noExplicitAny)
**Issue:** Using `any` type instead of specific types.

**Before:**
```typescript
function process(data: any) {
  return data.value;
}
```

**After:**
```typescript
interface Data {
  value: string;
}

function process(data: Data) {
  return data.value;
}

// Or use unknown for truly dynamic data
function process(data: unknown) {
  if (isData(data)) {
    return data.value;
  }
}
```

## References

- **Biome docs**: [Biome Documentation](https://biomejs.dev/)

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| CI failures after fixes | `ci-doctor` |
| Need refactoring | `code-refactoring` |
| Test failures | `test-writer` |