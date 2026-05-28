---
name: control-plane-guide
description: Guide for the fort control plane - secure inter-host communication system. Use when adding capabilities to hosts, writing handlers, understanding the GC protocol, or debugging control plane issues. Triggers on questions about fort.host.capabilities, fort.host.needs, the fort CLI, handler scripts, or inter-host calls.
---

# Fort Control Plane Guide

The fort control plane enables secure inter-host communication. Hosts expose **capabilities** (endpoints) that other hosts call via signed HTTP requests.

## Quick Reference

**Client (calling a capability):**
```bash
fort <host> <capability> [request-json]  # request-json defaults to '{}'
```

Examples:
```bash
fort drhorrible status                    # Simple status check
fort joker journal '{"unit": "nginx"}'    # Pass JSON for params
```

**Provider (exposing a capability):**
```nix
fort.host.capabilities.my-capability = {
  handler = ./handlers/my-capability;  # Script handling requests
  needsGC = false;                     # Enable garbage collection
  ttl = 0;                             # GC time-to-live (seconds)
  description = "What this does";
};
```

**Consumer (depending on a capability):**
```nix
fort.host.needs.my-capability.my-id = {
  providers = ["hostname"];            # Host(s) providing this
  request = { key = "value"; };        # Request payload
  store = "/var/lib/myapp/response";   # Where to store response
  restart = ["myapp.service"];         # Services to restart on change
};
```

## Key Files

| Path | Purpose |
|------|---------|
| `common/fort/control-plane.nix` | Nix module: options and config generation |
| `pkgs/fort/` | Client CLI (Bash) |
| `pkgs/fort-provider/` | Server (Go FastCGI) |
| `/etc/fort/` | Runtime config on hosts |
| `/var/lib/fort/` | GC handles and state |

## Standard Capabilities

All hosts expose these:

| Capability | Returns |
|------------|---------|
| `status` | Hostname, uptime, failed units, deploy info |
| `manifest` | Apps, aspects, roles, exposed services |
| `needs` | Declared needs (for GC enumeration) |

## Authentication & RBAC

- Requests signed with SSH keys (`ssh-keygen -Y sign`)
- RBAC computed at eval time from cluster topology
- Only hosts declaring `fort.host.needs` for a capability can call it
- Config: `/etc/fort/hosts.json`, `/etc/fort/rbac.json`

## Detailed Documentation

- [capabilities.md](references/capabilities.md) - Adding capabilities to hosts
- [handlers.md](references/handlers.md) - Writing handler scripts
- [gc-protocol.md](references/gc-protocol.md) - Garbage collection system
- [troubleshooting.md](references/troubleshooting.md) - Debugging issues
