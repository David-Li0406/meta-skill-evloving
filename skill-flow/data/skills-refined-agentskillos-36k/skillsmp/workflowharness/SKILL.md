---
name: workflow:harness
description: "WHAT: Ralph Wiggum external harness pattern for autonomous Claude Code loops with spec-based progress tracking. WHEN: implementing multi-step features, refactoring with clear criteria, autonomous development. KEYWORDS: harness, loop, autonomous, Ralph Wiggum, specs, PLAN.md, iterations, acceptance criteria, external bash loop, devorch harness."
---

# Harness Loop (Ralph Wiggum Technique)

**Run Claude Code in an external bash loop for autonomous, iterative development.**

The Harness Loop implements the [Ralph Wiggum technique](https://ghuntley.com/ralph/) for fully autonomous development by running Claude Code in an external bash loop. Each iteration, Claude reads specs, works on tasks, logs progress, and continues until all acceptance criteria are met.

## Overview

**Key benefits:**
- **Autonomous execution:** Claude works through tasks without manual intervention
- **Progress tracking:** Acceptance criteria checkboxes track completion
- **Iteration logs:** Every iteration creates a detailed report
- **Graceful completion:** Loop stops when "## COMPLETED" marker is added to PLAN.md

## Quick Start

```bash
# 1. Initialize a feature folder
devorch harness init my-feature

# 2. Generate specs (Claude investigates and writes detailed specs)
devorch harness create-specs my-feature

# 3. Review and edit PLAN.md to add tasks

# 4. Start the autonomous loop
devorch harness loop my-feature
```

## Available Commands

### `devorch harness init <feature>`

Creates the feature folder structure with templates.

```bash
devorch harness init auth-system
```

**Creates:**
```
devorch/harness/auth-system/
├── PROMPT.md      # Prompt sent to Claude each iteration
├── PLAN.md        # Tasks with acceptance criteria
├── specs/         # For specification files
└── logs/          # Iteration reports
```

### `devorch harness create-specs <feature>`

Boots Claude interactively to investigate the codebase and write detailed specifications.

```bash
devorch harness create-specs auth-system

# Or run in headless mode (no user interaction)
devorch harness create-specs auth-system --headless
```

Claude will:
1. Ask clarifying questions about the feature (interactive mode)
2. Explore the existing codebase structure
3. Identify relevant patterns and conventions
4. Write specification files in `specs/`
5. Update PLAN.md with tasks

### `devorch harness loop <feature>`

Runs Claude in an external bash loop until completion.

```bash
# Basic usage
devorch harness loop auth-system

# With iteration limit
devorch harness loop auth-system --max-iterations 20

# Show all message types (tool calls, etc.)
devorch harness loop auth-system --verbose
```

**Options:**
| Flag | Description |
|------|-------------|
| `--max-iterations N` | Stop after N iterations (default: 20) |
| `--verbose` | Show all message types instead of just assistant/result |

**Loop behavior:**
1. Reads PROMPT.md and sends to Claude
2. Claude works on the first incomplete task
3. Claude creates iteration log in `logs/`
4. Claude updates PLAN.md with progress
5. Loop checks for "## COMPLETED" marker
6. Repeats until complete or max iterations reached

**Stopping the loop:**
- Press `Ctrl+C` to stop gracefully after current iteration
- Add `## COMPLETED` to PLAN.md to signal completion

### `devorch harness list`

Lists all existing features with their status.

```bash
devorch harness list
```

**Output:**
```
Found 3 feature(s):

  [DONE] auth-system
     3 specs, 12 iterations

  [....] payment-flow
     2 specs, 5 iterations

  [    ] new-feature
     no specs, no iterations
```

### `devorch harness status <feature>`

Shows detailed progress for a feature.

```bash
devorch harness status auth-system
```

## Workflow

### 1. Initialize Feature

```bash
devorch harness init my-feature
```

This creates the folder structure and template files.

### 2. Create Specifications

```bash
devorch harness create-specs my-feature
```

When prompted, describe what the feature should do. Claude will investigate your codebase and create detailed specs in the `specs/` folder.

### 3. Define Tasks in PLAN.md

Edit `PLAN.md` to define tasks with acceptance criteria:

```markdown
# Plan: my-feature

## Status: IN_PROGRESS

## Tasks

### Task 1: Create database schema
**Acceptance Criteria:**
- [ ] Add users table with email, password_hash columns
- [ ] Add sessions table with user_id, token, expires_at
- [ ] Create migration file

### Task 2: Implement authentication endpoints
**Acceptance Criteria:**
- [ ] POST /auth/register - create new user
- [ ] POST /auth/login - authenticate and return token
- [ ] POST /auth/logout - invalidate session
- [ ] Add input validation for all endpoints
```

### 4. Run the Loop

```bash
devorch harness loop my-feature
```

Claude will:
1. Read specs and PLAN.md
2. Find the first task with unchecked criteria
3. Work on that task only
4. Create an iteration log
5. Update PLAN.md checkboxes
6. Repeat until all tasks complete

### 5. Monitor Progress

Check progress anytime:

```bash
devorch harness status my-feature
```

Or review iteration logs in `devorch/harness/my-feature/logs/`.

## File Formats

### PROMPT.md

The prompt sent to Claude each iteration. Created at `init` time with context training path baked in.

### PLAN.md

Tracks tasks and progress:

```markdown
# Plan: {{FEATURE_NAME}}

## Status: IN_PROGRESS

## Tasks

### Task 1: [Task Name]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

### Task 2: [Task Name]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

### Iteration Logs

Created in `logs/iteration-NNN.md`:

```markdown
# Iteration 005

**Timestamp:** 2024-01-15T14:30:00Z
**Task:** Task 2 - Implement authentication endpoints
**Status:** COMPLETE

## Changes Made
- `src/routes/auth.ts` - Created - Added login/register/logout endpoints
- `src/middleware/auth.ts` - Created - Token verification middleware

## Approach
Implemented JWT-based authentication following existing patterns in the codebase.

## Verification
- [x] POST /auth/register - create new user: Works, tested with curl
- [x] POST /auth/login - authenticate and return token: Returns valid JWT
- [x] POST /auth/logout - invalidate session: Removes session from DB

## Next Steps
Move to Task 3: Add middleware to protected routes
```

## Best Practices

### Writing Good Acceptance Criteria

- **Be specific:** "Add email validation" → "Validate email format using regex, return 400 for invalid"
- **Be testable:** Each criterion should be verifiable
- **Be atomic:** One thing per criterion
- **Include edge cases:** "Handle duplicate email registration with 409 response"

### Organizing Specs

Number spec files for clear ordering (00-, 01-, etc.):

```
specs/
├── 00-overview.md       # High-level feature description
├── 01-data-model.md     # Database schema, types
├── 02-api-endpoints.md  # REST API specifications
├── 03-business-logic.md # Core logic requirements
└── 99-integration.md    # How components connect (last)
```

### When to Use Harness Loop

**Good fit:**
- Multi-step feature implementation
- Refactoring with clear acceptance criteria
- Bug fixes requiring multiple changes
- Adding tests to existing code

**Not ideal for:**
- Exploratory work without clear specs
- One-off quick fixes
- Tasks requiring human judgment at each step

## Learn More

- **Full Documentation:** [docs/user-guide/harness-loop.md](../../docs/user-guide/harness-loop.md)
- **Ralph Wiggum Technique:** [https://ghuntley.com/ralph/](https://ghuntley.com/ralph/)
