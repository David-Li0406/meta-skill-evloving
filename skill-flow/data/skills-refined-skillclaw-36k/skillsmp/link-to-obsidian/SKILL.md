---
name: link-to-obsidian
description: Generate shareable http(s) links that redirect into Obsidian via the link-to-obsidian service. Use when sending Obsidian note links in chat apps (Discord/WhatsApp) that can’t open obsidian:// URLs, or when converting obsidian://open links to http(s) format.
---

# Link-to-Obsidian (usage)

## Overview

Generate HTTP links that redirect to `obsidian://open` so they’re clickable in apps that only allow http(s) links.

## Quick start

Format:

```
http://<host>:<port>/open?vault=<VaultName>&file=<Path/Note.md>
```

Example:

```
http://dev.quail-mercat.ts.net:7777/open?vault=Obsidian-Notes&file=0-Inbox/Tasks.md
```

Notes:
- Keep the **entire** query string; only scheme/host/port change from `obsidian://open`.
- Percent-encode the `file=` path the same way Obsidian expects.
- Use the **Tailscale host/IP** (e.g., `dev.quail-mercat.ts.net`) for shareable links.
- **Do not** use `127.0.0.1` unless the link is only for your own browser on the same host.
- Default port is `7777` (unless overridden by config).

## Convert from obsidian://open

Given:

```
obsidian://open?vault=Vault&file=Inbox/Note.md
```

Convert to:

```
http://<host>:<port>/open?vault=Vault&file=Inbox/Note.md
```

## Troubleshooting link format

- If the link doesn’t open, check for bad encoding in `file=` or a missing `vault=`.
- If unsure of host/port, check `/etc/link-to-obsidian/link-to-obsidian.env` (read-only) for `LTO_TAILSCALE_DNS`, `LTO_TAILSCALE_IP`, and `PORT`.
