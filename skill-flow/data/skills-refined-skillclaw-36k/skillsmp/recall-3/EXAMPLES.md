# Examples

Common usage patterns and workflows for recall.

## Finding Past Work

### Search for a Topic

Find sessions where you worked on authentication:

```bash
recall search "authentication"
recall search "oauth login"
recall search "JWT token"
```

### Search Within Bash Commands

Find bash commands related to git:

```bash
recall search "git" --tool Bash
recall search "rebase" --tool Bash
```

The `--tool` flag filters to Bash tool calls only, searching within bash command text.

### Filter by Source

Search only Claude Code sessions (input accepts `claude-code` or `claude_code`):

```bash
recall search "refactor" --source claude-code
```

Search only Codex sessions:

```bash
recall search "fix bug" --source codex
```

Note: Output displays `claude_code` (underscore) in results.

## Browsing Sessions

### Recent Activity

See what you worked on today:

```bash
recall list --since 24h
```

This week:

```bash
recall list --since 7d
```

Since a specific date:

```bash
recall list --since 2024-01-01
```

### By Project

Find sessions in a specific repository:

```bash
recall list --project /path/to/my-app
recall list --project ~/code/api-server
```

Combine with time filter:

```bash
recall list --project /path/to/repo --since 7d
```

## Session Deep Dive

### View Session Details

Get full conversation with tool calls:

```bash
recall show abc123def456 --tools
```

Include thinking blocks (Claude Code):

```bash
recall show abc123def456 --tools --thinking
```

### Export for Analysis

Get JSON for processing:

```bash
recall show abc123def456 --json > session.json
```

Extract specific fields with jq:

```bash
recall show abc123 --json | jq '.messages[] | select(.role == "assistant") | .content'
```

## Analytics

### Tool Usage Patterns

See which tools you use most:

```bash
recall stats tools
```

Output:
```
Bash: 456
Read: 312
Edit: 234
Glob: 156
Grep: 89
Write: 45
```

### Bash Command Analysis

Break down bash commands by type:

```bash
recall stats bash
```

Output:
```
git status: 45
npm test: 32
git diff: 28
uv run: 22
```

### Permission Suggestions

Generate patterns for auto-approval:

```bash
recall stats bash --suggest
```

Output:
```
Suggested Bash Permissions
==========================
high: run tests (45 uses)
high: git operations (73 uses)
medium: npm/yarn commands (47 uses)
```

Use these suggestions to configure Claude Code permissions:

```json
{
  "permissions": {
    "allow": [
      {"tool": "Bash", "prompt": "run tests"},
      {"tool": "Bash", "prompt": "git operations"}
    ]
  }
}
```

### Token Usage

See token consumption by project:

```bash
recall stats tokens
```

Output:
```
/path/to/project-a: 125000 in / 45000 out
/path/to/project-b: 89000 in / 32000 out
```

## Maintenance

### Initial Setup

Index all existing sessions:

```bash
recall index
```

This scans:
- `~/.claude/projects/**/*.jsonl` (Claude Code)
- `~/.codex/sessions/*/rollout.jsonl` (Codex)

### Periodic Updates

Run index to pick up new sessions:

```bash
recall index
```

Already-indexed sessions are skipped automatically.

### Force Reindex

If data seems stale, force a full reindex:

```bash
recall index --full
```

### Rebuild Database

Start fresh (creates backup first):

```bash
recall index --recreate
```

### Index Specific Source

Only index Claude Code sessions:

```bash
recall index --source claude-code
```

Only index Codex sessions:

```bash
recall index --source codex
```

## JSON Output for Scripts

All commands support `--json` for scripting:

```bash
# Get session IDs from last week
recall list --since 7d --json | jq -r '.[].id'

# Find most-used tool
recall stats tools --json | jq 'to_entries | max_by(.value) | .key'

# Count sessions by source
recall list --json | jq 'group_by(.source) | map({source: .[0].source, count: length})'
```

## Workflow: Review Past Implementation

1. Search for the topic:
   ```bash
   recall search "rate limiting"
   ```

2. List sessions in that project:
   ```bash
   recall list --project /path/to/api --since 30d
   ```

3. Deep dive into relevant session:
   ```bash
   recall show abc123 --tools
   ```

## Workflow: Optimize Permissions

1. Index recent sessions:
   ```bash
   recall index
   ```

2. Get permission suggestions:
   ```bash
   recall stats bash --suggest
   ```

3. Review and add trusted patterns to Claude Code config.

4. Periodically re-run to discover new patterns:
   ```bash
   recall index && recall stats bash --suggest
   ```
