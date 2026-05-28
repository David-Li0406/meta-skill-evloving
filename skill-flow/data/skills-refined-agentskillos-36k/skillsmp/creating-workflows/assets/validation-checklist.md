# Workflow Validation Checklist

Use this checklist before deploying a new workflow.

## File Structure

- [ ] Workflow file is in `.claude/workflows/` directory
- [ ] File has `.yaml` extension
- [ ] File name is kebab-case (e.g., `my-workflow.yaml`)
- [ ] File is valid YAML (no syntax errors)

## Top-Level Fields

- [ ] `name` field is present and non-empty
- [ ] `description` field describes workflow purpose (recommended)
- [ ] `phases` field is present and non-empty array

## Phase Configuration

### For Each Phase:

- [ ] `id` field is unique within the workflow
- [ ] `id` uses kebab-case convention

### Simple Phases:

- [ ] `prompt` field is present
- [ ] `prompt` contains clear instructions
- [ ] No `for-each` or `workflow` fields present

### For-Each Phases:

- [ ] `for-each` field is set to `step`
- [ ] `workflow` field references existing workflow
- [ ] Referenced workflow exists in `.claude/workflows/`
- [ ] No `prompt` field present

## Template Variables

- [ ] Variables use correct syntax: `{{variable.property}}`
- [ ] `{{step.*}}` only used in for-each phases or their nested workflows
- [ ] `{{phase.*}}` and `{{sprint.*}}` used appropriately
- [ ] No typos in variable names

## Workflow References

- [ ] All referenced workflows exist
- [ ] No circular references (workflow A → B → A)
- [ ] Referenced workflows are valid
- [ ] References don't include `.yaml` extension

## Content Quality

- [ ] Prompts are clear and actionable
- [ ] Instructions are specific enough for execution
- [ ] Output expectations are documented
- [ ] Error handling instructions provided where needed

## Integration

- [ ] Workflow works with existing SPRINT.yaml structure
- [ ] Step-level workflows receive proper step context
- [ ] Artifacts use consistent naming (e.g., `{{step.id}}-plan.md`)

## Testing

- [ ] Compiled PROGRESS.yaml structure is correct
- [ ] Template variables resolve properly
- [ ] Execution order is as expected
- [ ] All phases produce expected results

---

## Quick Validation Commands

```bash
# Check YAML syntax
cat .claude/workflows/my-workflow.yaml | yq .

# Verify phase IDs are unique
yq '.phases[].id' .claude/workflows/my-workflow.yaml | sort | uniq -d

# List all workflow references
yq '.phases[] | select(.workflow) | .workflow' .claude/workflows/my-workflow.yaml

# Check for required fields
yq '.name, .phases | length' .claude/workflows/my-workflow.yaml
```

## Common Issues

| Issue | Check | Fix |
|-------|-------|-----|
| Workflow not found | File exists in correct location | Move to `.claude/workflows/` |
| Phase skipped | Has `prompt` or `for-each` | Add required field |
| Variable not resolved | Correct context | Check availability matrix |
| Compilation error | Valid YAML | Fix syntax |
| Wrong execution order | Phase order | Reorder phases array |
