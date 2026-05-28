---
name: "skill-transcoder"
description: "Convert skills between Codex, Claude Code, and OpenCode by normalizing SKILL.md frontmatter and copying resources. Use when you need a skill to work across agents or install it into each agent's skill directory."
---

# Skill Transcoder

## Overview

Normalize skill frontmatter to a target agent profile and copy the skill directory so it can be loaded by Codex, Claude Code, or OpenCode.

## Quick start

```bash
python3 scripts/skill_transcode.py \
  --src /path/to/skill \
  --target universal \
  --out /tmp/skill-universal

python3 scripts/skill_transcode.py \
  --src /path/to/skill \
  --target claude \
  --install
```

## Workflow

1. Identify the source skill directory that contains `SKILL.md`.
2. Choose the target profile: `codex`, `claude`, `opencode`, or `universal`.
3. Run `scripts/skill_transcode.py` with `--out` (staging) or `--install` (copy into the agent's default directory).
4. Verify the target skill folder exists and restart the agent if needed.

## Script reference

### `scripts/skill_transcode.py`

Usage:

```bash
skill_transcode.py \
  --src <skill-dir> \
  --target <codex|claude|opencode|universal> \
  [--out <dir>] \
  [--install] \
  [--install-dir <dir>] \
  [--overwrite] \
  [--normalize-name] \
  [--truncate-description]
```

Notes:
- Keep only `name` and `description` by default for maximum compatibility.
- Use `--normalize-name` to force the name into a lowercase, hyphenated form.
- Use `--truncate-description` to fit agent description length limits.
- Use `--install` to copy into the agent's default user-scope skill directory.

## References

- See `references/agent-paths.md` for default locations and profile constraints.
