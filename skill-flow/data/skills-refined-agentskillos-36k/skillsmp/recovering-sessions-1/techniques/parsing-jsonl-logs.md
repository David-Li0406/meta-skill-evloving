# Parsing JSONL Agent Logs

Techniques for extracting actionable information from Claude Code agent conversation logs.

## Log Format

Each agent log is a JSONL file (JSON Lines format) where each line is a complete JSON object:

```json
{
  "message": {
    "role": "assistant",
    "content": [
      {"type": "tool_use", "name": "Write", "input": {"file_path": "..."}},
      {"type": "text", "text": "..."}
    ]
  }
}
```

### Content Block Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `text` | Assistant's text output | `text` |
| `tool_use` | Tool invocation | `name`, `input` |
| `tool_result` | Tool execution result | `content` |

## Extraction Patterns

### Files Created (Write tool)

```bash
# Extract all file paths from Write tool calls
grep -o '"name":"Write"[^}]*"file_path":"[^"]*"' agent.jsonl | \
  grep -o '"file_path":"[^"]*"' | \
  sed 's/"file_path":"//;s/"//' | \
  sort -u
```

### Files Modified (Edit tool)

```bash
# Extract file paths from Edit tool calls
grep -o '"name":"Edit"[^}]*"file_path":"[^"]*"' agent.jsonl | \
  grep -o '"file_path":"[^"]*"' | \
  sed 's/"file_path":"//;s/"//' | \
  sort -u
```

### All File Operations

```bash
# Combined file operations (Write + Edit)
grep -E '"name":"(Write|Edit)"' agent.jsonl | \
  grep -o '"file_path":"[^"]*"' | \
  sed 's/"file_path":"//;s/"//' | \
  sort -u
```

### Test Results

```bash
# Find test result lines
grep -iE 'passed|failed|PASSED|FAILED' agent.jsonl

# Extract test counts
grep -oE '[0-9]+ (passed|failed)' agent.jsonl | sort -u

# Detailed test output
grep -E 'test.*passed|test.*failed|pytest|jest' agent.jsonl
```

### Error Messages

```bash
# Find error indicators
grep -iE 'error|failed|exception|traceback' agent.jsonl

# Python tracebacks
grep -i 'traceback\|exception' agent.jsonl

# JavaScript errors
grep -i 'error:\|TypeError\|ReferenceError' agent.jsonl
```

### Completion Markers

```bash
# Success indicators in final messages
tail -10 agent.jsonl | grep -iE 'complete|success|finished|done'

# Check if task completed
tail -5 agent.jsonl | grep -q 'successfully' && echo "COMPLETE" || echo "UNKNOWN"
```

## Using jq for Advanced Parsing

### Extract All Tool Uses

```bash
# List all tools used
jq -r '.message.content[]? | select(.type == "tool_use") | .name' agent.jsonl | sort | uniq -c

# Get tool use count
jq -r '.message.content[]? | select(.type == "tool_use") | .name' agent.jsonl | wc -l
```

### Extract File Paths by Tool

```bash
# Write tool file paths
jq -r '.message.content[]? | select(.type == "tool_use" and .name == "Write") | .input.file_path' agent.jsonl

# Edit tool file paths
jq -r '.message.content[]? | select(.type == "tool_use" and .name == "Edit") | .input.file_path' agent.jsonl
```

### Get Last N Messages

```bash
# Last 5 assistant messages
tail -10 agent.jsonl | jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' | tail -5
```

### Extract Specific Content

```bash
# Find Bash commands executed
jq -r '.message.content[]? | select(.type == "tool_use" and .name == "Bash") | .input.command' agent.jsonl

# Find file contents written
jq -r '.message.content[]? | select(.type == "tool_use" and .name == "Write") | .input.content' agent.jsonl
```

## Status Determination

### Status Assessment Script

```bash
#!/bin/bash
# Determine agent completion status
LOG_FILE="$1"

# Check for completion markers
if tail -10 "$LOG_FILE" | grep -qiE 'complete|successfully|finished'; then
    echo "COMPLETE"
    exit 0
fi

# Check for errors in final lines
if tail -10 "$LOG_FILE" | grep -qiE 'error|failed|exception'; then
    echo "FAILED"
    exit 0
fi

# Check for substantial activity
LINE_COUNT=$(wc -l < "$LOG_FILE")
FILE_SIZE=$(stat -f "%z" "$LOG_FILE")

if [ "$LINE_COUNT" -gt 50 ] && [ "$FILE_SIZE" -gt 10000 ]; then
    # Large file without completion marker = likely crashed
    echo "IN_PROGRESS"
    exit 0
fi

if [ "$LINE_COUNT" -lt 10 ]; then
    echo "NOT_STARTED"
    exit 0
fi

echo "UNKNOWN"
```

### Status Logic

```
COMPLETE: Log contains success markers in final messages
FAILED: Log contains unhandled errors in final lines
IN_PROGRESS: Large log, no completion marker (crashed mid-task)
NOT_STARTED: Small log with no file operations
UNKNOWN: Requires manual review
```

## Analysis Summary Script

```bash
#!/bin/bash
# Generate summary for a single agent log

LOG_FILE="$1"
AGENT_ID=$(basename "$LOG_FILE" | sed 's/agent-\(.*\)\.jsonl/\1/')

echo "=== Agent $AGENT_ID ==="

# Basic stats
echo "Lines: $(wc -l < "$LOG_FILE")"
echo "Size: $(stat -f "%z" "$LOG_FILE") bytes"
echo "Modified: $(stat -f "%Sm" "$LOG_FILE")"

# Files created
echo ""
echo "Files Created:"
grep -o '"name":"Write"[^}]*"file_path":"[^"]*"' "$LOG_FILE" | \
  grep -o '"file_path":"[^"]*"' | \
  sed 's/"file_path":"//;s/"//' | \
  sort -u | \
  sed 's/^/  /'

# Files modified
echo ""
echo "Files Modified:"
grep -o '"name":"Edit"[^}]*"file_path":"[^"]*"' "$LOG_FILE" | \
  grep -o '"file_path":"[^"]*"' | \
  sed 's/"file_path":"//;s/"//' | \
  sort -u | \
  sed 's/^/  /'

# Test results
echo ""
echo "Test Results:"
grep -oE '[0-9]+ (passed|failed)' "$LOG_FILE" | tail -1 || echo "  No test results found"

# Status
echo ""
echo "Status: $(
  if tail -10 "$LOG_FILE" | grep -qiE 'complete|successfully'; then
    echo "COMPLETE"
  elif tail -10 "$LOG_FILE" | grep -qiE 'error|failed|exception'; then
    echo "FAILED"
  else
    echo "UNKNOWN"
  fi
)"
```

## Node.js Analysis

For programmatic analysis, use `../scripts/analyze-agent-log.js`:

```javascript
import { readFile } from 'fs/promises';

async function analyzeLog(logPath) {
  const content = await readFile(logPath, 'utf-8');
  const lines = content.trim().split('\n');

  const result = {
    totalMessages: lines.length,
    filesCreated: new Set(),
    filesModified: new Set(),
    testResults: null,
    status: 'UNKNOWN',
    errors: []
  };

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const content = entry.message?.content || [];

      for (const block of content) {
        if (block.type === 'tool_use') {
          if (block.name === 'Write' && block.input?.file_path) {
            result.filesCreated.add(block.input.file_path);
          }
          if (block.name === 'Edit' && block.input?.file_path) {
            result.filesModified.add(block.input.file_path);
          }
        }
      }
    } catch (e) {
      // Skip malformed lines
    }
  }

  return result;
}
```

## Common Patterns

### Find Task ID in Log

```bash
# Look for task references
grep -oE 'TASK-[0-9]+\.[0-9]+' agent.jsonl | head -1

# Look for phase references
grep -oE 'Phase [0-9]+' agent.jsonl | head -1
```

### Find Component Name

```bash
# React component names
grep -oE 'function [A-Z][a-zA-Z]+|const [A-Z][a-zA-Z]+ =' agent.jsonl | head -5

# Python class names
grep -oE 'class [A-Z][a-zA-Z]+' agent.jsonl | head -5
```

### Find Test Coverage

```bash
# Jest coverage
grep -oE '[0-9]+%.*coverage|coverage.*[0-9]+%' agent.jsonl

# Pytest coverage
grep -oE 'TOTAL.*[0-9]+%|[0-9]+% coverage' agent.jsonl
```

## Troubleshooting

### Malformed JSON Lines

Some lines may be incomplete (from crash):

```bash
# Validate each line
while read line; do
  echo "$line" | jq . > /dev/null 2>&1 || echo "Invalid: $line"
done < agent.jsonl
```

### Large Log Files

For very large logs, use streaming:

```bash
# Process line by line (memory efficient)
head -1000 agent.jsonl | jq -r '...'

# Sample every Nth line
awk 'NR % 10 == 0' agent.jsonl | jq -r '...'
```

### Binary Content

Some tool results contain binary or encoded content:

```bash
# Skip tool_result blocks
jq -r '.message.content[]? | select(.type != "tool_result")' agent.jsonl
```

## Next Steps

After analyzing logs:
1. Verify files exist on disk with `./verifying-on-disk-state.md`
2. Generate recovery report with `./generating-resumption-plans.md`
