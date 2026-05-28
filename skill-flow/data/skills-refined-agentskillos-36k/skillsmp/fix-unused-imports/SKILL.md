---
name: fix-unused-imports
description: Automatically detect and fix TypeScript unused imports/variables errors (TS6133). Use when encountering "declared but its value is never read" errors during tsc, build, or CI checks.
---

# Fix Unused Imports

Automatically detect and remove unused imports/variables in TypeScript/JavaScript projects.

## When to Use

This skill should be invoked when:
- `tsc --noEmit` fails with TS6133 errors
- Build or CI fails due to unused import/variable errors
- User asks to fix unused imports or clean up imports

## Execution Steps

1. **Identify the error**: Parse the TypeScript error message to extract:
   - File path
   - Line number
   - The unused identifier name

2. **Read the file**: Use the Read tool to examine the file content around the error line.

3. **Determine the fix strategy**:
   - **Single import**: If the line is `import { Foo } from 'module';` and `Foo` is unused, delete the entire line.
   - **Multiple imports**: If the line is `import { Foo, Bar, Baz } from 'module';` and only `Bar` is unused, remove just `Bar` from the import list.
   - **Unused variable**: If it's a variable declaration, consider if it should be removed or prefixed with `_`.

4. **Apply the fix**: Use the Edit tool to remove or modify the unused import/variable.

5. **Verify**: Re-run `tsc --noEmit` or the original command to confirm the fix.

## Example Error Patterns

```
src/pages/Example.tsx(24,3): error TS6133: 'ChevronRight' is declared but its value is never read.
```

Parse this as:
- File: `src/pages/Example.tsx`
- Line: 24
- Identifier: `ChevronRight`

## Fix Patterns

### Single Unused Import (delete entire line)
```typescript
// Before
import { UnusedComponent } from './components';

// After
// (line deleted)
```

### One of Multiple Imports (remove from list)
```typescript
// Before
import { Used, Unused, AlsoUsed } from './components';

// After
import { Used, AlsoUsed } from './components';
```

### Type-only Import
```typescript
// Before
import { type UnusedType, UsedType } from './types';

// After
import { UsedType } from './types';
```

## Batch Processing

When multiple TS6133 errors exist:
1. Collect all errors from the TypeScript output
2. Group by file to minimize file reads
3. Fix all issues in each file before moving to the next
4. Re-verify after all fixes

## Commands to Detect Issues

```bash
# For prd-admin
cd prd-admin && pnpm tsc --noEmit

# For prd-desktop
cd prd-desktop && pnpm tsc --noEmit

# Full CI check
./quick.sh ci
```
