---
name: simple-task-management
description: This skill should be used when the user asks to "generate tasks from a spec", "break down a spec", "create tasks from a PRD", "decompose requirements", "generate a task list from a design document", or mentions working from specification documents. Provides guidance for transforming specifications into structured, actionable task lists organized under missions.
version: 0.2.0
---

# Simple Task Management

Transform specification documents (PRDs, Technical Specifications, Design Documents) into structured task lists organized under named missions that can be executed systematically.

## Core Workflow

### 1. Document Analysis

Parse the specification document to extract:

- **Explicit requirements**: Stated features, functionality, acceptance criteria
- **Implicit requirements**: Technical considerations, infrastructure needs, error handling
- **Constraints**: Technology choices, performance requirements, compatibility needs
- **Scope boundaries**: What is and isn't included in the specification

Read the source document thoroughly. Identify section headings, numbered requirements, user stories, acceptance criteria, and technical specifications. Note any cross-references between sections.

### 2. Task Decomposition

Break requirements into atomic tasks with these characteristics:

| Characteristic | Description |
|----------------|-------------|
| Single responsibility | Each task addresses one specific piece of functionality |
| Independence | Tasks can be worked on without coordination where possible |
| Clear boundaries | Well-defined start and end conditions |
| Testable | Verifiable completion criteria exist |

**Decomposition process:**
1. Identify each distinct requirement in the specification
2. Determine if the requirement is atomic or needs splitting
3. Create task entries with unique IDs (TASK-001, TASK-002, etc.)
4. Ensure each task maps to specific specification sections

### 3. Dependency Mapping

Identify blocking dependencies between tasks:

- **Blocking dependencies**: Task B cannot start until Task A completes

Populate the `dependencies` array with task IDs this task depends on. Calculate `blocked_by` (incomplete dependencies) and `blocks` (tasks depending on this one).

### 4. Priority Calculation

Score and prioritize tasks based on:

1. **Dependency depth**: Tasks unblocking many others rank higher
2. **Complexity**: Use T-shirt sizing (XS, S, M, L, XL)
3. **Risk level**: Higher uncertainty = higher priority (do risky things early)
4. **Business value**: When indicated in specification

Map to priority levels: critical, high, medium, low.

**PRD Priority Mapping:**
- P0 -> critical
- P1 -> high
- P2 -> medium
- P3 -> low

### 5. Acceptance Criteria

For each task, generate acceptance criteria:

- Specific conditions that must be true when complete
- Derived from the specification's acceptance criteria and user stories
- Each criterion should be independently verifiable

### 6. Execution Phases

Group tasks into phases based on dependency analysis:

- **Phase 1**: No blocking dependencies (can start immediately)
- **Phase 2**: Dependencies only on Phase 1 tasks
- **Phase N**: Dependencies satisfied by previous phases

## Output Format

Generate task lists as JSON following the schema in `references/task-schema.json`.

**Key structure:**
```json
{
  "mission": {
    "name": "Build User Authentication System",
    "metadata": {
      "source_document": "path/to/spec.md",
      "generated_at": "2024-01-15T10:30:00Z",
      "last_updated": "2024-01-15T10:30:00Z",
      "version": "1.0.0",
      "total_tasks": 12,
      "completion_percentage": 0
    },
    "tasks": [...],
    "execution_phases": [...]
  }
}
```

## Storage Convention

Store task files at: `missions/<mission-slug>/<project-name>.tasks.json`

The mission slug is derived from the mission name:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters

Example: "Build User Authentication" → `missions/build-user-authentication/`

Create the `missions/<mission-slug>/` directory if it doesn't exist. Use the specification filename (without extension) as the project name, or derive from specification title.

Maintain version history by incrementing `mission.metadata.version` on updates.

## Task Status Management

Track task lifecycle:

| Status | Description |
|--------|-------------|
| not_started | Task not yet begun |
| in_progress | Currently being worked on |
| blocked | Cannot proceed due to incomplete dependencies |
| complete | Task finished and verified |

When marking a task complete:
1. Update status to "complete"
2. Recalculate `blocked_by` for all dependent tasks
3. Update `completion_percentage` in metadata
4. Suggest next best tasks based on updated state

## Complexity Estimation

Use T-shirt sizing with these guidelines:

| Size | Typical Scope |
|------|---------------|
| XS | Single function, simple change, < 20 lines |
| S | Single file, straightforward logic, 20-100 lines |
| M | Multiple files, moderate complexity, 100-300 lines |
| L | Multiple components, significant logic, 300-800 lines |
| XL | System-wide, complex integration, > 800 lines |

## Handling Ambiguity

When specifications are unclear:

1. Note assumptions in the task's `notes` field
2. Flag ambiguous requirements for human review
3. Create tasks for clarification if significant
4. Document which specification sections need clarification

## Quick Reference

**Generate command flow:**
1. Accept mission name and specification document path
2. Read specification document
3. Extract requirements and structure
4. Decompose into atomic tasks
5. Map blocking dependencies
6. Calculate priorities and phases
7. Generate acceptance criteria
8. Write to `missions/<mission-slug>/<project-name>.tasks.json`

**Next task selection criteria:**
1. Status is "not_started"
2. No incomplete dependencies (blocked_by is empty)
3. Highest priority first
4. Lowest complexity as tiebreaker (quick wins)

## Additional Resources

### Reference Files

For the task list schema, consult:
- **`references/task-schema.json`** - JSON schema for task list format
