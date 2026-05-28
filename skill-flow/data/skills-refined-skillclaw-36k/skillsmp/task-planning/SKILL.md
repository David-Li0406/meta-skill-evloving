---
name: task-planning
description: Plan operational tasks (docker, installs, organization) that skip TDD
user-invocable: false
model: opus
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read, Glob, Grep
---

# Task Planning Skill

## Overview

The **task-planning** skill guides planning of operational tasks that don't require test-driven development. Unlike feature work (which goes through brainstorming → rough-draft → TDD), operational tasks follow a simpler path: brainstorming → task-planning → direct execution.

This skill is invoked internally by the collab workflow for items classified as "task" type (docker, installs, configuration, organization, cleanup, deployment).

## When to Use

- After brainstorming completes for a "task" type work item
- For operational work that doesn't involve code implementation with tests
- When planning: docker container setup, library installations, folder organization, deployment procedures, cleanup tasks

## Collab Session Required

This skill operates within an active collab session. It reads the current work item from the session's design document and updates it with planning phases.

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

```
Collab Session Structure:
.collab/[session-name]/
├── design.md                 (updated with Prerequisites/Steps/Verification)
├── collab-state.json        (contains currentItem reference)
└── context-snapshot.json    (saved at phase transitions)
```

## The Process

### Phase 1: Prerequisites

Identify what must exist before the task can start.

**Steps:**
1. Read the design.md file for the current work item
2. Ask: "What needs to exist before starting this task?"
   - Example: Docker installed, project repository cloned, user has admin access
3. For each prerequisite identified:
   - Document the prerequisite name
   - Document how to check if it exists
4. Ask: "Anything else that needs to exist?"
5. When user confirms prerequisites are complete, save snapshot and proceed to Steps phase

**Snapshot Saving:**
```
// After each prerequisite documented, save to preserve context
Tool: mcp__mermaid__save_snapshot
Args: {
  "project": "<cwd>",
  "session": "<session-name>",
  "activeSkill": "task-planning",
  "currentStep": "prerequisites",
  "pendingQuestion": "Are there more prerequisites?",
  "inProgressItem": currentItem,
  "recentContext": []
}
// Note: version and timestamp are automatically added
```

### Phase 2: Steps

Define the ordered sequence of commands/actions to complete the task.

**Steps:**
1. Ask: "What are the steps to complete this task?"
   - Example: Run docker build, deploy to staging, verify health checks
2. For each step identified:
   - Document the command or action to run
   - Document the expected outcome after running it
3. Order steps by dependency (what must run before what)
4. Ask: "Are there more steps?"
5. When user confirms steps are complete, save snapshot and proceed to Verification phase

**Snapshot Saving:**
```
// After each step documented, save context
Tool: mcp__mermaid__save_snapshot
Args: {
  "project": "<cwd>",
  "session": "<session-name>",
  "activeSkill": "task-planning",
  "currentStep": "steps",
  "pendingQuestion": "Are there more steps?",
  "inProgressItem": currentItem,
  "recentContext": []
}
// Note: version and timestamp are automatically added
```

### Phase 3: Verification

Define how to confirm the task completed successfully.

**Steps:**
1. Ask: "How will you verify this task succeeded?"
   - Example: Run health check endpoint, check container logs, verify files exist
2. Document verification commands/checks
3. Update the design.md with all three phases (Prerequisites, Steps, Verification)
4. Mark item as "task-planning" phase complete
5. Save final snapshot
6. Return to collab skill (indicate item is ready for executing-plans phase)

**Snapshot Saving:**
```
// After verification documented and design.md updated
Tool: mcp__mermaid__save_snapshot
Args: {
  "project": "<cwd>",
  "session": "<session-name>",
  "activeSkill": "task-planning",
  "currentStep": "verification-complete",
  "pendingQuestion": null,
  "inProgressItem": currentItem,
  "recentContext": []
}
// Note: version and timestamp are automatically added
```

## Integration

### Called From
- **collab** skill (Step 4 routing): After brainstorming completes for task-type items

### Routing Logic
```
Item Type → Path
- "code" type  → brainstorming → rough-draft → test-driven-development → executing-plans
- "bugfix" type → systematic-debugging → executing-plans
- "task" type  → brainstorming → task-planning → executing-plans (NO TDD)
```

### Next Skill
After task-planning completes:
- Invoke **executing-plans** skill with task type indicator
- executing-plans will skip test-driven-development for task items
- executing-plans will execute the commands and run verification checks

### Design Document Format

The task-planning skill updates the work item in design.md with this structure:

```markdown
### Item N: [Task Name]
**Type:** task
**Status:** planning → executing
**Problem/Goal:** [Brief description]

**Approach:**
[Results from brainstorming]

**Prerequisites:**
- Prerequisite 1: how to check if it exists
- Prerequisite 2: how to check if it exists

**Steps:**
1. [Command/action] → Expected: [outcome]
2. [Command/action] → Expected: [outcome]
3. [Command/action] → Expected: [outcome]

**Verification:**
- Check 1: [verification command/check]
- Check 2: [verification command/check]

**Success Criteria:**
[From original brainstorming]
```

## Context Preservation

This skill saves snapshots at key transitions to preserve planning progress if the session is compacted.

**Snapshot Structure (returned by mcp__mermaid__load_snapshot):**
```json
{
  "version": 1,
  "timestamp": "2025-01-21T14:30:00Z",
  "activeSkill": "task-planning",
  "currentStep": "prerequisites|steps|verification-complete",
  "pendingQuestion": "Are there more prerequisites?",
  "inProgressItem": { "id": "item-1", "name": "..." },
  "recentContext": []
}
```
Note: `version` and `timestamp` are automatically added by `mcp__mermaid__save_snapshot`.

When the collab session resumes after compaction:
1. collab skill reads context-snapshot.json
2. Restores the task-planning skill state
3. Resumes from pendingQuestion (continues the conversation)

## Tools Available

- `mcp__plugin_mermaid_collab_mermaid__*` - Full access to mermaid-collab MCP for reading/updating design documents
- `Read` - Read files to understand task context
- `Glob` - Search for files related to the task
- `Grep` - Search file contents for relevant information
