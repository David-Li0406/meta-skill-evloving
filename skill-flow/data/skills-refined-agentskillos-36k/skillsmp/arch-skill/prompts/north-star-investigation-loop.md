# /prompts:north-star-investigation-loop
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

# Arguments: $ARGUMENTS

You are executing the North Star Investigation LOOP for an existing investigation doc.

This is Phase 2: ITERATE + LEARN + REFINE.
- You MAY edit code and add temporary instrumentation/traps.
- Optimize for wall-clock time to learn the truth and ship v1.
- We are not writing a scientific paper. We are shipping.

Input (steering, may be messy/freeform):
$ARGUMENTS

Operating principles (non-negotiable):
- Start every loop by re-reading the doc's:
  - North Star
  - Scope
  - Non-negotiables
  - Scoreboard
  Treat these as law.
- Avoid local maxima:
  - Re-check that you're attacking the best lever for the North Star (not the closest lever).
- Math-first when quantitative:
  - Use back-of-envelope math + repo data to rank levers and interpret results.
  - If needed data is missing: add the cheapest measurement, then proceed.
- No reruns:
  - Do NOT rerun the same test/config "hoping for a different result."
  - If a run already exists in the Worklog with the same config/purpose, you must either:
    - change ONE lever,
    - narrow to a smaller repro,
    - add a trap/negative proof,
    - move to the next hypothesis.
- Brutal tests > logging:
  - Prefer traps, negative proofs, toggles, assertions, oracles, minimal repros.
  - Logs are allowed only if they directly disambiguate a hypothesis and are time-boxed.
- Questions to the user:
  - Only for true product decisions or external unknowns.
  - Never ask "repo-answerable" questions.

Core rule for documentation:
- Save ALL details into the Worklog.
- "State of the Union" is for print only (chat output), not for the doc.

Loop protocol (do this in order, every time):
1) Identify the target investigation doc from $ARGUMENTS and open it.
   - If ambiguous, ask ONCE with concrete candidates.

2) Print "State of the Union" (for the human; chat only; Amir-style):
   - Line 1: North Star reminder (1 line, plain English)
   - Line 2: punchline (1 line, plain English)
   - Then bullets (3-10 bullets max):
     - current best belief (high level)
     - biggest uncertainty (1 bullet)
     - next bet (exactly ONE bet) + time budget

3) Choose ONE hypothesis / bet (highest info gain).
   - Write the bet as 1–2 sentences.
   - Pre-commit the decision rule (pass/fail).

4) Design the fastest brutal test.
   - Prefer negative proofs / traps / toggles / oracles / minimal repro.
   - Define what you will measure and exactly what outcome means.

5) Execute the minimum required work:
   - Implement minimal instrumentation or code changes.
   - Run only the smallest test needed to answer the question.
   - Fix obvious compile/runtime issues immediately (do not stop to ask permission for trivial fixes).
   - Keep temporary instrumentation explicitly disposable; remove it when it has served its purpose unless it's clearly valuable as a lightweight guardrail.

6) Update the doc (authoritative) immediately:
   - Append a Worklog entry that includes:
     - timestamp/date
     - the bet/hypothesis attacked
     - what changed (files touched)
     - commands run
     - artifacts produced (logs, output files, screenshots if any)
     - result (raw facts)
     - conclusion (what we believe now, and why)
     - next step recommendation
   - Update hypotheses status/ranking if the result changed what’s plausible.
   - Keep non-worklog sections concise; put details in Worklog.

7) Stop conditions:
   - Stop if the next step requires a product decision; ask ONE well-formed question with context + options + recommendation.
   - Stop if the time budget is hit; print State of the Union + next bet, and ensure Worklog is updated.

Output to the user (in chat; Amir-style):
- Line 1: 1-line North Star reminder.
- Line 2: punchline (what happened / are we unblocked).
- Then bullets (3-10 bullets max):
  - what changed this loop (high level)
  - what we proved (smallest signal)
  - issues/risks (if any)
  - next bet (ONE) + time budget
  - pointers: doc path you updated (details live in the Worklog)
