# Cross-Package Changes

Strategies for safely making coordinated changes across multiple packages in a monorepo.

## Understanding Cross-Package Dependencies

### Dependency Types

| Type | Direction | Example |
|------|-----------|---------|
| Direct | A imports B | `import { util } from '@org/utils'` |
| Peer | A expects B at runtime | peerDependencies in package.json |
| Dev | A uses B for build/test | devDependencies |
| Transitive | A -> B -> C | A depends on B which depends on C |

### Mapping Dependencies

```bash
# List direct dependencies of a package
cat packages/target/package.json | grep -A20 '"dependencies"'

# Find all packages that depend on target
rg '"@org/target"' packages/*/package.json

# Visualize dependency graph
turbo run build --graph
nx graph
```

### Dependency Order Rules

Always edit in dependency order (leaves first):

```
shared-types     (Level 0 - No internal deps)
     |
     v
utils           (Level 1 - Depends on shared-types)
     |
     v
core            (Level 2 - Depends on utils)
     |
     v
api, web        (Level 3 - Depends on core)
```

**Rule:** Never edit a package before editing its dependencies.

## Cross-Package Change Workflow

### Phase 1: Analysis

```bash
# 1. What are you changing?
echo "Changing: InterfaceName in packages/types"

# 2. Find all affected packages
rg -l "InterfaceName" packages/*/src/ --type ts

# 3. Map dependency order
cat packages/affected/package.json | grep "@org/"
```

- [ ] Identified all affected packages
- [ ] Mapped dependency order
- [ ] Documented change plan

### Phase 2: Schema/Type Changes

Edit foundational types first:

```bash
# Edit shared types
# packages/types/src/models/user.ts
```

- [ ] Updated type/interface definitions
- [ ] Updated type exports
- [ ] Ran type check on types package

```bash
turbo run typecheck --filter=@org/types
```

### Phase 3: Implementation Changes

Edit in dependency order:

```bash
# Level 1: Utils that use the types
# packages/utils/src/user-utils.ts

# Level 2: Core logic
# packages/core/src/user-service.ts

# Level 3: API/App layer
# apps/api/src/routes/users.ts
```

- [ ] Updated each package in order
- [ ] Type checked after each package
- [ ] No circular dependencies introduced

### Phase 4: Test Updates

Update tests last (they depend on implementation):

```bash
# Update test files
# packages/core/tests/user-service.test.ts
# apps/api/tests/users.test.ts
```

- [ ] Updated affected tests
- [ ] All tests pass

### Phase 5: Validation

```bash
# Full build of affected packages
turbo run build --filter=...@org/changed-package

# Full test of affected packages
turbo run test --filter=...@org/changed-package

# Type check everything
turbo run typecheck
```

- [ ] All packages build
- [ ] All tests pass
- [ ] No type errors

## Common Change Patterns

### Pattern 1: Renaming an Export

**Scenario:** Rename `UserData` to `UserProfile`

```bash
# Step 1: Find all usages
rg "UserData" packages/ --type ts

# Step 2: Add alias in source (non-breaking)
# packages/types/src/user.ts
export interface UserProfile { ... }
export type UserData = UserProfile; // Deprecated alias

# Step 3: Update all imports (can be done in parallel)
rg -l "UserData" packages/ --type ts
# Update each file to use UserProfile

# Step 4: Remove alias after all usages updated
# Remove: export type UserData = UserProfile;

# Step 5: Build and test
turbo run build test
```

### Pattern 2: Adding a Required Field

**Scenario:** Add `email` field to `User` interface

```bash
# Step 1: Update interface with optional first
# packages/types/src/user.ts
interface User {
  id: string;
  name: string;
  email?: string;  // Optional first
}

# Step 2: Update all creators to provide field
# packages/core/src/user-factory.ts
createUser({ ...data, email: data.email ?? '' })

# Step 3: Update database schema if needed
# packages/db/migrations/add-user-email.ts

# Step 4: Make field required
# packages/types/src/user.ts
interface User {
  id: string;
  name: string;
  email: string;  // Now required
}

# Step 5: Fix any remaining type errors
turbo run typecheck
```

### Pattern 3: Moving Code Between Packages

**Scenario:** Move `formatDate` from `utils` to `date-utils`

```bash
# Step 1: Copy to new location
# packages/date-utils/src/format.ts
export function formatDate(...) { ... }

# Step 2: Re-export from old location (backward compat)
# packages/utils/src/date.ts
export { formatDate } from '@org/date-utils';

# Step 3: Update package.json dependencies
# packages/utils/package.json
{
  "dependencies": {
    "@org/date-utils": "workspace:*"
  }
}

# Step 4: Update imports in consuming packages
rg "from '@org/utils'.*formatDate" packages/ --type ts
# Change to: import { formatDate } from '@org/date-utils'

# Step 5: Remove re-export after migration complete
# Remove from packages/utils/src/date.ts

# Step 6: Build and test
turbo run build test
```

### Pattern 4: Updating Shared Dependency Version

**Scenario:** Upgrade React from 18 to 19

```bash
# Step 1: Check which packages use React
rg '"react"' packages/*/package.json

# Step 2: Update root package.json or each package
# package.json (root)
{
  "dependencies": {
    "react": "^19.0.0"
  }
}

# Step 3: Install
pnpm install

# Step 4: Fix breaking changes in each package
# Check migration guide, update code

# Step 5: Build and test all
turbo run build test
```

## Dependency Management

### Adding Dependencies

```bash
# Add to specific package
pnpm --filter @org/target add dependency-name
bun add dependency-name --cwd packages/target

# Add internal dependency
pnpm --filter @org/consumer add @org/provider
# Or edit package.json directly:
# "dependencies": { "@org/provider": "workspace:*" }
```

### Removing Dependencies

```bash
# Check no code uses it first
rg "import.*from 'dependency'" packages/target/

# Remove from package
pnpm --filter @org/target remove dependency-name

# Rebuild
turbo run build --filter=@org/target
```

### Version Synchronization

```bash
# Ensure consistent versions across packages
# Check for version mismatches
rg '"react":' packages/*/package.json

# Use workspace protocol for internal deps
# package.json
{
  "dependencies": {
    "@org/shared": "workspace:*"
  }
}
```

## Avoiding Circular Dependencies

### Detection

```bash
# Check for circular imports
npx madge --circular packages/*/src/index.ts

# Nx provides built-in detection
nx graph --affected
```

### Resolution Strategies

1. **Extract shared code to new package**
   ```
   A -> B -> A  (circular)

   Fix: A -> shared <- B
   ```

2. **Dependency inversion**
   ```
   core -> specific  (wrong direction)

   Fix: specific -> core (via interface)
   ```

3. **Event-based communication**
   ```
   A -> B for direct calls

   Fix: A emits event, B subscribes
   ```

## Cross-Package Testing

### Testing Changed Packages

```bash
# Test only affected
turbo run test --filter=...[HEAD^]
nx affected --target=test

# Test package and dependents
turbo run test --filter=...@org/changed

# Test with coverage
turbo run test:coverage --filter=@org/changed
```

### Integration Testing

```bash
# Test packages work together
turbo run test:integration

# E2E tests that span packages
turbo run test:e2e --filter=apps/web
```

## Error Recovery

### Build Fails After Change

```bash
# Identify failing package
turbo run build 2>&1 | grep "error"

# Check dependency order
turbo run build --dry-run

# Build only the failing package to see full errors
turbo run build --filter=@org/failing-package
```

### Type Errors Cascade

```bash
# Start from root packages
turbo run typecheck --filter=@org/types

# Fix errors, then check next level
turbo run typecheck --filter=@org/utils

# Continue up the chain
turbo run typecheck --filter=@org/core
```

### Tests Fail After Change

```bash
# Run failing test in isolation
turbo run test --filter=@org/failing -- --grep "test name"

# Check if it's a dependency issue
cat packages/failing/package.json | grep "@org/"

# Rebuild dependencies
turbo run build --filter=@org/failing^...
```

## Best Practices

### Do

- [ ] Map dependencies before making changes
- [ ] Edit in dependency order (leaves first)
- [ ] Make type changes backward compatible initially
- [ ] Test each package after modification
- [ ] Use workspace protocol for internal deps
- [ ] Commit at logical checkpoints

### Avoid

- [ ] Editing dependents before dependencies
- [ ] Making breaking changes to types immediately
- [ ] Skipping validation between phases
- [ ] Creating circular dependencies
- [ ] Ignoring type errors during migration

## Checklists

### Before Cross-Package Change

- [ ] Identified all affected packages
- [ ] Mapped dependency order
- [ ] Documented change plan
- [ ] Checked for existing circular deps
- [ ] Created branch for change

### After Cross-Package Change

- [ ] All packages build
- [ ] All tests pass
- [ ] No new type errors
- [ ] No new circular dependencies
- [ ] Changes committed with clear message
- [ ] PR description lists affected packages
