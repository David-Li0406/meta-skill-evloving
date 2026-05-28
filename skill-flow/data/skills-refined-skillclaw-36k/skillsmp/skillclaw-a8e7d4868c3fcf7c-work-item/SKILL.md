---
name: work-item
description: Use this skill when you need to finish an active work item end-to-end with proof, ensuring all criteria are met before opening a pull request.
---

# Skill body

## Intent
Ship one work item end-to-end with proof (≥1 validation signal). Shipping protocol: constrain scope, define "done," require evidence.

## Definition of Done
Done when:
- Work item criteria met.
- Formatter/lint-typecheck/build/tests run (or **N/A**).
- ≥1 validation *signal* recorded.
- PR opened (do not merge).

## Workflow

### 0) Preflight (don't skip)
- Confirm source-of-truth record (issue/ticket/PR) + explicit `work` invocation; if blocked (missing requirements/no active work item), stop.

### 1) Identify the active work item (source of truth)
1. Anchor on the source-of-truth record.
2. Find the active work item; if none, propose the next work item and get explicit confirmation before proceeding.
3. Restate "done" for this work item (1 sentence + acceptance criteria).

### 2) Clarify until requirements are implementable
- Ask only judgment calls; everything else is in repo/work item.
- If ambiguity appears mid-implementation, stop and re-clarify.

### 3) Audit the working tree (scope containment)
- Audit early/often; keep work item changes surgical.

### 4) Do the work (how the work is accomplished)

#### 4.1) Mandatory TRACE mini-pass
Before first incision, run a small `$fix` pass:
1. **Heat map**: hotspots + surprises.
2. **Failure triage**: crash > corruption > logic.
3. **Invariant**: what must remain true after the change?
4. **Footgun scan**: any misuse-prone surface?
5. **Incidental complexity**: flatten/rename/extract only if risk drops.

#### 4.2) Complexity gate (pause and invoke CPS)
If complex (multi-constraint, cross-subsystem, high uncertainty, multiple viable designs), stop and invoke `$creative-problem-solver`: produce a five-tier portfolio (signals + escape hatches), ask for selection, resume after choice.

#### 4.3) Surgeon loop (execution)
Tight loop:
1. **Hypothesis**: what change likely satisfies the work item?
2. **Smallest incision**: smallest change that could be correct.
3. **Observable**: test/invariant/log.
4. **Implement**: minimal collateral.
5. **Re-check**: rerun closest fast signal.
6. Repeat until acceptance criteria pass.

Autonomy gate (borrowed from `$fix`): proceed without further clarification only when all are true:
- Local repro (or a tight, credible signal).
- Invariant stated.
- Minimal diff.
- At least one validation signal passes.

Otherwise, clarify before widening scope.