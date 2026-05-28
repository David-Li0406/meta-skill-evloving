---
name: jira-bug-fetcher
description: Fetches bug tickets from Jira using Atlassian MCP and formats them for AI-assisted bug fixing. Use when user mentions a Jira ticket key (like EMS-1234, PROJ-567) and wants to fix a bug, or when starting a bug-fixing workflow.
license: MIT
compatibility: Requires Atlassian MCP connection configured in VS Code
metadata:
  author: accruent
  version: "1.0"
---

# Jira Bug Fetcher

This skill retrieves bug information from Jira and formats it for the bug-fixing workflow.

## When to Use

- User provides a Jira ticket key (e.g., EMS-1234, PROJ-567)
- User wants to start fixing a bug
- Need to fetch bug context for research
- Starting the bug-fixing workflow pipeline

## Prerequisites

- Atlassian MCP must be configured and connected
- User must have access to the Jira project containing the ticket

## Process

### Step 1: Create Directory Structure

Before fetching the ticket, create the bug context directory:

```
context/bugs/{TICKET-ID}/
├── research/           # Will contain research documents
└── bug-context.md      # Main bug context file
```

### Step 2: Fetch the Issue

Use `mcp_atlassian-mcp_search` to search for the ticket:

```
Query: "{TICKET-ID}"
```

This returns the issue details including:
- Summary (title)
- Description
- Status, Priority
- Reporter, Assignee
- Comments
- Attachments metadata

### Step 3: Extract Key Fields

From the Jira response, extract and format:

| Field | Source | Notes |
|-------|--------|-------|
| Title | `summary` | Main bug title |
| Description | `description` | Full description, preserve formatting |
| Status | `status.name` | Current workflow status |
| Priority | `priority.name` | Bug priority level |
| Reporter | `reporter.displayName` | Who reported the bug |
| Created | `created` | When bug was created |
| Steps to Reproduce | `description` or custom field | Extract from description if not separate |
| Expected Behavior | `description` or custom field | May need parsing |
| Actual Behavior | `description` or custom field | May need parsing |
| Acceptance Criteria | `customfield_10035` | If available |
| Comments | Via search or nested data | Chronological order |
| Attachments | `attachment` array | List with metadata |

### Step 4: Process Attachments

For each attachment:
1. Record filename, size, content type
2. Note the download URL for manual retrieval if needed
3. For images: describe that they exist and their likely purpose

### Step 5: Create Bug Context Document

Create `context/bugs/{TICKET-ID}/bug-context.md` using the template below.

## Output Template

See [templates/bug-context-template.md](templates/bug-context-template.md) for the full template.

## Error Handling

### Issue Not Found
```
⚠️ JIRA ISSUE NOT FOUND

Could not find issue: {TICKET-ID}

Possible causes:
1. Ticket key is incorrect
2. You don't have access to this project
3. MCP connection issue

Please verify the ticket key and try again.
```

### MCP Connection Issues
```
⚠️ ATLASSIAN MCP CONNECTION ERROR

Could not connect to Jira.

Please verify:
1. Atlassian MCP is configured in VS Code
2. You are authenticated to Atlassian
3. Network connectivity is available

Try: Check VS Code MCP settings or re-authenticate.
```

## Example Usage

**Input:**
```
Fetch bug EMS-1234
```

**Output:**
- Creates: `context/bugs/EMS-1234/bug-context.md`
- Creates: `context/bugs/EMS-1234/research/` directory
- Reports: Summary of fetched content

## Tips for Best Results

1. **Provide the exact ticket key** - don't abbreviate or modify it
2. **Check MCP status first** if you encounter connection errors
3. **Review the generated context** - you may need to manually add information from attachments
4. **Preserve the directory structure** - other workflow steps depend on it
