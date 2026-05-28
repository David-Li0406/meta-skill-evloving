---
name: jira
description: Query and manage JIRA issues using the jira CLI. Search issues, view details, and transition statuses. READ-ONLY by default - always ask user approval before modifying issues.
license: MIT
compatibility: opencode
---

# JIRA CLI Skill

Query and manage JIRA issues for task tracking and project management using the `jira` CLI. This skill is READ-ONLY by default.

## CRITICAL RULES

### READ-ONLY BY DEFAULT

**NEVER execute state-changing commands without explicit user approval.**

Allowed without asking:
- `jira issue list`
- `jira issue view`
- `jira sprint list`
- `jira board list`
- `jira project list`
- `jira me` (view current user)
- Any search or query command

**MUST ASK USER BEFORE (state-changing):**
- `jira issue move` (transition status)
- `jira issue assign`
- `jira issue edit`
- `jira issue comment add`
- `jira issue create`
- `jira issue delete`
- `jira issue link`
- `jira issue clone`
- Any command that creates, modifies, or deletes resources

### Approval Request Format

Before any state-changing operation, ask:

```
I need to run a state-changing JIRA command:
  Command: jira issue move PROJ-123 "In Progress"
  Impact: Will transition issue PROJ-123 to "In Progress" status
  Project: PROJ

Do you approve? (yes/no)
```

## Prerequisites

- `jira` CLI installed (go-jira or jira-cli)
- Authenticated with JIRA instance
- Configuration in `~/.jira.d/config.yml` or `~/.config/.jira/.config.yml`

### Check Authentication

```bash
# Check current user
jira me

# Check available projects
jira project list
```

---

## Searching Issues - Read-Only Commands

### Basic Search

```bash
# List issues assigned to me
jira issue list -a$(jira me)

# List issues assigned to me (alternative)
jira issue list --assignee "currentUser()"

# List issues in a project
jira issue list -p PROJ

# List issues with specific status
jira issue list -p PROJ --status "In Progress"

# List open issues
jira issue list -p PROJ --status "Open"
jira issue list -p PROJ --status "To Do"

# List issues with multiple statuses
jira issue list -p PROJ --status "Open" --status "In Progress"

# Limit results
jira issue list -p PROJ --limit 20
```

### JQL Search (Advanced)

```bash
# Search with JQL
jira issue list --jql "project = PROJ AND status = 'In Progress'"

# Complex JQL queries
jira issue list --jql "project = PROJ AND assignee = currentUser() AND status != Done"

# Search by label
jira issue list --jql "project = PROJ AND labels = 'backend'"

# Search by component
jira issue list --jql "project = PROJ AND component = 'API'"

# Search by priority
jira issue list --jql "project = PROJ AND priority = High"

# Search by type
jira issue list --jql "project = PROJ AND type = Bug"
jira issue list --jql "project = PROJ AND type = Story"
jira issue list --jql "project = PROJ AND type = Task"

# Search by sprint
jira issue list --jql "project = PROJ AND sprint in openSprints()"
jira issue list --jql "project = PROJ AND sprint = 'Sprint 42'"

# Search by date
jira issue list --jql "project = PROJ AND created >= -7d"
jira issue list --jql "project = PROJ AND updated >= -1d"

# Search by text
jira issue list --jql "project = PROJ AND text ~ 'search term'"

# Combine multiple conditions
jira issue list --jql "project = PROJ AND assignee = currentUser() AND status in ('Open', 'In Progress') AND priority in (High, Highest) ORDER BY priority DESC"
```

### Output Formatting

```bash
# Plain output
jira issue list -p PROJ --plain

# JSON output (for parsing)
jira issue list -p PROJ --json

# Custom columns
jira issue list -p PROJ --columns key,summary,status,assignee,priority

# Table format
jira issue list -p PROJ --table
```

---

## Viewing Issues - Read-Only Commands

### View Issue Details

```bash
# View issue details
jira issue view PROJ-123

# View in plain text
jira issue view PROJ-123 --plain

# View in JSON format
jira issue view PROJ-123 --json

# Open issue in browser
jira open PROJ-123
jira browse PROJ-123
```

### View Issue Comments

```bash
# View issue with comments
jira issue view PROJ-123 --comments

# View comments only
jira issue comment list PROJ-123
```

### View Issue History

```bash
# View issue changelog/history
jira issue history PROJ-123

# View worklog
jira issue worklog list PROJ-123
```

### View Linked Issues

```bash
# View issue with links
jira issue view PROJ-123 --links

# View subtasks
jira issue list --jql "parent = PROJ-123"
```

---

## Sprint and Board - Read-Only Commands

### Sprints

```bash
# List sprints for a board
jira sprint list --board-id <board-id>

# List active sprints
jira sprint list --board-id <board-id> --state active

# List sprint issues
jira sprint list --board-id <board-id> --sprint-id <sprint-id>

# View sprint details
jira sprint view <sprint-id>
```

### Boards

```bash
# List all boards
jira board list

# List boards for project
jira board list -p PROJ

# View board details
jira board view <board-id>
```

---

## Transitioning Issues (REQUIRES APPROVAL)

### View Available Transitions

```bash
# List available transitions for an issue (read-only)
jira issue transitions PROJ-123
jira issue move --list PROJ-123
```

### Move Issue to New Status (REQUIRES APPROVAL)

```bash
# Move issue to new status - ASK APPROVAL FIRST
jira issue move PROJ-123 "In Progress"

# Move with comment - ASK APPROVAL FIRST
jira issue move PROJ-123 "Done" --comment "Completed the implementation"

# Move with resolution - ASK APPROVAL FIRST
jira issue move PROJ-123 "Done" --resolution "Fixed"

# Common status transitions - ALL REQUIRE APPROVAL
jira issue move PROJ-123 "To Do"
jira issue move PROJ-123 "In Progress"
jira issue move PROJ-123 "In Review"
jira issue move PROJ-123 "Done"
jira issue move PROJ-123 "Blocked"
```

### Bulk Transitions (REQUIRES APPROVAL)

```bash
# Move multiple issues - ASK APPROVAL FIRST
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue move $issue "In Progress"
done
```

---

## Modifying Issues (REQUIRES APPROVAL)

### Edit Issue

```bash
# Edit summary - ASK APPROVAL FIRST
jira issue edit PROJ-123 --summary "New summary"

# Edit description - ASK APPROVAL FIRST
jira issue edit PROJ-123 --description "New description"

# Edit priority - ASK APPROVAL FIRST
jira issue edit PROJ-123 --priority High

# Edit labels - ASK APPROVAL FIRST
jira issue edit PROJ-123 --label "backend" --label "urgent"

# Edit component - ASK APPROVAL FIRST
jira issue edit PROJ-123 --component "API"

# Edit fix version - ASK APPROVAL FIRST
jira issue edit PROJ-123 --fix-version "1.2.0"
```

### Assign Issue (REQUIRES APPROVAL)

```bash
# Assign to user - ASK APPROVAL FIRST
jira issue assign PROJ-123 "username"

# Assign to self - ASK APPROVAL FIRST
jira issue assign PROJ-123 $(jira me)

# Unassign - ASK APPROVAL FIRST
jira issue assign PROJ-123 --unassign
```

### Add Comment (REQUIRES APPROVAL)

```bash
# Add comment - ASK APPROVAL FIRST
jira issue comment add PROJ-123 "This is my comment"

# Add comment from file - ASK APPROVAL FIRST
jira issue comment add PROJ-123 --file comment.txt

# Add comment with mention - ASK APPROVAL FIRST
jira issue comment add PROJ-123 "[~username] please review"
```

### Link Issues (REQUIRES APPROVAL)

```bash
# Link issues - ASK APPROVAL FIRST
jira issue link PROJ-123 PROJ-456 "blocks"
jira issue link PROJ-123 PROJ-456 "is blocked by"
jira issue link PROJ-123 PROJ-456 "relates to"
jira issue link PROJ-123 PROJ-456 "duplicates"
```

### Log Work (REQUIRES APPROVAL)

```bash
# Log time - ASK APPROVAL FIRST
jira issue worklog add PROJ-123 --time-spent "2h"
jira issue worklog add PROJ-123 --time-spent "1d" --comment "Completed feature"
```

---

## Creating Issues (REQUIRES APPROVAL)

```bash
# Create issue interactively - ASK APPROVAL FIRST
jira issue create -p PROJ -t Task

# Create with details - ASK APPROVAL FIRST
jira issue create -p PROJ -t Task \
  --summary "Implement feature X" \
  --description "Detailed description here"

# Create bug - ASK APPROVAL FIRST
jira issue create -p PROJ -t Bug \
  --summary "Fix login issue" \
  --priority High

# Create story - ASK APPROVAL FIRST
jira issue create -p PROJ -t Story \
  --summary "User can reset password" \
  --label "auth" \
  --component "Authentication"

# Create subtask - ASK APPROVAL FIRST
jira issue create -p PROJ -t Sub-task \
  --parent PROJ-123 \
  --summary "Subtask description"

# Create with assignee - ASK APPROVAL FIRST
jira issue create -p PROJ -t Task \
  --summary "Review PR" \
  --assignee "username"
```

---

## Project Information - Read-Only Commands

```bash
# List all projects
jira project list

# View project details
jira project view PROJ

# List project components
jira project component list PROJ

# List project versions
jira project version list PROJ

# List project issue types
jira project issuetype list PROJ
```

---

## Common Workflows

### Start Working on an Issue

```bash
# 1. Find your assigned issues (read-only)
jira issue list -a$(jira me) --status "To Do"

# 2. View issue details (read-only)
jira issue view PROJ-123

# 3. Move to In Progress - ASK APPROVAL FIRST
jira issue move PROJ-123 "In Progress"
```

### Complete an Issue

```bash
# 1. View current status (read-only)
jira issue view PROJ-123

# 2. Add completion comment - ASK APPROVAL FIRST
jira issue comment add PROJ-123 "Implementation complete, PR #456 merged"

# 3. Move to Done - ASK APPROVAL FIRST
jira issue move PROJ-123 "Done"
```

### Daily Standup Quick View

```bash
# Issues I'm working on
jira issue list --jql "assignee = currentUser() AND status = 'In Progress'"

# Issues I completed recently
jira issue list --jql "assignee = currentUser() AND status = Done AND updated >= -1d"

# Blocked issues
jira issue list --jql "assignee = currentUser() AND status = Blocked"
```

### Sprint Overview

```bash
# Current sprint issues
jira issue list --jql "project = PROJ AND sprint in openSprints()"

# Sprint progress by status
jira issue list --jql "project = PROJ AND sprint in openSprints()" --columns key,summary,status

# Unassigned sprint issues
jira issue list --jql "project = PROJ AND sprint in openSprints() AND assignee is EMPTY"
```

---

## Configuration

### Config File Location

```bash
# Common locations
~/.jira.d/config.yml
~/.config/.jira/.config.yml
~/.config/jira/config.yml
```

### Example Configuration

```yaml
# ~/.jira.d/config.yml
endpoint: https://your-domain.atlassian.net
user: your-email@company.com
login: your-email@company.com

# Default project
project: PROJ

# Default board
board: 42

# Authentication (API token)
# Store token in ~/.jira.d/.token.yml or use environment variable
```

### Environment Variables

```bash
# Set JIRA endpoint
export JIRA_API_URL="https://your-domain.atlassian.net"

# Set authentication
export JIRA_AUTH_TYPE="basic"
export JIRA_API_TOKEN="your-api-token"
```

---

## Troubleshooting

### Authentication Issues

```bash
# Check current auth status
jira me

# Re-authenticate
jira login

# Verify endpoint
jira config
```

### "Issue Not Found"

- Verify issue key format (PROJECT-NUMBER)
- Check project access permissions
- Ensure issue exists: `jira issue view PROJ-123`

### "Transition Not Available"

```bash
# List available transitions
jira issue transitions PROJ-123

# Check issue current status
jira issue view PROJ-123 --json | jq '.status'
```

### "Permission Denied"

- Verify user has permission in the project
- Check project role assignments
- Contact JIRA administrator

---

## Safety Checklist

Before ANY state-changing operation:

1. [ ] Is this a read-only command? If yes, proceed. If no, continue checklist.
2. [ ] Have I asked the user for explicit approval?
3. [ ] Did the user say "yes" or approve the specific command?
4. [ ] Verified correct project context
5. [ ] Understood the impact (what will be created/modified/deleted)

### State-Changing Commands Summary

| Category | Commands Requiring Approval |
|----------|---------------------------|
| Status | `issue move` |
| Assignment | `issue assign` |
| Editing | `issue edit` |
| Comments | `issue comment add` |
| Creation | `issue create` |
| Deletion | `issue delete` |
| Links | `issue link` |
| Worklog | `issue worklog add` |
| Clone | `issue clone` |

---

## Editing Issue Descriptions with Rich Formatting (REQUIRES APPROVAL)

The `jira` CLI `--body` flag converts markdown to plain ADF without panels. For rich formatting with info panels (like the standard Jira task template), use the REST API directly with Atlassian Document Format (ADF) JSON.

### View Existing Issue ADF Structure

```bash
# Get raw ADF JSON to understand existing formatting
jira issue view PROJ-123 --raw | jq '.fields.description'
```

### Update Description with ADF Panels

Use the Jira REST API v3 with proper ADF JSON:

```bash
# Create ADF JSON file
cat <<'EOF' > /tmp/issue-description.json
{
  "fields": {
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "panel",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Description", "marks": [{"type": "strong"}]}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Your description text here."}
              ]
            }
          ],
          "attrs": {"panelType": "info"}
        },
        {
          "type": "panel",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Acceptance Criteria", "marks": [{"type": "strong"}]}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "AC.1", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " First acceptance criterion"}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "AC.2", "marks": [{"type": "strong"}]},
                {"type": "text", "text": " Second acceptance criterion"}
              ]
            }
          ],
          "attrs": {"panelType": "info"}
        },
        {
          "type": "panel",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Technical Solution / Design", "marks": [{"type": "strong"}]}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Link to design: "},
                {"type": "inlineCard", "attrs": {"url": "https://confluence.example.com/page"}}
              ]
            }
          ],
          "attrs": {"panelType": "info"}
        },
        {
          "type": "panel",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "Technical Notes", "marks": [{"type": "strong"}]}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "• First technical note"}
              ]
            },
            {
              "type": "paragraph",
              "content": [
                {"type": "text", "text": "• Second technical note"}
              ]
            }
          ],
          "attrs": {"panelType": "info"}
        }
      ]
    }
  }
}
EOF

# Update issue via REST API - ASK APPROVAL FIRST
source ~/.config/.jira/.credentials
curl -s -X PUT \
  -H "Content-Type: application/json" \
  -u "your-email@company.com:$JIRA_API_TOKEN" \
  "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123" \
  -d @/tmp/issue-description.json
```

### ADF Panel Structure Reference

```
Panel types: "info", "note", "warning", "error", "success"

Key ADF node types:
- panel: Container with colored background
- paragraph: Text block
- text: Inline text (can have marks like "strong", "em", "link")
- bulletList/orderedList: Lists with listItem children
- inlineCard: Rich link preview (for Confluence/Jira links)

Important: In panel nodes, "content" must come before "attrs"
```

### Links in ADF

```json
// Simple link
{"type": "text", "text": "link text", "marks": [{"type": "link", "attrs": {"href": "https://..."}}]}

// Rich card (for Atlassian links - shows preview)
{"type": "inlineCard", "attrs": {"url": "https://confluence.example.com/page"}}
```

---

## Quick Reference Card

### Read-Only (Always Safe)

```bash
jira me                              # Current user
jira project list                    # List projects
jira issue list -p PROJ              # List issues
jira issue view PROJ-123             # View issue
jira issue transitions PROJ-123      # View available transitions
jira sprint list                     # List sprints
jira board list                      # List boards
```

### State-Changing (Always Ask First)

```bash
jira issue move PROJ-123 "Status"    # Change status
jira issue assign PROJ-123 user      # Assign
jira issue edit PROJ-123 --opt val   # Edit fields
jira issue comment add PROJ-123 msg  # Add comment
jira issue create -p PROJ -t Type    # Create issue
```
