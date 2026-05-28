# Recovery Procedures

Procedures for recovering from Claude Code issues and restoring normal operation.

## Clearing Cache

### Session Cache

```bash
# Clear current session
rm -rf ~/.claude/sessions/current/

# Clear all sessions (keeps settings)
rm -rf ~/.claude/sessions/

# Clear session with backup
mv ~/.claude/sessions/ ~/.claude/sessions.bak/
```

### Response Cache

```bash
# Start without cache
claude --no-cache

# Clear response cache
rm -rf ~/.claude/cache/
```

### MCP Cache

```bash
# Clear MCP connection cache
rm -rf ~/.claude/mcp/

# Reset MCP approvals for project
claude mcp reset-project-choices
```

### Full Cache Clear

```bash
#!/bin/bash
# clear-all-caches.sh

echo "Clearing Claude Code caches..."

# Session cache
rm -rf ~/.claude/sessions/

# Response cache
rm -rf ~/.claude/cache/

# MCP cache
rm -rf ~/.claude/mcp/

# Temporary files
rm -rf /tmp/claude-*

echo "Caches cleared."
```

---

## Resetting Permissions

### View Current Permissions

```bash
/permissions
```

### Reset to Defaults

```bash
# Remove permission overrides from settings
jq 'del(.permissions)' ~/.claude/settings.json > tmp.json
mv tmp.json ~/.claude/settings.json

# Restart Claude Code
```

### Reset Project Permissions

```bash
# Remove project-specific permissions
rm .claude/settings.local.json

# Or edit to remove permissions
jq 'del(.permissions)' .claude/settings.json > tmp.json
mv tmp.json .claude/settings.json
```

### Reset MCP Tool Approvals

```bash
# Reset all MCP approvals for current project
claude mcp reset-project-choices

# This clears remembered "allow" decisions for MCP tools
```

### Grant Fresh Permissions

After reset, Claude will ask for permissions again. Or pre-configure:

```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash",
      "Glob",
      "Grep"
    ]
  }
}
```

---

## Reinstalling Claude Code

### Standard Reinstall

```bash
# Using npm
npm uninstall -g @anthropic/claude-code
npm install -g @anthropic/claude-code

# Using bun
bun remove -g @anthropic/claude-code
bun add -g @anthropic/claude-code
```

### Clean Reinstall

```bash
#!/bin/bash
# clean-reinstall.sh

echo "Performing clean reinstall of Claude Code..."

# 1. Uninstall
npm uninstall -g @anthropic/claude-code 2>/dev/null
bun remove -g @anthropic/claude-code 2>/dev/null

# 2. Clear caches (but preserve settings)
rm -rf ~/.claude/cache/
rm -rf ~/.claude/sessions/
rm -rf ~/.claude/mcp/

# 3. Reinstall
npm install -g @anthropic/claude-code

# 4. Verify
claude --version

echo "Reinstall complete."
```

### Full Clean Reinstall (Warning: Removes Settings)

```bash
#!/bin/bash
# full-clean-reinstall.sh

echo "WARNING: This will remove all Claude Code settings and data."
read -p "Continue? (y/N) " confirm
if [ "$confirm" != "y" ]; then
  echo "Aborted."
  exit 0
fi

# 1. Backup settings
cp -r ~/.claude/ ~/.claude.backup.$(date +%Y%m%d)/

# 2. Uninstall
npm uninstall -g @anthropic/claude-code 2>/dev/null
bun remove -g @anthropic/claude-code 2>/dev/null

# 3. Remove all data
rm -rf ~/.claude/

# 4. Reinstall
npm install -g @anthropic/claude-code

# 5. Initial setup
claude

echo "Full reinstall complete. Previous settings backed up."
```

### Verify Installation

```bash
# Check installation
which claude
claude --version

# Test basic functionality
claude --help

# Test API connection
claude doctor
```

---

## Session Recovery

### Recover from Hung Session

```bash
# 1. Try Ctrl+C first
^C

# 2. If that doesn't work, find and kill process
ps aux | grep claude
kill -9 <pid>

# 3. Start fresh
claude
```

### Recover Session Context

```bash
# List recent sessions
ls -lt ~/.claude/sessions/ | head -10

# View session transcript
cat ~/.claude/sessions/<session-id>/transcript.json | jq '.messages | length'

# Sessions are not resumable, but you can reference transcripts
```

### Resume from Checkpoint

If using `/checkpoint` command:

```bash
# List checkpoints
ls ~/.claude/checkpoints/

# Reference checkpoint in new session
# (Provide context from checkpoint manually)
```

### Export Session History

```bash
# Export current session
/export session.json

# Export as markdown
/export session.md
```

---

## Configuration Reset

### Reset User Settings

```bash
# Backup first
cp ~/.claude/settings.json ~/.claude/settings.json.bak

# Option 1: Remove entirely (uses defaults)
rm ~/.claude/settings.json

# Option 2: Reset to minimal
echo '{}' > ~/.claude/settings.json
```

### Reset Specific Settings

```bash
# Reset hooks only
jq 'del(.hooks)' ~/.claude/settings.json > tmp.json && mv tmp.json ~/.claude/settings.json

# Reset permissions only
jq 'del(.permissions)' ~/.claude/settings.json > tmp.json && mv tmp.json ~/.claude/settings.json

# Reset MCP servers only
jq 'del(.mcpServers)' ~/.claude/settings.json > tmp.json && mv tmp.json ~/.claude/settings.json
```

### Reset Project Settings

```bash
# Remove project settings
rm .claude/settings.json
rm .claude/settings.local.json

# Remove MCP config
rm .mcp.json
```

### Reset Credentials

```bash
# Remove credentials
rm ~/.claude/.credentials.json

# Re-authenticate
claude auth login
```

### Default Configuration Template

```json
// ~/.claude/settings.json - Sensible defaults
{
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(bun:*)"
    ]
  },
  "hooks": {},
  "mcpServers": {}
}
```

---

## When to Contact Support

### Use /bug Command

```bash
# In Claude Code session
/bug

# Follows guided bug report process
# Includes system info automatically
```

### Support-Worthy Issues

Contact support when:

- `claude doctor` shows persistent failures
- Crashes that are reproducible
- API errors that persist after credential refresh
- Behavior that contradicts documentation
- Security concerns

### Information to Include

1. **Version Information**
   ```bash
   claude --version
   uname -a
   ```

2. **Debug Output**
   ```bash
   ANTHROPIC_LOG=debug claude --debug 2>&1 | head -500
   ```

3. **Steps to Reproduce**
   - Exact commands run
   - Expected vs actual behavior
   - Frequency of issue

4. **Configuration** (sanitized)
   ```bash
   cat ~/.claude/settings.json | jq 'del(.credentials)'
   ```

### Do NOT Include

- API keys
- Authentication tokens
- Sensitive file contents
- Personal information

### Bug Report Template

```markdown
## Summary
Brief description of the issue.

## Environment
- Claude Code version: X.Y.Z
- OS: macOS/Linux/Windows + version
- Shell: bash/zsh/fish

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Debug Output
```
Relevant debug output here
```

## Configuration
```json
Sanitized settings here
```

## Additional Context
Any other relevant information.
```

---

## Recovery Checklist

Use this checklist when troubleshooting:

### Quick Recovery
- [ ] Try `Ctrl+C` to cancel current operation
- [ ] Run `claude doctor` to check health
- [ ] Check `/permissions` for blocked tools
- [ ] Check `/hooks` for misconfigured hooks
- [ ] Check `/mcp` for disconnected servers

### Configuration Recovery
- [ ] Validate JSON with `jq . settings.json`
- [ ] Check for conflicting project settings
- [ ] Reset specific settings if needed
- [ ] Verify credentials are valid

### Cache Recovery
- [ ] Clear session cache
- [ ] Clear response cache
- [ ] Reset MCP approvals
- [ ] Restart Claude Code

### Full Recovery
- [ ] Back up current settings
- [ ] Uninstall Claude Code
- [ ] Clear all caches and data
- [ ] Reinstall Claude Code
- [ ] Restore settings from backup
- [ ] Test with `claude doctor`

### When Nothing Works
- [ ] Gather debug output
- [ ] Document steps to reproduce
- [ ] Use `/bug` to report issue
- [ ] Check for known issues in release notes

---

## Backup Best Practices

### Regular Backups

```bash
#!/bin/bash
# backup-claude-config.sh

BACKUP_DIR=~/.claude-backups
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup settings
tar -czf "$BACKUP_DIR/claude-$DATE.tar.gz" \
  ~/.claude/settings.json \
  ~/.claude/projects.json \
  .claude/settings.json \
  .claude/settings.local.json \
  .mcp.json \
  2>/dev/null

echo "Backed up to $BACKUP_DIR/claude-$DATE.tar.gz"

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/*.tar.gz | tail -n +11 | xargs rm -f 2>/dev/null
```

### Restore from Backup

```bash
#!/bin/bash
# restore-claude-config.sh

BACKUP_DIR=~/.claude-backups

# List available backups
echo "Available backups:"
ls -lt "$BACKUP_DIR"/*.tar.gz | head -10

# Select backup
read -p "Enter backup filename: " BACKUP

# Restore
tar -xzf "$BACKUP_DIR/$BACKUP" -C /

echo "Restored from $BACKUP"
```

### Version Control Settings

```bash
# Add Claude settings to git (if appropriate)
git add .claude/settings.json
git add .mcp.json

# Exclude local settings
echo ".claude/settings.local.json" >> .gitignore
echo ".claude/.credentials.json" >> .gitignore
```
