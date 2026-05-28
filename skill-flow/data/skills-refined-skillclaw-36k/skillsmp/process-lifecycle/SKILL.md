---
name: process-lifecycle
description: Unified process lifecycle management for all Ralph agents
category: orchestration
depends-on: [ralph-core]
---

# Process Lifecycle Management

**MANDATORY**: All agents MUST follow these rules for any process they start.

---

## The Golden Rules

1. **ALWAYS** check the process registry before starting a process
2. **ALWAYS** register processes you start
3. **ALWAYS** cleanup your processes when done
4. **NEVER** start a duplicate process if one is already running
5. **NEVER** leave background processes running when you exit

---

## Process Registry

**Location**: `.claude/session/process-registry.json`

The process registry tracks all running processes across all agents. It prevents duplicate processes and enables proper cleanup.

**Format**:

```json
{
  "version": "1.0",
  "lastUpdated": "2026-01-21T10:00:00Z",
  "processes": {
    "dev-server-3000": {
      "name": "dev-server",
      "port": 3000,
      "pid": 12345,
      "agent": "qa",
      "startedAt": "2026-01-21T09:55:00Z",
      "command": "npm run dev",
      "status": "running",
      "purpose": "browser-validation"
    }
  },
  "agents": {
    "qa": ["dev-server-3000"],
    "developer": [],
    "pm": []
  }
}
```

---

## Before Starting Any Process

### 1. Check if Already Running

**Use the helper function**:

```powershell
# Check if dev server is already running
$existing = Get-ManagedProcess -Name "dev-server" -Port 3000

if ($existing) {
    # Reuse existing process
    Write-Host "Reusing existing dev server (PID: $($existing.pid))"
} else {
    # Start new process
    $process = Start-ManagedProcess -Name "dev-server" -Port 3000 -Command "npm run dev"
}
```

### 2. Check Port Availability

```powershell
# Cross-platform port check
$portInUse = Test-Port -Port 3000

if ($portInUse) {
    # Find what's using it
    $owner = Get-ProcessByPort -Port 3000
    # Decide: reuse or terminate
}
```

---

## When You're Done

### Cleanup is MANDATORY

**At the end of your task, before marking complete**:

```powershell
# Stop all processes you started
Stop-ManagedProcess -Agent "qa"  # or "developer" or "pm"
```

**CRITICAL**: Update your status to "idle" ONLY AFTER cleanup.

---

## Agent-Specific Rules

### QA Agent

- **Dev server**: Start once, reuse for all browser tests, cleanup after validation
- **Test watcher**: Start if needed, cleanup after test loop
- **E2E test server**: Start, test, cleanup immediately

### Developer Agent

- **Build watcher**: Start if doing iterative builds, cleanup after commit
- **Dev server**: Start only if testing, cleanup immediately

### PM Agent

- Usually doesn't start processes
- If starting a research server: cleanup after research

---

## Process Types

| Type | Port | Reuse? | Cleanup |
|------|------|-------|---------|
| dev-server | 3000 | Yes | After validation |
| test-server | varies | No | After tests |
| build-watcher | N/A | Yes | After commit |
| storybook | 6006 | Yes | After review |

---

## Anti-Patterns

### DON'T

- Start processes in background without tracking
- Use `&` or `Start-Process` without registration
- Leave processes running after your task completes
- Start the same process multiple times
- Assume someone else will cleanup

### DO

- Always use `Start-ManagedProcess` helper
- Always register in process-registry.json
- Always cleanup with `Stop-ManagedProcess`
- Check for existing processes before starting
- Cleanup your own processes before going idle

---

## Workflow Example

### Complete QA Validation Workflow

```powershell
# 1. Check for existing dev server
$server = Get-ManagedProcess -Name "dev-server" -Port 3000

# 2. Start if needed
if (-not $server) {
    $server = Start-ManagedProcess -Name "dev-server" -Port 3000 -Command "npm run dev"
    Write-Host "Started dev server (PID: $($server.pid))"
} else {
    Write-Host "Reusing existing dev server (PID: $($server.pid))"
}

# 3. Run validation tests
npm run type-check
npm run lint
npm run test
npm run build

# 4. Run browser tests (using existing server)
# ... Playwright MCP tests ...

# 5. MANDATORY: Cleanup after validation completes
Stop-ManagedProcess -Agent "qa"

# 6. Only AFTER cleanup, update task status
# ... update coordinator-state.json ...
```

---

## Helper Scripts Reference

| Script | Purpose |
|--------|---------|
| `Get-ManagedProcess.ps1` | Check if process exists, return details or start new |
| `Stop-ManagedProcess.ps1` | Stop all processes owned by an agent |
| `Test-Port.ps1` | Check if a port is in use |

---

## Reference

- [auxiliary-scripts.md](auxiliary-scripts.md) — Script management
- [ralph-core.md](ralph-core.md) — Session structure
- [atomic-updates.md](atomic-updates.md) — Safe file updates
