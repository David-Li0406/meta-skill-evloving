---
name: eiffel-tasks
description: Phase 3 of Eiffel Spec Kit. Breaks reviewed contracts into implementation tasks with acceptance criteria. Use with /eiffel.tasks command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.tasks - Phase 3: Task Decomposition

**Purpose:** Break contracts into implementable chunks with clear acceptance criteria.

## Usage

```
/eiffel.tasks <project-path>
```

**Example:**
```
/eiffel.tasks d:\prod\simple_cache
```

## Project Scoping

All files are created inside the PROJECT directory:
```
<project-path>/
├── .eiffel-workflow/
│   ├── tasks.md                       (implementation tasks)
│   ├── prompts/
│   │   └── phase3-task-review.md      (optional AI review)
│   └── evidence/
│       └── phase3-tasks.txt
```

## Prerequisites

- Phase 2 complete: `<project-path>/.eiffel-workflow/synopsis.md` exists and approved

## Workflow

### Step 1: Read Inputs

Read:
- `<project-path>/src/*.e` (contracts)
- `<project-path>/.eiffel-workflow/approach.md` (implementation strategy)
- `<project-path>/.eiffel-workflow/synopsis.md` (resolved issues)

### Step 2: Generate Tasks

Create `<project-path>/.eiffel-workflow/tasks.md`:

```markdown
# Implementation Tasks: [Library Name]

## Task 1: [Feature/Component Name]
**Files:** src/[file].e
**Features:** [feature_name], [feature_name]

### Acceptance Criteria
- [ ] Preconditions satisfied
- [ ] Postconditions verified by contracts
- [ ] Compiles clean
- [ ] Skeletal tests pass

### Implementation Notes
[From approach.md - relevant algorithm details]

### Dependencies
[Other tasks that must complete first]

---

## Task 2: [Next Feature]
...
```

### Step 3: Generate Optional AI Review Prompt

Create `<project-path>/.eiffel-workflow/prompts/phase3-task-review.md`:

```markdown
# Task Completeness Review

Review the task breakdown for completeness.

## Check For:
- Features in contracts not covered by tasks
- Missing dependencies between tasks
- Tasks too large (should be split)
- Tasks too small (should be combined)

## Tasks
[PASTE tasks.md]

## Contracts
[PASTE src/*.e]

## Output
List any gaps or issues found.
```

### Step 4: Human Approval

Present task list and ask:

**"[N] tasks identified. Review the task breakdown. Approve to proceed to Phase 4 (Implementation)?"**

**DO NOT PROCEED until user explicitly approves.**

### Step 5: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase3-tasks.txt`:
```
# Phase 3 Task Evidence
# Project: <project-path>
# Date: [timestamp]

Tasks created: [count]
Dependencies identified: [count]
Human approved: [yes/no]

# Status: APPROVED
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context
- Keep large file contents in working memory

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Ask targeted questions when task dependencies involve external libraries
- Release context after getting answers

**Example - Ecosystem Query:**
```
Task depends on simple_mml patterns? Don't read all its files.
Instead: Task(subagent_type=Explore) → "How does simple_mml handle set operations?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Completion

```
Phase 3 COMPLETE: Tasks defined.
Project: <project-path>

Task file: .eiffel-workflow/tasks.md
Task count: [N]

Next: Run /eiffel.implement <project-path> to write feature bodies.
```
