# Clorch → Ralph Handoff Protocol

Clorch does deep analysis, Ralph executes with fresh context.

## Phase 1: Codebase Analysis (Clorch)

When `/ralph "goal"` is invoked on an existing codebase:

### 1.1 Quick Detection

```bash
# Is this brownfield?
[ -f "package.json" ] || [ -f "go.mod" ] || [ -f "pyproject.toml" ] || [ -d "src" ]
```

### 1.2 Deep Analysis (Use Clorch Tools)

**Structure Analysis:**
```bash
# Use tldr for fast structure mapping
tldr tree . --ext .ts,.tsx,.js,.jsx,.py,.go
tldr structure . --lang typescript  # or python, go, etc.
```

**Pattern Detection:**
```bash
# Find auth patterns
tldr search "auth|jwt|session|login" src/

# Find test patterns
tldr search "describe|test|it\(" tests/ __tests__/

# Find API patterns
tldr search "router|endpoint|handler" src/
```

**Memory Recall:**
```bash
# Get past learnings about this project
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/recall_learnings.py \
  --query "{project_name} {goal_keywords}" --k 5
```

### 1.3 Goal-Specific Exploration

Use scout agent to find code related to the goal:

```
Task(subagent_type="scout", prompt="
  Find all code related to: {goal}

  Look for:
  - Functions/methods handling this
  - Test files for this area
  - Related configuration
  - Database models involved

  Return: file paths, key functions, patterns used
")
```

### 1.4 Generate Project Context

Create comprehensive `.ralph/project-context.md`:

```markdown
# Project Context for Ralph

## Stack
- Framework: {from analysis}
- Language: {detected}
- Database: {detected ORM/driver}
- Auth: {detected pattern}

## Commands
- Test: `{actual command from package.json}`
- Test specific: `{command} -- --grep "{pattern}"`
- Lint: `{actual lint command}`
- Build: `{actual build command}`
- Typecheck: `{if exists}`

## Key Directories
{from tldr tree}

## Files Related to Goal
{from scout exploration}
- `src/lib/auth/token.ts` - JWT token handling
- `src/app/api/auth/route.ts` - Auth API routes
- `tests/auth.test.ts` - Auth tests

## Patterns Detected
- Auth: JWT with httpOnly cookies
- API: Next.js App Router
- Database: Prisma with PostgreSQL
- State: Zustand for client state

## From Memory
{recalled learnings about this project}

## Guardrail Seeds
{patterns that should become guardrails}
- Always run migrations before schema changes
- Auth tokens stored in httpOnly cookies only
- Use transaction for multi-table operations
```

---

## Phase 2: Task Generation (Clorch)

### 2.1 Smart Decomposition

Based on analysis, create tasks that:
- Reference specific files discovered
- Use actual test commands
- Include investigation steps for bugs
- Follow project patterns

### 2.2 Task Template with Context

```markdown
### {Task Name}
- description: {what to do} in `{specific_file}`
- context: {relevant patterns from analysis}
- validation: `{actual_test_command} -- --grep "{pattern}"`
- passes: false
```

### 2.3 Example: Bug Fix Tasks

```markdown
# Task: Fix login failing after password reset

Created: 2026-01-22
Max Iterations: 15
Project: my-app (Next.js + Prisma)

## Context (from Clorch analysis)
- Auth logic: src/lib/auth/
- Token handling: src/lib/auth/token.ts (JWT, refreshToken function)
- Tests: tests/auth.test.ts (12 existing tests)
- Pattern: Tokens stored in httpOnly cookies, refreshed via middleware

## Tasks

### Investigate Token Invalidation
- description: Check if tokens are invalidated on password change in `src/lib/auth/token.ts`
- context: Look at `refreshToken()` and `invalidateTokens()` functions
- validation: `echo "See .ralph/investigation.md" && test -f .ralph/investigation.md`
- passes: false

### Fix Token Refresh Logic
- description: Update `refreshToken()` in `src/lib/auth/token.ts` to check password change timestamp
- context: User model has `passwordChangedAt` field (from Prisma schema)
- validation: `npm test -- --testNamePattern "token refresh"`
- passes: false

### Add Regression Test
- description: Add test case in `tests/auth.test.ts` for login after password reset
- context: Follow existing test patterns (see test file for style)
- validation: `npm test -- --testNamePattern "login after password reset"`
- passes: false

### Verify Full Auth Suite
- description: Run all auth tests to ensure no regressions
- validation: `npm test -- --testPathPattern "auth"`
- passes: false
```

---

## Phase 3: Prompt Generation (Clorch)

### 3.1 Context-Rich prompt.md

```markdown
# Ralph Agent

You are a fresh Ralph agent. Your context is clean but you have project knowledge below.

## Project Context

{paste from project-context.md}

## Your Current Task

1. Read `.ralph/guardrails.md` FIRST
2. Read `.ralph/task.md` for current task
3. Find FIRST task where `passes: false`
4. Read the `context` field for that task
5. Implement ONLY that task
6. Run validation
7. Update passes flag
8. Commit and exit

## Rules

- Do ONE task only
- Follow patterns described in project context
- Match existing code style
- Don't break existing tests
- Trust the files, not your memory
```

---

## Phase 4: Guardrails (Clorch Seeds)

### 4.1 Seed from Analysis

```markdown
# Guardrails

## Project Patterns (from Clorch analysis)

### Pattern: Auth Token Storage
- Trigger: Working with auth tokens
- Rule: Tokens go in httpOnly cookies only, never localStorage
- Source: Detected in src/lib/auth/token.ts

### Pattern: Database Transactions
- Trigger: Multi-table operations
- Rule: Wrap in Prisma transaction
- Source: Pattern found in src/lib/db/

### Pattern: API Error Handling
- Trigger: API route errors
- Rule: Use NextResponse.json({ error }, { status })
- Source: Consistent pattern in src/app/api/

## From Memory

{any recalled learnings}

---

## Signs Learned This Run

(Ralph adds here during execution)
```

---

## Handoff Checklist

Before handing off to Ralph loop:

- [ ] Project context generated (.ralph/project-context.md)
- [ ] Tasks decomposed with specific file paths
- [ ] Validation commands use actual test setup
- [ ] Guardrails seeded from patterns + memory
- [ ] prompt.md includes project context
- [ ] Loop script ready (ralph-loop-host.sh)

---

## Example Clorch Workflow

```
User: /ralph "add rate limiting to API"

Clorch:
1. Detect brownfield (package.json exists)
2. Run: tldr structure src/ --lang typescript
3. Run: tldr search "middleware|rateLimit" src/
4. Spawn: scout agent to find API patterns
5. Recall: memory for rate limiting learnings
6. Generate: project-context.md with findings
7. Create: task.md with smart tasks
8. Seed: guardrails.md with patterns
9. Output: "Ready! Run ralph-loop-host.sh 20"

User: (in separate terminal)
~/.claude/ralph-docker/ralph-loop-host.sh 20

Fresh Claude instances:
- Read project context (pre-analyzed)
- Execute one task each
- Have full understanding without analysis cost
```
