# Jira CLI Patterns

Best practices for using jira-cli in automation.

## Prerequisites Check

```bash
# Check installation
if ! command -v jira &> /dev/null; then
    echo "❌ jira CLI not installed"
    echo "Install: https://github.com/ankitpokhrel/jira-cli"
    exit 1
fi

# Check config
if [ ! -f ~/.config/jira/.config.yml ]; then
    echo "❌ Run: jira init"
    exit 1
fi

# Check auth (Cloud)
if [ -z "$JIRA_API_TOKEN" ]; then
    echo "❌ Set JIRA_API_TOKEN"
    exit 1
fi
```

## Error Handling

```bash
# Always check exit codes
if ! RESULT=$(jira issue view "$KEY" --json 2>&1); then
    echo "❌ Failed to fetch $KEY"
    echo "$RESULT"
    return 1
fi

# Validate JSON structure
if ! echo "$RESULT" | jq -e '.fields.summary' > /dev/null 2>&1; then
    echo "❌ Invalid JSON"
    return 1
fi
```

## Parsing Patterns

```bash
# Use jq with defaults for optional fields
TICKET=$(jira issue view PROJ-123 --json)
ASSIGNEE=$(echo "$TICKET" | jq -r '.fields.assignee.displayName // "Unassigned"')
DESCRIPTION=$(echo "$TICKET" | jq -r '.fields.description // "No description"')
LABELS=$(echo "$TICKET" | jq -r '.fields.labels[]?' | tr '\n' ',' | sed 's/,$//')
```

## Posting Comments

```bash
# Always use heredoc with quotes for multi-line
jira issue comment add PROJ-123 <<'EOF'
## Questions

1. Question one?
2. Question two?
EOF

# Check success
if [ $? -eq 0 ]; then
    echo "✅ Posted to PROJ-123"
else
    echo "❌ Failed to post"
fi
```

## Batch Processing

```bash
# Process tickets sequentially with error handling
KEYS=("PROJ-123" "PROJ-124" "PROJ-125")

for KEY in "${KEYS[@]}"; do
    echo "Processing $KEY..."

    if ! jira issue view "$KEY" --json > "${KEY}.json" 2>&1; then
        echo "❌ Failed: $KEY, skipping..."
        continue
    fi

    echo "✅ $KEY"
done
```

## Multiple Configs

```bash
# Function to fetch from specific instance
fetch_ticket() {
    local config=$1
    local key=$2
    JIRA_CONFIG_FILE="$config" jira issue view "$key" --json
}

# Use
fetch_ticket ~/.config/jira/project-a.yml PROJ-123
fetch_ticket ~/.config/jira/project-b.yml PROJ-456
```

## Common Mistakes

❌ **Don't parse interactive UI:**
```bash
jira issue list | grep "PROJ"  # Won't work
```

✅ **Use --json or --plain:**
```bash
jira issue list --json | jq '.issues[].key'
jira issue list --plain --no-headers
```

❌ **Don't assume fields exist:**
```bash
ASSIGNEE=$(echo "$TICKET" | jq -r '.fields.assignee.displayName')  # Fails if null
```

✅ **Use defaults:**
```bash
ASSIGNEE=$(echo "$TICKET" | jq -r '.fields.assignee.displayName // "Unassigned"')
```

❌ **Don't skip error handling:**
```bash
TICKET=$(jira issue view PROJ-123 --json)
SUMMARY=$(echo "$TICKET" | jq -r '.fields.summary')  # May fail silently
```

✅ **Check exit codes:**
```bash
if ! TICKET=$(jira issue view PROJ-123 --json 2>&1); then
    echo "Failed to fetch"
    exit 1
fi
```

## Key Points

- ✅ Always use `--json` for scripting
- ✅ Check exit codes before parsing output
- ✅ Use `jq` with defaults: `.field // "default"`
- ✅ Quote heredocs: `<<'EOF'` not `<<EOF`
- ✅ Handle errors gracefully (skip failed, continue)
- ❌ Don't parse interactive UI output
- ❌ Don't assume fields are always present
- ❌ Don't skip prerequisite checks

## Posting Long Specs/Documents

For large specs (>32KB or >1000 lines), attach the file and post a summary.

**jira-cli does NOT support attachments** - use the provided script:

**Script:** `./scripts/jira-attach.sh`

```bash
# Attach a file to a Jira issue
./scripts/jira-attach.sh PROJ-123 /path/to/spec.md

# Output:
# Attached 'spec.md' to PROJ-123
# Link in Jira: [^spec.md]
```

**Complete workflow for posting a spec:**

```bash
# 1. Attach the full spec file
./scripts/jira-attach.sh PROJ-123 ux-spec.md

# 2. Post summary with reference to attachment
jira issue comment add PROJ-123 <<'EOF'
h2. UX Implementation Spec

*Summary:* Implement the Storefront screen for React Native.

h3. Key Components
* Product Card
* Week Navigation
* Category Tabs
* Sticky Footer

h3. Full Specification
See attached: [^ux-spec.md]
EOF
```

**Jira attachment link syntax:** `[^filename.ext]`

## External References Checklist

Before posting to Jira:

- ❌ Remove local filesystem paths (`/Users/...`, `./local/...`)
- ❌ Remove internal URLs not accessible from Jira
- ✅ Attach files instead of referencing local paths
- ✅ Use `[^filename.ext]` to link attachments
- ✅ Use public URLs (GitHub, Confluence) for external refs
