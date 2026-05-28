find ~ -name "*.jsonl" -path "*/.claude/projects/*" 2>/dev/null

# Step 4: List all sessions currently stored
echo "Total sessions:"
find ~/.claude/projects -name "*.jsonl" -type f | wc -l
```

### Fix

```bash
/usr/bin/env bash << 'VALIDATE_EOF'
# Immediate fix (current shell only)
export HOME=/home/$(whoami)

# Test session creation
echo "test" | claude --dangerously-skip-permissions --model sonnet

# Verify new session appears
find ~/.claude/projects -name "*.jsonl" -type f -newermt "1 minute ago"
VALIDATE_EOF
```

### Prevention

**Check IDE/Terminal Settings:**

- **Cursor**: Settings → Environment → Verify HOME variable
- **VS Code**: Settings → Environment → Check Remote SSH config
- **macOS Terminal**: System Preferences → Advanced → Shell login behavior
- **Zellij/Tmux**: Check shell initialization in config files

## Session Creation Troubleshooting

### Checklist: If Sessions Aren't Creating

1. **Verify Authentication**

   ```bash
   claude /login
   # Should show: "✓ Authenticated as user@email.com"
   ```

1. **Check HOME Variable**

   ```bash
   echo "HOME: $HOME"
   # Should show: /home/username (on Linux) or /Users/username (on macOS)
   ```

1. **Test Directory Access**

   ```bash
   ls -ld ~/.claude/projects/
   # Should show: drwx------ (readable/writable)

   # Write test
   touch ~/.claude/projects/test.tmp && rm ~/.claude/projects/test.tmp
   # Should succeed without errors
   ```

1. **Monitor Session File Creation**

   ```bash
/usr/bin/env bash << 'TROUBLESHOOTING_SCRIPT_EOF'
   # Count before
   BEFORE=$(find ~/.claude/projects -name "*.jsonl" | wc -l)

   # Run a quick test
   echo "test" | claude --dangerously-skip-permissions

   # Count after
   AFTER=$(find ~/.claude/projects -name "*.jsonl" | wc -l)
   echo "Before: $BEFORE, After: $AFTER"
   # Should show increase of 1
   
TROUBLESHOOTING_SCRIPT_EOF
```

1. **Check for Sessions in Wrong Locations**

   ```bash
   # Sessions might be in /tmp or other $HOME variants
   find /tmp -name "*.jsonl" -path "*/.claude/projects/*" -newermt "1 hour ago" 2>/dev/null
   ```

## Session Resume Behavior

### "No Conversations Found to Resume"

**This message can mean:**

- Sessions exist but are marked as complete (normal behavior)
- Sessions exist but have format issues
- Sessions stored in wrong location (HOME variable issue)
- No valid incomplete sessions available

**Incomplete sessions** (can resume):

- Must have at least one assistant message
- Must not be marked as complete
- Must be reachable via `~/.claude/projects/`

**Complete sessions** (won't resume):

- Are archived automatically after finishing
- Can be viewed but not resumed
- Don't appear in `claude -r` output

### Verification Commands

```bash
# Count total sessions (all types)
find ~/.claude/projects -name "*.jsonl" -type f | wc -l

# Check recent sessions (last 24 hours)
find ~/.claude/projects -name "*.jsonl" -type f -newermt "1 day ago"

# Inspect first session's format
head -n 1 ~/.claude/projects/*/*.jsonl | python -m json.tool

# Count resumable sessions (with assistant messages)
find ~/.claude/projects -name "*.jsonl" -exec grep -l "\"role\":\"assistant\"" {} \;
```

## Session Recovery (Migration)

### Migrating Legacy Sessions

For sessions in non-standard locations (e.g., `~/.claude/system/sessions/`):

```bash
# Using provided recovery script
bash ~/.claude/tools/session-recovery.sh

# What it does:
# - Detects multiple session directory formats
# - Preserves timestamps and metadata
# - Maps platform-specific paths to ~/.claude/projects/
# - Idempotent (safe to run multiple times)
```

### Manual Recovery

```bash
/usr/bin/env bash << 'VALIDATE_EOF_2'
# Step 1: Backup existing sessions
cp -r ~/.claude/projects ~/.claude/projects.backup

# Step 2: Move legacy sessions
mv ~/.claude/system/sessions/* ~/.claude/projects/

# Step 3: Verify all sessions still exist
echo "Sessions before: $(find ~/.claude/projects.backup -name '*.jsonl' | wc -l)"
echo "Sessions after: $(find ~/.claude/projects -name '*.jsonl' | wc -l)"

# Step 4: Test resume
claude -r
VALIDATE_EOF_2
```

## Key Learnings

1. **Official format is correct**: `~/.claude/projects/` confirmed by isolated Docker tests
1. **Environment is critical**: Wrong `$HOME` breaks everything, regardless of file structure
1. **IDE settings override**: Terminal.app, Cursor, VS Code can override HOME variable
1. **Resumability requirements**: Sessions need assistant responses to be resumable (complete sessions are auto-archived)
1. **Symlinks can confuse tools**: Avoid symlinks pointing to custom session directories

## Setup Checklist

- [ ] Verify `$HOME` matches system expectation: `echo $HOME` vs `getent passwd $(whoami)`
- [ ] Check IDE terminal settings (Cursor, VS Code remote)
- [ ] Verify `~/.claude/projects/` directory exists and is writable
- [ ] Run recovery script if migrating from old session storage
- [ ] Test session creation: `echo "test" | claude --dangerously-skip-permissions`
- [ ] Verify new session file appears: `find ~/.claude/projects -name "*.jsonl" -newermt "1 minute ago"`
- [ ] Test resume: `claude -r` should show resumable conversations

## See Also

- **Reference**: Check `TROUBLESHOOTING.md` for complete troubleshooting workflows and diagnostic procedures
- **Full Context**: `docs/standards/CLAUDE_SESSION_STORAGE_STANDARD.md` for empirical evidence (Docker test)
- **Related**: `docs/setup/TEAM_SETUP.md` for workspace initialization on new machines
