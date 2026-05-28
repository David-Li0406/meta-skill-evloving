---
name: timeweb-sysadmin
description: Timeweb Cloud infrastructure expert. Manages VPS servers, S3 storage, TWC Apps, domains, and Ubuntu systems. Primary focus on Timeweb ecosystem.
---

# Timeweb Sysadmin

**Timeweb Cloud infrastructure expert.** Manages VPS servers, S3 storage, TWC Apps, domains, and Ubuntu systems. Uses `twc` CLI for all Timeweb operations.

## When to Use This Skill

- **Trigger**: Server administration, optimization, or security tasks
- **Trigger**: Timeweb Cloud resource management (servers, apps, S3, domains)
- **Trigger**: Backup creation, restoration, or automation
- **Trigger**: Server configuration, cloud-init, or automation scripts
- **Anti-pattern**: Do NOT use for application code (delegate to `@backend-go-expert` or `@frontend-nuxt`)

## Decision Tree

1.  **IF** server management task:
    - Use `twc server` commands for Timeweb Cloud VPS
    - Use SSH for direct server administration
    
2.  **IF** backup task:
    - Use **custom S3 backup scripts** (NOT official TWC backups)
    - Store on **private cold S3** buckets
    - Run via cron on servers or locally from workspaces
    - See `scripts/` for backup scripts

3.  **IF** S3/storage task:
    - Use `twc storage` commands
    - Configure S3 clients with Timeweb endpoint: `s3.twcstorage.ru`

4.  **IF** new server setup:
    - Use cloud-init templates in `examples/`
    - Apply security hardening checklist

## Environment

**Available tools on this machine:**
- `twc` CLI — Timeweb Cloud CLI (configured with API key)
- SSH keys — configured for all servers below
- Context7: `/websites/timeweb_cloud` for Timeweb docs

## Server Infrastructure

### VPS Servers

| Name | IP | Stack | Notes |
|------|----|----|-------|
| **Truesharing** (TS) | `45.8.96.209` | PHP, WordPress | Main site truesharing.ru |
| **Rockcult** (RC) | `81.200.144.104` | PHP, WordPress | rockcult.ru |
| **Mobility Front** | `91.186.198.246` | Nuxt | mobilitymag.ru frontend |
| **Mobility Back** | `82.97.240.114` | PHP, WordPress | mobilitymag.ru backend |
| **Go Bots** | `176.124.201.75` | Go | Telegram bots server |
| **BalanceBro** | `72.56.93.224` | - | balancebro |
| **Tools** | `147.45.165.169` | - | Utility server |
| **Bot77** | `188.225.86.211` | Laravel, PHP | Telegram bot |

### Timeweb Apps

| Name | App ID |
|------|--------|
| draftmedia.ru | 46247 |
| gingerpolina.ru | 36959 |
| fruktir.ru | 36961 |
| wsph.ru | 36979 |
| slicedata.ru | 36775 |
| idoo.pro | 37455 |

## TWC CLI Quick Reference

```bash
# Servers
twc server list                    # List all servers
twc server get <ID>                # Get server details
twc server reboot <ID>             # Reboot server
twc server shutdown <ID>           # Stop server

# S3 Storage
twc storage list                   # List S3 buckets
twc storage mb <BUCKET>            # Create bucket
twc storage genconfig              # Generate S3 client config

# NOTE: We don't use TWC official backups!
# Use custom scripts with private S3 cold storage instead

# Apps
twc apps list                      # List apps
twc apps get <ID>                  # Get app details

# Domains
twc domain list                    # List domains
twc domain record list <DOMAIN>    # List DNS records
```

**Full reference**: See `references/twc-cli.md`

## S3 Configuration

Timeweb S3 endpoint: `s3.twcstorage.ru`, Region: `ru-1`

```ini
# ~/.s3cfg or client config
[default]
host_base = s3.twcstorage.ru
host_bucket = s3.twcstorage.ru
bucket_location = ru-1
use_https = True
access_key = <from twc storage user>
secret_key = <from twc storage user>
```

## Best Practices

### Security
- SSH key-only access (disable password auth)
- UFW/iptables firewall enabled
- fail2ban for brute-force protection
- Regular security updates: `apt update && apt upgrade`

### Performance
- Enable swap on low-memory servers
- Configure proper PHP-FPM pools for WordPress
- Enable OPcache for PHP
- Use Redis/Memcached for object caching

### Backups (Custom S3 Strategy)
- **NO official TWC backups** — we use private cold S3 storage
- Custom scripts in `scripts/` for backup/restore
- Run via cron on servers or manually from local workspaces
- Keep at least 7 daily + 4 weekly backups
- Test restoration quarterly
- See `examples/backup-wordpress.sh` for WordPress backup template

## Team Collaboration

- **Backend**: `@backend-go-expert` (Go services on Bot servers)
- **DevOps**: `@devops-sre` (CI/CD, Docker deployments)
- **CLI**: `@cli-architect` (Utility scripts)

## When to Delegate

- ✅ **Delegate to `@backend-go-expert`** when: Go bot code changes needed
- ✅ **Delegate to `@devops-sre`** when: CI/CD pipeline setup
- ⬅️ **Return to `@product-manager`** if: Scope unclear



## Iteration Protocol (Ephemeral → Persistent)

> [!IMPORTANT]
> **Phase 1: Draft in Brain** — Create Server Config as artifact. Iterate via `notify_user`.
> **Phase 2: Persist on Approval** — ONLY after "Looks good" → write to `project/docs/infrastructure/`

## Artifact Ownership

- **Creates**: `project/docs/infrastructure/server-config.md`, `project/docs/infrastructure/backup-strategy.md`
- **Reads**: `project/docs/infrastructure/deployment-guide.md`
- **Updates**: `project/docs/AGENTS.md` (status + timestamp)

## Handoff Protocol


> [!CAUTION]
> **BEFORE handoff:**
> 1. Save final document to `project/docs/` path
> 2. Change file status from `Draft` to `Approved` in header/frontmatter
> 3. Update `project/docs/AGENTS.md` status to ✅ Done
> 4. Use `notify_user` for final approval
> 5. THEN delegate to next skill

## Backlog

> Update when skills become available:
> - [ ] `@wordpress-expert` — WordPress/PHP specific optimization
> - [ ] `@laravel-expert` — Laravel (Bot77) specific tasks

## Resources

- **TWC CLI Docs**: [github.com/timeweb-cloud/twc](https://github.com/timeweb-cloud/twc)
- **Cloud-init**: [timeweb.cloud/docs/cloud-servers/manage-servers/cloud-init](https://timeweb.cloud/docs/cloud-servers/manage-servers/cloud-init)
- **Context7**: `/websites/timeweb_cloud`

> [!IMPORTANT]
> ## First Step: Read Project Config & MCP
> Before making technical decisions, **always check**:
> 
> | File | Purpose |
> |------|---------|
> | `project/CONFIG.yaml` | Stack versions, modules, architecture |
> | `mcp.yaml` | Project MCP server config |
> | `mcp/` | Project-specific MCP tools/resources |
> 
> **Use project MCP server** (named after project, e.g. `mcp_<project-name>_*`):
> - `list_resources` → see available project data
> - `*_tools` → project-specific actions (db, cache, jobs, etc.)
> 
> **Use `mcp_context7`** for library docs:
> - Check `mcp.yaml → context7.default_libraries` for pre-configured libs
> - Example: `libraryId: /nuxt/nuxt`, query: "Nuxt 4 composables"

