---
name: groom-backlog
description: Groom the Jira backlog by closing completed tickets, removing redundant/stale tickets, reprioritizing, and assigning agents
allowed-tools: Bash, Glob, Grep, Read
---

# Groom Backlog Skill

Grooms the local tasks database by identifying completed, redundant, incorrectly prioritized, or unassigned tasks.

## Step 1: Fetch All Backlog Tasks

Query all open tasks from the local SQLite database:

```bash
# Get all open tasks (not Done)
sqlite3 -header -column tasks.db "SELECT id, summary, status, priority, domain, assignee FROM tasks WHERE status != 'Done' ORDER BY priority DESC, id"

# Get full details for analysis
sqlite3 -header -column tasks.db "SELECT * FROM tasks WHERE status != 'Done'"

# Get dependency information - blocked tasks and all dependencies
python3 scripts/manage_dependencies.py blocked
python3 scripts/manage_dependencies.py all
```

## Step 2: Categorize Tasks

Analyze each task and categorize it into one of the following:

### Category A: Candidates for Done (Acceptance Criteria Already Met)
Tasks where the acceptance criteria has already been implemented in the codebase:

1. **Verify against code**: For each task, read the description and search the codebase to determine if the work has already been completed
2. **Evidence required**: Provide specific file paths, function names, or code snippets that demonstrate the criteria is met
3. **Mark as Done**: Use SQLite to update the status: `sqlite3 tasks.db "UPDATE tasks SET status = 'Done' WHERE id = <id>"`

### Category B: Candidates for Deletion
Tasks that should be removed from the backlog:

1. **Redundant tasks**: Duplicates or near-duplicates of other tasks
2. **Obsolete tasks**: Tasks for features or fixes that are no longer relevant due to:
   - Changes in product direction
   - Superseded by other work
   - Technical approach that's no longer applicable
3. **Stale tasks**: Tasks that have been untouched for an extended period with no clear path forward
4. **Vague tasks**: Tasks with insufficient detail that cannot be acted upon

**IMPORTANT**: Before recommending deletion, check if other tasks depend on this task:
```bash
python3 scripts/manage_dependencies.py dependents <id>
```
If other tasks depend on it, do NOT recommend deletion unless those dependent tasks are also being deleted or the dependency should be removed.

### Category C: Candidates for Reprioritization
Tasks that have incorrect priority levels:

1. **Under-prioritized**: Important tasks marked as low priority
   - Security-related issues
   - User-facing bugs
   - Dependencies for other critical work
2. **Over-prioritized**: Low-impact tasks marked as high priority
   - Nice-to-have features
   - Minor code improvements
   - Speculative future work

### Category D: Unassigned Tasks
Tasks that don't have an agent assignee. These should be assigned to the appropriate agent based on their content:

```bash
# Check for unassigned tasks
sqlite3 -header -column tasks.db "SELECT id, summary, domain FROM tasks WHERE status != 'Done' AND assignee IS NULL"

# Preview agent assignments
python3 scripts/assign_tasks_to_agents.py assign --dry-run
```

Available agents (in `.claude/agents/`):
- **ios-engineer**: iOS/SwiftUI, ViewModels, navigation, UserDefaults, haptics
- **fastapi-architect**: API endpoints, FastAPI, backend services, authentication
- **database-engineer**: SQL, database, migrations, schemas, queries
- **statistical-analysis-scientist**: Statistics, math, formulas, calculations, percentiles
- **python-code-guardian**: Python refactoring, error handling, background jobs
- **technical-product-manager**: Features, requirements, product planning
- **project-code-reviewer**: Code review, standards, patterns

### Category E: Healthy Tasks
Tasks that are correctly prioritized, assigned, and relevant. No action needed.

## Step 3: Review Context

Before taking action, gather additional context:

```bash
# View details of a specific task
sqlite3 -header -column tasks.db "SELECT * FROM tasks WHERE id = <id>"
```

Also review:
- Recent commits to see what work has been completed
- The product documentation in `docs/` to understand current priorities
- Any related tasks that might be duplicates

## Step 4: Present Findings for Approval

Present your analysis to the user in the following format:

```markdown
## Backlog Grooming Analysis

### Total Tasks Analyzed: X

---

### Ready for Done - Acceptance Criteria Met (W tasks)

| ID | Summary | Evidence |
|----|---------|----------|
| 12 | "Add login validation" | Implemented in `src/auth/validator.ts:45-89` |
| 13 | "Create user model" | Found in `backend/models/user.py` with all required fields |

---

### Recommended for Deletion (Y tasks)

| ID | Summary | Reason |
|----|---------|--------|
| 15 | "Add feature X" | Duplicate of task 8 |
| 16 | "Fix bug Y" | Obsolete - feature removed |

---

### Recommended for Reprioritization (Z tasks)

| ID | Summary | Current | Recommended | Reason |
|----|---------|---------|-------------|--------|
| 17 | "Security fix" | Low | High | Security issues should be high priority |
| 18 | "Nice to have" | High | Low | No user impact, speculative |

---

### Unassigned Tasks (U tasks)

| ID | Summary | Recommended Agent | Reason |
|----|---------|-------------------|--------|
| 19 | "Add SwiftUI view" | ios-engineer | Contains SwiftUI keywords |
| 20 | "Optimize SQL query" | database-engineer | Database-related task |

---

### No Action Needed (V tasks)
These tasks are correctly prioritized, assigned, and relevant.
```

## Step 5: Get User Confirmation

**IMPORTANT**: Before making any changes, explicitly ask the user:

1. "Do you approve moving the W tasks to Done (acceptance criteria verified in codebase)?"
2. "Do you approve deleting the X tasks listed above?"
3. "Do you approve the priority changes for the Y tasks listed above?"
4. "Do you approve the agent assignments for the U unassigned tasks?"
5. "Would you like me to modify any of these recommendations?"

Wait for explicit user approval before proceeding.

## Step 6: Execute Changes

Only after user approval, execute the changes:

### For Done Transitions (Acceptance Criteria Met):
```bash
sqlite3 tasks.db "UPDATE tasks SET status = 'Done' WHERE id = <id>"
```

### For Deletions:
```bash
sqlite3 tasks.db "DELETE FROM tasks WHERE id = <id>"
```

### For Priority Changes:
```bash
sqlite3 tasks.db "UPDATE tasks SET priority = '<New Priority>' WHERE id = <id>"
```

Valid priority values: High, Medium, Low

### For Agent Assignments:
```bash
# Assign all unassigned tasks automatically
python3 scripts/assign_tasks_to_agents.py assign

# Or assign a specific task manually
sqlite3 tasks.db "UPDATE tasks SET assignee = '<agent-name>' WHERE id = <id>"
```

Valid agent names: ios-engineer, fastapi-architect, database-engineer, statistical-analysis-scientist, python-code-guardian, technical-product-manager, project-code-reviewer

### After Each Change:
Confirm the change was applied:
```bash
sqlite3 -header -column tasks.db "SELECT id, summary, status, priority FROM tasks WHERE id = <id>"
```

## Step 7: Compute Priority Scores

After all grooming changes are complete, compute `priority_score` for all open tasks. This enables `/next-task` to select the most important task without LLM inference.

### Scoring Formula

```
priority_score = base_priority + unblocks_bonus + age_bonus
```

Where:
- **base_priority**: Highest=40, High=30, Medium=20, Low=10
- **unblocks_bonus**: +15 if task has any dependents, +5 per dependent task
- **age_bonus**: +10 if created more than 14 days ago

### Compute and Update Scores

```bash
# Update priority_score for all open tasks
sqlite3 tasks.db "
UPDATE tasks SET priority_score = (
  -- Base priority
  CASE priority
    WHEN 'Highest' THEN 40
    WHEN 'High' THEN 30
    WHEN 'Medium' THEN 20
    WHEN 'Low' THEN 10
    ELSE 15
  END
  -- Unblocks bonus: +15 if has dependents, +5 per dependent
  + COALESCE((
    SELECT CASE WHEN COUNT(*) > 0 THEN 15 + (COUNT(*) * 5) ELSE 0 END
    FROM task_dependencies d
    WHERE d.depends_on_id = tasks.id
  ), 0)
  -- Age bonus: +10 if older than 14 days
  + CASE WHEN julianday('now') - julianday(created_at) > 14 THEN 10 ELSE 0 END
)
WHERE status != 'Done';
"

# Verify the scores
sqlite3 -header -column tasks.db "
SELECT id, summary, priority, priority_score
FROM tasks
WHERE status = 'To Do'
ORDER BY priority_score DESC
LIMIT 10;
"
```

## Step 8: Generate Summary Report

After all changes are complete, provide a summary:

```markdown
## Backlog Grooming Complete

### Actions Taken:
- **Moved to Done**: W tasks (acceptance criteria verified)
- **Deleted**: X tasks
- **Reprioritized**: Y tasks
- **Assigned**: U tasks (agent assignments)
- **Unchanged**: Z tasks

### Completed Tasks (Moved to Done):
- ID 12: "Add login validation" (verified in `src/auth/validator.ts`)
- ID 13: "Create user model" (verified in `backend/models/user.py`)

### Deleted Tasks:
- ID 15: "Add feature X" (was duplicate)
- ID 16: "Fix bug Y" (obsolete)

### Priority Changes:
- ID 17: Low -> High
- ID 18: High -> Low

### Agent Assignments:
- ID 19: -> ios-engineer
- ID 20: -> database-engineer

### Current Backlog Health:
- Total open tasks: N
- High priority: X
- Medium priority: Y
- Low priority: Z
- Unassigned: U (should be 0 after grooming)

### Tasks by Agent:
- ios-engineer: X tasks
- fastapi-architect: Y tasks
- database-engineer: Z tasks
- (etc.)
```

Show final backlog state:
```bash
sqlite3 -header -column tasks.db "SELECT id, summary, status, priority, domain, assignee FROM tasks WHERE status != 'Done' ORDER BY priority DESC, id"
```

## Important Guidelines

1. **Never modify without approval**: Always present findings and wait for explicit user confirmation before moving tasks to Done or deleting them
2. **Verify against code thoroughly**: When checking if acceptance criteria is met, search the codebase comprehensively. Use Glob, Grep, and Read tools to find evidence. Provide specific file paths and line numbers as proof.
3. **Be conservative**: When in doubt about completion or deletion, recommend keeping the task open and flagging it for review
4. **Preserve history**: Note in the summary which tasks were moved to Done or deleted and why, so the information is not lost
5. **Consider dependencies**: Before deleting a task, check if other tasks reference it
6. **Explain reasoning**: For each recommendation, provide clear reasoning that the user can evaluate
7. **Batch operations carefully**: Execute changes one at a time to handle any errors gracefully

## Error Handling

- If the database doesn't exist, inform the user: "Database not found. Run `python3 scripts/jira_to_sqlite.py` to sync tasks first."
- If a task ID doesn't exist, report the error and continue with other tasks
- If no open tasks are found, report "No open tasks found in the backlog"

Begin by fetching all backlog tasks.
