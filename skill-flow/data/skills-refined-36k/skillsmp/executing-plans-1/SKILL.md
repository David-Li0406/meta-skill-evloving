---
name: executing-plans
description: Use when executing implementation plans with independent tasks in the current session
user-invocable: false
model: haiku
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read, Glob, Grep, Task
---

## Collab Session Required

Before proceeding, check for active collab session:

1. Check if `.collab/` directory exists
2. Check if any session folders exist within
3. If no session found:
   ```
   No active collab session found.

   Use /collab to start a session first.
   ```
   **STOP** - do not proceed with this skill.

4. If multiple sessions exist, check `COLLAB_SESSION_PATH` env var or ask user which session.

## Browser-Based Questions

When a collab session is active, use `render_ui` for all user interactions.

**Component selection:**
| Question Type | Component |
|--------------|-----------|
| Yes/No | Card with action buttons |
| Choose 1 of 2-5 | RadioGroup |
| Choose 1 of 6+ | MultipleChoice |
| Free text | TextInput or TextArea |

**Example - Yes/No:**
```
Tool: mcp__mermaid__render_ui
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "ui": {
    "type": "Card",
    "props": { "title": "<question context>" },
    "children": [{ "type": "Markdown", "props": { "content": "<question>" } }],
    "actions": [
      { "id": "yes", "label": "Yes", "primary": true },
      { "id": "no", "label": "No" }
    ]
  },
  "blocking": true
}
```

**Terminal prompts only when:** No collab session exists (pre-session selection).

# Executing Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create TodoWrite and proceed

### Step 1.1: Parse Task Dependency Graph (Collab Workflow)

When called from `rough-draft` within a collab workflow, the plan includes a task dependency graph. Parse and prepare for intelligent execution.

**Graph Format (YAML in design doc):**
```yaml
tasks:
  - id: auth-types
    files: [src/auth/types.ts]
    description: Core auth type definitions
    parallel: true

  - id: auth-service
    files: [src/auth/service.ts]
    description: Authentication service implementation
    depends-on: [auth-types]

  - id: auth-middleware
    files: [src/middleware/auth.ts]
    description: Express middleware for auth
    depends-on: [auth-service]
```

**Parsing Steps:**
1. Extract YAML block from design doc (look for `## Task Dependency Graph`)
2. Parse task list with: `id`, `files`, `description`, `parallel`, `depends-on`
3. Build adjacency list for dependency relationships
4. Validate: check for cycles (topological sort must succeed)
5. If cycle detected: STOP and report error to user

**Build Execution Order:**
1. Topological sort on dependency graph
2. Group tasks by "wave" (tasks with all dependencies satisfied)
3. Within each wave, identify parallel-safe tasks (those with `parallel: true` or independent file sets)

**Execution State Tracking:**

Initialize task tracking via MCP:

```
Tool: mcp__mermaid__update_session_state
Args: {
  "project": "<cwd>",
  "session": "<name>",
  "phase": "implementation",
  "completedTasks": [],
  "pendingTasks": ["task-1", "task-2", "task-3"],
  "pendingVerificationIssues": []
}
```
Note: `lastActivity` is automatically updated by the MCP tool.

### MANDATORY: Subagent Dispatch

**GATE:** Implementation MUST use the Task tool with subagent-driven-development skill.

**NEVER implement inline** - always dispatch a Task agent for each implementation task.

This is a hard requirement, not a suggestion. If you find yourself writing implementation code directly instead of spawning a Task agent, STOP immediately.

**Why this matters:**
- Task agents invoke subagent-driven-development which enforces TDD
- Spec compliance review only happens in subagent flow
- Code quality review only happens in subagent flow
- Skipping this means skipping ALL quality gates

**Pre-Task Checklist (before starting ANY task):**
- [ ] Will spawn a Task agent (not implement inline)
- [ ] Task prompt includes design doc location
- [ ] Task prompt specifies subagent-driven-development skill

**Post-Task Checklist (before marking ANY task complete):**
- [ ] Task agent was spawned (verified Task tool was used)
- [ ] subagent-driven-development skill was invoked by the agent
- [ ] Spec compliance review passed
- [ ] Code quality review passed

**If ANY checklist item fails:** Do NOT mark task as complete. Fix the issue first.

---

### Anti-Drift Rules

**NO INTERPRETATION:**
- Implement EXACTLY what the plan says, even if you think there's a better way
- If the plan says "create function foo(x) that returns x+1" - do that, not "a more flexible version"
- If something seems wrong or suboptimal, STOP and ask - do not "fix" it silently
- Your job is execution, not design improvement

**NO SHORTCUTS:**
- Complete every step in order, even if you "know" the outcome
- Run every test command, even if you're "sure" it will pass
- Write every file listed, even if you think some are "unnecessary"
- If a step feels redundant, do it anyway - the plan author had a reason

**DESIGN VERIFICATION:**
- Before each task: re-read the relevant design doc section
- If mermaid-collab diagrams are referenced, open and verify against them
- After each task: diff your implementation against the spec - EXACT match required
- Any deviation = undo and redo, or STOP and ask

**When in doubt:** Ask, don't improvise.

### Design Freeze

Once execution begins, the design is FROZEN.

**No changes during implementation:**
- No "small tweaks" to requirements
- No "I realized we need X" additions
- No "let's just add this while we're here"
- No scope creep, no matter how reasonable it sounds

**If something needs to change:**
1. STOP execution immediately
2. Document what needs to change and why
3. Go back to design doc - update it formally
4. Update the plan to reflect changes
5. THEN resume execution

**Why this matters:**
- Mid-implementation changes cause drift
- "Quick additions" compound into chaos
- The plan is a contract - honor it

### Step 1.5: Pre-Flight Check

Before executing ANY tasks, verify:
- [ ] Design doc exists and is complete
- [ ] All referenced mermaid-collab diagrams exist and are accessible
- [ ] No ambiguous requirements in the plan
- [ ] Every task has explicit file paths and pseudo code

**If anything is missing:** STOP. Go back to brainstorming/writing-plans. Do not proceed with incomplete specs.

### Step 1.6: Create Task Execution Diagram (MANDATORY)

**REQUIREMENT:** Always create a task execution diagram at the start of implementation. Never skip this step.

When within a collab workflow, create a visual diagram showing all tasks and their dependencies. This diagram serves as a live progress tracker throughout implementation.

**Build diagram content from task dependency graph:**

Extract task information from the design doc's task dependency graph YAML and build a Mermaid graph:

```
graph TD
    %% Node Definitions (one per task)
    <for each task: task-id(["task-id"])>

    %% Dependencies (arrow from dependency to dependent)
    <for each dependency: dep-id --> task-id>

    %% Styles (all waiting initially)
    <for each task: style task-id fill:#e0e0e0,stroke:#9e9e9e>
```

**Create the diagram:**
```
Tool: mcp__mermaid__create_diagram
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "name": "task-execution",
  "content": <generated-mermaid-content>
}
```

**Display to user:**
```
Task execution diagram created: <preview-url>

Tracking tasks:
- task-1 (dependency root)
- task-2 (depends on task-1)
[etc.]
```

**State tracking - Style definitions:**
| State | Style | Meaning |
|-------|-------|---------|
| waiting | `fill:#e0e0e0,stroke:#9e9e9e` | Task queued, waiting for dependencies |
| executing | `fill:#bbdefb,stroke:#1976d2,stroke-width:3px` | Task currently being implemented |
| completed | `fill:#c8e6c9,stroke:#2e7d32` | Task finished and verified |
| failed | `fill:#ffcdd2,stroke:#c62828` | Task encountered error |

**Update diagram on state change:**

Use `patch_diagram` for atomic style updates when task state changes:

```
Tool: mcp__mermaid__patch_diagram
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "id": "task-execution",
  "old_string": "style <task-id> fill:#e0e0e0,stroke:#9e9e9e",
  "new_string": "style <task-id> fill:#bbdefb,stroke:#1976d2,stroke-width:3px"
}
```

If `patch_diagram` fails (old_string not found), use `update_diagram` instead.

**Helper function pseudocode:**

```
FUNCTION buildTaskDiagram(taskDependencyGraph):
  nodes = []
  edges = []
  styles = []

  FOR EACH task IN taskDependencyGraph.tasks:
    nodes.append(`${task.id}(["${task.id}"])`)
    styles.append(`style ${task.id} fill:#e0e0e0,stroke:#9e9e9e`)

    FOR EACH dependency IN task.depends-on:
      edges.append(`${dependency} --> ${task.id}`)

  content = "graph TD\n"
  content += "    %% Node Definitions\n"
  content += nodes.join("\n    ") + "\n"
  content += "\n    %% Dependencies\n"
  content += edges.join("\n    ") + "\n"
  content += "\n    %% Styles\n"
  content += styles.join("\n    ")

  RETURN content
```

### Step 1.7: Verify Task Diagram Created

**REQUIRED:** Verify the task execution diagram exists before proceeding to execution.

```
Tool: mcp__mermaid__get_diagram
Args: { "project": "<cwd>", "session": "<session>", "id": "task-execution" }
```

**If diagram not found:**
```
Task execution diagram not found. Creating now...
```
-> Return to Step 1.6 and create the diagram.

**If diagram exists:**
```
Task execution diagram verified. Proceeding to execution.
```
-> Proceed to Step 2.

**This gate ensures the diagram is always created before any tasks execute.**

### Step 1.8: Understand Item Types and Execution Paths

**CONTEXT:** Within collab workflows, items come from the design doc with a `type` field. The execution path differs based on this type.

**Item Types:**
- **code:** New features, implementations, refactoring, investigations -> uses test-driven-development (TDD)
- **bugfix:** Bug fixes, crashes, errors -> uses test-driven-development (TDD)
- **task:** Operational tasks (docker setup, installs, configuration, organization) -> skips TDD, executes directly

**How to Determine Item Type:**

1. Read the design doc
2. For each work item in the "Work Items" section, check the `Type:` field
3. The current item being executed should have an associated type from the design doc

**Execution Logic by Type:**

| Type | Execution Flow |
|------|----------------|
| code/bugfix | Invoke test-driven-development skill -> Write failing test -> Implement -> Verify test passes |
| task | Execute task steps directly -> Run verification checks |

**Task Type Items:**
- Use phases from task-planning: Prerequisites -> Steps -> Verification
- Prerequisites define what must exist before starting
- Steps are ordered commands/actions to execute
- Verification confirms success
- No TDD cycle needed (these are operational, not code)

**Code/Bugfix Type Items:**
- Follow standard TDD flow with red-green-refactor
- Still require verification but through test suite

## Step 2: Execute Batch

Execute tasks following the dependency graph, dispatching parallel-safe tasks together.

**Invoke skill: executing-plans-execution** for detailed execution logic, task routing, and agent prompts.

Key points:
- Standard execution: First 3 tasks in sequence
- Collab workflow: Use dependency-aware parallel dispatch
- Always spawn Task agents - never implement inline
- Update task diagram on state changes

## Verification and Review

After each task completes, verify implementation against design and check for drift.

**Invoke skill: executing-plans-review** for detailed verification, drift detection, and snapshot logic.

Key points:
- Per-task verification compares output against design doc
- Drift detection identifies mismatches with pros/cons analysis
- Snapshots enable recovery after context compaction
- Proposing design changes uses special markdown tags

### Step 3: Report
When batch complete:
- Show what was implemented
- Show verification output (including any drift decisions)
- Say: "Ready for feedback."

### Step 4: Continue
Based on feedback:
- Apply changes if needed
- Execute next batch
- Repeat until complete

### Step 5: Complete Development

After all tasks complete and verified, show summary and ask for confirmation:

```
Implementation complete:
- [N] tasks completed: [list task IDs]
- All tests passing
- All TODOs resolved

Ready to move to finishing-a-development-branch?

1. Yes
2. No
```

- If **1 (Yes)**: Invoke finishing-a-development-branch skill
- If **2 (No)**: Ask what needs to be addressed

**On confirmation:**
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

### Step 5.1: Offer Collab Cleanup (Within Collab Workflow)

**REQUIRED** when executing within a collab session:

After development work completes (whether through finishing-a-development-branch or direct user commands like "commit and push"), always offer collab session cleanup:

```
Development complete.

Clean up collab session? This will archive or delete design artifacts.
Run /collab-cleanup?

1. Yes
2. No
```

- If **1 (Yes)**: Invoke collab-cleanup skill
- If **2 (No)**: "Session kept open. Run `/collab-cleanup` when ready."

**This step ensures users always get the option to clean up, regardless of how they chose to finish the work.**

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Between batches: just report and wait
- Stop when blocked, don't guess

## Integration with Collab Workflow

This skill can be invoked in two contexts:

### Standalone (Traditional)
- Called directly by user with a plan file
- No dependency graph
- Standard batch execution (3 tasks at a time)
- Uses `writing-plans` output format

### Within Collab Workflow
- Called by `rough-draft` skill after skeleton phase completes
- Receives task dependency graph from design doc
- Uses dependency-aware parallel execution
- Per-task verification via `verify-phase` hook
- On completion, triggers `collab-cleanup` hook

**Collab Workflow Chain:**
```
collab -> brainstorming -> rough-draft -> executing-plans -> finishing-a-development-branch
                                            ^
                                     (you are here)
```

**When called from rough-draft:**
1. Design doc is already complete with task dependency graph
2. Skeleton files already exist with TODOs
3. Your job: implement TODOs respecting dependency order
4. Parallel dispatch independent tasks via `subagent-driven-development`
5. Verify each task against design before unlocking dependents

## Sub-Skills

- **executing-plans-execution** - Detailed task execution logic, routing, and agent prompts
- **executing-plans-review** - Verification, drift detection, and snapshot saving
