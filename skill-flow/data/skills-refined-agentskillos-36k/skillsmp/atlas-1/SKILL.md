---
name: atlas
description: "Task execution engine with fresh context per task. Spawns sub-agents for complex implementation, runs simple tasks inline. Tracks state persistently, supports pause/resume across sessions."
---

# Atlas - Task Execution Engine

Autonomous agent loop for implementing tasks. Atlas picks tasks from TodoWrite and executes them systematically, using fresh sub-agent contexts for complex work to prevent context degradation.

---

## Overview

```
Pick ready task -> Decide inline vs sub-agent -> Implement -> Validate -> Commit -> Repeat
```

**Memory persists via:**
- **git commits** - Work history
- **STATE.md** - Current position + context notes
- **progress.txt** - Short-term learnings (current feature)
- **CLAUDE.md / AGENTS.md** - Long-term memory (codebase patterns)

---

## When to Use Atlas

| Scenario | Use |
|----------|-----|
| Tasks already planned (TodoWrite populated) | `run atlas` or `/atlas` |
| After `compound-engineering` plan phase | `run atlas` |
| After `build-feature` approval gate | Automatic |
| Need to plan first | Use `compound-engineering` or `build-feature` instead |

---

## Execution Loop

### Step 0: Read Current State

```bash
cat .claude/atlas/current-feature.txt
cat .claude/atlas/STATE.md
cat .claude/atlas/progress.txt
```

Check TodoWrite for current tasks and their status.

---

### Step 1: Find Ready Tasks

From TodoWrite, find tasks that are:
- `status: "pending"`
- All dependencies completed (earlier tasks in list are done)

**Skip container/parent tasks** - only work on leaf tasks.

---

### Step 2: If No Ready Tasks

Check if all tasks are completed:
- **If yes:** Signal completion (see Completion section)
- **If blocked:** Report which tasks are blocked and why

---

### Step 3: Execute Ready Task

**Pick the next task:**
- Prefer tasks related to what was just completed (same module/area)
- If no prior context, pick the first ready task

#### Decide: Inline vs Sub-Agent

**Run inline (same context) when:**
- Rename/move files
- Add/remove imports
- Fix typos or small bugs
- < ~15 lines changed
- Running npm commands
- Simple file edits

**Spawn sub-agent (fresh 200k context) when:**
- New component or file
- Significant logic changes (>15 lines)
- Multi-file changes
- Task requires understanding patterns from other files
- Complex implementation

---

### Step 4a: Inline Execution

For simple tasks:

1. **Mark as in_progress** via TodoWrite

2. **Implement directly** - Make the changes

3. **Run validation:**
   ```bash
   {{validate_cmd}}
   ```
   Fix any issues before proceeding.

4. **Update STATE.md** with new position

5. **Commit changes:**
   ```bash
   git add -A && git commit -m "feat: [task description]"
   ```

6. **Mark task complete** via TodoWrite

7. **Continue the loop** - go to Step 1

---

### Step 4b: Sub-Agent Execution

For complex tasks, spawn a fresh sub-agent with Opus model:

#### Prepare Context Bundle

Always include:
1. **Task description** - Full acceptance criteria from TodoWrite
2. **STATE.md** - Current position + context notes
3. **Feature context** - What we're building and why
4. **Project essentials** - Extracted from CLAUDE.md:
   - Code style rules
   - Key commands ({{validate_cmd}})
   - Component patterns
5. **Folder AGENTS.md** - If exists for target directory
6. **Related files to read** - Explicit paths the agent should Read first
7. **Pattern example** - "Follow the pattern in src/components/X"

Never include:
- Full CLAUDE.md (too long, dilutes focus)
- Unrelated architectural context
- Previous task details (fresh context = fresh start)

#### Sub-Agent Prompt Template

```markdown
You are implementing a task for the Atlas execution loop.

## Feature
[feature name and brief description]

## Your Task
[full task description with acceptance criteria]

## Context
[context notes from STATE.md]

## Read First
Before implementing, read these files to understand patterns:
- [file1]
- [file2]

## Project Rules
[key rules from CLAUDE.md - code style, imports, etc.]

## Follow This Pattern
[specific file to use as reference]

## Return
When complete, report:
1. Files changed
2. Any learnings/gotchas discovered
3. Any blockers or concerns
4. Confirmation that `{{validate_cmd}}` passes
```

#### Spawn the Agent

```
Task(subagent_type="general-purpose", model="opus"):
  [prepared prompt with context bundle]
```

#### Process Agent Result

1. **Review agent's report** - files changed, learnings, blockers
2. **Update STATE.md** with new position and any context notes
3. **Append learnings to progress.txt** (see format below)
4. **Commit changes:**
   ```bash
   git add -A && git commit -m "feat: [task description]"
   ```
5. **Mark task complete** via TodoWrite
6. **Continue the loop** - go to Step 1

---

### Step 5: Update Progress

After each task, append to progress.txt:

```markdown
## [Date] - [Task Title]
Task: [task description]
- What was implemented
- Files changed
- **Learnings:**
  - Patterns discovered
  - Gotchas encountered
---
```

---

## Multi-Model Routing

| Task Type | Model | When |
|-----------|-------|------|
| Complex implementation | Opus | Sub-agent tasks |
| Research/exploration | Sonnet | Explore agents |
| Code review | Sonnet | Review phase |
| Validation commands | Haiku | {{validate_cmd}} |
| Simple inline edits | Haiku | Typos, imports, renames |

**Default for work:** Opus (maintains quality)

---

## Task Discovery

While working, **create new tasks** when you discover:
- Failing tests or test gaps
- Code that needs refactoring
- Missing error handling
- TODOs or FIXMEs in the code
- Build/lint warnings

Add them via TodoWrite with appropriate position in the list.

---

## Browser Verification (UI Tasks)

For UI tasks, check if the `playwright-browser` skill is available:

```bash
test -f .claude/skills/playwright-browser/SKILL.md && echo "available" || echo "not installed"
```

**If available**, invoke the skill:
```
/skill playwright-browser
```

**Functional testing:**
```
browser_navigate(url: "{{dev_url}}/...")
browser_snapshot()  # Returns a11y tree as text
```

**If not available**, skip browser verification and note in progress.txt.

---

## Quality Requirements

Before marking ANY task complete:
- `{{validate_cmd}}` must pass
- Changes must be committed
- STATE.md must be updated
- Progress must be logged

---

## Pause & Resume

### Pausing Mid-Feature

Run `/atlas-pause` or say "pause atlas":

1. Update STATE.md with current position + context notes
2. Commit any uncommitted work as WIP
3. Report pause state

### Resuming

Run `/atlas-resume` or say "resume atlas":

1. Read STATE.md for position
2. Read progress.txt for recent learnings
3. Present state and ask for confirmation
4. Wait for user approval before continuing

See `.claude/commands/atlas-pause.md` and `.claude/commands/atlas-resume.md` for details.

---

## Completion

When all tasks are done:

**If running standalone:**

1. Archive progress:
   ```bash
   DATE=$(date +%Y-%m-%d)
   FEATURE=$(cat .claude/atlas/current-feature.txt | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
   mkdir -p .claude/atlas/archive/$DATE-$FEATURE
   mv .claude/atlas/progress.txt .claude/atlas/archive/$DATE-$FEATURE/
   ```

2. Reset for next feature:
   ```bash
   echo "" > .claude/atlas/current-feature.txt
   cat > .claude/atlas/STATE.md << 'EOF'
   # Atlas State

   ## Position
   - Feature: (none)
   - Task: 0 of 0
   - Last Commit: (none)

   ## Context Notes
   (No active feature)

   ## Deferred
   (none)
   EOF
   cat > .claude/atlas/progress.txt << 'EOF'
   # Atlas Progress Log
   (No active feature)
   EOF
   ```

3. Report completion:
   ```
   Atlas complete - all tasks finished!

   **Summary:**
   - [X] Task 1
   - [X] Task 2
   - [X] Task 3
   ...

   **Commits:** [list of commits]
   ```

**If running within build-feature orchestrator:**
Signal completion and return control for review phase. Do NOT archive - orchestrator handles that after compound phase.

---

## Relationship to Other Skills

```
compound-engineering    ->    atlas    ->    compound-engineering
   (Research + Plan)       (Execute)       (Review + Compound)
```

- **compound-engineering** owns: research, planning, review, compounding learnings
- **atlas** owns: task execution loop (inline + sub-agent)
- **build-feature** orchestrates: the full flow with approval gate

---

## Complete

When this skill completes:
- All TodoWrite tasks marked complete
- Each task validated with `{{validate_cmd}}`
- Each task committed individually
- STATE.md reflects completion
- Progress logged to `.claude/atlas/progress.txt`
- Progress archived (if running standalone)
- Summary of completed tasks reported

**Outputs:**
- Git commits for each completed task
- Updated TodoWrite with all tasks complete
- Archived progress file (standalone mode only)

**Ready for:** `/compound` to capture learnings, or code review
