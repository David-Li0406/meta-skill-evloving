---
name: analysis-design
description: Systematic analysis and reasoning workflows. Use when performing audits, investigation, requirements analysis, risk analysis, scenario/edge-case enumeration, or design analysis that demands evidence-based, comprehensive coverage.
allowed-tools: ["shell", "apply_patch", "read_file", "write_file", "update_plan"]
metadata:
  short-description: Structured analysis workflow
---

# Analysis Design

**Read these reference files before proceeding:**
- `~/.config/agent/core/behavior.md` - Critical thinking and evidence requirements
- `~/.config/agent/core/methodology.md` - 5-phase problem-solving framework
- `~/.config/agent/core/efficiency.md` - Parallelization and throughput
- `~/.config/agent/core/task-management.md` - TODO discipline
- `~/.config/agent/core/principles.md` - Engineering principles
- `~/.config/agent/core/communication.md` - Communication standards
- `~/.config/agent/domain/architecture/decomposition.md` - Problem breakdown
- `~/.config/agent/domain/architecture/parallelization.md` - Parallel execution
- `~/.config/agent/domain/testing/unit.md` - Unit testing strategy
- `~/.config/agent/domain/testing/coverage.md` - Coverage expectations

## Instructions

Apply all guidance from the reference files listed above.

Use this workflow when the task requires rigorous, comprehensive analysis:

1. **Scope & Objective**
   - Restate the objective and success criteria explicitly.
   - Define in-scope and out-of-scope boundaries.
   - Capture constraints and assumptions up front.

2. **Evidence Collection**
   - Read relevant files and source-of-truth artifacts before reasoning.
   - Record evidence with precise references (paths, symbols, tests).
   - Mark each claim as Verified or Unverified based on evidence.

3. **Scenario/Edge-Case Matrix**
   - Enumerate all viable scenarios/contexts (including non-goals).
   - For each scenario, specify expected behavior and verification status.
   - Tag missing coverage explicitly as TODO with a test plan.

4. **Risk & Unknowns**
   - Identify unknowns and risks early; propose mitigations or decision points.
   - Separate solvable risks from unsolvable ones; document residual risk.

5. **Recommendations & Plan**
   - Provide prioritized recommendations (P0/P1/P2 or equivalent).
   - Map each recommendation to evidence and a verification step.
   - Update or produce a plan that reflects verified gaps and required policy decisions.

6. **Verification Strategy**
   - Define how correctness, safety, and completeness will be validated.
   - Prefer tests or reproducible checks; document gaps if verification is blocked.

**Deliverables (as applicable):**
- Evidence log (Verified vs Unverified)
- Scenario/edge-case matrix with TODOs
- Risk register with mitigation plan
- Updated implementation plan or decision record

## Arguments

Target: ${ARGUMENTS}
