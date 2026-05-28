---
name: edge-context
description: Load project state and workflow context before starting any coding task. Use automatically when beginning work, implementing features, fixing bugs, or continuing a project.
---

# Load Project Context

This skill loads the current project state from `active_context.yaml` and provides orientation for the upcoming work.

## When This Skill Activates

This skill should trigger implicitly when:
- Starting work on a new task
- Beginning a coding session
- Resuming work on a project
- The user says "let's work on...", "implement...", "fix...", "continue..."

## Instructions

### 0. Bootstrap State File (if missing)

**FIRST**, check if `active_context.yaml` exists in the project root.

If it does NOT exist, create it with this template:

```yaml
# Operator's Edge - Active Context
# This file tracks your workflow state

objective: null
current_step: 0
plan: []
constraints: []
memory: []
```

Then inform the user:
```
Created active_context.yaml - Operator's Edge is now initialized.
Run $edge-plan to create your first plan.
```

### 1. Read Current State

Load `active_context.yaml` from the project root and extract:
- `objective`: Current goal
- `current_step`: Which step to work on
- `plan`: List of steps and their status
- `constraints`: Things that must NOT happen
- `memory`: Relevant lessons from past work

### 2. Check Workflow Status

Determine the current state:

| Condition | Status | Action |
|-----------|--------|--------|
| No objective or empty plan | Needs Planning | Suggest `$edge-plan` |
| Has plan, step in_progress | Resume Work | Continue current step |
| Has plan, all pending | Ready to Start | Suggest `$edge-step` |
| Has plan, all completed | Work Complete | Suggest review or new objective |

### 3. Surface Relevant Memory

Scan the `memory` section for lessons whose triggers match the current task keywords.

For each matching lesson, display:
```
RELEVANT LESSON: [trigger]
  [lesson text]
  (reinforced N times)
```

### 4. Display Context Summary

Output a summary like:

```
OPERATOR'S EDGE - Context Loaded

Objective: [objective text]
Progress: [N/M] steps completed
Current: Step [N] - [description]

Status: [READY | IN_PROGRESS | NEEDS_PLAN | COMPLETE]

Constraints:
  - [constraint 1]
  - [constraint 2]

Relevant Lessons:
  - [lesson 1]
  - [lesson 2]

Next Action: [suggested skill to run]
```

### 5. Three Gears Mode

Determine the current "gear" based on state:

| Gear | Condition | Behavior |
|------|-----------|----------|
| ACTIVE | Has objective + plan with pending/in_progress steps | Execute work |
| PATROL | Objective complete OR no steps in progress | Review, validate, suggest |
| DREAM | No objective, empty plan | Explore, brainstorm, propose |

Display the current gear:
```
Current Gear: [ACTIVE | PATROL | DREAM]
```

## Output Format

```
========================================
OPERATOR'S EDGE - Codex CLI Edition
========================================

Gear: [ACTIVE | PATROL | DREAM]

Objective: [objective or "Not set"]
Progress: [N/M steps] | Current: Step [N]

Status: [description of current state]

Constraints:
  - [list constraints]

Memory (relevant to this task):
  - [matching lessons]

Suggested Action: $[skill-name]
========================================
```

## Why This Matters

Without automatic hooks, this skill provides the "session start" context that Claude Code injects automatically. Running this skill:
1. Orients you to the current work
2. Surfaces relevant lessons
3. Prevents starting work without a plan
4. Maintains workflow discipline

## Tip

If Codex doesn't invoke this skill automatically, explicitly run `$edge-context` at the start of each session to load state.
