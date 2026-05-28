---
description: "00a) Ramp-up (agent-assisted): parallel read-only orientation on plan doc + code anchors before acting."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-ramp-up-agent — $ARGUMENTS
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

Read-only ramp-up:
- This prompt is for orientation only. DO NOT modify code or docs.
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Subagents (agent-assisted ramp-up; parallel read-only scans when beneficial)
- Use subagents when DOC_PATH is large or references lots of code so that doing everything inline would blow up context.
- Do NOT use subagents for small/simple docs; do the work directly.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or create artifacts.
  - Shared environment: avoid commands that generate/overwrite outputs; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents with “are you done?”; wait for completion, then integrate.
- Main agent produces the final synthesis and readiness call.

Spawn subagents as needed (disjoint scopes; read-only):
1) Subagent: Doc Extractor (read-only)
   - Task: read DOC_PATH and extract the minimum high-signal orientation:
     - North Star claim + UX scope
     - Current phase / what's done / what's in progress (as written)
     - References / ground-truth anchors (paths, symbols, commands)
     - Any explicit stop-the-line invariants
   - Output format (bullets only):
     - North Star:
       - <bullet>
     - Scope:
       - In scope: <bullets>
       - Out of scope: <bullets>
     - Phase / status:
       - <bullet>
     - Ground truth anchors:
       - <path> — <what it defines>
     - Open questions (as written):
       - <question> (or "None")

2) Subagent: Code Anchor Spot-Check (read-only)
   - Task: use the doc’s referenced paths/symbols to spot-check reality:
     - confirm anchors exist
     - identify the 2–4 primary control paths relevant to the plan
     - flag any obvious doc-vs-code mismatches (facts only; no edits)
   - Output format (bullets only):
     - Primary flows (as-is):
       - <flow> — <evidence anchors>
     - Anchor sanity:
       - <path> — <exists|missing> — <note>
     - Doc-vs-code mismatches (if any):
       - <mismatch> — <evidence anchor>

3) Subagent: Repo Commands Scout (read-only; optional)
   - Task: find the minimal commands to build/test/run relevant to this plan by reading repo docs (AGENTS.md, QUICKSTART.md, Makefile, scripts).
   - Output format (bullets only):
     - Setup:
       - <command> — <why>
     - Fast checks:
       - <command> — <pass/fail signal>
     - Plan-adjacent dev loops:
       - <command> — <why>

Main-agent procedure:
1) Resolve DOC_PATH.
2) Derive WORKLOG_PATH (same rule as implementation prompts):
   - `<DOC_BASENAME>_WORKLOG.md` next to DOC_PATH (if it exists).
3) Decide whether to spawn subagents:
   - If DOC_PATH is short and has few anchors, do everything directly.
   - Otherwise, spawn Doc Extractor + Code Anchor Spot-Check (and Repo Commands Scout if the repo commands are unclear).
4) Integrate results into a single human-readable readiness summary:
   - Do not drown the user in details; keep to the required output format.
   - Prefer evidence anchors over speculation.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
