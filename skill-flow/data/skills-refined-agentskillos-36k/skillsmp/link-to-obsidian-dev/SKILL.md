---
name: link-to-obsidian-dev
description: Verify, configure, and manage the link-to-obsidian redirect service (systemd). Use when checking service status/logs, editing config, rebuilding the binary, or restarting the service.
---

# Link-to-Obsidian (service)

## Overview

Operate the link-to-obsidian redirect service on the devbox (systemd unit `link-to-obsidian`).

## Status / logs

```bash
systemctl status link-to-obsidian --no-pager
journalctl -u link-to-obsidian -f
```

## Config

- Env file: `/etc/link-to-obsidian/link-to-obsidian.env`
- Override path: `LTO_CONFIG`
- Common keys: `LTO_TAILSCALE_IP`, `LTO_TAILSCALE_DNS`, `LTO_VAULT_NAME`, `LTO_SAMPLE_FILE`, `PORT`

## Restart

```bash
sudo systemctl restart link-to-obsidian
```

## Build / install binary

```bash
cd /data/projects/link-to-obsidian
sudo go build -o /usr/local/bin/link-to-obsidian .
```

## Tests

```bash
go test -cover ./...
```

## Source / docs

- Repo: `/data/projects/link-to-obsidian`
- Reference: `README.md`, `spec.md`
