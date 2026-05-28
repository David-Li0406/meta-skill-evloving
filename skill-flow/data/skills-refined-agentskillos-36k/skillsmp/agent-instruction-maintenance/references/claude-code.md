# Claude Opus Guidance (Claude Code)

## Scope
- Project-wide guidance lives in `CLAUDE.md`.
- Subagents live in `~/.claude/agents/*.md`.
- Slash commands live in `~/.claude/commands/*.md`.
- Skills can live in `~/.claude/skills` with SKILL.md format.

## Key updates from the current docs
- Built-in subagents include Explore, Plan, and general-purpose.
- Custom slash commands are now unified with skills; `.claude/commands/` still works but skills are preferred.
- Subagents can preload skills, set permission modes, and define hooks.
- Hooks can run at PreToolUse/PostToolUse/Stop and session-level events.

## Frontmatter checklist (agents)
- Required: `name`, `description`, `tools`, `model`, `color`.
- Keep `description` task-focused with trigger phrases.
- Keep tool lists minimal and relevant.

## Authoring best practices
- Prefer CLI-first workflows; do not assume MCP servers exist.
- Include explicit "when to ask" guidance for missing context.
- Use concise, actionable steps; avoid long narratives.
- Keep instructions aligned with repository conventions.

## Hooks overview (deterministic automation)
- Hooks run shell commands at lifecycle events (e.g., PreToolUse, PostToolUse, Stop, SessionStart).
- Use hooks to enforce policy (formatting, logging, file protection) instead of relying on prompt text.
- Configure via `/hooks` or `~/.claude/settings.json`.
- Hooks run with your credentials; review for security.

## Safety and consistency
- Avoid secrets and tokens in prompts.
- Respect repository guardrails and operational policies.
- Keep output formats stable to reduce reviewer churn.

## References
- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Hooks guide: https://code.claude.com/docs/en/hooks-guide
