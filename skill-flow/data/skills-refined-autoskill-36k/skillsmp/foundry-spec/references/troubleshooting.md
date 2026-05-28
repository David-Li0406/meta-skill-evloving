# Troubleshooting

Common issues and their resolutions.

## Validation Errors

**Error:** "Circular dependency detected"

**Resolution:**
1. Check `depends_on` arrays for cycles
2. Use `spec action="validate"` to identify specific tasks
3. Remove or reorder dependencies

**Error:** "Missing file_path for implementation task"

**Resolution:**
1. Add `metadata.file_path` to task
2. Or change `task_category` to `investigation`

**Error:** "Missing mission"

**Resolution:** Add `metadata.mission` (required for complex/security specs).

**Error:** "Missing task description / acceptance_criteria / task_category"

**Resolution:** For complex/security specs, ensure every `type: "task"` includes:
- `description`
- `acceptance_criteria` (array with at least one item)
- `metadata.task_category`

**Error:** "Invalid task ID format"

**Resolution:**
- Follow pattern: `task-{phase}-{n}`, `verify-{phase}-{n}`
- Phase number must match parent phase

## Spec Not Found

**Symptoms:** MCP tools can't find spec

**Checks:**
1. Verify file exists: `ls specs/pending/` or `specs/active/`
2. Check spec_id matches filename (without .json)
3. Ensure valid JSON: `spec action="validate"`

## Plan Review Fails

**Symptoms:** `plan action="review"` returns error

**Checks:**
1. Plan file exists in `specs/.plans/`
2. Markdown is well-formed
3. Required sections present (Objective, Phases)

## LSP Not Available

**Symptoms:** LSP tools return errors

**Fallbacks:**
1. Use Explore agent with specific search terms
2. Use Grep for symbol search: `Grep pattern="class AuthService"`

## Phase-Add-Bulk Errors

**Error:** "At least one task definition is required"

**Resolution:** Ensure `tasks` array contains at least one task object with `type` and `title`.

**Error:** "Task at index N must have type 'task' or 'verify'"

**Resolution:** Each task must specify `type` as either `"task"` or `"verify"`.

**Error:** "Task at index N must have a non-empty title"

**Resolution:** Every task requires a non-empty `title` string.

**Error:** "Task at index N has invalid estimated_hours"

**Resolution:** `estimated_hours` must be a non-negative number if provided.

**Error:** "Phase title is required"

**Resolution:** The `phase` object must include a `title` field.

---

# Quick Reference

## Creation Commands

```bash
# Create markdown plan
mcp__plugin_foundry_foundry-mcp__plan action="create" name="Feature Name" template="detailed"

# Review plan
mcp__plugin_foundry_foundry-mcp__plan action="review" plan_path="specs/.plans/feature-name.md" review_type="full"

# Create JSON spec
mcp__plugin_foundry_foundry-mcp__authoring action="spec-create" name="feature-name" template="empty"

# Validate spec
mcp__plugin_foundry_foundry-mcp__spec action="validate" spec_id="{spec-id}"

# Auto-fix validation errors
mcp__plugin_foundry_foundry-mcp__spec action="validate-fix" spec_id="{spec-id}" auto_fix=true
```

## Phase Template Commands

```bash
# List available phase templates
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="list"

# Show template structure (preview before applying)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="show" template_name="implementation"

# Apply template to existing spec (adds new phase)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-template" template_action="apply" template_name="testing" spec_id="{spec-id}"
```

**Available templates:** `planning`, `implementation`, `testing`, `security`, `documentation`

## Phase-Add-Bulk Commands

```bash
# Add phase with tasks atomically (basic)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Phase Title"}' tasks='[{"type": "task", "title": "Task 1", "description": "Explain the task", "task_category": "investigation", "acceptance_criteria": ["Notes captured in spec journal"]}]'

# Add phase with full metadata and verification tasks
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Implementation", "description": "Build core features", "estimated_hours": 8}' tasks='[{"type": "task", "title": "Implement feature", "description": "Build the primary workflow", "task_category": "implementation", "file_path": "src/feature/core.py", "estimated_hours": 4, "acceptance_criteria": ["Core workflow passes unit tests"]}, {"type": "verify", "title": "Run tests", "verification_type": "run-tests"}, {"type": "verify", "title": "Fidelity review", "verification_type": "fidelity"}]'

# Preview phase creation without saving (dry run)
mcp__plugin_foundry_foundry-mcp__authoring action="phase-add-bulk" spec_id="{spec-id}" phase='{"title": "Test Phase"}' tasks='[{"type": "task", "title": "Test task"}]' dry_run=true
```

## Analysis Commands

```bash
# LSP tools (preferred)
documentSymbol(file="src/auth/service.py")
findReferences(file="src/auth/service.py", symbol="AuthService", line=15, character=6)
goToDefinition(file="src/api/routes.py", symbol="authenticate", line=42, character=10)
incomingCalls(file="src/auth/service.py", symbol="authenticate", line=42, character=10)

# Fallback: Grep
Grep pattern="class ClassName" type="py"
Grep pattern="def functionName" type="py"
```

## File Locations

| Artifact | Location |
|----------|----------|
| Markdown plans | `specs/.plans/` |
| Plan reviews | `specs/.plan-reviews/` |
| Pending specs | `specs/pending/` |
| Active specs | `specs/active/` |
| Completed specs | `specs/completed/` |
| Archived specs | `specs/archived/` |
