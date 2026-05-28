# Codex Skill Guidance (GPT-5.2 Codex)

## Scope
- Codex skills live in `~/.codex/skills/<skill-name>/SKILL.md`.
- The frontmatter `name` and `description` are the only trigger inputs.
- Keep SKILL.md concise; add deeper docs under `references/` and scripts under `scripts/`.

## Related docs
- Skills: https://developers.openai.com/codex/skills
- Custom prompts: https://developers.openai.com/codex/custom-prompts
- AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Rules: https://developers.openai.com/codex/rules

## AGENTS.md discovery (custom instructions)
- Global: `$CODEX_HOME/AGENTS.override.md` or `AGENTS.md` (first non-empty wins).
- Project: walk from repo root to CWD; per directory use `AGENTS.override.md`, then `AGENTS.md`, then configured fallbacks.
- Merge order: root to CWD; later files override earlier guidance by position.
- Size cap: stops at `project_doc_max_bytes` (default 32 KiB).
- Configure fallbacks in `~/.codex/config.toml` via `project_doc_fallback_filenames`.

## Custom prompts (slash commands)
- Stored in `~/.codex/prompts/*.md` and require explicit invocation.
- Frontmatter supports `description` and `argument-hint`.
- Arguments: `$ARGUMENTS`, `$1..$9`, and `KEY=value` placeholders.
- Restart Codex after editing prompt files.

## Skills (agent skills)
- Locations are scoped and override lower precedence:
  - Repo: `$CWD/.codex/skills`, parent repo folder, repo root `.codex/skills`
  - User: `$CODEX_HOME/skills`
  - Admin: `/etc/codex/skills`
  - System: bundled
- Symlinked skills are supported.
- Per-skill enablement via `[[skills.config]]` is experimental.

## Frontmatter checklist
- `name`: lowercase letters/numbers/hyphens only, <=64 chars.
- `description`: single line, <=500 chars, includes when to use + trigger keywords.
- Avoid extra frontmatter keys unless required by Codex.

## Authoring best practices
- Use a clear "When to use it" section with trigger phrases.
- Keep workflow steps short and ordered; avoid long prose.
- Put large examples or detailed formats into `references/`.
- Avoid duplicating info across skills; link to references instead.

## Safety and consistency
- Do not include secrets or tokens in any instruction file.
- Respect project-level guidance (AGENTS.md/CLAUDE.md) when present.
- Avoid tool-specific assumptions that Codex cannot enforce.
