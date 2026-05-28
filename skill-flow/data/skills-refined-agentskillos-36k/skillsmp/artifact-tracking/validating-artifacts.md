# VALIDATE Function: Quality Assurance for Tracking Artifacts

Use artifact-validator agent for comprehensive validation before phase completion.

## Validate Progress File

**Command**:
```markdown
Task("artifact-validator", "Validate Phase [N] progress for [PRD]")
```

**Checks**:
- YAML schema compliance
- Required fields present (assigned_to, dependencies)
- Data type correctness
- Task count accuracy
- Progress percentage calculation
- Blocker consistency

## Validate Context File

**Command**:
```markdown
Task("artifact-validator", "Validate context file for [PRD]")
```

**Checks**:
- YAML frontmatter structure
- Agent contribution tracking
- Decision documentation format
- Link integrity

## Validate Before Phase Completion

**Command**:
```markdown
Task("artifact-validator", "Pre-completion validation for [PRD] Phase [N]:
- All tasks should be complete
- No active blockers
- Progress at 100%
- Success criteria met")
```

## Validate Orchestration Readiness

**Command**:
```markdown
Task("artifact-validator", "Validate orchestration readiness for [PRD] Phase [N]:
- Every task has assigned_to
- Every task has dependencies
- Parallelization computed
- Task() commands generated")
```

## Bulk Validation

**Command**:
```markdown
Task("artifact-validator", "Validate all progress files for [PRD] across all phases")
```

## Validation Report

Returns structured report:
```markdown
## Validation Report: [PRD] Phase [N]

**Status**: ✅ PASS / ⚠️ WARNINGS / ❌ FAIL

### Schema Compliance
- [x] YAML frontmatter valid
- [x] Required fields present
- [ ] assigned_to missing on TASK-2.3

### Metric Accuracy
- [x] Task counts match
- [x] Progress calculation correct

### Orchestration Readiness
- [ ] TASK-2.3 missing assigned_to
- [x] All dependencies specified
- [x] Parallelization computed

### Recommendations
1. Add assigned_to to TASK-2.3
2. Consider splitting TASK-3.1 (estimated 8h)
```

## Using Python Validation Script

For programmatic validation:
```bash
python .claude/skills/artifact-tracking/scripts/validate_artifact.py \
  .claude/progress/auth-overhaul/phase-2-progress.md
```

## Validation Schemas

JSON schemas in `./schemas/`:
- `progress.schema.yaml` - Progress file validation
- `context.schema.yaml` - Context file validation

## Best Practices

1. **Validate before marking phase complete**
2. **Fix warnings** even if not errors
3. **Run orchestration validation** before delegating tasks
4. **Use bulk validation** at project milestones
