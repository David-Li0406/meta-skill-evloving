---
description: "13) Maestro rerun last: re-run most recent failed flow."
argument-hint: <optional guidance>
---
# /prompts:maestro-rerun-last — $ARGUMENTS
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Execution rule: do not block on unrelated dirty files in git; ignore unrecognized changes. If committing, stage only files you touched (or as instructed).
Do not preface with a plan or restate these instructions. Begin work immediately. If a tool-call preamble is required by system policy, keep it to a single terse line with no step list. Console output must ONLY use the specified format; no extra narrative.

Find the most recent Maestro run under logs/maestro/**. If it failed, re-run the same target with the same platform/device settings. If no failure is found, run the most recent target once.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline (did it pass this time?)>
- Ran: <flow/target>
- Result: <pass|fail>
- If failed: <short reason + where>
- Next: <smallest unblock step>
