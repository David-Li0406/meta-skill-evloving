# Troubleshooting Guide

Solutions for common Requirements Framework issues.

## Quick Diagnostics

Run these commands first:

```bash
req doctor          # Comprehensive diagnostics
req verify          # Quick installation check
req status          # Current requirement status
req sessions        # Active sessions
```

---

## Hook Not Triggering

### Symptoms
- Requirements not blocking Edit/Write
- No error messages appearing
- Hook seems inactive

### Checklist

1. **On main/master branch?**
   - By design, some configurations skip these branches
   - Check if `protected_branch` guard is configured

2. **Config enabled?**
   ```bash
   cat .claude/requirements.yaml | grep enabled
   # Should show: enabled: true
   ```

3. **Specific requirement enabled?**
   ```bash
   req config commit_plan
   # Check: enabled: true
   ```

4. **Hook registered?**
   ```bash
   cat ~/.claude/settings.local.json | grep PreToolUse
   # Should show hook path
   ```

   Expected in `~/.claude/settings.local.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": "~/.claude/hooks/check-requirements.py"
     }
   }
   ```

5. **Wildcard permissions?**
   - Check if `Edit(*)` or `Write(*)` in `permissions.allow`
   - These bypass hooks entirely

6. **Skip flag set?**
   ```bash
   echo $CLAUDE_SKIP_REQUIREMENTS
   # Should be empty or not set
   ```

### Resolution

```bash
# Re-register hooks
req doctor

# Check hook file permissions
ls -la ~/.claude/hooks/check-requirements.py
# Should be executable: -rwx------

# Make executable if needed
chmod +x ~/.claude/hooks/*.py
```

---

## Session Not Found

### Symptoms
- `req satisfy` fails with "session not found"
- CLI can't auto-detect session

### Causes
- Running from terminal outside Claude session
- Session registry out of sync
- Stale session entries

### Resolution

```bash
# List active sessions
req sessions

# Use explicit session ID
req satisfy commit_plan --session <id-from-above>

# Clean stale sessions
req prune

# Check session registry
cat ~/.claude/sessions.json
```

---

## Sync Issues

### Symptoms
- Changes to framework not taking effect
- Different behavior than expected
- `req doctor` shows sync warnings

### Check Status

```bash
cd ~/Tools/claude-requirements-framework
./sync.sh status
```

### Resolution

```bash
# Deploy latest from repository
./sync.sh deploy

# View differences
./sync.sh diff
```

---

## Permission Denied

### Symptoms
- Requirement blocking file modifications
- Can't proceed with edits

### Resolution

```bash
# Check which requirement is blocking
req status

# Satisfy the requirement
req satisfy <requirement_name>

# Or temporarily disable
req config <requirement_name> --disable --local
```

---

## Tests Failing

### Symptoms
- `python3 ~/.claude/hooks/test_requirements.py` fails
- Tests pass in repo but fail when deployed

### Debugging

```bash
# Run with verbose output
python3 ~/.claude/hooks/test_requirements.py -v

# Check file permissions
ls -la ~/.claude/hooks/check-requirements.py

# Check imports
python3 -c "import sys; sys.path.insert(0, '/Users/$USER/.claude/hooks'); from lib.requirements import BranchRequirements"

# Check for missing files
cd ~/Tools/claude-requirements-framework
./sync.sh status
```

### Common Causes

1. **Permission issues** - Files not executable
2. **Missing files** - Sync incomplete
3. **Import errors** - lib/ modules not deployed
4. **Python version** - Requires 3.9+

---

## Error Messages Explained

### "No commit plan found for this session"

**Cause**: `commit_plan` requirement enabled but not satisfied

**Solution**:
1. Create a commit plan (use EnterPlanMode)
2. Run: `req satisfy commit_plan`

### "Session not found"

**Cause**: CLI can't auto-detect current session

**Solution**:
```bash
req sessions                  # Find session ID
req satisfy commit_plan --session <id>
```

### "Cannot edit files on protected branch"

**Cause**: Guard requirement blocking edits on main/master

**Solution**:
```bash
# Create feature branch
git checkout -b feature/your-feature

# Or emergency override (temporary)
req approve protected_branch
```

### "Branch has X changes (threshold: Y)"

**Cause**: Dynamic branch size limit exceeded

**Solution**:
- Split work into smaller PRs
- Or temporarily increase threshold:
  ```bash
  req config branch_size_limit --set threshold=600 --local
  ```

---

## Temporarily Disabling Requirements

### Option 1: Local Override (per project)

```yaml
# .claude/requirements.local.yaml
enabled: false
```

### Option 2: Environment Variable

```bash
export CLAUDE_SKIP_REQUIREMENTS=1
```

### Option 3: Disable Specific Requirement

```bash
req config commit_plan --disable --local
```

---

## Configuration Not Loading

### Symptoms
- Changes to `.claude/requirements.yaml` ignored
- Default settings used instead

### Debugging

```bash
# Check config files exist
ls -la .claude/requirements.yaml
ls -la .claude/requirements.local.yaml
ls -la ~/.claude/requirements.yaml

# View effective config
req config

# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.claude/requirements.yaml'))"
```

### Common Causes

1. **YAML syntax errors** - Invalid indentation or formatting
2. **Wrong location** - File not in `.claude/` directory
3. **Inheritance issues** - `inherit: false` blocking global config

---

## Report Issues

If problems persist:

1. Run `req doctor` and capture output
2. Check logs: `tail -50 ~/.claude/requirements.log`
3. Check test suite: `python3 ~/.claude/hooks/test_requirements.py`
4. Report at: https://github.com/HarmAalbers/claude-requirements-framework/issues

Include:
- `req doctor` output
- Relevant log entries
- Steps to reproduce
- Expected vs actual behavior
