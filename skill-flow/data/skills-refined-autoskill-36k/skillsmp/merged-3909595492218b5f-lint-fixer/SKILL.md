---
name: lint-fixer
description: Use this skill for analyzing and fixing linting and formatting issues in TypeScript projects using Biome. It is applicable when resolving lint errors, applying code formatting, or reviewing code quality.
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

1. **Assess** - `npx @biomejs/biome lint .`
2. **Auto-fix** - `npx @biomejs/biome check --write .`
3. **Manual fixes** - Priority: errors → warnings → infos
4. **Verify** - `npx tsc --noEmit && npx @biomejs/biome check .`

## Capabilities
- Analyze Biome lint errors, warnings, and infos
- Auto-fix safe linting issues
- Review and apply TypeScript strict mode fixes
- Explain linting rules and best practices
- Batch fix common patterns

## Common Biome Issues

### 1. Template Literals (useTemplate)
**Issue:** String concatenation should use template literals

**Before:**
```javascript
alert('Error: ' + err.message);
```

**After:**
```javascript
alert(`Error: ${err.message}`);
```

### 2. Const Declarations (useConst)
**Issue:** Variables that are never reassigned should use `const`

**Before:**
```javascript
let value = 10;
```

**After:**
```javascript
const value = 10;
```

### 3. Unused Variables (noUnusedVariables)
**Issue:** Variables declared but never used

**Fix:**
```typescript
// Remove if truly unused
// const unused = value;

// Or prefix with _ if intentionally unused
const _intentionallyUnused = value;
```

### 4. Console Statements (noConsole)
**Issue:** Console statements in production code

**Fix:**
```typescript
// Remove or conditionally include
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info');
}
```

### 5. Any Type (noExplicitAny)
**Issue:** Using `any` type instead of specific types

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
```

### 6. Non-Null Assertions (noNonNullAssertion)
**Issue:** Using `!` non-null assertion

**Before:**
```typescript
const element = document.getElementById('app')!;
```

**After:**
```typescript
const element = document.getElementById('app');
if (!element) {
  throw new Error('Element not found');
}
```

## Usage Examples

### Example 1: Auto-Fix Safe Issues
**User:** "Fix all safe linting issues"

**Assistant:**
```bash
# Run Biome with auto-fix
npx @biomejs/biome check --write .

# Review changes
git diff

# If changes look good, commit
git add .
git commit -m "fix: apply Biome auto-fixes"
```

### Example 2: Fix Template Literal Issues
**User:** "Fix the template literal warnings"

**Assistant:**
I'll fix the string concatenation issues. Looking at the error:

```javascript
alert('Audion toisto epäonnistui: ' + err.message);
```

Let me fix this:

```javascript
alert(`Audion toisto epäonnistui: ${err.message}`);
```

### Example 3: Fix TypeScript Errors
**User:** "I have TypeScript errors in my component"

**Assistant:**
Let me check the TypeScript errors:

```bash
npx tsc --noEmit 2>&1 | head -20
```

Common fixes include adding type annotations and handling implicit any.

### Example 4: Batch Fix Const Issues
**User:** "Convert all `let` to `const` where possible"

**Assistant:**
```bash
# First, let Biome auto-fix
npx @biomejs/biome check --write .

# For remaining cases, manual review needed
```

### Example 5: Clean Up Console Statements
**User:** "Remove or fix console.log statements"

**Assistant:**
Strategy:
1. **Development logs** - Wrap in environment check
2. **Debug logs** - Remove or convert to proper logging
3. **Error logs** - Keep but use console.error

## Biome Configuration

The project likely has a `biome.json` config file:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["node_modules", "dist", ".next", "build"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "useTemplate": "error",
        "useConst": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsole": "warn"
      }
    }
  }
}
```

## CI/CD Integration

Your GitHub Actions already runs these checks:
```yaml
# .github/workflows/ci.yml
- name: Lint
  run: |
    if npx -y @biomejs/biome --version > /dev/null 2>&1; then
      npx @biomejs/biome lint .
      npx @biomejs/biome format . --check
    fi

- name: TypeScript
  run: npm run typecheck --if-present || npx tsc --noEmit
```

## Quick Reference

| Issue Type | Command to Fix | Manual Review? |
|------------|----------------|----------------|
| Template literals | `--write` | No |
| Const declarations | `--write` | No |
| Formatting | `--write` | No |
| Unused variables | `--write` | Yes - verify not needed |
| Any types | Manual | Yes - add proper types |
| Console statements | Manual | Yes - keep errors only |
| Non-null assertions | Manual | Yes - add null checks |

## Related Documentation
- Biome: https://biomejs.dev/
- TypeScript strict mode: https://www.typescriptlang.org/tsconfig#strict
- See `Docs/04-DEV-WORKFLOW.md` for CI/CD details