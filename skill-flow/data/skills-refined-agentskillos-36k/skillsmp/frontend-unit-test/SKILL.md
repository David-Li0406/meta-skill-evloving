---
name: frontend-unit-test
description:
  Writes unit tests for JavaScript/TypeScript and frontend projects using Vitest
  or Jest. Use when writing or running tests.
---

# Unit Test Protocol

## Framework Detection

Never assume Jest or Vitest. Detect first:

- Check imports in test files
- Check config: `vitest.config.*`, `jest.config.*`
- Check `package.json` dependencies (workspace-specific in monorepos)
- Grep test scripts in package.json

## Running Tests

Run relevant tests only unless explicitly requested:

```bash
pnpm run test path/to/file.test.ts
# monorepo: cd apps/demo-app && pnpm run test path/to/file.test.ts
```

For all tests, use `test` script in closest `package.json`:

```bash
pnpm run test
# monorepo: cd apps/demo-app && pnpm run test
```
