# Transcript Search Reference

Quick reference for searching Claude Code session transcripts.

---

## Transcript Location

```bash
# Default location
~/.claude/projects/<project-hash>/<session-id>.jsonl

# Find your project hash
ls ~/.claude/projects/

# Example: /Users/me/myproject becomes -Users-me-myproject
```

---

## Basic grep Patterns

### Find User Prompts

```bash
# All user messages
grep '"type":"user"' session.jsonl

# User messages containing a term
grep '"type":"user"' *.jsonl | grep -i "database"

# Case-insensitive search
grep -i '"type":"user"' *.jsonl | grep -i "schema"
```

### Find Assistant Responses

```bash
# All assistant messages
grep '"type":"assistant"' session.jsonl

# Assistant mentions of a topic
grep '"type":"assistant"' *.jsonl | grep -i "migration"
```

### Find Tool Uses

```bash
# All tool invocations
grep '"tool_use"' session.jsonl

# Specific tool
grep '"tool_use"' *.jsonl | grep '"name":"Edit"'
grep '"tool_use"' *.jsonl | grep '"name":"Bash"'
grep '"tool_use"' *.jsonl | grep '"name":"Write"'
grep '"tool_use"' *.jsonl | grep '"name":"Read"'

# Tool results
grep '"tool_result"' session.jsonl
```

### Find Errors

```bash
# Error indicators
grep -i '"is_error":true' session.jsonl
grep -i '"error"' session.jsonl
grep -i 'failed' session.jsonl
grep -i 'exception' session.jsonl
```

---

## jq Patterns (Precise Extraction)

### Extract User Prompts

```bash
# All user prompt text
cat session.jsonl | jq -c 'select(.type == "user") | .message.content'

# User prompts as readable text
cat session.jsonl | jq -r 'select(.type == "user") | .message.content | if type == "array" then .[0].text else . end'
```

### Extract Assistant Responses

```bash
# Text responses only (skip tool calls)
cat session.jsonl | jq -r '
  select(.type == "assistant") |
  .message.content |
  if type == "array" then
    .[] | select(.type == "text") | .text
  else
    .
  end'

# All assistant content (including tool calls)
cat session.jsonl | jq -c 'select(.type == "assistant") | .message.content'
```

### List Tools Used

```bash
# Unique tool names with counts
cat session.jsonl | jq -r '
  select(.message.content | type == "array") |
  .message.content[] |
  select(.type == "tool_use") |
  .name' | sort | uniq -c | sort -rn

# Tool sequence (order of invocation)
cat session.jsonl | jq -r '
  select(.message.content | type == "array") |
  .message.content[] |
  select(.type == "tool_use") |
  .name'
```

### Find Files Modified

```bash
# Files edited or written
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use") |
  select(.name == "Edit" or .name == "Write") |
  .input.file_path' 2>/dev/null | sort -u

# Files read
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use") |
  select(.name == "Read") |
  .input.file_path' 2>/dev/null | sort -u

# All file paths mentioned in tool results
cat session.jsonl | jq -r '
  .toolUseResult.file.filePath //
  .message.content[]?.input.file_path //
  empty' 2>/dev/null | sort -u
```

### Extract Bash Commands

```bash
# All bash commands executed
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use") |
  select(.name == "Bash") |
  .input.command' 2>/dev/null

# Commands with descriptions
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use") |
  select(.name == "Bash") |
  "\(.input.description // "no desc"): \(.input.command)"' 2>/dev/null
```

### Token Usage

```bash
# Usage statistics
cat session.jsonl | jq 'select(.type == "result") | .usage'

# Total input/output tokens
cat session.jsonl | jq -s '
  [.[] | select(.type == "result") | .usage] |
  {
    total_input: (map(.input_tokens) | add),
    total_output: (map(.output_tokens) | add)
  }'
```

---

## Cross-Session Search

### Search All Sessions in Project

```bash
# Set project directory
PROJECT_DIR=~/.claude/projects/-Users-username-project-name

# Find sessions containing a term
grep -l "search term" "$PROJECT_DIR"/*.jsonl

# Search with context (2 lines before/after)
grep -B2 -A2 "search term" "$PROJECT_DIR"/*.jsonl

# Search with filename prefix
grep -H "search term" "$PROJECT_DIR"/*.jsonl
```

### Search by Date

```bash
# Sessions modified today
ls -la ~/.claude/projects/*/*.jsonl | grep "$(date '+%b %e')"

# Sessions from specific date
ls -la ~/.claude/projects/*/*.jsonl | grep "Jan  7"

# Find by timestamp in content
grep "2026-01-07" ~/.claude/projects/*/*.jsonl
```

### Search Recent Sessions

```bash
# Last 5 sessions (by modification time)
ls -t ~/.claude/projects/*/*.jsonl | head -5

# Search only recent sessions
for f in $(ls -t ~/.claude/projects/*/*.jsonl | head -5); do
  echo "=== $f ==="
  grep -i "search term" "$f"
done
```

---

## Common Search Scenarios

### "What did we decide about X?"

```bash
# Decision keywords
grep -i -E "(decided|chose|going with|will use|settled on|picked)" session.jsonl | grep -i "X"

# jq version - extract decision context
cat session.jsonl | jq -r '
  select(.type == "assistant") |
  .message.content |
  if type == "array" then .[] | select(.type == "text") | .text else . end' |
  grep -i -E "(decided|chose|going with)" | head -20
```

### "How did we fix the Y error?"

```bash
# Find error mentions
grep -i "Y error" session.jsonl

# Find fix/solution mentions
grep -i -E "(fixed|solved|resolved|works now|the issue was)" session.jsonl

# Combine: error followed by fix
grep -A50 '"is_error":true' session.jsonl | grep -i "fix"
```

### "What files were modified?"

```bash
# All Edit operations
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Edit") |
  .input.file_path' 2>/dev/null | sort -u

# All Write operations
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Write") |
  .input.file_path' 2>/dev/null | sort -u

# Combined (Edit + Write)
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use") |
  select(.name == "Edit" or .name == "Write") |
  .input.file_path' 2>/dev/null | sort -u
```

### "What was the token usage?"

```bash
# Final usage stats
cat session.jsonl | jq 'select(.type == "result") | .usage' | tail -1

# Cumulative totals
cat session.jsonl | jq -s '
  [.[] | select(.type == "result") | .usage | select(. != null)] |
  {
    total_input: (map(.input_tokens // 0) | add),
    total_output: (map(.output_tokens // 0) | add),
    cache_read: (map(.cache_read_input_tokens // 0) | add),
    cache_creation: (map(.cache_creation_input_tokens // 0) | add)
  }'
```

### "What tests were run?"

```bash
# Bash commands with test keywords
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Bash") |
  .input.command' 2>/dev/null | grep -i -E "(test|jest|vitest|pytest|bun test)"
```

### "What was installed?"

```bash
# Package install commands
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Bash") |
  .input.command' 2>/dev/null | grep -i -E "(npm install|bun add|yarn add|pip install)"
```

---

## Advanced Patterns

### Conversation Flow Extraction

```bash
# User-Assistant pairs (simplified)
cat session.jsonl | jq -r '
  if .type == "user" then
    "USER: " + (if .message.content | type == "array" then .message.content[0].text else .message.content end)
  elif .type == "assistant" then
    "ASSISTANT: " + (
      if .message.content | type == "array" then
        (.message.content[] | select(.type == "text") | .text) // "[tool use]"
      else
        .message.content
      end
    )
  else
    empty
  end'
```

### Find Skills/Commands Invoked

```bash
# Skill tool calls
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Skill") |
  .input.skill' 2>/dev/null | sort | uniq -c
```

### Find Web Searches

```bash
# WebSearch queries
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "WebSearch") |
  .input.query' 2>/dev/null
```

### Find Git Operations

```bash
# Git commands
cat session.jsonl | jq -r '
  .message.content[]? |
  select(.type == "tool_use" and .name == "Bash") |
  .input.command' 2>/dev/null | grep "^git "
```

---

## Helper Scripts

### Create a Search Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
alias claude-search='grep -r -i --include="*.jsonl" -H'

# Usage
claude-search "database migration" ~/.claude/projects/
```

### Quick Session Summary

```bash
#!/bin/bash
# save as ~/bin/claude-session-summary
SESSION=$1
echo "=== Session Summary ==="
echo "User prompts: $(grep -c '"type":"user"' "$SESSION")"
echo "Assistant responses: $(grep -c '"type":"assistant"' "$SESSION")"
echo "Tool uses: $(grep -c '"tool_use"' "$SESSION")"
echo "Errors: $(grep -c '"is_error":true' "$SESSION")"
echo ""
echo "=== Tools Used ==="
cat "$SESSION" | jq -r '.message.content[]? | select(.type == "tool_use") | .name' 2>/dev/null | sort | uniq -c | sort -rn
```

---

## Tips

1. **Pipe to `less`** for large outputs: `cat session.jsonl | jq '...' | less`

2. **Use `head`/`tail`** to limit output: `... | head -20`

3. **Pretty print JSON**: Add no flags to jq for formatted output

4. **Suppress errors**: Add `2>/dev/null` when parsing may fail

5. **Combine with ripgrep** for speed:
   ```bash
   rg -l "search term" ~/.claude/projects/*/*.jsonl
   ```

6. **Export to file** for analysis:
   ```bash
   cat session.jsonl | jq '...' > analysis.json
   ```
