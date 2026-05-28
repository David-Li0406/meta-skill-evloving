# Jira CLI Examples

Essential command patterns for the jira-cli tool.

## Fetch Ticket Data

```bash
# Get ticket in JSON
jira issue view PROJ-123 --json

# With comments
jira issue view PROJ-123 --comments 5 --json

# Parse fields
TICKET=$(jira issue view PROJ-123 --json)
SUMMARY=$(echo "$TICKET" | jq -r '.fields.summary')
DESCRIPTION=$(echo "$TICKET" | jq -r '.fields.description // "No description"')
STATUS=$(echo "$TICKET" | jq -r '.fields.status.name')
COMMENTS=$(echo "$TICKET" | jq -r '.fields.comment.comments[].body')
```

## Post Comments

```bash
# Simple comment
jira issue comment add PROJ-123 "Status update"

# Multi-line from heredoc
jira issue comment add PROJ-123 <<'EOF'
## Clarifying Questions

1. Question one?
2. Question two?

Please answer to proceed with planning.
EOF

# From stdin
echo "Comment text" | jira issue comment add PROJ-123
```

## Error Handling

```bash
# Check CLI exists
if ! command -v jira &> /dev/null; then
    echo "❌ jira CLI not installed"
    exit 1
fi

# Fetch with error handling
if ! TICKET=$(jira issue view "$KEY" --json 2>&1); then
    echo "❌ Failed to fetch $KEY"
    echo "$TICKET"
    exit 1
fi

# Validate JSON
if ! echo "$TICKET" | jq -e '.fields.summary' > /dev/null 2>&1; then
    echo "❌ Invalid response"
    exit 1
fi
```

## Batch Fetch

```bash
KEYS=("PROJ-123" "PROJ-124" "PROJ-125")

for KEY in "${KEYS[@]}"; do
    if ! jira issue view "$KEY" --json > "${KEY}.json" 2>&1; then
        echo "❌ Failed: $KEY"
        continue
    fi
    echo "✅ $KEY"
done
```

## Multiple Configs

```bash
# Use specific config
JIRA_CONFIG_FILE=~/.config/jira/project-a.yml jira issue view PROJ-123 --json

# Or with flag
jira issue view PROJ-123 --json --config ~/.config/jira/project-b.yml
```
