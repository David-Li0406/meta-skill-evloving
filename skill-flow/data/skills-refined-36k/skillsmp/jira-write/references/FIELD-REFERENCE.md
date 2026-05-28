# Jira Field Reference

Complete guide to working with Jira fields in write operations.

## Standard Fields

### Core Fields

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `summary` | String | "Add login button" | Max 255 chars |
| `description` | String/ADF | "Detailed description..." | Converted to ADF |
| `issuetype` | Object | `{"name": "Bug"}` | Must exist in project |
| `project` | Object | `{"key": "PROJ"}` | Required for create |
| `priority` | Object | `{"name": "High"}` | Project-specific |
| `assignee` | Object | `{"accountId": "..."}` | Use accountId |
| `labels` | Array | `["frontend", "urgent"]` | Replaces existing |

### Date Fields

| Field | Format | Example |
|-------|--------|---------|
| `duedate` | YYYY-MM-DD | "2024-03-15" |
| `startDate` | YYYY-MM-DD | "2024-03-01" |

### Relationship Fields

| Field | Type | Example |
|-------|------|---------|
| `parent` | Object | `{"key": "PROJ-100"}` | For subtasks |
| `fixVersions` | Array | `[{"name": "v1.0"}]` | Release versions |
| `components` | Array | `[{"name": "API"}]` | Project components |

## Custom Fields

Custom fields use IDs like `customfield_XXXXX`.

### Common Custom Fields

| Purpose | Typical ID Pattern | Example Value |
|---------|-------------------|---------------|
| Story Points | `customfield_10016` | `5` (number) |
| Sprint | `customfield_10020` | Sprint ID (number) |
| Epic Link | `customfield_10014` | `"PROJ-50"` (string) |
| Team | `customfield_10001` | `{"value": "Frontend"}` |

### Discovering Custom Field IDs

Use the `jira_discover_fields` tool:
```json
{
  "search": "story",
  "type": "number"
}
```

## Field Value Formats

### Priority Values
```json
// By name
{"name": "Highest"}
{"name": "High"}
{"name": "Medium"}
{"name": "Low"}
{"name": "Lowest"}
```

### Assignee Format
```json
// Assign to user (use accountId, not email)
{"accountId": "5b10a2844c20165700ede21g"}

// Unassign
null
```

### Labels Format
```json
// Set labels (replaces all existing)
["bug", "frontend", "urgent"]

// Clear labels
[]
```

### Description Format

Plain text is automatically converted to Atlassian Document Format (ADF):

```json
// Input (plain text)
"description": "This is the description.\n\nWith multiple paragraphs."

// Converted to ADF internally
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "This is the description."}]
    }
  ]
}
```

## Update Operations

### Partial Updates

Only provided fields are changed:
```json
{
  "issueKey": "PROJ-123",
  "summary": "New title",
  "priority": {"name": "High"}
}
```

### Clearing Fields

Set to `null` or empty:
```json
{
  "issueKey": "PROJ-123",
  "assignee": null,
  "labels": []
}
```

## Validation Rules

| Field | Constraint |
|-------|------------|
| `summary` | Required, max 255 chars |
| `description` | Max 32KB |
| `labels` | Max 255 chars per label |
| `issuetype` | Must exist in project |
| `priority` | Must be valid for project |
| `assignee` | Must have project access |

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Field not found" | Invalid field ID | Use discover_fields |
| "Invalid value" | Wrong format | Check field type |
| "Cannot set field" | Field is read-only | Some fields auto-calculated |
| "User not found" | Invalid accountId | Verify user exists |
