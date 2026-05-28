# wt CLI Reference

Complete command reference for the wt worktree session manager.

## Global Options

These options apply to most commands:

| Flag | Description |
|------|-------------|
| `--help`, `-h` | Show help for command |

---

## Commands

### wt / wt list

List all active worker sessions.

```bash
wt
wt list
```

**Output columns:**
- Name - Session name (from namepool)
- Bead - Associated bead ID
- Status - Working/Idle/Error
- Last Activity - Time since last activity
- Title - Bead title (truncated)

**Status indicators:**
- `Working` - Claude actively using tools
- `Idle` - Waiting for input >5 minutes (marked with `!!`)
- `Error` - Error detected in session

**Example output:**
```
┌─ Active Sessions ───────────────────────────────────────────────────────┐
│                                                                         │
│  Name       Bead              Status    Last Activity   Title           │
│  ────       ────              ──────    ─────────────   ─────           │
│  toast      supabyoi-pks     Working   2m ago          Auto-harden VM  │
│  shadow     supabyoi-g4a     Idle      15m ago  !!     Encrypt secrets │
│  obsidian   reddit-saas-8lr  Working   1m ago          Supabase setup  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### wt new

Spawn a new worker session for a bead.

```bash
wt new <bead-id> [flags]
```

**Arguments:**
- `<bead-id>` - The bead ID to work on (required)

**Flags:**
| Flag | Description |
|------|-------------|
| `--name <name>` | Use specific name instead of pool |
| `--repo <path>` | Explicit project repository path |
| `--no-switch` | Don't switch to session after creating |

**What happens:**
1. Validates bead exists (`bd show <bead-id>`)
2. Determines project from bead prefix or `--repo`
3. Allocates session name from namepool
4. Creates git worktree at `~/worktrees/<name>/`
5. Creates branch named after bead
6. Allocates port offset for test isolation
7. Runs `test_env.setup` (e.g., docker compose up)
8. Runs `hooks.on_create` commands
9. Launches Claude in tmux session
10. Switches to session (unless `--no-switch`)

**Examples:**
```bash
# Basic spawn (auto-switch)
wt new supabyoi-pks

# Stay in hub after spawning
wt new supabyoi-pks --no-switch

# Use specific name
wt new supabyoi-pks --name myworker

# Explicit project path
wt new feature-123 --repo ~/myproject
```

**Errors:**
- "Bead not found" - Run `bd show <bead-id>` to verify
- "Session already exists for bead" - One bead = one session
- "Project not found" - Register with `wt project add`
- "Namepool exhausted" - Close some sessions first

---

### wt <name-or-bead>

Switch to an existing worker session.

```bash
wt <name>       # By session name
wt <bead-id>    # By bead (looks up session)
```

**What happens:**
1. Looks up session in sessions.json
2. Attaches to tmux session
3. You're now in the worker's Claude conversation

**Returning to hub:**
- Press `Ctrl-b d` to detach from tmux
- You return to the hub terminal

**Examples:**
```bash
wt toast           # Switch by name
wt supabyoi-pks    # Switch by bead
```

---

### wt status

Show current session info. Run from inside a worker session.

```bash
wt status
```

**Output:**
```
Session:   toast
Bead:      supabyoi-pks
Title:     Auto-harden VM security on add
Project:   supabyoi
Worktree:  ~/worktrees/toast/
Branch:    supabyoi-pks
Port:      1 (15432, 13000)
Status:    Working
```

---

### wt done

Complete work in current session. Run from inside a worker session.

```bash
wt done [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--merge-mode <mode>` | Override project's merge mode |

**Merge modes:**
- `direct` - Merge directly to main, delete branch
- `pr-auto` - Create PR, enable auto-merge
- `pr-review` - Create PR, wait for review (default)

**What happens:**
1. Checks for uncommitted changes (blocks if present)
2. Pushes branch to remote
3. Creates PR or merges (based on mode)
4. Updates bead status
5. Session remains active for potential fixes

**Examples:**
```bash
wt done                     # Use project's default merge mode
wt done --merge-mode direct # Force direct merge
```

---

### wt close

Complete work and cleanup session.

**From hub:**
```bash
wt close <name>
```

**From worker:**
```bash
wt close
```

**What happens:**
1. Runs `wt done` if work not submitted
2. Runs `hooks.on_close` commands
3. Runs `test_env.teardown` (docker compose down)
4. Removes worktree
5. Kills tmux session
6. Returns name to pool
7. Closes bead (`bd close`)

---

### wt kill

Terminate session without completing work.

```bash
wt kill <name> [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--keep-worktree` | Don't remove the worktree |

**What happens:**
1. Runs `test_env.teardown`
2. Removes worktree (unless --keep-worktree)
3. Kills tmux session
4. Returns name to pool
5. Bead remains open

**Use when:**
- Need to restart a stuck session
- Task is blocked, want to work on something else
- Debugging worktree issues

---

### wt abandon

Discard work and close session. Run from inside a worker.

```bash
wt abandon
```

**What happens:**
1. Prompts for confirmation
2. Discards all uncommitted changes
3. Runs teardown and cleanup
4. Bead remains open

---

### wt watch

Live monitoring dashboard.

```bash
wt watch [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--notify` | Desktop notifications on idle |
| `--interval <secs>` | Refresh interval (default: 30) |

**Interactive commands:**
- `q` - Quit
- `r` - Refresh
- `Enter` - Switch to selected session
- Arrow keys - Navigate

**Shows:**
- All active sessions with real-time status
- Idle detection with `!!` markers
- PRs pending review

---

### wt ready

Show beads ready for work across projects.

```bash
wt ready [project]
```

**Arguments:**
- `[project]` - Optional project name to filter

**Behavior:**
- Without project: Aggregates ready beads from ALL registered projects
- With project: Shows ready beads only from that project's `.beads/`

**Shows beads that:**
- Status is `open` (not in_progress or closed)
- Have no blocking dependencies
- Don't already have a worker session

**Examples:**
```bash
wt ready                    # All projects combined
wt ready foo-backend        # Just foo-backend beads
```

---

### wt create

Create a bead in a specific project from the hub.

```bash
wt create <project> <title> [flags]
```

**Arguments:**
- `<project>` - Registered project name
- `<title>` - Bead title

**Flags:**
| Flag | Description |
|------|-------------|
| `-d, --description` | Detailed description |
| `-p, --priority` | Priority (0=critical, 1=high, 2=normal, 3=low) |
| `-t, --type` | Issue type (task, bug, feature, epic, chore) |

**What happens:**
1. Looks up project in registered projects
2. Creates bead in `<project-repo>/.beads/`
3. Project's `.beads/` remains source of truth

**Examples:**
```bash
wt create foo-frontend "Implement login form"
wt create foo-backend "Add /users endpoint" -p 1 -t feature
wt create myapp "Fix auth bug" -d "Token refresh fails" -t bug
```

---

### wt beads

List beads for a specific project.

```bash
wt beads <project> [flags]
```

**Arguments:**
- `<project>` - Registered project name

**Flags:**
| Flag | Description |
|------|-------------|
| `-s, --status` | Filter by status (open, in_progress, closed) |

**Examples:**
```bash
wt beads foo-frontend                    # All beads
wt beads foo-frontend --status open      # Only open beads
wt beads foo-backend -s in_progress      # In-progress beads
```

---

### wt projects

List registered projects.

```bash
wt projects
```

**Output columns:**
- Name - Project name
- Repo - Repository path
- Merge Mode - Default merge strategy
- Active Sessions - Count of active workers

---

### wt project add

Register a new project.

```bash
wt project add <name> <path>
```

**Arguments:**
- `<name>` - Project name
- `<path>` - Path to repository

**Creates config at:** `~/.config/wt/projects/<name>.json`

**Example:**
```bash
wt project add myapp ~/myapp
```

---

### wt project config

Edit project configuration.

```bash
wt project config <name>
```

Opens project config in `$EDITOR`.

**Config options:**
```json
{
  "name": "myapp",
  "repo": "~/myapp",
  "default_branch": "main",
  "beads_prefix": "myapp",
  "merge_mode": "pr-review",
  "require_ci": true,
  "auto_merge_on_green": false,
  "test_env": {
    "setup": "docker compose up -d",
    "teardown": "docker compose down",
    "port_env": "PORT_OFFSET",
    "health_check": "curl -f http://localhost:${PORT_OFFSET}3000/health"
  },
  "hooks": {
    "on_create": ["npm install"],
    "on_close": ["docker compose down"]
  }
}
```

---

### wt project remove

Unregister a project.

```bash
wt project remove <name>
```

Removes config file. Does not delete repository.

---

### wt seance

List or interact with past sessions.

**List past sessions:**
```bash
wt seance [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--project <name>` | Filter by project |
| `--recent <n>` | Show last N sessions (default: 20) |

**Talk to past session:**
```bash
wt seance <name> [flags]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--prompt <text>`, `-p` | One-shot question |

**Examples:**
```bash
# List recent sessions
wt seance

# Filter by project
wt seance --project supabyoi

# Interactive conversation with past session
wt seance toast

# One-shot question
wt seance toast -p "What was blocking you?"
```

---

## Configuration Files

### Global Config

**Location:** `~/.config/wt/config.json`

```json
{
  "worktree_root": "~/worktrees",
  "editor_cmd": "claude",
  "default_merge_mode": "pr-review",
  "idle_threshold_minutes": 5,
  "notify_on_idle": true,
  "watch_interval_seconds": 30
}
```

### Namepool

**Location:** `~/.config/wt/namepool.txt`

One name per line. Names are allocated sequentially, returned when sessions close.

### Session State

**Location:** `~/.config/wt/sessions.json`

Tracks active sessions. Updated automatically.

### Event Log

**Location:** `~/.config/wt/events.jsonl`

Append-only log of session lifecycle events. Used by `wt seance`.

---

## Environment Variables

Workers receive these environment variables:

| Variable | Description |
|----------|-------------|
| `BEADS_DIR` | Path to project's .beads directory |
| `PORT_OFFSET` | Unique port offset for test isolation |
| `WT_SESSION` | Session name |
| `WT_BEAD` | Bead ID |
| `WT_PROJECT` | Project name |
