---
description: "Plan enhancer: turn an existing plan into the best possible architecture by your standards."
argument-hint: "<Paste anything. If you have a doc, include docs/<...>.md somewhere in the text.>"
---
# /prompts:arch-plan-enhance — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

# North Star (authoritative)
Given DOC_PATH + the repo, produce the best possible target architecture and plan for this change by my standards — i.e. the most idiomatic, simplest design that is correct‑by‑construction, single‑source‑of‑truth, and hard to drift. It must proactively consolidate related patterns across the codebase, define enforceable boundaries/invariants (structure, APIs, deletions, tests/CI where appropriate), and eliminate parallel implementations. The only remaining open questions are true product/UX scope decisions that cannot be derived from code or the stated North Star.

$ARGUMENTS is freeform steering. Treat it as intent + constraints + random thoughts.

DOC_PATH:
- If $ARGUMENTS includes a docs/<...>.md path, use it.
- Otherwise infer from the conversation.
- If ambiguous, ask me to pick from the top 2–3 candidates.

Question policy (strict: no dumb questions):

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
- You may read code and run read-only searches to ground architectural decisions and call-site lists.
- If you discover implementation gaps or required refactors, write them into DOC_PATH (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Work you do (high-level, no ceremony):
- Read DOC_PATH fully.
- Read enough code to make real decisions (code is ground truth).
- Improve the plan/architecture aggressively:
  - Make SSOT explicit; remove parallel solutions.
  - Make boundaries/invariants enforceable (module/API structure, deletes/cleanup, fail-loud behavior). Prefer architectural enforcement over new harnesses/lints/scripts by default.
  - Find and list all call sites; include adoption/migration steps.
  - Drift sweep: identify other places that should adopt the central pattern; propose include vs follow-up vs ignore.
    - Treat the plan’s scope as authoritative; do NOT ask the user to re-decide scope here.
    - If it expands UX scope or meaningfully expands work, default to follow-up/ignore and proceed.
  - Evidence plan must be common-sense and non-blocking: prefer existing tests/checks; otherwise instrumentation/log signature or a short manual checklist. Avoid verification bureaucracy.

Stop-the-line gates (must pass before heavy edits)
- North Star Gate: doc has a falsifiable + verifiable claim, and explicit stop-the-line invariants.
- UX Scope Gate: explicit UX in-scope and UX out-of-scope (what users see changes vs does not change).
If either gate fails, STOP and ask me to fix/confirm those sections (no other questions).

Update DOC_PATH by inserting/replacing this block (do NOT assume section numbers):
1) If `<!-- arch_skill:block:plan_enhancer:start -->` exists, replace inside markers.
2) Else insert near the end before Decision Log, or just append.

<!-- arch_skill:block:plan_enhancer:start -->
# Plan Enhancer Notes (authoritative)

## What I changed (plan upgrades)
- <bullets>

## Architecture verdict
- Is this now “best possible by our standards”? <yes/no>
- Biggest remaining risks:
  - <bullets>

## Enforceable rules (drift-proofing)
- <rules we will enforce architecturally, not socially>

## Call sites + migration
- Must-change call sites:
  - `<path>` — <symbol> — <why>
- Deletes / cleanup (no parallel paths):
  - `<path>` — <what gets deleted>

## Consolidation sweep (anti-blinders)
- Other places that should adopt the new central pattern:
  - <area> — Proposed: <include|follow-up|ignore> — <why>

## Evidence (non-blocking)
- Proof we’ll rely on:
  - <existing test/check OR instrumentation/log signature OR manual checklist> — <pass/fail>
- What we will not block on:
  - <e.g. “screen recordings”, “sim screenshot baselines”>

## Questions (ONLY if truly needed)
- <product/UX scope decision> (must include context + your default recommendation)
<!-- arch_skill:block:plan_enhancer:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
