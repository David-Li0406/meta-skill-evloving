# AutoSkill Reflection CLI Command Catalog

Run these commands from `scripts/`. For conceptual details see
`references/README.md`. For interpretation guidance see `SKILL.md`. For an
end-to-end example see `references/examples.md`.

## Quick start

```bash
python3 reflect_sessions.py --output -
```

```bash
python3 reflect_sessions.py --output-style human --output -
```

Note: ensure your shell command timeout is at least 120000 ms (2 minutes) so runs are not cut off.

## Common recipes

List projects after filtering:

```bash
python3 reflect_sessions.py --list-projects
```

Filter by project:

```bash
python3 reflect_sessions.py --project ExampleProject --output -
```

Filter by date range (inclusive):

```bash
python3 reflect_sessions.py --since 2026-01-01 --until 2026-01-12 --output -
```

Filter by session id (repeatable):

```bash
python3 reflect_sessions.py --session-id <uuid> --output -
```

Comma-separated session ids:

```bash
python3 reflect_sessions.py --session-ids <uuid1,uuid2> --output -
```

Include the most recent session (skipped by default):

```bash
python3 reflect_sessions.py --include-most-recent --output -
```

Include extra metadata:

```bash
python3 reflect_sessions.py --output-style json_extra_metadata --output -
```

Refresh cache automatically when stale:

```bash
python3 reflect_sessions.py --refresh-mode auto --output -
```

Run sequentially:

```bash
python3 reflect_sessions.py --sequential --output -
```

Use a custom prompt file:

```bash
python3 reflect_sessions.py --prompt-file /path/to/prompt.txt --output -
```

Use a preset prompt:

```bash
python3 reflect_sessions.py --prompt-preset summary --output -
```

Preset names: `reflection`, `summary`, `bloat`, `incomplete`, `decisions`, `next_steps`.

Use inline prompt text:

```bash
python3 reflect_sessions.py --prompt-text "Summarize the session in 5 bullets." --output -
```

## reflect_sessions.py flags (reference)

**Session roots**

- `--sessions-root <path>`: Root directory containing Codex session JSONL files.
- `--cache-dir <path>`: Cache directory (default: `sessions_root/reflection_cache`).

**Selection**

- `--project <label>`: Only include sessions matching this project label.
- `--since <date|datetime>`: Only include sessions on/after this ISO date.
- `--until <date|datetime>`: Only include sessions on/before this ISO date.
- `--session-id <uuid>`: Include a specific session id (repeatable).
- `--session-ids <uuid1,uuid2>`: Comma-separated session ids to include.
- `--limit <n>`: Limit to the most recent N sessions after filtering.
- `--include-most-recent`: Include the most recent session (skipped by default).

Notes:

- When explicit session ids are provided, project/date filters and `--limit`
  are ignored.
- The default skip of the most recent session happens before applying `--limit`.

**Output**

- `--output <path|->`: Output JSON path or `-` for stdout.
- `--output-style human|json|json_extra_metadata`: Output format.
- `--list-projects`: List available projects after filtering and exit.

**Reflection behavior**

- `--prefix <text>`: Prefix for the duplicated session's first user message.
- `--prompt-preset <name>`: Built-in prompt preset (default: reflection).
- `--prompt-text <text>`: Inline prompt text (mutually exclusive with preset/file).
- `--prompt-file <path>`: Override the reflection prompt file.
- `--refresh-mode never|auto|always`: Cache reuse policy.
- `--sequential`: Run reflections sequentially.

**Codex execution**

- `--codex-sandbox <mode>`: Sandbox mode passed to Codex.
- `--codex-approval <policy>`: Approval policy passed to Codex.
- `--codex-timeout-seconds <n>`: Timeout per reflection (seconds).
- `--codex-path <path>`: Override Codex binary path.

**Debugging**

- `--debug`: Print debug information to stderr.

## cleanup_reflection_copies.py

Dry run (report only):

```bash
python3 cleanup_reflection_copies.py --dry-run --output -
```

Flags:

- `--sessions-root <path>`: Root directory containing Codex session JSONL files.
- `--prefix <text>`: Prefix marking reflection copies.
- `--output <path|->`: Output path or `-` for stdout.
- `--dry-run`: List reflection copies without deleting them.

## parse_traces.py (optional)

Generate a `trace_examples.md` file from session logs (writes to the current
working directory by default):

```bash
python3 parse_traces.py --sessions-root ~/.codex/sessions --limit 3
```

Or provide explicit session files:

```bash
python3 parse_traces.py ~/.codex/sessions/2026/01/12/rollout-*.jsonl
```
