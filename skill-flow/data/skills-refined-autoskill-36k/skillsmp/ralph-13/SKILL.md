---
name: ralph
description: Convert PRDs to prd.json format for the Ralph autonomous agent system. Use when you have an existing PRD and need to convert it to Ralph's JSON format.
---

# Ralph PRD Converter

Converts existing PRDs to the prd.json format that Ralph uses for autonomous execution.

---

## The Job

Take a PRD (markdown file or text) and convert it to `prd.json`.

**ALWAYS save to the global Ralph projects directory — never ask the user where to save.**

### Auto-detect Project Directory

1. Get project directory:
   ```bash
   ralph project-dir
   ```

2. Save `prd.json` to: `$(ralph project-dir)/prd.json`

---

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "[detected-prefix]/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "userStories": [
    {
      "id": "[TICKET-0000 or US-001]",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**Note:** Branch prefix and ticket IDs are detected from project conventions. See "Ticket Convention Detection" and "Branch Convention Detection" sections below.

---

## Story Size: The Number One Rule

**Each story must be completable in ONE Ralph iteration (one context window).**

Ralph spawns a fresh Claude Code instance per iteration with no memory of previous work. If a story is too big, the LLM runs out of context before finishing and produces broken code.

### Right-sized stories:

- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):

- "Build the entire dashboard" - Split into: schema, queries, UI components, filters
- "Add authentication" - Split into: schema, middleware, login UI, session handling
- "Refactor the API" - Split into one story per endpoint or pattern

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must not depend on later ones.

**Correct order:**

1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**

1. UI component (depends on schema that does not exist yet)
2. Schema change

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something Ralph can CHECK, not something vague.

### Good criteria (verifiable):

- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "Typecheck passes"
- "Tests pass"

### Bad criteria (vague):

- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include as final criterion:

```
"Typecheck passes"
```

For stories with testable logic, also include:

```
"Tests pass"
```

### For stories that change UI, also include:

```
"Verify in browser using dev-browser skill"
```

Frontend stories are NOT complete until visually verified. Ralph will use the dev-browser skill to navigate to the page, interact with the UI, and confirm changes work.

---

## Ticket Convention Detection

Before assigning story IDs, detect the project's existing ticket convention from git history:

```bash
# Run in the target project directory to find ticket patterns
git log --oneline -50 | grep -oE '[A-Z]{2,10}-[0-9]+' | cut -d'-' -f1 | sort | uniq -c | sort -rn | head -1
```

This returns the most common ticket prefix with its count. Example output: `31 CI` means "CI" prefix was found 31 times → use `CI-0000`.

**Rules:**

1. If a prefix is found (e.g., "CI", "JIRA", "PROJ"):
   - Use that prefix + "0000" for ALL stories: `CI-0000`, `JIRA-0000`
   - All stories share the same placeholder ID (no real ticket assigned)

2. If NO ticket convention is found:
   - Use sequential IDs: `US-001`, `US-002`, etc.

**Examples of detected patterns:**

- `feat: CI-1234 - Something` → prefix is `CI` → use `CI-0000`
- `fix: JIRA-567 Something` → prefix is `JIRA` → use `JIRA-0000`
- `[PROJ-890] Something` → prefix is `PROJ` → use `PROJ-0000`
- No pattern found → use `US-001`, `US-002`, etc.

---

## Branch Convention Detection

Before setting the branch name, detect the project's existing branch naming convention:

```bash
# Run in the target project directory to find branch prefixes
git branch -a | grep -oE '(feature|feat|fix|bugfix|hotfix|release|chore)/' | sort | uniq -c | sort -rn | head -1
```

This returns the most common branch prefix with its count. Example output: `150 feat/` means "feat/" prefix was found 150 times → use `feat/`.

**Rules:**

1. If a branch prefix is found (e.g., `feature/`, `feat/`, `fix/`):
   - Use that prefix instead of `ralph/`
   - Example: `feature/task-status` instead of `ralph/task-status`

2. If NO branch convention is found:
   - Use `ralph/` prefix: `ralph/feature-name`

**Common prefixes to detect:**

- `feature/`
- `feat/`
- `fix/`
- `bugfix/`
- `hotfix/`
- `release/`
- `chore/`

**Examples:**

- Project has `feature/add-login`, `feature/user-profile` → use `feature/task-status`
- Project has `feat/api-v2`, `feat/dashboard` → use `feat/task-status`
- Project has no convention → use `ralph/task-status`

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Based on detected ticket convention (see Ticket Convention Detection)
   - With convention: All stories get `PREFIX-0000` (e.g., `CI-0000`)
   - Without convention: Sequential `US-001`, `US-002`, etc.
3. **Priority**: Based on dependency order, then document order
4. **All stories**: `passes: false` and empty `notes`
5. **branchName**: Based on detected branch convention (see Branch Convention Detection)
   - With convention: Use detected prefix (e.g., `feature/task-status`)
   - Without convention: Use `ralph/` prefix (e.g., `ralph/task-status`)
6. **Always add**: "Typecheck passes" to every story's acceptance criteria

---

## Splitting Large PRDs

If a PRD has big features, split them:

**Original:**

> "Add user notification system"

**Split into:**

1. US-001: Add notifications table to database
2. US-002: Create notification service for sending notifications
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Add mark-as-read functionality
6. US-006: Add notification preferences page

Each is one focused change that can be completed and verified independently.

---

## Specifications for Complex Features

For features with significant logic or multiple components, create specification files in the project's `.specs/` directory.

### When to Create Specs

- Feature has complex business logic
- Multiple stories will reference the same requirements
- Technical decisions need documenting (API contracts, data models)
- The feature spans more than 4-5 stories

### Specs Structure

```
<project-root>/.specs/
├── feature-name.md       # Feature specification
├── api-contracts.md      # API definitions (if applicable)
└── data-models.md        # Schema/type definitions
```

### Spec File Format

```markdown
# [Feature Name] Specification

## Overview

Brief description of the feature.

## Requirements

- REQ-1: Specific requirement
- REQ-2: Another requirement

## Technical Decisions

- Decision 1: We chose X because Y
- Decision 2: Pattern Z will be used for...

## Data Model

[Schema definitions, types, etc.]

## API Contract (if applicable)

[Endpoints, request/response formats]
```

### Why Specs Matter

Ralph reads specs at the start of **EVERY iteration**. Well-written specs:

- Prevent Ralph from making inconsistent decisions across iterations
- Provide deterministic context loading (same files every loop)
- Serve as single source of truth for requirements
- Help future iterations understand the "why" behind decisions

### When Converting PRD to prd.json

If the PRD describes a complex feature, suggest creating specs:

1. Identify if the feature has complex logic or multiple interdependent parts
2. If so, create `.specs/<feature-name>.md` with the key decisions and contracts
3. Reference the spec in story descriptions: "Implement per .specs/feature-name.md"

---

## Example

**Input PRD:**

```markdown
# Task Status Feature

Add ability to mark tasks with different statuses.

## Requirements

- Toggle between pending/in-progress/done on task list
- Filter list by status
- Show status badge on each task
- Persist status in database
```

**Output prd.json (no conventions detected - uses defaults):**

```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-status", // No branch convention found → ralph/
  "description": "Task Status Feature - Track task progress with status indicators",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**Output prd.json (when project has conventions detected):**

If the project has:

- Ticket convention: commits like `feat: CI-1234 - Add login` → ticket prefix is `CI`
- Branch convention: branches like `feature/add-login` → branch prefix is `feature/`

```json
{
  "project": "TaskApp",
  "branchName": "feature/task-status",  // Detected branch prefix
  "userStories": [
    { "id": "CI-0000", "title": "Add status field to tasks table", ... },
    { "id": "CI-0000", "title": "Display status badge on task cards", ... },
    { "id": "CI-0000", "title": "Add status toggle to task list rows", ... },
    { "id": "CI-0000", "title": "Filter tasks by status", ... }
  ]
}
```

---

## Archiving Previous Runs

**Before writing a new prd.json, check if there is an existing one from a different feature:**

1. Read the current `prd.json` if it exists
2. Check if `branchName` differs from the new feature's branch name
3. If different AND `progress.txt` has content beyond the header:
   - Create archive folder: `archive/YYYY-MM-DD-feature-name/`
   - Copy current `prd.json` and `progress.txt` to archive
   - Reset `progress.txt` with fresh header

**The ralph.sh script handles this automatically** when you run it, but if you are manually updating prd.json between runs, archive first.

---

## Checklist Before Saving

Before writing prd.json, verify:

- [ ] **Ticket convention checked** (detect from git history, use PREFIX-0000 or US-XXX)
- [ ] **Branch convention checked** (detect from branches, use detected prefix or ralph/)
- [ ] **Previous run archived** (if prd.json exists with different branchName, archive it first)
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema to backend to UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify in browser using dev-browser skill" as criterion
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
