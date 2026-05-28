# Common CI Error Patterns

Quick reference for diagnosing CI failures by error message.

## TypeScript Errors

| Error Code | Meaning | Fix |
|------------|---------|-----|
| TS2304 | Cannot find name 'X' | Add import or declare type |
| TS2322 | Type 'X' not assignable to 'Y' | Fix type mismatch |
| TS2339 | Property 'X' does not exist | Add property or fix typo |
| TS2345 | Argument type mismatch | Cast or fix function call |
| TS2531 | Object possibly 'null' | Add null check |
| TS2532 | Object possibly 'undefined' | Add optional chaining `?.` |
| TS6133 | 'X' declared but never used | Remove or prefix with `_` |
| TS7006 | Parameter implicitly has 'any' | Add explicit type |

## Biome Lint Errors

| Rule | Meaning | Fix |
|------|---------|-----|
| `lint/correctness/noUnusedVariables` | Unused variable | Remove or use |
| `lint/correctness/noUnusedImports` | Unused import | Remove import |
| `lint/style/useConst` | Should be const | Change `let` to `const` |
| `lint/suspicious/noExplicitAny` | Explicit `any` | Add proper type |
| `lint/a11y/useSemanticElements` | Accessibility | Use semantic HTML |

Quick fix all: `npx @biomejs/biome check --write .`

## Vitest Test Failures

| Pattern | Meaning | Check |
|---------|---------|-------|
| `expect(received).toBe(expected)` | Value mismatch | Compare actual vs expected |
| `TypeError: Cannot read property` | Null/undefined access | Check mocks and setup |
| `ReferenceError: X is not defined` | Missing mock/import | Add mock or import |
| `Timeout - Async callback` | Test didn't complete | Check async/await, increase timeout |

## GitHub Actions Specific

| Error | Cause | Fix |
|-------|-------|-----|
| `Resource not accessible by integration` | Missing permissions | Add `permissions:` to workflow |
| `EACCES: permission denied` | File permission | Check file modes |
| `npm ci can only install with existing lock` | Lock file mismatch | Commit package-lock.json |
| `Process completed with exit code 1` | Generic failure | Check step logs above |

## Generated Types Failures

**"Generated Supabase types changed"**
```bash
npx supabase gen types typescript --project-id "$SUPABASE_PROJECT_ID" > apps/raamattu-nyt/src/integrations/supabase/types.ts
git add apps/raamattu-nyt/src/integrations/supabase/types.ts
```

**"Generated OpenAPI types changed"**
```bash
npx openapi-typescript ./openapi.yaml -o apps/raamattu-nyt/src/lib/openapi.types.ts
git add apps/raamattu-nyt/src/lib/openapi.types.ts
```

## Network/Timeout Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ETIMEDOUT` | Network timeout | Retry, check external services |
| `ECONNREFUSED` | Service not running | Check if service should be mocked |
| `429 Too Many Requests` | Rate limited | Add delay or use caching |

Usually transient - retry with `gh run rerun <id> --failed`
