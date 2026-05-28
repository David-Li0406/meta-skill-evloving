# Silvan Best Practices Reference

## Product principles

- Progressive disclosure: show essentials first, details on demand.
- Fail forward: every error includes next steps and recovery guidance.
- No silent operations: successful commands confirm what happened.
- Scriptable by default: `--json` everywhere with stable schemas.
- Semantic colors: consistent meaning across all commands and UI.
- Operator-grade: resumable, deterministic, and safe by default.

## CLI output conventions

### Semantic colors

Use consistent meanings for colors across all output:

- Green: success, completed, good state
- Yellow: warning, attention needed
- Red: error, failure, blocked
- Cyan: running, in progress
- Blue: info, links, references
- Dim: secondary info (timestamps, paths, ids)
- Bold: section headers

### Formatting patterns

- Section headers should be consistent and scannable.
- Key-value blocks should align for easy reading.
- Lists should be numbered when ordered, bulleted when unordered.
- Always end with a "Next steps" block when a user action is logical.
- Avoid emojis and decorative symbols unless they are standardized.

Example layout:

```
  Section Title
  ------------------------------------------------------------
  Key       Value
  Another   Value

  Steps:
    1. First step
    2. Second step

  Next steps:
    silvan task start "Your task"
    silvan run status <runId>
```

### TTY vs non-TTY

- TTY output may use color and spinners.
- Non-TTY output must be plain text and parseable.
- `--json` output must never mix with human text.

## JSON and verbosity

- Every command supports `--json` with a consistent response envelope.
- Errors in JSON mode must also be JSON (no mixed output).
- `--quiet` suppresses non-error output.
- `--verbose` adds debug context (timings, API calls, config paths).
- `--trace` includes raw payloads when safe.

Suggested JSON envelope:

```
{
  "success": true,
  "command": "run.list",
  "data": { ... },
  "nextSteps": ["..."]
}
```

```
{
  "success": false,
  "command": "task.start",
  "error": {
    "code": "ISSUE_NOT_FOUND",
    "message": "GitHub issue #999 not found",
    "details": { ... },
    "suggestions": ["..."],
    "docsUrl": "..."
  }
}
```

## Error messaging

- Provide a concise error headline.
- Explain likely causes when it is helpful.
- Provide 1-3 actionable next steps.
- Link to relevant help topics or docs.
- Suggest `silvan doctor` for environment or auth issues.

## Success confirmations and next steps

- Every successful command prints a confirmation line.
- Include the key identifiers (path, run id, PR URL).
- End with "Next steps" if there is a logical follow-on action.

## Onboarding and help

- First-run experience should be welcoming and prescriptive.
- `silvan quickstart` should demonstrate the full workflow safely.
- `silvan init` should auto-detect repo settings and avoid destructive changes.
- `silvan help <topic>` should be concise and example-driven.

## Run lifecycle and operator UI

- Surface run phase, step, and gating status clearly.
- Provide summaries for CI and review state.
- Prefer attention queues for blocked/stuck runs.
- Ensure UI lists scale with pagination and audit summaries.

## Safety and resumability

- Destructive actions require explicit `--apply` and/or `--dangerous`.
- Do not repeat destructive steps on resume.
- Respect `--yes` and `--force` semantics.

## Testing and docs

- Update tests when output format or schemas change.
- Add or adjust snapshot tests for CLI output as needed.
- Update docs or help text when behavior changes.
