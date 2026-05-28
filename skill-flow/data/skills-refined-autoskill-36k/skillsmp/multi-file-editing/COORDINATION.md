# Multi-File Coordination

Techniques for coordinating changes, managing dependencies, and validating across files.

---

## Dependency Order Analysis

### Understanding File Dependencies

Before editing, understand how files depend on each other.

#### Dependency Types

| Type | Direction | Example |
|------|-----------|---------|
| Import | A imports B | A depends on B |
| Type | A uses type from B | A depends on B |
| Runtime | A calls function in B | A depends on B |
| Test | Test imports module | Test depends on module |

#### Building the Dependency Graph

```bash
# Find what a file imports
rg "^import" src/services/user.service.ts

# Find what imports a file
rg "from.*user\.service" --type ts

# Find all imports in a directory
rg "^import.*from" src/services/ --no-heading
```

#### Visualization

```
                    types/user.ts
                         |
          +--------------+--------------+
          |              |              |
     user.repo.ts   user.validator.ts   |
          |              |              |
          +--------------+              |
                 |                      |
          user.service.ts               |
                 |                      |
          +------+------+               |
          |             |               |
    user.routes.ts   user.controller.ts |
          |             |               |
          +-------------+---------------+
                        |
                   app.ts (entry)
```

**Edit order:** types -> repo/validator -> service -> routes/controller -> app

---

## Dependency Order Rules

### Rule 1: Interfaces Before Implementations

Always edit interfaces and types before code that implements them.

```
CORRECT ORDER:
1. types/user.ts (interface)
2. services/user.service.ts (implements)
3. routes/user.routes.ts (uses)

WRONG ORDER:
1. services/user.service.ts (breaks - interface doesn't match)
2. types/user.ts
3. routes/user.routes.ts
```

### Rule 2: Utilities Before Consumers

Edit shared utilities before files that use them.

```
CORRECT ORDER:
1. utils/validation.ts (utility)
2. services/user.service.ts (uses utility)
3. services/project.service.ts (uses utility)

WRONG ORDER:
1. services/user.service.ts (might use old utility behavior)
2. utils/validation.ts (changes behavior)
3. services/project.service.ts (uses new behavior)
```

### Rule 3: Core Before Edge

Edit core/central code before peripheral code.

```
CORRECT ORDER:
1. src/core/database.ts (core)
2. src/repositories/user.repo.ts (uses core)
3. src/routes/users.ts (uses repo)

WRONG ORDER:
1. src/routes/users.ts (references old API)
2. src/core/database.ts (changes API)
3. src/repositories/user.repo.ts (has to adapt)
```

### Rule 4: Source Before Tests

Edit source files before their tests.

```
CORRECT ORDER:
1. src/services/user.service.ts (source)
2. tests/services/user.service.test.ts (test)

WRONG ORDER:
1. tests/services/user.service.test.ts (tests old API)
2. src/services/user.service.ts (breaks tests)
```

---

## Finding Edit Order

### Method 1: Type Checker Guidance

Let TypeScript guide you:

1. Make one change
2. Run `bun run typecheck`
3. Fix errors in order they appear
4. Repeat

```bash
# Watch mode for continuous feedback
bun run typecheck --watch
```

### Method 2: Import Analysis

Trace imports to find order:

```bash
# What does this file depend on?
rg "^import" src/services/user.service.ts

# What depends on this file?
rg "from.*user\.service" --type ts -l
```

### Method 3: Layered Approach

Work through architectural layers:

```
Layer 1: Types/Interfaces
   ↓
Layer 2: Data Access (Repositories)
   ↓
Layer 3: Business Logic (Services)
   ↓
Layer 4: Presentation (Routes/Controllers/Components)
   ↓
Layer 5: Tests
```

---

## Parallel vs Sequential Edits

### When Edits Can Be Parallel

Files can be edited in parallel when:
- They don't import each other
- They both import from a stable source
- Changes are independent

**Example: Parallel Edits**

```
user.service.ts     project.service.ts
       |                    |
       +--------------------+
               |
         shared/types.ts (already edited, stable)
```

After editing `shared/types.ts`, you can edit `user.service.ts` and `project.service.ts` in parallel.

### When Edits Must Be Sequential

Files must be edited sequentially when:
- One imports the other
- One's changes affect the other's interface
- Order matters for correctness

**Example: Sequential Edits**

```
types/user.ts (edit first)
       |
user.service.ts (edit second - uses type)
       |
user.routes.ts (edit third - uses service)
```

---

## Validation Strategies

### Strategy 1: Type Check After Each File

Most thorough, catches issues early:

```bash
# After each file edit
bun run typecheck
```

**Pros:** Immediate feedback, easy to fix issues
**Cons:** Slower for large changes

### Strategy 2: Type Check After Each Layer

Balance of speed and safety:

```bash
# Edit all type files
# Then typecheck
bun run typecheck

# Edit all service files
# Then typecheck
bun run typecheck
```

**Pros:** Faster than per-file, still catches issues
**Cons:** More errors to fix at once

### Strategy 3: Type Check at End

Fastest, for confident changes:

```bash
# Edit all files
# Then typecheck once
bun run typecheck
```

**Pros:** Fastest for known patterns
**Cons:** More errors to untangle if issues

### Strategy 4: Watch Mode

Continuous validation:

```bash
# In one terminal
bun run typecheck --watch

# Edit files in editor, see instant feedback
```

---

## Cross-File Validation Checklist

After completing multi-file changes:

### Type Safety

- [ ] `bun run typecheck` passes
- [ ] No `any` types introduced
- [ ] No type assertions (`as Type`) added unnecessarily
- [ ] Generic types still work

### Runtime Safety

- [ ] `bun test` passes
- [ ] No undefined access at runtime
- [ ] Error handling still works
- [ ] Null checks still valid

### Import/Export

- [ ] No circular imports introduced
- [ ] All exports used
- [ ] No orphaned imports
- [ ] Barrel files updated

### Integration

- [ ] API endpoints respond correctly
- [ ] Database queries work
- [ ] Frontend renders without errors
- [ ] E2E tests pass

---

## Handling Circular Dependencies

### Detecting Circular Dependencies

```bash
# If you get circular dependency errors
# Look for import cycles

# Tool: madge (if installed)
npx madge --circular src/

# Manual: trace imports
rg "import.*from.*'\./" src/services/user.service.ts
# Then check if any of those import user.service
```

### Breaking Circular Dependencies

**Pattern 1: Extract Shared Types**

```
BEFORE (circular):
user.service.ts <-> project.service.ts

AFTER (broken):
types.ts (shared types)
    |
    +-- user.service.ts
    +-- project.service.ts
```

**Pattern 2: Dependency Injection**

```typescript
// BEFORE: Direct import (circular risk)
import { projectService } from './project.service';

// AFTER: Injected dependency
class UserService {
  constructor(private projectService: ProjectService) {}
}
```

**Pattern 3: Lazy Import**

```typescript
// BEFORE: Top-level import
import { helper } from './other';

// AFTER: Lazy import inside function
function doSomething() {
  const { helper } = require('./other');
  return helper();
}
```

---

## Coordination Patterns

### Pattern 1: Interface-First Changes

When changing APIs, define the interface first:

```typescript
// Step 1: Define new interface
interface UserServiceV2 {
  getProfile(id: string): Promise<UserProfile>;  // New method
}

// Step 2: Implement interface
class UserService implements UserServiceV2 {
  async getProfile(id: string) { ... }
}

// Step 3: Update consumers
const profile = await userService.getProfile(userId);
```

### Pattern 2: Feature Flag Coordination

Use feature flags for gradual rollout:

```typescript
// Step 1: Add feature flag
const USE_NEW_AUTH = process.env.USE_NEW_AUTH === 'true';

// Step 2: Implement both paths
function authenticate(req) {
  if (USE_NEW_AUTH) {
    return newAuthSystem(req);
  }
  return oldAuthSystem(req);
}

// Step 3: Update consumers to support both
// Step 4: Enable flag, monitor
// Step 5: Remove old code when stable
```

### Pattern 3: Strangler Fig Pattern

Gradually replace old system:

```typescript
// Step 1: Wrap old system
function getUser(id: string) {
  return oldUserSystem.get(id);
}

// Step 2: Route some traffic to new
function getUser(id: string) {
  if (id.startsWith('new-')) {
    return newUserSystem.get(id);
  }
  return oldUserSystem.get(id);
}

// Step 3: Migrate more traffic
// Step 4: Remove old system
```

---

## Error Recovery

### When Type Check Fails

```bash
# See all errors
bun run typecheck 2>&1 | head -50

# Fix in dependency order
# Start with errors in type files, then services, then routes
```

### When Tests Fail

```bash
# Run failing test in isolation
bun test path/to/failing.test.ts

# Add verbose output
bun test path/to/failing.test.ts --verbose

# Check if it's the test or the code
```

### When Everything Breaks

```bash
# Stash changes and verify main works
git stash
bun run typecheck
bun test

# If main works, pop and diff
git stash pop
git diff

# Consider atomic rollback
git checkout -- .
```

---

## Communication During Changes

### For Team Changes

Document your change plan:

```markdown
## Multi-File Change: Add Organization Support

**Status:** In Progress
**Branch:** feature/organizations

### Files to Change
- [x] src/types/organization.ts (new)
- [x] src/types/user.ts (add orgId)
- [ ] src/services/user.service.ts
- [ ] src/routes/users.ts
- [ ] tests/...

### Blocked Files
Please don't edit:
- src/services/user.service.ts (I'm working on it)

### Timeline
- Day 1: Types and services
- Day 2: Routes and tests
- Day 3: Review and merge
```

### For Solo Changes

Keep notes for yourself:

```markdown
## Session Notes: Refactoring Auth

### Done
- [x] types/auth.ts - new session type
- [x] services/auth.service.ts - session methods

### Next
- [ ] routes/auth.ts - new endpoints
- [ ] middleware/session.ts - new middleware

### Issues Found
- Need to update user type too (unexpected dependency)
- Tests use hardcoded tokens, need to update

### Rollback Point
commit: abc123 "last working state"
```

---

## Quick Reference Commands

```bash
# Find files using a symbol
rg -l "SymbolName" --type ts

# Find imports of a module
rg "from.*module-name" --type ts

# Check for circular dependencies
rg "import.*from.*\./" src/file.ts  # then trace

# Type check
bun run typecheck

# Type check with watch
bun run typecheck --watch

# Run specific test
bun test path/to/file.test.ts

# See git changes
git status --short

# Diff specific file
git diff src/services/user.service.ts

# Stash work in progress
git stash

# Restore stashed work
git stash pop
```
