---
name: otterstack-usage
description: Use this skill when deploying Docker Compose applications with OtterStack, managing projects, configuring environment variables, or troubleshooting deployments.
---

# OtterStack Usage Guide

Complete reference for using OtterStack - a Git-driven deployment orchestrator for Docker Compose applications with zero-downtime deployments via Traefik priority-based routing.

## What is OtterStack?

OtterStack is a **Git-driven deployment orchestrator** for Docker Compose applications running on a single VPS. It provides:

- **Zero-downtime deployments** using Traefik priority-based routing
- **Git worktree isolation** - each deployment gets its own directory
- **Health check validation** before traffic switching
- **Automatic rollback** if deployments fail
- **Environment variable management** with smart type detection
- **Deployment history** and retention policies

### Core Concepts

1. **Projects**: A project is a Docker Compose application tracked in git.
2. **Worktrees**: Each deployment creates an isolated git worktree.
3. **Deployments**: Deploy any git ref (commit, branch, tag).
4. **Priority Routing**: New containers start at priority 200, old at 100.
5. **Health Checks**: Validates containers before traffic switch (5 min timeout).

## Installation

```bash
go build ./cmd/otterstack
./otterstack version
```

## Quick Start

### 1. Add Your First Project

**Local repository:**
```bash
otterstack project add myapp /srv/myapp
```

**Remote repository:**
```bash
otterstack project add myapp https://github.com/user/repo.git
```

**With Traefik zero-downtime routing:**
```bash
otterstack project add myapp https://github.com/user/repo.git --traefik-routing
```

**Custom compose file:**
```bash
otterstack project add myapp /srv/myapp --compose-file docker-compose.prod.yml
```

### 2. Configure Environment Variables

OtterStack has **smart environment variable management** with auto-discovery!

**Option 1: Auto-discovery during project add**
```bash
# Create .env.<project-name> in current directory
echo "DATABASE_URL=postgres://localhost/mydb" > .env.myapp
echo "API_KEY=secret123" >> .env.myapp

# Add project - OtterStack will auto-discover and load the file
otterstack project add myapp /srv/
```