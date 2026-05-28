---
description: "07a) DevX (agent-assisted): CLI-output mocks + artifacts with subagent discovery."
argument-hint: "<Freeform guidance. Include a docs/<...>.md path anywhere to pin the plan doc (optional).>"
---
# /prompts:arch-devx-agent — $ARGUMENTS
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
1) Subagent: Existing Commands + Entry Points
   - Task: find existing repo commands/targets/scripts relevant to this plan (make/just/npm/flutter/etc.).
   - Output format (bullets only):
     - <command> — <what it does> — <where defined (path)>
2) Subagent: Artifacts + Debugging Shortcuts
   - Task: find existing artifact/log conventions and the fastest debug/inspection shortcuts already used in-repo.
   - Output format (bullets only):
     - Artifact: <path pattern> — <what it contains>
     - Shortcut: <command> — <why useful>
3) Subagent: DX Acceptance Checks
   - Task: propose cheap, signal-only DX acceptance checks using existing commands (no new harness).
   - Output format (bullets only):
     - <command> — <what it proves> — <expected artifacts>

Documentation-only (planning):
- This prompt is for documentation and planning only. DO NOT modify code.
- You may inspect existing scripts/harnesses to propose idiomatic DX commands and artifact paths.
- If DX suggests code changes, describe them in DOC_PATH (do not implement them here).
- Do not commit/push unless explicitly requested in $ARGUMENTS.

Stop-the-line gates (must pass before writing DevX targets)
- North Star Gate: falsifiable + verifiable, bounded + coherent.
- UX Scope Gate: explicit UX in-scope/out-of-scope (what users see changes vs does not change).
If either gate does not pass, STOP and ask the user to fix/confirm in the doc before proceeding.
Add a Dev Experience section to DOC_PATH.
Capture developer-facing outputs and commands:
- CLI/console mockups (startup + summary)
- Structured output schemas and canonical artifact paths
- Debugging/inspection shortcuts
- DX acceptance tests (cheap, signal-only; avoid overbuilt harnesses)
Update the section in place if it already exists.
Write/update the section into DOC_PATH (anti-fragile: do NOT assume section numbers match the template).
Placement rule (in order):
1) If a block marker exists, replace the content inside it:
   - `<!-- arch_skill:block:devx:start -->` … `<!-- arch_skill:block:devx:end -->`
2) Else insert after the most relevant existing testing section (heading match, case-insensitive):
   - "Test Strategy", "Testing", "Verification"
3) Else insert near the end of the doc, before the Decision Log (if present), otherwise append.
Numbering rule:
- If the doc uses numbered headings, preserve numbering; do not renumber the rest of the document.
Do not paste the full block to the console.

DOCUMENT INSERT FORMAT:
<!-- arch_skill:block:devx:start -->
# Dev Experience (DX) Targets
## CLI / Console UX (if relevant)
- Principles:
- Canonical commands:
  - `<command>`
- Startup banner mock (exact):
```text
<CLI startup banner mockup>
```
- Per-epoch / summary mock (exact):
```text
<CLI per-epoch or summary block mockup>
```

## Structured outputs + artifacts
- Canonical output paths:
  - `runs/<run_id>/...`
- Schema expectations:
```json
{
  "field": "example"
}
```

## Debugging / inspection shortcuts
- `rg -n "<pattern>" <log_path>`
- `jq -r "<filter>" <json_path>`

## DX acceptance tests
- Principle: keep these fast and runnable; prefer smoke-level checks over verification bureaucracy. Do not block the plan on flaky device/sim steps.
- `<command>` — expected artifacts + pass/fail signal
<!-- arch_skill:block:devx:end -->

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
