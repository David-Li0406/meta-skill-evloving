---
name: next-task
description: Get the most important task that is ready to be worked on
allowed-tools: Bash, Task, Read, Edit, Write, Grep, Glob
---

# Next Task Skill

The primary interface for working with tasks from the local `tasks.db` SQLite database. Use this to get the next task, start working on it, and manage the full development workflow.

## Commands

### Get Next Task (default - no arguments)

Finds the highest-priority task that is ready to work on (no incomplete dependencies) and **automatically begins working on it**.

```bash
sqlite3 -header -column tasks.db "
SELECT t.id, t.summary, t.priority, t.priority_score, t.domain, t.assignee, t.description
FROM tasks t
WHERE t.status = 'To Do'
  AND NOT EXISTS (
    SELECT 1 FROM task_dependencies d
    JOIN tasks blocker ON d.depends_on_id = blocker.id
    WHERE d.task_id = t.id AND blocker.status != 'Done'
  )
ORDER BY t.priority_score DESC, t.id
LIMIT 1;
"
```

**Note**: The `priority_score` is pre-computed by `/groom-backlog` and factors in priority level, how many tasks this unblocks, and task age. This enables fast, intelligent task selection without LLM inference.

After finding the next ready task, **immediately proceed to the "Begin Work on a Task" workflow** using the retrieved task ID. Do not wait for user confirmation.

### Begin Work on a Task (with task ID argument)

When called with a task ID (e.g., `/next-task 6`), begin the full development workflow:

**Follow these steps IN ORDER:**

1. **Fetch the task** from the local database:
   ```bash
   sqlite3 -header -column tasks.db "SELECT * FROM tasks WHERE id = <id>"
   ```

2. **Start task metrics tracking**:
   ```bash
   ~/.claude/task-metrics.sh start "TASK-<id>" "<task_summary>"
   ```

3. **Update the task status** to In Progress:
   ```bash
   sqlite3 tasks.db "UPDATE tasks SET status = 'In Progress', updated_at = datetime('now') WHERE id = <id>"
   ```

4. **Extract task details** including:
   - Summary
   - Description
   - Priority
   - Domain
   - Assignee

5. **Create a new git branch IMMEDIATELY**:
   - Format: `feature/TASK-<id>-brief-description`
   - Commands:
     ```bash
     git checkout main && git pull origin main
     git checkout -b feature/TASK-<id>-brief-description
     ```

6. **Use the technical-product-manager subagent** to determine the best subagent(s) for the task based on:
   - Task domain (iOS, Backend, etc.)
   - Task assignee field (often indicates the right agent type)
   - Task description and requirements

7. **Delegate the work** to the chosen subagent(s).

8. **Create atomic commits** as you complete logical units of work.
   - All commits should be on the feature branch, NOT main.

9. **Review the code locally** before considering the work complete.
   - Use the appropriate code review agent for the domain.

10. **Push the branch and create a PR**:
    ```bash
    git push -u origin feature/TASK-<id>-description
    gh pr create --title "[TASK-<id>] Brief task description" --body "..."
    ```
    Capture the PR URL from the output (e.g., `https://github.com/gioe/aiq/pull/540`).

11. **Update the task status and PR URL**:
    ```bash
    sqlite3 tasks.db "UPDATE tasks SET status = 'In Review', github_pr = '<pr_url>', updated_at = datetime('now') WHERE id = <id>"
    ```

12. **Review loop - iterate until Claude approves**:
    After the PR is created, enter a review loop with the remote Claude reviewer. Continue until agreement is reached that the PR is ready to merge.

    ```
    ┌─► Poll for Claude's review
    │         │
    │         ▼
    │   Analyze review
    │         │
    │         ▼
    │   ┌─────────────┐
    │   │ Approved?   │───Yes──► Exit loop (ready to merge)
    │   └─────────────┘
    │         │ No
    │         ▼
    │   Address comments
    │         │
    │         ▼
    │   Push fixes
    │         │
    └─────────┘
    ```

    **Step 12a: Poll for Claude's review**
    ```bash
    # Extract PR number from URL (e.g., 540 from https://github.com/gioe/aiq/pull/540)
    PR_NUMBER=<extracted_pr_number>

    # Poll for Claude's review (check every 30 seconds, timeout after 10 minutes)
    # IMPORTANT: Use `gh pr view --comments` to fetch ALL comment types (issue comments,
    # PR reviews, and inline review comments). Do NOT use the API endpoint
    # `/issues/{number}/comments` as it only returns issue comments and misses PR reviews.
    # NOTE: `gh pr view --comments` shows author as "claude" (not "claude[bot]")
    for i in {1..20}; do
      COMMENTS=$(gh pr view $PR_NUMBER --comments 2>/dev/null)
      if echo "$COMMENTS" | grep -q "^author:.*claude"; then
        echo "Claude review found!"
        break
      fi
      echo "Waiting for Claude review... (attempt $i/20)"
      sleep 30
    done
    ```

    Then fetch the actual review content:
    ```bash
    gh pr view $PR_NUMBER --comments | grep -A 500 "^author:.*claude"
    ```

    Alternatively, for more structured access to review content:
    ```bash
    gh api repos/gioe/aiq/issues/$PR_NUMBER/comments --jq '.[] | select(.user.login == "claude[bot]") | .body'
    ```

    **Step 12b: Check if Claude approved**
    Parse the review to determine if Claude has approved the PR. Look for approval signals:
    - "LGTM" (Looks Good To Me)
    - "Approved"
    - "Ready to merge"
    - "No blocking issues"
    - No Category A (blocking) comments in the review

    If approved → Exit loop, proceed to step 13.
    If not approved → Continue to step 12c.

    **Step 12c: Address Claude's review comments**

    **Category A - Address Immediately (blocking):**
    - Security concerns (XSS, SQL injection, auth issues, secrets)
    - Bug reports (logic errors, null pointers, race conditions)
    - Breaking changes (API contract violations)
    - Test failures or missing tests
    - Critical performance issues
    - Type errors or missing error handling

    For each Category A comment:
    1. Read the relevant file(s)
    2. Make the code fix using Edit tool
    3. Commit: `[TASK-<id>] Address PR review: <brief description>`

    **Category B - Defer to backlog (non-blocking):**
    - Code style suggestions
    - Refactoring suggestions
    - Documentation requests
    - Nice-to-have improvements
    - Minor TODOs

    For each Category B comment:
    1. Create a task in the local SQLite database:
       ```bash
       sqlite3 tasks.db "INSERT INTO tasks (summary, description, status, priority, domain, created_at, updated_at)
         VALUES ('[Deferred] <brief description>', 'Deferred from PR #<pr_number> review for TASK-<id>.\n\nOriginal comment: <comment text>\n\nReason deferred: <why this can wait>', 'To Do', 'Low', '<domain>', datetime('now'), datetime('now'))"
       ```
    2. Document in `.github/DEFERRED_REVIEW_ITEMS.md`

    **Step 12d: Push fixes and loop back**
    ```bash
    git push origin feature/TASK-<id>-description
    ```
    Update `LAST_REVIEW_TIME` to the current review's timestamp, then loop back to step 12a to wait for Claude's next review.

13. **PR approved - finalize and merge**:
    Once Claude approves, automatically perform ALL of these steps:

    **Step 13a: Create deferred tasks for Category B items**
    For each non-blocking suggestion in the review, create a task:
    ```bash
    sqlite3 tasks.db "INSERT INTO tasks (summary, description, status, priority, domain, created_at, updated_at)
      VALUES ('[Deferred] <brief description>', 'Deferred from PR #<pr_number> review for TASK-<id>.

Original comment: <comment text>

Reason deferred: <why this can wait>', 'To Do', 'Low', '<domain>', datetime('now'), datetime('now'))"
    ```

    **Step 13b: Merge the PR**
    ```bash
    gh pr merge $PR_NUMBER --squash --delete-branch
    ```

    **Step 13c: Update task status to Done**
    ```bash
    sqlite3 tasks.db "UPDATE tasks SET status = 'Done', updated_at = datetime('now') WHERE id = <id>"
    ```

14. **End task metrics tracking**:
    ```bash
    ~/.claude/task-metrics.sh end
    ```

15. **Check for newly unblocked tasks**:
    ```bash
    sqlite3 -header -column tasks.db "
    SELECT t.id, t.summary, t.priority
    FROM tasks t
    JOIN task_dependencies d ON t.id = d.task_id
    WHERE d.depends_on_id = <id> AND t.status = 'To Do'
    "
    ```

### Mark Task as Done

When called with `done <id>`:

```bash
sqlite3 tasks.db "UPDATE tasks SET status = 'Done', updated_at = datetime('now') WHERE id = <id>"
```

Then show newly unblocked tasks.

### View Task Details

When called with `view <id>`:

```bash
sqlite3 -header -column tasks.db "SELECT * FROM tasks WHERE id = <id>"
```

### List Top N Ready Tasks

When called with `list <n>` or just a number:

```bash
sqlite3 -header -column tasks.db "
SELECT t.id, t.summary, t.priority, t.domain, t.assignee
FROM tasks t
WHERE t.status = 'To Do'
  AND NOT EXISTS (
    SELECT 1 FROM task_dependencies d
    JOIN tasks blocker ON d.depends_on_id = blocker.id
    WHERE d.task_id = t.id AND blocker.status != 'Done'
  )
ORDER BY t.priority_score DESC, t.id
LIMIT <n>;
"
```

### Filter by Domain

When called with `domain <value>`:

Get next ready task for that domain only.

### Filter by Assignee

When called with `assignee <value>`:

Get next ready task for that assignee only.

### Show Blocked Tasks

When called with `blocked`:

```bash
sqlite3 -header -column tasks.db "
SELECT t.id, t.summary, t.priority,
  (SELECT GROUP_CONCAT(d.depends_on_id) FROM task_dependencies d WHERE d.task_id = t.id) as blocked_by
FROM tasks t
WHERE t.status = 'To Do'
  AND EXISTS (
    SELECT 1 FROM task_dependencies d
    JOIN tasks blocker ON d.depends_on_id = blocker.id
    WHERE d.task_id = t.id AND blocker.status != 'Done'
  )
ORDER BY t.id
"
```

### Show In Progress Tasks

When called with `wip` or `in-progress`:

```bash
sqlite3 -header -column tasks.db "SELECT id, summary, priority, domain, assignee, github_pr FROM tasks WHERE status = 'In Progress'"
```

### Show Tasks In Review

When called with `review` or `in-review`:

```bash
sqlite3 -header -column tasks.db "SELECT id, summary, priority, github_pr FROM tasks WHERE status = 'In Review'"
```

### Preview Next Task (without starting)

When called with `preview`:

Show the next ready task but do NOT start working on it. Just display the task details and stop.

```bash
sqlite3 -header -column tasks.db "
SELECT t.id, t.summary, t.priority, t.domain, t.assignee, t.description
FROM tasks t
WHERE t.status = 'To Do'
  AND NOT EXISTS (
    SELECT 1 FROM task_dependencies d
    JOIN tasks blocker ON d.depends_on_id = blocker.id
    WHERE d.task_id = t.id AND blocker.status != 'Done'
  )
ORDER BY t.priority_score DESC, t.id
LIMIT 1;
"
```

## Argument Parsing Summary

| Argument | Action |
|----------|--------|
| (none) | Get next ready task and automatically start working on it |
| `<id>` | Begin full workflow on task #id |
| `list <n>` | Show top N ready tasks |
| `done <id>` | Mark task as Done |
| `view <id>` | Show full task details |
| `domain <value>` | Filter next task by domain |
| `assignee <value>` | Filter next task by assignee |
| `blocked` | Show all blocked tasks |
| `wip` | Show all In Progress tasks |
| `review` | Show all In Review tasks with PR URLs |
| `preview` | Show next ready task without starting it |

## Important Guidelines

- Write tests for all tasks unless the task is untestable
- Ask clarifying questions if task requirements are ambiguous
- Use the TodoWrite tool to track progress within the task
- Make sure work is delegated to the correct subagent based on the assignee field
- Mark complete only when fully implemented and tested
- The widget at `~/.claude/widget.py` displays real-time task metrics while in progress
