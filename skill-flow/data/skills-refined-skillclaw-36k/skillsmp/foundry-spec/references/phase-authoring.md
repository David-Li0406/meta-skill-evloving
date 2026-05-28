# Phase Authoring Reference

This reference covers advanced phase authoring methods for spec creation.

## Phase Templates

Use phase templates to quickly add pre-configured phases with standard task structures. Templates include built-in verification tasks.

**Available templates:** `planning`, `implementation`, `testing`, `security`, `documentation`

```bash
# List available templates
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="list"

# Show template structure before applying
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="show" template_name="implementation"

# Apply template to an existing spec
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="apply" template_name="implementation" spec_id="{spec-id}"
```

**Template capabilities:**
- `template_action="list"` - View all available phase templates
- `template_action="show"` - Preview a template's structure (tasks, verification steps)
- `template_action="apply"` - Add template as new phase to existing spec

**When to use templates vs manual planning:**
- **Use templates** for standard phases (testing, security review, documentation)
- **Use manual planning** for custom feature-specific phases

> Templates automatically include verification tasks and follow consistent naming patterns.

## Phase-Add-Bulk Macro

For maximum control over phase structure, use `phase-add-bulk` to create a phase with all its tasks in a single atomic operation. This macro accepts a nested payload with phase metadata and task definitions.

```bash
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Implementation", "description": "Core feature implementation", "estimated_hours": 8}' tasks='[{"type": "task", "title": "Implement core logic", "description": "Build the main functionality", "task_category": "implementation", "file_path": "src/core/logic.py", "estimated_hours": 4, "acceptance_criteria": ["Core logic returns expected outputs"]}, {"type": "task", "title": "Add error handling", "description": "Handle edge cases and errors", "task_category": "implementation", "file_path": "src/core/errors.py", "estimated_hours": 2, "acceptance_criteria": ["Errors are surfaced with actionable messages"]}, {"type": "verify", "title": "Run tests", "verification_type": "run-tests"}, {"type": "verify", "title": "Fidelity review", "verification_type": "fidelity"}]'
```

**Payload structure:**

| Field | Required | Description |
|-------|----------|-------------|
| `spec_id` | Yes | Target specification ID |
| `phase.title` | Yes | Phase title |
| `phase.description` | No | Phase description |
| `phase.purpose` | No | Purpose/goal metadata |
| `phase.estimated_hours` | No | Time estimate for phase |
| `tasks` | Yes | Array of task definitions (min 1) |
| `tasks[].type` | Yes | `"task"` or `"verify"` |
| `tasks[].title` | Yes | Task title |
| `tasks[].description` | Medium/Complex | Task description |
| `tasks[].task_category` | Medium/Complex | Task category (`implementation`, `refactoring`, `investigation`, ...) |
| `tasks[].file_path` | Medium/Complex (impl/refactor) | Associated file path |
| `tasks[].estimated_hours` | No | Time estimate |
| `tasks[].acceptance_criteria` | Medium/Complex | Array of completion checks |
| `tasks[].verification_type` | No | For verify tasks: `"run-tests"` or `"fidelity"` |
| `position` | No | Zero-based insertion index |
| `link_previous` | No | Link to previous phase (default: true) |
| `dry_run` | No | Preview without saving (default: false) |

**When to use phase-add-bulk vs templates:**
- **Use `phase-add-bulk`** when you need custom task structures or specific verification configurations
- **Use `phase-template`** for standard phases with predefined task patterns
- **Use `phase-add-bulk`** to programmatically construct phases from plan sections

> The macro creates all nodes atomically - either the entire phase succeeds or nothing is created.

## Quick Phase Refinements

After creating a phase with `phase-add-bulk`, you may need to adjust phase-level metadata without using modification operations. Use `phase-update-metadata` for lightweight refinements:

```bash
# Adjust estimated hours after reviewing task breakdown
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id="{spec-id}" phase_id="phase-2" estimated_hours=6.5

# Refine phase description and purpose
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id="{spec-id}" phase_id="phase-2" description="Core API implementation with auth" purpose="Establish authenticated endpoints"

# Preview changes before applying
mcp__plugin_foundry_foundry-mcp__authoring action="phase-update-metadata" spec_id="{spec-id}" phase_id="phase-2" estimated_hours=4.0 dry_run=true
```

**When to use `phase-update-metadata` vs modification operations:**

| Scenario | Recommendation |
|----------|----------------|
| Adjust phase hours, description, or purpose | Use `phase-update-metadata` |
| Add/remove/reorder tasks within a phase | Use modification operations |
| Bulk changes across multiple phases | Use modification operations |
| Quick post-creation tweaks | Use `phase-update-metadata` |

> This action is ideal for iterative refinement during spec creation without leaving the planning workflow.

## Phase Removal

Remove phases that are no longer needed using `phase-remove`. This action removes a phase and all its child tasks.

```bash
# Preview removal (dry run)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-remove" spec_id="{spec-id}" phase_id="phase-2" dry_run=true

# Remove a phase
mcp__plugin_foundry_foundry-mcp__authoring action="phase-remove" spec_id="{spec-id}" phase_id="phase-2"

# Force removal even if other phases depend on it
mcp__plugin_foundry_foundry-mcp__authoring action="phase-remove" spec_id="{spec-id}" phase_id="phase-2" force=true
```

**Parameters:**

| Field | Required | Description |
|-------|----------|-------------|
| `spec_id` | Yes | Target specification ID |
| `phase_id` | Yes | Phase identifier to remove (e.g., `phase-2`) |
| `force` | No | Force removal even if other phases depend on this one (default: false) |
| `dry_run` | No | Preview what would be removed without saving (default: false) |

**Behavior:**
- Removes the phase and all child tasks/subtasks/verify nodes
- Fails if other phases have dependencies on this phase (unless `force=true`)
- Use `dry_run=true` to preview before committing changes

> Always use `dry_run=true` first to verify the scope of removal before executing.

## Phase Reordering

Reorganize phases during plan creation using `phase-move`. This is useful when you need to change the execution order without recreating phases.

```bash
# Move phase-3 to position 1 (making it the second phase, after phase-1)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-move" spec_id="{spec-id}" phase_id="phase-3" position=1

# Preview the move without applying
mcp__plugin_foundry_foundry-mcp__authoring action="phase-move" spec_id="{spec-id}" phase_id="phase-3" position=1 dry_run=true
```

**Parameters:**

| Field | Required | Description |
|-------|----------|-------------|
| `spec_id` | Yes | Target specification ID |
| `phase_id` | Yes | Phase identifier to move (e.g., `phase-3`) |
| `position` | Yes | Zero-based target position in phase order |
| `dry_run` | No | Preview the move without saving (default: false) |

**When to use `phase-move` vs recreating phases:**

| Scenario | Recommendation |
|----------|----------------|
| Simple reordering (e.g., swap phase 2 and 3) | Use `phase-move` |
| Phase has many tasks with complex dependencies | Use `phase-move` to preserve structure |
| Need to fundamentally restructure phase content | Recreate with `phase-add-bulk` |
| Moving phase would break cross-phase dependencies | Resolve dependencies first, then move |

**Behavior:**
- Preserves all child tasks, subtasks, and verification nodes
- Updates phase sequence indices automatically
- Does NOT update cross-phase dependencies (review manually)
- Use `dry_run=true` to preview changes before committing

> Tip: After moving phases, run `mcp__plugin_foundry_foundry-mcp__spec action="validate"` to catch any dependency issues.

## AI Review of Phase Plans

Before converting to JSON spec, get AI feedback to catch issues early:

```bash
mcp__plugin_foundry_foundry-mcp__plan action="review" plan_path="specs/.plans/feature-name.md" review_type="full"
```

Review types: `full`, `quick`, `security`, `feasibility`. Iterate until no critical blockers.

> See `ai-review.md` for review output format and iteration workflow.
