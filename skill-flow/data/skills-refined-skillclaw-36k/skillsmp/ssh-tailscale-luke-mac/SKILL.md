---
name: ssh-tailscale-luke-mac
description: How to connect to Luke's Mac over Tailscale via SSH.
---

# SSH to Luke's Mac via Tailscale

## When to use

Use this when you need terminal access to Luke's Mac (e.g., building or packaging the macOS app).

## Connection details

- Host: 100.67.77.99 (Tailscale IP)
- User: luke
- Key: /home/ubuntu/.ssh/clawdbot_macos_ed25519 (public at /home/ubuntu/.ssh/clawdbot_macos_ed25519.pub)
- Auth: publickey only; password auth is rejected
- Network: Tailscale only; do not use WAN port 22

## Connect

```bash
ssh -i ~/.ssh/clawdbot_macos_ed25519 luke@100.67.77.99
```

## Optional SSH config

Add to `~/.ssh/config` for a short alias:

```ssh-config
Host luke-mac
  HostName 100.67.77.99
  User luke
  IdentityFile ~/.ssh/clawdbot_macos_ed25519
  IdentitiesOnly yes
```

Then:

```bash
ssh luke-mac
```

## Notes

- If SSH fails, confirm Tailscale is up on both ends.
- Sudo on the Mac still requires Luke's password; do not attempt sudo changes remotely.
- If the host key changes, remove/update the old entry in `~/.ssh/known_hosts`.
