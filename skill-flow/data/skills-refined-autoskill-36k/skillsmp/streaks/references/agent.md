# Agent Mode

Use `--agent` or `STREAKS_CLI_AGENT=1` for NDJSON output and stable error payloads.

## Recommended pattern

1. `st --agent discover` once at startup (cache result).
2. `st --agent help` or `st --agent help <command>` when uncertain.
3. Run actions (e.g., `st --agent task-list`) and parse the last NDJSON line.
4. Read stderr for a single JSON error object.

## Output contract

- **stdout**: NDJSON objects (one per line).
- **stderr**: NDJSON error objects (single line).
- Errors include `code`, `error_code`, and optional `hint` for usage errors.

## Tips

- Prefer Shortcuts that return a Dictionary for structured output.
- Use `--shortcuts-output public.json` if your shortcut produces JSON.
- If a shortcut returns multiple files, output is aggregated into a JSON array.
