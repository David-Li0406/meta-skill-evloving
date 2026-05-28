---
name: zaira
description: Access Jira tickets offline using zaira CLI. Use when user needs to export, report, or refresh Jira tickets, or mentions "jira", "zaira", or ticket keys like "FOO-123".
---

# Zaira - Jira CLI

Exports Jira tickets to local markdown for offline access. See https://github.com/vivainio/zaira for setup.

## Commands

```bash
# Export tickets
zaira export FOO-1234 FOO-5678              # Export specific tickets
zaira export --jql "project = FOO"          # Export by JQL query
zaira export FOO-1234 --all-fields          # Include custom fields
zaira export FOO-1234 --files               # Force file output without zproject.toml

# Reports (group-by: status, priority, issuetype, assignee, labels, components, parent)
zaira report --board 123 --group-by status  # Generate report from board
zaira report my-tickets --full              # Named report + export tickets
zaira report --dashboard 123                # Report from Jira dashboard
zaira report --jql "project = FOO" --files  # Force file output
zaira report --jql "..." -g components      # Group by component
zaira refresh sprint-review.md              # Refresh existing report

# View tickets
zaira my                                    # Show my assigned tickets
zaira my -r                                 # Show tickets I reported (created)
zaira boards                                # List boards

# Create ticket from YAML front matter
zaira create ticket.md                      # Create from file
zaira create - --dry-run                    # Preview from stdin

# Edit ticket fields
zaira edit FOO-1234 --title "New title"
zaira edit FOO-1234 --description "New description"
zaira edit FOO-1234 --field "Priority=High" --field "Epic Link=FOO-100"
zaira edit FOO-1234 --field "assignee=me"   # Assign to yourself
zaira edit FOO-1234 --field "assignee=user@example.com"  # Assign by email
zaira edit FOO-1234 --from fields.yaml      # Update from YAML file
zaira edit FOO-1234 --from -                # Update from stdin YAML

# Other actions
zaira comment FOO-1234 "Comment text"       # Add comment to ticket
zaira link FOO-1234 FOO-5678 --type Blocks  # Link tickets
zaira transition FOO-1234 "In Progress"     # Change ticket status
zaira transition FOO-1234 --list            # List available transitions

# Instance metadata (cached locally)
zaira info statuses                         # List statuses
zaira info fields                           # List custom fields
zaira info fields --refresh                 # Refresh from Jira API
zaira info components FOO                   # List components for project
zaira info labels FOO                       # List labels for project
zaira info --save                           # Refresh all metadata
```

## Jira Formatting

When editing ticket descriptions or comments, use Jira wiki markup (not markdown):

```
h1. Heading 1
h2. Heading 2
h3. Heading 3

* Bullet item
* Another item

# Numbered item
# Another numbered item

*bold*  _italic_  -strikethrough-
[link text|https://example.com]
{code}code block{code}
```

## Confluence Wiki

Access Confluence pages using the same Jira credentials:

```bash
# Get page by ID or URL
zaira wiki get 123456                       # Get page by ID
zaira wiki get "https://acme.atlassian.net/wiki/spaces/DEV/pages/123456/Title"
zaira wiki get 123456 --format md           # Output as markdown (default)
zaira wiki get 123456 --format html         # Output raw HTML
zaira wiki get 123456 --format json         # Output full JSON response

# Search pages
zaira wiki search "search terms"            # Search in title and body
zaira wiki search "API docs" --space TEAM   # Search in specific space
zaira wiki search --creator "John Doe"      # Find pages by creator
zaira wiki search "onboarding" --limit 10   # Limit results
zaira wiki search "design" --format url     # Output just URLs
zaira wiki search "arch" --format id        # Output just page IDs
zaira wiki search "test" --format json      # Full JSON response
```

## Programmatic Access

```python
import zaira

# Jira client
jira = zaira.client()
issue = jira.issue("FOO-123")

# Instance schema (fields, statuses, priorities, issue types, link types)
s = zaira.schema()
s["statuses"]    # {'Open': 'To Do', 'In Progress': 'In Progress', ...}
s["fields"]      # {'customfield_10001': 'Epic Link', ...}
s["priorities"]  # ['Blocker', 'Critical', 'Major', ...]

# Project schema (components, labels)
ps = zaira.project_schema("FOO")
ps["components"]  # ['Backend', 'Frontend', ...]
ps["labels"]      # ['bug', 'feature', ...]
```

## Output

- `tickets/` - Exported ticket markdown files
- `reports/` - Generated reports
- `~/.cache/zaira/` - Cached schema (fields, statuses, etc.)

## Project Setup

```bash
zaira init FOO                              # Generate zproject.toml for project
zaira init FOO BAR                          # Multiple projects
zaira init FOO --force                      # Overwrite existing config
```

In a directory with `zproject.toml`, you can use named queries, report aliases, and batch operations.
