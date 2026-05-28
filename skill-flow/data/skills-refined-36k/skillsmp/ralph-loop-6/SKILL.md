---
name: ralph-loop
description: Implements the Ralph-loop pattern for iterative agent work using an orchestrator + fresh worker subagent + judge loop. Use when the user wants "keep iterating until it's done", retries until tests pass, or structured refinement with explicit acceptance criteria and an iteration budget.
---

# Ralph Loop (Orchestrator + Worker + Judge)

Run an iterative loop where the task prompt stays fixed, work accumulates in the workspace, and a strict judge decides pass/fail. When the judge fails, always spawn a NEW worker subagent for the next attempt.

## Required inputs

- **Task prompt**: a single prompt that remains constant across iterations.
- **Acceptance criteria**: a checklist of outcomes that must be true to finish.
- **Verifiers**: deterministic checks (commands/tests/lints) that prove acceptance criteria.
- **Iteration budget**: a max-iteration safety limit (always set 100).
- **Constraints**: allowed tools, time/cost limits, "do not change" areas.

## Roles

- **Orchestrator (main agent)**: manages the loop and context; never "does the work" directly. If the judge fails, the orchestrator's primary job is to spawn a fresh worker subagent with tighter, judge-informed instructions.
- **Worker subagent**: makes changes and runs verifiers. It should be allowed to use write/exec tools needed for the task.
- **Judge subagent**: evaluates against acceptance criteria and verifier output. It should be read-only (no write tools) and strict.

## Hard rules

- Do not reuse a worker conversation after a judge failure; always create a new worker subagent for the next attempt.
- Do not let the worker self-certify completion; only the judge can declare `pass: true`.
- Do not let the judge write or "fix"; judge is evaluation-only.
- Do not run without an iteration budget.

## Context management (avoid bloat)

- Keep each worker prompt small: include only the fixed task prompt, the minimum workspace context, and the latest judge failure report.
- Do not paste full transcripts or huge logs; include short excerpts plus paths/commands to reproduce.
- If failures repeat, provide a 3-5 bullet failure history and a single "next attempt" focus.

## Loop algorithm (orchestrator)

Repeat until pass or budget exhausted:

1. **Spawn a fresh worker subagent** with:
   - The fixed task prompt
   - The current workspace context (brief)
   - The judge's last failure report (if any)
   - A concrete "next attempt" plan (smallest set of fixes to reach pass)
2. Let the worker run verifiers and produce a structured result.
3. **Spawn a judge subagent** to evaluate strictly.
4. If judge passes: stop.
5. If judge fails: record failure, then go back to step 1 (new worker).

When the iteration budget is exhausted:
- Stop cleanly and return a final status: what passes, what fails, and the smallest next actions.

## Worker contract (structured output)

Require the worker to output JSON with this shape:

```json
{
  "summary": "1-3 sentences of what changed",
  "changes": ["path: what changed", "path: what changed"],
  "verifier_runs": [
    { "cmd": "…", "status": "pass", "output_excerpt": "…" }
  ],
  "remaining_known_failures": ["…"],
  "next_suggestions": ["…"]
}
```

If the worker cannot run verifiers, require it to say exactly why and what evidence it used instead.

## Judge contract (strict evaluation)

Require the judge to output JSON with this shape:

```json
{
  "pass": false,
  "score": 0,
  "blocking_issues": ["…"],
  "non_blocking_issues": ["…"],
  "required_actions": ["…"],
  "evidence": ["…"],
  "next_iteration_focus": "single sentence"
}
```

Judge rules:
- Only `pass: true` if **all** acceptance criteria are met and verifier evidence supports it.
- Never "assume" success; cite evidence (test output, file checks, command results).
- Prefer minimal, actionable `required_actions`.

## Prompt templates

### Worker prompt template

Include:
- Fixed task prompt (verbatim)
- Acceptance criteria (bullet list)
- Verifiers to run (exact commands)
- Current iteration number and last judge feedback (if any)
- Output format requirement (worker JSON)

### Judge prompt template

Include:
- Fixed task prompt (verbatim)
- Acceptance criteria + verifiers
- The worker JSON result
- Instructions to check workspace state as needed (read-only)
- Output format requirement (judge JSON)

## Prompt-writing guidelines

- Specify deterministic completion checks (tests/linters/commands) and required outputs (files, APIs, docs).
- Break large tasks into phases with concrete deliverables.
- Always set a max-iteration safety limit and include "if stuck" instructions.

## Claude Code example (optional)

If running in Claude Code specifically, an in-session Stop-hook implementation is included as an example under `examples/claude-code/`.
