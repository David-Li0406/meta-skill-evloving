---
name: prd-to-tasks
description: "Convert PRDs to Claude Code Tasks via TaskCreate. Use when you have an existing PRD and need to create tasks for Ralph. Triggers on: convert this prd, turn this into tasks, create tasks from this, prd to tasks."
---

# PRD to Tasks Converter

Converts existing PRDs to Claude Code Tasks that Ralph uses for autonomous execution.

---

## Task Namespace Detection

**At the START**, detect both namespaces:

1. **Current namespace** (where tasks will be created): Use Bash `echo "${CLAUDE_CODE_TASK_LIST_ID:-default}"`
2. **Ralph's expected namespace**: Use Bash `echo "$(basename "$(pwd)")-$(git branch --show-current 2>/dev/null || echo main)"`

Proceed with creating tasks in the current namespace.

---

## The Job

Take a PRD (markdown file or text) and convert it to tasks via TaskCreate. Tasks persist via `CLAUDE_CODE_TASK_LIST_ID` environment variable.

**Workflow:**
1. Audit codebase for existing functionality
2. Create tasks via TaskCreate
3. Set dependencies via TaskUpdate
4. Output summary
5. **STOP** - Do NOT implement anything

---

## Codebase Audit

Before creating tasks, thoroughly audit the codebase:

1. **Use subagents** - Spawn explore agents to search in parallel for faster results
2. **For each PRD feature**, determine:
   - **EXISTS**: Functionality already implemented → create task then immediately mark `completed`
   - **PARTIAL**: Some pieces exist → note in description what's missing
   - **NEW**: Must be built from scratch

### Example Gap Analysis
```
Feature: User authentication
- Login form → EXISTS (found in app/login/page.tsx)
- Password reset → PARTIAL (email sending exists in lib/email.ts, reset flow missing)
- 2FA → NEW (nothing exists)
```

### Search Patterns
- Use Grep for function/class names mentioned in PRD
- Use Glob to find related files by name
- Check for existing database tables/migrations
- Look for similar UI components

---

## Output Format

Each task requires these fields for TaskCreate:

```json
{
  "subject": "Add status column to tasks table",
  "description": "Add status column to tasks table with enum values: pending, in_progress, completed. Set default to pending.",
  "activeForm": "Adding status column to tasks table"
}
```

| Field | Description | Example |
|-------|-------------|---------|
| `subject` | Brief imperative task title | "Add login API endpoint" |
| `description` | Detailed description of what needs to be done | "Create POST /api/login endpoint that accepts email/password and returns JWT token" |
| `activeForm` | Present participle (-ing) form shown in spinner | "Adding login API endpoint" |

All tasks are created with status `pending`. Use TaskUpdate to change status to `in_progress` or `completed`.

---

## Task Size: The Number One Rule

**Each task must be completable in ONE Ralph iteration (one context window).**

Ralph spawns a fresh Claude Code instance per iteration with no memory of previous work. If a task is too big, the LLM runs out of context before finishing and produces broken code.

### Right-sized tasks:
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):
- "Build the entire dashboard" → Split into: schema, queries, UI components, filters
- "Add authentication" → Split into: schema, middleware, login UI, session handling
- "Refactor the API" → Split into one task per endpoint or pattern

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Task Ordering: Dependencies First

Tasks execute in list order. Earlier tasks must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

---

## Task Descriptions: Must Be Verifiable

Each task description should be something Ralph can CHECK, not something vague.

### Good descriptions (verifiable):
- "Add `status` column to tasks table with default 'pending'"
- "Create filter dropdown with options: All, Active, Completed"
- "Add delete button that shows confirmation dialog"
- "Build login form with email/password fields"

### Bad descriptions (vague):
- "Implement the feature correctly"
- "Make it work"
- "Add good UX"
- "Handle edge cases"

---

## Splitting Large PRDs

If a PRD has big features, split them:

**Original:**
> "Add user notification system"

**Split into:**
1. Add notifications table to database
2. Create notification service for sending notifications
3. Add notification bell icon to header
4. Create notification dropdown panel
5. Add mark-as-read functionality
6. Add notification preferences page

Each is one focused change that can be completed and verified independently.

---

## Dependency Planning

After creating ALL tasks, establish dependencies:

1. **Get task IDs** - Call TaskList to see created tasks with their IDs
2. **Analyze relationships** based on:
   - Schema/migration tasks block backend tasks
   - Backend tasks block UI tasks that consume them
   - Foundation utilities block features using them
   - Shared entities (same table/model mentioned) indicate dependency
3. **Set dependencies** via TaskUpdate:
   ```json
   {
     "taskId": "3",
     "addBlockedBy": ["1", "2"]
   }
   ```

### Dependency Detection Rules

| Pattern | Example | Dependency |
|---------|---------|------------|
| Schema → Backend | "Add users table" → "Add user API" | API blocked by schema |
| Backend → UI | "Create auth endpoint" → "Build login form" | Form blocked by endpoint |
| Shared entity | Both mention "notifications" | Later task blocked by earlier |
| Explicit in PRD | "Filter requires status field" | Filter blocked by status |

### Keep Chains Shallow

- Avoid deep chains (A→B→C→D→E serializes everything)
- Independent tasks should have NO blockers (enables parallel execution)
- Only block on direct dependencies

### Example

Tasks created:
1. Add status column to tasks table
2. Display status badge on task cards
3. Add status dropdown to task rows
4. Add status filter dropdown

Dependencies to set:
```
TaskUpdate: {"taskId": "2", "addBlockedBy": ["1"]}  // badge needs column
TaskUpdate: {"taskId": "3", "addBlockedBy": ["1"]}  // dropdown needs column
TaskUpdate: {"taskId": "4", "addBlockedBy": ["1"]}  // filter needs column
```

Tasks 2, 3, 4 can run in parallel after Task 1 completes.

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

**Process:**
1. Audit codebase for existing status handling → None found
2. Break into 4 ordered tasks (schema → UI → interaction → filtering)
3. Create tasks via TaskCreate (call TaskCreate 4 times)
4. Set dependencies via TaskUpdate

**Output TaskCreate calls:**
```json
// Task 1
{
  "subject": "Add status field to tasks table",
  "description": "Add status field to tasks table with enum: pending, in_progress, done (default pending). Include database migration.",
  "activeForm": "Adding status field to tasks table"
}

// Task 2
{
  "subject": "Display status badge on task cards",
  "description": "Display status badge on task cards with colors: gray=pending, blue=in_progress, green=done",
  "activeForm": "Displaying status badge on task cards"
}

// Task 3
{
  "subject": "Add status dropdown to task rows",
  "description": "Add status dropdown to each task row that saves immediately without page refresh",
  "activeForm": "Adding status dropdown to task rows"
}

// Task 4
{
  "subject": "Add status filter dropdown",
  "description": "Add status filter dropdown (All, Pending, In Progress, Done) that persists in URL params",
  "activeForm": "Adding status filter dropdown"
}
```

**Output TaskUpdate calls (dependencies):**
```json
{"taskId": "2", "addBlockedBy": ["1"]}
{"taskId": "3", "addBlockedBy": ["1"]}
{"taskId": "4", "addBlockedBy": ["1"]}
```

**Output summary:**
```
✓ Created 4 tasks in namespace: {current_namespace}

Ralph expects namespace: {ralph_namespace}
✓ Namespaces match - ralph will find these tasks

Tasks:
1. Add status field to tasks table - pending
2. Display status badge on task cards - pending (blocked by #1)
3. Add status dropdown to task rows - pending (blocked by #1)
4. Add status filter dropdown - pending (blocked by #1)

Dependencies:
- #2, #3, #4 ← #1 (all UI needs schema first)

Run: ./.ralph/ralph.sh 10
```

---

## Checklist Before Creating Tasks

Before calling TaskCreate, verify:

- [ ] Audited codebase for existing functionality (EXISTS/PARTIAL/NEW)
- [ ] Each task is completable in one iteration (small enough)
- [ ] Tasks are ordered by dependency (schema → backend → UI)
- [ ] Task descriptions are verifiable (not vague)
- [ ] No task depends on a later task
- [ ] `subject` uses imperative form ("Add...", "Create...", "Build...")
- [ ] `description` provides detailed context and acceptance criteria
- [ ] `activeForm` uses present participle ("Adding...", "Creating...", "Building...")

After calling TaskCreate, set dependencies via TaskUpdate.

---

## After Creating Tasks and Dependencies

**YOU ARE DONE.** Output the summary with namespace info and dependency graph, tell user to run `./ralph.sh`, and STOP.

Do NOT:
- Ask if they want you to implement
- Start coding
- Suggest next steps beyond running ralph
- Make any code changes

The skill ends here. Ralph handles implementation.
