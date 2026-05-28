# Milestone Checks

Criteria for phase and batch completion validation.

## Batch Completion Criteria

A batch is complete when:

1. **All tasks in batch have `status: completed`**
2. **All task tests pass**
3. **No blockers** from batch tasks
4. **Progress tracker updated**

### Batch Validation Template

```
@task-completion-validator

Phase ${phase_num} Milestone: Batch {batch_num} Complete

Completed tasks:
- {task_id_1}: {brief description}
- {task_id_2}: {brief description}

Expected outcomes from plan:
- [Outcome 1]
- [Outcome 2]

Validate:
1. All batch tasks complete
2. Success criteria met
3. No regressions
4. Tests comprehensive
5. Documentation updated
```

## Phase Completion Criteria

A phase is **ONLY** complete when ALL of these are true:

### Execution Criteria

- [ ] **All tasks** in implementation plan completed
- [ ] **All success criteria** met (verified)
- [ ] **All tests** passing (backend + frontend + e2e)
- [ ] **Quality gates** passed (types, lint, build)

### Documentation Criteria

- [ ] **Code comments** added where needed
- [ ] **ADRs created** if architectural decisions made
- [ ] **API docs updated** if endpoints added

### Tracking Criteria

- [ ] **Progress tracker** shows `status: completed`
- [ ] **Context document** updated with learnings
- [ ] **All commits** pushed to branch

### Validation Criteria

- [ ] **Validation completed** by task-completion-validator
- [ ] **No critical blockers** or P0 issues

**Never mark phase complete if any criterion is unmet.**

## Phase Validation Checklist

### Full Validation Script

```bash
#!/bin/bash
set -euo pipefail

echo "🎯 Phase ${phase_num} Final Quality Gates"

# All tests must pass
pnpm -r test || { echo "❌ Tests failed"; exit 1; }
uv run --project services/api pytest 2>/dev/null || true

# Type safety
pnpm -r typecheck || { echo "❌ Type check failed"; exit 1; }
uv run --project services/api mypy app 2>/dev/null || true

# Linting
pnpm -r lint || { echo "❌ Lint failed"; exit 1; }
uv run --project services/api ruff check 2>/dev/null || true

# Build
pnpm --filter "./apps/web" build 2>/dev/null || pnpm build || { echo "❌ Build failed"; exit 1; }

# A11y (if UI phase)
pnpm --filter "./packages/ui" test:a11y 2>/dev/null || true

echo "✅ All quality gates passed"
```

### Final Validation with Subagent

```
@task-completion-validator

Phase ${phase_num} FINAL VALIDATION

Plan: ${plan_path}
Progress: ${progress_file}

Comprehensive validation required:
1. All tasks in plan completed
2. All success criteria met
3. All tests passing
4. No critical issues
5. Documentation complete
6. Ready for next phase
```

## Success Criteria Review

For each success criterion in the plan:

```markdown
## Success Criteria Review

### Performance Requirements (if applicable)
- [x] Lighthouse Performance score >90 - Score: 92
- [x] FCP <1.5s - Measured: 1.2s
- [x] LCP <2.5s - Measured: 2.1s

### Accessibility Requirements (if applicable)
- [x] WCAG 2.1 AA compliance - Validated with axe
- [x] Zero critical violations - Confirmed

### Testing Requirements
- [x] E2E coverage >80% - Coverage: 85%
- [x] Unit coverage >70% - Coverage: 78%
```

## Final Progress Update

Update progress tracker via artifact-tracker:

```
Task("artifact-tracker", "Finalize ${PRD_NAME} phase ${phase_num}:
- Mark phase as completed
- Update completion to 100%
- Generate phase completion summary")
```

### Expected Final State

```yaml
---
status: completed
completion: 100%
completed_at: ${timestamp}
---

## Phase Completion Summary

**Total Tasks:** X
**Completed:** X
**Success Criteria Met:** X/X
**Tests Passing:** ✅
**Quality Gates:** ✅

**Key Achievements:**
- [Achievement 1]
- [Achievement 2]

**Technical Debt Created:**
- [Any intentional shortcuts with tracking issue]

**Recommendations for Next Phase:**
- [Suggestion 1]
- [Suggestion 2]
```

## Context Document Update

After phase completion, update `.claude/worknotes/${PRD_NAME}/context.md`:

```markdown
## Important Learnings from Phase ${phase_num}

- **[Learning 1]:** Description and how to handle
- **[Learning 2]:** Description and implications

## Patterns Established

- **[Pattern]:** How it was implemented and why
```

## Push All Changes

```bash
git push origin ${branch_name}
echo "✅ Phase ${phase_num} complete and pushed"
```
