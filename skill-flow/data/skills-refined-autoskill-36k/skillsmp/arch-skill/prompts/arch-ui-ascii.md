---
description: "05) UI ASCII: current-target mockups (if UI)."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-ui-ascii — $ARGUMENTS
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

Stop-the-line gates (must pass before adding UI ASCII)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.
If the change touches UI/UX, add ASCII mockups for current and target states in DOC_PATH.
Keep them contract-level, not illustrative.
Write/update the ASCII blocks into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If marker blocks exist, replace content inside them:
   - `<!-- arch_skill:block:ui_ascii_current:start -->` … `<!-- arch_skill:block:ui_ascii_current:end -->`
   - `<!-- arch_skill:block:ui_ascii_target:start -->` … `<!-- arch_skill:block:ui_ascii_target:end -->`
2) Else, if the doc has "Current Architecture"/"As-is" and "Target Architecture"/"To-be" sections, add a `## UI surfaces (ASCII)` subsection under each (or update it if it exists).
3) Else, append a standalone `# UI Surfaces (ASCII)` section near the architecture content with both blocks.
Do not paste the full blocks to the console.

DOCUMENT INSERT FORMAT (use wherever it fits best per the rules above):
<!-- arch_skill:block:ui_ascii_current:start -->
Current UI ASCII:
```ascii
<ASCII mockups for current UI states>
```
<!-- arch_skill:block:ui_ascii_current:end -->

<!-- arch_skill:block:ui_ascii_target:start -->
Target UI ASCII:
```ascii
<ASCII mockups for target UI states>
```
<!-- arch_skill:block:ui_ascii_target:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
