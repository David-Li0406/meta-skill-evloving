---
description: "12) Maestro autopilot: run tests, fix flow issues, re-run."
argument-hint: "<Slang is fine: 'run onboarding on android', 'start from the top on both sims'>"
---
# /prompts:maestro-autopilot — $ARGUMENTS
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Goal: autonomously run Maestro QA automation (end-to-end UI flows) and make it stable. Prefer centralized, reusable subflows and avoid one-off fixes.

$ARGUMENTS is intentionally slang. Treat it like a human request and infer what to run.

Autonomy policy:
- Do NOT “check in” after each run. Execute end-to-end until COMPLETE or a real stop condition.
- Fix obvious blockers (build/compile/automation drift) instead of stopping.
- Stop only for real product bugs that require a product decision.

Interpretation (slang → intent):
1) Platform intent:
   - If $ARGUMENTS mentions android/emulator/pixel → run Android only.
   - If $ARGUMENTS mentions ios/iphone/simulator → run iOS only.
   - If $ARGUMENTS mentions both/both sims/both platforms → run both (iOS then Android).
   - Otherwise default to both (iOS then Android).
2) Breadth intent:
   - If $ARGUMENTS includes “start from the top”, “from the top”, “smoke”, “baseline”, “get working”, “get green”, “stabilize” → run the canonical baseline/smoke suite.
   - Otherwise treat it as a focused feature request (onboarding, auth, puzzles, etc).
3) Feature query (focused mode only):
   - Extract the feature phrase from $ARGUMENTS (e.g. “onboarding”, “sign in”, “puzzles home”).
   - Use it to find matching Maestro flows and run the most relevant set (prefer a folder when one exists).

Target resolution (most specific wins):
1) If $ARGUMENTS contains an explicit target (highest confidence):
   - A Make target (e.g. “make test-smoke”, “make maestro-onboarding-android”) OR
   - A Maestro flow path / folder (e.g. “maestro/onboarding/”, “maestro/foo.yaml”)
   → use it exactly.
2) Else if breadth intent is baseline/smoke:
   - Prefer the repo’s canonical smoke entrypoint:
     - `make test-smoke` if present, otherwise the closest equivalent (Makefile/script/docs).
3) Else (focused mode):
   - Find matching Maestro flows by searching the repo (path/filename/content) for the feature query.
   - Prefer a single folder run if it exists (e.g. `maestro/onboarding/`).
   - Otherwise run the minimal set of flows that covers the happy path end-to-end (don’t run 50 unrelated flows just because they match a word).
   - If nothing matches, fall back to baseline smoke and note that no focused flows were found.

Execution (end-to-end):
1) Preflight quickly:
   - Ensure the requested simulator/emulator is booted and the app is installed/launched as needed by the repo’s Maestro harness.
   - Prefer existing repo scripts/targets for boot/build/install.
2) Run on requested platform(s) (iOS, Android, or both):
   - Run the resolved target(s).
   - If it fails, classify and act:
     - Build/compile/harness failure: fix it (small, local, high-confidence), then re-run.
     - Automation instability: fix it systemically (shared subflows, dedupe selectors/patterns, remove drift), then re-run.
     - Product bug:
       - If it’s an obvious bug with a safe, in-scope fix → note it, fix it, re-run.
       - If it needs a product decision → STOP and report (with the smallest crisp repro + where the flow failed).
   - Repeat until it passes on that platform, then move to the next requested platform.
3) Keep a short work log and note fixes in the relevant doc if one exists.
4) Commit only files you changed; ignore other dirty files. Push if requested.

OUTPUT FORMAT (console only; Amir-style):
Only print this when STOPPING (complete/blocked) or when a real product decision is required.

<1 line north star reminder>
<1 line punchline (pass/fail + what’s blocking)>
- Ran: <platform(s)> — <what suite/feature>
- Result: <pass|fail> (per platform)
- Fixes made: <high-level>
- Issues/Risks: <none|what’s still broken>
- Next: <only if blocked: decision needed or smallest unblock step>
- Pointers: <targets/flow paths or worklog if one exists>
