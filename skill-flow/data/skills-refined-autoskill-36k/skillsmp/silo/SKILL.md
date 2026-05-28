---
name: silo
description: Guides usage of the silo CLI for isolated Tilt and k3d dev environments. Use when working with silo.toml, silo commands, profile switching, port isolation, or Tilt/k3d bootstrap.
---

# silo

Use this Skill when a project uses `silo.toml` or the user asks about `silo` commands, profiles, port isolation, or k3d/Tilt integration.

## Instructions

1. Prefer bundled docs for authoritative behavior: `silo doc <topic>` (see topics below).
2. Use CLI commands directly; keep changes minimal and aligned with current config:
   - `silo up [name]` starts an instance (k3d optional, Tilt starts).
   - `silo down` stops Tilt; `--delete-cluster` removes k3d; `--clean` removes env/lockfile.
   - `silo env [name]` generates env + lockfile only.
   - `silo profiles` lists profile names.
   - `silo status` reports current instance.
   - `silo version` prints CLI version.
3. Profiles:
   - Resolution order: `--profile` > `SILO_PROFILE` > lockfile > base config.
   - Switching profiles requires `--force`.
4. Hosts and URLs:
   - Prefer `*.localhost` hostnames for cookie isolation (avoid `localhost:PORT`).
5. k3d:
   - If `k3d.registry.enabled = true`, ensure `K3D_REGISTRY_PORT` is defined in `[ports]`.
6. Do not edit `.silo.lock` by hand; rerun `silo up` or `silo down --clean` instead.

## Bundled Docs

Use `silo doc [topic]` (or `--list` / `--json` for discovery):

| Topic | Description |
| --- | --- |
| `config` | silo.toml reference |
| `profiles` | Profile configuration |
| `commands` | CLI command reference |
| `lockfile` | Lockfile format and behavior |
| `interpolation` | Template variables and phases |
| `ports` | Port allocation and validation |
| `hosts` | Hostnames and browser isolation |
| `urls` | URL templates and derived vars |
| `k3d` | k3d cluster integration |
| `hooks` | Lifecycle hooks |
| `logging` | Logging behavior and verbosity |
| `troubleshooting` | Common errors and fixes |
| `tilt` | Tilt integration and expectations |

## Examples

```bash
silo up dev
silo up --profile testnet --force
silo doc profiles
```
