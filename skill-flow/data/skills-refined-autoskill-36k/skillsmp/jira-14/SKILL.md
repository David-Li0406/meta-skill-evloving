---
name: jira
description: Jira integration for fetching issue context (Epics, Stories, Bugs) to enhance development workflows. Use for automatic issue detection, retrieving ticket details, acceptance criteria, and linked dependencies.
version: 1.1.0
---

# Jira Integration

## When to Use

- User mentions a Jira issue key (e.g., "PLAT-123")
- Need to fetch Epic details for decomposition
- Retrieve story context for implementation
- Get bug details and reproduction steps
- Check acceptance criteria from tickets
- Review linked issues and dependencies
- Fetch customer comments and context

## What This Skill Does

**Provides read-only Jira integration** to enrich development workflows:

- **Automatic Detection**: Recognizes issue keys in conversation (PLAT-123, ISSUE-456)
- **Context Fetching**: Retrieves full issue details via Jira REST API using curl
- **Structured Formatting**: Presents issue data in clear, development-ready format
- **Linked Issues**: Follows Epic → Story → Task relationships
- **Comment History**: Shows recent comments and customer feedback
- **Acceptance Criteria**: Extracts AC from description or custom fields
- **Dependency Tracking**: Identifies blockers and related issues

## Core Principles

### 🎫 The Jira Integration Mindset

**Automated context retrieval** without leaving your workflow:

- **Proactive Detection**: Automatically spots issue keys in conversation
- **Read-Only**: Safe, non-intrusive access to Jira data
- **Privacy Respecting**: Only fetches explicitly mentioned or approved issues
- **Session Caching**: Stores fetched data for conversation duration
- **Graceful Degradation**: Continues without Jira if unavailable
- **Security First**: Credentials via environment variables only

## Implementation Method

The skill uses **curl via Bash tool** to fetch Jira data:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "https://resolvesys.atlassian.net/rest/api/3/issue/{issueKey}"
```

**Why curl instead of WebFetch:**
- WebFetch doesn't support custom authentication headers
- curl can read credentials directly from environment variables
- Direct API access with Basic Authentication
- Reliable and proven approach

## Quick Start

### Fetch an Issue

**When user mentions issue key:**

1. Detect issue key pattern `[A-Z]+-\d+`
2. Use curl with Bash tool to fetch from Jira API
3. Parse JSON response
4. Format and display structured summary

**Example workflow:**
```
User: "jira PLAT-3213"

Agent executes:
curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-3213"

Parses response and displays formatted issue details
```

### Automatic Issue Detection

**Standard workflow:**

1. User mentions issue key (e.g., "Let's work on PLAT-456")
2. Skill detects pattern matching `[A-Z]+-\d+`
3. Fetches issue details via curl
4. Displays formatted summary
5. Proceeds with requested task using context

### Proactive Inquiry

**When user describes work without ticket:**

```
User: "I need to implement the login feature"
Agent: "Great! Do you have a JIRA ticket number so I can get more context?"
User: "PLAT-456"
Agent: Fetches and displays issue details via curl
```

## Available Commands

All Jira capabilities (when using this skill):

| Command | Purpose |
|---------|---------|
| **Issue Retrieval** | |
| `jira {issueKey}` | Fetch and display full issue details |
| `jira-epic {epicKey}` | Fetch epic and all child stories/tasks |
| `jira-search {jql}` | Search issues using JQL query |
| **Workflow Integration** | |
| `auto-detect` | Enable/disable automatic issue key detection |

→ [API Reference](./reference/api-reference.md)

## Issue Detection Patterns

The skill automatically detects these patterns:

- **Primary Project**: `PLAT-123` (from core-config.yaml defaultProject)
- **Any Project**: `[A-Z]+-\d+` format (e.g., JIRA-456, DEV-789)
- **Multiple Issues**: Detects all issue keys in single message

## Fetching Issues - Implementation

### Step 1: Detect Issue Key

Extract issue key from user message using regex:
```regex
[A-Z]+-\d+
```

### Step 2: Fetch via curl

Use Bash tool to execute curl command:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "https://resolvesys.atlassian.net/rest/api/3/issue/{ISSUE_KEY}" \
  2>&1
```

**Critical points:**
- Use `$JIRA_EMAIL` and `$JIRA_TOKEN` environment variables
- Use `-u` flag for Basic Authentication
- Use `-s` for silent mode (no progress bar)
- Redirect stderr with `2>&1` to catch errors

### Step 3: Parse JSON Response

Use Python one-liner to extract key fields:

```bash
curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123" | \
python -c "
import json, sys
data = json.load(sys.stdin)
fields = data['fields']
print('Key:', data['key'])
print('Type:', fields['issuetype']['name'])
print('Summary:', fields['summary'])
print('Status:', fields['status']['name'])
print('Assignee:', fields.get('assignee', {}).get('displayName', 'Unassigned'))
"
```

### Step 4: Format and Display

Format the extracted data as structured markdown:

```markdown
## 📋 [{ISSUE_KEY}](https://resolvesys.atlassian.net/browse/{ISSUE_KEY})

**Type:** {Type} | **Status:** {Status} | **Priority:** {Priority}
**Assignee:** {Assignee} | **Reporter:** {Reporter}

### Description
{Description text}

### Acceptance Criteria
{Extracted AC or "Not specified"}

### Related Issues
- Blocks: {list}
- Blocked by: {list}
- Parent: [{PARENT}](link)

### Additional Context
- Labels: {labels}
- Components: {components}
- Updated: {date}

[View in Jira](https://resolvesys.atlassian.net/browse/{ISSUE_KEY})
```

## Extracted Information

When fetching issues, the skill extracts:

- **Core Details**: Issue Key, Type (Epic/Story/Bug/Task), Summary, Description
- **Status**: Current status, Priority, Resolution
- **People**: Assignee, Reporter
- **Hierarchy**: Epic Link (for stories), Parent (for subtasks)
- **Estimation**: Story Points, Original/Remaining Estimate
- **Acceptance Criteria**: From description or custom fields
- **Comments**: Last 3 most recent comments with authors
- **Links**: Blocks, is blocked by, relates to, duplicates
- **Metadata**: Labels, Components, Fix Versions

→ [Extraction Details](./reference/extraction-format.md)

## Integration with PRISM Skills

The Jira skill enhances other PRISM skills:

### Story Master (sm)
- Fetch epic details when decomposing
- Retrieve all child stories to avoid duplication
- Extract epic acceptance criteria and goals

### Developer (dev)
- Fetch story/bug implementation context
- Review technical notes in comments
- Check blocking/blocked issues

### Product Owner (po)
- Fetch story details for validation
- Check acceptance criteria completeness
- Review linked dependencies

### QA (qa)
- Fetch story acceptance criteria
- Review test requirements from description
- Check linked test issues

### Support (support)
- Fetch bug details and reproduction steps
- Check existing comments for customer info
- Identify related bugs and patterns

### Architect (architect)
- Fetch epic scope and technical requirements
- Review architectural decisions in comments
- Check component relationships

### Peer (peer)
- Fetch story context for code review
- Verify implementation matches acceptance criteria
- Check for architectural alignment

## Authentication & Security

**Configuration:**

Credentials are configured via Windows environment variables:

```
JIRA_EMAIL=your.email@resolve.io
JIRA_TOKEN=your-jira-api-token
```

**Core config reference** ([core-config.yaml](../../core-config.yaml)):

```yaml
jira:
  enabled: true
  baseUrl: https://resolvesys.atlassian.net
  email: ${JIRA_EMAIL}
  token: ${JIRA_TOKEN}
  defaultProject: PLAT
```

**Security Best Practices:**

- Credentials read from system environment variables
- Never hardcode credentials in code
- Basic Authentication via curl `-u` flag
- Credentials passed securely to curl

**Setup:**

1. Set Windows environment variables (System level):
   - `JIRA_EMAIL` = your Atlassian email
   - `JIRA_TOKEN` = your API token
2. Generate API token at: https://id.atlassian.com/manage-profile/security/api-tokens
3. Restart terminal/IDE after setting variables

→ [Authentication Reference](./reference/authentication.md)

## Error Handling

**Authentication Failed:**
```bash
# Response: "Client must be authenticated to access this resource."
# Action: Verify JIRA_EMAIL and JIRA_TOKEN are set correctly
```

**Issue Not Found (404):**
```bash
# Response: {"errorMessages":["Issue does not exist or you do not have permission to see it."]}
# Action: Verify issue key spelling and user has permission
```

**Network Error:**
```bash
# Response: curl connection error
# Action: Check network connectivity and Jira availability
```

**Graceful Degradation:**
- Display error message to user
- Offer to proceed without Jira context
- Never block workflow on Jira failures

→ [Error Handling Guide](./reference/error-handling.md)

## Best Practices

### Fetching Issues

✅ **DO:**
- Always use environment variables for credentials
- Format output in clear, structured markdown
- Cache fetched issue data for the conversation session
- Include clickable Jira links
- Handle missing fields gracefully
- Check authentication before attempting fetch

❌ **DON'T:**
- Hardcode credentials in commands
- Expose credentials in error messages
- Skip error handling
- Fetch entire project data at once
- Ignore API rate limits

### Workflow Integration

✅ **DO:**
- Proactively detect issue keys in user messages
- Display issue summary before proceeding with task
- Use issue context to inform implementation decisions
- Reference Jira tickets in commit messages

❌ **DON'T:**
- Skip issue detection to save time
- Assume issue data is always current
- Modify Jira issues (read-only integration)


## Example Implementation

### Complete Issue Fetch

```bash
# Step 1: Fetch issue data
ISSUE_DATA=$(curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-3213")

# Step 2: Check for errors
if echo "$ISSUE_DATA" | grep -q "errorMessages"; then
  echo "Error fetching issue"
  exit 1
fi

# Step 3: Extract and format
echo "$ISSUE_DATA" | python -c "
import json, sys
data = json.load(sys.stdin)
fields = data['fields']

print(f\"## 📋 [{data['key']}](https://resolvesys.atlassian.net/browse/{data['key']})\")
print(f\"**Type:** {fields['issuetype']['name']} | **Status:** {fields['status']['name']}\")
print(f\"**Assignee:** {fields.get('assignee', {}).get('displayName', 'Unassigned')}\")
print(f\"\n### Summary\")
print(fields['summary'])
"
```

## Reference Documentation

Core references (loaded as needed):

- **[Quick Reference](./reference/README.md)** - Setup guide and quick start
- **[API Reference](./reference/api-reference.md)** - Jira REST API endpoints and curl usage
- **[Extraction Format](./reference/extraction-format.md)** - Issue data formatting and structure
- **[Authentication](./reference/authentication.md)** - Security and credential management
- **[Error Handling](./reference/error-handling.md)** - Handling API errors gracefully

## Common Questions

**Q: Why use curl instead of WebFetch?**
A: WebFetch doesn't support custom authentication headers needed for Jira API. curl with `-u` flag provides reliable Basic Authentication.

**Q: Do I need to manually invoke this skill?**
A: No! The skill automatically activates when it detects Jira issue keys in conversation.

**Q: Is this read-only?**
A: Yes. This integration only fetches data from Jira, it never creates or modifies issues.

**Q: What if I don't have credentials configured?**
A: The skill gracefully degrades. It will inform you that Jira integration is unavailable and proceed without it.

**Q: How do I verify credentials are working?**
A: Test with: `curl -s -u "$JIRA_EMAIL:$JIRA_TOKEN" "https://resolvesys.atlassian.net/rest/api/3/myself"`

**Q: Can I search for issues using JQL?**
A: Yes! Use `jira-search "project = PLAT AND type = Bug"` to search using Jira Query Language.

## Triggers

This skill activates when you mention:
- Jira issue keys (e.g., "PLAT-123", "JIRA-456")
- "jira" command explicitly
- "get issue" or "fetch ticket"
- "check Jira" or "look up issue"
- When other skills need issue context (SM decomposing epic, Dev implementing story)

---

**Skill Version**: 1.1.0
**Integration Type**: Read-Only (curl + Bash)
**Icon**: 🎫
**Last Updated**: 2025-11-20
**Method**: curl via Bash tool with Basic Authentication
