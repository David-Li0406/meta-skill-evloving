# Duplicate Code Consolidation

Finds and refactors duplicated logic by extracting shared code.

## Types of Duplication

### Function Duplication

**Exact duplicates:** Same function in multiple files
```bash
grep -r "function functionName" --include="*.ts" .
```

**Near duplicates:** Same logic with minor variations - consolidate into parameterized function.

### Component Duplication (React)

Similar components that differ only in styling or minor props should be consolidated into a single parameterized component.

### Logic Duplication

**Repeated conditionals:**
```typescript
// Before: Same check in multiple places
if (user && user.isActive && user.hasPermission('edit')) { ... }

// After: Extracted function
function canUserEdit(user: User | null): boolean {
  return Boolean(user && user.isActive && user.hasPermission('edit'));
}
```

**Repeated transformations:**
```typescript
// Before: Same mapping repeated
const names = users.map(u => `${u.firstName} ${u.lastName}`);

// After: Extracted utility
const getFullName = (p: { firstName: string; lastName: string }) =>
  `${p.firstName} ${p.lastName}`;
```

### API/Data Fetching Duplication

Repeated fetch patterns should be consolidated into generic utilities.

## Where to Place Shared Code

| Scope | Location |
|-------|----------|
| Used across app | `src/utils/`, `src/helpers/`, `src/lib/` |
| Used in one feature | `src/features/[feature]/utils/` |
| Used in one component | Same file, above the component |
| Shared React hooks | `src/hooks/` |
| Shared components | `src/components/shared/` |

Check existing patterns:
```bash
ls src/utils/ src/helpers/ src/lib/ 2>/dev/null
```

## Refactoring Process

1. **Create shared utility** - Extract common logic, parameterize differences, add proper typing
2. **Update all usage sites** - Import new utility, replace inline code
3. **Verify behavior unchanged** - Run tests, type check
4. **Delete orphaned original code**

## When NOT to Deduplicate

- **Intentional duplication**: Separate implementations may be clearer
- **Different lifecycles**: Code that changes for different reasons
- **Test fixtures**: Repeated test setup for isolation
- **Simple expressions**: `x + 1` appearing twice doesn't need extraction
- **Premature extraction**: If code is duplicated but likely to diverge, leave it
