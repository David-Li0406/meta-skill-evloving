---
name: jikime-workflow-verify
description: Comprehensive verification workflow with LSP Quality Gates and TRUST 5 integration
version: 1.0.0
tags: ["workflow", "verify", "quality", "lsp", "trust5", "ci-cd"]
triggers:
  keywords: ["verify", "verification", "quality gate", "pre-pr", "LSP", "검증"]
  phases: ["run", "sync"]
  agents: ["manager-quality", "reviewer", "build-fixer"]
  languages: []
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~6000
user-invocable: false
context: fork
agent: manager-quality
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Comprehensive Verification Skill

A unified quality verification system integrating build checks, type safety, linting, testing, security scanning, LSP Quality Gates, and TRUST 5 compliance.

## Overview

```
┌─────────────────────────────────────────────────┐
│           VERIFICATION PIPELINE                 │
├─────────────────────────────────────────────────┤
│  Phase 1: Build          → Compilation check    │
│  Phase 2: Types          → Type safety          │
│  Phase 3: Lint           → Code quality         │
│  Phase 4: Tests          → Functionality        │
│  Phase 5: Security       → Vulnerability scan   │
│  Phase 6: LSP Gates      → Regression check     │
│  Phase 7: TRUST 5        → Principle compliance │
└─────────────────────────────────────────────────┘
```

---

## Verification Profiles

### Quick Profile
**Use case**: Active development, frequent checks
**Duration**: ~10 seconds

```
Checks:
  ✓ Build compilation
  ✓ Type checking
  ✗ Lint (skip)
  ✗ Tests (skip)
  ✗ Security (skip)
```

### Standard Profile (Default)
**Use case**: After completing a feature/change
**Duration**: ~30-60 seconds

```
Checks:
  ✓ Build compilation
  ✓ Type checking
  ✓ Lint validation
  ✓ Test suite
  ✗ Security scan (basic only)
```

### Full Profile
**Use case**: Before major commits
**Duration**: ~2-5 minutes

```
Checks:
  ✓ Build compilation
  ✓ Type checking
  ✓ Lint validation (strict)
  ✓ Test suite with coverage
  ✓ Security scan
  ✓ Dependency audit
  ✓ LSP Quality Gates
```

### Pre-PR Profile
**Use case**: Before creating pull request
**Duration**: ~5-10 minutes

```
Checks:
  ✓ All Full profile checks
  ✓ Secret detection (thorough)
  ✓ Console.log audit
  ✓ TODO/FIXME audit
  ✓ TRUST 5 compliance
  ✓ Diff review suggestions
```

---

## Phase Details

### Phase 1: Build Verification

**Objective**: Ensure project compiles without errors

**Framework Detection**:
| Indicator | Framework | Command |
|-----------|-----------|---------|
| `package.json` + build script | Node.js | `npm run build` |
| `pnpm-lock.yaml` | pnpm | `pnpm build` |
| `Cargo.toml` | Rust | `cargo build` |
| `go.mod` | Go | `go build ./...` |
| `pyproject.toml` | Python | `python -m build` |

**Failure Handling**:
```
IF build fails:
  → Show last 30 lines of error
  → Suggest: /jikime:build-fix
  → STOP verification (critical)
```

### Phase 2: Type Checking

**Objective**: Ensure type safety across codebase

**Commands by Language**:
```bash
# TypeScript
npx tsc --noEmit

# Python
pyright .
# OR
mypy .

# Go
go vet ./...
```

**Error Classification**:
| Severity | Action |
|----------|--------|
| Error | Must fix before PR |
| Warning | Review, document if intentional |

### Phase 3: Lint Validation

**Objective**: Enforce code quality standards

**Auto-Fix Support**:
```bash
# JavaScript/TypeScript
npm run lint -- --fix

# Python
ruff check . --fix

# Go
gofmt -w .
```

**Output Interpretation**:
```
Errors: Code quality violations (must fix)
Warnings: Style suggestions (should fix)
Info: Minor improvements (optional)
```

### Phase 4: Test Suite

**Objective**: Verify functionality and measure coverage

**Coverage Targets** (from quality.yaml):
```yaml
test_coverage_target: 100  # Target for AI-assisted development

# Realistic thresholds:
business_logic: 90%+
api_endpoints: 80%+
ui_components: 70%+
overall: 80%+
```

**Test Reporting**:
```
Tests:     47 passed, 0 failed, 2 skipped
Coverage:  87% statements, 82% branches
Duration:  4.2s
```

### Phase 5: Security Scan

**Objective**: Identify vulnerabilities and secrets

**Checks Performed**:
```bash
# Secret patterns
sk-           # OpenAI/Anthropic keys
api_key       # Generic API keys
password      # Hardcoded passwords
-----BEGIN    # Private keys

# Dependency vulnerabilities
npm audit --production
pip-audit
cargo audit
```

**Severity Levels**:
| Level | Response |
|-------|----------|
| Critical | Block PR, immediate fix |
| High | Must fix before merge |
| Medium | Should fix, can document |
| Low | Informational |

### Phase 6: LSP Quality Gates

**Objective**: Prevent quality regression

**Integration with quality.yaml**:
```yaml
lsp_quality_gates:
  run:
    max_errors: 0
    max_type_errors: 0
    max_lint_errors: 0
    allow_regression: false

  sync:
    max_errors: 0
    max_warnings: 10
    require_clean_lsp: true
```

**Baseline Comparison**:
```
Baseline (phase_start):
  Errors: 0, Warnings: 5

Current:
  Errors: 0, Warnings: 7

Delta: +2 warnings
Threshold: 10 warning increase allowed
Result: PASS (within threshold)
```

**Regression Detection**:
```
IF current_errors > baseline_errors:
  → BLOCK: Error regression detected
  → Show diff: which new errors appeared
  → Suggest: Fix before proceeding

IF current_warnings > baseline_warnings + threshold:
  → WARN: Warning increase detected
  → List new warnings
  → Suggest: Review and address
```

### Phase 7: TRUST 5 Compliance

**Objective**: Verify quality principles are maintained

For detailed checks and scoring, see:
- [TRUST 5 Compliance](modules/trust5-compliance.md) - Principle checks, commands, and scoring

| Principle | Key Checks |
|-----------|------------|
| **[T] Tested** | 80%+ coverage, critical paths, edge cases |
| **[R] Readable** | < 50 line functions, complexity < 10 |
| **[U] Unified** | Architecture compliance, no duplicates |
| **[S] Secured** | No secrets, input validation, OWASP |
| **[T] Trackable** | Structured logging, error context |

**Target**: 0.8+ (80% compliance) overall TRUST 5 score

---

## Incremental Verification

For large codebases, verify only changed files:

```bash
# Get changed files
git diff --name-only HEAD~1

# Filter by extension
*.ts, *.tsx, *.js, *.jsx → Type + Lint
*.py → Pyright + Ruff
*.go → go vet + golint
```

**Benefits**:
- 10x faster feedback
- Focused on recent changes
- Immediate during development

**Limitations**:
- May miss cross-file impacts
- Full verification still needed pre-PR

---

## Auto-Fix Workflow

When `--fix` is enabled:

```
Step 1: Run initial verification
        ↓
Step 2: Identify auto-fixable issues
        - Lint formatting
        - Import sorting
        - Trailing whitespace
        ↓
Step 3: Apply fixes
        - eslint --fix
        - prettier --write
        - isort (Python)
        ↓
Step 4: Re-run verification
        ↓
Step 5: Report remaining issues
        - Type errors (manual fix)
        - Logic issues (manual fix)
        - Security issues (manual fix)
```

---

## Integration Points

### With Orchestrators

**J.A.R.V.I.S.**:
```
Iteration cycle includes verification:
  Implement → Verify → If fail: pivot strategy

Automatic verification triggers:
  - After each major change
  - Before completing phase
  - On iteration boundary
```

**F.R.I.D.A.Y.**:
```
Module-by-module verification:
  Migrate module → Verify module → Next module

Migration cannot proceed if:
  - Type errors in current module
  - Regression evals failing
```

### With Commands

| Command | Integration |
|---------|-------------|
| `/jikime:2-run` | Verify after implementation |
| `/jikime:3-sync` | Pre-PR verification required |
| `/jikime:loop` | Verify in each iteration |
| `/jikime:eval` | Verification as grader |

### With Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "condition": "\\.(ts|tsx)$",
        "command": "npx tsc --noEmit $FILE 2>&1 | head -5"
      }
    ],
    "Stop": [
      {
        "command": "jikime-adk hooks verify-check",
        "message": "Run /jikime:verify before committing"
      }
    ]
  }
}
```

---

## CI/CD Integration

### Exit Code Convention

```
0: All checks passed
1: Build failure
2: Type errors
3: Lint errors
4: Test failures
5: Security issues
6: LSP regression
7: TRUST 5 violation
```

### GitHub Actions Example

```yaml
name: Verification
on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Verification
        run: |
          jikime-adk verify pre-pr --ci --json > results.json

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: verification-results
          path: results.json

      - name: Check Status
        run: |
          status=$(jq -r '.status' results.json)
          if [ "$status" != "PASS" ]; then
            jq '.warnings' results.json
            exit 1
          fi
```

---

## Troubleshooting

### Common Issues

**Build fails but code looks correct**:
```
1. Clear caches: rm -rf node_modules/.cache
2. Reinstall: rm -rf node_modules && npm install
3. Check tsconfig.json for path issues
```

**Type errors after dependency update**:
```
1. Check @types/* versions match
2. Regenerate lock file
3. Review breaking changes in changelog
```

**Tests pass locally but fail in CI**:
```
1. Check environment variables
2. Verify database/service mocks
3. Check for timing-dependent tests
```

---

## Works Well With

- `jikime-workflow-testing`: Deep dive into testing
- `jikime-workflow-eval`: Eval-driven verification
- `jikime-foundation-core`: TRUST 5 framework
- `jikime-workflow-loop`: Iterative fix cycles
- `jikime-workflow-spec`: SPEC-based quality requirements

---

Last Updated: 2026-01-25
Version: 1.0.0
Integration: LSP Quality Gates, TRUST 5, J.A.R.V.I.S./F.R.I.D.A.Y.
