# Debugging Guide for Hooks

Comprehensive troubleshooting and testing strategies for Claude Code hooks.

## Verification Tools

### Check Hook Registration

Use the `/hooks` command in Claude Code to see all registered hooks:

```
/hooks
```

**Expected Output**:
```
Registered Hooks:
- PreToolUse (Write): .claude/hooks/pre-write.sh
- PostToolUse (Write|Edit): .claude/hooks/report-tracker.py
- SessionStart: .claude/hooks/session-start.sh
```

**What to Check**:
- Hook appears in the list
- Correct event type (PreToolUse, PostToolUse, etc.)
- Correct matcher if applicable
- Script path is correct

### Enable Debug Mode

Run Claude Code with debug flag for detailed hook execution logs:

```bash
claude --debug
```

**Debug Output Includes**:
- Hook loading at startup
- Hook triggering events
- Hook execution time
- Hook output and exit codes
- Hook errors and failures

### Validate JSON Configuration

Check settings file for valid JSON:

```bash
# Validate JSON syntax
python -m json.tool .claude/settings.json

# Or use jq
jq . .claude/settings.json
```

**Common Errors**:
- Missing commas
- Trailing commas
- Unmatched brackets
- Unquoted keys
- Incorrect escape sequences

## Common Issues and Solutions

### Issue: Hook Not Loading

**Symptoms**:
- Hook doesn't appear in `/hooks` output
- No errors visible

**Diagnostic Steps**:
1. Check JSON syntax in settings file
2. Verify file location (correct settings.json)
3. Confirm file named exactly `SKILL.md` for skills
4. Check YAML frontmatter for hooks
5. Restart Claude Code

**Solutions**:

**Problem: Invalid JSON**
```bash
# Check syntax
python -m json.tool .claude/settings.json
```
Fix syntax errors (missing commas, brackets, etc.)

**Problem: Wrong file location**
- User hooks: `~/.claude/settings.json`
- Project hooks: `.claude/settings.json` (relative to project root)
- Local hooks: `.claude/settings.local.json`

**Problem: YAML errors in skills**
```yaml
# BAD: Missing closing delimiter
---
name: skill-name
description: Description here

# GOOD: Proper delimiters
---
name: skill-name
description: Description here
---
```

**Problem: Needs restart**
- Claude Code loads hooks at startup
- Changes require restart to take effect
- Run: `claude restart` or restart the application

### Issue: Hook Not Activating

**Symptoms**:
- Hook appears in `/hooks` but doesn't trigger
- No output or errors when expected

**Diagnostic Steps**:
1. Verify matcher matches the tool being used
2. Check if script is executable
3. Test script independently
4. Review debug logs
5. Confirm hook event type is correct

**Solutions**:

**Problem: Matcher doesn't match tool**
```json
// BAD: Typo in tool name
"matcher": "Writes"  // Should be "Write"

// GOOD: Correct tool name
"matcher": "Write"
```

**Problem: Script not executable**
```bash
# Check permissions
ls -l .claude/hooks/script.sh
# Output: -rw-r--r-- (not executable)

# Fix: Add execute permission
chmod +x .claude/hooks/script.sh

# Verify
ls -l .claude/hooks/script.sh
# Output: -rwxr-xr-x (executable)
```

**Problem: Wrong hook event type**
- PreToolUse: Before tool execution
- PostToolUse: After tool execution
- SessionStart: Only at session start
- etc.

Confirm you're using the right event for your use case.

### Issue: Hook Executes But Doesn't Block (PreToolUse)

**Symptoms**:
- PreToolUse hook runs
- Output appears
- But operation isn't blocked

**Solution**: Use exit code 2 to block:

```bash
# BAD: Exits with 0 (allows operation)
echo "Blocking this operation" >&2
exit 0

# GOOD: Exits with 2 (blocks operation)
echo "Blocking this operation" >&2
exit 2
```

**Note**: PostToolUse hooks cannot block operations (tool already executed).

### Issue: Script Fails Silently

**Symptoms**:
- Hook activates
- No output or errors
- Operation proceeds normally

**Diagnostic Steps**:
1. Run script manually with test input
2. Check for syntax errors
3. Add debug output
4. Check error handling

**Solutions**:

**Add Debug Output**:
```bash
#!/bin/bash
set -e

echo "Hook started" >&2  # Debug message

INPUT=$(cat)
echo "Received input: $INPUT" >&2  # Debug: show input

# ... rest of script
```

```python
#!/usr/bin/env python3
import sys

print("Hook started", file=sys.stderr)

input_data = json.load(sys.stdin)
print(f"Received: {input_data}", file=sys.stderr)

# ... rest of script
```

**Check Error Handling**:
```python
# BAD: Errors suppressed
try:
    # logic here
except:
    pass  # Silent failure

# GOOD: Errors logged
try:
    # logic here
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(0)
```

### Issue: Timeout Errors

**Symptoms**:
- Hook starts but doesn't complete
- Timeout error in logs
- Operation blocked or delayed

**Solutions**:

**Increase Timeout**:
```json
{
  "type": "command",
  "command": "/path/to/slow-script.sh",
  "timeout": 120000  // 120 seconds instead of default 60
}
```

**Optimize Script**:
- Remove unnecessary operations
- Use more efficient algorithms
- Avoid network calls if possible
- Cache results when appropriate

**Make Async** (if appropriate):
- Run logging asynchronously
- Don't block on non-critical operations

### Issue: Path Not Found

**Symptoms**:
- Script not found error
- File not found in hook script

**Solutions**:

**Use Environment Variables**:
```json
// BAD: Absolute path (not portable)
"command": "/home/user/project/.claude/hooks/script.sh"

// GOOD: Use environment variable
"command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
```

**Use Forward Slashes** (cross-platform):
```json
// BAD: Windows backslashes
"command": ".claude\\hooks\\script.sh"

// GOOD: Forward slashes (works everywhere)
"command": ".claude/hooks/script.sh"
```

**Check Working Directory**:
```bash
# In hook script
echo "Working directory: $(pwd)" >&2
```

### Issue: JSON Parsing Errors

**Symptoms**:
- Hook fails with JSON errors
- Cannot parse input

**Solutions**:

**Bash: Better JSON Parsing**:
```bash
# If jq is available (better)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')

# Fallback: basic parsing
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)

# Handle missing fields
if [[ -z "$TOOL_NAME" ]]; then
  echo "tool_name not found in input" >&2
  exit 0
fi
```

**Python: Safe Parsing**:
```python
# Use .get() with defaults
tool_name = input_data.get("tool_name", "")
if not tool_name:
    print("tool_name not found", file=sys.stderr)
    sys.exit(0)

# Safe nested access
file_path = input_data.get("tool_input", {}).get("file_path", "")
```

## Testing Strategies

### Test Hook Script Independently

Create test input and run script directly:

**Bash Script Test**:
```bash
# Create test input
cat > test-input.json <<EOF
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/test/file.txt",
    "content": "test content"
  }
}
EOF

# Run hook with test input
cat test-input.json | .claude/hooks/pre-write.sh

# Check exit code
echo "Exit code: $?"
```

**Python Script Test**:
```bash
# Create test input
echo '{"tool_name":"Write","tool_input":{"file_path":"/test.txt"}}' | python3 .claude/hooks/script.py

# Check exit code
echo "Exit code: $?"
```

### Test With Various Inputs

**Test Missing Fields**:
```json
{"tool_name": "Write"}  // No tool_input
```

**Test Empty Values**:
```json
{"tool_name": "", "tool_input": {"file_path": ""}}
```

**Test Malicious Input**:
```json
{"tool_name": "Write", "tool_input": {"file_path": "../../../etc/passwd"}}
```

**Test Special Characters**:
```json
{"tool_name": "Bash", "tool_input": {"command": "rm -rf /; echo 'hacked'"}}
```

### Test Hook Integration

**Trigger Hook Intentionally**:
1. Start Claude Code with hook registered
2. Use tool that should trigger hook
3. Observe behavior
4. Check output and logs

**Example**: Testing Pre-Write Hook
```
User: Write "test content" to test.txt
Claude: [Uses Write tool]
[Hook should activate and show warning if test.txt is protected]
```

### Test Edge Cases

- Empty files
- Very large files
- Special characters in paths
- Concurrent hook executions
- Rapid successive triggers
- Network timeouts (if applicable)

## Debugging Techniques

### Add Verbose Logging

**Temporary Debug Mode**:
```bash
#!/bin/bash
set -x  # Print each command before execution
set -e

# ... rest of script
```

**Structured Logging**:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('/tmp/hook-debug.log')]
)

logging.debug(f"Hook started with input: {input_data}")
```

### Capture Full Input

Save input to file for inspection:

```bash
#!/bin/bash
INPUT=$(cat)

# Save for debugging
echo "$INPUT" > /tmp/hook-input-$(date +%s).json

# Continue with script...
```

### Test Exit Codes

```bash
# Test different scenarios
.claude/hooks/script.sh < normal-input.json
echo "Normal: $?"

.claude/hooks/script.sh < malicious-input.json
echo "Malicious: $?"

.claude/hooks/script.sh < empty-input.json
echo "Empty: $?"
```

### Trace Execution

**Bash**:
```bash
# Run with tracing
bash -x .claude/hooks/script.sh < test-input.json
```

**Python**:
```bash
# Run with verbose output
python3 -v .claude/hooks/script.py < test-input.json
```

## Performance Debugging

### Measure Execution Time

**In Script**:
```bash
#!/bin/bash
START=$(date +%s%N)

# ... hook logic ...

END=$(date +%s%N)
DURATION=$((($END - $START) / 1000000))
echo "Hook execution time: ${DURATION}ms" >&2
```

```python
import time

start = time.time()

# ... hook logic ...

duration = (time.time() - start) * 1000
print(f"Hook execution time: {duration:.2f}ms", file=sys.stderr)
```

### Profile Slow Hooks

**Python**:
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... hook logic ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest operations
```

### Identify Bottlenecks

- Network requests (use timeouts)
- File I/O (especially on network drives)
- Complex regex patterns
- Large data processing
- Subprocess calls

## Common Error Messages

### "Hook not found"

**Cause**: Script path incorrect or file doesn't exist

**Fix**: Verify path in settings.json and check file exists

### "Permission denied"

**Cause**: Script not executable

**Fix**: `chmod +x .claude/hooks/script.sh`

### "Command not found"

**Cause**: Script uses command not in PATH

**Fix**: Use absolute paths or ensure commands available

### "JSON decode error"

**Cause**: Invalid JSON in input or output

**Fix**: Validate JSON syntax, handle parsing errors

### "Timeout exceeded"

**Cause**: Script takes too long

**Fix**: Increase timeout or optimize script

## Debug Checklist

When debugging a hook issue:

- [ ] Hook appears in `/hooks` output
- [ ] JSON configuration is valid
- [ ] Script file exists at correct path
- [ ] Script has execute permissions (`chmod +x`)
- [ ] Script has correct shebang line
- [ ] Matcher correctly targets intended tools
- [ ] Hook event type appropriate for use case
- [ ] Script runs successfully with test input
- [ ] Exit codes used correctly (0 = allow, 2 = block)
- [ ] Error messages helpful and visible
- [ ] Script doesn't timeout
- [ ] Security validation passed
- [ ] Debug mode enabled for detailed logs
- [ ] Tested with various inputs including edge cases

## Getting Help

If issues persist:

1. **Review Documentation**: Check official Claude Code hooks documentation
2. **Check Examples**: Compare with working examples from cookbooks
3. **Simplify**: Create minimal reproduction case
4. **Community**: Ask in Claude Code community forums
5. **Support**: Contact Anthropic support with debug logs

## Debugging Tools

**Useful Commands**:
```bash
# Validate JSON
python -m json.tool settings.json

# Check file permissions
ls -la .claude/hooks/

# Test script syntax (bash)
bash -n script.sh

# Test script syntax (python)
python3 -m py_compile script.py

# Watch hook directory
watch -n 1 'ls -la .claude/hooks/'

# Monitor logs
tail -f ~/.claude/logs/debug.log  # If applicable
```

**Useful Tools**:
- `jq`: JSON parsing and manipulation
- `shellcheck`: Bash script linting
- `pylint`: Python code linting
- `strace`: System call tracing (advanced)
