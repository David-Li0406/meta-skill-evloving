# Quality Gates

Required checks that must pass at various execution stages.

## Core Quality Gates

All execution modes require these gates:

| Gate | Command | When |
|------|---------|------|
| Type checking | `pnpm typecheck` | After each change |
| Tests | `pnpm test` | After each change |
| Lint | `pnpm lint` | After each change |
| Build | `pnpm build` | Before completion |

## Quick Quality Check

Run after each significant change:

```bash
pnpm test && pnpm typecheck && pnpm lint
```

## Full Quality Validation

Run at milestones and before phase completion:

```bash
#!/bin/bash
set -euo pipefail

echo "Running full quality validation..."

# Type checking
echo "Type checking..."
pnpm -r typecheck
uv run --project services/api mypy app 2>/dev/null || true

# Linting
echo "Linting..."
pnpm -r lint
uv run --project services/api ruff check 2>/dev/null || true

# Tests
echo "Running tests..."
pnpm -r test
uv run --project services/api pytest 2>/dev/null || true

# Build check
echo "Build check..."
pnpm --filter "./apps/web" build 2>/dev/null || pnpm build

echo "✅ Validation complete"
```

## Backend Quality Gates

### Python Backend (if applicable)

```bash
# Type checking
uv run --project services/api mypy app

# Linting
uv run --project services/api ruff check

# Tests
uv run --project services/api pytest

# Specific test file
uv run --project services/api pytest app/tests/test_X.py -v
```

### TypeScript Backend

```bash
# Type checking
pnpm typecheck

# Linting
pnpm lint

# Tests
pnpm test
```

## Frontend Quality Gates

### Web Application

```bash
# Type checking
pnpm --filter "./apps/web" typecheck

# Linting
pnpm --filter "./apps/web" lint

# Tests
pnpm --filter "./apps/web" test

# Build
pnpm --filter "./apps/web" build
```

### UI Package

```bash
# Tests
pnpm --filter "./packages/ui" test

# A11y tests
pnpm --filter "./packages/ui" test:a11y

# Storybook build
pnpm --filter "./packages/ui" storybook
```

## Gate Failure Protocol

### Test Failures

1. **If related to current work**: Fix immediately before proceeding
2. **If unrelated**: Document in progress tracker, create tracking issue
3. **Never proceed** to next task if tests fail for current work

### Type Errors

1. **Fix immediately**: Type errors indicate real problems
2. **Do not use `any`**: Find proper types
3. **Check strict mode**: Ensure TypeScript strict mode is enabled

### Lint Errors

1. **Auto-fix when possible**: `pnpm lint --fix`
2. **Manual fix for complex issues**
3. **Never disable lint rules** without justification

### Build Failures

1. **Clean and rebuild**:
   ```bash
   rm -rf .next node_modules/.cache
   pnpm install
   pnpm build
   ```
2. **Check dependencies**: Ensure all deps installed
3. **Review recent changes**: What might have broken the build?

## Architecture Compliance Checklist

### Backend Implementation

- [ ] Layered architecture: router → service → repository → DB
- [ ] DTOs separate from ORM models
- [ ] ErrorResponse envelope for all errors
- [ ] Cursor pagination for list endpoints
- [ ] Telemetry spans named `{route}.{operation}`
- [ ] Structured logs with trace_id, span_id
- [ ] Migration if schema changed
- [ ] OpenAPI docs updated

### Frontend Implementation

- [ ] Import from @meaty/ui only (no direct Radix)
- [ ] React Query for data fetching
- [ ] Error boundaries around components
- [ ] Loading states handled
- [ ] Accessibility checked (keyboard, ARIA, contrast)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] TypeScript strict mode, no `any`
- [ ] Storybook story if in packages/ui
- [ ] Tests for components and hooks

### Testing Requirements

- [ ] Unit tests for business logic
- [ ] Integration tests for API flows
- [ ] E2E tests for critical paths
- [ ] Negative test cases included
- [ ] Edge cases covered
- [ ] A11y tests for UI components
- [ ] Coverage meets requirements

## Validation with Subagent

For major completions, use task-completion-validator:

```
@task-completion-validator

Task: {task_id}

Expected outcomes:
- [Outcome 1]
- [Outcome 2]

Files changed:
- {list files}

Validate:
1. All acceptance criteria met
2. Project architecture patterns followed
3. Tests exist and pass
4. No regression introduced
```
