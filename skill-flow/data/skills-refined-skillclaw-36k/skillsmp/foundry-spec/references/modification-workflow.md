# Modification Workflow

This reference describes how to apply spec modifications systematically with safety checks.

## Overview

Apply spec modifications with automatic backup, preview (dry-run), validation, and rollback capabilities. Never apply changes without previewing first.

**Core Philosophy:**
- **Safe Systematic Changes**: All changes are validated before applying
- **Spec is Truth**: The spec file is authoritative; all changes flow through MCP tools
- **Preview First**: Always dry-run before applying modifications

## When to Apply Modifications

**Use modifications for:**
- Apply review feedback from foundry-spec review
- Bulk modify task descriptions, metadata, or verification steps
- Add/remove tasks or verification nodes
- Update task metadata across multiple nodes
- Interactive spec updates with preview and validation

**Do NOT use for:**
- Status tracking or task completion (use `foundry-implement`)
- Creating new specifications (during initial planning)
- Finding next actionable task (use `foundry-implement`)

## MCP Tooling

| Router | Key Actions |
|--------|-------------|
| `spec` | `apply-plan`, `validate`, `validate-fix`, `history` |
| `review` | `parse-feedback` |
| `authoring` | `task-add`, `task-remove`, `phase-move`, `phase-update-metadata`, `spec-find-replace`, `spec-rollback` |
| `task` | `update-metadata`, `move` |

## Core Workflow

### Step 1: Parse Review Feedback (if from review)

When starting from a review report, convert it to structured modifications:

```bash
mcp__plugin_foundry_foundry-mcp__review action="parse-feedback" spec_id="my-spec-001" review_path="reports/plan-review.md"
```

This creates a modifications JSON file with structured changes.

### Step 2: Preview with Dry-Run

**Always preview before applying.** Use dry-run mode:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="apply-plan" spec_id="my-spec-001" modifications_file="suggestions.json" dry_run=true
```

**Review checklist:**
- All intended changes are listed
- No unexpected changes
- Task IDs are correct
- Values look correct

### Step 3: Apply Modifications

After confirming the preview, apply changes:

```bash
mcp__plugin_foundry_foundry-mcp__spec action="apply-plan" spec_id="my-spec-001" modifications_file="suggestions.json"
```

**What happens automatically:**
1. **Backup created** at `specs/.backups/{spec-id}-{timestamp}.json`
2. **Modifications applied** in order
3. **Validation runs** on the modified spec
4. **Rollback occurs** if validation fails (original restored from backup)

### Step 4: Verify & Report

Report a structured summary including:
- Spec ID and source
- Changes applied
- Backup location
- Validation status
- Next steps

## Common Workflows

### Task Repositioning

Move tasks within a phase or between phases:

```bash
# Move task-2-3 to position 1 within same phase
mcp__plugin_foundry_foundry-mcp__task action="move" spec_id="my-spec-001" task_id="task-2-3" position=1

# Move task to different phase
mcp__plugin_foundry_foundry-mcp__task action="move" spec_id="my-spec-001" task_id="task-2-3" parent="phase-3" position=1
```

### Phase Reordering

Change the execution order of phases:

```bash
# Move phase-3 to first position
mcp__plugin_foundry_foundry-mcp__authoring action="phase-move" spec_id="my-spec-001" phase_id="phase-3" position=1
```

### Bulk Find-Replace

Replace text across multiple nodes:

```bash
# Replace across all text fields
mcp__plugin_foundry_foundry-mcp__authoring action="spec-find-replace" spec_id="my-spec-001" find="old-api" replace="new-api" scope="all"

# Replace only in titles
mcp__plugin_foundry_foundry-mcp__authoring action="spec-find-replace" spec_id="my-spec-001" find="v1" replace="v2" scope="titles"
```

**Scope options:**
- `all` - Search titles and descriptions
- `titles` - Only search task/phase titles
- `descriptions` - Only search descriptions

### Rollback Recovery

Restore a specification to a previous state:

```bash
# List available backups
mcp__plugin_foundry_foundry-mcp__spec action="history" spec_id="my-spec-001"

# Preview rollback
mcp__plugin_foundry_foundry-mcp__authoring action="spec-rollback" spec_id="my-spec-001" version="2025-12-27T20-54-48.149929" dry_run=true

# Apply rollback
mcp__plugin_foundry_foundry-mcp__authoring action="spec-rollback" spec_id="my-spec-001" version="2025-12-27T20-54-48.149929"
```

## Safety Features

- **Automatic backup** before every modification
- **Dry-run preview** before applying any changes
- **Validation** after every apply
- **Rollback** if validation fails
- **Idempotent** operations (safe to retry)

## Output Format

Return a structured markdown summary:

```markdown
## Modifications Applied

**Spec:** my-spec-001
**Source:** suggestions.json
**Backup:** specs/.backups/my-spec-001-20251018-143000.json

### Changes Applied
- Updated 2 task descriptions
- Added 1 verification step
- Modified 1 metadata field

### Validation
Status: PASSED

### Next Steps
- Review changes in context
- Continue with foundry-implement if ready for implementation
```
