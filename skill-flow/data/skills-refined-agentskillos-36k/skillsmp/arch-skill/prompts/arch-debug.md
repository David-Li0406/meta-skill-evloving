---
description: "15) Debug (plan-aware): prove root cause with high certainty, then propose an elegant plan-aligned fix."
argument-hint: "<Paste what you're seeing: symptoms, logs, repro steps. Optional: include a docs/<...>.md path anywhere to pin the plan doc.>"
---
# /prompts:arch-debug — $ARGUMENTS
Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: In the context of the relevant architecture plan, debug holistically and get to “100% certainty” on the root cause (or explicitly state what prevents certainty), then propose the most elegant fix that is aligned with the plan and reduces competing sources of truth.

Inputs:
- $ARGUMENTS is the symptom report (everything the user typed after invoking this prompt). Treat it as: symptoms + logs + repro steps + environment notes + random steering.

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

Stop-the-line gates (must pass before debugging deeper)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the plan doc before proceeding.

Hard rules:
1) Code is ground truth. No speculation without evidence anchors.
2) Prefer the earliest failure site (where state first becomes wrong), not the last place that notices it.
3) You MAY add minimal instrumentation/logs if required to prove causality; keep instrumentation in place until the user confirms the fix works.
4) Do not implement the final fix in this prompt. End with a proposal aligned to the plan and mapped to plan phases.

Process:
1) Read DOC_PATH fully and extract:
   - Current phase (or best inference)
   - Stop-the-line invariants + definition-of-done evidence
   - Relevant call-site audit rows + internal ground truth anchors
   - Constraints/tradeoffs that affect debugging or fixes

2) Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`.
   - If WORKLOG_PATH does not exist, create it.
   - Add cross-links:
     - Plan doc should reference the worklog near the top.
     - Worklog should link back to the plan doc.

3) If WORKLOG_PATH exists, read it and extract:
   - Latest progress notes related to this subsystem
   - Any prior similar failures / mitigations

4) Parse the symptom report ($ARGUMENTS) into:
   - Expected vs actual
   - Trigger / repro steps (if present)
   - Environment (platform, build type, branch/commit, device/sim, etc. if present)
   If essential repro info is missing and cannot be inferred from logs/worklog, ask only for the minimum needed.

5) Holistic grounding (do not “local-fix”):
   - Read the relevant code referenced by the plan doc (internal anchors, call sites).
   - Expand outward: immediate upstream/downstream boundaries, concurrency/thread boundaries, caches, and “sources of truth” transitions.

6) Build a small hypothesis table (2–5 max):
   - Hypothesis (concrete, falsifiable)
   - What evidence would prove/disprove it
   - Earliest failure site candidate (file/symbol)
   - Smallest discriminating experiment

7) Reproduce:
   - Prefer the plan doc’s phase test plan.
   - Otherwise prefer the smallest existing harness (targeted unit test, make target, script, minimal UI flow).
   - If no repro is available, use logs to build the smallest reproducible probe (but do NOT guess).

8) Reach certainty (or state why you can’t):
   - Iterate on discriminating experiments (not additional speculation).
   - If you cannot reach certainty, list:
     - What evidence is missing
     - The minimal next experiment/instrumentation to settle it

9) Write a “Debugging Session” entry to WORKLOG_PATH (append). Do not paste the full block to the console:
   - Symptoms (expected vs actual)
   - Repro(s) tried + results
   - Hypotheses considered + which were eliminated and why
   - Root cause (proven vs not yet proven) + evidence anchors (file:line)
   - Instrumentation added (if any)
   - Plan-aligned fix proposal (recommended + alternatives) and which plan phase(s) it maps to

10) Update DOC_PATH only if needed:
   - If debugging reveals plan drift or requires changing sequencing/assumptions, append a Decision Log entry.
   - Otherwise keep the plan doc unchanged.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
