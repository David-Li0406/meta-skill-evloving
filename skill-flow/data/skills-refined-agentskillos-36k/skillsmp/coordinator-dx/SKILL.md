---
name: coordinator-dx
description: Coordinator playbook for running multi‑repo, multi‑VM work in parallel without relying on humans copy/pasting long checklists.
---

# coordinator-dx

Coordinator playbook for running multi‑repo, multi‑VM work in parallel without relying on humans copy/pasting long checklists.

Key conventions:
- Each VM/agent sets `AGENT_NAME=<vm>-<tool>` (e.g. `macmini-codex`, `epyc6-claude-code`, `homedesktop-wsl-gemini`)
- For in-repo coordination, `thread_id` should equal the repo’s local Beads issue id (no cross-repo renames).
- Always start a session with `bash scripts/cli/dx_doctor.sh` and follow the warnings (soft, advisory).

Recommended coordinator flow:
1. Assign work by repo (prime-radiant-ai / affordabot / llm-common / agent-skills).
2. Require agents to report:
   - `git status --porcelain`
   - `git branch --show-current`
   - output of `bash scripts/cli/dx_doctor.sh`
3. Prevent collisions:
   - one repo per VM by default
   - prefer small PRs
4. Enforce “automation not checklists”:
   - if a step is repeated, codify it in `dx_doctor.sh` or shared skills.

