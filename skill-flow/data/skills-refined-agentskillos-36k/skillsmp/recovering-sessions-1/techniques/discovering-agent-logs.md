# Discovering Agent Logs

Techniques for finding Claude Code agent conversation logs after a session crash or interruption.

## Log Location

Agent logs are stored in the Claude Code projects directory:

```
~/.claude/projects/{project-path-with-dashes}/
├── agent-{8-char-id}.jsonl    # Subagent conversation log
├── agent-{8-char-id}.jsonl    # Another subagent
└── ...
```

### Path Derivation

The project path is transformed into a directory name:

```bash
# Project path: /Users/name/dev/my-project
# Log directory: ~/.claude/projects/-Users-name-dev-my-project/

# Derive log directory from current working directory
LOG_DIR="$HOME/.claude/projects/$(pwd | sed 's/\//-/g' | sed 's/^-//')"
```

### JavaScript Path Derivation

```javascript
import { homedir } from 'os';
import { join } from 'path';

function getLogDirectory(projectPath) {
  const sanitized = projectPath.replace(/\//g, '-').replace(/^-/, '');
  return join(homedir(), '.claude/projects', sanitized);
}
```

## Discovery Techniques

### 1. By Recency (Most Common)

Find agents active within a time window:

```bash
# Last 3 hours (180 minutes)
find "$LOG_DIR" -name "agent-*.jsonl" -mmin -180

# Last hour
find "$LOG_DIR" -name "agent-*.jsonl" -mmin -60

# Last 24 hours
find "$LOG_DIR" -name "agent-*.jsonl" -mtime -1
```

### 2. By Known Agent ID

When you have agent IDs from error messages or progress tracking:

```bash
# Single agent
ls "$LOG_DIR" | grep "a91845a"

# Multiple agents
ls "$LOG_DIR" | grep -E "(a91845a|abec615|adad508)"
```

### 3. By File Size

Find substantial logs (active agents create larger logs):

```bash
# Logs larger than 10KB from today
find "$LOG_DIR" -name "*.jsonl" -size +10k -mtime -1

# Logs larger than 50KB (very active agents)
find "$LOG_DIR" -name "*.jsonl" -size +50k

# Sort by size descending
ls -lS "$LOG_DIR"/agent-*.jsonl | head -10
```

### 4. By Modification Time (Sorted)

List agents by most recently modified:

```bash
# List 20 most recent agent logs
ls -lt "$LOG_DIR"/agent-*.jsonl | head -20

# Get just filenames
ls -t "$LOG_DIR"/agent-*.jsonl | head -20

# With detailed timestamps
stat -f "%Sm %N" "$LOG_DIR"/agent-*.jsonl | sort -r | head -20
```

### 5. Combined Filters

Powerful combinations for targeted discovery:

```bash
# Recent AND substantial
find "$LOG_DIR" -name "agent-*.jsonl" -mmin -180 -size +10k

# Today's large logs, sorted by modification time
find "$LOG_DIR" -name "agent-*.jsonl" -mtime -1 -size +10k -exec ls -lt {} + | head -20
```

## Quick Discovery Script

Use `../scripts/find-recent-agents.js` for automated discovery:

```bash
# Find agents from last 3 hours
node find-recent-agents.js --minutes 180

# Find agents with specific project
node find-recent-agents.js --project /Users/name/dev/project
```

## Correlating with Tasks

### From Progress Tracking

If using artifact-tracking skill, progress files may contain agent IDs:

```yaml
# In .claude/progress/[prd]/phase-N-progress.md
session_tracking:
  last_checkpoint: "2025-12-23T10:30:00Z"
  active_agents: ["a91845a", "abec615"]
  batch_in_progress: 2
```

### From Error Messages

Claude Code error messages often include agent IDs:

```
Error in agent a91845a: Context window exceeded
Agent abec615 failed: API rate limit
```

### From Console Output

During execution, agent IDs appear in console:

```
Launching agent a91845a for TASK-2.1...
Agent abec615 starting TASK-2.2...
```

## Understanding Log Structure

Each `.jsonl` file contains one JSON object per line:

```json
{"message":{"role":"user","content":"..."}}
{"message":{"role":"assistant","content":[...]}}
{"message":{"role":"user","content":"..."}}
```

Key fields:
- `message.role`: "user" or "assistant"
- `message.content`: Array of content blocks (text, tool_use, tool_result)

See `./parsing-jsonl-logs.md` for extraction patterns.

## Discovery Workflow

```bash
#!/bin/bash
# Full discovery workflow

# 1. Get project log directory
PROJECT_PATH=$(pwd)
LOG_DIR="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's/\//-/g' | sed 's/^-//')"

# 2. Check if directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "No log directory found at: $LOG_DIR"
    exit 1
fi

# 3. Find recent agent logs
echo "=== Recent Agent Logs (last 3 hours) ==="
RECENT_LOGS=$(find "$LOG_DIR" -name "agent-*.jsonl" -mmin -180)

if [ -z "$RECENT_LOGS" ]; then
    echo "No recent agent logs found"
    exit 0
fi

# 4. Display with details
echo "$RECENT_LOGS" | while read log; do
    AGENT_ID=$(basename "$log" | sed 's/agent-\(.*\)\.jsonl/\1/')
    SIZE=$(stat -f "%z" "$log")
    MTIME=$(stat -f "%Sm" "$log")
    LINES=$(wc -l < "$log")
    echo "  $AGENT_ID: ${SIZE}B, $LINES lines, modified $MTIME"
done
```

## Troubleshooting

### No Logs Found

1. **Check project path**: Ensure you're in the correct directory
2. **Expand time window**: Use `-mmin -360` (6 hours) or `-mtime -2` (2 days)
3. **Check log directory exists**: `ls ~/.claude/projects/`
4. **Verify log directory name**: Path transformation may differ

### Many Logs Found

1. **Filter by size**: Exclude small/empty logs with `-size +10k`
2. **Narrow time window**: Use `-mmin -60` for last hour only
3. **Sort by recency**: `ls -t | head -10` for most recent
4. **Check git status**: Compare log times to git commit times

### Agent ID Not Found

1. **Check error messages**: Agent IDs may appear in crash output
2. **Check progress files**: May be recorded in session_tracking YAML
3. **Use time-based discovery**: Find logs modified around crash time
4. **Check console scrollback**: Agent IDs printed during execution

## Next Steps

After discovering agent logs:
1. Analyze each log with `./parsing-jsonl-logs.md` techniques
2. Verify on-disk state with `./verifying-on-disk-state.md`
3. Generate recovery report with `./generating-resumption-plans.md`
