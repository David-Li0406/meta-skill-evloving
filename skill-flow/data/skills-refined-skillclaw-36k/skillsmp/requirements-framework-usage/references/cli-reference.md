# CLI Command Reference

Complete reference for the `req` command-line tool.

## Command Overview

| Command | Purpose | Common Flags |
|---------|---------|--------------|
| `req status` | Show requirement status | `--verbose`, `--session` |
| `req satisfy <name>` | Mark requirement satisfied | `--session`, `--ttl`, `--metadata` |
| `req clear <name>` | Clear a requirement | `--session` |
| `req list` | List all requirements | `--enabled-only` |
| `req sessions` | View active sessions | `--project`, `--all` |
| `req init` | Interactive project setup | `--preset`, `--yes`, `--project`, `--local` |
| `req config` | View/modify configuration | `--enable`, `--disable`, `--scope`, `--set` |
| `req doctor` | Verify installation | - |
| `req verify` | Quick installation check | - |
| `req prune` | Clean stale data | `--dry-run` |
| `req enable <name>` | Enable a requirement | `--project`, `--local` |
| `req disable <name>` | Disable a requirement | `--project`, `--local` |
| `req logging` | Configure logging | `--level`, `--destinations`, `--local` |

---

## req status

Show current requirement status for the session/branch.

```bash
req status                    # Default view
req status --verbose          # Detailed output
req status --session abc123   # Specific session
```

**Output includes**:
- Satisfied/unsatisfied requirements
- Session ID and project path
- Scope information (session/branch/permanent/single_use)

---

## req satisfy

Mark a requirement as satisfied.

```bash
req satisfy commit_plan                      # Basic usage
req satisfy commit_plan --session abc123     # Explicit session
req satisfy commit_plan --ttl 3600           # Expire after 1 hour
req satisfy commit_plan --metadata '{"key":"value"}'  # Store metadata
```

**Flags**:
- `--session <id>` - Specify session ID (auto-detected if omitted)
- `--ttl <seconds>` - Time-to-live before auto-expiration
- `--metadata <json>` - Attach JSON metadata to satisfaction

---

## req clear

Clear a satisfied requirement.

```bash
req clear commit_plan                    # Basic usage
req clear commit_plan --session abc123   # Explicit session
```

---

## req list

List all configured requirements.

```bash
req list                  # All requirements
req list --enabled-only   # Only enabled ones
```

**Output shows**:
- Requirement name
- Enabled status
- Scope
- Type (blocking/dynamic/guard)

---

## req sessions

View active Claude Code sessions.

```bash
req sessions              # All sessions
req sessions --project    # Current project only
req sessions --all        # Include stale sessions
```

**Output includes**:
- Session ID
- Project path
- Branch name
- PID (process ID)
- Start time

---

## req init

Interactive project initialization wizard.

```bash
req init                     # Interactive mode
req init --preset strict     # Use preset (non-interactive)
req init --yes               # Non-interactive with defaults
req init --project           # Force project config
req init --local             # Force local config
req init --preview           # Show changes without writing
req init --force             # Overwrite existing config
```

**Presets**:
- `strict` - All requirements, session scope (recommended for teams)
- `relaxed` - Basic requirements, branch scope
- `minimal` - Only commit_plan (learning mode)
- `advanced` - All features + branch size limits + guards
- `inherit` - Inherit from global config

---

## req config

View and modify requirement configuration.

### View Configuration

```bash
req config                   # View all requirements
req config commit_plan       # View specific requirement
```

### Modify Configuration

```bash
# Toggle requirement
req config commit_plan --enable
req config commit_plan --disable

# Change scope
req config commit_plan --scope branch
req config commit_plan --scope session
req config commit_plan --scope permanent
req config commit_plan --scope single_use

# Update message
req config commit_plan --message "New message text"

# Set arbitrary fields (auto-parses JSON)
req config adr_reviewed --set adr_path=/custom/path
req config branch_size_limit --set threshold=500
req config github_ticket --set auto_extract=true
req config my_requirement --set metadata='{"key":"value"}'
```

**Flags**:
- `--enable` / `--disable` - Toggle requirement on/off
- `--scope <scope>` - Change scope (session/branch/permanent/single_use)
- `--message <text>` - Update user-facing message
- `--set KEY=VALUE` - Set arbitrary fields
- `--yes` - Skip confirmation prompts
- `--project` - Modify project config
- `--local` - Modify local config

---

## req doctor

Comprehensive diagnostics for the framework installation.

```bash
req doctor
```

**Checks**:
1. Python version (minimum 3.9)
2. Hook registration in `~/.claude/settings.json`
3. File permissions (executable)
4. Sync status (repo vs deployed)
5. Library imports
6. Test suite (pass/fail count)

---

## req verify

Quick installation verification.

```bash
req verify
```

**Checks**:
- CLI accessibility
- Hooks directory exists
- Core libraries present
- Test suite accessible

---

## req prune

Clean stale sessions and branch data.

```bash
req prune              # Clean stale data
req prune --dry-run    # Show what would be cleaned
```

---

## req logging

Configure logging settings.

```bash
req logging                                    # Show current config
req logging --level debug                      # Set log level
req logging --level debug --local              # Set for current project only
req logging --destinations file stdout         # Log to file and stdout
req logging --destinations file --local        # Project-specific
```

**Log levels**: debug, info, warning, error

**Destinations**: file, stdout, stderr

**Log file location**: `~/.claude/requirements.log`

---

## Session ID Auto-Detection

Most commands auto-detect the correct session ID based on:
1. Current working directory
2. Active Claude Code process (PID)
3. Session registry (`~/.claude/sessions.json`)

Use `--session <id>` when:
- Running from outside a Claude session
- Multiple sessions active for same project
- Session auto-detection fails

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Requirement not found |
| 3 | Session not found |
| 4 | Configuration error |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CLAUDE_SKIP_REQUIREMENTS` | Skip all requirement checks |
| `CLAUDE_SESSION_ID` | Override session ID detection |
| `NO_COLOR` | Disable colored output |
| `FORCE_COLOR` | Force colored output |
