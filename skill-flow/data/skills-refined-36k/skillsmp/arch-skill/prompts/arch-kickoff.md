---
description: "02) Phase 1 kickoff: research setup + checkpoints."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-kickoff — $ARGUMENTS
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
- You may read code and run read-only searches to inform research anchors.
- If you discover code changes we likely need, write them into DOC_PATH as plan items (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line: North Star Gate (must pass before ANY research/architecture work)
- Falsifiable + verifiable: the North Star states a concrete claim AND the smallest credible pass/fail signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Do NOT invent new harnesses/screenshot frameworks or drift scripts by default.
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before ANY research/architecture work)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

Start Phase 1 (Research). Ask clarifying questions only for product-level ambiguity or missing external constraints.
Summarize research anchors and pause for a lightweight check before Phase 2 (Architectural planning: current/target architecture + call-site audit).
Write the kickoff + summary block into DOC_PATH (anti-fragile placement; do not assume template section numbers).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:phase1_kickoff:start -->` … `<!-- arch_skill:block:phase1_kickoff:end -->`
2) Else insert immediately after the TL;DR section if present.
3) Else insert immediately after YAML front matter if present.
4) Else insert at the top of the document.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:phase1_kickoff:start -->
## Phase 1 Kickoff (Research)
- Repo: <current>
- Target doc: <path>
- Assumptions:
  - <list>
- Questions (ONLY if required for a product decision / external constraint):
  - <Q1> (or "None")
- Plan:
  1) <step>
  2) <step>

## Phase 1 Summary (fill after research)
- Internal anchors:
  - <path> — <behavior>
- External anchors:
  - <source> — <adopt/reject>
- Open questions:
  - <Q> — <evidence needed>

Decision: proceed to Phase 2 (Architectural planning: current/target architecture + call-site audit)? (yes/no)
<!-- arch_skill:block:phase1_kickoff:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
