---
name: clickup-push-tasks
description: Push a local task file to ClickUp as a new task with subtasks. Use when you have a structured task file (docs/tasks/*.md) and want to create visibility in ClickUp for clients or team members. Creates parent task + phases as subtasks + items as sub-subtasks.
---

# ClickUp Push Tasks

Create a ClickUp task hierarchy from a local task markdown file.

## Invocation

```
/clickup-push-tasks <path-to-task-file>
/clickup-push-tasks docs/tasks/my-feature.md
/clickup-push-tasks ./outputs/project/tasks.md
```

**Arguments:**
- Required: Path to a task file in the standard format (see Task File Format below)

## Prerequisites

- **ClickUp Access Token** - Set in `~/.claude/skills/clickup-push-tasks/.env` (see `.env.example` for setup)

## Task File Format

The task file must follow the standard format:

```markdown
# Task: <Title>

> Optional summary description

**Type:** development | research | documentation
**Branch:** feat/<id>  (optional)

---

## Context

Description of the task for business users.

---

## Tasks

### Phase 1: <Phase Name>

- [ ] Task item one
  - File: `path/to/file.ts`
- [ ] Task item two
- [x] Completed item

### Phase 2: <Another Phase>

- [ ] More tasks here
```

## Workflow

### Step 1: Validate Environment

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts validate
```

If token is missing, instruct user to set `CLICKUP_ACCESS_TOKEN` in `~/.claude/skills/clickup-push-tasks/.env`.

### Step 2: Parse Task File

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/task-parser.ts <taskFilePath>
```

Validate the output has:
- `title` - Required for parent task name
- `phases` - At least one phase with items

If missing, report error and exit.

### Step 3: Ask User for Destination and Status

Fetch workspace and space hierarchy:

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts workspaces
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts spaces <workspaceId>
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts lists <spaceId>
```

The `spaces` command returns available statuses for each space.

**IMPORTANT:** Status names are case-sensitive. Use the EXACT status values returned by the API (e.g., "Open", "backlog", "Closed" - not normalized to lowercase).

Use `AskUserQuestion` to prompt user:
1. **Which Space?** (Engineering, Marketing, etc.)
2. **Which List?** (Backlog, Sprint, etc.)
3. **Initial Status?** (Use EXACT status values from the selected space's `statuses` array)

Store the selected status (with exact casing) for use when creating tasks.

### Step 4: Create Parent Task

Create the main task in the selected list with the selected status:

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts create-task <listId> "<title>" "<description>" --status=<selectedStatus>
```

- **Name:** From task file `# Task: <title>` (or main heading if no `Task:` prefix)
- **Description:** From the Context section of the task file
- **Status:** The status selected in Step 3

Note the created task ID from the response.

### Step 4.5: Generate Business Descriptions

Before creating subtasks, generate a business-friendly description for each task item. This is the key step that makes tasks understandable to business users.

For each phase and task item, create a description following this framework:

**Phase Description Template:**
```
This phase focuses on [high-level goal]. Completing these tasks will [business outcome].

Tasks: X items | Status: Y completed
```

**Task Item Description Template:**
```
**What:** [Plain English explanation of what will be done]

**Why:** [Business reason - why this matters to the project/users]

**Outcome:** [What success looks like - measurable if possible]

---
Phase: {phase name}
File: {file path} (if applicable)
```

**Example Transformation:**

Input task item:
```
- [ ] **Task 2.1: Implement core logic**
  - File: `src/core/processor.ts`
```

Generated description:
```
**What:** Build the main processing engine that validates and transforms user input into the required output format.

**Why:** This is the core functionality that enables the entire feature. Without it, no user requests can be processed.

**Outcome:** Processing function accepts input, validates against schema, transforms data, and returns structured response. Unit tests pass with >80% coverage.

---
Phase: Core Implementation
File: src/core/processor.ts
```

**Guidelines for generating descriptions:**
- Use plain English, avoid jargon
- Focus on business value, not technical implementation details
- Make outcomes specific and measurable when possible
- Keep descriptions concise but informative (3-5 sentences total)

### Step 5: Create Subtask Hierarchy

Create tasks manually with the generated descriptions (do NOT use sync-from-file).

Use the `--status` flag to set the initial status selected in Step 3.

**5a. Create Phase Subtasks**

For each phase, create a phase subtask with its generated description:

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts create-subtask <parentTaskId> "<phase name>" "<phase description>" --status=<selectedStatus>
```

Note the phase task ID from the response.

**5b. Create Item Subtasks**

For each task item in the phase, create an item subtask under the phase task:

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts create-subtask <phaseTaskId> "<item name>" "<generated description>" --status=<selectedStatus>
```

**5c. Mark Completed Items**

If the item is already completed (`[x]` in the task file), update its status to CLOSED (overrides the initial status):

```bash
npx tsx ~/.claude/skills/clickup-push-tasks/scripts/clickup-api.ts update-status <itemTaskId> "CLOSED"
```

**Rate Limiting:** Add ~100ms delay between API calls to avoid hitting the 100 req/min limit.

### Step 5.5: Save Mapping File

Create a mapping file at `.clickup-sync/<parentTaskId>.json` to enable future sync-completion:

```json
{
  "parentTaskId": "<id>",
  "taskFile": "<path to task file>",
  "syncedAt": "<ISO timestamp>",
  "phases": {
    "<phase name>": {
      "clickupId": "<phase task id>",
      "items": {
        "<item text>": "<item task id>"
      }
    }
  }
}
```

Use the Write tool to create this file. Ensure the `.clickup-sync/` directory exists first.

### Step 6: Update Task File with ClickUp Link

Add the ClickUp URL to the task file if not present:

If the task file doesn't have a `**ClickUp:**` line, add it after the title block:

```markdown
**ClickUp:** https://app.clickup.com/t/<taskId>
```

### Step 7: Report Results

Display to user:
- Created task URL (clickable)
- Number of phases created
- Number of items created
- Path to mapping file (`.clickup-sync/<taskId>.json`)

## Example Output

```
Created ClickUp task hierarchy:

Parent Task: https://app.clickup.com/t/868h2xyz

Phase: Database Schema
  Description: This phase focuses on setting up the data foundation. Completing these tasks will enable user data storage and retrieval.
  - Add user table migration
    What: Create database migration to add users table with required columns
    Why: Users need persistent storage for account information
    Outcome: Migration runs successfully, users table exists with correct schema
  - Create indexes
  - Add seed data

Phase: API Endpoints
  Description: This phase focuses on building the REST API layer. Completing these tasks will allow frontend to interact with user data.
  - GET /users endpoint
  - POST /users endpoint
  - PUT /users/:id endpoint
  - DELETE /users/:id endpoint

Total: 2 phases, 7 items
Mapping saved to: .clickup-sync/868h2xyz.json
```

**In ClickUp, each task item will have a rich description like:**

```
**What:** Create database migration to add users table with all required columns (id, email, name, created_at, updated_at).

**Why:** Users need persistent storage for their account information. This is the foundation for all user-related features.

**Outcome:** Migration runs successfully in all environments. Users table exists with correct schema and constraints. Rollback migration also works.

---
Phase: Database Schema
File: src/migrations/001_create_users.ts
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Token missing | Set `CLICKUP_ACCESS_TOKEN` in `~/.claude/skills/clickup-push-tasks/.env` |
| No title in task file | Add `# Task: <title>` to file |
| No phases found | Add `### Phase N: <name>` sections with `- [ ]` items |
| API rate limit | Wait and retry (100 req/min limit) |
