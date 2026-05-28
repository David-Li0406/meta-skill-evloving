---
name: codex-review
description: Use this skill for iterative code reviews using the Codex CLI, refining code until the review is satisfactory.
---

# Codex Iterative Review

## Workflow
Determine the scale of changes → Codex review based on scale → Claude Code modifications → Re-review until `ok: true`.

```
[Scale Determination] → small:  diff ──────────────────→ [Modification Loop]
                   → medium: arch → diff ───────────→ [Modification Loop]
                   → large:  arch → diff in parallel → cross-check → [Modification Loop]
```

- **Codex**: Acts as a read-only reviewer.
- **Claude Code**: Responsible for making modifications.

## Scale Determination

```bash
git diff <diff_range> --stat
git diff <diff_range> --name-status --find-renames
```

| Scale  | Criteria                     | Strategy                          |
|--------|------------------------------|-----------------------------------|
| small  | ≤3 files, ≤100 lines         | diff                              |
| medium | 4-10 files, 100-500 lines    | arch → diff                       |
| large  | >10 files, >500 lines        | arch → diff in parallel → cross-check |

When `diff_range` is omitted, HEAD is used, targeting uncommitted changes in the working tree (staged/unstaged distinction is ignored).

**For large scale:**
- Parallel: 3-5 sub-agents, each responsible for specific files.
- Split: Maximum of 5 files/300 lines per call, split by directory (cross-cutting concerns detected during cross-check).
- Integration is handled by the main (Claude Code).

## Modification Loop

If `ok: false`, iterate up to `max_iters`:
1. Analyze `issues` → Create modification plan.
2. Claude Code makes modifications (only minimal diffs, unresolved issues remain).
3. Run tests/linter (if possible).
4. Request re-review from Codex.

Stopping conditions:
`ok: true` / `max_iters` reached / two consecutive test failures.

## Codex Execution

```bash
codex exec --sandbox read-only "<PROMPT>"
```

- Pass the final prompt (including schema) to PROMPT.
- Claude Code explicitly states the paths of major related files.
- Wait for review completion (mandatory): Do not proceed to the next step while `codex exec` is running (no starting new tasks or guessing interruptions).
  - Regular checks: Log every 60 seconds for a maximum of 20 times, only log elapsed time and do not perform additional work.
  - If 20 checks are reached without completion, treat it as a "timeout" and follow error rules.
  - Since long periods without output may occur, consider running `codex exec` in the background and treating process survival checks as polls.

## Codex Output Schema

Codex should output only one JSON object. Claude Code appends the following schema and field descriptions at the end of the prompt.

```json
{
  "ok": true,
  "phase": "arch|diff|cross-check",
  "summary": "Summary of the review",
  "issues": [
    {
      "severity": "blocking",
      "category": "security",
      "file": "src/auth.py",
      "lines": "42-45",
      "problem": "Description of the problem",
      "recommendation": "Suggested fix"
    }
  ],
  "notes_for_next_review": "Notes"
}
```

Field descriptions:
- `ok`: true if there are no blocking issues, false if one or more exist.
- `severity`: two levels
  - blocking: must fix. If any exist, `ok: false`.
  - advisory: recommendations/warnings. Can output with `ok: true`, noted in the report.
- `category`: correctness / security / performance / maintainability / testing / style.
- `notes_for_next_review`: Notes left by Codex. Claude Code includes these in the prompt for re-review.

## Prompt Templates

### arch

```
Review the architectural consistency of the following changes. Output only one JSON object. Refer to the schema at the end.

This is executed as a review gate. If there is even one blocking issue, set `ok: false` and provide feedback for modifications and re-review.

diff_range: {diff_range}
Focus: dependencies, responsibility separation, breaking changes, security design.
Previous notes: {notes_for_next_review}
```

### diff

```
Review the following changes. Output only one JSON object. Refer to the schema at the end.

This is executed as a review gate. If there is even one blocking issue, set `ok: false` and provide feedback for modifications and re-review.

diff_range: {diff_range}
Target: {target_files}
Focus: {review_focus}
Previous notes: {notes_for_next_review}
```

### cross-check

```
Integrate parallel review results and conduct a cross-check. Output only one JSON object. Refer to the schema at the end.

This is executed as a review gate. If there are any cross-cutting blocking issues (e.g., interface inconsistencies, authorization leaks, API compatibility breaks), set `ok: false`.

Overall stat: {stat_output}
Group results: {group_jsons}
Focus: interface consistency, error handling consistency, authorization, API compatibility, test coverage.
```

## Common Error Rules

In case of Codex exec failures (timeouts, API failures, etc.):
1. Retry once (for timeouts, split the number of files in half).
2. On second failure → Skip the relevant phase and record the reason in the report.
3. If arch is skipped, continue with diff only; if diff is skipped, mark those files as "unreviewed" in the report.

## Parameters

| Argument      | Default | Description                          |
|---------------|---------|--------------------------------------|
| max_iters     | 5       | Maximum iterations (up to 5)        |
| review_focus   | -       | Focus areas for review               |
| diff_range    | HEAD    | Comparison range                     |
| parallelism   | 3       | Degree of parallelism for large scale (up to 5) |

## Example Completion Report

```
## Codex Review Results
- Scale: large (12 files, 620 lines)
- Parallel: 3 sub-agents, 4 groups
- Iterations: 2/3 / Status: ✅ ok

### Modification History
- auth.py: Added authorization checks

### Advisory (for reference)
- main.py: Function names are somewhat verbose, refactoring recommended

### Unreviewed (only in case of errors)
- utils/legacy.py: Codex timeout, manual review recommended

### Unresolved (if any)
- main.py: Content, risks, recommended actions
```