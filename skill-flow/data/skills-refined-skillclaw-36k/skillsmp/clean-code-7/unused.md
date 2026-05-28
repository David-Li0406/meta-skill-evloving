# Unused Code Removal

Identifies and removes dead code introduced in the current branch.

## What to Check

Look for additions (lines starting with `+` in diff) that define:
- Functions/methods
- Variables/constants
- Imports/requires
- Type definitions
- Classes/interfaces

## Checking Usage

### Functions
```bash
grep -r "functionName" --include="*.ts" --include="*.tsx" .
```

A function is unused if:
- Not called anywhere in the codebase
- Not exported and used externally
- Not passed as a callback
- Not referenced in tests (test references count as usage)

### Variables
A variable is unused if:
- Declared but never read
- Only assigned but value never consumed
- Shadowed by another variable immediately

### Imports
Look for imports where:
- Imported symbol never appears elsewhere in file
- Type-only imports where type is never referenced
- Namespace imports (`import * as`) where namespace is unused

### Types/Interfaces
```bash
grep -r "TypeName" --include="*.ts" --include="*.tsx" .
```

A type is unused if:
- Never used as type annotation
- Never extended or implemented
- Never used in generic parameter

## Safety Checks

**Do NOT remove if:**
- Function/variable is exported (may be used externally)
- Referenced in tests
- React component that might be lazy-loaded
- Callback registered with external system
- Has special name pattern (e.g., `_` prefix for intentionally unused)
- Part of interface implementation

## Language-Specific Notes

**TypeScript/JavaScript:**
- Check for dynamic imports: `import('./module')`
- Check for string-based access: `obj['functionName']`
- Check for decorators that might reference the code

**Python:**
- Check for `__all__` exports
- Check for dynamic `getattr` usage

**Go:**
- Compiler catches unused imports
- Check for blank identifier assignments `_ = value`
