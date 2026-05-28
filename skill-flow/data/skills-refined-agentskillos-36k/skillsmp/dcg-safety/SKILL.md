---
name: dcg-safety
description: |
  Destructive Command Guard (DCG) safety hook for all AI coding agents.
  Rust-based PreToolUse hook that blocks dangerous git and filesystem commands.
  Use when agent attempts destructive operations, safety verification is needed,
  or when checking protection status across VMs.
  Keywords: safety, git reset, rm -rf, destructive, guard, hooks, protection
tags: [safety, hooks, git, protection]
compatibility: Requires DCG binary installed via curl script. Works with Claude Code, Gemini CLI, Codex CLI, Antigravity.
allowed-tools:
  - Bash(dcg:*)
  - Bash(which:*)
  - Read
---

# DCG Safety Guard

**Replaces:** git-safety-guard (deprecated)

DCG is a Rust-based safety hook that blocks dangerous commands before they execute.

## What It Blocks

### Git Operations
- `git reset --hard` - Discards uncommitted changes
- `git checkout -- <files>` - Discards file changes
- `git clean -f` - Deletes untracked files
- `git push --force` - Rewrites remote history
- `git branch -D` - Force deletes branches
- `git stash drop/clear` - Deletes stashed work

### Filesystem Operations
- `rm -rf /` or `rm -rf ~` - Recursive delete of important paths
- `chmod -R 777` - Insecure permissions

### Database Operations (with database pack)
- `DROP TABLE`, `DROP DATABASE`
- `TRUNCATE TABLE`
- `DELETE FROM` without WHERE

### What It ALLOWS
- `git reset --soft` - Safe undo
- `rm -rf /tmp/*` - Temp cleanup
- `git checkout <branch>` - Branch switching (no `--`)

## Quick Verification

```bash
# Check DCG installed
which dcg && dcg --version

# Test blocking (should output {"decision": "block"})
echo '{"tool": "Bash", "input": {"command": "git reset --hard"}}' | dcg

# Test allowing (should output {"decision": "allow"})
echo '{"tool": "Bash", "input": {"command": "git status"}}' | dcg
```

## Installation (All VMs)

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/destructive_command_guard/main/install.sh?$(date +%s)" | bash
```

## Configuration

### Claude Code (`~/.claude/settings.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "dcg"}]
      }
    ]
  }
}
```

### Gemini CLI (`~/.gemini/settings.json`)
```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Bash", "hooks": [{"type": "command", "command": "dcg"}]}
    ]
  }
}
```

### Enable Database Pack (`~/.config/dcg/config.toml`)
```toml
[packs]
enabled = ["database.postgresql"]
```

## Verify Across VMs

```bash
# Check all VMs have DCG
for vm in homedesktop-wsl epyc6 macmini; do
    ssh $vm "which dcg && dcg --version" 2>/dev/null || echo "❌ $vm missing DCG"
done
```

## If Blocked Unexpectedly

DCG explains why in its output:
```json
{
  "decision": "block",
  "reason": "git reset --hard discards uncommitted changes",
  "pattern": "git.reset_hard",
  "suggestion": "Use 'git reset --soft' to keep changes staged"
}
```

If you need to run a blocked command legitimately, ask the human to run it directly.

---

**Last Updated:** 2026-01-14
**Repository:** https://github.com/Dicklesworthstone/destructive_command_guard
**Replaces:** ~/agent-skills/git-safety-guard/
