---
name: beads
description: Use Beads to structure and execute work via epics, tasks, and dependencies
license: MIT
compatibility: opencode
metadata:
  audience: coders
---

## Purpose

Beads (`bd`) is my **external working memory** - a temporal graph that survives session restarts.

I treat Beads as the single source of truth for:
- what work exists
- what blocks what
- what is allowed to be worked on next
- **context and decisions** (via descriptions and comments)

The plan lives as **data**, not prose. I query instead of remember.

---

## ⚠️ CRITICAL: Hierarchical IDs

I use hierarchical IDs to organize **related** work. The prefix is project-specific (e.g., `opencode`, `myapp`).

**Independent work streams get their own top-level IDs:**
```
opencode-a1b2      (Epic: User Management)
opencode-a1b2.1    (Task: Registration)
opencode-a1b2.1.1  (Subtask: Email validation)
opencode-a1b2.2    (Task: Profile editing)

opencode-c3d4      (Epic: TUI System)
opencode-c3d4.1    (Task: Layout engine)
opencode-c3d4.2    (Task: Key bindings)
opencode-c3d4.3    (Task: Theme support)
```

**To get the ID of a top-level issue:**
```bash
# When creating - capture the ID
bd create "User Management" -t epic -p 0 --silent   # outputs: opencode-a1b2
bd q "Quick task title"                              # outputs: opencode-x7y8

# In a new session - find existing issues
bd list -t epic                        # list all epics
bd list --title "User"                 # filter by title
bd search "User Management"            # search across title/description/ID
bd search "User" -t epic --json        # JSON output for parsing
```

**When to use top-level epics/tasks:**
- Independent features (User Management vs TUI vs CLI)
- Unrelated bug fixes
- Work that doesn't belong under any existing task

**When to use hierarchy (children):**
- Subtasks that break down a larger task
- Work discovered while implementing a parent task
- Features with multiple implementation steps

---

## Concepts

### Epics

High-level goals. I create them but never work on them directly. **Always include a description with context, constraints, and acceptance criteria.**

```bash
bd create "User Management" -t epic -p 0 -d "Complete user auth system with registration, login, and profile management. Must support OAuth providers."
```

### Tasks

Concrete, executable units of work. Tasks are the only issues I actively work on.

Good tasks:
- fit in one work session
- produce a clear result
- unblock other tasks

**Top-level tasks (independent work):**
```bash
bd create "CLI argument parsing" -p 1 -d "Parse --config, --verbose, --output flags using cobra"
bd create "TUI layout engine" -p 1 -d "Flexbox-style layout system for terminal UI components"
bd create "Config file loading" -p 2 -d "Load YAML/JSON config from ~/.config/app/"
```

**Child tasks (related to a parent):**
```bash
bd create "User registration flow" -p 1 --parent opencode-a3f8 -d "Email/password registration with validation"
bd create "Profile editing page" -p 1 --parent opencode-a3f8 -d "Allow users to update name, avatar, preferences"
bd create "Email validation" -p 2 --parent opencode-a3f8.1 -d "Send verification email with token, validate on click"
```

Using `--parent` automatically assigns hierarchical IDs (e.g., `opencode-a3f8.1`, `opencode-a3f8.2`).

### Descriptions and Comments

**Description** (`-d`): Initial context when creating an issue.

```bash
bd create "User auth system" -t epic -p 0 -d "Implement full authentication flow including OAuth"
```

**Comments**: Ongoing updates, rules, progress notes. Use for:
- Adding rules/constraints to epics
- Progress updates
- Implementation notes
- Decisions made during work

```bash
bd comment opencode-a3f8 "Rules for this epic:
1. All tasks must have unit tests
2. No task should take more than 4 hours"

bd comment opencode-a3f8.1 "Decided to use JWT tokens instead of sessions"

bd comments opencode-a3f8           # list all comments
bd comments opencode-a3f8 --json    # JSON output (returns array)
```

`bd show` displays both description and comments.

### Dependencies

Edges that define execution order. Four types:

| Type | Meaning |
|------|---------|
| **blocks** | Task A must complete before Task B starts |
| **related** | Tasks are conceptually linked |
| **parent-child** | Hierarchical organization (via `--parent`) |
| **discovered-from** | Task found while working on another |

```bash
bd dep add opencode-a3f8.2 opencode-a3f8.1  # opencode-a3f8.2 blocked by opencode-a3f8.1
```

Note: Children already depend on their parent via hierarchy. Don't add explicit `discovered-from` to children - it will error.

Example graph:
```
opencode-a3f8 (Epic: User Management)
    ├── opencode-a3f8.1 (Task: Registration)
    │       ↓ blocks
    │   opencode-a3f8.2 (Task: Profile editing)
    │
    └── opencode-a3f8.1.1 (Subtask: Email validation)
            (inherits dependency from parent)
```

### Graph-Based Structure

- nodes = epics and tasks
- edges = blocking relationships
- order comes only from dependencies
- priority affects choice among ready work, not execution order

If order matters, it must be encoded as a dependency.

---

## Execution Loop

### 1. Start Session - Get Ready Work

```bash
bd ready --json
```

Returns tasks that are open and have no unmet dependencies. **Only these are allowed to be worked on.**

### 2. Claim a Task

**⚠️ MANDATORY: Always read the task with `bd show` BEFORE starting work. Read the description AND all comments - they contain critical context, decisions, and constraints.**

```bash
bd show opencode-a3f8.1                    # READ THIS FIRST - description + comments!
bd update opencode-a3f8.1 -s in_progress
```

### 3. Implement and Commit Code

Add comments to record important decisions and progress:
```bash
bd comment opencode-a3f8.1 "Using bcrypt for password hashing, cost factor 12"
bd comment opencode-a3f8.1 "Decided against OAuth in this task - will be separate"
```

### 4. Handle Discovered Work

If I discover new work while implementing, I file it **immediately**:

**As a subtask (child inherits dependency automatically):**
```bash
bd create "Fix token refresh bug" -p 1 --parent opencode-a3f8.1 -d "Token expires but refresh fails silently - found during registration testing"
# Creates opencode-a3f8.1.2 - automatically depends on parent
```

**As a separate task with discovered-from link:**
```bash
bd create "Unrelated auth bug found" -p 1 --deps "discovered-from:opencode-a3f8.1" -d "Session cookie not set correctly on Safari - unrelated to registration"
# For work that doesn't belong under the current task's hierarchy
```

Note: Children already inherit dependency from parent via hierarchy. Use `discovered-from` only for work that belongs elsewhere in the graph but was found while working on something.

The `discovered-from` edge preserves causal history - how work unfolded over time. This is critical for maintaining context across sessions.

### 5. Close the Task

```bash
bd close opencode-a3f8.1 -r "Completed registration flow"
```

Closing may unblock other tasks. Use `--suggest-next` to see newly unblocked work.

---

## JSON Output

All `--json` outputs return **arrays**, even for single items:

```bash
bd show opencode-a3f8.1 --json      # returns [{ ... }] not { ... }
bd update opencode-a3f8.1 -s in_progress --json  # returns [{ ... }]
bd list --json
bd ready --json
bd search "query" --json
bd close opencode-a3f8.1 -r "done" --json
```

When parsing with `jq`, use `.[0]` to get the first element:
```bash
bd show opencode-a3f8.1 --json | jq '.[0].title'    # correct
bd show opencode-a3f8.1 --json | jq '.title'        # WRONG - will error
```

---

## Batch Operations

When making multiple changes, batch within 30 seconds:

```bash
bd create "Fix validation bug" -p 1 --parent opencode-a3f8 -d "Form validation fails on special characters"
bd create "Add unit tests" -p 2 --parent opencode-a3f8 -d "Cover registration and login flows"
bd update opencode-a3f8.1 -s in_progress
```

---

## Compaction

For large projects, summarize old closed issues:

```bash
bd compact --analyze --json   # Get candidates for review
bd compact --prune            # Remove expired tombstones
```

This implements **"agentic memory decay"** - replacing detailed content with concise summaries.

---

## Rules

1. I only work on tasks, never epics
2. I use hierarchical IDs for related work, top-level IDs for independent work
3. I always respect dependencies
4. I never infer order from names or priority - order comes from edges
5. I always close tasks explicitly with `-r` reason
6. I NEVER drop discovered work - file immediately (as child or with `discovered-from`)
7. I always start sessions with `bd ready --json`
8. **I ALWAYS run `bd show` and READ description + comments before starting any task**
9. I always add descriptions (`-d`) when creating issues
10. I record decisions and context as comments during work

**Beads is used to execute work deterministically, not to improvise.**

---

## Why This Matters

Beads solves **session amnesia**. Without it:
- I forget discovered work after compaction/restart
- I re-discover the same tasks repeatedly
- I declare victory at phase 3-of-6 because that's all I can "see"

With Beads:
- I query the plan instead of carrying it in context
- `discovered-from` chains preserve how work unfolded over time
- I can resume any session by running `bd ready --json`
- Descriptions and comments preserve context and decisions for future sessions

---

## ⛔ NEVER DO THIS

**NEVER run `git push`, `git commit`, or any git commands.**

Git operations are handled by the human or by other tools. This skill is ONLY for managing work via `bd` commands. Do not touch git.
