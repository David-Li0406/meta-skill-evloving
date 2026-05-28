---
name: spec-task-management
description: This skill should be used when the user asks to "analyze a specification", "break down a spec", "create tasks from a PRD", "decompose requirements", "generate a task list from a design document", or mentions working from specification documents. Provides comprehensive guidance for transforming specifications into structured, actionable task lists optimized for AI coding agents.
version: 0.1.0
---

# Spec Task Management

Transform specification documents (PRDs, Technical Specifications, Design Documents) into structured task lists that AI coding agents can execute independently or in parallel.

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
| Independence | Tasks can be worked on by different agents without coordination |
| Clear boundaries | Well-defined start and end conditions |
| Testable | Verifiable completion criteria exist |

**Decomposition process:**
1. Identify each distinct requirement in the specification
2. Determine if the requirement is atomic or needs splitting
3. Create task entries with unique IDs (TASK-001, TASK-002, etc.)
4. Ensure each task maps to specific specification sections

### 3. Dependency Mapping

Identify three types of dependencies between tasks:

- **Hard dependencies**: Task B cannot start until Task A completes
- **Soft dependencies**: Task B benefits from Task A being complete but can proceed
- **Resource dependencies**: Tasks share files, modules, or services

Populate `dependencies.hard` and `dependencies.soft` arrays. Calculate `blocked_by` (incomplete hard dependencies) and `blocks` (tasks depending on this one).

For detailed dependency patterns, consult `references/dependency-patterns.md`.

### 4. Priority Calculation

Score and prioritize tasks based on:

1. **Dependency depth**: Tasks unblocking many others rank higher
2. **Complexity**: Use T-shirt sizing (XS, S, M, L, XL)
3. **Risk level**: Higher uncertainty = higher priority (do risky things early)
4. **Business value**: When indicated in specification

Map to priority levels: critical, high, medium, low.

### 5. Testing Criteria Generation

For each task, generate:

- **Acceptance criteria**: Specific conditions that must be true when complete
- **Test scenarios**: Concrete examples to verify implementation
- **Edge cases**: Boundary conditions and error scenarios

Derive these from the specification's acceptance criteria, user stories, and technical requirements.

### 6. Execution Phases

Group tasks into phases based on dependency analysis:

- **Phase 1**: No hard dependencies (can start immediately)
- **Phase 2**: Dependencies only on Phase 1 tasks
- **Phase N**: Dependencies satisfied by previous phases

Calculate phases to enable maximum parallel execution by multiple agents.

### 7. Context Window Grouping

Organize tasks into context groups that fit within AI coding agent context windows:

**Why Context Groups Matter:**
- AI coding agents have limited context windows (e.g., 100K tokens)
- Loading too many tasks exhausts context capacity
- Context groups enable efficient agent handoffs between sessions

**Grouping Algorithm:**
1. Calculate effective limit: `max_tokens - reserve_tokens`
2. Topologically sort tasks by execution phase
3. Bin-pack tasks respecting:
   - Token limits (complexity-based estimation)
   - Hard dependencies (must be in same or earlier group)
4. Mark first/last tasks with boundary flags

**Token Estimation:**
| Complexity | Base Tokens | Description |
|------------|-------------|-------------|
| XS | 500 | Single function, < 20 lines |
| S | 1,500 | Single file, 20-100 lines |
| M | 4,000 | Multiple files, 100-300 lines |
| L | 10,000 | Multiple components, 300-800 lines |
| XL | 25,000 | System-wide, > 800 lines |

**Overhead:**
- Base per task: 200 tokens
- Per hard dependency: 100 tokens
- Group transition: 500 tokens

Use `/task-manager:context-groups` to generate groups after analyzing a specification.

## Output Format

Generate task lists as JSON following the schema in `references/task-schema.json`.

**Key structure:**
```json
{
  "metadata": {
    "source_document": "path/to/spec.md",
    "generated_at": "2024-01-15T10:30:00Z",
    "version": "1.0.0",
    "total_tasks": 12,
    "completion_percentage": 0
  },
  "tasks": [...],
  "dependency_graph": { "nodes": [...], "edges": [...] },
  "execution_phases": [...]
}
```

## Storage Convention

Store task files at: `tasks/<project-name>.tasks.json`

Create the `tasks/` directory if it doesn't exist. Use the specification filename (without extension) as the project name, or derive from specification title.

Maintain version history by incrementing `metadata.version` on updates.

## Task Status Management

Track task lifecycle:

| Status | Description |
|--------|-------------|
| not_started | Task not yet begun |
| in_progress | Currently being worked on |
| blocked | Cannot proceed due to incomplete dependencies |
| complete | Task finished and verified |
| obsolete | Task no longer relevant (spec changed) |

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

## ID Stability

Maintain stable task IDs across regenerations:

- Base IDs on requirement content, not position
- When updating, match existing tasks by requirement reference
- Only assign new IDs for genuinely new requirements
- Mark removed requirements as "obsolete" rather than deleting

## Additional Resources

### Reference Files

For detailed patterns and schema, consult:
- **`references/task-schema.json`** - Complete JSON schema for task list format
- **`references/dependency-patterns.md`** - Detailed dependency identification patterns
- **`references/context-defaults.json`** - Default configuration for context grouping

## Quick Reference

**Analyze command flow:**
1. Read specification document
2. Extract requirements and structure
3. Decompose into atomic tasks
4. Map dependencies (hard, soft, resource)
5. Calculate priorities and phases
6. Generate testing criteria
7. Write to `tasks/<project-name>.tasks.json`

**Context grouping flow:**
1. Run `/task-manager:context-groups` on existing task list
2. Algorithm bin-packs tasks into groups respecting token limits
3. Each task gets `context_group_id`, boundary flags, token estimates
4. `context_groups` array added to task file with summaries

**Agent execution workflow:**
1. `/task-manager:next-group` - Get next group to work on
2. Work through tasks in group, marking complete
3. When group complete, agent resets context
4. New session runs `/task-manager:next-group` for next group

**Next task selection criteria:**
1. Status is "not_started"
2. No incomplete hard dependencies (blocked_by is empty)
3. Prefer tasks in active context group
4. Highest priority first
5. Lowest complexity as tiebreaker (quick wins)
