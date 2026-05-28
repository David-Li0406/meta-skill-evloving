# Troubleshooting Development

Solutions for common development issues with the Requirements Framework.

## Test Failures

### Tests Pass in Repo But Fail When Deployed

**Symptoms**: Tests work when run from repo, fail from deployed location.

**Causes**:
1. Files not synced properly
2. Import path differences
3. Missing library files

**Solution**:
```bash
# 1. Check sync status
cd ~/Tools/claude-requirements-framework
./sync.sh status

# 2. Deploy if needed
./sync.sh deploy

# 3. Check file permissions
ls -la ~/.claude/hooks/*.py
chmod +x ~/.claude/hooks/*.py

# 4. Run tests from deployed location
python3 ~/.claude/hooks/test_requirements.py
```

### Import Errors

**Symptoms**: `ModuleNotFoundError: No module named 'lib.something'`

**Solution**:
```bash
# Check lib directory exists
ls ~/.claude/hooks/lib/

# Check specific module
ls ~/.claude/hooks/lib/requirements.py

# Verify sync
./sync.sh status

# Re-deploy if missing
./sync.sh deploy
```

### Test Database Issues

**Symptoms**: Tests fail due to state file conflicts.

**Solution**:
```bash
# Clean test artifacts
rm -rf /tmp/test-requirements-*

# Run tests fresh
python3 ~/.claude/hooks/test_requirements.py
```

---

## Hook Not Working

### Hook Not Triggering

**Check 1: Hook Registration**
```bash
# View registered hooks
cat ~/.claude/settings.local.json | jq '.hooks'

# Should show:
# {
#   "PreToolUse": "~/.claude/hooks/check-requirements.py",
#   "SessionStart": "~/.claude/hooks/handle-session-start.py",
#   ...
# }
```

**Check 2: File Exists**
```bash
ls -la ~/.claude/hooks/check-requirements.py
```

**Check 3: File Executable**
```bash
# Check permissions
ls -la ~/.claude/hooks/*.py

# Fix if needed
chmod +x ~/.claude/hooks/*.py
```

**Check 4: Python Syntax**
```bash
python3 -m py_compile ~/.claude/hooks/check-requirements.py
```

### Hook Errors Not Visible

**Symptoms**: Hook seems to do nothing, no errors shown.

**Solution**:
```bash
# Enable debug logging
req logging --level debug --local

# View logs
tail -f ~/.claude/requirements.log

# Run test to trigger hook
# Then check log output
```

---

## Sync Issues

### sync.sh Shows Differences After Deploy

**Symptoms**: After running `./sync.sh deploy`, status still shows differences.

**Causes**:
1. File modified during deploy
2. Line ending differences
3. Permission differences

**Solution**:
```bash
# Check exact differences
./sync.sh diff

# Force fresh deploy
rm -f ~/.claude/hooks/problematic-file.py
./sync.sh deploy

# Verify
./sync.sh status
```

### Files Missing in Deployed

**Symptoms**: New file exists in repo but not in deployed.

**Causes**:
1. File not in sync.sh patterns
2. File path incorrect

**Solution**:
```bash
# Check sync.sh patterns
grep "your_file" ~/Tools/claude-requirements-framework/sync.sh

# If not listed, add to sync.sh or copy manually
cp hooks/your_new_file.py ~/.claude/hooks/

# Then deploy to maintain consistency
./sync.sh deploy
```

---

## Git Issues

### Detached HEAD

**Symptoms**: Git shows "detached HEAD" state.

**Solution**:
```bash
# Return to master
git checkout master

# If you have changes, stash first
git stash
git checkout master
git stash pop
```

### Merge Conflicts

**Symptoms**: `git pull` fails with conflicts.

**Solution**:
```bash
# Stash local changes
git stash

# Pull remote
git pull origin master

# Reapply changes
git stash pop

# Manually resolve conflicts
# Files will be marked with <<<<< ===== >>>>>

# After resolving
git add .
git commit -m "merge: resolve conflicts"

# Deploy resolved version
./sync.sh deploy
```

### Accidentally Committed to Wrong Branch

**Solution**:
```bash
# Save commit hash
git log -1 --format="%H"

# Switch to correct branch
git checkout correct-branch

# Cherry-pick the commit
git cherry-pick <commit-hash>

# Remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1

# Deploy from correct branch
git checkout correct-branch
./sync.sh deploy
```

---

## Performance Issues

### Hooks Running Slowly

**Symptoms**: Claude operations feel sluggish.

**Causes**:
1. Calculation cache disabled
2. Too many file operations
3. Complex regex patterns

**Solution**:
```bash
# Check cache configuration
req config branch_size_limit

# Ensure caching enabled
# calculation_cache_ttl: 30  (seconds)

# Check log for slow operations
grep "slow\|timeout\|delay" ~/.claude/requirements.log
```

### Tests Running Slowly

**Symptoms**: Test suite takes longer than expected.

**Solution**:
```bash
# Run specific test categories
python3 ~/.claude/hooks/test_requirements.py -k "test_session"

# Skip slow tests during development
python3 ~/.claude/hooks/test_requirements.py -k "not slow"
```

---

## Development Environment

### Python Version Issues

**Symptoms**: Syntax errors or missing features.

**Required**: Python 3.9+

**Check**:
```bash
python3 --version

# Should be 3.9 or higher
# If lower, use pyenv or update system Python
```

### Editor Not Recognizing Types

**Symptoms**: IDE shows type errors that don't affect runtime.

**Solution**:
```bash
# Ensure type stubs installed (if using strict typing)
pip install types-PyYAML

# Configure IDE to use correct Python interpreter
which python3
# Use this path in IDE settings
```

---

## Recovery Procedures

### Complete Reset

If everything is broken:

```bash
# 1. Backup any local changes
cp -r ~/.claude/hooks ~/.claude/hooks.backup

# 2. Clean deployed location
rm -rf ~/.claude/hooks

# 3. Re-run installation
cd ~/Tools/claude-requirements-framework
./install.sh

# 4. Deploy fresh
./sync.sh deploy

# 5. Verify
python3 ~/.claude/hooks/test_requirements.py
```

### Revert to Previous Version

```bash
cd ~/Tools/claude-requirements-framework

# See recent commits
git log --oneline -10

# Revert to specific commit
git checkout <commit-hash>

# Deploy that version
./sync.sh deploy

# Test
python3 ~/.claude/hooks/test_requirements.py

# Return to latest when done
git checkout master
./sync.sh deploy
```

---

## Debugging Tips

### Add Debug Logging

```python
# In any hook or library file
from lib.logger import logger

logger.debug("Variable value", extra={"variable": value})
```

### View Logs in Real-Time

```bash
# Terminal 1: Tail logs
tail -f ~/.claude/requirements.log

# Terminal 2: Work in Claude Code
# Logs appear in Terminal 1
```

### Run Hook Manually

```python
# Create test input
import json
test_input = {
    "tool_name": "Edit",
    "tool_input": {"file_path": "/test/file.py"},
    "session_id": "test123"
}

# Import and test
import sys
sys.path.insert(0, "/Users/harm/.claude/hooks")
from check_requirements import main
result = main(test_input)
print(json.dumps(result, indent=2))
```
