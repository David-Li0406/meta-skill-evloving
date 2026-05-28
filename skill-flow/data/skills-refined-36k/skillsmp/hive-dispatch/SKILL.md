---
name: hive-dispatch
description: |
  Dispatch Beads tasks to Claude Code on remote VMs via SSH.
  Use when: "dispatch to hive", "run on VM", "assign to runner", "send to host".
tags: [workflow, hive, automation, ssh, vm]
allowed-tools:
  - Bash(ssh:*)
  - Bash(python:*)
  - Bash(bd:*)
  - Read
---

# Hive Dispatch Skill

**Purpose:** Dispatch Beads tasks to Claude Code running on remote VMs via SSH.

## Activation

**Triggers:**
- "dispatch this to hive"
- "run bd-123 on the VM"
- "send to runner"
- "assign to host"

## Quick Start

```bash
# Dispatch a specific task
python ~/.agent/skills/hive-dispatch/dispatch.py bd-xyz

# Dispatch all hive-ready tasks
python ~/.agent/skills/hive-dispatch/dispatch.py --all

# Dry-run (preview commands)
python ~/.agent/skills/hive-dispatch/dispatch.py bd-xyz --dry-run
```

## How It Works

1. **Check Queue**: Reads Beads for in-progress tasks with `hive-ready` label
2. **Find VM**: Checks each VM via SSH `pgrep claude` for availability
3. **Dispatch**: Updates status to `in_progress`, SSHs prompt to VM

## Protection Layers

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| 1 | Beads `count_running() >= MAX` | Queue limit |
| 2 | SSH `pgrep -c claude` | VM busy check |
| 3 | systemd `TasksMax=1` | Kernel-enforced |

## Configuration

Environment variables:
- `HIVE_VMS`: Comma-separated VM hostnames (default: `runner1`)
- `HIVE_MAX_CONCURRENT`: Max simultaneous tasks (default: `2`)
- `HIVE_REPO_PATH`: Repo path on VM (default: `~/affordabot`)

## Preparing Tasks

```bash
# Add hive-ready label
bd update bd-xyz --labels hive-ready

# Dispatch
python ~/.agent/skills/hive-dispatch/dispatch.py bd-xyz
```

## VM Host Requirements

On each VM, install the systemd protection slice:

```bash
mkdir -p ~/.config/systemd/user
cat <<EOF > ~/.config/systemd/user/claude.slice
[Slice]
TasksMax=1
CPUQuota=80%
MemoryMax=8G
EOF
systemctl --user daemon-reload
```

## Version History

- **v2.0.0** (2025-12-31): Complete rewrite
  - Replaced daemon with on-demand dispatch
  - Added 3-layer protection
  - Uses Beads as queue
