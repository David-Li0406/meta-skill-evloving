# /prompts:north-star-investigation-bootstrap
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

# Arguments: $ARGUMENTS

You are creating or refreshing a "North Star Investigation" document (Commander's Intent) that will drive an optimization effort or root-cause investigation.

This is Phase 1: BOOTSTRAP THE DOC.
- Primary output is documentation.
- Do NOT edit production code in this phase.
- Do NOT run long test suites "just to see."
- You may run minimal read-only commands (ripgrep, reading files, tiny scripts) only when needed to extract ground truth.

Input (steering, may be messy/freeform):
$ARGUMENTS

Operating principles (non-negotiable):
- Math-first when the question is quantitative:
  - Hypotheses must be grounded in back-of-envelope math and/or real data available in the repo.
  - If data is missing, propose the cheapest way to measure it (do not guess).
- Repo is not a black box:
  - If you can answer something by reading code/config/docs, do it. Do not ask the user.
- Questions to the user are allowed ONLY for:
  - product/UX decisions that cannot be derived from repo or SSOT docs,
  - external constraints you truly cannot infer (e.g., unknown API semantics),
  - permission/access blockers.
  Every question must include:
  - full context (what file(s) you checked and what you found),
  - 2 concrete options,
  - your recommendation.
- Ship v1 mindset:
  - We are not writing a scientific paper.
  - Evidence burden is "works and is elegant," not peer review.
  - Avoid busywork: no NASA-grade proof burdens.
- Avoid local maxima:
  - This doc is the controller. It must make the best next move obvious, not just a plausible move.

Task:
1) Determine the target investigation document from $ARGUMENTS.
   - If $ARGUMENTS names a doc path, use it.
   - If it doesn't, infer the best candidate from context.
   - If ambiguous, ask ONCE, offering concrete candidate paths.

2) Create or refresh the doc so it contains the following components.
   - Use whatever headings make sense; do NOT rely on section numbers or template ordering.
   - Keep non-worklog sections concise and stable. Put detailed evidence in the Worklog.

Required components:
- North Star:
  - What "best possible" means here (according to our standards), and what "done" means for v1.
- Scope (user-experience framed):
  - In scope: what changes from the user's POV.
  - Out of scope: what explicitly does NOT change.
- Non-negotiables:
  - Locked assumptions required for comparability.
  - Explicit rule: changing a non-negotiable = new experiment family/version.
- Scoreboard:
  - Metrics (and how computed) that determine success.
- Ground truth anchors:
  - Exact paths/commands/docs that define reality (code locations, configs, datasets, scripts).
- Quant model / sanity checks:
  - Back-of-envelope math, budgets, bounds, expected effect sizes.
  - Explicitly call out what numbers are assumed vs measured.
- Hypotheses (ranked):
  - Each hypothesis must include:
    - math/data rationale,
    - the fastest brutal test (trap / negative proof / oracle / minimal repro),
    - decision rule (pre-committed pass/fail),
    - what evidence would refute it.
- First iteration plan (fast learning plan):
  - 1–3 highest-info-gain "bets," each time-boxed.
  - Each bet has: expected learning outcome + success criteria.
- Worklog (authoritative; details live here):
  - Create a Worklog section with an initial entry capturing:
    - what you read/inspected,
    - what facts were established (with file anchors),
    - initial quant assumptions + why,
    - initial hypotheses and why they're ranked that way,
    - what you will do first in the loop phase.

3) Output to the user (in chat; Amir-style):
- Line 1: 1-line North Star reminder (plain English).
- Line 2: punchline (plain English).
- Then bullets (3-10 bullets max):
  - what you changed in the doc,
  - what we now know / don’t know (high level),
  - the next 1-3 timeboxed bets,
  - "Need from Amir:" only if you truly need a decision.
- IMPORTANT: this "State of the Union" is for print only. Do NOT add it as a doc section or keep rewriting it in the doc.
- Point to the doc path you updated (details live in the doc Worklog).
