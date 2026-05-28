---
description: "Plan audit: score plan readiness across phases (FULLY specified architecture, FULLY idiomatic, CALL SITES audited)."
argument-hint: "<Paste anything. If you have a doc, include docs/<...>.md somewhere in the text.>"
---
# /prompts:arch-plan-audit — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Goal:
Audit a plan doc against the planning phases and tell me what’s “done / good” vs what’s not there yet.
This is NOT a checkbox exercise; it should reflect the highest standard: best-possible architecture, fully specified, fully idiomatic, drift-proof, and call-site complete.

Inputs:
- $ARGUMENTS is freeform steering. Treat it as intent + constraints + any relevant context.

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

Hard rules:
- Do not modify any files; output only.
- Code is ground truth: you may (and should) read code + use `rg` to validate “call sites audited” claims.

How to score phases:
- PASS = genuinely complete and implementation-ready.
- PARTIAL = present but missing key specifics / not enforceable yet.
- FAIL = missing or too vague to implement safely.
- SKIP = optional for this plan (say why).

What MUST be emphasized (the “big 3”):
1) Target architecture is FULLY specified (not vibes):
   - SSOT is explicit, boundaries are enforceable, contracts/APIs are concrete, migration + delete list prevent parallel paths.
2) Architecture is FULLY idiomatic:
   - Reuses existing repo patterns, avoids inventing new frameworks/abstractions unless clearly necessary.
3) Call sites are AUDITED (exhaustive):
   - Plan enumerates affected call sites; verify by searching the repo for additional call sites and flag any misses.

Minimum audit procedure:
1) Read DOC_PATH fully.
2) Identify the sections (or nearest equivalents) for:
   - North Star + UX scope
   - Research grounding
   - Current architecture (as-is)
   - Target architecture (to-be)
   - Call-site audit / change inventory
   - Phase plan
   - (optional) DevX targets
   - (optional) Review gate
3) Call-site validation:
   - Extract 2–5 key symbols/files from the plan’s target APIs or call-site table.
   - Use `rg` to find call sites in the repo.
   - If you find plausible call sites not represented in the plan, mark Call‑Site Audit as FAIL and list the misses.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
