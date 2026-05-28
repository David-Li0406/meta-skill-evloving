# CLI Reference

Complete documentation for all recall commands.

## recall index

Index sessions from Claude Code and Codex into the database.

```bash
recall index [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--full` | Force full reindex of all sessions |
| `--source` | Filter by source: `claude-code` or `codex` |
| `--recreate` | Backup and rebuild database from scratch |
| `-v, --verbose` | Enable verbose logging |
| `--json` | Output results as JSON |

**Example output:**
```
Indexed 15 sessions, skipped 42, failed 0 (total 57).
```

## recall search

Full-text search across session content and tool calls.

```bash
recall search <query> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--tool` | Filter to Bash tool calls only (searches bash commands) |
| `--source` | Filter by source: `claude-code` or `codex` |
| `--json` | Output results as JSON |

**Example output:**
```
[0.85] abc123def456 (claude_code)
  assistant: Implemented OAuth2 authentication flow using...
  source: ~/.claude/projects/my-app/session.jsonl
  time: 2024-01-15T10:30:00
```

## recall list

List sessions with optional filters.

```bash
recall list [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--source` | Filter by source: `claude-code` or `codex` |
| `--since` | Time window: `7d`, `24h`, `2024-01-01` |
| `--project` | Filter by git repo path |
| `--json` | Output results as JSON |

**Example output:**
```
[2024-01-15 10:30] abc123 (claude_code) /path/to/repo messages=25 tools=12
[2024-01-14 14:22] def456 (codex) /path/to/project messages=8 tools=3
```

## recall show

Display detailed session information.

```bash
recall show <session-id> [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--tools` | Include tool calls in output |
| `--thinking` | Include thinking blocks (Claude Code) |
| `--json` | Output results as JSON |

**Example output:**
```
[2024-01-15 10:30] Session abc123def456 (claude_code)
Project: /path/to/my-app
Duration: 1234s | Messages: 25 | Tools: 12

[10:30:15] user:
Fix the authentication bug

[10:30:45] assistant:
I'll look into the authentication code...
  [Read] src/auth.py
  [Edit] src/auth.py
```

## recall stats

Analytics subcommands for usage patterns.

### recall stats (overview)

```bash
recall stats [--json]
```

**Output:**
```
Overview
  Sessions: 142
  Messages: 3567
  Tool calls: 1234
  Bash calls: 456
```

### recall stats tools

Tool usage frequency.

```bash
recall stats tools [--json]
```

**Output:**
```
Bash: 456
Read: 312
Edit: 234
Glob: 156
Grep: 89
Write: 45
```

### recall stats bash

Bash command breakdown and permission suggestions.

```bash
recall stats bash [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--suggest` | Generate permission suggestions for auto-approval |
| `--json` | Output results as JSON |

**Without --suggest:**
```
git status: 45
npm test: 32
git diff: 28
npm install: 15 (compound)
```

**With --suggest:**
```
Suggested Bash Permissions
==========================
high: run tests (45 uses)
high: git operations (73 uses)
medium: npm/yarn commands (47 uses)
Skipped
- rm -rf: dangerous command
```

### recall stats tokens

Token usage by project.

```bash
recall stats tokens [--json]
```

**Output:**
```
/path/to/project-a: 125000 in / 45000 out
/path/to/project-b: 89000 in / 32000 out
```

## JSON Output

All commands support `--json` for machine-readable output. JSON output includes all fields and is suitable for piping to `jq` or programmatic processing.

```bash
recall list --json | jq '.[] | .id'
recall stats tools --json | jq 'to_entries | sort_by(-.value) | .[0]'
```

## Data Locations

| Data | Path |
|------|------|
| Database | `~/.local/share/recall/recall.duckdb` |
| Lock file | `~/.local/share/recall/recall.lock` |
| Claude Code sessions | `~/.claude/projects/**/*.jsonl` |
| Codex sessions | `~/.codex/sessions/*/rollout.jsonl` |
