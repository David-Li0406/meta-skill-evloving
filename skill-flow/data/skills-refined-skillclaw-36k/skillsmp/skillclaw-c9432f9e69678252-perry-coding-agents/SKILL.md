---
name: perry-coding-agents
description: Use this skill to dispatch coding tasks to OpenCode or Claude Code on Perry workspaces for development work, PR reviews, or any coding task requiring an isolated environment.
---

# Perry Coding Agents

Dispatch coding tasks to isolated Perry workspaces on your tailnet using OpenCode or Claude Code.

## Rules
- **Always create a task first** — before any dispatch, no exceptions.
- **No hard timeouts** — allow background dispatch; let the agent run.
- **Use IPs** — MagicDNS may be broken in containers (`tailscale status` for IPs).
- **One task per PR** — continue the same session until done.
- **Reuse sessions** — OpenCode keeps context in `~/.opencode/`.
- **Never code directly** — always dispatch to agents.

## Quick Reference Commands
| Action | Command |
|--------|---------|
| List workspaces | `tailscale status | grep -v offline` |
| Create workspace | `perry start <name> --clone git@github.com:user/repo.git` |
| Shell into workspace | `ssh workspace@<name>` |
| Run OpenCode task | `ssh workspace@<name> "cd ~/<projname> && /home/workspace/.opencode/bin/opencode run 'task'"` |
| Run Claude Code | `ssh -t workspace@<name> "cd ~/<projname> && /home/workspace/.local/bin/claude 'task'"` |
| Remove workspace | `perry remove <name>` |

## Dispatch Pattern
1. **Find or Create Workspace**
   ```bash
   # List available workspaces
   tailscale status | grep -v offline

   # Create new one for the task
   perry start feat-new-feature --clone git@github.com:user/repo.git
   ```

2. **Get Wake Callback Info**
   ```bash
   # Get tailnet IP
   WAKE_IP=$(tailscale status --self --json | jq -r '.Self.TailscaleIPs[0]')
   TOKEN="<your-gateway-token>"
   ```

3. **Dispatch Task with Wake Callback**
   ```bash
   ssh -t workspace@<name> "cd ~/<projname> && /home/workspace/.opencode/bin/opencode run 'Your task.

   When done: curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Content-Type: application/json\" -H \"Authorization: Bearer ${TOKEN}\" -d \"{\\\"text\\\": \\\"Done: summary\\\", \\\"mode\\\": \\\"now\\\"}\"
   '" &
   ```

## Task Tracking
Create a task before dispatching with: workspace IP, branch, goal, and done criteria. Use the same task until CI is green. Complete with a result summary.

## Example: Full PR Flow
```bash
# 1. Create task
# Track: workspace feat1 (100.109.173.45), branch feat/auth, goal: add auth

# 2. Dispatch (background, no timeout)
ssh -o StrictHostKeyChecking=no workspace@100.109.173.45 "cd ~/perry && /home/workspace/.opencode/bin/opencode run 'Add bearer token auth to all API endpoints. Create PR when done.

When finished: curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Content-Type: application/json\" -H \"Authorization: Bearer <token>\" -d \"{\\\"text\\\": \\\"Done: Auth PR created\\\", \\\"mode\\\": \\\"now\\\"}\"
'" &

# 3. Wake received → check CI
ssh workspace@100.109.173.45 "cd ~/perry && gh pr checks 145"

# 4. CI fails → dispatch follow-up (same task, agent has context)
ssh -o StrictHostKeyChecking=no workspace@100.109.173.45 "cd ~/perry && /home/workspace/.opencode/bin/opencode run 'Follow-up task.'"
```