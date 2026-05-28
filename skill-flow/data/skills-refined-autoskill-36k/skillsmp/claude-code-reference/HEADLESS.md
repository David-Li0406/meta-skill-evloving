# Claude Code Headless Mode (Agent SDK CLI)

> Run Claude Code programmatically from the CLI for automation, scripting, and CI/CD pipelines.

**Note:** Headless mode is now officially called "Agent SDK CLI". The `-p` flag and all CLI options work the same way.

## What is Headless Mode?

Headless mode allows you to run Claude Code non-interactively, making it suitable for:

- Automated scripts and batch processing
- CI/CD pipelines (GitHub Actions, GitLab CI/CD)
- Programmatic code analysis and generation
- Integration with other tools and workflows

When you pass the `-p` (or `--print`) flag, Claude Code runs without interactive prompts and exits after completing the task.

---

## Invocation Flags

### Core Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-p`, `--print` | Run non-interactively, print response and exit | `claude -p "explain this function"` |
| `--output-format` | Output format: `text`, `json`, `stream-json` | `claude -p --output-format json "query"` |
| `--model` | Specify model (`sonnet`, `opus`, or full name) | `claude -p --model opus "query"` |
| `--fallback-model` | Fallback model when default is overloaded | `claude -p --fallback-model sonnet "query"` |

### Session Management

| Flag | Description | Example |
|------|-------------|---------|
| `-c`, `--continue` | Continue most recent conversation | `claude -p -c "follow up question"` |
| `-r`, `--resume` | Resume specific session by ID or name | `claude -p --resume "session-id" "query"` |
| `--session-id` | Use specific session ID (must be valid UUID) | `claude --session-id "uuid" "query"` |
| `--fork-session` | Create new session when resuming | `claude --resume abc123 --fork-session` |

### Tool Control

| Flag | Description | Example |
|------|-------------|---------|
| `--allowedTools` | Auto-approve specific tools | `claude -p --allowedTools "Bash,Read,Edit" "query"` |
| `--disallowedTools` | Remove tools from model context | `claude -p --disallowedTools "Bash" "query"` |
| `--tools` | Specify available tools (empty string disables all) | `claude -p --tools "Read,Glob" "query"` |
| `--dangerously-skip-permissions` | Skip all permission prompts (use with caution) | `claude -p --dangerously-skip-permissions "query"` |

### System Prompt Customization

| Flag | Description | Example |
|------|-------------|---------|
| `--system-prompt` | Replace entire system prompt | `claude -p --system-prompt "You are a Python expert" "query"` |
| `--system-prompt-file` | Load system prompt from file | `claude -p --system-prompt-file ./prompt.txt "query"` |
| `--append-system-prompt` | Append to default system prompt | `claude -p --append-system-prompt "Focus on security" "query"` |

### Advanced Options

| Flag | Description | Example |
|------|-------------|---------|
| `--json-schema` | Get structured output matching JSON Schema | `claude -p --json-schema '{"type":"object",...}' "query"` |
| `--max-turns` | Limit number of agentic turns | `claude -p --max-turns 3 "query"` |
| `--verbose` | Enable verbose turn-by-turn logging | `claude -p --verbose "query"` |
| `--debug` | Enable debug mode with category filtering | `claude -p --debug "api,mcp" "query"` |
| `--add-dir` | Add additional working directories | `claude -p --add-dir ../apps ../lib "query"` |

---

## Output Formats

### Text (Default)

Plain text output, suitable for human reading or simple piping:

```bash
claude -p "What does the auth module do?"
```

### JSON

Structured JSON with result, session ID, and metadata:

```bash
claude -p "Summarize this project" --output-format json
```

Response structure:
```json
{
  "result": "The text response...",
  "session_id": "uuid-of-session",
  "usage": { ... },
  "structured_output": null
}
```

### Stream-JSON

Newline-delimited JSON for real-time streaming:

```bash
claude -p "Generate code" --output-format stream-json
```

Use `--include-partial-messages` to include partial streaming events:

```bash
claude -p "query" --output-format stream-json --include-partial-messages
```

### Structured Output with JSON Schema

Get validated JSON output conforming to a specific schema:

```bash
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

The structured data appears in the `structured_output` field of the response.

---

## Session Management

### Continue Most Recent Conversation

```bash
# Initial request
claude -p "Review this codebase for performance issues"

# Continue with follow-up
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

### Resume Specific Session

Capture and reuse session IDs for parallel workflows:

```bash
# Capture session ID from first request
session_id=$(claude -p "Start analyzing auth module" --output-format json | jq -r '.session_id')

# Resume that specific session later
claude -p "Continue the analysis" --resume "$session_id"
```

### Fork a Session

Create a branch from an existing session without modifying it:

```bash
claude --resume "abc123" --fork-session -p "Try an alternative approach"
```

---

## MCP Configuration in Headless Mode

### Load MCP Servers

```bash
# From JSON file
claude -p --mcp-config ./mcp.json "query"

# Strict mode - only use specified MCP config
claude -p --strict-mcp-config --mcp-config ./mcp.json "query"
```

### Permission Prompt Tool

Handle permission prompts programmatically via MCP:

```bash
claude -p --permission-prompt-tool mcp_auth_tool "query"
```

---

## CI/CD Integration Patterns

### GitHub Actions Example

```yaml
name: Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "Review this PR for issues" \
            --output-format json \
            --append-system-prompt "Focus on security and performance"
```

### GitLab CI/CD Example

```yaml
code-review:
  stage: review
  script:
    - npm install -g @anthropic-ai/claude-code
    - |
      git diff origin/main...HEAD | \
      claude -p "Review these changes" \
        --output-format json \
        --allowedTools "Read,Glob,Grep"
  only:
    - merge_requests
```

### Shell Script Automation

```bash
#!/bin/bash
set -e

# Auto-commit with AI-generated message
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff:*),Bash(git log:*),Bash(git status:*),Bash(git commit:*)"
```

---

## Common Use Cases

### Automated Code Review

```bash
# Review a specific file
claude -p "Review auth.py for security vulnerabilities" \
  --allowedTools "Read" \
  --append-system-prompt "You are a security engineer"

# Review staged changes
git diff --cached | claude -p "Review these changes for issues" --output-format json
```

### Test Generation

```bash
claude -p "Generate unit tests for src/utils.ts" \
  --allowedTools "Read,Write,Bash" \
  --output-format json
```

### Documentation Updates

```bash
claude -p "Update the README.md based on recent changes to the API" \
  --allowedTools "Read,Edit,Glob"
```

### Batch Processing

```bash
# Process multiple files
for file in src/*.ts; do
  claude -p "Add JSDoc comments to $file" \
    --allowedTools "Read,Edit" \
    --output-format json >> results.jsonl
done
```

### Extract Structured Data

```bash
# Extract function signatures
claude -p "List all exported functions in src/" \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "functions": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "file": {"type": "string"},
            "parameters": {"type": "array", "items": {"type": "string"}}
          }
        }
      }
    }
  }'
```

### Piping Content

```bash
# Analyze logs
cat error.log | claude -p "Identify the root cause of these errors"

# Process PR diff
gh pr diff 123 | claude -p "Summarize the changes in this PR"

# Analyze test output
npm test 2>&1 | claude -p "Explain why these tests are failing"
```

---

## Limitations and Considerations

### Interactive Features Not Available

- Slash commands (`/commit`, `/review`, etc.) only work in interactive mode
- In headless mode, describe the task you want accomplished instead

### Permission Handling

- Without `--allowedTools`, Claude will not auto-approve tool use
- `--dangerously-skip-permissions` skips ALL prompts - use with extreme caution
- For CI/CD, explicitly list allowed tools for security

### Session Persistence

- Sessions are stored locally - not available across different machines
- Use `--session-id` with a consistent UUID for predictable session management

### Rate Limiting

- Headless mode is subject to the same API rate limits as interactive mode
- Use `--fallback-model` to handle overload situations gracefully

### Output Size

- Large outputs may be truncated depending on model context limits
- Use `--verbose` to debug turn-by-turn execution

### Tool Restrictions

```bash
# Restrict to read-only operations
claude -p "query" --tools "Read,Glob,Grep"

# Disable all tools
claude -p "query" --tools ""

# Allow specific bash commands only
claude -p "query" --allowedTools "Bash(git status:*),Bash(git log:*)"
```

---

## Tips and Best Practices

1. **Use `--output-format json` for scripting** - Enables programmatic parsing of results

2. **Capture session IDs** - Store them for multi-step workflows:
   ```bash
   session=$(claude -p "Start task" --output-format json | jq -r '.session_id')
   ```

3. **Use `jq` for JSON parsing**:
   ```bash
   claude -p "query" --output-format json | jq -r '.result'
   ```

4. **Prefer `--append-system-prompt`** - Keeps default Claude Code capabilities while adding custom instructions

5. **Limit tool permissions** - Only allow the tools actually needed for the task

6. **Use `--max-turns` for safety** - Prevents runaway agent loops in automation

7. **Test locally first** - Verify commands work before adding to CI/CD pipelines

---

## See Also

- [CLI Reference](https://code.claude.com/docs/en/cli-reference) - Complete CLI documentation
- [GitHub Actions Integration](https://code.claude.com/docs/en/github-actions) - GitHub workflow setup
- [GitLab CI/CD Integration](https://code.claude.com/docs/en/gitlab-ci-cd) - GitLab pipeline setup
- [Agent SDK Documentation](https://docs.claude.com/en/docs/agent-sdk) - Python and TypeScript SDK
- [MCP Configuration](https://code.claude.com/docs/en/mcp) - Model Context Protocol setup
