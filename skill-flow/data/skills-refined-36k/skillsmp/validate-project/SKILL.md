---
name: validate-project
description: Run full CI validation for the current project directory
version: 1.0.0
author: AI Team
tags: [ci, validation, pre-commit]
---

# Validate Project

Run complete pre-commit validation for the current project.

## When to Use

- Before committing changes
- After major refactoring
- When CI is failing and you need to reproduce locally
- Before creating a pull request

## Available Operations

1. **Go Validation**: generate, tidy, fmt, lint, vet, test
2. **Frontend Validation**: lint, format, type-check, test
3. **Clean Check**: Verify no uncommitted changes from generation

## Instructions

### Step 1: Detect Project Type

Check for these indicators:

- `go.mod` → Go project
- `package.json` in `ui/` → Has frontend
- Directory name → Project identification

### Step 2: Go Validation (if applicable)

```bash
# 1. Generate code (if applicable)
if grep -q "go:generate" **/*.go 2>/dev/null; then
    go generate ./...
fi

# 2. Tidy dependencies
go mod tidy

# 3. Format code
go fmt ./...

# 4. Lint (if config exists)
if [ -f .golangci.yml ] || [ -f .golangci.yaml ]; then
    golangci-lint run
fi

# 5. Vet
go vet ./...

# 6. Test
go test -short ./...
```

### Step 3: Frontend Validation (if applicable)

```bash
cd ui/user
pnpm run ci
```

### Step 4: Clean Check

```bash
if [ -n "$(git status --porcelain)" ]; then
    echo "ERROR: Uncommitted changes after generate/tidy"
    git status --short
    exit 1
fi
```

## Resources

Load these Level 3 resources as needed:

- `scripts/validate.sh` - Complete validation script (run directly)
- `references/ci-pipeline.md` - CI pipeline documentation

## Examples

### Example 1: Go Project

**User asks:** "Validate my changes before committing"

**Response:**

1. Detect go.mod → Go project
2. Run go generate, tidy, fmt, lint, vet, test
3. Check for uncommitted changes
4. Report status with ✓ or ✗ for each step

### Example 2: Full-Stack Project (obot-entraid)

**User asks:** "Run full validation"

**Response:**

1. Run Go validation in root
2. Run frontend validation in ui/user
3. Check for uncommitted changes
4. Report combined status

## Notes

- Stop on first failure for faster feedback
- Always run clean check last to catch generated file changes
- Use `--short` flag for tests to skip long-running integration tests
