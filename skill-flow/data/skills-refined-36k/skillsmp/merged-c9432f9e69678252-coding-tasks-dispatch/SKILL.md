---
name: coding-tasks-dispatch
description: Use this skill to dispatch coding tasks to OpenCode or Claude Code on Perry workspaces for development work, PR reviews, or any coding task requiring an isolated environment.
---

# Coding Tasks Dispatch

Dispatch coding tasks to isolated Perry workspaces on your tailnet using **OpenCode** and **Claude Code**.

## Rules
- **Always create a task FIRST** — before any dispatch, no exceptions.
- **No hard timeouts** — allow background dispatch, let the agent run.
- **Use IPs** — MagicDNS may not work in containers; use `tailscale status` for IPs.
- **One task per PR** — continue the same session until done.
- **Reuse sessions** — OpenCode keeps context in `~/.opencode/`.
- **Never code directly** — always dispatch to agents.

## Quick Reference

| Action | Command |
|--------|---------|
| List workspaces | `tailscale status | grep -v offline` |
| Create workspace | `perry start <name> --clone git@github.com:user/repo.git` |
| Shell into workspace | `ssh workspace@<name>` |
| Run OpenCode task | `ssh workspace@<name> "cd ~/<projname> && opencode run 'task'"` |
| Run Claude Code | `ssh -t workspace@<name> "cd ~/<projname> && claude 'task'"` |
| Remove workspace | `perry remove <name>` |

## Dispatch Pattern

### 1. Find or Create Workspace
```bash
# List available workspaces
tailscale status | grep -v offline

# Create new one for the task
perry start <workspace-name> --clone git@github.com:user/repo.git
```

### 2. Get Wake Callback Info
```bash
# Get tailnet IP
WAKE_IP=$(tailscale status --self --json | jq -r '.Self.TailscaleIPs[0]')
TOKEN="<your-gateway-token>"
```

### 3. Dispatch Task with Wake Callback
Include wake instruction in the prompt so the agent notifies when done:
```bash
ssh -t workspace@<name> "cd ~/<projname> && opencode run 'Your task here.

When completely finished, notify me by running:
curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Content-Type: application/json\" -H \"Authorization: Bearer ${TOKEN}\" -d \"{\\\"text\\\": \\\"Done: task summary\\\", \\\"mode\\\": \\\"now\\\"}\"
'"
```

### 4. Schedule Follow-up (Always!)
After dispatching, schedule a cron reminder as a backup:
```bash
clawdbot cron add --at +20m --message "Fallback check: <workspace> for <task>. The agent should have woken us by now."
```

## OpenCode Tasks

### One-shot task
```bash
ssh -t workspace@<name> "cd ~/<projname> && opencode run 'Your task here'"
```

### Background task
```bash
# Dispatch with wake callback
ssh workspace@<name> "cd ~/<projname> && nohup opencode run 'Your task.

When done: curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Authorization: Bearer <hooks-token>\" -d \"{\\\"text\\\":\\\"Done: task summary\\\"}\"
' > /tmp/opencode.log 2>&1 &"
```

## Claude Code Tasks

Use Claude Code when you need its specific capabilities.

### Interactive session
```bash
ssh -t workspace@<name> "cd ~/<projname> && claude"
```

### One-shot task
```bash
ssh -t workspace@<name> "cd ~/<projname> && claude 'Your task here'"
```

## PR Reviews

### Single PR Review
```bash
# Create workspace for the review
perry start review-pr-<number> --clone git@github.com:user/repo.git

# Checkout and review
ssh workspace@review-pr-<number> "cd ~/<projname> && gh pr checkout <number>"
ssh -t workspace@review-pr-<number> "cd ~/<projname> && opencode run 'Review this PR for bugs, security issues, and improvements.'"
```

### Batch PR Review
Spin up parallel workspaces for multiple PRs:
```bash
for pr in <list-of-prs>; do
  perry start review-pr-${pr} --clone git@github.com:user/repo.git
  ssh workspace@review-pr-${pr} "cd ~/<projname> && gh pr checkout ${pr}"
  ssh workspace@review-pr-${pr} "cd ~/<projname> && nohup opencode run 'Review PR #${pr}.' > /tmp/review.log 2>&1 &"
done
```

## Troubleshooting
- **Can't reach workspace:** `tailscale status | grep <name>`
- **Commands not found:** Use full paths for commands.
- **Wake callback not firing:** Check the agent's completion and verify IP/token.

This skill provides a structured approach to dispatch coding tasks effectively within Perry workspaces, ensuring efficient task management and follow-up.