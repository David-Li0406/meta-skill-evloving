---
name: jira-cli
description: Reference guide for acli commands covering JQL queries, ticket transitions, comments, and workflow operations—includes common patterns and syntax
---

# Atlassian CLI (acli) - Jira Command Reference

## Search Commands

```bash
acli jira workitem search --jql "project = <PROJECT> AND assignee = currentUser() AND resolution = Unresolved"
acli jira workitem search --jql "project = <PROJECT>" --fields "key,status,summary"
acli jira workitem search --jql "project = <PROJECT>" --limit 50 --paginate
acli jira workitem search --jql "project = <PROJECT>" --count
```

Output flags: `--json`, `--csv`, `--web`

## JQL Syntax

- Single quotes for values with spaces: `status = 'Some Status'`
- Avoid `!=` with backslash - use `NOT status = 'Done'` instead
- Functions: `currentUser()`, `now()`, `startOfDay()`, `endOfWeek()`
- Status categories: `statusCategory = Done`, `statusCategory = 'In Progress'`
- Operators: `AND`, `OR`, `NOT`, `IN`, `IS`, `IS NOT`, `~` (contains), `ORDER BY`

### Common JQL Patterns

```sql
project = <PROJECT> AND assignee = currentUser() AND resolution = Unresolved
project = <PROJECT> AND status = '<status-name>'
project = <PROJECT> AND statusCategory = 'In Progress'
project = <PROJECT> AND updated >= -7d ORDER BY updated DESC
project = <PROJECT> AND Sprint = '<sprint-name>'
project = <PROJECT> AND component = <component>
```

## View Commands

```bash
acli jira workitem view <KEY>
acli jira workitem view <KEY> --fields "summary,description,status,comment"
acli jira workitem view <KEY> --fields "*all" --json
```

Field values: `*all` (all fields), `*navigable` (navigable fields), `-fieldname` (exclude field)

## Comment Commands

```bash
acli jira workitem comment create --key <KEY> --body "Comment text"
acli jira workitem comment create --key <KEY> --body-file comment.txt
acli jira workitem comment create --jql "project = <PROJECT> AND labels = needs-review" --body "Reviewed"
acli jira workitem comment list --key <KEY>
acli jira workitem comment create --key <KEY> --edit-last --body "Updated comment"
acli jira workitem comment create --key <KEY> --editor
```

### ADF (Atlassian Document Format)

Jira Cloud uses ADF (JSON-based). Plain `\n` newlines don't create paragraph breaks.

**acli limitations:** Headings, text marks (bold/italic/code), and code block syntax highlighting are rejected or stripped.

**Supported:** Paragraphs, bullet/ordered lists, code blocks (no highlighting).

```json
{"version":1,"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Your text"}]}]}
```

```json
{"version":1,"type":"doc","content":[{"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"Item one"}]}]}]}]}
```

```json
{"version":1,"type":"doc","content":[{"type":"codeBlock","attrs":{"language":"python"},"content":[{"type":"text","text":"def hello():\n    print('Hello')"}]}]}
```

```bash
acli jira workitem comment create --key <KEY> --body '{"version":1,"type":"doc","content":[...]}'
acli jira workitem comment create --key <KEY> --body-file comment.json
```

## Transition Commands

```bash
acli jira workitem transition --key <KEY> --status "Done"
acli jira workitem transition --key "<KEY1>,<KEY2>" --status "<status>"
acli jira workitem transition --jql "project = <PROJECT> AND labels = ready" --status "Done" --yes
acli jira workitem transition --filter 10001 --status "Done"
```

## Edit Commands

```bash
acli jira workitem edit --key <KEY> --summary "New title"
acli jira workitem edit --key <KEY> --description "New description"
acli jira workitem edit --key <KEY> --description-file desc.txt
acli jira workitem edit --key <KEY> --assignee "user@example.com"  # or "@me" or "default"
acli jira workitem edit --key <KEY> --remove-assignee
acli jira workitem edit --key <KEY> --labels "bug,urgent"
acli jira workitem edit --key <KEY> --remove-labels "wontfix"
acli jira workitem edit --key <KEY> --type "Bug"
acli jira workitem edit --jql "project = <PROJECT> AND labels = old" --labels "new" --yes
acli jira workitem edit --from-json workitem.json
acli jira workitem edit --generate-json
```

## Other Commands

```bash
# Attachments
acli jira workitem attachment list --key <KEY>
acli jira workitem attachment delete --key <KEY> --attachment-id 12345

# Links
acli jira workitem link create --key <KEY> --link-type "blocks" --outward-key <OTHER-KEY>
acli jira workitem link list-types

# Watchers
acli jira workitem watcher add --key <KEY> --user "user@example.com"
acli jira workitem watcher remove --key <KEY> --user "user@example.com"

# Misc
acli jira workitem clone --key <KEY>
acli jira workitem archive --key <KEY>
acli jira workitem unarchive --key <KEY>
acli jira workitem delete --key <KEY>
```

## Project Commands

```bash
acli jira project list --recent
acli jira project view --key <PROJECT>
acli jira project view --key <PROJECT> --json
```

## Common Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--key` | `-k` | Ticket key(s), comma-separated |
| `--jql` | `-j` | JQL query string |
| `--filter` | | Saved filter ID |
| `--json` | | Output as JSON |
| `--csv` | | Output as CSV |
| `--web` | `-w` | Open in browser |
| `--yes` | `-y` | Skip confirmation prompts |
| `--limit` | `-l` | Maximum results |
| `--paginate` | | Fetch all results |
| `--fields` | `-f` | Fields to include |
| `--ignore-errors` | | Continue on errors |

## Workflow Patterns

### Review Tickets Workflow

When reviewing ticket status against codebase:

1. List open tickets: `acli jira workitem search --jql "assignee = currentUser() AND resolution = Unresolved" --fields "key,status,summary"`
2. For each ticket, search git history: `git log --oneline --grep="<KEY>"`
3. Check if work is deployed: compare commits against release tags
4. Transition or comment as needed

### Transitions

Transition syntax: `acli jira workitem transition --key <KEY> --status "<target-status>"`

Common workflow patterns vary by organization. Consult your team's workflow documentation for valid status transitions.

### Batch Operations

```bash
# Add same comment to multiple tickets
acli jira workitem comment create --key "<KEY1>,<KEY2>,<KEY3>" --body "Batch update: <message>"

# Transition multiple tickets
acli jira workitem transition --key "<KEY1>,<KEY2>" --status "Done" --yes
```

## Error Handling

- Use `--ignore-errors` to continue when some operations fail
- JQL errors often indicate syntax issues - check quotes and escapes
- Transition errors may indicate invalid target status for current state
- Use `--web` to debug by viewing in Jira UI
