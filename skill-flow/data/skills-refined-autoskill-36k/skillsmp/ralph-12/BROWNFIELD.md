# Ralph Brownfield Mode

For existing codebases, Ralph needs context before generating tasks.

## Brownfield Workflow

```
/ralph "fix auth bug"
        │
        ▼
┌─────────────────────────────┐
│  1. ANALYZE CODEBASE        │
│  - Package manager          │
│  - Test framework           │
│  - Directory structure      │
│  - Existing patterns        │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  2. GENERATE CONTEXT        │
│  - Project-aware prompt.md  │
│  - Smart validation cmds    │
│  - Seeded guardrails        │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  3. DECOMPOSE TASK          │
│  - Scoped to goal           │
│  - Uses project patterns    │
│  - Realistic validations    │
└─────────────────────────────┘
```

---

## Step 1: Codebase Analysis

Before creating Ralph files, analyze the project:

### 1.1 Detect Package Manager & Commands

```bash
# Check which package manager
if [ -f "bun.lockb" ]; then
  PKG_MANAGER="bun"
elif [ -f "pnpm-lock.yaml" ]; then
  PKG_MANAGER="pnpm"
elif [ -f "yarn.lock" ]; then
  PKG_MANAGER="yarn"
elif [ -f "package-lock.json" ]; then
  PKG_MANAGER="npm"
else
  PKG_MANAGER="npm"  # default
fi
```

### 1.2 Extract Scripts from package.json

```bash
# Get available scripts
cat package.json | jq -r '.scripts | keys[]' 2>/dev/null
```

Common scripts to detect:
| Script | Purpose |
|--------|---------|
| `test` | Run tests |
| `lint` | Linting |
| `build` | Build project |
| `dev` | Dev server |
| `typecheck` | Type checking |

### 1.3 Detect Test Framework

```bash
# Check package.json for test frameworks
grep -E "jest|vitest|mocha|pytest|go test" package.json pyproject.toml go.mod 2>/dev/null
```

| Framework | Validation Pattern |
|-----------|-------------------|
| Jest | `npm test -- --testNamePattern "pattern"` |
| Vitest | `npx vitest run --grep "pattern"` |
| Pytest | `pytest -k "pattern"` |
| Go | `go test -run "Pattern"` |

### 1.4 Map Directory Structure

```bash
# Quick structure scan
find . -type d -maxdepth 2 -not -path '*/node_modules/*' -not -path '*/.git/*'
```

Key directories to identify:
- `src/`, `lib/`, `app/` - Source code
- `tests/`, `__tests__/`, `spec/` - Tests
- `components/` - UI components
- `api/`, `routes/` - API routes
- `prisma/`, `drizzle/` - Database

### 1.5 Detect Existing Patterns

Look for:
- Auth patterns (JWT, session, OAuth)
- State management (Redux, Zustand, Context)
- API patterns (REST, GraphQL, tRPC)
- Database patterns (ORM, raw SQL)

---

## Step 2: Generate Context-Aware Files

### 2.1 Enhanced prompt.md Template

```markdown
# Ralph Agent

You are a fresh Ralph agent working on an **existing codebase**.

## Project Context

**Stack:** {detected stack}
**Package Manager:** {pkg_manager}

**Key Directories:**
{directory_map}

**Commands:**
- Test: `{test_command}`
- Lint: `{lint_command}`
- Build: `{build_command}`
- Typecheck: `{typecheck_command}`

**Patterns to Follow:**
{detected_patterns}

## Instructions

1. Read `.ralph/guardrails.md` FIRST - project-specific constraints
2. Read `.ralph/task.md` for your current task
3. Find the FIRST task where `passes: false`
4. **EXPLORE** related code before implementing
5. **FOLLOW** existing patterns in the codebase
6. Implement ONLY that task
7. Run validation command
8. If passes: update `passes: false` → `passes: true`
9. If fails: add guardrail explaining what went wrong
10. Commit with clear message
11. Exit

## Rules

- Do ONE task only
- **Match existing code style**
- **Don't break existing functionality**
- Run lint before committing
- Trust the files, not your memory
```

### 2.2 Smart Validation Commands

Generate validation commands based on project setup:

| Task Type | Validation Template |
|-----------|---------------------|
| New file | `test -f {path} && {lint_cmd} {path}` |
| Bug fix | `{test_cmd} -- --grep "{related_test}"` |
| Feature | `{test_cmd} && {build_cmd}` |
| Refactor | `{test_cmd} && {lint_cmd}` |
| API endpoint | `{test_cmd} -- --grep "{endpoint}"` |

### 2.3 Seeded Guardrails

```markdown
# Guardrails

Project-specific constraints for this codebase.

## Project Rules

{from CONTRIBUTING.md, README.md, or .github/}

## Detected Patterns

- Authentication: {auth_pattern}
- Database: {db_pattern}
- API style: {api_pattern}

## Memory Recall

{relevant learnings from past sessions on this project}

---

Signs learned during this run will be added below:
```

---

## Step 3: Task Decomposition for Brownfield

### Scoping Principles

1. **Investigate First** - Add exploration tasks before implementation
2. **Narrow Scope** - Point to specific files/directories
3. **Validate Incrementally** - Small validatable steps
4. **Preserve Existing** - Don't break what works

### Task Templates by Goal Type

#### Bug Fix

```markdown
### Investigate {bug}
- description: Find root cause of {bug} in {suspected_area}
- validation: `echo "Investigation notes in .ralph/notes.md" && test -f .ralph/notes.md`
- passes: false

### Fix {bug}
- description: Implement fix in {file} based on investigation
- validation: `{test_cmd} -- --grep "{related_test}"`
- passes: false

### Add Regression Test
- description: Add test to prevent {bug} from recurring
- validation: `{test_cmd} -- --grep "{new_test_name}"`
- passes: false
```

#### Feature Addition

```markdown
### Explore Related Code
- description: Understand existing patterns in {related_area}
- validation: `test -f .ralph/exploration.md`
- passes: false

### Add {feature} Tests
- description: Write tests for {feature} before implementing (TDD)
- validation: `{test_cmd} -- --grep "{feature}" || true`  # OK to fail initially
- passes: false

### Implement {feature}
- description: Implement {feature} following patterns from exploration
- validation: `{test_cmd} -- --grep "{feature}"`
- passes: false

### Update Documentation
- description: Update README or docs for {feature}
- validation: `grep -q "{feature}" README.md || grep -q "{feature}" docs/`
- passes: false
```

#### Refactor

```markdown
### Verify Existing Tests Pass
- description: Ensure all tests pass before refactoring
- validation: `{test_cmd}`
- passes: false

### Refactor {target}
- description: Refactor {target} to {goal}
- validation: `{test_cmd} && {lint_cmd}`
- passes: false

### Verify No Regressions
- description: Run full test suite after refactor
- validation: `{test_cmd} && {build_cmd}`
- passes: false
```

---

## Integration with /ralph Command

When `/ralph "goal"` is invoked:

1. **Detect if brownfield** (existing package.json, go.mod, etc.)
2. **If brownfield:**
   - Run codebase analysis
   - Generate context-aware prompt.md
   - Create smart validation commands
   - Seed guardrails from project + memory
3. **If greenfield:**
   - Use standard Ralph setup

### Detection Logic

```bash
is_brownfield() {
  # Check for existing project markers
  [ -f "package.json" ] || \
  [ -f "go.mod" ] || \
  [ -f "pyproject.toml" ] || \
  [ -f "Cargo.toml" ] || \
  [ -f "pom.xml" ] || \
  [ -d "src" ] || \
  [ -d "lib" ]
}
```

---

## Example: Brownfield Bug Fix

**User command:**
```
/ralph "fix login failing after password reset"
```

**Analysis output:**
```
Detected: Next.js 14 + TypeScript + Prisma
Test: npm test (Jest)
Auth: src/lib/auth/ (JWT pattern)
Related files: src/lib/auth/token.ts, src/app/api/auth/
```

**Generated task.md:**
```markdown
# Task: Fix login failing after password reset

Created: 2026-01-22
Max Iterations: 15

## Tasks

### Investigate Auth Flow
- description: Trace password reset → login flow in src/lib/auth/
- validation: `test -f .ralph/investigation.md && grep -q "root cause" .ralph/investigation.md`
- passes: false

### Find Token Invalidation Issue
- description: Check if tokens are properly invalidated after password reset
- validation: `grep -rn "invalidate\|revoke" src/lib/auth/`
- passes: false

### Fix Token Refresh Logic
- description: Update token.ts to invalidate old tokens on password change
- validation: `npm test -- --testNamePattern "token" --passWithNoTests`
- passes: false

### Add Password Reset Login Test
- description: Add test: user can login immediately after password reset
- validation: `npm test -- --testNamePattern "password reset login"`
- passes: false

### Verify Full Auth Flow
- description: Run all auth tests to ensure no regressions
- validation: `npm test -- --testPathPattern "auth"`
- passes: false
```

**Generated guardrails.md:**
```markdown
# Guardrails

Project-specific constraints for this codebase.

## Project Patterns

- Auth logic is in src/lib/auth/
- JWT tokens stored in httpOnly cookies
- Token refresh happens in middleware
- Prisma for database operations

## From Memory

- Previous session: "Token invalidation requires updating both DB and cookie"
- Previous session: "Always test with real Prisma client, not mocks"

---

Signs learned during this run:
```
