---
name: devservers-register-service
description: Register a dev server using the CLI. Use when an agent needs to add/update/remove a service entry (name, cwd, command, env, port, port mode).
---

# Devservers Register Service

## Overview

Register a service via the CLI so it can be managed. Optionally start it if requested.
Rule: Use CLI only. Do not edit config files directly or interact with internal services.

## Workflow

### 1) Gather inputs

Collect:
- `name` (alphanumeric plus `._-`)
- `cwd` (absolute path)
- `command` (shell command, e.g. `pnpm dev`)
- optional `env` entries (`KEY=VALUE`)
- optional `port`
- optional `port mode` (`static`, `detect`, `registry`)

Ask if the user wants the service started immediately.

## 2) Register via CLI

CLI (from anywhere):

```
devservers add \
  --name <name> \
  --cwd <absolute-path> \
  --command "<command>" \
  --port <port> \
  --port-mode <mode> \
  --env KEY=VALUE
```

- `--port`, `--port-mode`, and `--env` are optional.
- Repeat `--env` for multiple vars.

Verify:

```
devservers list
```

Port lookup (when running):

```
devservers status
```

- The status output includes the current port when known (e.g. `service: running (port 3000)`).
- For `detect` or `registry` modes, the port appears once it is discovered/assigned.

### 3) Start service (optional)

Start via CLI:

```
devservers start <name>
```
### 4) Troubleshoot

- If a CLI call fails due to connectivity, ask the user to start the manager and retry.
