---
name: agent-manager-skill
description: Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling.
---

# Agent Manager Skill

## When to use

Use this skill when you need to:

- run multiple local CLI agents in parallel (separate tmux sessions)
- start/stop agents and tail their logs
- assign tasks to agents and monitor output
- schedule recurring agent work (cron)

## Prerequisites

Install `agent-manager-skill` in your workspace:

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## Common commands

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start <agent_id>
python3 agent-manager/scripts/main.py monitor <agent_id> --follow
python3 agent-manager/scripts/main.py assign <agent_id> <<'EOF'
Follow <workflow_file> Workflow
EOF
```

## Notes

- Requires `tmux` and `python3`.
- Agents are configured under an `agents/` directory (see the repo for examples).