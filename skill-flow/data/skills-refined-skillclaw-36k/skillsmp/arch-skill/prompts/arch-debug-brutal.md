---
description: "15a) Brutal debug: prove root cause fast (temporary hacks allowed)."
argument-hint: "<Paste symptoms/logs/repro. Optional: include a docs/<...>.md path to write the diagnosis doc.>"
---
# /prompts:arch-debug-brutal — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: minimize WALL-CLOCK TIME to prove the root cause with high certainty.
This is a DEV diagnosis workflow. Code is NOT precious here:
- You MAY make temporary "brutal cut" changes (comment out layers, force returns, clamp values, hard-code sizes, bypass caches, etc.).
- You SHOULD prefer the fastest discriminating experiments over elegant solutions.
- We will delete/revert the temporary code later; do not waste time building permanent gates or frameworks.
- Avoid adding dev gates/flags/config surfaces (e.g., `__DEV__`, feature flags, env vars) unless absolutely required. Prefer direct edits + quick reverts.

Question policy (extreme):

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

Doc policy (diagnosis log):
1) If $ARGUMENTS includes a docs/<...>.md path, use it as DIAG_PATH (write findings there).
2) Otherwise create a new doc in docs/:
   - `docs/DIAG_<TITLE_SCREAMING_SNAKE>_<DATE>.md`
   - TITLE_SCREAMING_SNAKE = derived from the symptom report as a short 5–9 word title.
   - DATE = today's date in YYYY-MM-DD.
This doc is a scratchpad for brutal efficiency. It does NOT need to match the full architecture template.

Stop conditions:
- Stop as soon as the root cause is proven with evidence anchors.
- If you cannot reach certainty quickly, stop with the single smallest next experiment that will settle it.

Stop-the-line (MANDATORY; prevents “wandering”):
- You MUST write the structured theory doc + brutal test plan into DIAG_PATH BEFORE touching code or running experiments.
  - Minimum bar: at least 3 top theories + at least 3 brutal tests (B1–B3) written down.
- Brutal tests are TRAPS / NEGATIVE PROOF — not logs.
  - A brutal test must force a binary outcome by changing the world (disable/bypass/short-circuit/clamp/replace), not merely observe.
  - “Add logs” is instrumentation, not a brutal test, and does not count as B*.

Process (optimize for binary isolation):
1) Parse $ARGUMENTS into: expected vs actual, repro steps (if any), scope notes (what is NOT affected), and any evidence already present (logs, screenshots).
2) Build a short hypothesis list (max 6). Each hypothesis must be falsifiable and must name a likely earliest failure site.
3) Design a brutal test plan that maximizes information per minute:
   - Start coarse (disable entire suspect subtrees/layers/providers) before going fine-grained.
   - When the render tree is complex, do a literal binary search: cut ~50% of the suspect subtree, repro, then cut again based on results.
   - One change at a time; run the fastest repro; record outcome; revert; repeat.
   - Prefer “hard cut” tests like:
     - Temporarily disable a render layer / overlay / provider / effect scene.
     - Render a neon full-rect sentinel (proves stacking/opacity/culling quickly).
     - Clamp suspect opacities/alphas to 1 (or 0) to isolate alpha accumulation.
     - Replace `SkiaOpacity(requiresLayer)` with a plain Group to eliminate saveLayer behavior.
     - Short-circuit an entire component subtree: `return null`.
     - Freeze state updates (force a constant snapshot) to rule out state churn.
     - Force a single mount (assert only one provider/scene exists).
4) Instrumentation rules (fast, disposable):
   - Logs are NOT a brutal test. Logs are only for pinpointing the exact line AFTER a trap isolates the guilty subsystem.
   - Add logs at the earliest failure site (and 1–2 key boundaries) only if needed to prove causality after hard-cut tests narrow the search.
   - Avoid hot-loop logs unless absolutely necessary.
   - You MAY keep logs/instrumentation in place until the issue is fixed; do not prematurely clean up.
5) Track “files modified” continuously so we can revert quickly.

Write/update the diagnosis doc at DIAG_PATH as you go (do not wait until the end).
Use this structure (adapt as needed; do not be verbose):

# <Title> (Diagnosis)
Date: <YYYY-MM-DD>

## Problem statement
- <1–3 bullets: expected vs actual>

## Scope
- In scope:
- Out of scope:

## Evidence
- <logs/traces/observations already known>

## Top theories (structured; must be written before coding)
- T1 — <hypothesis (falsifiable)>
  - Earliest failure site: `<path#symbol>`
  - Trap (negative proof): <disable/bypass/clamp/replace>
  - Pass/fail signal: <what proves/disproves>
  - Status: <untried|ruled out|likely|proven>
- T2 — ...
- T3 — ...

## Brutal test plan (TRAPS; not logs)
> Rule: B* tests must change the world to force a binary outcome (disable/bypass/short-circuit/clamp/replace). Logging is not a B* test.
- B1 — <short name>
  - Change (trap): <hard cut / bypass / clamp / replace>
  - What it proves (binary): <proves/disproves>
  - Expected (if theory true):
  - Expected (if theory false):
  - Revert notes: <how to revert fast>
- B2 — ...
- B3 — ...

## Experiments run (append-only; keep it tight)
- B1 — <what you changed (trap)>
  - Result: <pass|fail>
  - What it proved: <ruled out / narrowed to>
  - Files modified:
    - <path>
    - <path>
- B2 — ...

## Root cause (proven)
- <one sentence>
- Evidence anchors:
  - <path:line> — <why it proves it>

## Fix shape (proposal, not implementation)
- <minimal fix that removes the cause>
- Cleanup to do after fix:
  - remove diagnostics / revert temporary cuts

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
