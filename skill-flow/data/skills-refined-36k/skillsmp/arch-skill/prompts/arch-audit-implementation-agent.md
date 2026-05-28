---
description: "Implementation audit (agent-assisted): prove plan compliance + completeness with subagent scans, then opus+gemini second opinions."
argument-hint: "<Paste anything. Include docs/<...>.md to pin the plan doc (optional).>"
---
# /prompts:arch-audit-implementation-agent — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

# North Star (authoritative)
Running this audit should stop us from “missing parts” of the implementation. After it runs:
- the plan doc reflects reality (no false “complete”),
- any missing implementation is explicitly listed with evidence anchors (file paths/symbols/tests),
- phases that were marked complete but aren’t truly done are reopened with concrete missing work,
- and we have two independent second opinions (opus + gemini) on completeness + idiomatic fit.

$ARGUMENTS is freeform steering. Treat it as intent + constraints + any relevant context.

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

Subagents (agent-assisted; parallel read-only sweeps when beneficial)
- Use subagents to keep grep-heavy scanning and long outputs out of the main agent context.
- Spawn these subagents in parallel only when they are read-only and disjoint.
- Subagent ground rules:
  - Read-only: subagents MUST NOT modify files or create artifacts.
  - Shared environment: avoid commands that generate/overwrite outputs; prefer pure read/search.
  - No questions: subagents must answer from repo/doc evidence only.
  - No recursion: subagents must NOT spawn other subagents.
  - Output must match the exact format requested (no extra narrative).
  - Do not spam/poll subagents; wait for completion, then integrate.
  - Close subagents once their results are captured.

Spawn subagents as needed (disjoint scopes; read-only):
1) Subagent: Call-Site Completeness Scan
   - Task: verify call-site audit items and find missed migrations (search for old APIs/patterns; enumerate misses).
   - Output format (nested lists; no tables):
     - Missing item:
       - Evidence anchors:
         - <path:line>
       - Plan expects:
         - <expected>
       - Code reality:
         - <actual>
       - Fix:
         - <fix>
2) Subagent: SSOT + Cleanup / Delete Verification
   - Task: verify SSOT is enforced (no parallel writers/readers) and delete/cleanup expectations are met.
   - Output format (nested lists; no tables):
     - Finding:
       - Evidence anchors:
         - <path:line>
       - Why it violates SSOT/cleanup:
         - <reason>
       - Fix:
         - <fix>
3) Subagent: Guardrails / Evidence Scan
   - Task: verify claimed tests/checks/instrumentation exist and are wired to the real failure site (ignore manual QA).
   - Output format (bullets only):
     - <claim in plan> — <exists yes/no> — <evidence anchor> — <note>

Hard rules:
- You MUST update DOC_PATH.
- You MUST output a friendly human-readable report to the console.
- Code is ground truth: validate “complete” claims by reading code and searching the repo.
- This audit is about whether the CODE was built right.
  - Do NOT reopen phases or mark NOT COMPLETE solely because manual QA/screenshot evidence wasn’t captured.
  - If manual QA is pending, record it as a non-blocking follow-up (it may be important, but it is not “missing code”).
- Avoid verification bureaucracy: evidence should be common-sense and fast (existing tests/checks, instrumentation/log signatures). Manual QA can be listed as follow-up, but it is not a gating criterion for “code complete”.
- Audit-only (no implementation):
  - DO NOT modify code in this prompt. Only update DOC_PATH with audit findings.
  - Do not “fix it while you’re here”; capture code gaps with evidence anchors instead.
  - Do not commit/push unless explicitly requested in $ARGUMENTS.

What you are auditing for (highest bar):
1) ABSOLUTE completeness:
   - If the plan says something is done, it is actually shipped in code (not hand-wavy).
2) Architecture compliance:
   - SSOT is real (no parallel sources of truth).
   - Boundaries/contracts match the plan.
   - Old paths are deleted or provably unreachable if the plan requires it.
3) FULL idiomatic fit:
   - Aligns to existing repo patterns (no unnecessary new abstractions).
4) CALL SITES AUDITED:
   - Every call site that should be migrated is migrated, and you verify by searching for misses.

Audit procedure (do this in order):
1) Read DOC_PATH fully.
2) Extract the plan’s authoritative anchors (from wherever they live in the doc):
   - Target architecture contracts/APIs (names + paths)
   - Call-site audit / change inventory (table or equivalent)
   - Phase plan + which phases are marked complete (any “Status: complete”, checkmarks, “done”, etc.)
   - Delete list / cleanup expectations (if present)
   - Any “Definition of done” evidence expectations, but split them into:
     - Code/verifiable evidence (tests, invariants, automation, assertions)
     - Manual evidence (manual QA, screenshots) — track as non-blocking follow-up
3) Validate completeness against code:
   - For each call-site audit item: verify the code has the required change (path + symbol usage).
   - Search for old APIs/old patterns/old paths to find misses (do not trust the table blindly).
   - Verify SSOT enforcement: look for lingering writers/readers of the old source of truth.
   - Verify deletions/cleanup: if the plan says “remove X”, confirm X is removed OR no longer referenced.
   - Verify code-evidence: if the plan claims a test/automation/invariant/assertion proves the North Star, confirm it exists and is wired to the real failure site.
   - Do NOT treat missing manual QA evidence as “missing implementation”.
4) Determine phase truth:
   - If a phase is marked complete but CODE work is missing → REOPEN it.
   - If a phase is code-complete but only manual QA evidence is missing → do NOT reopen; instead record “Manual QA pending (non-blocking)” as follow-up.
   - Always refer to phases as `Phase <n> (<what it does>)` (use the phase heading text; if missing, infer from that phase’s Goal/Work bullets).
5) Second opinions (required):
   - Get two independent reviews (via read-only reviewer subagents; do not bloat main context):
     - Opus (anthropic/claude-opus-4.5)
     - Gemini (gemini-3-pro-preview)
   - Reviewer subagent rules:
     - Read-only: MUST NOT modify files.
     - No questions: MUST answer from DOC_PATH + repo evidence only.
     - No recursion: MUST NOT spawn other subagents.
     - Output must be short, actionable bullets with evidence anchors (file paths/symbols).
   - Ask them: “Is the implementation complete and idiomatic relative to DOC_PATH? What’s missing? Where does code drift from plan? Any SSOT/contract violations?”
   - Provide them enough context to answer (DOC_PATH + top gaps + key file anchors). Do not be vague.
   - Record their feedback in the doc, even if you disagree (label: accepted/rejected).

DOC UPDATES (anti-fragile; do NOT assume section numbers):
A) Insert/replace an audit block near the top:
Placement rule (in order):
1) If `<!-- arch_skill:block:implementation_audit:start -->` exists: replace inside it.
2) Else insert after TL;DR if present, otherwise after YAML front matter, otherwise at top.

<!-- arch_skill:block:implementation_audit:start -->
# Implementation Audit (authoritative)
Date: <YYYY-MM-DD>
Verdict (code): <COMPLETE|NOT COMPLETE>
Manual QA: <pending|complete|n/a> (non-blocking)

## Code blockers (why code isn’t done)
- <bullets only about missing/incorrect code>

## Reopened phases (false-complete fixes)
- Phase <n> (<what it does>) — reopened because:
  - <missing items>

## Missing items (code gaps; evidence-anchored; no tables)
- <area>
  - Evidence anchors:
    - <path:line>
  - Plan expects:
    - <expected>
  - Code reality:
    - <actual>
  - Fix:
    - <fix>

## Non-blocking follow-ups (manual QA / screenshots / human verification)
- <follow-up item>

## External second opinions
- Opus: <received|pending>
  - Key points:
    - <bullet>
  - Disposition: <accepted|rejected> — <why>
- Gemini: <received|pending>
  - Key points:
    - <bullet>
  - Disposition: <accepted|rejected> — <why>
<!-- arch_skill:block:implementation_audit:end -->

B) Reopen phases in-place (only when needed):
- Find the phase section in the doc.
- If CODE work is missing:
  - Add/replace a status line directly under the phase heading:
    - `Status: REOPENED (audit found missing code work)`
  - Add a short `Missing (code):` list with concrete items (file paths/symbols/tests/deletes).
- If code is complete but manual QA is pending:
  - Do NOT reopen.
  - Add (or update) a short `Manual QA (non-blocking):` note with the smallest checklist needed.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
