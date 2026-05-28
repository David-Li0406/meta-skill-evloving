---
name: analysis-to-tasks
description: Convert analysis reports from docs/analysis/ into actionable tasks in the SQLite database
allowed-tools: Bash, Task, Read, Glob, Grep
---

# Analysis to Tasks Skill

Converts analysis reports from `docs/analysis/` into actionable tasks in the local `tasks.db` SQLite database, using the technical-product-manager subagent to break down recommendations into well-structured tasks.

## Arguments

The skill accepts an optional file path argument:

- **No argument**: Uses the most recent analysis file in `docs/analysis/`
- **Filename**: Uses the specified file (e.g., `/analysis-to-tasks 2026-01-16-ios-code-quality.md`)
- **Full path**: Uses the exact path provided

## Execution Steps

### Step 1: Locate the Analysis File

If no argument provided, find the most recent analysis file:

```bash
ls -t docs/analysis/*.md | head -1
```

If an argument is provided, resolve it:
- If it's just a filename, prepend `docs/analysis/`
- If it's a full path, use as-is

Verify the file exists before proceeding.

### Step 2: Read the Analysis File

Read the full analysis file to extract:
1. The analysis topic/title
2. The recommendations table
3. The detailed recommendations section

Use the Read tool to get the file contents.

### Step 3: Parse Recommendations

Extract recommendations from the analysis file. Look for:

1. **Recommendations table** - Usually formatted as:
   ```markdown
   | Priority | Recommendation | Effort | Impact |
   |----------|---------------|--------|--------|
   | Critical | Fix silent delete... | Low | High |
   ```

2. **Detailed Recommendations** - Individual sections with:
   - Problem description
   - Solution approach
   - Files affected

### Step 4: Check Database for Existing Tasks

**Before creating any tasks**, query the database to identify work that's already tracked. This prevents creating redundant tasks.

#### 4a. Get All Open Tasks

```bash
sqlite3 -header -column tasks.db "SELECT id, summary, description, status, priority, domain FROM tasks WHERE status != 'Done' ORDER BY id"
```

#### 4b. Analyze Overlap

For each recommendation from the analysis, check if there's an existing task that:
1. **Exact match**: Summary contains the same key phrases
2. **Semantic overlap**: Description addresses the same problem/file/component
3. **Partial coverage**: Existing task covers part of the recommendation

Use these search patterns for each recommendation:

```bash
# Search by key terms from the recommendation
sqlite3 tasks.db "SELECT id, summary, status FROM tasks WHERE status != 'Done' AND (summary LIKE '%<key_term_1>%' OR summary LIKE '%<key_term_2>%' OR description LIKE '%<key_term_1>%')"
```

#### 4c. Categorize Recommendations

Classify each recommendation into one of these categories:

| Category | Meaning | Action |
|----------|---------|--------|
| **New** | No existing task covers this | Create new task |
| **Duplicate** | Existing task fully covers this | Skip (link to existing) |
| **Partial** | Existing task covers part of this | Ask user - update existing or create new? |
| **Supersedes** | This recommendation replaces/improves an existing task | Ask user - update existing or create new? |

#### 4d. Present Overlap Report

Before proceeding to task creation, present a report:

```markdown
## Pre-Creation Database Check

**Existing open tasks:** {count}
**Recommendations from analysis:** {count}

### Already Tracked (Will Skip)
| Recommendation | Existing Task ID | Existing Summary |
|----------------|------------------|------------------|
| Fix silent delete... | #42 | Handle delete account errors |

### Partial Overlap (Needs Decision)
| Recommendation | Existing Task ID | Overlap |
|----------------|------------------|---------|
| Add comprehensive logging | #38 | Existing task only covers API logging |

### New Work (Will Create)
| Recommendation | Priority |
|----------------|----------|
| Enable UI tests with mock backend | High |
```

If there are duplicates or partial overlaps, ask the user how to proceed before continuing to Step 5.

### Step 5: Use Technical Product Manager to Create Tasks

Invoke the `technical-product-manager` subagent via the Task tool to:
1. Break down each **non-duplicate** recommendation into actionable tasks
2. Determine appropriate priority based on the analysis priority
3. Identify the correct domain and assignee based on the task content
4. Identify any dependencies between tasks (including dependencies on existing tasks from Step 4)

**Prompt for the subagent:**

```
You are creating tasks for our SQLite tasks database based on an analysis report.

IMPORTANT: Only create tasks for the NEW recommendations listed below. Duplicates and already-tracked work have been filtered out.

## Existing Tasks (for dependency reference only - do NOT recreate these)

{existing_tasks_summary}

## Analysis File: {filename}

## NEW Recommendations to Convert (filtered - duplicates removed):

{recommendations_content}

## Database Schema

The tasks table has these columns:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- summary: TEXT NOT NULL (brief task title, ~60 chars max)
- description: TEXT (detailed description with context, acceptance criteria)
- status: TEXT (always 'To Do' for new tasks)
- priority: TEXT (Highest, High, Medium, Low - map from analysis priority)
- domain: TEXT (iOS, Backend, Infrastructure, Docs, etc.)
- assignee: TEXT (ios-engineer, fastapi-architect, database-engineer, statistical-analysis-scientist, python-code-guardian, technical-product-manager, project-code-reviewer)
- task_type: TEXT (bug, feature, refactor, test, docs)
- created_at: TEXT (datetime)
- updated_at: TEXT (datetime)

## Priority Mapping

- Critical (analysis) -> Highest (database)
- High (analysis) -> High (database)
- Medium (analysis) -> Medium (database)
- Low (analysis) -> Low (database)

## Domain Assignment Rules

- iOS/Swift/SwiftUI/ViewModel -> domain: iOS, assignee: ios-engineer
- API/FastAPI/Backend/Python -> domain: Backend, assignee: fastapi-architect
- SQL/Database/Schema -> domain: Backend, assignee: database-engineer
- Statistics/Math/Formulas -> domain: Backend, assignee: statistical-analysis-scientist
- Tests/Coverage -> domain matches content, assignee matches domain
- Docs/README -> domain: Docs, assignee: technical-product-manager

## Output Format

For each task, provide:
1. summary (concise title)
2. description (include problem context from analysis, acceptance criteria, files affected)
3. priority
4. domain
5. assignee
6. task_type
7. dependencies (list of other task summaries this depends on, if any)

Group related tasks and identify dependencies where one task must be completed before another.
```

### Step 6: Review Generated Tasks

Present the generated tasks to the user in a table format:

```markdown
## Tasks Generated from Analysis

**Source:** {analysis_file}
**Total Tasks:** {count}

| # | Summary | Priority | Domain | Assignee | Type |
|---|---------|----------|--------|----------|------|
| 1 | Fix silent delete account error handling | Highest | iOS | ios-engineer | bug |
| 2 | Enable UI tests with mock backend | High | iOS | ios-engineer | test |
| ... | ... | ... | ... | ... | ... |

### Dependencies Identified

- Task 2 (Enable UI tests) -> depends on Task 1 (Fix error handling)
```

### Step 7: Get User Confirmation

Ask the user:

1. "Do you approve creating these {N} tasks in the database?"
2. "Would you like to modify any tasks before creation?"
3. "Should I add the identified dependencies?"

Wait for explicit approval before proceeding.

### Step 8: Insert Tasks into Database

After approval, insert each task:

```bash
sqlite3 tasks.db "INSERT INTO tasks (summary, description, status, priority, domain, assignee, task_type, created_at, updated_at)
VALUES (
  '<summary>',
  '<description>',
  'To Do',
  '<priority>',
  '<domain>',
  '<assignee>',
  '<task_type>',
  datetime('now'),
  datetime('now')
)"
```

Capture the inserted task IDs for dependency linking:

```bash
sqlite3 tasks.db "SELECT last_insert_rowid()"
```

### Step 9: Add Dependencies

If dependencies were identified and approved, add them:

```bash
python3 scripts/manage_dependencies.py add <task_id> <depends_on_id>
```

### Step 10: Generate Summary Report

After all tasks are created, provide a summary:

```markdown
## Tasks Created Successfully

**Source Analysis:** {analysis_file}
**Recommendations in Analysis:** {total_recommendations}
**Already Tracked (Skipped):** {skipped_count}
**Tasks Created:** {created_count}

### Skipped (Already Tracked)

| Recommendation | Existing Task |
|----------------|---------------|
| Fix silent delete... | #42 - Handle delete account errors |

### New Tasks Created

| ID | Summary | Priority | Assignee |
|----|---------|----------|----------|
| 45 | Fix silent delete account error handling | Highest | ios-engineer |
| 46 | Enable UI tests with mock backend | High | ios-engineer |
| ... | ... | ... | ... |

### Dependencies Added

- Task 46 depends on Task 45

### Next Steps

Run `/next-task` to start working on the highest priority task.
```

Show the final state:

```bash
sqlite3 -header -column tasks.db "SELECT id, summary, priority, domain, assignee FROM tasks WHERE status = 'To Do' ORDER BY CASE priority WHEN 'Highest' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 WHEN 'Low' THEN 4 ELSE 5 END, id DESC LIMIT 10"
```

## Error Handling

- **File not found**: "Analysis file not found: {path}. Available files: {list}"
- **No recommendations**: "No recommendations found in the analysis file. The file should contain a Recommendations section."
- **Database error**: "Failed to insert task: {error}. Rolling back..."
- **Duplicate task**: Check for existing tasks with similar summaries before inserting

## Duplicate Detection (Step 4)

Duplicate detection is performed **early in Step 4**, before task creation begins. This prevents creating redundant work and keeps the database clean.

### Search Strategies

Use multiple search strategies to find potential duplicates:

```bash
# 1. Search by key phrases from recommendation
sqlite3 tasks.db "SELECT id, summary, status FROM tasks WHERE status != 'Done' AND summary LIKE '%<key_phrase>%'"

# 2. Search by affected file/component names
sqlite3 tasks.db "SELECT id, summary, status FROM tasks WHERE status != 'Done' AND (description LIKE '%ViewModel%' OR description LIKE '%TestTakingFlow%')"

# 3. Search by domain for broader overlap check
sqlite3 tasks.db "SELECT id, summary, description FROM tasks WHERE status != 'Done' AND domain = 'iOS'"
```

### Handling Duplicates

When duplicates or overlaps are found:

| Situation | Action |
|-----------|--------|
| Exact duplicate | Skip and note existing task ID |
| Partial overlap | Ask user: skip, create new, or update existing |
| Recommendation supersedes existing | Ask user: update existing task or create replacement |
| No overlap | Proceed with creation |

### User Options for Overlaps

If duplicates or partial overlaps are found, present options:
1. **Skip** - Don't create the redundant task
2. **Create anyway** - May be intentional (different scope)
3. **Update existing** - Enhance the existing task with new details
4. **Replace existing** - Mark old as Done, create new with improved scope

## Important Guidelines

1. **Check the database FIRST** - Always run Step 4 before creating tasks. This prevents redundant work and keeps the backlog clean
2. **Use the technical-product-manager subagent** - Don't try to parse and create tasks manually; the subagent provides better task breakdown and prioritization
3. **Always get user approval** - Never insert tasks without explicit confirmation
4. **Report what was skipped** - Always show the user which recommendations were already tracked
5. **Preserve context** - Include relevant details from the analysis in task descriptions
6. **Set proper priorities** - Map analysis priorities to database priorities correctly
7. **Identify dependencies** - Critical issues often block other work; new tasks may depend on existing tasks
8. **Assign correctly** - Use domain keywords to assign the right agent
9. **Link to source** - Include the analysis file reference in task descriptions

## Example Usage

```
/analysis-to-tasks
```
Uses the most recent analysis file.

```
/analysis-to-tasks 2026-01-16-ios-code-quality.md
```
Uses the specified analysis file.

Begin by locating and reading the analysis file.
