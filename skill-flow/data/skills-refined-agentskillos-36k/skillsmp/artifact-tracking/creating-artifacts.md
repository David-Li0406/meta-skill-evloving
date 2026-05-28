# CREATE Function: Creating Progress & Context Artifacts

Use artifact-tracker agent to create new tracking files.

## Creating Progress Files

**Command**:
```markdown
Task("artifact-tracker", "Create Phase [N] progress tracking for [PRD_NAME] PRD.
Include tasks: [task1, task2, ...]. Phase title: '[Title]'")
```

**Required Follow-up** (for orchestration):
```markdown
Task("lead-architect", "Annotate Phase [N] progress for [PRD_NAME]:
- Add assigned_to field to every task
- Add dependencies field to every task
- Compute parallelization batches
- Generate Orchestration Quick Reference section")
```

**Output**: `.claude/progress/[prd]/phase-N-progress.md`

## Creating Context Files

**Command**:
```markdown
Task("artifact-tracker", "Create context worknotes for [PRD_NAME] PRD")
```

**Output**: `.claude/worknotes/[prd]/context.md`

**Note**: Context files are ONE per PRD (not per phase). They start nearly empty and grow as agents add observations.

## Best Practices

1. **ONE progress file per phase** - Never create duplicates
2. **Annotate immediately** - Use lead-architect to add assigned_to and dependencies
3. **Include all tasks** - Extract complete task list from implementation plan
4. **Use consistent IDs** - Pattern: TASK-[PHASE].[SEQUENCE] (e.g., TASK-2.1)

## Example: Full Progress Creation Flow

```markdown
# Step 1: Create progress file
Task("artifact-tracker", "Create Phase 1 progress tracking for sync-redesign PRD.
Include tasks: Create ArtifactFlowBanner, Create ComparisonSelector, Create DiffPreviewPanel.
Phase title: 'Sync Status Sub-Components'. Mark all as pending.")

# Step 2: Annotate for orchestration
Task("lead-architect", "Annotate Phase 1 progress for sync-redesign:
- ArtifactFlowBanner → ui-engineer-enhanced (no dependencies)
- ComparisonSelector → ui-engineer-enhanced (no dependencies)
- DiffPreviewPanel → ui-engineer-enhanced (no dependencies)
All can run in parallel as batch_1. Generate Task() delegation commands.")
```

## YAML Fields Created

See `./schemas/progress.schema.yaml` for full schema. Key fields:
- `type: progress`
- `prd`: PRD identifier (kebab-case)
- `phase`: Integer (1-99)
- `status`: planning|in-progress|review|complete|blocked
- `tasks`: Array with required `assigned_to` and `dependencies`
- `parallelization`: Computed batch groupings

## Templates

- Progress: `./templates/progress-template.md`
- Context: `./templates/context-template.md`
