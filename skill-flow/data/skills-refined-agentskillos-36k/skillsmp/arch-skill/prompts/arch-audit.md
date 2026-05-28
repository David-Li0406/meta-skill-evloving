---
description: "08) Audit: code vs plan gaps list."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-audit — $ARGUMENTS
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

Documentation-only (audit output):
- This prompt audits code vs plan and updates DOC_PATH. DO NOT modify code.
- You may read code and run read-only searches to find drift/missed call sites.
- If the audit reveals missing code work, record it as gaps/follow-ups in DOC_PATH (do not implement here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line gates (must pass before audit)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.
Compare the architecture doc at DOC_PATH against the actual code in the current repo.
Find gaps, drift, missed call sites, and violations of conventions/patterns.
Update the doc with a **Gaps & Concerns List** using the exact format below.
Write/update the block into DOC_PATH (anti-fragile placement; do not assume specific section numbering).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:gaps_concerns:start -->` … `<!-- arch_skill:block:gaps_concerns:end -->`
2) Else, if a "Gaps & Concerns" section already exists (heading match), update it in place.
3) Else, insert near the end of the doc:
   - Prefer inserting before the Decision Log (if present),
   - otherwise append.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:gaps_concerns:start -->
# Gaps & Concerns List (audit vs code)
## Summary
- Coverage: <what % or rough completeness>
- Primary risk areas:
  - <risk>

## Gaps Table
| Area | File | Symbol / Call site | Expected (per plan) | Actual (in code) | Impact | Fix | Status |
| ---- | ---- | ------------------ | ------------------- | ---------------- | ------ | --- | ------ |
| <module> | <path> | <fn/cls> | <plan intent> | <observed> | <risk> | <proposed> | open |

## Drift / Convention violations
- <rule violated> — <where> — <why it matters>

## Missed spots (unimplemented or partially implemented)
- <spot> — <symptom> — <what remains>

## Follow-ups / questions
- <question>
<!-- arch_skill:block:gaps_concerns:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
