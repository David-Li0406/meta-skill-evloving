# Large-Scale Refactoring

Strategies for refactoring across multiple files, modules, or the entire codebase.

## When Is It Large-Scale?

| Scope | Examples |
|-------|----------|
| API Migration | Changing function signatures used across codebase |
| Dependency Update | Major version upgrade with breaking changes |
| Architecture Change | Moving from callbacks to promises, class to functional |
| Module Restructure | Reorganizing directory structure |
| Naming Convention | Renaming patterns across codebase |

## Core Principles

### 1. Incremental Migration

Never do "big bang" migrations. Instead:

```
Old API --> Bridge --> New API --> Remove Bridge --> Clean
```

**Example: Function Signature Change**

```typescript
// Phase 1: Add new signature, old calls existing
function getUser(id: string): User;  // old
function getUser(id: string, options?: GetUserOptions): User;  // new

// Phase 2: Migrate call sites incrementally
// File 1: getUser(id) --> getUser(id, {})
// File 2: getUser(id) --> getUser(id, {})
// ...

// Phase 3: Remove old signature support
function getUser(id: string, options: GetUserOptions): User;
```

### 2. Parallel Implementations

Run old and new side-by-side:

```typescript
// Feature flag approach
function processData(data: Input) {
  if (useNewProcessor) {
    return newProcessor(data);
  }
  return oldProcessor(data);
}

// Verify in production
// Then remove old path
```

### 3. Strangler Fig Pattern

Gradually replace old system:

```
Request --> Router --> Old System (90%)
                   --> New System (10%)

// Over time...

Request --> Router --> Old System (10%)
                   --> New System (90%)

// Finally...

Request --> New System (100%)
```

## Workflow: Large-Scale Refactoring

### Phase 1: Preparation

- [ ] Map all affected files
- [ ] Ensure comprehensive test coverage
- [ ] Create tracking document
- [ ] Get team alignment (if applicable)
- [ ] Create feature branch

**Find affected files:**

```bash
# Find all usages of function/type
rg -l "oldFunctionName" --type ts

# Find all imports from module
rg -l "from ['\"].*old-module" --type ts

# Count occurrences
rg -c "oldFunctionName" --type ts
```

### Phase 2: Bridge

- [ ] Create adapter/bridge layer
- [ ] New code uses new patterns
- [ ] Old code continues working
- [ ] Tests pass

**Bridge Pattern Example:**

```typescript
// bridge.ts - temporary compatibility layer

// Re-export new API as old names
export { newFunction as oldFunction } from './new-module';

// Or wrap with adapter
export function oldFunction(oldArgs: OldType): OldReturn {
  const newArgs = convertToNew(oldArgs);
  const result = newFunction(newArgs);
  return convertToOld(result);
}
```

### Phase 3: Incremental Migration

- [ ] Migrate files in small batches
- [ ] Commit after each batch
- [ ] Run tests frequently
- [ ] Track progress

**Batch Strategy:**

```
Batch 1: Low-risk utilities (5 files)
  --> Test, Commit

Batch 2: Internal modules (10 files)
  --> Test, Commit

Batch 3: Core logic (15 files)
  --> Test, Commit

Batch 4: External interfaces (5 files)
  --> Test, Commit
```

### Phase 4: Cleanup

- [ ] Remove bridge layer
- [ ] Remove old implementations
- [ ] Update documentation
- [ ] Final comprehensive test

## API Migration Patterns

### Deprecation Approach

```typescript
/**
 * @deprecated Use `newFunction` instead. Will be removed in v3.0.
 */
export function oldFunction(args: OldArgs): OldReturn {
  console.warn('oldFunction is deprecated, use newFunction');
  return newFunction(convertArgs(args));
}

export function newFunction(args: NewArgs): NewReturn {
  // New implementation
}
```

### Codemods

For large-scale automated changes, use codemods:

```typescript
// Transform: oldFunc(a, b) --> newFunc({ first: a, second: b })

import { Transform } from 'jscodeshift';

const transform: Transform = (file, api) => {
  const j = api.jscodeshift;

  return j(file.source)
    .find(j.CallExpression, { callee: { name: 'oldFunc' } })
    .replaceWith(path => {
      const [a, b] = path.node.arguments;
      return j.callExpression(
        j.identifier('newFunc'),
        [j.objectExpression([
          j.property('init', j.identifier('first'), a),
          j.property('init', j.identifier('second'), b),
        ])]
      );
    })
    .toSource();
};
```

### Search-Replace with Verification

For simpler changes:

```bash
# Find and review first
rg "oldPattern" --type ts -C 3

# If pattern is consistent, use sed/replace
# But ALWAYS review the diff before committing

# Example with ripgrep and sed
rg -l "oldImport" --type ts | xargs sed -i '' 's/oldImport/newImport/g'

# Review changes
git diff

# If wrong, reset
git checkout -- .
```

## Dependency Updates

### Major Version Upgrades

1. **Read the migration guide**
2. **Check breaking changes**
3. **Update incrementally**

```bash
# Check current version
bun pm ls <package>

# Check latest version and changes
npm info <package> versions
npm info <package> changelog

# Update
bun add <package>@latest

# If breaking changes, might need to pin
bun add <package>@^3.0.0
```

### Handling Breaking Changes

**Step-by-step approach:**

```typescript
// 1. Create compatibility layer
// compat/old-api.ts
import { newThing } from 'updated-package';

export function oldApiFunction() {
  // Wrap new API to match old interface
  return newThing.method();
}

// 2. Update internal imports to use compat layer
import { oldApiFunction } from './compat/old-api';

// 3. Gradually update to new API directly
import { newThing } from 'updated-package';
newThing.method();

// 4. Remove compat layer
```

## Directory Restructure

### Planning the New Structure

```
# Document current structure
tree src/ -I node_modules > structure-before.txt

# Design new structure
# src/
# ├── features/
# │   ├── auth/
# │   ├── users/
# │   └── orders/
# ├── shared/
# │   ├── components/
# │   └── utils/
# └── core/
#     ├── api/
#     └── config/
```

### Safe Restructure Process

1. **Create new directories first**

```bash
mkdir -p src/features/{auth,users,orders}
mkdir -p src/shared/{components,utils}
mkdir -p src/core/{api,config}
```

2. **Move files with git (preserves history)**

```bash
git mv src/auth/* src/features/auth/
git mv src/components/* src/shared/components/
```

3. **Update imports systematically**

```bash
# Find files with old imports
rg -l "from ['\"].*src/auth" --type ts

# Update each file's imports
```

4. **Create barrel exports for compatibility**

```typescript
// src/auth/index.ts (temporary re-export)
export * from '../features/auth';
```

5. **Test after each major move**

6. **Remove temporary re-exports**

## Tracking Progress

### Progress Document

```markdown
# Refactoring: Migrate to New Auth API

## Status: In Progress (60%)

## Files to Migrate: 45
- [x] src/api/users.ts
- [x] src/api/orders.ts
- [x] src/services/auth.ts
- [ ] src/services/permissions.ts
- [ ] src/routes/admin.ts
...

## Blockers
- [ ] Need to update auth library first

## Rollback Plan
- Revert to commit: abc1234
- Or revert PR: #123
```

### Git Commit Strategy

```bash
# Use consistent commit prefixes
git commit -m "refactor(auth): migrate users.ts to new auth API"
git commit -m "refactor(auth): migrate orders.ts to new auth API"
git commit -m "refactor(auth): migrate services to new auth API"
git commit -m "refactor(auth): remove legacy auth bridge"
```

## When to Pause

Stop large-scale refactoring if:

- [ ] Tests are failing and fix is non-obvious
- [ ] Scope is expanding beyond original plan
- [ ] You're making behavior changes, not just restructuring
- [ ] Team members need to work on affected files
- [ ] You've hit an unexpected architectural issue

**Pause strategy:**
1. Commit working state
2. Document what's done, what's left
3. Create issues for remaining work
4. Ship what's complete if possible

## Recovery from Failed Migration

### Partial Rollback

```bash
# Identify where things went wrong
git log --oneline

# Revert specific commits
git revert <commit-hash>

# Or reset to known good state (careful!)
git reset --hard <known-good-commit>
```

### Bridge Restoration

If you removed the bridge too early:

1. Revert the bridge removal commit
2. Re-run tests
3. Identify what was missed
4. Complete migration properly
5. Try bridge removal again

### Feature Flag Emergency

```typescript
// Quick rollback mechanism
const useNewImplementation = process.env.USE_NEW_IMPL === 'true';

function criticalFunction() {
  if (useNewImplementation) {
    return newImplementation();
  }
  return oldImplementation(); // Keep old code for emergency
}
```
