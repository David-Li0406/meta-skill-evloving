# Task Hierarchy

The specification uses a hierarchical task structure for organization.

## Size Guidelines

| Complexity | Phases | Tasks | Verification Coverage |
|------------|--------|-------|----------------------|
| Short (<5 files) | 1-2 | 3-8 | 20% minimum |
| Medium (5-15 files) | 2-4 | 10-25 | 30-40% |
| Large (>15 files) | 4-6 | 25-50 | 40-50% |

**Splitting recommendation:** If >6 phases or >50 tasks, split into multiple specs.

## Hierarchy Levels

```
Spec
└── Phase (phase-1, phase-2, ...)
    └── Task Group (optional: task-group-1-1, ...)
        └── Task (task-1-1, task-1-2, ...)
            └── Subtask (optional: subtask-1-1-1, ...)
        └── Research (research-1-1, ...)
        └── Verify (verify-1-1, ...)
```

## Node Types

| Type | ID Pattern | Purpose |
|------|------------|---------|
| `phase` | `phase-{n}` | Major milestone grouping |
| `task-group` | `task-group-{phase}-{n}` | Optional task grouping |
| `task` | `task-{phase}-{n}` | Actionable work item |
| `subtask` | `subtask-{phase}-{task}-{n}` | Task breakdown |
| `research` | `research-{phase}-{n}` | AI-powered research/investigation |
| `verify` | `verify-{phase}-{n}` | Verification step |

## Task Categories

| Category | Description | Requires file_path |
|----------|-------------|-------------------|
| `investigation` | Research/exploration | No |
| `implementation` | New code creation | Yes |
| `refactoring` | Code restructuring | Yes |
| `decision` | Architecture/design decisions | No |
| `research` | External research/learning | No |

## Required Task Fields

Best practices for well-structured specs - every `type: "task"` should include:
- `description`
- `acceptance_criteria` (array with at least one item)
- `metadata.task_category`
- `metadata.file_path` when `task_category` is `implementation` or `refactoring`

## Verification Types

| Type | Skill Used | Purpose |
|------|------------|---------|
| `run-tests` | `Skill(foundry:foundry-test)` | Execute test suite |
| `fidelity` | `Skill(foundry:foundry-review)` | Compare implementation to spec |
| `manual` | Human verification | Manual testing checklist |

## Verification Task Structure

```json
{
  "verify-1-1": {
    "title": "Verify Phase 1 Implementation",
    "type": "verify",
    "status": "pending",
    "metadata": {
      "verification_type": "fidelity",
      "scope": "phase",
      "target": "phase-1"
    }
  }
}
```

## Research Nodes

Research nodes use AI-powered workflows for investigation, ideation, and consensus-building before or during implementation.

### Research Types

| Type | Workflow | Use Case |
|------|----------|----------|
| `chat` | Single-model conversation | Follow-up questions, iteration |
| `consensus` | Multi-model parallel synthesis | Multiple perspectives, validation |
| `thinkdeep` | Hypothesis-driven investigation | Complex problems, systematic analysis |
| `ideate` | Creative brainstorming with clustering | Generating options, design exploration |
| `deep-research` | Multi-phase web research | Comprehensive external research |

### Blocking Modes

| Mode | Behavior |
|------|----------|
| `none` | Research never blocks dependents |
| `soft` (default) | Informational - dependents can start without waiting |
| `hard` | Must complete before dependent tasks can start |

### Research Node Structure

```json
{
  "research-1-1": {
    "title": "Research authentication patterns",
    "type": "research",
    "status": "pending",
    "metadata": {
      "research_type": "consensus",
      "blocking_mode": "soft",
      "query": "What authentication patterns are used in similar projects?"
    }
  }
}
```

### When to Use Research Nodes

**Use `type: "research"` when:**
- Need AI-powered multi-model consensus before decisions
- Systematic investigation with hypothesis testing required
- Creative ideation with structured clustering
- External web research with source synthesis

**Use `task_category: "investigation"` when:**
- Simple codebase exploration (use Explore subagent)
- Reading documentation or existing code
- No AI workflow needed, just file searching

### Research Node Patterns

**Pattern 1: Blocking Research (before implementation)**
```json
{
  "research-1-1": {
    "title": "Research API design patterns",
    "type": "research",
    "metadata": {
      "research_type": "consensus",
      "blocking_mode": "hard",
      "query": "What REST API patterns should we use for this service?"
    }
  },
  "task-1-1": {
    "title": "Implement API endpoints",
    "type": "task",
    "depends_on": ["research-1-1"]
  }
}
```

**Pattern 2: Parallel Research (soft dependency)**
```json
{
  "research-1-1": {
    "title": "Research performance optimizations",
    "type": "research",
    "metadata": {
      "research_type": "thinkdeep",
      "blocking_mode": "soft",
      "query": "What performance bottlenecks might exist?"
    }
  },
  "task-1-1": {
    "title": "Implement core feature",
    "type": "task",
    "metadata": {
      "soft_depends_on": ["research-1-1"],
      "notes": "Research findings may inform optimization"
    }
  }
}
```

## Dependencies

### Hard Dependencies (blocks)

```json
{
  "task-2-1": {
    "depends_on": ["task-1-1", "task-1-2"],
    "metadata": {
      "blocks": ["task-2-2", "task-2-3"]
    }
  }
}
```

### Soft Dependencies

```json
{
  "task-2-1": {
    "metadata": {
      "soft_depends_on": ["task-1-3"],
      "notes": "Can start without 1-3 but may need revision"
    }
  }
}
```

## Dependency Rules

1. **No circular dependencies** - Validation will fail
2. **Cross-phase deps allowed** - But prefer phase ordering
3. **Verify tasks depend on implementation** - Implicit dependency on phase tasks
4. **Blocked tasks** - Cannot start until blocker resolved

## Task Reorganization

Move tasks between parents or reorder within a phase using `task action="move"`:

```bash
# Move task-2-3 to phase-1 (becomes a child of phase-1)
mcp__plugin_foundry_foundry-mcp__task action="move" spec_id="{spec-id}" task_id="task-2-3" parent="phase-1"

# Move task to specific position within parent
mcp__plugin_foundry_foundry-mcp__task action="move" spec_id="{spec-id}" task_id="task-1-3" parent="phase-1" position=0

# Preview move without applying
mcp__plugin_foundry_foundry-mcp__task action="move" spec_id="{spec-id}" task_id="task-2-3" parent="phase-1" dry_run=true
```

**Parameters:**

| Field | Required | Description |
|-------|----------|-------------|
| `spec_id` | Yes | Target specification ID |
| `task_id` | Yes | Task identifier to move |
| `parent` | Yes | New parent node (phase, task-group, or task for subtasks) |
| `position` | No | Zero-based position within new parent |
| `dry_run` | No | Preview without saving (default: false) |

**Use cases:**
- Reorganize tasks discovered during implementation
- Move related tasks together after initial planning
- Promote subtasks to top-level tasks

## Dependency Management

Manage task dependencies programmatically during planning:

### Adding Dependencies

```bash
# Add a hard dependency (task-2-1 depends on task-1-3)
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="{spec-id}" task_id="task-2-1" depends_on="task-1-3"

# Add soft dependency
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="{spec-id}" task_id="task-2-1" depends_on="task-1-3" dependency_type="soft"
```

### Removing Dependencies

```bash
# Remove a dependency
mcp__plugin_foundry_foundry-mcp__task action="remove-dependency" spec_id="{spec-id}" task_id="task-2-1" depends_on="task-1-3"
```

### Adding Acceptance Requirements

```bash
# Add acceptance criteria to a task
mcp__plugin_foundry_foundry-mcp__task action="add-requirement" spec_id="{spec-id}" task_id="task-1-2" requirement="API returns 200 OK for valid requests"

# Add multiple requirements
mcp__plugin_foundry_foundry-mcp__task action="add-requirement" spec_id="{spec-id}" task_id="task-1-2" requirement="Error responses include actionable messages"
```

### Setting Up Task Dependencies: Examples

**Scenario 1: Sequential implementation**
```bash
# Task 2 depends on Task 1 completing first
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="my-spec" task_id="task-1-2" depends_on="task-1-1"
```

**Scenario 2: Multiple prerequisites**
```bash
# Task 3 requires both Task 1 and Task 2
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="my-spec" task_id="task-1-3" depends_on="task-1-1"
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="my-spec" task_id="task-1-3" depends_on="task-1-2"
```

**Scenario 3: Cross-phase dependency**
```bash
# Phase 2 task depends on Phase 1 task
mcp__plugin_foundry_foundry-mcp__task action="add-dependency" spec_id="my-spec" task_id="task-2-1" depends_on="task-1-3"
```

> Tip: After modifying dependencies, run `mcp__plugin_foundry_foundry-mcp__spec action="analyze-deps"` to detect cycles or orphans.
