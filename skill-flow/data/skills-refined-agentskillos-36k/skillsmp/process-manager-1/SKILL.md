---
name: process-manager
description: Manage dev servers and long-running processes. Use when starting, stopping, or checking status of Node.js dev servers.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: development
  type: utility
  mode: application
---

# Process Manager: Dev Server Control

You manage dev servers and long-running processes for development workflows. Your role is to start, stop, and monitor processes without hanging or losing track of state.

## Core Principle

**Ports are ground truth.** Don't trust PID files or memory - check what's actually listening on each port. Start processes detached and verify by port, never wait for dev servers to exit.

## When to Use This Skill

- User asks to "start the server" or "run the dev server"
- User says "stop the API" or "kill the frontend"
- User asks "what's running?" or "is the server up?"
- Before running tests that need a server
- When debugging port conflicts
- When starting/stopping related processes together (groups)

## Quick Reference

### Script Location

```
.claude/skills/process-manager/scripts/process-manager.ts
```

### Common Commands

| Action | Command |
|--------|---------|
| Check all processes | `deno run --allow-run --allow-read --allow-net scripts/process-manager.ts status --all` |
| Start a process | `deno run ... start authoring-api` |
| Start a group | `deno run ... start authoring` |
| Stop everything | `deno run ... stop all` |
| Check single process | `deno run ... status authoring-api` |
| See what's on ports | `deno run ... ports` |
| List configured processes | `deno run --allow-read ... list` |

### Process States

| State | Meaning |
|-------|---------|
| RUNNING | Process listening on port |
| RUNNING [healthy] | Process responding to health check |
| RUNNING [unhealthy] | Process listening but health check fails |
| STOPPED | Nothing on port |

## Configuration

Configuration lives in `.claude/process-config.json` at project root.

### Config Schema

```json
{
  "processes": {
    "process-id": {
      "name": "Human-Readable Name",
      "port": 4000,
      "command": "pnpm dev:something",
      "healthCheck": {
        "url": "http://localhost:4000/health",
        "timeout": 5000
      },
      "startupTime": 5000,
      "group": "group-name"
    }
  },
  "groups": {
    "group-name": ["process-id-1", "process-id-2"],
    "all": ["process-id-1", "process-id-2", "process-id-3"]
  },
  "defaults": {
    "startupTime": 3000,
    "healthCheckTimeout": 5000
  }
}
```

## Operations

### Starting Processes

Before starting:
1. Check if port is already in use
2. If in use by expected process: report already running, skip
3. If in use by different process: report conflict

When starting:
1. Run command in background (detached with nohup)
2. Wait for configured startup time
3. Verify port is now in use
4. Report success/failure

**Key behavior**: Never wait for dev server to exit. Start detached and verify by port.

### Stopping Processes

1. Find PID via port (lsof)
2. Send SIGTERM
3. Wait up to 5s for graceful shutdown
4. If still running, SIGKILL
5. Verify port is free

### Checking Status

- Use `status --all` for overview
- Use `status <name>` for specific process
- Use `status <group>` for a group
- Includes health check if configured
- Exit code 1 if any requested process is stopped

### Port Scanning

The `ports` command shows:
- All configured ports and their status
- Common dev ports (3000, 4000, 5173, 8080, etc.)
- Unknown processes on expected ports

## Anti-Patterns

### The Hanging Start
**Pattern:** Running `pnpm dev` and waiting forever because dev servers don't exit.
**Problem:** Blocks the session, loses control of the process.
**Fix:** Start detached, verify by port, return immediately.

### The Stale PID File
**Pattern:** Trusting a PID file that refers to a dead or different process.
**Problem:** False positives/negatives about what's running.
**Fix:** Always check ports. Ports are ground truth.

### The Port Conflict Blindspot
**Pattern:** Starting a server without checking if port is in use.
**Problem:** Confusing errors, orphaned processes.
**Fix:** Always check port before starting. Report conflicts clearly.

### The Orphan Process
**Pattern:** Killing parent process but leaving child dev server running.
**Problem:** Port stays occupied, next start fails mysteriously.
**Fix:** Kill by port, not by PID hierarchy.

## Available Tools

### process-manager.ts

Main CLI tool for all process operations.

**Permissions:**
- `list`: `--allow-read`
- `status`, `start`, `restart`: `--allow-run --allow-read --allow-net`
- `stop`, `ports`: `--allow-run --allow-read`

**General permission set:** `--allow-run --allow-read --allow-net`

```bash
# List all configured processes
deno run --allow-read scripts/process-manager.ts list

# Check status of all processes
deno run --allow-run --allow-read --allow-net scripts/process-manager.ts status --all

# Check single process
deno run --allow-run --allow-read --allow-net scripts/process-manager.ts status authoring-api

# Start a process
deno run --allow-run --allow-read --allow-net scripts/process-manager.ts start authoring-api

# Start a group
deno run --allow-run --allow-read --allow-net scripts/process-manager.ts start authoring

# Stop a process
deno run --allow-run --allow-read scripts/process-manager.ts stop authoring-api

# Stop all
deno run --allow-run --allow-read scripts/process-manager.ts stop all

# Restart
deno run --allow-run --allow-read --allow-net scripts/process-manager.ts restart authoring-api

# Check port usage
deno run --allow-run --allow-read scripts/process-manager.ts ports

# JSON output (any command)
deno run ... status --all --json
```

## Example Interactions

### User: "Start the authoring API"

**Your approach:**
1. Run `status authoring-api` to check current state
2. If RUNNING: "Authoring API is already running on port 4000 (PID: X)"
3. If STOPPED: Run `start authoring-api`
4. Report: "Started Authoring API on port 4000 (PID: X)"

### User: "I'm getting port 4000 already in use error"

**Your approach:**
1. Run `ports` to see what's using port 4000
2. If it's the expected process: "Authoring API is already running. Use restart if you need to restart it."
3. If unexpected: "Port 4000 is in use by [command]. You can run `stop authoring-api` to kill it, or manually kill PID X."

### User: "Stop everything"

**Your approach:**
1. Run `stop all`
2. Report which processes were stopped

### User: "What's running?"

**Your approach:**
1. Run `status --all`
2. Report the status table

### User: "Start the frontend and API"

**Your approach:**
1. Check if there's a group that matches (e.g., "authoring" = authoring-api + authoring-app)
2. Run `start authoring` to start the group
3. Or run `start authoring-api` then `start authoring-app` if no group

## What You Do NOT Do

- You do not wait for dev servers to exit (they run forever)
- You do not trust PID files over port checks
- You do not start processes without checking port first
- You do not kill processes without user awareness
- You do not run commands outside the configured process list without asking
- You do not assume a process started successfully without verifying the port

## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Trigger | Action |
|---|---|---|
| Any development skill | "start the server" | Use start command |
| Testing workflows | Before tests | Ensure server running |

### Outbound (To Other Skills)
| Trigger | Target Skill | Action |
|---|---|---|
| Port conflict | User decision | Ask whether to kill conflicting process |
| Start failure | Debugging | Check logs, environment |

### Complementary Skills
| Skill | Relationship |
|---|---|
| github-agile | Start servers before testing PRs |
| mastra-hono | Manage Mastra API servers |

## Output Persistence

This skill does not produce persistent output. Process state is ephemeral and determined by port checks. Configuration lives in `.claude/process-config.json`.

## Verification

### What This Skill Can Verify
- Process is listening on port (High confidence - lsof)
- Health check endpoint responds (High confidence - HTTP)
- Process was started by expected command (Medium confidence - ps)

### What Requires User Judgment
- Whether to kill a conflicting process
- Whether startup failure is due to port conflict or code error
- Whether health check failure is transient
