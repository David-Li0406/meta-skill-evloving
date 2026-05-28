---
name: dev-server
description: Manage the development server lifecycle. Use when starting, stopping, restarting the dev server, checking server status, viewing server logs, or before testing changes that require a running server.
---

# Dev Server Management

This skill manages the development server for this Next.js/PayloadCMS project. It ensures a single server instance is shared across all Claude Code sessions.

## Quick Start

```bash
# Default: Start server (if needed) + show 100 lines + tail logs
.claude/skills/dev-server/dev-server.sh
```

## Commands

| Command | Description |
|---------|-------------|
| *(none)* | **Default**: Start if needed, show last 100 lines, tail logs |
| `start` | Start server if not running |
| `stop` | Stop server gracefully |
| `restart` | Stop and start server |
| `status` | Show server status and health |
| `logs [N]` | Show last N lines (default 100) and tail |
| `health` | Quick health check |

## Usage Examples

```bash
# Default - most common usage
.claude/skills/dev-server/dev-server.sh

# Start without tailing logs
.claude/skills/dev-server/dev-server.sh start

# Check if server is running and healthy
.claude/skills/dev-server/dev-server.sh status

# View logs only
.claude/skills/dev-server/dev-server.sh logs

# Restart after config changes
.claude/skills/dev-server/dev-server.sh restart

# Stop when done
.claude/skills/dev-server/dev-server.sh stop
```

## Server Details

- **Port**: 3000 (configurable via PORT env var)
- **Start Command**: `pnpm devsafe` (cleans .next before starting)
- **Health Check**: `/api/managers/me` endpoint
- **Logs**: `.claude/skills/dev-server/state/server.log`

## URLs

Once running:
- **App**: http://localhost:3000
- **Admin**: http://localhost:3000/admin

## Admin Credentials

- **Email**: contact@sydevelopers.com
- **Password**: evk1VTH5dxz_nhg-mzk

## How It Works

The skill uses PID-based state tracking to ensure a single server across all Claude instances:

1. **PID File**: Tracks running server process
2. **Stale Detection**: Cleans up if process died
3. **Port Check**: Detects conflicts with other processes
4. **Health Check**: Waits up to 60s for server to be healthy

## When to Use

- Before testing any changes that require a running server
- When debugging server issues (use `logs` command)
- After configuration changes (use `restart` command)
- When switching branches or pulling changes (use `restart` command)
