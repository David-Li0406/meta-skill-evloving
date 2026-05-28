---
description: Validate build, tests, and lint before push - ensures code quality gates pass
---

# Build Validator

Agent สำหรับตรวจสอบ build, tests, และ lint ก่อน push - ทำให้มั่นใจว่า quality gates ผ่าน

## Purpose

- รัน tests และตรวจสอบผลลัพธ์
- รัน build และตรวจสอบ success
- รัน linter และตรวจสอบ errors
- รวบรวมผลลัพธ์เป็น report
- Block push ถ้าไม่ผ่าน

## When to Use

- ก่อน `git push`
- ก่อนสร้าง PR
- ใน `/td` workflow
- CI/CD validation

## Instructions

### Step 1: Detect Project Type

```bash
echo "=== Project Detection ==="

# Check for build tools
[ -f "Makefile" ] && echo "Makefile detected"
[ -f "package.json" ] && echo "Node.js project"
[ -f "go.mod" ] && echo "Go project"
[ -f "Cargo.toml" ] && echo "Rust project"
[ -f "pyproject.toml" ] && echo "Python project"
```

### Step 2: Run Tests

#### Makefile Projects
```bash
echo "=== Running Tests ==="
make test
TEST_EXIT_CODE=$?
echo "Test exit code: $TEST_EXIT_CODE"
```

#### Node.js Projects
```bash
npm test
# or
bun test
# or
yarn test
```

#### Go Projects
```bash
go test ./...
```

#### Python Projects
```bash
pytest
# or
python -m pytest
```

### Step 3: Run Build

#### Makefile Projects
```bash
echo "=== Running Build ==="
make build
BUILD_EXIT_CODE=$?
echo "Build exit code: $BUILD_EXIT_CODE"
```

#### Node.js Projects
```bash
npm run build
# or
bun run build
```

#### Go Projects
```bash
go build ./...
```

#### Rust Projects
```bash
cargo build
```

### Step 4: Run Linter

#### Node.js/TypeScript
```bash
echo "=== Running Lint ==="
npm run lint
# or
eslint .
```

#### Go
```bash
golangci-lint run
# or
go vet ./...
```

#### Python
```bash
ruff check .
# or
flake8
```

#### Rust
```bash
cargo clippy
```

### Step 5: Run Type Check (if applicable)

#### TypeScript
```bash
echo "=== Type Checking ==="
npm run typecheck
# or
tsc --noEmit
```

#### Python
```bash
mypy .
```

### Step 6: Analyze Results

Collect all results and determine status:

| Check | Pass Criteria |
|-------|---------------|
| Tests | Exit code 0, no failures |
| Build | Exit code 0, artifacts created |
| Lint | No errors (warnings OK) |
| Types | No type errors |

## Output Format

```markdown
## Build Validation Report

**Project:** [project-name]
**Date:** YYYY-MM-DD HH:MM:SS
**Branch:** [branch-name]

---

### Overall Status: ✅ PASS / ❌ FAIL

---

### Test Results

| Status | Details |
|--------|---------|
| ✅ PASS | X tests passed |
| ❌ FAIL | Y tests failed |

```
[Test output summary]
```

**Failed Tests (if any):**
- `test_name`: Error message

---

### Build Results

| Status | Details |
|--------|---------|
| ✅ PASS | Build successful |
| ❌ FAIL | Build failed |

```
[Build output summary]
```

**Build Errors (if any):**
- [Error description]

---

### Lint Results

| Status | Details |
|--------|---------|
| ✅ PASS | No errors |
| ⚠️ WARN | X warnings |
| ❌ FAIL | Y errors |

**Lint Errors (if any):**
| File | Line | Error |
|------|------|-------|
| `file.ts` | 42 | [error] |

---

### Type Check Results

| Status | Details |
|--------|---------|
| ✅ PASS | No type errors |
| ❌ FAIL | X type errors |

---

### Summary

| Check | Status | Time |
|-------|--------|------|
| Tests | ✅/❌ | Xs |
| Build | ✅/❌ | Xs |
| Lint | ✅/❌ | Xs |
| Types | ✅/❌ | Xs |

---

### Recommendation

**✅ Ready to Push** - All checks passed

OR

**❌ Do Not Push** - Fix the following:
1. [Issue 1]
2. [Issue 2]
```

## Quick Commands

```bash
# All-in-one validation (Makefile)
make test && make build && make lint

# Node.js
npm test && npm run build && npm run lint

# Go
go test ./... && go build ./... && golangci-lint run
```

## Integration

- Required step in `/td` workflow
- Blocks push if failed
- Generates report for PR
- Logs results to activity log

## Error Recovery

### Common Test Failures
- Missing dependencies → `npm install` / `go mod tidy`
- Stale cache → Clean and rebuild
- Environment issues → Check .env files

### Common Build Failures
- Type errors → Fix types
- Missing imports → Add imports
- Circular dependencies → Refactor

### Common Lint Failures
- Formatting → Run formatter
- Unused variables → Remove or use
- Style violations → Fix per rules
