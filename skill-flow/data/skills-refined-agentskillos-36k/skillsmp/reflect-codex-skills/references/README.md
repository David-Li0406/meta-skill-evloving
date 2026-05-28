# AutoSkill Reflection CLI Overview

Generate reflections for Codex session histories, cache them, and
emit grouped output by project (JSON or human-readable).

## How it works

- Scan `~/.codex/sessions/**/rollout-*.jsonl` for session histories.
- Filter sessions by id, project, and time window.
- Duplicate each selected session with a new UUID.
- Prefix the first user message in the duplicate (default: `[SELF-REFLECTION] `).
- Run Codex non-interactively to produce a single-paragraph reflection.
- Parse the reflection from the duplicated session history.
- Delete the duplicated session file after extraction.
- Cache reflections per session for reuse.
- Output grouped results by project (cwd basename), ordered chronologically.

## Inputs and configuration

- **Session roots**: `--sessions-root` and `--cache-dir`.
- **Selection**: `--project`, `--since`, `--until`, `--session-id(s)`, `--limit`.
- **Prompt control**: `--prompt-preset`, `--prompt-text`, `--prompt-file`, and `--prefix`.
- **Execution**: `--sequential` to avoid parallel runs.
- **Codex overrides**: `--codex-sandbox`, `--codex-approval`,
  `--codex-timeout-seconds`, `--codex-path`.

Default prompt file: `scripts/prompts/reflection.md` (preset: `reflection`).
Other built-in presets include `summary`, `bloat`, `incomplete`, `decisions`,
and `next_steps`. Prompt versions are tracked alongside the prompt file
(`scripts/prompts/reflection_version.json` for the default).
Inline prompts are recorded as `inline:<hash>` in `prompt_path` metadata.

See `references/cli.md` for the full command catalog and flag list.

## Output schema (JSON)

The default JSON payload includes:

- `generated_at`: ISO timestamp for the run.
- `sessions_root`: Root directory scanned for session histories.
- `prompt_version`: Current prompt version string.
- `projects`: List of project groups, each with ordered `sessions`.

Each session entry includes:

- `session_id`, `conversation_started_at`, `conversation_updated_at`
- `reflection` (single paragraph)
- `reflection_created_at`
- `cache_status` (`fresh` or `out_of_date`)
- `cache_status_reason`

Use `--output-style human` for a readable summary, or
`--output-style json_extra_metadata` to include cache/prompt/path metadata.
When using `--list-projects`, the JSON output includes `current_project` and
project counts (human output marks the current project with `*`).

## Cache semantics

Cache files live alongside session histories and are keyed by session + prompt:

```
~/.codex/sessions/reflection_cache/<session_id>-<prompt_key>.json
```

`prompt_key` is a short hash derived from the prompt label (preset path or
`inline:<hash>` for inline prompts). Legacy cache files without the prompt key
are still read for the default `reflection` preset.

Refresh modes:

- `never` (default): reuse cache if present.
- `auto`: refresh when cache is out of date.
- `always`: refresh every time.

Prompt changes do not force refreshes; they only appear in cache status reasons
until you opt into `auto` or `always`.

## Codex execution defaults

The CLI runs Codex in read-only mode and with approval set to never, equivalent
to:

```
codex --sandbox read-only --ask-for-approval never exec --skip-git-repo-check resume <SESSION_ID> -
```

If `codex` is not on PATH, pass `--codex-path` or set `CODEX_BIN`.
The CLI also scans VS Code extension bins under `~/.vscode` and
`~/.vscode-insiders` for a bundled `codex` binary.

## Interpretation reminder

Reflections are heuristic summaries. For guardrails on how to interpret and
surface them (non-niche, repeated patterns only), see `SKILL.md`.

## Related references

- `references/cli.md` for usage recipes and flags.
- `references/examples.md` for an ExampleProject example.
