# Verification Cascade

Non-negotiable gates for all auto work. Reality-grounded, not vibes.

## The Four Gates

Every piece of work must pass all four gates before completion:

| Gate | Command | What it Validates |
|------|---------|-------------------|
| **codegen** | `npx convex codegen` | Convex schema coherence, types generated |
| **types** | `pnpm typecheck` | TypeScript compilation, no type errors |
| **tests** | `verify --format=summary` | All tests pass, coverage maintained |
| **build** | `pnpm build` | Production bundle builds successfully |

## Gate Details

### 1. Convex Codegen

```bash
npx convex codegen
```

**Validates:**
- Schema is valid (`convex/schema.ts`)
- All functions type-check against schema
- Generated types are consistent (`convex/_generated/`)

**Common Failures:**
- Schema field type mismatch
- Missing index definition
- Invalid validator usage

**On Failure:**
```bash
# Check schema
cat convex/schema.ts

# Look for type errors in output
npx convex codegen 2>&1 | grep -i error
```

### 2. TypeScript Typecheck

```bash
pnpm typecheck
# or: pnpm --filter ./packages/backend exec tsc --noEmit
# or: pnpm --filter ./packages/web exec tsc --noEmit
```

**Validates:**
- No TypeScript compilation errors
- All imports resolve
- Type annotations correct

**Common Failures:**
- Missing type imports
- Incorrect function signatures
- Null/undefined handling

**On Failure:**
```bash
# Get detailed errors
pnpm typecheck 2>&1 | head -50

# Check specific file
pnpm exec tsc --noEmit path/to/file.ts
```

### 3. Tests Pass

```bash
verify --format=summary
# or: pnpm test
# or: pnpm --filter ./packages/backend test
```

**Validates:**
- All existing tests pass
- New tests pass
- No regressions introduced

**Common Failures:**
- Test assertion failures
- Missing mocks
- Async timing issues

**On Failure:**
```bash
# Run with verbose output
verify --json --failures-only

# Run specific test file
pnpm test path/to/file.test.ts

# Check test output
pnpm test -- --reporter=verbose
```

### 4. Production Build

```bash
pnpm build
# or: pnpm --filter ./packages/web build
```

**Validates:**
- Production bundle compiles
- No build-time errors
- Assets generate correctly

**Common Failures:**
- Import resolution in production mode
- Environment variable issues
- Bundle size limits

**On Failure:**
```bash
# Get detailed build output
pnpm build 2>&1 | tail -100

# Check for specific errors
pnpm build 2>&1 | grep -i "error\|failed"
```

## Verification Script

Standard verification sequence:

```bash
#!/bin/bash
# verify-all.sh

set -e  # Exit on first failure

echo "=== Gate 1: Convex Codegen ==="
npx convex codegen
echo "✓ codegen passed"

echo "=== Gate 2: TypeScript ==="
pnpm typecheck
echo "✓ types passed"

echo "=== Gate 3: Tests ==="
verify --format=summary
echo "✓ tests passed"

echo "=== Gate 4: Build ==="
pnpm build
echo "✓ build passed"

echo "=== ALL GATES PASSED ==="
```

## Output Contract

Verification results in codex output contract:

```json
{
  "verification": {
    "codegen": "pass",
    "types": "pass",
    "tests": "pass",
    "build": "pass"
  }
}
```

Or on failure:

```json
{
  "verification": {
    "codegen": "pass",
    "types": "fail",
    "tests": "skip",
    "build": "skip"
  },
  "blockers": [
    "Type error in convex/notifications.ts:42 - Property 'email' does not exist on type 'NotificationPrefs'"
  ]
}
```

## Failure Handling

```
Verification failed
├── Which gate?
│   ├── codegen → Schema issue, fix schema.ts
│   ├── types → Type error, fix type annotations
│   ├── tests → Test failure, fix test or implementation
│   └── build → Build error, check imports/config
├── Is it fixable?
│   ├── Yes → Fix and re-run verification
│   └── No → Report as blocked with blocker details
└── After 2 fix attempts
    └── Escalate to copilot review
```

## Gate Dependencies

Gates must run in order because later gates depend on earlier ones:

```
codegen → types → tests → build
   │        │        │       │
   │        │        │       └── needs compiled code
   │        │        └── needs valid types
   │        └── needs generated types
   └── generates types
```

Don't skip gates. Don't reorder gates.

## Partial Verification

For quick checks during development:

```bash
# Just schema
npx convex codegen

# Just types for one package
pnpm --filter ./packages/backend exec tsc --noEmit

# Just one test file
pnpm test path/to/file.test.ts
```

But before reporting completion: **all four gates, full run**.

## CI Alignment

These gates mirror CI pipeline:

```yaml
# .github/workflows/ci.yml
jobs:
  verify:
    steps:
      - run: npx convex codegen
      - run: pnpm typecheck
      - run: pnpm test
      - run: pnpm build
```

If auto verification passes, CI should pass. If CI fails but auto passed, there's a gap to fix.
