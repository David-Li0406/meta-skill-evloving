# Ralph-Ready Bead Specification

This document defines the bead format for god-ralph execution.

## Standard Bead Fields

These are the core beads fields:

```yaml
id: beads-abc123          # Auto-generated
title: "Add user API"     # Required, clear and actionable
description: |            # Required, detailed
  Implement GET /api/users endpoint that returns
  paginated user list with filtering support.
type: feature             # feature, task, bug, epic
priority: 2               # 0-4 (0=critical, 4=backlog)
status: open              # open, in_progress, blocked, closed
assignee: null            # Optional, username
```

## Ralph-Specific Fields (ralph_spec)

These fields tell Ralph how to execute the bead.

### completion_promise
String that Ralph outputs when truly complete.

```yaml
completion_promise: "BEAD COMPLETE"
```

Ralph outputs: `<promise>BEAD COMPLETE</promise>`

**Rules:**
- Only output when ALL acceptance criteria met
- Never lie to escape the loop
- Case-sensitive exact match

### max_iterations
Safety limit for iterations.

```yaml
max_iterations: 50
```

**Guidelines:**
- Simple task: 20
- Medium task: 50 (default)
- Complex task: 100

### acceptance_criteria
List of checks that must pass for completion.

```yaml
acceptance_criteria:
  - type: test
    command: "npm test -- --grep 'users'"
  - type: lint
    command: "npm run lint"
  - type: build
    command: "npm run build"
```

## Acceptance Criteria Types

### test
Run a test command, check exit code.

```yaml
- type: test
  command: "npm test"
```

### lint
Run linter, no errors allowed.

```yaml
- type: lint
  command: "npm run lint"
```

### build
Run build, must succeed.

```yaml
- type: build
  command: "npm run build"
```

### api
Check API endpoint response.

```yaml
- type: api
  check: "GET /api/users returns 200"
  preview_url: true  # Use Vercel/Railway preview
```

### ui
Visual verification via Chrome extension.

```yaml
- type: ui
  check: "Settings page renders form with 3 fields"
  using: chrome_extension
```

### manual
Requires human verification.

```yaml
- type: manual
  check: "Design matches Figma mockup"
```

## Complete Example

```yaml
title: "Add user settings API endpoint"
description: |
  Implement GET and POST /api/settings endpoints.

  GET: Return user's current settings
  POST: Update settings with validation

  Settings schema:
  - theme: "light" | "dark"
  - notifications: boolean
  - language: string (ISO 639-1)
type: feature
priority: 2

ralph_spec:
  completion_promise: "SETTINGS API COMPLETE"
  max_iterations: 30
  acceptance_criteria:
    - type: test
      command: "npm test -- --grep 'settings'"
    - type: lint
      command: "npm run lint src/api/settings.ts"
    - type: api
      check: "GET /api/settings returns valid JSON"
      preview_url: true
    - type: build
      command: "npm run build"
```

## Storing ralph_spec

Until beads schema is extended, store ralph_spec in comments:

```bash
bd comments beads-abc --add "ralph_spec:
completion_promise: BEAD COMPLETE
max_iterations: 50
acceptance_criteria:
  - type: test
    command: npm test"
```

## Granularity Guidelines

### Too Large
```yaml
title: "Implement user authentication system"
# Too many moving parts, unclear completion
```

### Just Right
```yaml
title: "Add JWT token validation middleware"
# Focused, clear acceptance criteria
```

### Too Small
```yaml
title: "Fix typo in error message"
# Trivial, not worth Ralph overhead
```

## Dependency Patterns

### Sequential Chain
```
Database Schema (beads-001)
    ↓
API Endpoints (beads-002) [depends on beads-001]
    ↓
Frontend UI (beads-003) [depends on beads-002]
```

### Fan-out
```
Core Library (beads-001)
    ↓
├── Service A (beads-002) [depends on beads-001]
├── Service B (beads-003) [depends on beads-001]
└── Service C (beads-004) [depends on beads-001]
```

### Epic Pattern
```
Feature Epic (beads-001) [type: epic]
    │
    ├── Task 1 (beads-002)
    ├── Task 2 (beads-003)
    └── Task 3 (beads-004)
    │
Epic depends on all tasks (reversed from normal)
```

## Canonical Bead-Farmer Invocation

This section defines the standardized patterns for invoking bead-farmer from different agents in the god-ralph ecosystem.

**Key principle:** All bead-farmer invocations use `worktree_policy="none"` because bead-farmer operates on the main repository, not in worktrees.

### From Ralph Worker (Discovered Issue)

When a Ralph worker discovers a bug or issue unrelated to its current task, it should file it via bead-farmer and continue working.

```python
Task(
    subagent_type="bead-farmer",
    description="Create bead for discovered bug",
    prompt="""
Validate and create a bead for this discovered issue:

BUG: [description]

Location: [file:line]
Discovered while working on [current-bead-id].

[error details or stack trace]

Expected: [expected behavior]
Actual: [actual behavior]

Check for duplicates and recent fixes before creating.
This is non-blocking - Ralph is continuing its work.
    """
)
```

**Example:**
```python
Task(
    subagent_type="bead-farmer",
    description="Create bead for N+1 query issue",
    prompt="""
Validate and create a bead for this discovered issue:

BUG: N+1 query in User model causing slow page loads

Location: src/models/User.ts:47
Discovered while working on beads-settings-api.

When fetching users with their posts, each post triggers
a separate query for the author.

Expected: Single query with JOIN
Actual: N+1 queries (visible in debug logs)

Check for duplicates and recent fixes before creating.
This is non-blocking - Ralph is continuing its work.
    """
)
```

### From Orchestrator (Merge Conflict)

When the orchestrator encounters a merge conflict while integrating a Ralph worker's changes, it creates a fix-bead.

```python
Task(
    subagent_type="bead-farmer",
    description="Create fix-bead for merge conflict",
    prompt="""
Create a fix-bead for this merge conflict:

Merge conflict while merging branch ralph/[bead-id] to main.

Conflicting files:
- [file1]
- [file2]

Original bead: [bead-id] '[title]'

Create a high-priority (P0) bug bead to resolve this conflict.
Link it as a dependency of the original bead.
    """
)
```

**Example:**
```python
Task(
    subagent_type="bead-farmer",
    description="Create fix-bead for merge conflict",
    prompt="""
Create a fix-bead for this merge conflict:

Merge conflict while merging branch ralph/beads-user-api to main.

Conflicting files:
- src/routes/index.ts
- src/middleware/auth.ts

Original bead: beads-user-api 'Add user API endpoint'

Create a high-priority (P0) bug bead to resolve this conflict.
Link it as a dependency of the original bead.
    """
)
```

### From Verification Agent (Test Failure)

When post-merge verification fails, the verification agent creates a fix-bead to address the regression.

```python
Task(
    subagent_type="bead-farmer",
    description="Create fix-bead for verification failure",
    prompt="""
Create a fix-bead for this verification failure:

Verification failed after merging [bead-id].

Failed criteria:
- [criterion description]

Stack trace:
[stack trace]

Suggested fix: [suggestion]

Create a P0 bug bead and link to [original-bead-id].
    """
)
```

**Example:**
```python
Task(
    subagent_type="bead-farmer",
    description="Create fix-bead for verification failure",
    prompt="""
Create a fix-bead for this verification failure:

Verification failed after merging beads-settings-api.

Failed criteria:
- type: test
  command: "npm test"
  exit_code: 1

Stack trace:
FAIL src/api/settings.test.ts
  Settings API
    ✓ GET /api/settings returns 200
    ✗ POST /api/settings validates input
      TypeError: Cannot read property 'validate' of undefined
        at SettingsController.update (src/api/settings.ts:34)

Suggested fix: Import SettingsSchema at top of settings.ts

Create a P0 bug bead and link to beads-settings-api.
    """
)
```

### Invocation Guidelines

| Scenario | Priority | Blocking? | Dependencies |
|----------|----------|-----------|--------------|
| Discovered bug (unrelated) | P2-P3 | No | None |
| Discovered bug (blocks current) | P1 | Yes | Current bead |
| Merge conflict | P0 | Yes | Original bead |
| Verification failure | P0 | Yes | Original bead |

**Best practices:**
1. Provide clear context about where the issue was discovered
2. Include relevant file paths and line numbers
3. For bugs, include expected vs actual behavior
4. For failures, include stack traces when available
5. Let bead-farmer handle deduplication - don't skip filing
