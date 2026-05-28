---
name: gobby-plan
description: This skill should be used when the user asks to "/gobby-plan", "create plan", "plan feature", "write specification". Guide users through structured specification planning and task creation.
version: "1.0"
---

# /gobby-plan - Implementation Planning Skill

Guide users through structured requirements gathering, specification writing, and task creation.

## Workflow Overview

1. **Requirements Gathering** - Ask questions to understand the feature
2. **Draft Plan** - Write structured plan document
3. **Plan Verification** - Check for TDD anti-patterns and dependency issues
4. **User Approval** - Present plan for review
5. **Task Creation** - Create tasks from approved plan
6. **Task Verification** - Update plan with task refs

## Step 0: **REQUIRED** ENTER PLAN MODE

Before creating any plan, you must enter Claude Code's plan mode to explore the codebase
and design the implementation approach.

**How to enter**: Use the `EnterPlanMode` tool or respond with a planning-focused message
that triggers plan mode. Plan mode allows you to read files and design without making edits.

**Why required**: Plan creation requires understanding existing code patterns, architecture
constraints, and dependencies before proposing new work.

## Step 1: Requirements Gathering

Ask the user:
1. "What is the name/title for this feature or project?"
2. "What is the high-level goal? (1-2 sentences)"
3. "Are there any constraints or requirements I should know about?"
4. "What are the unknowns or risks?"

## Step 2: Draft Plan Structure

Create a plan with:
- **Epic title**: The overall feature name
- **Phases**: Logical groupings of work (e.g., "Foundation", "Core Implementation", "Polish")
- **Tasks**: Atomic units of work under each phase
- **Dependencies**: Which tasks block which (use notation: `depends: #N` or `depends: Phase N`)

## Step 3: Write Plan Document

Write to `.gobby/plans/{kebab-name}.md`:

```markdown
# {Epic Title}

## Overview
{Goal and context from Step 1}

## Constraints
{Constraints from Step 1}

## Phase 1: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 1 title
- [ ] Task 2 title (depends: Task 1)
- [ ] Task 3 title (parallel)

## Phase 2: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 4 (depends: Phase 1)
- [ ] Task 5 (parallel with Task 4)

## Task Mapping

<!-- Updated after task creation -->
| Plan Item | Task Ref | Status |
|-----------|----------|--------|
```

**Dependency Notation:**
- Use `(depends: Task 1)` or `(depends: Phase N)` in markdown
- Dependencies are resolved when tasks are created via `create_task` with `parent_task_id`

## Step 4: Plan Verification (REQUIRED)

Before presenting to the user, verify the plan does NOT contain TDD anti-patterns:

### Check 1: No Explicit Test Tasks

Scan for tasks that should NOT exist (TDD sandwich creates these automatically):

**FORBIDDEN patterns - remove these if found:**
- `"Write tests for..."` or `"Add tests for..."`
- `"Test..."` as task title prefix
- `"[TDD]..."` or `"[IMPL]..."` or `"[REF]..."`
- `"Ensure tests pass"` or `"Run tests"`
- `"Add unit tests"` or `"Add integration tests"`
- Any task with `test` as the primary verb

**ALLOWED (these are fine):**
- `"Add TestClient fixture"` (not a test task, but test infrastructure)
- `"Configure pytest settings"` (configuration, not test writing)

### Check 2: Dependency Tree Validation

Verify the dependency structure is valid:

1. **No circular dependencies**: Task A → B → A is invalid
2. **No missing dependencies**: If Task B depends on Task A, Task A must exist
3. **Phase dependencies are valid**: `depends: Phase N` must reference an existing phase
4. **Leaf tasks are implementation work**: Bottom-level tasks should be concrete work, not meta-tasks

### Check 3: Task Categorization

Ensure each task has a valid category:
- `code` - Implementation tasks (gets TDD triplets)
- `config` - Configuration changes (gets TDD triplets)
- `docs` - Documentation tasks (no TDD)
- `test` - Test infrastructure (no TDD)
- `research` - Investigation tasks (no TDD)
- `planning` - Architecture/design (no TDD)
- `manual` - Manual verification (no TDD)

### Verification Output

After verification, report:
```
Plan Verification:
✓ No explicit test tasks found
✓ Dependency tree is valid (no cycles, all refs exist)
✓ Categories assigned correctly

Ready for user approval.
```

Or if issues found:
```
Plan Verification:
✗ Found 2 explicit test tasks (removed):
  - "Add tests for user authentication" → REMOVED
  - "Ensure all tests pass" → REMOVED
✓ Dependency tree is valid
✓ Categories assigned correctly

Plan updated. Ready for user approval.
```

## Step 5: User Approval

Present the plan to the user:
- Show the full plan document
- Show verification results
- Ask: "Does this plan look correct? Would you like any changes before I create tasks?"
- Make changes if requested
- Once approved, proceed to task creation

## Step 6: Task Creation

**IMPORTANT**: `expand_task` creates FLAT children only - it does not create nested hierarchies.
To get a proper Epic → Phases → Tasks structure, you must create the hierarchy manually.

**Required: session_id** - All `create_task` calls require a `session_id` parameter. Find your session ID in the SessionStart hook context (look for `session_id: <uuid>` in the startup system reminder).

### 6a. Create the Root Epic

```python
epic = call_tool("gobby-tasks", "create_task", {
    "title": "{Epic Title}",
    "task_type": "epic",
    "description": "See .gobby/plans/{name}.md",
    "session_id": "<your_session_id>"
})
# Returns: {"ref": "#42", ...}
```

### 6b. Create Phase Epics Manually

For EACH phase in your plan, create a child epic. Include the phase's task list in the description
so `expand_task` knows what leaf tasks to create:

```python
# Phase 1
phase1 = call_tool("gobby-tasks", "create_task", {
    "title": "Phase 1: {Phase Name}",
    "task_type": "epic",
    "parent_task_id": "#42",  # Root epic ref
    "description": "{Phase goal}\n\nTasks:\n- Task 1 title (category: code)\n- Task 2 title (category: code)\n- Task 3 title (category: config)",
    "session_id": "<your_session_id>"
})
# Returns: {"ref": "#43", ...}

# Phase 2
phase2 = call_tool("gobby-tasks", "create_task", {
    "title": "Phase 2: {Phase Name}",
    "task_type": "epic",
    "parent_task_id": "#42",
    "description": "{Phase goal}\n\nTasks:\n- Task 4 title (category: code)\n- Task 5 title (category: docs)",
    "session_id": "<your_session_id>"
})
# ... repeat for each phase in the plan
```

### 6c. Create Feature Tasks Under Each Phase

For EACH feature task listed in your plan, create it as a child of the appropriate phase epic.
Include the `category` so TDD knows whether to apply triplets:

```python
# Feature tasks under Phase 1 (#43)
call_tool("gobby-tasks", "create_task", {
    "title": "Create protocol.py with type definitions",
    "task_type": "task",  # NOT epic
    "parent_task_id": "#43",  # Phase 1 epic ref
    "category": "code",  # code/config gets TDD, docs/research/planning don't
    "description": "Implementation details...",
    "session_id": "<your_session_id>"
})
# Returns: {"ref": "#45", ...}

call_tool("gobby-tasks", "create_task", {
    "title": "Create backends/__init__.py with factory",
    "task_type": "task",
    "parent_task_id": "#43",
    "category": "code",
    "description": "Implementation details...",
    "session_id": "<your_session_id>"
})
# Returns: {"ref": "#46", ...}

# ... repeat for all feature tasks in the plan
```

**IMPORTANT**: Create feature tasks as `task_type: "task"` (not epic). TDD triplets are
only applied when expanding tasks, NOT epics.

### 6d. Expand Feature Tasks for TDD Triplets

Now expand each **feature task** (NOT the phase epics!) to get TDD triplets:

```python
# Expand feature task #45 - this creates TDD triplets
call_tool("gobby-tasks", "expand_task", {
    "task_id": "#45",  # Feature task, NOT phase epic
    "session_id": "<your_session_id>"
})

# Expand feature task #46
call_tool("gobby-tasks", "expand_task", {
    "task_id": "#46",
    "session_id": "<your_session_id>"
})

# ... repeat for each feature task
```

**Why expand feature tasks, not phase epics?**
- TDD is explicitly SKIPPED when `task.task_type == "epic"` (line 496 in task_expansion.py)
- Expanding a phase epic creates feature tasks BUT without TDD triplets
- Expanding a feature task creates implementation subtasks WITH TDD triplets

**What expand_task does per feature task:**
- LLM reads the task title + description
- Creates implementation subtasks (granular work items)
- TDD steps embedded in code/config task descriptions
- Sets `is_expanded=True` on the feature task

### 6e. Update Plan Doc with Task Refs

After all expansions complete:

```python
# Get the full task tree
call_tool("gobby-tasks", "list_tasks", {
    "parent_task_id": "#42",
    "session_id": "<your_session_id>"
})
```

- Fill in Task Mapping table with created task refs
- Use Edit tool to update `.gobby/plans/{name}.md`

## Step 7: Task Verification

After creating all tasks:
1. Show the created task tree (call `list_tasks` with `parent_task_id`)
2. Confirm task count matches plan items
3. Show the updated plan doc with task refs

## Task Granularity Guidelines

Each task should be:
- **Atomic**: Completable in one AI session 
- **Testable**: Has clear pass/fail criteria
- **Verb-led**: Starts with action verb (Add, Create, Implement, Update, Remove)
- **Scoped**: References specific files/functions when possible

Good: "Add TaskEnricher class to src/gobby/tasks/enrich.py"
Bad: "Implement enrichment" (too vague)

## TDD Compatibility (IMPORTANT)

The /gobby-plan skill creates **feature tasks** knowing that `expand_task` will apply TDD triplets to each one.

### TDD Triplet Pattern

Each feature task (category: code) gets expanded into three children:
- **[TDD]** - Write failing tests first
- **[IMPL]** - Make tests pass
- **[REF]** - Refactor while keeping tests green

```
Feature Task
├── [TDD] Write failing tests for feature
├── [IMPL] Implement feature
└── [REF] Clean up, verify tests pass
```

### Task Categories

Valid categories (from `src/gobby/storage/tasks.py`):
- `code` - Implementation tasks (gets TDD triplets)
- `config` - Configuration changes (gets TDD triplets)
- `docs` - Documentation tasks (no TDD)
- `refactor` - Refactoring tasks, including updating existing tests (no TDD)
- `test` - Test infrastructure tasks (fixtures, helpers) (no TDD)
- `research` - Investigation tasks (no TDD)
- `planning` - Architecture/design tasks (no TDD)
- `manual` - Manual functional testing (observe output) (no TDD)

### What You Create vs What expand_task Produces

**DO NOT manually create:**
- `[TDD]`, `[IMPL]`, `[REF]` prefixed tasks
- "Write tests for: ..." tasks
- "Ensure tests pass" tasks
- Separate test tasks alongside implementation

**DO create:**
- Feature tasks with `category: "code"` or `category: "config"`
- Documentation tasks with `category: "docs"`

**Example - Two-step creation process:**

**Step 1: Skill creates Levels 1-3 manually via create_task:**

```
#100 [epic] Memory V3 Backend                    ← L1: Root Epic
├── #101 [epic] Phase 1: Backend Setup           ← L2: Phase Epic
│   ├── #102 [task] Create protocol.py (code)    ← L3: Feature Task
│   ├── #103 [task] Create backends/__init__.py  ← L3: Feature Task
│   └── #104 [task] Add config schema (config)   ← L3: Feature Task
└── #105 [epic] Phase 2: Integration             ← L2: Phase Epic
    └── ...
```

**Step 2: Expand each feature task to get TDD triplets (Level 4):**

```python
expand_task(task_id="#102")  # Feature task, NOT phase epic
expand_task(task_id="#103")
expand_task(task_id="#104")
```

**Result after expansion:**

```
#100 [epic] Memory V3 Backend                      L1
├── #101 [epic] Phase 1: Backend Setup             L2
│   ├── #102 [task] Create protocol.py             L3 (is_expanded=True)
│   │   ├── #105 Define MemoryCapability enum      L4
│   │   ├── #106 Define MemoryQuery dataclass      L4
│   │   └── #107 Add type exports                  L4
│   ├── #103 [task] Create backends/__init__.py    L3 (is_expanded=True)
│   │   ├── #108 Implement get_backend()           L4
│   │   └── #109 Add backend registry              L4
│   └── #104 [task] Add config schema              L3 (is_expanded=True)
│       ├── #110 Add memory.backend option         L4
│       └── #111 Add validation                    L4
```

### 3-Level Hierarchy

```
L1: Root Epic (created manually)
└── L2: Phase Epic (created manually)
    └── L3: Feature Task (created manually, category: code/config)
        └── L4: Implementation subtasks (created by expand_task)
```

**NOTE**: TDD steps are embedded in task descriptions for code/config category tasks.
The descriptions include test requirements that agents follow during implementation.

## Example Usage

User: `/gobby-plan`
Agent: "What feature would you like to plan?"
User: "Add dark mode support to the app"
Agent: [Asks clarifying questions]
Agent: [Writes plan to .gobby/plans/dark-mode.md]
Agent: [Runs verification - removes any test tasks found]
Agent: "Here's the plan. Does this look correct?"
User: "Yes, create the tasks"
Agent: [Creates epic + phases + tasks]
Agent: "Created 12 tasks under epic #47. The plan has been updated with task refs."

## Optional: Workflow-Enforced Planning

For stricter enforcement of the planning process with step gates and tool restrictions,
you can activate the `plan-expansion` workflow instead of following this skill manually.

### When to Use the Workflow

Use the workflow when you want:
- **Hard step gates** - Can't proceed to task creation without approval
- **Tool restrictions** - Edit/Write blocked during discovery and gather phases
- **Loop enforcement** - Expansion loop can't be skipped or abandoned
- **State persistence** - Workflow state survives context compaction

### How to Activate

After gathering requirements (Step 1), activate the workflow:

```python
call_tool("gobby-workflows", "activate_workflow", {
    "name": "plan-expansion",
    "variables": {
        "context_analyzed": false,  # Start from discovery
        "apc_choice": null
    }
})
```

Or skip discovery if you've already analyzed the codebase:

```python
call_tool("gobby-workflows", "activate_workflow", {
    "name": "plan-expansion",
    "step": "gather",  # Start from requirements elicitation
    "variables": {
        "context_analyzed": true
    }
})
```

### Workflow Steps

1. **discover** - Analyze existing context (blocks Edit/Write)
2. **gather** - A/P/C elicitation menu (blocks Edit/Write)
3. **draft_plan** - Write plan document (only .gobby/plans/ allowed)
4. **verify_plan** - Check structure and dependencies
5. **create_hierarchy** - Create epic → phase → task structure
6. **expand_loop** - Auto-expand feature tasks with TDD
7. **cleanup** - Evaluate tree, fix deps, identify duplicates, offer cleanup
8. **verify_tasks** - Confirm task tree and update plan
9. **complete** - Workflow finished

### Hybrid Approach

The skill and workflow are complementary:
- **Skill**: Interactive flexibility for requirements and drafting
- **Workflow**: Deterministic expansion with enforced gates

Recommended pattern:
1. Use this skill for Steps 1-5 (requirements through approval)
2. Activate `plan-expansion` workflow at Step 6 (task creation)
3. Workflow handles expansion loop deterministically
