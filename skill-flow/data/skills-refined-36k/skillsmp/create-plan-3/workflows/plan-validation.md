# Phase 4: Validate Plan

**Purpose**: Ensure plan meets quality gates before implementation begins.

---

## Step 4.1: Requirement Coverage Check

**Validate 100% Coverage**:

```markdown
### Requirement Coverage
- [ ] REQ-001 → T1, T2, T3 ✓
- [ ] REQ-002 → T4, T5 ✓
- [ ] REQ-003 → T6, T7 ✓
- [ ] Coverage: 100% ✓
```

**Enforcement**:
- Every requirement MUST map to at least one task
- Every task SHOULD map to a requirement (or mark as infrastructure)
- No orphaned tasks or uncovered requirements

**If < 100%**:
1. Identify missing requirements → Add tasks
2. Identify orphaned tasks → Map to requirement or remove

---

## Step 4.2: Task Quality Check

**Acceptance Criteria Validation** (Article III):

```markdown
### Task Quality
- [ ] All tasks have 2+ ACs
- [ ] All ACs are testable (pass/fail clear)
- [ ] No vague ACs ("works", "is good", "looks nice")
- [ ] ACs are independently verifiable
```

**Per-Task Checklist**:
```markdown
Task T1:
- [ ] Has ≥2 ACs ✓
- [ ] Each AC testable ✓
- [ ] ACs specific (not vague) ✓

Task T2:
- [ ] Has ≥2 ACs ✓
- [ ] Each AC testable ✓
- [ ] ACs specific ✓
```

**Violation Example**:
```markdown
### Task 3: Add login button
**Acceptance Criteria:**
- [ ] Button works  ❌ Vague!
```

**Fixed**:
```markdown
### Task 3: Add login button
**Acceptance Criteria:**
- [ ] AC1: Button renders with "Log in with Google" text
- [ ] AC2: Button click triggers OAuth redirect
- [ ] AC3: Button shows loading spinner during authentication
```

---

## Step 4.3: Dependency Validation

**Check Dependency Graph**:

```markdown
### Dependencies
- [ ] All dependencies identified
- [ ] No circular dependencies
- [ ] Critical path documented
- [ ] Parallel work opportunities marked
```

**Circular Dependency Check**:
```
T1 → T2 → T3 → T1  ❌ Cycle detected!
```

**Resolution**: Break cycle by restructuring or removing optional dependency.

---

## Step 4.4: Estimate Validation

**Check Task Sizing**:

```markdown
### Estimates
- [ ] All tasks have time estimates
- [ ] Tasks sized to 2-8 hours
- [ ] Large tasks (>8h) broken down
- [ ] Critical path timing documented
```

**Example**:
```
T1: 2 hours ✓
T2: 6 hours ✓
T3: 12 hours ❌ Too large! Break into T3a, T3b
```

---

## Step 4.5: Constitutional Compliance Check

**Article I: Intelligence-First**:
- [ ] project-intel.mjs queries executed
- [ ] Evidence saved to /tmp/*.json
- [ ] File:line references in plan

**Article II: Evidence-Based Reasoning**:
- [ ] CoD^Σ traces documented
- [ ] Claims have file:line evidence
- [ ] Assumptions marked explicitly

**Article III: Test-First Imperative**:
- [ ] Every task has ≥2 ACs
- [ ] ACs are testable
- [ ] Tests run before implementation

**Article IV: Specification-First**:
- [ ] spec.md exists (input requirement)
- [ ] Plan derived from spec, not invented
- [ ] Spec requirements mapped to tasks

**Article V: Template-Driven Quality**:
- [ ] plan.md follows template structure
- [ ] Required sections present
- [ ] Consistent format

**Article VI: Simplicity & Anti-Abstraction**:
- [ ] Complexity justified if >3 layers
- [ ] Framework features used directly
- [ ] No unnecessary abstractions

**Article VII: User-Story-Centric**:
- [ ] Tasks grouped by user story (if applicable)
- [ ] Stories independently testable
- [ ] MVP-first organization

**Article VIII: Parallelization Markers**:
- [ ] Independent tasks marked [P]
- [ ] Parallel work documented

---

## Step 4.6: Generate plan.md

**File Naming**: `YYYYMMDD-HHMM-plan-<id>.md` OR `specs/<feature>/plan.md`

**Template**: @.claude/templates/plan.md

**Required Sections**:
```markdown
---
plan-id: <id>
created: <YYYY-MM-DD>
status: Draft
---

# Implementation Plan: <Title>

## Summary
[One-paragraph overview]

## Requirements
[REQ-001, REQ-002, etc.]

## Tasks
[T1, T2, T3, ... with ACs]

## Dependencies
[Task graph, critical path]

## Estimates
[Time per task, total time]

## Risks
[Potential blockers]

## Verification
[How to validate completion]
```

---

## Step 4.7: Success Criteria

**Plan Quality Metrics**:

```markdown
### Plan Quality
- [ ] 100% requirement coverage
- [ ] 100% of tasks have 2+ ACs
- [ ] No circular dependencies
- [ ] Critical path identified
- [ ] Parallel work marked
```

**Estimating Quality**:
```markdown
### Estimating
- [ ] Tasks sized to 2-8 hours
- [ ] Critical path identified
- [ ] Total time estimate: <N> hours
- [ ] Parallel work opportunities noted
```

---

## Step 4.8: Review Checklist

Before finalizing plan, verify:

**Content Quality**:
- [ ] Every requirement covered by tasks
- [ ] Every task has ≥2 testable ACs
- [ ] Dependencies identified and valid
- [ ] Estimates realistic (2-8h per task)

**Constitutional Compliance**:
- [ ] Article I: Intelligence queries executed
- [ ] Article II: CoD^Σ traces with evidence
- [ ] Article III: Test-first ACs defined
- [ ] Article IV: Derived from spec.md
- [ ] Article V: Follows plan.md template
- [ ] Article VII: User-story organization (if applicable)

**Readability**:
- [ ] Task descriptions clear and specific
- [ ] ACs unambiguous (pass/fail clear)
- [ ] Dependencies visualized (graph or table)
- [ ] Risks and blockers documented

---

## Output of Phase 4

**Files Generated**:
- `plan.md` (or `specs/<feature>/plan.md`)

**Validation Status**:
```
Requirements Coverage: 100% ✓
Task Quality: All tasks ≥2 ACs ✓
Dependencies: Valid, no cycles ✓
Estimates: All 2-8h, critical path identified ✓
Constitutional: All 8 articles compliant ✓
```

**Next Steps**:
- If validation PASS → Proceed to task generation (generate-tasks skill)
- If validation FAIL → Fix issues, re-validate
- Recommended: Run `/audit` before implementation to catch cross-artifact issues
