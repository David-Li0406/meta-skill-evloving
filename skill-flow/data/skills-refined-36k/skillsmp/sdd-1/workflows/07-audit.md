# Phase 7: Audit Workflow

## Purpose

Validate consistency and completeness of SDD artifacts before implementation. Creates `specs/$FEATURE/audit-report.md` with PASS/FAIL status.

**Command**: `/audit`
**Requires**: `spec.md`, `plan.md`, `tasks.md`
**Output**: `specs/$FEATURE/audit-report.md`
**Next**: If PASS → Phase 8 (`/implement`), If FAIL → Fix issues and re-audit

---

## Prerequisites

```bash
# Verify all artifacts exist
for file in spec.md plan.md tasks.md; do
  if [ ! -f "specs/$FEATURE/$file" ]; then
    echo "ERROR: Missing specs/$FEATURE/$file"
    exit 1
  fi
done
```

---

## Step 1: Artifact Inventory

```markdown
## Artifact Inventory

| Artifact | Path | Exists | Last Modified |
|----------|------|--------|---------------|
| Specification | specs/$FEATURE/spec.md | ✅/❌ | [date] |
| Plan | specs/$FEATURE/plan.md | ✅/❌ | [date] |
| Tasks | specs/$FEATURE/tasks.md | ✅/❌ | [date] |
| Research | specs/$FEATURE/research.md | ✅/❌/N/A | [date] |
| Data Model | specs/$FEATURE/data-model.md | ✅/❌/N/A | [date] |
```

---

## Step 2: Constitution Compliance

**Check each article:**

### Article I: Intelligence-First
- [ ] Intel queries documented in research.md or plan.md
- [ ] No blind file reads in plan

### Article II: Evidence-Based
- [ ] CoD^Σ traces in plan.md
- [ ] All claims have file:line references

### Article III: Test-First
- [ ] Each user story has ≥2 acceptance criteria
- [ ] Test tasks exist in tasks.md

### Article IV: Specification-First
- [ ] spec.md created before plan.md (check timestamps)
- [ ] plan.md created before tasks.md

### Article V: Template-Driven
- [ ] Standard templates used
- [ ] Consistent formatting

### Article VI: Simplicity
- [ ] Architecture ≤3 projects
- [ ] Abstraction ≤2 layers

### Article VII: User-Story-Centric
- [ ] Tasks organized by user story
- [ ] P1 → P2 → P3 priority order

---

## Step 3: Requirement Coverage

**Trace requirements through artifacts:**

```markdown
## Requirement Traceability Matrix

| FR | In Spec | User Story | Tasks | ACs | Coverage |
|----|---------|------------|-------|-----|----------|
| FR-001 | ✅ | US-1 | T1.1-T1.5 | 5 | 100% |
| FR-002 | ✅ | US-2 | T2.1-T2.3 | 4 | 100% |
| FR-003 | ✅ | US-3 | None | 0 | 0% ❌ |
```

**Coverage Threshold**: 100% (all FRs must have tasks)

---

## Step 4: AC Coverage

**Verify acceptance criteria propagation:**

```markdown
## Acceptance Criteria Coverage

| User Story | Spec ACs | Task ACs | Gap |
|------------|----------|----------|-----|
| US-1 | 3 | 8 | +5 (OK) |
| US-2 | 2 | 4 | +2 (OK) |
| US-3 | 2 | 1 | -1 ❌ |
```

**Rule**: Task ACs ≥ User Story ACs

---

## Step 5: Dependency Validation

**Check for issues:**

```markdown
## Dependency Analysis

### Circular Dependencies
[None found / List any cycles]

### Missing Dependencies
| Task | Declared Dep | Exists | Status |
|------|--------------|--------|--------|
| T1.3 | T1.2 | ✅ | OK |
| T2.1 | T1.5 | ✅ | OK |

### Orphan Tasks
[Tasks with no dependents and not end tasks]
```

---

## Step 6: Consistency Checks

**Cross-artifact validation:**

```markdown
## Consistency Checks

| Check | Status | Details |
|-------|--------|---------|
| Task count matches plan | ✅/❌ | Plan: X, Tasks: Y |
| US count matches spec | ✅/❌ | Spec: X, Plan: Y |
| Estimates reasonable | ✅/❌ | No XL tasks |
| No [NEEDS CLARIFICATION] | ✅/❌ | Count: 0 |
| Priority order | ✅/❌ | P1 → P2 → P3 |
```

---

## Step 7: Risk Assessment

```markdown
## Risk Assessment

| Category | Risk | Severity | Mitigation |
|----------|------|----------|------------|
| Technical | External API dependency | HIGH | Fallback documented |
| Schedule | Large task count | MEDIUM | Parallelization identified |
| Quality | Low AC coverage | LOW | ACs expanded |
```

---

## Step 8: Generate Audit Report

**Template:**

```markdown
# Audit Report: $FEATURE

**Audited**: [timestamp]
**Artifacts**: spec.md, plan.md, tasks.md
**Result**: **PASS** / **FAIL**

---

## Executive Summary

[One paragraph summary of audit findings]

---

## Artifact Inventory

[From Step 1]

---

## Constitution Compliance

| Article | Status | Notes |
|---------|--------|-------|
| I. Intelligence-First | ✅ PASS / ❌ FAIL | [details] |
| II. Evidence-Based | ✅ PASS / ❌ FAIL | [details] |
| III. Test-First | ✅ PASS / ❌ FAIL | [details] |
| IV. Specification-First | ✅ PASS / ❌ FAIL | [details] |
| V. Template-Driven | ✅ PASS / ❌ FAIL | [details] |
| VI. Simplicity | ✅ PASS / ❌ FAIL | [details] |
| VII. User-Story-Centric | ✅ PASS / ❌ FAIL | [details] |

**Overall**: X/7 PASS

---

## Coverage Analysis

### Requirement Coverage
[From Step 3 - RTM]

### AC Coverage
[From Step 4]

**Coverage Score**: X%

---

## Dependency Validation

[From Step 5]

---

## Consistency Checks

[From Step 6]

---

## Risks & Blockers

### Critical Blockers (Must Fix)
1. [Blocker requiring fix before /implement]

### Warnings (Should Fix)
1. [Issue that should be addressed]

### Recommendations
1. [Suggestion for improvement]

---

## Verdict

### PASS Criteria
- [ ] All 7 constitution articles pass
- [ ] 100% FR coverage
- [ ] All US have sufficient task ACs
- [ ] No circular dependencies
- [ ] No [NEEDS CLARIFICATION] markers
- [ ] No critical blockers

### Result: **PASS** / **FAIL**

[If FAIL: List specific items to fix]

---

## Next Steps

**If PASS**:
Ready for `/implement plan.md`

**If FAIL**:
1. Fix blockers listed above
2. Run `/audit` again
```

---

## PASS Criteria

**All must be true for PASS:**

| Criterion | Threshold |
|-----------|-----------|
| Constitution compliance | 7/7 articles |
| FR coverage | 100% |
| AC coverage | ≥1 task AC per story AC |
| Dependencies | No cycles, no missing |
| Clarifications | 0 markers |
| Critical blockers | 0 |

---

## Handling FAIL

**If audit fails:**

1. **Critical blockers**: Must fix before re-audit
2. **Warnings**: Should fix, won't block
3. **Recommendations**: Optional improvements

**After fixes:**
```bash
/audit  # Re-run audit
```

---

## Handoff to Phase 8

**After PASS:**

```markdown
## Phase 7 → Phase 8 Handoff

✅ Audit PASS
✅ All constitution articles compliant
✅ 100% requirement coverage
✅ No blockers

**Ready for**: /implement plan.md
```

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
