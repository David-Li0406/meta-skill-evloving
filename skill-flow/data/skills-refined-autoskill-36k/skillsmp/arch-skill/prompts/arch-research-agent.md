---
description: "03a) Research grounding (agent-assisted): external + internal anchors with subagents."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-research-agent — $ARGUMENTS
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

Subagents (agent-assisted research; use when repo surface is large)
- Use subagents when grounding requires lots of repo-wide searching (patterns, fixtures, call-site clusters).
- Do NOT use subagents for small/simple docs; do the work directly.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or run destructive commands.
  - Shared environment: avoid commands that generate/overwrite artifacts; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents with “are you done?”; wait for completion, then integrate.
- Main agent writes DOC_PATH and owns all synthesis/decisions.

Spawn subagents as needed (disjoint scopes):
1) Subagent: Internal Ground Truth + Patterns (read-only)
   - Task: find authoritative behavior anchors + existing reusable patterns relevant to DOC_PATH.
   - Output format (bullets only):
     - Authoritative anchor: <path> — <what it defines> — <evidence: symbol/test/comment>
     - Reusable pattern: <path> — <pattern name> — <how it maps to this change>
2) Subagent: Fixtures / Examples / Tests Scan (read-only)
   - Task: find fixtures/examples/tests that encode behavior relevant to the change.
   - Output format (bullets only):
     - <path> — <what scenario it encodes> — <why it is authoritative>

Close subagents once their results are captured. If a subagent is mis-scoped, interrupt/redirect sparingly.


Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may read code and run read-only searches to ground the doc.
- If you discover code changes we likely need, write them into DOC_PATH as plan items with file anchors (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line: North Star Gate (must pass before research grounding)
- Falsifiable + verifiable: the North Star states a concrete claim AND the smallest credible pass/fail signal (prefer existing tests/checks; otherwise minimal instrumentation/log signature; otherwise a short manual checklist). Do NOT invent new harnesses/screenshot frameworks or drift scripts by default.
- Bounded + coherent: the North Star clearly states in-scope + out-of-scope and does not contradict the TL;DR/plan.
If the North Star Gate does not pass, STOP and ask the user to fix/confirm the North Star in the doc before proceeding.

Stop-the-line: UX Scope Gate (must pass before research grounding)
- The doc explicitly states UX in-scope and UX out-of-scope: what screens/states/behaviors change vs do NOT change.
- UX scope is coherent with the North Star and does not silently expand.
If the UX Scope Gate does not pass, STOP and ask the user to fix/confirm scope in the doc before proceeding.

You are doing research. Good research looks like:
- Internal ground truth (code as spec): concrete file paths + the behaviors/contracts they define (what is authoritative and why).
- Existing patterns to reuse: concrete file paths + a short name for the pattern (so we don't reinvent).
- External anchors (optional): papers/systems/prior art with explicit adopt/reject and why it applies here (no cargo cult).
- Open questions framed as evidence: what information would settle the question; do not leave vague TODOs.

Write/update a Research Grounding section in DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:research_grounding:start -->` … `<!-- arch_skill:block:research_grounding:end -->`
2) Else, if the doc already has a section whose heading contains "Research" or "Grounding" or "Anchors" (case-insensitive), update it in place.
3) Else insert a new top-level "Research Grounding" section:
   - Prefer inserting after the Problem Statement / "What exists today" section if present,
   - otherwise after TL;DR,
   - otherwise after YAML front matter,
   - otherwise at the top.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:research_grounding:start -->
# Research Grounding (external + internal “ground truth”)
## External anchors (papers, systems, prior art)
- <source> — <adopt/reject + what exactly> — <why it applies>

## Internal ground truth (code as spec)
- Authoritative behavior anchors (do not reinvent):
  - `<path>` — <what it defines / guarantees>
- Existing patterns to reuse:
  - `<path>` — <pattern name> — <how we reuse it>

## Open questions (evidence-based)
- <question> — <what evidence would settle it>
<!-- arch_skill:block:research_grounding:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
