# tdd workflow

test-driven development philosophy and workflow for all project types.

## philosophy

> "the unit test is a design document. the code is merely the implementation."
> — ward cunningham

### testing trophy (not pyramid)

| layer | volume | purpose |
|-------|--------|---------|
| E2E | few | critical user paths |
| integration | many | real behavior across units |
| unit | some | complex isolated logic |
| static | all | types, linting |

**key insight**: integration tests give best ROI. test behavior at boundaries, not implementation details.

### principles

- **test behavior, not implementation**: don't test private methods
- **fast feedback**: sub-second test runs
- **shameless green**: make it work first, then make it right
- **isolation**: each test independent, no shared state

## workflow: red-green-refactor

### 1. red - write failing test

```typescript
it('creates task for authenticated user', async () => {
  const t = convexTest(schema)
  const asUser = t.withIdentity({ name: 'Luke', subject: 'user_123' })

  await asUser.mutation(api.tasks.create, { text: 'Test task' })

  const tasks = await asUser.query(api.tasks.list)
  expect(tasks).toHaveLength(1)
  expect(tasks[0].text).toBe('Test task')
})
```

**key**: test should fail for the right reason (missing functionality, not syntax error)

### 2. green - minimal implementation

write just enough code to pass the test.

**anti-pattern**: don't write extra features "while you're in there"

### 3. refactor - clean up

tests green → improve structure while keeping tests green.

**refactor targets**:
- extract helpers for repeated patterns
- improve naming
- remove duplication

## test layers by project type

### convex turborepo

| layer | tool | location |
|-------|------|----------|
| convex functions | convex-test | packages/backend/convex/__tests__/ |
| react components | @testing-library/react | apps/app/__tests__/ |
| E2E | playwright | apps/app/e2e/ |

### web (non-convex)

| layer | tool | location |
|-------|------|----------|
| unit | vitest | src/__tests__/ |
| component | @testing-library/react | src/components/__tests__/ |
| E2E | playwright | e2e/ |

### xcode

| layer | tool | location |
|-------|------|----------|
| unit | XCTest | Tests/ |
| UI | XCUITest | UITests/ |

## running tests

```bash
# all tests
pnpm test

# watch mode
pnpm test:watch

# coverage
pnpm test:coverage

# specific package (turborepo)
pnpm --filter @repo/backend test

# using verify CLI
verify --format=summary
verify --json --failures-only
```

## package versions (dec 2025)

| package | version | notes |
|---------|---------|-------|
| vitest | 4.0.15+ | test runner |
| @testing-library/react | 16.3.0+ | react 19 compatible |
| convex-test | 0.0.38+ | convex function testing |
| @playwright/test | 1.57.0+ | E2E |
| jsdom | 26.0.0+ | DOM simulation |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| testing implementation | brittle, breaks on refactor | test behavior at boundaries |
| mocking everything | tests pass but real code fails | use real dependencies where possible |
| slow tests | breaks fast feedback | optimize, parallelize |
| skipping red | test may not test what you think | always see test fail first |
| shared state | flaky tests | fresh context per test |
| testing private methods | implementation coupling | test through public API |
