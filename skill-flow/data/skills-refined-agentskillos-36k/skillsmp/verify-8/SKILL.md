---
name: verify
description: 'Rigorous self-assessment checklist before marking any task as complete. Use when about to claim task completion, before final commit, when user asks "is it done?", or when transitioning from implementation to reporting. Prevents premature completion claims by requiring evidence for every assertion.'
user-invocable: true
---

# Verification Protocol

**Workflow Reference**: See [Master Workflow](./../knowledge/workflow-diagrams/master-workflow.md) for how this skill fits into the verification stage of the agentic workflow.

**STOP.** You are NOT done yet. Generate this checklist and provide **EVIDENCE** for every item.

---

## 1. Task Type & Strategy

- [ ] **Type:** FIX / FEATURE / REFACTOR / DOCS / INVESTIGATION
- [ ] **Strategy:** Executable verification vs. Static verification?

---

## 2. The "WORKS" Check

Choose A or B based on task type:

### A. For Code (Executable)

- [ ] **Execution:** Terminal output showing successful run? (Exit code 0 is NOT enough)
- [ ] **Regression:** Evidence that existing tests still pass?
- [ ] **Edge Cases:** Evidence of testing failure scenarios?

```text
EVIDENCE:
- Execution output: [paste actual output]
- Test results: [paste test output]
- Edge case tested: [describe scenario and result]
```

### B. For Static Assets (Docs, Configs, Analysis)

- [ ] **Accuracy:** Verified against source code/schema?
- [ ] **Clarity:** Does it follow the established format?
- [ ] **Validity:** Do links/references resolve?

```text
EVIDENCE:
- Accuracy check: [how verified]
- Format compliance: [standard followed]
- Links validated: [method used]
```

---

## 3. The "FIXED" Check

For bug fixes specifically:

- [ ] **Reproduction:** Did I observe the pre-fix state?
- [ ] **Resolution:** Does the original problem NO LONGER occur?

```text
EVIDENCE:
- Pre-fix behavior: [what was observed]
- Post-fix behavior: [what is now observed]
- Regression test added: [yes/no, location]
```

---

## 4. Quality Gates

- [ ] Pre-commit hooks passed?
- [ ] Linting passed? (Necessary, but not sufficient)
- [ ] Type checking passed? (if applicable)

```text
EVIDENCE:
- Pre-commit: [output or "not configured"]
- Linting: [tool and result]
- Type check: [tool and result]
```

---

## 5. Honesty Check

- [ ] Did I verify the _full scope_?
- [ ] Am I distinguishing between "should work" and "verified to work"?
- [ ] Can I answer YES to: "I have VALIDATED this output in its intended context"?

---

## The Golden Rule

**If you cannot demonstrate it working in practice with evidence, it is NOT done.**

| Claim           | Required Evidence                  |
| --------------- | ---------------------------------- |
| "Code works"    | Terminal output showing execution  |
| "Tests pass"    | Actual test output, not assumption |
| "Bug fixed"     | Before/after comparison            |
| "Docs accurate" | Cross-reference with source        |
| "Config valid"  | Validation command output          |

---

## Quick Reference

```text
VERIFICATION SUMMARY:
Task Type: [FIX/FEATURE/REFACTOR/DOCS/INVESTIGATION]
Works Check: [PASS/FAIL] - Evidence: ___
Fixed Check: [PASS/FAIL/N/A] - Evidence: ___
Quality Gates: [PASS/FAIL] - Evidence: ___
Honesty Check: [PASS/FAIL]

VERDICT: [COMPLETE / NOT COMPLETE - reason]
```
