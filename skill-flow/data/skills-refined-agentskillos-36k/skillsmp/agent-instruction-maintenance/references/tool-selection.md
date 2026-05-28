# Choosing Commands vs Skills vs Agents

## Default priority (unless the user specifies a tool)
1) **Skills (SKILL.md)**: portable across Codex, Claude, and Copilot. Prefer skills for reusable workflows.
2) **AGENTS.md**: repo or global behavioral guardrails that should always apply.
3) **Tool-specific configs**: only when a feature is unique to a tool or explicitly requested.

## Codex (GPT-5.2 Codex) - default target
- Use **skills** for reusable workflows or domain guidance (SKILL.md + references/scripts).
- Use **custom prompts** for explicit, user-invoked commands that should not auto-trigger.
- Use **AGENTS.md** for repo-scoped behavior and guardrails.
- See: [Codex skills](https://developers.openai.com/codex/skills)
- See: [Codex custom prompts](https://developers.openai.com/codex/custom-prompts)
- See: [Codex agent guides](https://developers.openai.com/codex/guides/agents-md)

## Claude Code (only when requested or needed)
- Use **commands** (`/name`) for explicit, user-invoked actions you want tightly controlled.
- Use **skills** for reusable workflows or reference guidance. Add `disable-model-invocation: true` for manual-only workflows.
- Use **subagents** for isolated context, tool restrictions, or cost control.
- Use **hooks** for deterministic enforcement (formatters, logging, file protection).
- See: [Claude skills](https://code.claude.com/docs/en/skills)
- See: [Claude subagents](https://code.claude.com/docs/en/sub-agents)
- See: [Claude hooks](https://code.claude.com/docs/en/hooks-guide)

## VS Code / Copilot (only when requested or needed)
- Use **Agent Skills** when you want portable skills to show up in the agent UI.
- Use **custom instructions** for always-on style or repo policies.
- Use **agents** (`*.agent.md`) for tool-specific personas or modes.
- See: [Copilot response customization](https://docs.github.com/en/copilot/concepts/prompting/response-customization?tool=vscode)
