---
name: beads
description: |
  Manage beads issues for tracking development work. Use this skill when: (1) Starting a new task or feature, (2) Creating implementation or testing plans, (3) Tracking session progress and discoveries, (4) Finding available work, (5) Closing completed work. Beads stores issues in git-tracked JSONL with rich fields for design notes, acceptance criteria, and session notes.
---

# Beads Issue Management

## Core Principle

**All work must be tracked in beads.** Before starting any task:
1. Check for existing issue: `bd ready` or `bd list --status=open`
2. Create issue if none exists
3. Claim work: `bd update <id> --status=in_progress`

## Rich Context Fields

Store implementation plans, testing criteria, and session notes directly in issues:

| Field | Flag | Purpose |
|-------|------|---------|
| `--design` | Design notes | Implementation plans, architecture decisions |
| `--acceptance` | Acceptance criteria | Testing plans, definition of done |
| `--notes` | Additional notes | Session discoveries, to-dos, context |
| `--description` | Full description | Problem statement, background |

## Creating Issues

```bash
# Feature with full context
bd create --title="Add user authentication" \
  --type=feature \
  --priority=2 \
  --description="Users need secure login/logout functionality" \
  --design="## Implementation Plan
1. Add JWT middleware to FastAPI
2. Create /auth/login and /auth/register endpoints
3. Add AuthContext to React frontend
4. Implement protected route wrapper" \
  --acceptance="## Definition of Done
- [ ] Unit tests for JWT validation
- [ ] Integration tests for auth endpoints
- [ ] E2E test for login flow
- [ ] Password hashing with bcrypt" \
  --notes="## Context
- Decision: JWT over OAuth for simplicity
- Token expiry: 24h with refresh tokens"
```

**Issue types:** `task`, `bug`, `feature`, `epic`
**Priorities:** 0-4 or P0-P4 (0=critical, 2=medium, 4=backlog)

## Required Fields by Issue Type

### Features (--type=feature)
Features **MUST** include:
- `--design`: Implementation plan with numbered steps
- `--acceptance`: Definition of done with testable criteria

### Bugs (--type=bug)
Bugs **MUST** include:
- `--description`: Steps to reproduce the bug
- `--acceptance`: How to verify the fix works

### Tasks (--type=task)
Tasks **SHOULD** include:
- `--description`: Clear scope of work

### Example: Well-Formed Feature

```bash
bd create --title="Add recipe rating system" \
  --type=feature \
  --priority=2 \
  --description="Users need to rate recipes 1-5 stars for recommendations" \
  --design="## Implementation Plan
1. Add rating column to recipes table (migration)
2. Create POST /api/recipes/{id}/rate endpoint
3. Add RatingStars component to RecipeDetail page
4. Update RecipeCard to show average rating
5. Add rating filter to recipe list" \
  --acceptance="## Definition of Done
- [ ] Database migration passes
- [ ] API endpoint validates 1-5 range
- [ ] Frontend shows clickable stars
- [ ] Average updates on new rating
- [ ] Unit tests for rating calculation"
```

## Session Workflow

### Starting Work
```bash
bd ready                              # Find available work
bd show <id>                          # Review issue details
bd update <id> --status=in_progress   # Claim it
```

### During Development
Update notes as you discover things:
```bash
bd update <id> --notes="## Session $(date +%Y-%m-%d)
- Found edge case: empty responses cause 500
- Decision: return empty array instead of null
- TODO: add input validation for edge cases"
```

### Completing Work
```bash
bd close <id> --reason="Implemented JWT auth with refresh tokens.
Tests: 15 unit, 4 integration, all passing.
See design notes for architecture decisions."
```

### MANDATORY: Commit After Closure

**Every `bd close` MUST be immediately followed by a git commit:**

```bash
bd close <id> --reason="Implemented feature X with tests"

# IMMEDIATELY after bd close:
git add .
git commit -m "feat(scope): implement feature X

Closes: <id>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

**Why this matters:**
- Bead closures modify `.beads/issues.jsonl`
- Without commit, closure exists only in local database
- Team members won't see status changes until committed
- Risk of data loss if local state is lost

**Rule: One closure = One commit. Never batch closures.**

## Common Commands

| Command | Purpose |
|---------|---------|
| `bd ready` | Show issues ready to work (no blockers) |
| `bd list --status=open` | All open issues |
| `bd show <id> --json` | Full issue details as JSON |
| `bd update <id> --status=in_progress` | Claim work |
| `bd close <id>` | Mark complete |
| `bd close <id1> <id2>` | Close multiple at once |
| `bd dep add <child> <blocker>` | Add dependency |
| `bd stats` | Project statistics |
| `bd sync --from-main` | Pull beads updates from main |

## Dependencies

Link related issues:
```bash
bd create --title="Implement feature X" --type=feature
bd create --title="Write tests for X" --type=task
bd dep add <test-id> <feature-id>  # Tests blocked by feature
```

## TDD Workflow (RED-GREEN-REVIEW)

When working on **features** or **bugs**, follow this TDD workflow. Documentation and config changes may skip to completion.

### RED Phase (Test First)

1. **Read the issue's `--acceptance` criteria** - This IS your test plan
2. **Write failing tests** that implement those criteria
3. **Verify tests fail for the right reason** - Missing implementation, not syntax errors

```bash
# Backend
cd backend && pytest tests/path/to/new_tests.py -v

# Frontend
cd frontend && npm test -- --run path/to/new.test.ts
```

### GREEN Phase (Implementation)

1. **Write minimal code** to make tests pass
2. **Run tests continuously** - Don't batch test runs
3. **All tests must pass** before proceeding (new + existing)

### REVIEW Phase (Before Closing)

Spawn a review agent to verify:
- Implementation matches `--design` field
- All `--acceptance` criteria satisfied
- No scope creep (unplanned features)
- Tests are meaningful, not just for coverage

```
Task tool with subagent_type="general-purpose":
"Review changes for bead <id>. Verify:
1. Implementation matches --design
2. All --acceptance criteria satisfied
3. Code follows project conventions"
```

### Documenting Test Results

When closing, document what was tested:

```bash
bd close <id> --reason="Implemented recipe rating system.
Tests: 8 unit (rating calc, validation), 2 integration (API endpoints).
All passing. Edge cases: 0 ratings, max ratings handled."
```

---

## Session Close Protocol

Before ending a session:
```bash
git status                    # Check changes
git add <files>               # Stage code
bd sync --from-main           # Pull beads updates
git commit -m "..."           # Commit changes
```
