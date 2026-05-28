---
name: validate
description: Run lint, typecheck, and tests. Fix all issues automatically. 린트, 타입체크, 테스트 실행. 문제 자동 수정.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Validate

**IMPORTANT: 모든 설명과 요약은 한국어로 작성하세요. 단, 코드 예시와 명령어는 원문 그대로 유지합니다.**

Run lint, typecheck, and tests. Fix all failures. Repeat until all pass.

## Rules

- Read files completely before fixing
- Fix root causes, not symptoms
- Make minimal, focused changes
- Never skip or ignore failures
- Re-run checks after each fix

## Process

### 1. Detect Project Type
Scan for configuration files to determine project type:

| File | Project Type | Tools |
|------|--------------|-------|
| `package.json` | Node.js | npm/pnpm scripts |
| `pyproject.toml` / `setup.py` | Python | pytest, mypy, ruff/pylint |
| `go.mod` | Go | go vet, golangci-lint, go test |

### 2. Run Lint
```bash
# Node.js (Primary)
npm run lint
pnpm lint
npx eslint .

# Python
ruff check .
pylint **/*.py

# Go
golangci-lint run
go vet ./...
```

On failure:
1. Read error messages carefully
2. Read the entire affected file
3. Identify the root cause
4. Fix with minimal changes
5. Re-run lint

### 3. Run Typecheck
```bash
# Node.js (TypeScript) (Primary)
npm run typecheck
pnpm typecheck
npx tsc --noEmit

# Python
mypy .
pyright

# Go (built-in)
go build ./...
```

On failure:
1. Read type error messages
2. Trace the type flow
3. Fix type definitions or usage
4. Re-run typecheck

### 4. Run Tests
```bash
# Node.js (Primary)
npm test
pnpm test
npx jest
npx vitest

# Python
pytest

# Go
go test ./...
```

On failure:
1. Read test failure output
2. Read the failing test code
3. Read the implementation being tested
4. Determine if test or code is wrong
5. Fix the root cause
6. Re-run tests

### 5. Final Validation
Re-run all checks in sequence:
1. Lint
2. Typecheck
3. Tests

All must pass before completion.

### 6. Report Summary
```
## Validation Summary

Checks Run:
- Lint: PASS (fixed 3 issues)
- Typecheck: PASS
- Tests: PASS (15 tests)

Files Modified:
- src/utils.ts: Fixed unused variable
- src/api.ts: Fixed type error
- src/config.ts: Fixed missing return type
```

## Common Fixes

### Lint Issues
- Unused variables: Remove or use them
- Missing semicolons: Add them (if required by style)
- Inconsistent quotes: Standardize
- Import order: Sort alphabetically

### Type Issues
- Missing types: Add explicit type annotations
- Type mismatch: Fix the source of mismatch
- Null/undefined: Add proper null checks
- Generic inference: Add explicit type parameters

### Test Issues
- Assertion failures: Fix code or update test expectation
- Timeout: Optimize or increase timeout
- Missing mocks: Add proper mocks/stubs
- Flaky tests: Fix race conditions

## Anti-Patterns

- Do NOT disable lint rules without justification
- Do NOT use `any` type to bypass type errors
- Do NOT skip failing tests
- Do NOT add `// @ts-ignore` without fixing root cause
- Do NOT modify test expectations without understanding why
