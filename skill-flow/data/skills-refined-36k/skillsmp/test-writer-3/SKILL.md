---
name: test-writer
description: |
  Create and maintain tests for the Raamattu Nyt monorepo using Vitest and React Testing Library.

  Use when:
  - Writing new tests for hooks, components, or utility functions
  - Analyzing recent git commits to identify code needing tests
  - Reviewing existing tests for correctness and coverage
  - Creating mocks for Supabase, auth, or other dependencies
  - Debugging test failures or flaky tests

  Triggers: "write tests", "test this", "add tests", "need tests for", "analyze test coverage", "fix failing tests", "mock this", "review tests"
---

# Test Writer

Write and maintain tests for the Raamattu Nyt monorepo.

## Context Files (Read First)

For structure and conventions, read from `Docs/context/`:
- `Docs/context/repo-structure.md` - Where test files go
- `Docs/context/conventions.md` - Naming patterns

## Quick Start

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npx vitest run path/to/file.test.ts
```

## Test File Conventions

- Place tests adjacent to source: `useHook.ts` → `useHook.test.ts`
- Use `.test.ts` for pure logic, `.test.tsx` for React components/hooks
- Name: `describe("ComponentName")` or `describe("hookName")`

## Standard Test Structure

```typescript
import { describe, expect, it, vi, beforeEach } from "vitest";

// Mocks BEFORE imports (hoisted)
vi.mock("@/integrations/supabase/client", () => ({
  supabase: { rpc: vi.fn() }
}));

// Import module under test AFTER mocks
import { myFunction } from "./myModule";

describe("myFunction", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("does expected behavior", () => {
    expect(myFunction()).toBe(expected);
  });
});
```

## Hook Testing Pattern

```typescript
import { renderHook, waitFor } from "@testing-library/react";

// Wrapper for context providers
const wrapper = ({ children }) => (
  <AuthProvider>{children}</AuthProvider>
);

it("returns initial state", () => {
  const { result } = renderHook(() => useMyHook(), { wrapper });
  expect(result.current.loading).toBe(true);
});

it("updates on async action", async () => {
  const { result } = renderHook(() => useMyHook(), { wrapper });
  await waitFor(() => {
    expect(result.current.data).toBeDefined();
  });
});
```

## Common Mocks

See [references/mocks.md](references/mocks.md) for reusable mock patterns:
- Supabase client (RPC, auth, schema queries)
- useAuth hook
- React Query
- localStorage

## Workflow

1. **Identify what to test**
   - Use `code-wizard` skill to find the file/function
   - Check git log for recent changes: `git log --oneline -20`

2. **Check existing tests**
   - Find tests: `Glob pattern: **/*.test.{ts,tsx}`
   - Read related test files for patterns

3. **Write tests covering**
   - Happy path (normal operation)
   - Error cases (API failures, invalid input)
   - Edge cases (empty arrays, null, undefined)
   - Loading states for async operations

4. **Run and verify**
   ```bash
   npx vitest run path/to/file.test.ts
   ```

## Test Quality Checklist

- [ ] Tests are independent (no shared state between tests)
- [ ] Mocks are cleared in `beforeEach`
- [ ] Async operations use `waitFor` not arbitrary delays
- [ ] Error scenarios are tested
- [ ] Edge cases covered (null, empty, boundary values)

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| Find code to test | `code-wizard` |
| Debug test failures | `systematic-debugging` |
| CI test failures | `ci-doctor` |
| Lint errors in tests | `lint-fixer` |
