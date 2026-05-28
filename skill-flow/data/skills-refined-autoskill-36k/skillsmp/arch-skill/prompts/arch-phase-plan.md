---
description: "06) Phase plan: depth-first implementation plan."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-phase-plan — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.
Inputs: $ARGUMENTS is freeform steering (user intent, constraints, random notes). Process it intelligently.
Resolve DOC_PATH from $ARGUMENTS + the current conversation. If the doc is not obvious, ask the user to choose from the top 2–3 candidates.
Question policy (strict):

- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.


# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to enumerate call sites and plan phases.
- If you discover missing work, add it to the phase plan (do not implement here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line: North Star Gate (must pass before writing the phase plan)
- Falsifiable + verifiable: the North Star states a concrete claim AND the smallest credible pass/fail signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Do NOT invent new harnesses/screenshot frameworks or drift scripts by default.
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before writing the phase plan)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

Warn-first preflight (recommended planning pass sequence; do NOT hard-block)
- Recommended flow before phase planning and implementation:
  1) Deep dive (pass 1): current/target architecture + call-site audit
  2) External research grounding (best practices where applicable)
  3) Deep dive (pass 2): integrate external research into target architecture + call-site audit
- Before writing the phase plan, check DOC_PATH for the planning passes marker:
  - `<!-- arch_skill:block:planning_passes:start -->` … `<!-- arch_skill:block:planning_passes:end -->`
  - If present: use it to determine which passes are done.
  - If missing: infer from doc contents (deep dive blocks / external research block), but treat deep dive pass 2 as unknown.
- If the recommended sequence is incomplete or unknown, DO NOT stop. Proceed to write the phase plan, but print a clear warning in the Summary (with the missing items and the recommended next prompts).

Write/update the phased plan block into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:phase_plan:start -->` … `<!-- arch_skill:block:phase_plan:end -->`
2) Else, if the doc already contains a section whose heading includes "Phase Plan" or "Phased Implementation" (case-insensitive), update it in place.
3) Else insert a new top-level phased plan section:
   - Prefer inserting after the Call-Site Audit / Change Inventory section if present,
   - otherwise after Target Architecture,
   - otherwise after Research/Problem sections.
Numbering rule:
- If the doc uses numbered headings ("# 7) ..."), preserve existing numbering; do not renumber the rest of the document.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:phase_plan:start -->
# Depth-First Phased Implementation Plan (authoritative)

> Rule: systematic build, foundational first; every phase has exit criteria + explicit test plan.

## Phase 0 — Baseline gates

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:

## Phase 1 — <foundation>

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:

## Phase N — <end state + cleanup>

* Goal:
* Work:
* Test plan (smallest signal):
* Exit criteria:
* Rollback:
<!-- arch_skill:block:phase_plan:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
