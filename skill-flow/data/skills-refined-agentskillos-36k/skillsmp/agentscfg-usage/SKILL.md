---
name: agentscfg-usage
description: Use when the repo contains .agentscfg and the user asks to add/update agent configuration, skills, MCP, or tool settings. Enforce the agentscfg workspace layout and avoid creating separate/legacy agent config locations.
---

# agentscfg Usage

## Quick rules

- Only apply if `.agentscfg/` exists; if missing, ask whether to run `agentscfg init`.
- Use `.agentscfg/` as the single source of truth; do not create separate agent config folders/files elsewhere.

## Add or update a skill

1. Create/modify `.agentscfg/skills/<skill-name>/SKILL.md` (plus optional `scripts/`, `references/`, `assets/`).
2. Keep the skill concise and task-focused.

## Add or update tool settings

- Preferred: edit `.agentscfg/targets/<tool>/**` (e.g. `claude/`, `opencode/`, `codex/`).
- Legacy single-file mapping (only if needed):
  - `.agentscfg/targets/claude.settings.json`
  - `.agentscfg/targets/opencode.json`
  - `.agentscfg/targets/codex.config.toml`

## Add or update MCP

- Edit `.agentscfg/mcp/mcp.json`.

## After changes

- Suggest `agentscfg plan` / `agentscfg diff` and `agentscfg sync` to apply outputs.
