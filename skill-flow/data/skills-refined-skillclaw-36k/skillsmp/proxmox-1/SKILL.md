---
name: proxmox
description: |
  Proxmox VE sysadmin for home lab infrastructure. Use when triaging services,
  checking container/VM status, viewing logs, managing resources, or debugging
  self-hosted apps. Can discover infrastructure dynamically via SSH.
allowed-tools: Bash, Read
---

# Proxmox Home Lab Manager

Sysadmin skill for managing Proxmox VE home lab infrastructure.

## Connection

```bash
# Proxmox host (requires 2FA - password then OTP)
ssh proxmox

# Synology NAS (see ~/.ssh/config for Host entry)
ssh nas
```

## Discovery Commands

### List All Infrastructure

```bash
# All containers with status, IPs
ssh proxmox "pct list"

# All VMs
ssh proxmox "qm list"

# Detailed resource usage (CPU, memory, disk) for everything
ssh proxmox "pvesh get /cluster/resources --type vm --output-format json" | jq

# Container config (shows IP, mounts, resources)
ssh proxmox "pct config <CTID>"

# VM config
ssh proxmox "qm config <VMID>"
```

### Network Discovery

```bash
# Find container IP
ssh proxmox "pct exec <CTID> -- ip -4 addr show eth0"

# What's listening in a container
ssh proxmox "pct exec <CTID> -- ss -tlnp"

# Host network config
ssh proxmox "cat /etc/network/interfaces"
```

### Storage Discovery

```bash
# Storage pools
ssh proxmox "pvesm status"

# Storage config
ssh proxmox "cat /etc/pve/storage.cfg"

# NFS mounts
ssh proxmox "mount | grep nfs"

# Disk usage
ssh proxmox "df -h"
```

## Container Management

```bash
# Start/stop/restart
ssh proxmox "pct start <CTID>"
ssh proxmox "pct shutdown <CTID>"   # graceful
ssh proxmox "pct stop <CTID>"       # force
ssh proxmox "pct reboot <CTID>"

# Enter container shell
ssh proxmox "pct enter <CTID>"

# Run command in container
ssh proxmox "pct exec <CTID> -- <command>"
```

## VM Management

```bash
ssh proxmox "qm start <VMID>"
ssh proxmox "qm shutdown <VMID>"
ssh proxmox "qm stop <VMID>"        # force
ssh proxmox "qm reboot <VMID>"
ssh proxmox "qm status <VMID>"
```

## Service Debugging

### Find and Check Services

```bash
# List systemd services in container
ssh proxmox "pct exec <CTID> -- systemctl list-units --type=service --state=running"

# Check specific service
ssh proxmox "pct exec <CTID> -- systemctl status <service>"

# Service logs
ssh proxmox "pct exec <CTID> -- journalctl -u <service> -n 100 --no-pager"

# Follow logs live
ssh proxmox "pct exec <CTID> -- journalctl -u <service> -f"

# All recent logs in container
ssh proxmox "pct exec <CTID> -- journalctl -n 100 --no-pager"
```

### Common Service Names

Most containers run a single main service. Discover with:
```bash
ssh proxmox "pct exec <CTID> -- systemctl list-units --type=service --state=running" | grep -v systemd
```

Typical patterns: `jellyfin`, `AdGuardHome`, `caddy`, `sonarr`, `radarr`, `sabnzbd`, `tailscaled`

## Host Health

```bash
# Overview
ssh proxmox "pvesh get /nodes/pve/status"

# Quick health
ssh proxmox "uptime && free -h && df -h /"

# ZFS status
ssh proxmox "zpool status"

# Host logs
ssh proxmox "journalctl -n 100 --no-pager"
```

## Backups

```bash
# Backup job config
ssh proxmox "cat /etc/pve/jobs.cfg"

# List backups in storage
ssh proxmox "pvesm list <storage-name> --content backup"
```

## Troubleshooting

### Container Won't Start

```bash
ssh proxmox "pct config <CTID>"                    # check config
ssh proxmox "df -h"                                 # disk space
ssh proxmox "ls /var/lock/pve-manager/pve-config/" # stale locks
```

### Service Not Responding

```bash
# 1. Container running?
ssh proxmox "pct status <CTID>"

# 2. Service running?
ssh proxmox "pct exec <CTID> -- systemctl status <service>"

# 3. Logs
ssh proxmox "pct exec <CTID> -- journalctl -u <service> -n 100 --no-pager"

# 4. Port listening?
ssh proxmox "pct exec <CTID> -- ss -tlnp"

# 5. Restart
ssh proxmox "pct exec <CTID> -- systemctl restart <service>"
```

### NFS Mount Issues

```bash
ssh proxmox "mount | grep nfs"           # current mounts
ssh proxmox "cat /etc/fstab | grep nfs"  # configured mounts
ssh proxmox "mount -a"                   # remount all
```

### Tailscale (if present)

```bash
# Find tailscale container
ssh proxmox "pct list" | grep -i tail

# Check status (replace CTID)
ssh proxmox "pct exec <CTID> -- tailscale status"
```

## Documentation Reference

Detailed infrastructure docs (IPs, service configs, setup history) are in:
`~/obsidian/Notes/PROXMOX_SETUP.md`

Read this file if you need static reference info not discoverable via commands.
