---
name: agent-mail-guide
description: Guide for installing and using MCP Agent Mail across heterogeneous agent tools/VMs.
---

# agent-mail-guide

Guide for installing and using MCP Agent Mail across heterogeneous agent tools/VMs.

High-level:
- Run the Agent Mail server on the coordinator VM (reachable via Tailscale/MagicDNS).
- Distribute the bearer token via **1Password** or local env injection (not via prompts, git, or logs).
- Configure MCP clients (Claude Code / Codex CLI / Gemini CLI / Antigravity) to point to `http://<coordinator>:8765/mcp/` with `Authorization: Bearer <token>`.

Identity convention:
- Set `AGENT_NAME=<vm>-<tool>` on each VM. Examples:
  - `macmini-codex`
  - `macmini-claude-code`
  - `epyc6-claude-code`
  - `homedesktop-wsl-gemini`

Operational rules:
- Never paste bearer tokens into shared threads or PRs.
- Use Beads issue ids as thread ids inside a repo.
- Cross-repo work: link threads by referencing the other repo’s issue id in the body (don’t rename ids).

