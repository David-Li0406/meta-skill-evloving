# Agent paths and profile constraints

## Codex

- User scope: `~/.codex/skills/<skill-name>/SKILL.md`
- Repo scope: `.codex/skills/<skill-name>/SKILL.md`
- Required frontmatter: `name`, `description`
- Limits: `name` <= 100 chars, `description` <= 500 chars, both single-line
- Extra keys: ignored by Codex

## Claude Code

- Personal scope: `~/.claude/skills/<skill-name>/SKILL.md`
- Project scope: `.claude/skills/<skill-name>/SKILL.md`
- Nested discovery: also discovers `.claude/skills/` under subdirectories
- Frontmatter: optional, with `name` (<= 64 chars, lowercase letters/numbers/hyphens) and `description` recommended
- Additional fields: invocation controls, allowed tools, subagent config, hooks, etc.

## OpenCode

- Global scope: `~/.config/opencode/skills/<skill-name>/SKILL.md`
- Project scope: `.opencode/skills/<skill-name>/SKILL.md`
- Compatibility: also scans `.claude/skills/<skill-name>/SKILL.md` and `~/.claude/skills/<skill-name>/SKILL.md`
- Frontmatter: `name`, `description` required; optional `license`, `compatibility`, `metadata`
- Limits: `name` 1-64 chars with regex `^[a-z0-9]+(-[a-z0-9]+)*$`, `description` 1-1024 chars
