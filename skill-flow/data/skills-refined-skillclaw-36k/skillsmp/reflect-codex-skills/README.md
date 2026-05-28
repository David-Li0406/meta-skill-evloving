# Codex Reflect Skill

Generate reflections for past Codex session histories using the AutoSkill Reflection CLI.
This skill helps surface repeated patterns, friction, and potential skill ideas from
prior Codex conversations.

## What’s included

- `SKILL.md`: guidance on when and how to use the skill
- `scripts/`: the CLI tools (`reflect_sessions.py` and helpers)
- `references/`: command catalog, usage notes, and examples

## Requirements

- Python 3.11+
- A local Codex session archive in `~/.codex/sessions`
- The `codex` binary available on your PATH (or pass `--codex-path`)

## Quick start

Run commands from `scripts/`:

```bash
python3 reflect_sessions.py --output -
```

Human-readable output:

```bash
python3 reflect_sessions.py --output-style human --output -
```

Project filter example:

```bash
python3 reflect_sessions.py --project ExampleProject --output -
```

Preset prompt example:

```bash
python3 reflect_sessions.py --prompt-preset summary --output -
```

Inline prompt example:

```bash
python3 reflect_sessions.py --prompt-text "Summarize in 5 bullets." --output -
```

## Prompt presets

Available presets:

- `reflection` (default): full reflection on repetition, friction, and skill ideas
- `summary`: concise summary of goals, actions, outputs, and decisions
- `bloat`: bloat/dead ends/cleanup opportunities introduced during the session
- `incomplete`: open loops and unfinished tasks
- `decisions`: key decisions, alternatives, and rationale
- `next_steps`: concrete follow-up actions, tests, and validations

Use `--prompt-preset <name>`, `--prompt-text "<prompt>"`, or `--prompt-file /path/to/prompt.md`.

## Cache behavior

Reflections are cached per session *and* prompt. Cache files live here:

```
~/.codex/sessions/reflection_cache/<session_id>-<prompt_key>.json
```

`prompt_key` is a short hash derived from the prompt label (preset path or
`inline:<hash>` for inline prompts). Legacy cache files without the prompt key
are still read for the default `reflection` preset.

## Notes on privacy

The CLI reads local session histories from `~/.codex/sessions`. Reflections may contain
sensitive content from those sessions. Review outputs before sharing them publicly.

## License

MIT. See `LICENSE`.
