# Breaking Down Projects into Tasks

How to decompose large projects into atomic, manageable tasks.

## The Goal

Each task should be:
- **Completable in one focused session** (30 min - 2 hours of work)
- **Independently testable** (you can verify it works)
- **Clear when done** (no ambiguity about completion)

## Decomposition Strategy

### 1. Start with Outcomes, Not Activities

Bad: "Work on authentication"
Good: "Users can log in with email/password"

Ask: "What will be different when this is done?"

### 2. Find Natural Boundaries

Look for:
- **File boundaries** - one component, one module
- **Feature boundaries** - one user-facing capability
- **Layer boundaries** - API vs UI vs database
- **State boundaries** - before/after a migration

### 3. Make Tasks Atomic

A task is atomic when:
- It can be committed independently
- Rolling it back doesn't break other work
- Another developer could pick it up with minimal context

### 4. Use the "Coffee Test"

If you went for coffee after completing a task, could someone else:
- Understand what you did from the commit?
- Continue from where you left off?
- Test that it works?

If yes, the task is well-scoped.

## Planning Fields

When creating tasks, capture planning context to help future sessions:

### Approach

How you plan to implement. Be specific enough that you (or another agent) can
follow the plan later without re-researching:

```bash
# Bad - too vague
--approach "Add caching"

# Good - actionable
--approach "Use Redis for session cache, 1hr TTL, invalidate on logout"
```

### Acceptance Criteria

What conditions must be true when the task is done. Think "how will I verify
this works?" before starting:

```bash
--criteria "Login returns JWT" "Invalid creds return 401" "Token expires in 24h"
```

### Relevant Files

Which files are involved. Saves time finding them again:

```bash
--files src/routes/auth.ts src/middleware/jwt.ts tests/auth.test.ts
```

### Example: Full Task with Planning

```bash
task.py add "Implement session caching" \
  --description "Speed up authenticated requests by caching sessions" \
  --approach "Use Redis with 1hr TTL, key by session ID, invalidate on logout" \
  --criteria "Cache hit rate > 80%" "Auth latency < 50ms" "Sessions invalidate on logout" \
  --files src/middleware/auth.ts src/services/redis.ts
```

## Common Patterns

### Feature Implementation

```
01-implement-user-login/
  00-index.md           # Parent: Implement user login
  01-add-login-api.md   # Add login API endpoint
  02-create-form.md     # Create login form component
  03-wire-form.md       # Wire form to API
  04-error-handling.md  # Add error handling
  05-write-tests.md     # Write tests
```

### Bug Fix

```
01-fix-checkout-race/
  00-index.md           # Parent: Fix checkout race condition
  01-reproduce-bug.md   # Reproduce and document the bug
  02-write-test.md      # Write failing test
  03-implement-fix.md   # Implement fix
  04-verify-test.md     # Verify test passes
```

### Refactoring

```
01-extract-payments/
  00-index.md           # Parent: Extract payment processing module
  01-identify-code.md   # Identify all payment-related code
  02-create-module.md   # Create new module structure
  03-move-functions.md  # Move functions (no behavior change)
  04-update-imports.md  # Update imports
  05-verify-tests.md    # Verify tests still pass
```

### Research/Spike

```
01-evaluate-caching/
  00-index.md           # Parent: Evaluate caching strategies
  01-baseline.md        # Document current performance baseline
  02-redis-proto.md     # Prototype Redis approach
  03-memory-proto.md    # Prototype in-memory approach
  04-recommend.md       # Compare and recommend
```

## Task Sizing Heuristics

### Too Big (split it)
- "Implement the admin dashboard"
- "Refactor the database layer"
- "Add testing"
- Anything that touches 10+ files
- Anything you can't hold in your head

### Too Small (combine them)
- "Add import statement"
- "Fix typo in comment"
- "Rename variable"
- Pure formatting changes

### Just Right
- "Add pagination to user list API"
- "Create reusable Button component"
- "Migrate user table to add email column"
- "Write tests for auth middleware"

## Dependencies

Use dependencies to encode order:

```bash
task.py add "Create database schema"
task.py add "Implement data access layer" --deps 01-create-database-schema
task.py add "Build API endpoints" --deps 02-implement-data-access-layer
task.py add "Create UI components" --deps 03-build-api-endpoints
```

But prefer independent tasks when possible - they can be worked in parallel and
reduce blocking.

## When Starting a New Project

1. **Write down the end state** - What does "done" look like?
2. **Identify major milestones** - 3-5 big chunks
3. **Break first milestone into tasks** - Don't plan everything upfront
4. **Start working** - Refine as you learn

## Adjusting As You Go

Tasks will change. That's fine.

- **Task too big?** Add subtasks with `--parent`
- **Task unnecessary?** `task.py update <id> --status wont_do`
- **New work discovered?** Add tasks, set dependencies
- **Order wrong?** Update dependencies or use `task.py move`

The task list is a living document, not a contract.

## Example: Building a Newsletter Feature

```bash
# Plan the backend
task.py add "Newsletter signup backend"
task.py add "Create subscribers table migration" --parent 01-newsletter-signup-backend
task.py add "Add Subscriber model and validation" --parent 01-newsletter-signup-backend
task.py add "Build POST /api/subscribe endpoint" --parent 01-newsletter-signup-backend
task.py add "Add email verification flow" --parent 01-newsletter-signup-backend
task.py add "Write API tests" --parent 01-newsletter-signup-backend

# Plan the frontend (depends on API being ready)
task.py add "Newsletter signup frontend" --deps 01-newsletter-signup-backend/03-build-post-apisubscribe-endpoint
task.py add "Create EmailInput component" --parent 02-newsletter-signup-frontend
task.py add "Build SignupForm with validation" --parent 02-newsletter-signup-frontend
task.py add "Wire form to API endpoint" --parent 02-newsletter-signup-frontend
task.py add "Add success/error states" --parent 02-newsletter-signup-frontend
task.py add "Write component tests" --parent 02-newsletter-signup-frontend
```

Result:
```
.claude/tasks/
  01-newsletter-signup-backend/
    00-index.md
    01-create-subscribers-table-migration.md
    02-add-subscriber-model-and-validation.md
    03-build-post-apisubscribe-endpoint.md
    04-add-email-verification-flow.md
    05-write-api-tests.md
  02-newsletter-signup-frontend/
    00-index.md
    01-create-emailinput-component.md
    02-build-signupform-with-validation.md
    03-wire-form-to-api-endpoint.md
    04-add-successerror-states.md
    05-write-component-tests.md
```

### Session Walkthrough

```bash
# Start working - depth-first on backend
task.py next                              # Returns 01-newsletter-signup-backend/01-create-subscribers-table-migration
task.py start 01-newsletter-signup-backend
task.py start 01-newsletter-signup-backend/01-create-subscribers-table-migration
# ... do the work ...
task.py done
task.py next                              # Returns 01-.../02-add-subscriber-model

# After completing the API endpoint, frontend is unblocked
task.py done 01-newsletter-signup-backend/03-build-post-apisubscribe-endpoint
# Frontend still blocked until backend parent is done

# Complete backend
task.py done 01-newsletter-signup-backend/04-add-email-verification-flow
task.py done 01-newsletter-signup-backend/05-write-api-tests
task.py done 01-newsletter-signup-backend
task.py next                              # Returns 02-newsletter-signup-frontend/01-...
```

### Why This Structure Works

- **Backend tasks are sequential** - each builds on the previous
- **Frontend depends on API existing** - can't wire to endpoint that doesn't exist
- **Subtasks are atomic** - each is one commit, one test
- **Parent tasks group related work** - easy to see progress on "backend" vs "frontend"
- **Depth-first completion** - finish what you started before context-switching
