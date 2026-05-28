# arch_skill — Purpose + Execution Outline

## Purpose
Define a repeatable, interactive workflow for producing high-quality architecture documents using the standard template in `docs/arch_skill_raw_notes.md`.

## Intended outcome (final work product)
A completed architecture document that:
- Follows the structure and quality bar in `docs/arch_skill_raw_notes.md`.
- Is grounded in code and external evidence.
- Includes an executable phased plan with tests and rollback criteria.
- Stays updated during execution with decisions, changes, and status.

## Scope
- The skill governs the end-to-end workflow of producing the architecture doc and guiding execution.
- The skill does not implement code by default; it drives planning, alignment, and verification.

## Inputs
- Target repo path.
- Problem statement or change request.
- The architecture template in `docs/arch_skill_raw_notes.md`.
- Access to internal code and external sources.

## Outputs
- Primary: one architecture document using the template.
- Secondary: research notes, call-site audit table, phase plan, decision log.

## UI work requirement (ASCII mockups)
If the change touches UI/UX, the architecture doc must include **ASCII mockups** for:
- Current UI states (as-is).
- Target UI states (to-be).

Minimal example (structure only):
```ascii
┌───────────────────────────────┐
│ [ Left ]   [ Center ] [ Right ] │
└───────────────────────────────┘
```

---

# Skill Architecture (how the skill itself operates)

## Phase 1 — Research (internal + external)
Goal: establish ground truth and evidence.

Activities:
- Internal: codebase scans, call-site discovery, existing patterns, authoritative sources.
- External: prior art, papers, competitor patterns, standards.
- Open questions: list, evidence required to resolve.

Outputs:
- Template section 3 filled (Research Grounding).
- Initial inventory of current architecture and key call sites.

Exit criteria:
- Ground-truth anchors identified with paths/links.
- External anchors summarized with adopt/reject notes.
- User confirms research sufficiency before moving on.

---

## Phase 2 — Architectural planning (target design)
Goal: design the target architecture and make it falsifiable.

Activities:
- Define North Star (claim, scope, invariants, definition of done).
- Document current architecture (as-is).
- Draft target architecture (to-be), including invariants and boundaries.
- Capture tradeoffs and rejected alternatives.

Outputs:
- Template sections 0–6 completed.

Exit criteria:
- Target architecture is coherent and testable.
- Call-site audit is complete enough to plan changes.
- User alignment checkpoint before implementation planning.

---

## Phase 3 — Implementation planning (execution design)
Goal: design the complete implementation and test plan.

Activities:
- Depth-first phased plan with exit criteria and rollbacks.
- Test strategy beyond per-phase tests.
- Rollout + telemetry plan.

Outputs:
- Template sections 7–9 completed.

Exit criteria:
- Plan is executable without ambiguous gaps.
- Tests and rollback paths are explicit.
- User approval to execute.

---

## Phase 4 — Execution (iterative delivery)
Goal: execute the plan while keeping the architecture doc current.

Activities:
- Execute phases in order, with verification per phase.
- Update decision log and any sections that drift from reality.
- Capture telemetry/verification artifacts.

Outputs:
- Updated architecture doc with execution notes.
- Recorded decisions + changes.

Exit criteria:
- Definition of done satisfied.
- User confirms system meets the North Star.

---

# Helper Skill Structure (to make the process repeatable)

## Trigger + mode
- Trigger: user requests architecture planning or multi-phase architecture execution.
- Mode: interactive, step-by-step, gated by user approval per phase.

## Core loop
1) Ask for target repo + problem statement.
2) Load the architecture template.
3) Run Phase 1–4 (Research → Architectural planning → Implementation planning → Execution), pausing for alignment between phases.
4) Keep the doc updated as the single source of truth.

## Alignment gates
- End of Phase 1 (Research): research sufficiency check.
- End of Phase 2 (Architectural planning — target design): target architecture sign-off.
- End of Phase 3 (Implementation planning — execution design): implementation plan sign-off.
- End of Phase 4 (Execution — iterative delivery): verification sign-off.

## Quality guardrails
- Code is ground truth; no speculation without anchors.
- Single source of truth (no competing patterns).
- No silent fallbacks; fail-loud boundaries.
- Explicit testing for each phase.

## Oversight / verification helpers
- Call-site audit validation step.
- Test plan checklist with pass/fail criteria.
- Decision log upkeep and change tracking.

---

# Mocked Interaction (example planning exercise)

**User:**
We need to redesign the session replay pipeline to eliminate out-of-order state, keep UI responsive, and ship in phases.

**arch_skill:**
Understood. I'll run Phase 1 (research) first and return internal/external anchors for sign-off.

**arch_skill (Phase 1 (Research) summary):**
- Internal anchors: cursor ownership, phase machine, apply/coalescing paths.
- External anchors: cross-thread reconciliation patterns.
- Open questions: whether we can enforce atomic commit without UI regressions.

Proceed to Phase 2 (Architectural planning — target design)? (yes/no)

**User:**
yes

**arch_skill (Phase 2 (Architectural planning — target design) draft highlights):**
- North Star: atomic commit boundary prevents replay regressions.
- Target architecture: commit token + unified phase/apply boundary.
- Call-site audit started.

Proceed to Phase 3 (Implementation planning — execution design)? (yes/no)

**User:**
yes

**arch_skill (Phase 3 (Implementation planning — execution design) plan snapshot):**
- Phase 0: baseline invariant logging + tests.
- Phase 1: commit token + no-regression invariant.
- Phase 2: migrate apply pipeline.
- Phase 3: cleanup old paths.

Proceed to Phase 4 (Execution — iterative delivery)? (yes/no)

# Open Questions (for next iteration)
- What exact format should the final architecture document live in (markdown only, or markdown + YAML frontmatter)?
- Should the skill auto-generate a working doc stub at phase start or only after Phase 1 (Research)?
- What level of external research depth is expected by default?
