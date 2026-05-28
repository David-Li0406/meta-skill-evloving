# Jira REST API Reference

## Overview

This document provides detailed information about using the Jira REST API v3 for fetching issue context in PRISM workflows.

## Base Configuration

From [core-config.yaml](../../../core-config.yaml):

```yaml
jira:
  enabled: true
  baseUrl: https://resolvesys.atlassian.net
  email: ${JIRA_EMAIL}
  token: ${JIRA_API_TOKEN}
  defaultProject: PLAT
  issueKeyPattern: "[A-Z]+-\\d+"
```

## Authentication

All API requests require Basic Authentication:

```
Authorization: Basic base64(email:token)
```

Where:
- `email`: Your Atlassian account email (from `JIRA_EMAIL` env var)
- `token`: Your Jira API token (from `JIRA_API_TOKEN` env var)

**Security Notes:**
- Never hardcode credentials in code
- Never embed credentials in URLs
- WebFetch tool handles authentication securely
- Credentials are read from environment variables via core-config.yaml

## API Endpoints

### 1. Get Issue Details

**Endpoint:**
```
GET /rest/api/3/issue/{issueKey}
```

**URL Example:**
```
https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123
```

**Response Fields:**
- `key`: Issue key (e.g., "PLAT-123")
- `fields.summary`: Issue title
- `fields.description`: Full description (Atlassian Document Format)
- `fields.issuetype.name`: Type (Epic, Story, Bug, Task, Subtask)
- `fields.status.name`: Current status
- `fields.priority.name`: Priority level
- `fields.assignee`: Assignee details
- `fields.reporter`: Reporter details
- `fields.parent`: Parent issue (for Subtasks)
- `fields.customfield_xxxxx`: Epic Link (custom field ID varies)
- `fields.timetracking`: Original/remaining estimates
- `fields.customfield_xxxxx`: Story Points (custom field ID varies)
- `fields.comment.comments[]`: Array of comments
- `fields.issuelinks[]`: Linked issues
- `fields.labels[]`: Labels
- `fields.components[]`: Components
- `fields.fixVersions[]`: Fix versions

**Usage with WebFetch:**
```
WebFetch:
  url: https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123
  prompt: |
    Extract and format the following information from this Jira issue:
    - Issue Key and Type (Epic/Story/Bug/Task)
    - Summary and Description
    - Status and Priority
    - Assignee and Reporter
    - Epic Link (if applicable)
    - Story Points (if applicable)
    - Acceptance Criteria (from description or custom field)
    - Comments (last 3 most recent)
    - Linked Issues (blocks, is blocked by, relates to)
    - Labels and Components

    Format as a clear, structured summary for development context.
```

### 2. Search Issues (JQL)

**Endpoint:**
```
GET /rest/api/3/search?jql={query}
```

**URL Example:**
```
https://resolvesys.atlassian.net/rest/api/3/search?jql=project=PLAT+AND+type=Epic
```

**Common JQL Queries:**

**Get all epics in project:**
```jql
project = PLAT AND type = Epic
```

**Get all child stories of an epic:**
```jql
parent = PLAT-789
```

**Get all open bugs:**
```jql
project = PLAT AND type = Bug AND status != Done
```

**Get issues assigned to me:**
```jql
project = PLAT AND assignee = currentUser()
```

**Get recently updated issues:**
```jql
project = PLAT AND updated >= -7d
```

**Response Structure:**
```json
{
  "total": 25,
  "maxResults": 50,
  "startAt": 0,
  "issues": [
    {
      "key": "PLAT-123",
      "fields": { ... }
    }
  ]
}
```

**Usage with WebFetch:**
```
WebFetch:
  url: https://resolvesys.atlassian.net/rest/api/3/search?jql=parent=PLAT-789
  prompt: |
    List all issues returned from this search.
    For each issue, extract:
    - Issue Key
    - Type
    - Summary
    - Status
    - Assignee

    Format as a numbered list.
```

### 3. Get Epic Issues

**Endpoint:**
```
GET /rest/api/3/search?jql=parent={epicKey}
```

**URL Example:**
```
https://resolvesys.atlassian.net/rest/api/3/search?jql=parent=PLAT-789
```

**Purpose:**
Retrieves all Stories, Tasks, and Subtasks that belong to a specific Epic.

**Usage:**
Essential for Story Master when decomposing epics to:
- See existing child stories
- Avoid duplication
- Understand epic scope
- Identify gaps in decomposition

**Usage with WebFetch:**
```
WebFetch:
  url: https://resolvesys.atlassian.net/rest/api/3/search?jql=parent=PLAT-789
  prompt: |
    List all child stories/tasks for this epic.
    For each, extract:
    - Issue Key
    - Summary
    - Status
    - Story Points (if available)

    Calculate total story points across all children.
```

### 4. Get Issue Comments

**Endpoint:**
```
GET /rest/api/3/issue/{issueKey}/comment
```

**URL Example:**
```
https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123/comment
```

**Response:**
```json
{
  "comments": [
    {
      "id": "12345",
      "author": {
        "displayName": "John Doe",
        "emailAddress": "john@example.com"
      },
      "body": { ... },
      "created": "2025-01-15T10:30:00.000+0000",
      "updated": "2025-01-15T10:30:00.000+0000"
    }
  ]
}
```

**Note:** Comments are included in issue details response by default. Use this endpoint only if you need ALL comments (issue details returns recent comments only).

### 5. Get Issue Transitions

**Endpoint:**
```
GET /rest/api/3/issue/{issueKey}/transitions
```

**Note:** This is a read-only integration. We do not modify issues, so transition endpoints are informational only.

## Rate Limiting

Jira Cloud enforces rate limits:

**Limits:**
- **Per-user**: 300 requests per minute
- **Per-app**: Based on your plan

**Best Practices:**
- Cache issue data for the conversation session
- Avoid fetching same issue multiple times
- Use search queries to fetch multiple issues in one request
- Batch operations when possible

**Handling Rate Limits:**
If you receive 429 (Too Many Requests):
```
Display: "Jira rate limit reached. Please wait a moment before fetching more issues."
Action: Wait and retry, or proceed without additional Jira data
```

## Custom Fields

Many Jira fields are custom and vary by instance:

**Common Custom Fields:**
- **Epic Link**: `customfield_10014` (varies by instance)
- **Story Points**: `customfield_10016` (varies by instance)
- **Sprint**: `customfield_10020` (varies by instance)
- **Epic Name**: `customfield_10011` (for Epic issues)

**Finding Custom Field IDs:**
1. Fetch any issue and examine the response
2. Look for `customfield_*` entries
3. Match field names to IDs in your instance

**Usage Tip:**
Use the WebFetch extraction prompt to handle custom fields generically:
```
Extract story points if available (may be in customfield_10016 or similar)
```

The AI extraction will find the relevant field without hardcoding IDs.

## Response Formats

### Atlassian Document Format (ADF)

Jira descriptions and comments use ADF (JSON structure):

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "This is the description"
        }
      ]
    }
  ]
}
```

**Handling ADF:**
Use WebFetch's AI extraction to convert ADF to readable text:
```
prompt: "Extract the description text from this issue and format as plain markdown"
```

## Error Codes

**400 Bad Request:**
- Invalid JQL syntax
- Malformed request

**401 Unauthorized:**
- Missing or invalid credentials
- Expired API token

**403 Forbidden:**
- User lacks permission to view issue
- Issue is in restricted project

**404 Not Found:**
- Issue key does not exist
- Issue was deleted

**429 Too Many Requests:**
- Rate limit exceeded
- Wait and retry

**500 Internal Server Error:**
- Jira service issue
- Retry or proceed without Jira data

## Example WebFetch Usage

### Fetch Single Issue

```javascript
// In Claude Code workflow
WebFetch({
  url: "https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123",
  prompt: `
    Extract and format this Jira issue:

    **[PLAT-123]**: {summary}

    **Type**: {type}
    **Status**: {status}
    **Priority**: {priority}

    **Description**:
    {description as markdown}

    **Acceptance Criteria**:
    {extract AC from description if present}

    **Assignee**: {assignee name}
    **Reporter**: {reporter name}

    **Linked Issues**:
    - {list linked issues with relationship type}

    **Comments** (last 3):
    - {author}: {comment text}
  `
})
```

### Search for Epic Children

```javascript
WebFetch({
  url: "https://resolvesys.atlassian.net/rest/api/3/search?jql=parent=PLAT-789",
  prompt: `
    List all child stories for this epic:

    1. [PLAT-XXX] {summary} - {status} - {story points}
    2. [PLAT-YYY] {summary} - {status} - {story points}

    Total Story Points: {sum of all story points}
    Completed: {count of Done stories}
    In Progress: {count of In Progress stories}
    Todo: {count of To Do stories}
  `
})
```

## Testing

**Verify Configuration:**
```bash
# Check environment variables
echo $JIRA_EMAIL
echo $JIRA_API_TOKEN

# Test API connection
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  https://resolvesys.atlassian.net/rest/api/3/myself
```

**Test Issue Fetch:**
```bash
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123
```

## References

- [Jira REST API v3 Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [JQL (Jira Query Language)](https://support.atlassian.com/jira-service-management-cloud/docs/use-advanced-search-with-jira-query-language-jql/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
