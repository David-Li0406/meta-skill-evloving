---
description: "11a) Implement (agent-assisted): ship the plan end-to-end using subagents for code + tests to keep main context lean."
argument-hint: "<Optional: paste symptoms/constraints. Optional: include a docs/<...>.md path anywhere to pin the plan doc.>"
---
# /prompts:arch-implement-agent — $ARGUMENTS
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

Subagents (agent-assisted implementation; keep main context lean)
- Use subagents to keep implementation detail + test logs out of the main agent context.
- Shared environment rule: only ONE code-writing subagent at a time.
- Parallel subagents are allowed ONLY for read-only work (e.g., call-site scanning), and must not write files.
- Subagent ground rules:
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - No commits: subagents must NOT commit/push; main agent handles final git operations.
  - No log spam: subagents must NOT paste long logs/diffs to the console; write details into WORKLOG_PATH and return a short summary.
  - Do not spam/poll subagents with “are you done?”; wait for completion, then integrate.
  - Close subagents once their results are captured. If a subagent is mis-scoped, interrupt/redirect sparingly.

Agent-assisted execution loop (main agent):
- Read DOC_PATH and identify the next phase in order.
- For each phase: spawn a Phase Implementer subagent with a tight scope, wait, review summary, merge/adjust docs, then close.
- Continue phase-by-phase until the plan is complete (unless blocked by a real stop-the-line invariant or missing external decision).

Spawn subagents as needed (disjoint scopes):
1) Subagent: Phase Implementer (write-capable; ONE phase only)
   - Task: implement exactly one phase from DOC_PATH (Phase <n> (<descriptor>)). Do not start the next phase.
   - Constraints:
     - Touch only the code required for that phase + any required compilation fallout.
     - Keep SSOT real (no parallel paths). Perform required deletes/cleanup for the phase.
     - Run the smallest relevant check for this phase (per DOC_PATH) and record results.
     - Update DOC_PATH + WORKLOG_PATH to reflect what was done and what was proven.
     - Do NOT ask the user technical questions; search the repo and decide.
     - Do NOT paste logs/diffs; write details to WORKLOG_PATH and return summary only.
   - Output format (summary only):
     Summary:
     - Phase: Phase <n> (<descriptor>)
     - Touched files:
       - <path>
     - Key changes:
       - <bullet>
     - Checks run:
       - <command> — <result>
     - Docs/worklog updated: <yes/no>
     - Status: <done|blocked>
     - Blockers (if any):
       - <evidence anchor>

2) Subagent: Test Runner (optional; log-heavy; no code edits)
   - Task: run the final test sweep specified in DOC_PATH (and only that), summarize results, and write them into WORKLOG_PATH.
   - Constraints:
     - Do NOT modify code.
     - Do NOT paste full logs; only summary + failing command + 3-5 key lines if needed.
   - Output format (summary only):
     Summary:
     - Commands run:
       - <command> — <result>
     - Failures (if any):
       - <short> — <evidence anchor>
     - WORKLOG_PATH updated: <yes/no>


Stop-the-line gates (must pass before executing the plan)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the plan doc before proceeding.

Read DOC_PATH fully. Treat the doc as the authoritative spec and checklist.

Warn-first preflight (recommended planning pass sequence; do NOT hard-block)
- Recommended flow before phase plan and implementation:
  1) Deep dive (pass 1): current/target architecture + call-site audit
  2) External research grounding (best practices where applicable)
  3) Deep dive (pass 2): integrate external research into target architecture + call-site audit
- Before executing any code changes, check DOC_PATH for the planning passes marker:
  - `<!-- arch_skill:block:planning_passes:start -->` … `<!-- arch_skill:block:planning_passes:end -->`
  - If present: use it to determine which passes are done.
  - If missing: infer from doc contents (deep dive blocks / external research block), but treat deep dive pass 2 as unknown.
- If the recommended sequence is incomplete or unknown, DO NOT stop. Proceed, but:
  - Print a clear warning in the Summary (missing items + recommended next prompts).
  - Continue to respect North Star + UX scope; do not “wing it.”

Implementation discipline (optimize for steady execution, not ceremony):
- Refresh discipline (prevent drift):
  - At the start of each phase (and at least every ~30–60 minutes of work), re-read the North Star, UX scope, and stop-the-line invariants in the plan doc.
  - Before starting any new phase, explicitly confirm you are executing the phases in order (no skipping), and that the next work item supports the North Star.
  - If you discover you are out of order or the plan is missing a prerequisite step, STOP and update the plan doc sequencing (Decision Log entry) before continuing.
- Implement SYSTEMATICALLY: follow the phased plan (or the plan’s checklist) in order.
- Test as you go: after each meaningful chunk (at least once per phase), gather the smallest relevant evidence (existing checks like tests/typecheck/lint/build/QA automation, targeted instrumentation/log signature, or a quick manual check) and record what it proved.
- Common-sense verification (avoid verification bureaucracy):
  - Prefer existing checks over building bespoke harnesses or drift scripts; add only minimal tests/instrumentation that pay off.
  - Do not block the entire plan on flaky sim/video/screenshot steps; if human visual verification is required, add a short manual checklist + clear log/trace signatures and keep moving (record pending QA explicitly in the doc/worklog).
- Keep the doc current: update DOC_PATH as you go to reflect real progress, phase completion, and any plan drift you discover.
  - If the plan drifts, update the plan doc and add a Decision Log entry (append-only).
  - If a phase is complete, mark it complete in the doc (do not leave the doc ambiguous).
- Avoid blinders: if you introduce/upgrade a centralized pattern (SSOT/primitives/contracts), scan for other call sites that should adopt it to prevent drift.
  - If it's clearly in-scope, do it (no question).
  - If it expands UX scope or meaningfully expands work, do NOT expand scope:
    - Record it as a follow-up candidate (with file paths/symbols + why) and continue.
    - Only stop+ask if the plan’s scope/North Star is internally contradictory (i.e., required work is declared out-of-scope).

Worklog (lightweight, required):
- Derive WORKLOG_PATH from DOC_PATH using the same directory and suffix: `<DOC_BASENAME>_WORKLOG.md`.
- If WORKLOG_PATH is missing, create it and add cross-links:
  - Plan doc should reference WORKLOG_PATH near the top (add if missing).
  - Worklog should link back to DOC_PATH at the top.
- When creating WORKLOG_PATH, initialize it with a minimal header + first entry (keep it short; avoid writing a second plan doc).
- Append short progress updates there as you go (at least once per phase).

Preferred worklog insert format:
## Phase <n> (<phase name>) Progress Update
- Work completed:
  - <item>
- Tests run + results:
  - <command> — <result>
- Issues / deviations:
  - <issue>
- Next steps:
  - <step>

Stop conditions (do not plow ahead):
- If a stop-the-line invariant fails: stop, fix immediately, and prove it with a test or evidence.
- If a real blocker prevents progress: stop and report with evidence anchors (file paths, logs, failing test).

Finish criteria:
- All phases / checklist items are complete and the North Star is satisfied.
- The doc reflects reality: no “done” claims without evidence.

Finalization (after implementation is complete):
1) Run a final test sweep appropriate to the plan (tests listed in the doc + any standard repo checks).
2) Get a code review from opus/gemini (via read-only reviewer subagents; keep main context lean):
   - Explicit question: “Is this complete and idiomatic relative to the plan?”
   - Reviewer subagent rules:
     - Read-only: MUST NOT modify files.
     - No questions: MUST answer from DOC_PATH + repo evidence only.
     - No recursion: MUST NOT spawn other subagents.
     - Output must be short, actionable bullets with evidence anchors (file paths/symbols).
   - Provide ALL context they need (plan doc + key code paths + diffs).
   - Integrate feedback you agree with; do not scope creep.
3) Commit and push AFTER review (unless the user explicitly requested a different sequence).
   - Stage only files you touched; ignore other dirty files.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
