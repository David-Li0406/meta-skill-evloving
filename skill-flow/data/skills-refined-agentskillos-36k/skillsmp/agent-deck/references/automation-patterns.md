# Automation Patterns

## Sub-Agent Script (Primary)

```bash
# Fire and forget (recommended)
scripts/launch-subagent.sh "Research" "Find info about X" --mcp exa

# With blocking wait
scripts/launch-subagent.sh "Query" "Answer Y" --wait --timeout 120

# Multiple MCPs
scripts/launch-subagent.sh "Deep Research" "Analyze Z" --mcp exa --mcp firecrawl
```

## Manual Sub-Agent Pattern

When script unavailable:

```bash
PARENT=$(agent-deck session current -q)
PROFILE=$(agent-deck session current --json | jq -r '.profile')

agent-deck -p "$PROFILE" add -t "Task" --parent "$PARENT" -c claude /tmp/task
agent-deck -p "$PROFILE" session start "Task"
sleep 10  # Wait for Claude readiness
agent-deck -p "$PROFILE" session send "Task" "Your prompt"
```

## Check Output

```bash
# Check status
agent-deck session show "Task" | grep Status

# Get response when waiting (◐)
agent-deck session output "Task"
```

## Batch Operations

```bash
# Start multiple sessions
for name in api frontend backend; do
  agent-deck session start "$name"
done

# Attach MCPs to multiple sessions
for session in proj1 proj2; do
  agent-deck mcp attach "$session" exa
  agent-deck session restart "$session"
done
```

## JSON Scripting

```bash
# Get all waiting sessions
agent-deck list --json | jq -r '.[] | select(.status == "waiting") | .title'

# Count by status
agent-deck status --json | jq '.running, .waiting, .idle'
```

## Warnings

1. **Avoid external polling agents** - They can send messages that interfere with target sessions
2. **Use on-demand checks** - Let user request output when ready
3. **Flags before arguments** - `session show --json name` not `session show name --json`
