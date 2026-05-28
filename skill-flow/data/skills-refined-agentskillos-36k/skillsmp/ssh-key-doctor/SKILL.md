---
name: ssh-key-doctor
description: |
  Fast, deterministic SSH health check for canonical VMs (no hangs, no secrets).
  Warn-only by default; strict mode is opt-in.
tags: [dx, ssh, verification]
allowed-tools:
  - Bash(ssh-key-doctor/check.sh:*)
---

# SSH Key Doctor

Checks local SSH setup and (optionally) remote reachability to canonical VMs.

## Usage

```bash
~/agent-skills/ssh-key-doctor/check.sh --local-only
DX_SSH_DOCTOR_REMOTE=1 ~/agent-skills/ssh-key-doctor/check.sh --remote-only
~/agent-skills/ssh-key-doctor/check.sh --strict
```

## Notes

- Never prints private key material.
- Uses `BatchMode=yes` + short timeouts to avoid hangs.
- GitHub SSH check is opt-in: `--check-github` (skips if `timeout` is unavailable).
