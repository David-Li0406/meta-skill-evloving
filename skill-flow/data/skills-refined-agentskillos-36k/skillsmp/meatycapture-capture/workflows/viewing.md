# Viewing & Searching Request-Logs

Workflows for viewing existing logs, searching past items, and using structured development history for context.

## When to Use

- **Development Context**: Reference past fixes when working on similar issues
- **Duplicate Check**: Verify an issue hasn't already been captured before creating
- **Progress Review**: See what items exist for a project or domain
- **Pattern Discovery**: Find related items across multiple documents
- **Status Tracking**: Check status of previously captured items

---

## List Documents

View all request-log documents for a project:

```bash
# List all docs for a project
meatycapture log list PROJECT_NAME --json

# List all docs across all projects
meatycapture log list --json

# List docs from a specific path
meatycapture log list --path /custom/path --json

# List only enabled projects' docs
meatycapture log list --enabled-only --json
```

**Output**:

```json
{
  "docs": [
    {
      "doc_id": "REQ-20251229-project-name",
      "path": "~/.meatycapture/project-name/REQ-20251229-project-name.md",
      "title": "Security Audit Findings",
      "item_count": 5,
      "tags": ["security", "validation", "testing"],
      "created_at": "2025-12-29T10:00:00Z",
      "updated_at": "2025-12-29T14:30:00Z"
    }
  ]
}
```

---

## View Document

Read a specific document with all items:

```bash
# View full document
meatycapture log view ~/.meatycapture/project/REQ-20251229-project.md --json

# View with type filter
meatycapture log view <doc-path> --filter-type bug --json

# View with status filter
meatycapture log view <doc-path> --filter-status triage --json

# View with priority filter
meatycapture log view <doc-path> --filter-priority critical --json
```

**Output**:

```json
{
  "doc_id": "REQ-20251229-project-name",
  "title": "Security Audit Findings",
  "project": "project-name",
  "item_count": 3,
  "tags": ["security", "validation"],
  "items": [
    {
      "id": "REQ-20251229-project-name-01",
      "title": "Sanitize user input",
      "type": "bug",
      "domain": "core",
      "priority": "critical",
      "status": "triage",
      "tags": ["security", "input-validation"],
      "notes": "Problem: Project names not sanitized..."
    }
  ]
}
```

---

## Search Items

Find items across documents by keyword, type, tag, or status:

### Basic Keyword Search

```bash
# Search by keyword in title or notes
meatycapture log search "validation" PROJECT_NAME --json

# Search across all projects
meatycapture log search "performance" --json
```

### Structured Search Patterns

```bash
# Search by type
meatycapture log search "type:bug" PROJECT_NAME --json
meatycapture log search "type:enhancement" PROJECT_NAME --json
meatycapture log search "type:task" PROJECT_NAME --json

# Search by tag
meatycapture log search "tag:security" PROJECT_NAME --json
meatycapture log search "tag:performance" PROJECT_NAME --json

# Search by status
meatycapture log search "status:triage" PROJECT_NAME --json
meatycapture log search "status:in-progress" PROJECT_NAME --json

# Search by priority
meatycapture log search "priority:critical" PROJECT_NAME --json
meatycapture log search "priority:high" PROJECT_NAME --json

# Search by domain
meatycapture log search "domain:core" PROJECT_NAME --json
meatycapture log search "domain:web" PROJECT_NAME --json
```

### Combined Search

```bash
# Find critical bugs in core domain
meatycapture log search "type:bug priority:critical domain:core" PROJECT_NAME --json

# Find security-tagged items in triage
meatycapture log search "tag:security status:triage" PROJECT_NAME --json
```

**Output**:

```json
{
  "query": "type:bug priority:critical",
  "matches": [
    {
      "doc_id": "REQ-20251229-project-name",
      "doc_path": "~/.meatycapture/project-name/REQ-20251229-project-name.md",
      "item_id": "REQ-20251229-project-name-01",
      "title": "Sanitize user input in project names",
      "type": "bug",
      "priority": "critical",
      "status": "triage",
      "tags": ["security", "input-validation"],
      "snippet": "Problem: Project names not sanitized, allowing path traversal..."
    }
  ],
  "total_matches": 1
}
```

---

## Development Context Patterns

### Find Past Fixes for Similar Work

When working on a feature, search for related past captures:

```bash
# Working on authentication? Check past auth issues
meatycapture log search "auth" --json | jq '.matches[] | {id: .item_id, title: .title, status: .status}'

# Working on API? Check past API items
meatycapture log search "domain:api" --json
```

### Check for Existing Solutions

Before implementing a fix, check if similar work was captured:

```bash
# Searching for validation issues
meatycapture log search "validation" PROJECT_NAME --json

# Check specific module context
meatycapture log search "context:serializer" PROJECT_NAME --json
```

### Review Technical Debt

See all technical debt items for planning:

```bash
# Find all task-type items (often tech debt)
meatycapture log search "type:task" PROJECT_NAME --json

# Find items tagged as tech-debt
meatycapture log search "tag:tech-debt" PROJECT_NAME --json
meatycapture log search "tag:refactor" PROJECT_NAME --json
```

### Pre-Capture Duplicate Check

Before capturing a new item, verify it doesn't exist:

```bash
# Check if similar item exists
meatycapture log search "tag aggregation" PROJECT_NAME --json

# If found, consider:
# 1. Reference existing item in notes
# 2. Append to existing document instead
# 3. Skip capture if truly duplicate
```

---

## Output Formats

All view/search commands support multiple output formats:

```bash
# JSON (default for programmatic use)
meatycapture log list PROJECT_NAME --json

# YAML
meatycapture log list PROJECT_NAME --yaml

# Table (human-readable)
meatycapture log list PROJECT_NAME --table

# CSV (for export)
meatycapture log list PROJECT_NAME --csv
```

---

## Filtering Patterns

### Filter by Multiple Criteria

```bash
# Get all open bugs in core domain
meatycapture log view <doc-path> --filter-type bug --filter-status triage --json

# Get high-priority items only
meatycapture log view <doc-path> --filter-priority high --json
```

### Parse with jq

For complex filtering, combine JSON output with jq:

```bash
# Get all item IDs with titles
meatycapture log view <doc-path> --json | jq '.items[] | {id, title}'

# Filter in-progress items
meatycapture log view <doc-path> --json | jq '.items[] | select(.status == "in-progress")'

# Count by type
meatycapture log view <doc-path> --json | jq '.items | group_by(.type) | map({type: .[0].type, count: length})'

# Find items with specific tag
meatycapture log view <doc-path> --json | jq '.items[] | select(.tags | contains(["security"]))'
```

---

## CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `meatycapture log list [project] --json` | List documents |
| `meatycapture log view <doc-path> --json` | View document |
| `meatycapture log search <query> [project] --json` | Search items |
| `meatycapture list [project] --json` | Alias for log list |

### View Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |
| `--yaml` | Output as YAML |
| `--table` | Output as table |
| `--csv` | Output as CSV |
| `--filter-type <type>` | Filter by item type |
| `--filter-status <status>` | Filter by status |
| `--filter-priority <priority>` | Filter by priority |

### List Options

| Option | Description |
|--------|-------------|
| `--path <dir>` | Custom directory path |
| `--enabled-only` | Only enabled projects |
| `--json` | Output as JSON |

---

## Use Cases

### 1. Start of Session Context

Load recent captures for context:

```bash
# What was captured recently?
meatycapture log list PROJECT_NAME --json | jq '.docs | sort_by(.updated_at) | reverse | .[0:3]'

# What's in triage?
meatycapture log search "status:triage" PROJECT_NAME --json
```

### 2. Before Implementing a Fix

```bash
# Check if issue was already captured
meatycapture log search "validation error" PROJECT_NAME --json

# Get full context on an item
DOC_PATH=$(meatycapture log search "REQ-20251229-project-03" --json | jq -r '.matches[0].doc_path')
meatycapture log view "$DOC_PATH" --json | jq '.items[] | select(.id == "REQ-20251229-project-03")'
```

### 3. Progress Review

```bash
# How many items per status?
meatycapture log search "" PROJECT_NAME --json | jq '.matches | group_by(.status) | map({status: .[0].status, count: length})'

# What's still in triage?
meatycapture log search "status:triage" PROJECT_NAME --json | jq '.matches | length'
```

### 4. Cross-Reference Items

```bash
# Find all items related to security
meatycapture log search "tag:security" --json

# Find items across projects
meatycapture log search "authentication" --json | jq '.matches[] | {project: .doc_id | split("-")[2], title: .title}'
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No matches found | Try broader search terms |
| Empty doc list | Check project exists: `meatycapture project list` |
| Path not found | Verify path with `ls ~/.meatycapture/` |
| JSON parse error | Ensure `--json` flag is used |

See `./references/troubleshooting.md` for detailed solutions.
