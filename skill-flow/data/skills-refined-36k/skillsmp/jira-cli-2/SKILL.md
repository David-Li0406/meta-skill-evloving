---
name: "jira-cli"
description: "WHAT: Command line tool for Atlassian Jira. WHEN: managing issues, adding comments, viewing tickets, sprint workflows. KEYWORDS: jira, ticket, issue, sprint, comment, cli, atlassian, backlog, story, epic."
---

# Jira CLI

Command line tool for Atlassian Jira. [GitHub](https://github.com/ankitpokhrel/jira-cli)

## Prerequisites

```bash
command -v jira >/dev/null 2>&1 || echo "ERROR: jira CLI not found"
test -f ~/.config/.jira/.config.yml || echo "ERROR: jira not configured"
```

**Setup:**
- Install: `brew install jira` or [download binary](https://github.com/ankitpokhrel/jira-cli/releases)
- Configure: `jira init`
- Cloud auth: `export JIRA_API_TOKEN=your_token`
- On-premise PAT: `export JIRA_AUTH_TYPE=bearer JIRA_API_TOKEN=your_pat`

## Core Commands

```bash
# View ticket (JSON format)
jira issue view PROJ-123 --json

# View with comments
jira issue view PROJ-123 --comments 10 --json

# Add comment
jira issue comment add PROJ-123 "Comment text"
echo "Comment" | jira issue comment add PROJ-123

# Add comment with heredoc
jira issue comment add PROJ-123 <<'EOF'
## Multi-line comment
Content here
EOF

# List issues
jira issue list --created -7d --json
jira issue list --jql "status = 'To Do'" --json

# Create issue (simple)
jira issue create -tBug -s"Summary" -b"Description" --no-input

# Create issue with heredoc body (IMPORTANT: use stdin, not -b with heredoc)
jira issue create -tTask -s"Summary" --project=PROJ --no-input <<'EOF'
h2. Overview
Description content here

h2. Subtasks
* Task 1
* Task 2
EOF
```

## Output Formats

- `--json` - Structured JSON (use with `jq`)
- `--plain` - Simple tabular output
- `--no-headers` - Remove column headers
- `--columns key,summary` - Select specific columns

## Parsing Output

```bash
# Parse JSON with jq
TICKET=$(jira issue view PROJ-123 --json)
SUMMARY=$(echo "$TICKET" | jq -r '.fields.summary')
DESCRIPTION=$(echo "$TICKET" | jq -r '.fields.description // "No description"')
COMMENTS=$(echo "$TICKET" | jq -r '.fields.comment.comments[].body')

# Parse plain output
jira issue list --plain --no-headers | while IFS=$'\t' read -r key summary; do
  echo "$key: $summary"
done
```

## ADF (Atlassian Document Format) Parsing

Jira stores descriptions and comments in ADF (nested JSON), not plain text.

**Parser script:** `/scripts/parse-adf.js`

**Usage:**
```bash
# Parse description
jira issue view PROJ-123 --json | jq '.fields.description' | node /scripts/parse-adf.js

# Parse comment
echo "$COMMENT_JSON" | jq '.body' | node /scripts/parse-adf.js

# Parse all comments
jq -c '.fields.comment.comments[]' ticket.json | while IFS= read -r comment; do
  AUTHOR=$(echo "$comment" | jq -r '.author.displayName')
  BODY=$(echo "$comment" | jq '.body' | node /scripts/parse-adf.js)
  echo "Comment by $AUTHOR:"
  echo "$BODY"
  echo "---"
done
```

## Error Handling

```bash
# Check prerequisites
if ! command -v jira &> /dev/null; then
    echo "❌ jira CLI not installed"
    exit 1
fi

# Handle failures
if ! RESULT=$(jira issue view "$KEY" --json 2>&1); then
    echo "❌ Failed to fetch $KEY"
    echo "$RESULT"
    exit 1
fi
```

## Common Patterns

**Fetch ticket for spec:**
```bash
TICKET=$(jira issue view PROJ-123 --json)
SUMMARY=$(echo "$TICKET" | jq -r '.fields.summary')
```

**Post questions:**
```bash
jira issue comment add PROJ-123 <<'EOF'
## Clarifying Questions
1. Question one?
2. Question two?
EOF
```

**Check for answers:**
```bash
jira issue view PROJ-123 --comments 5 --json | jq -r '.fields.comment.comments[].body'
```

## Key Points

- ✅ Always use `--json` for scripting
- ✅ Check exit codes before parsing
- ✅ Use `jq` with defaults: `.field // "default"`
- ✅ Quote heredocs: `<<'EOF'` not `<<EOF`
- ✅ Use stdin (heredoc) for long descriptions, not `-b` flag with heredoc
- ✅ For very long descriptions, use stdin directly instead of wrapping in `-b "$(cat <<'EOF' ...)"`
- ❌ Don't parse interactive UI output
- ❌ Don't assume fields exist (use `// "default"`)
- ❌ Don't use `-b"$(cat <<'EOF' ... EOF)"` pattern - it can cause hangs and syntax errors

## Common Issues and Solutions

### Issue 1: Command Hangs with Long Descriptions

**Problem:** Using `-b"$(cat <<'EOF' ... EOF)"` with very long descriptions causes the command to hang indefinitely.

**Root Cause:** Command substitution with heredocs in argument position can cause shell parsing issues and timeouts.

**Solution:** Use stdin directly instead of `-b` flag:

```bash
# ❌ BAD: This will hang with long descriptions
jira issue create -tTask -s"Summary" -b"$(cat <<'EOF'
Long description here...
EOF
)" --project=PROJ --no-input

# ✅ GOOD: Use stdin directly
jira issue create -tTask -s"Summary" --project=PROJ --no-input <<'EOF'
Long description here...
EOF
```

### Issue 2: Syntax Errors with Nested Quotes in Heredocs

**Problem:** Syntax errors like "unexpected EOF while looking for matching `''`" occur.

**Root Cause:** Mixing heredoc syntax with command substitution and quotes can create parsing ambiguities.

**Solution:** Use stdin directly without command substitution:

```bash
# ❌ BAD: Nested quotes and command substitution
jira issue create -tTask -s"Summary" -b"$(cat <<'EOF'
Text with 'quotes' here
EOF
)" --project=PROJ --no-input

# ✅ GOOD: Direct stdin
jira issue create -tTask -s"Summary" --project=PROJ --no-input <<'EOF'
Text with 'quotes' here
EOF
```

### Issue 3: Creating Multiple Tickets Efficiently

**Problem:** Need to create many tickets with full descriptions from a structured document.

**Solution:** Break into individual commands with stdin for each:

```bash
# Create ticket 1
jira issue create -tTask -s"[Project] Task 1: Title" --project=PROJ --no-input <<'EOF'
h2. Overview
Task 1 description

h2. Subtasks
* Subtask 1.1
* Subtask 1.2
EOF

echo "Created Task 1"

# Create ticket 2
jira issue create -tTask -s"[Project] Task 2: Title" --project=PROJ --no-input <<'EOF'
h2. Overview
Task 2 description

h2. Subtasks
* Subtask 2.1
* Subtask 2.2
EOF

echo "Created Task 2"
```

### Issue 4: Jira Wiki Markup Formatting

**Best Practices for Jira Wiki Markup in descriptions:**

```bash
jira issue create -tTask -s"Title" --project=PROJ --no-input <<'EOF'
h2. Main Heading
h3. Sub Heading

* Bullet point 1
* Bullet point 2
** Nested bullet

# Numbered list
# Item 2

*bold text*
_italic text_
{{monospace code}}
{code}
code block
{code}

[Link text|https://example.com]
EOF
```

**Common markup:**
- Headers: `h1.`, `h2.`, `h3.`, `h4.`, `h5.`, `h6.`
- Bold: `*bold*`
- Italic: `_italic_`
- Monospace: `{{text}}`
- Code blocks: `{code}...{code}`
- Bullets: `*`, `**` (nested)
- Numbered: `#`, `##` (nested)
- Links: `[text|url]`

## Multiple Configs

```bash
# Via env var
JIRA_CONFIG_FILE=/path/to/config.yml jira issue view PROJ-123 --json

# Via flag
jira issue view PROJ-123 --json --config /path/to/config.yml
```

## Attachments via REST API

**Note:** jira-cli does NOT support attachments. Use the provided script instead.

**Script:** `./scripts/jira-attach.sh`

```bash
# Attach a file to a Jira issue
./scripts/jira-attach.sh PROJ-123 /path/to/spec.md

# Output:
# Attached 'spec.md' to PROJ-123
# Link in Jira: [^spec.md]
```

The script reads `server` and `login` from existing jira-cli config (`~/.config/.jira/.config.yml`) and uses `JIRA_API_TOKEN` for authentication.

## Handling Long Content

For large documents (>32KB or >1000 lines), attach the full file and post a summary:

```bash
# Step 1: Attach full spec
./scripts/jira-attach.sh PROJ-123 spec.md

# Step 2: Post summary with attachment reference
jira issue comment add PROJ-123 <<'EOF'
h2. Implementation Spec

Summary of key components and requirements.

h3. Full Specification
See attached: [^spec.md]
EOF
```

**Attachment links:** Use `[^filename.ext]` to link to attachments in Jira.

## Markdown to Jira Wiki Conversion

Jira uses Wiki markup, not Markdown. Convert before posting:

| Markdown | Jira Wiki |
|----------|-----------|
| `# H1` | `h1. H1` |
| `## H2` | `h2. H2` |
| `**bold**` | `*bold*` |
| `_italic_` | `_italic_` |
| `[text](url)` | `[text\|url]` |
| `` `code` `` | `{{code}}` |
| ` ```lang ``` ` | `{code:lang}...{code}` |
| `- item` | `* item` |
| `1. item` | `# item` |
| `\| table \|` | `\|\| header \|\|` then `\| cell \|` |

## External References Warning

When posting to Jira, ensure all references are accessible:

- ❌ Never reference local filesystem paths (e.g., `/Users/foo/spec.md`)
- ❌ Never reference internal URLs inaccessible from Jira
- ✅ Use `[^filename.ext]` to reference Jira attachments
- ✅ Use Confluence/GitHub URLs for external docs
- ✅ Attach files instead of referencing local paths

## Best Practices for Bulk Ticket Creation

When creating multiple tickets with detailed descriptions:

1. **Use stdin for descriptions:** Always use heredoc via stdin, never `-b "$(cat <<'EOF' ...)"`
2. **One command per ticket:** Don't try to batch multiple creates in complex scripts
3. **Add progress indicators:** Use `echo "Created Task N"` between commands
4. **Handle timeouts:** Set appropriate timeout values for long operations
5. **Test first:** Create one ticket manually to verify format before bulk operations
6. **Quote properly:** Use `<<'EOF'` (quoted) to prevent variable expansion in heredocs

**Example workflow:**
```bash
# Test with one ticket first
jira issue create -tTask -s"[Test] Task 1" --project=PROJ --no-input <<'EOF'
h2. Overview
Test description
EOF

# If successful, proceed with remaining tickets
jira issue create -tTask -s"[Test] Task 2" --project=PROJ --no-input <<'EOF'
h2. Overview
Real description
EOF
echo "Created Task 2"

# Continue for remaining tickets...
```

## Documentation

- **[Examples](./references/examples.md)** - Real command examples
- **[API Reference](./references/api-docs.md)** - Complete command reference
- **[Patterns](./references/patterns.md)** - Best practices
