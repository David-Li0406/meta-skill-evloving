# Quality Gates Reference

## Purpose

Consolidated quality gates enforcing constitutional compliance across all SDD phases.

---

## Constitutional Article Mapping

| Article | Principle | Gate Location | Enforcement |
|---------|-----------|---------------|-------------|
| I | Intelligence-First | Phases 0, 3, 5 | Query project-intel.mjs BEFORE file reads |
| II | Evidence-Based | All phases | CoD^Σ traces required for all claims |
| III | Test-First | Phase 8 | ≥2 ACs per story, tests before code |
| IV | Specification-First | Phases 3-8 | spec.md → plan.md → code sequence |
| V | Template-Driven | All phases | Use standard templates |
| VI | Simplicity | Phases 0, 5 | ≤3 projects, ≤2 abstraction layers |
| VII | User-Story-Centric | Phases 3, 6 | Tasks organized by P1/P2/P3 stories |
| VIII | Parallelization | Phase 6 | [P] markers for parallel tasks |

---

## Phase-Specific Quality Gates

### Phase 0: System Understanding

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| Intel-First | All intel queries before file reads | Review query log |
| Entity Coverage | ≥80% of files mapped to entities | Count ratio |
| Relationship Accuracy | Dependencies verified | project-intel.mjs output |
| Diagram Validity | Mermaid renders | Syntax validation |
| Evidence | All entities have file:line | CoD^Σ presence |

**Pass Criteria**: All 5 gates pass

---

### Phase 1: Product Definition

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| User Focus | No technical details | Grep for "API", "database" |
| Clarity | Personas are specific | Named personas present |
| JTBD | ≥1 core job defined | Job statement exists |
| Boundaries | In/out of scope defined | Both sections populated |
| Evidence | Based on research | References section |

**Pass Criteria**: 4/5 gates pass (Boundaries can be optional for MVP)

---

### Phase 2: Constitution Generation

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| Traceability | Every article traces to product.md | CoD^Σ traces |
| Completeness | All 7 articles defined | Count articles |
| Enforcement | Each article has mechanism | Check sections |
| No Invention | Derived, not invented | Verify sources |

**Pass Criteria**: All 4 gates pass

---

### Phase 3: Feature Specification

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| FR Coverage | ≥3 functional requirements | Count FRs |
| AC Minimum | Each story has ≥2 ACs | Check all US-* |
| Testability | ACs can be tested | No vague language |
| Traceability | Links to product/constitution | References section |
| No Ambiguity | No [NEEDS CLARIFICATION] | Grep for marker |

**Pass Criteria**: All 5 gates pass (Gate 5 allows Phase 4 if failed)

---

### Phase 4: Clarification

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| All Resolved | Zero markers remaining | grep returns 0 |
| Documented | Clarification log updated | Log section exists |
| Consistent | Answers don't conflict | Review related FRs |

**Pass Criteria**: All 3 gates pass

---

### Phase 5: Implementation Planning

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| Constitutional | All articles pass | Gate check complete |
| Research | External deps documented | research.md exists |
| Coverage | All US mapped to tasks | Count matches |
| Estimates | No XL tasks | All tasks ≤ L |
| Dependencies | Clear task order | Deps column populated |
| Risks | Risks identified | Risk table has entries |

**Pass Criteria**: 5/6 gates pass (Research optional if no external deps)

---

### Phase 6: Task Generation

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| Coverage | All plan tasks in tasks.md | Count matches |
| ACs | Each task has ≥1 AC | No empty AC sections |
| Dependencies | Valid, no circular | Dependency graph check |
| Priorities | Organized P1 → P2 → P3 | Order correct |
| Parallelization | [P] markers present | Grep for markers |

**Pass Criteria**: All 5 gates pass

---

### Phase 7: Audit

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| Constitution | 7/7 articles pass | All checks green |
| FR Coverage | 100% | RTM complete |
| AC Coverage | ≥1 task AC per story AC | Count comparison |
| Dependencies | No cycles, no missing | Graph analysis |
| Clarifications | 0 markers | grep returns 0 |
| Blockers | 0 critical | Blocker count |

**Pass Criteria**: All 6 gates pass for PASS verdict

---

### Phase 8: Implementation

| Gate | Requirement | Check Method |
|------|-------------|--------------|
| TDD | Tests before code | File timestamps |
| AC Coverage | All ACs tested | Test docstrings |
| Task Updates | Immediate completion | Verify timestamps |
| Test Pass | All tests green | pytest output |
| Story Verification | Report per story | File exists |

**Pass Criteria**: All 5 gates pass per story

---

## Gate Failure Handling

### Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **CRITICAL** | Blocks progression | Must fix before next phase |
| **HIGH** | Should fix | Warn but allow with acknowledgment |
| **MEDIUM** | Recommended fix | Log and continue |
| **LOW** | Nice to have | Note in report |

### Failure Response Matrix

| Gate Failed | Phase | Severity | Response |
|-------------|-------|----------|----------|
| Intel-First | 0,3,5 | HIGH | Re-run with queries first |
| AC Minimum | 3 | CRITICAL | Add more ACs |
| [NEEDS CLARIFICATION] | 3 | CRITICAL | Run Phase 4 |
| Constitution | 7 | HIGH | Fix non-compliant articles |
| 100% Coverage | 7 | CRITICAL | Add missing task coverage |
| TDD | 8 | HIGH | Delete code, write tests first |

---

## Automated Gate Checks

```python
def run_quality_gates(phase: int, artifacts: dict) -> dict:
    """Run all quality gates for a phase."""

    gates = get_gates_for_phase(phase)
    results = {"pass": True, "gates": {}, "blockers": []}

    for gate in gates:
        gate_result = gate.check(artifacts)
        results["gates"][gate.name] = gate_result

        if not gate_result["pass"]:
            if gate.severity == "CRITICAL":
                results["pass"] = False
                results["blockers"].append(gate.name)
            elif gate.severity == "HIGH":
                results["warnings"].append(gate.name)

    return results
```

---

## Gate Report Format

```markdown
## Quality Gate Report

**Phase**: {phase_number} - {phase_name}
**Status**: **PASS** / **FAIL**

### Gate Results

| Gate | Status | Details |
|------|--------|---------|
| {gate_name} | ✅ PASS / ❌ FAIL | {details} |

### Blockers (Must Fix)
1. {blocker description}

### Warnings (Should Fix)
1. {warning description}

### Recommendations
1. {recommendation}
```

---

## Cross-Phase Consistency

**Artifacts must remain consistent across phases:**

| Check | Phases | Validation |
|-------|--------|------------|
| FR count | 3, 5, 7 | Same count across artifacts |
| US count | 3, 6, 7 | Same count across artifacts |
| Task count | 5, 6, 7 | Same count across artifacts |
| AC count | 3, 6, 8 | Task ACs ≥ Story ACs |
| Timestamps | All | Correct sequence |

---

## Constitutional Compliance Checklist

**For each phase, verify:**

```markdown
## Constitutional Compliance

- [ ] **Article I**: Intel queries before file reads
- [ ] **Article II**: CoD^Σ traces for all claims
- [ ] **Article III**: ≥2 ACs per user story
- [ ] **Article IV**: Spec before plan before code
- [ ] **Article V**: Standard templates used
- [ ] **Article VI**: ≤3 projects, ≤2 layers
- [ ] **Article VII**: Tasks by user story priority
- [ ] **Article VIII**: [P] markers for parallel tasks
```

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
