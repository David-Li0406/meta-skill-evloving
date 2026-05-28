# Error Handling Reference

This document describes how the reflect plugin handles various error scenarios and provides recovery procedures.

## Overview

The reflect system is designed to gracefully handle errors and provide clear recovery paths. All error conditions follow these principles:

1. **Fail safely**: Never corrupt existing data or state
2. **Provide context**: Explain what went wrong and why
3. **Offer solutions**: Give actionable recovery steps
4. **Log failures**: Record errors for debugging and improvement

---

## Common Error Scenarios

### 1. Context Compression Failure

**When it happens**: Large conversations (>10k tokens) fail to compress via context-manager agent

**Symptoms**:
- context-manager agent times out
- context-manager agent returns error
- Compressed output is empty or malformed

**Automatic Recovery**:
```bash
# Fallback strategy (automatic):
1. Detect compression failure
2. Log warning: "Context compression failed, using full conversation"
3. Proceed with full conversation analysis (may be slower)
4. Continue with reflect workflow
```

**Manual Recovery** (if needed):
```bash
# If full conversation also fails (extremely rare):
1. Break analysis into smaller time windows
2. Run /reflect multiple times on conversation segments
3. Manually combine insights
```

**Prevention**:
- Use context-manager for conversations >10k tokens
- Consider archiving old messages if conversation is extremely long
- Split very long sessions into multiple reflect runs

---

### 2. Git Push Failure

**When it happens**: `reflect-commit-changes.sh` cannot push to remote

**Symptoms**:
- Error: "Push failed"
- Message: "Commit succeeded but push failed"
- Changes are committed locally but not on remote

**Automatic Recovery**:
```bash
# System behavior:
1. Changes are committed locally (safe)
2. Push operation fails
3. User is warned with recovery steps
4. Script exits with error code 1
```

**Manual Recovery**:
```bash
# Option 1: Pull and rebase
cd /path/to/plugin-repo
git pull origin main --rebase
git push origin main

# Option 2: Force push (only if you own the branch)
git push origin main --force-with-lease

# Option 3: Use --pull-first flag next time
reflect-commit-changes.sh skill-name "message" --pull-first
```

**Prevention**:
- Always use `--pull-first` flag when working in shared repositories
- Check git status before running reflect commits
- Coordinate with team when making reflect improvements

---

### 3. Merge Conflicts

**When it happens**: Local skill file conflicts with remote changes

**Symptoms**:
- Pull fails with "merge conflict"
- Git shows conflict markers in skill files
- Cannot push until resolved

**Automatic Recovery**:
```bash
# System behavior:
1. Pull detects conflicts
2. Script exits with detailed conflict resolution steps
3. No changes are committed (safe)
```

**Manual Recovery**:
```bash
# Step 1: Identify conflicts
git status

# Step 2: Resolve conflicts manually
# Open the skill file and look for conflict markers:
# <<<<<<< HEAD
# your changes
# =======
# remote changes
# >>>>>>> origin/main

# Edit the file to combine changes appropriately

# Step 3: Mark as resolved
git add plugins/reflect/skills/[skill-name]/SKILL.md

# Step 4: Complete merge
git commit

# Step 5: Push
git push origin main
```

**Prevention**:
- Use `--pull-first` flag consistently
- Communicate with team before major reflect changes
- Consider using separate branches for experimental reflects

---

### 4. Metrics File Corruption

**When it happens**: `~/.claude/reflect-metrics.jsonl` becomes corrupted

**Symptoms**:
- JSON parsing errors
- Malformed JSONL entries
- reflect-stats.sh shows errors
- Cannot log new proposals

**Automatic Recovery**:
```bash
# System behavior:
1. Detect corruption on next metrics operation
2. Create backup: reflect-metrics.jsonl.backup.[timestamp]
3. Start fresh metrics file
4. Log error for investigation
```

**Manual Recovery**:
```bash
# Option 1: Restore from backup
cd ~/.claude
ls -la reflect-metrics.jsonl.backup.*
# Find most recent backup
cp reflect-metrics.jsonl.backup.[timestamp] reflect-metrics.jsonl

# Option 2: Repair corrupted file
# Open reflect-metrics.jsonl in editor
# Remove malformed lines (they won't have valid JSON syntax)
# Each line should be a complete JSON object like:
# {"type":"proposal","timestamp":"...","skill":"..."}

# Option 3: Start fresh (loses history)
rm ~/.claude/reflect-metrics.jsonl
touch ~/.claude/reflect-metrics.jsonl
```

**Prevention**:
- Ensure disk space available before reflects
- Avoid manually editing metrics file
- Use reflect-track-proposal.sh script for logging
- Regular backups of ~/.claude directory

---

### 5. Skill File Missing

**When it happens**: Requested skill file does not exist

**Symptoms**:
- Error: "Skill file not found"
- reflect-commit-changes.sh cannot find skill
- /reflect [skill-name] fails

**Automatic Recovery**:
```bash
# System behavior:
1. Detect missing skill file
2. List all available skills in error message
3. Suggest correct skill name
4. Exit without making changes
```

**Manual Recovery**:
```bash
# Option 1: Use correct skill name
# Check available skills:
ls -1 ~/.claude/skills/

# Run with correct name:
/reflect [correct-skill-name]

# Option 2: Create new skill (if intentional)
mkdir -p ~/.claude/skills/[new-skill-name]
touch ~/.claude/skills/[new-skill-name]/SKILL.md
# Add skill content
```

**Prevention**:
- Use tab completion for skill names
- Run `/reflect` without args to see available skills
- Check skill spelling before running

---

### 6. Missing Dependencies

**When it happens**: Required tools not available (jq, git, etc.)

**Symptoms**:
- Command not found errors
- Script fails early
- Missing functionality

**Automatic Recovery**:
```bash
# System behavior:
1. Detect missing tool
2. Provide installation instructions
3. Suggest workaround if available
4. Exit gracefully
```

**Manual Recovery**:
```bash
# Install missing tools:

# macOS (Homebrew)
brew install jq git

# Linux (apt)
sudo apt-get install jq git

# Linux (yum)
sudo yum install jq git

# Verify installation
which jq
which git
```

**Prevention**:
- Ensure required tools are installed (jq, git)
- Check system requirements before using reflect
- Use standard Unix/Linux environments

---

### 7. Permission Errors

**When it happens**: Cannot write to ~/.claude directory or git repository

**Symptoms**:
- "Permission denied" errors
- Cannot create pause files
- Cannot write metrics
- Cannot commit changes

**Automatic Recovery**:
```bash
# System behavior:
1. Detect permission error
2. Show exact path that failed
3. Suggest permission fixes
4. Exit without corrupting data
```

**Manual Recovery**:
```bash
# Fix ~/.claude permissions
chmod 755 ~/.claude
chmod 644 ~/.claude/*

# Fix git repository permissions
cd /path/to/plugin-repo
sudo chown -R $USER:$USER .

# Verify git config
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

**Prevention**:
- Ensure ~/.claude is user-writable
- Don't run reflect with sudo
- Check file ownership in git repos

---

### 8. Paused Skill Attempted

**When it happens**: User tries to reflect on auto-paused skill

**Symptoms**:
- Warning: "Skill is currently paused"
- Workflow stops at Step 0
- No analysis performed

**Automatic Recovery**:
```bash
# System behavior:
1. Check for pause file in Step 0
2. Display pause reason and timestamp
3. Show resume command
4. Stop workflow (prevent wasted effort)
```

**Manual Recovery**:
```bash
# Option 1: Resume the skill
/reflect resume [skill-name]

# Option 2: Check why it was paused
/reflect stats [skill-name]
# Review consecutive rejections

# Option 3: Delete pause manually (not recommended)
rm ~/.claude/reflect-paused-skills/[skill-name].paused
```

**Prevention**:
- Review rejection patterns before resuming
- Address underlying issues (signal detection, proposals)
- Use /reflect stats to understand rejection causes

---

### 9. Consecutive Rejections

**When it happens**: User rejects 3+ proposals in a row for same skill

**Symptoms**:
- Auto-pause triggered
- Pause file created
- Warning message displayed

**Automatic Recovery**:
```bash
# System behavior:
1. Count consecutive rejections
2. At 3rd rejection: Create pause file
3. Display detailed pause message
4. Prevent future reflects until resumed
```

**Manual Recovery**:
```bash
# Analyze why rejections are happening
/reflect stats [skill-name]

# Review recent proposals
tail -20 ~/.claude/reflect-metrics.jsonl | grep "skill-name"

# Consider:
- Are proposals too aggressive?
- Is signal detection misinterpreting feedback?
- Does the skill actually need changes?

# When ready, resume
/reflect resume [skill-name]
```

**Prevention**:
- Provide clear feedback in rejections
- Describe desired changes when rejecting
- Use "modify" instead of "reject" when possible
- Review signal-examples.md for guidance

---

## Recovery Workflows

### Complete Metrics Reset

If metrics become irreparably corrupted:

```bash
# 1. Backup existing metrics
cp ~/.claude/reflect-metrics.jsonl ~/.claude/reflect-metrics.jsonl.backup.$(date +%s)

# 2. Create fresh metrics file
cat > ~/.claude/reflect-metrics.jsonl <<EOF
# Reflect Metrics Database (JSONL format)
# Schema: Each line is a JSON object representing an event
# Event types: proposal, outcome
EOF

# 3. Verify it works
/reflect stats reflect
```

### Complete Reflect Reset

If reflect system is in unknown state:

```bash
# 1. Backup all reflect state
mkdir -p ~/.claude-backup-$(date +%s)
cp -r ~/.claude/reflect* ~/.claude-backup-$(date +%s)/

# 2. Clear all state
rm -f ~/.claude/reflect-metrics.jsonl
rm -f ~/.claude/reflect-skill-state.json
rm -rf ~/.claude/reflect-paused-skills

# 3. Reinitialize
touch ~/.claude/reflect-metrics.jsonl
echo '# Reflect Metrics Database' >> ~/.claude/reflect-metrics.jsonl

# 4. Test with a simple reflect
/reflect status
```

---

## Debugging Tips

### Enable Debug Logging

```bash
export DEBUG_REFLECT=1
/reflect [skill-name]
# Logs written to ~/.claude/reflect.log
```

### View Recent Metrics

```bash
# Last 10 events
tail -10 ~/.claude/reflect-metrics.jsonl

# Last 10 proposals only
grep '"type":"proposal"' ~/.claude/reflect-metrics.jsonl | tail -10

# Last 10 for specific skill
grep '"skill":"frontend-design"' ~/.claude/reflect-metrics.jsonl | tail -10
```

### Check Pause Status

```bash
# List all paused skills
ls -la ~/.claude/reflect-paused-skills/

# Read pause details
cat ~/.claude/reflect-paused-skills/[skill-name].paused | jq .
```

### Verify Git State

```bash
cd /path/to/plugin-repo
git status
git log --oneline -5
git diff HEAD
```

---

## Getting Help

If you encounter an error not covered here:

1. **Check logs**: `~/.claude/reflect.log` (if DEBUG_REFLECT=1)
2. **Check metrics**: `tail ~/.claude/reflect-metrics.jsonl`
3. **Check git status**: `git status` in plugin repo
4. **Review this document**: Search for similar error
5. **Create an issue**: Document the error and steps to reproduce

---

## Best Practices

1. **Always use --pull-first** when working in shared repos
2. **Enable debug logging** when troubleshooting: `DEBUG_REFLECT=1`
3. **Backup metrics regularly**: `cp ~/.claude/reflect-metrics.jsonl ~/.claude/reflect-metrics.jsonl.backup`
4. **Review rejections**: Use `/reflect stats [skill]` before resuming paused skills
5. **Use dry-run mode**: Test git operations with `--dry-run` flag first
6. **Check permissions**: Ensure ~/.claude is writable by your user
7. **Keep tools updated**: Ensure jq, git, and other dependencies are up to date

---

## Error Code Reference

| Exit Code | Meaning | Recovery |
|-----------|---------|----------|
| 0 | Success | - |
| 1 | General error | Check error message for details |
| 2 | Invalid arguments | Review command usage |
| 3 | Missing file | Check path, create if needed |
| 4 | Permission error | Fix file/directory permissions |
| 5 | Git operation failed | Review git state, resolve conflicts |
| 127 | Command not found | Install missing dependencies |

---

*This documentation is maintained as part of the reflect plugin. Last updated: 2026-01-17*
