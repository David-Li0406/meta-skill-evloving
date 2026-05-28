---
name: fetch-ticket
description: Skill for retrieving tickets from various sources (YouTrack, GitHub, file). Detects source automatically from ticket ID pattern and outputs normalized markdown format.
---

# Fetch Ticket Skill

This skill retrieves ticket/issue information from various sources and normalizes it to a consistent markdown format.

## Supported Sources

### 1. YouTrack (via MCP)
- **Pattern**: `PROJ-123`, `ABC-1`, any `UPPERCASE-NUMBER` format
- **Tool**: `mcp__youtrack__get_issue`
- **Also fetches**: Comments via `mcp__youtrack__get_issue_comments`

### 2. GitHub (via gh CLI)
- **Pattern**: `#123`, `123` (when github repo configured), `owner/repo#123`
- **Tool**: `gh issue view` or `gh pr view`
- **Detection**: Attempts issue first, falls back to PR

### 3. File (manual input)
- **Pattern**: Path to existing `.md` file
- **Use case**: When ticket is already saved or provided externally

## Source Detection Logic

```
Input ID → Detect Source
├── Matches /^[A-Z]+-\d+$/ → YouTrack
├── Matches /^#?\d+$/ → GitHub (issue/PR number)
├── Matches /^[\w-]+\/[\w-]+#\d+$/ → GitHub (explicit repo)
├── File exists at path → File
└── Otherwise → Error: Unknown format
```

## Retrieval Process

### YouTrack

1. Call `mcp__youtrack__get_issue` with issueId
2. Call `mcp__youtrack__get_issue_comments` for discussion context
3. Extract fields:
   - `summary` → Title
   - `description` → Description
   - `state.name` → Status
   - `priority.name` → Priority
   - `type.name` → Type
   - `assignee.name` → Assignee
   - `tags[].name` → Labels
   - `customFields` → Additional metadata

#### Target Branch Extraction from Milestone

When processing YouTrack issues, extract the target branch from milestone/sprint fields:

1. **Look for milestone fields** in customFields:
   - "Milestone", "Sprint", "Fix versions", "Target Version"

2. **Parse milestone format** to extract branch:
   - Format: `YYYY-MM-suffix` (e.g., "2025-12-continue", "2026-01")
   - Extract: `YYYY-MM` as branch name (e.g., "2025-12", "2026-01")

3. **Verify branch exists on origin**:
   ```bash
   git ls-remote --heads origin "{extracted-branch}" 2>/dev/null
   ```
   - If branch exists → use as Target Branch
   - If branch does NOT exist → target branch is `main` (release branch not yet created)

4. **Add to metadata table**:
   ```markdown
   | Target Branch | {branch} |
   ```

**Example**:
- Milestone: "2025-12-continue" → Target Branch: "2025-12" (if exists on origin)
- Milestone: "2026-01" → Target Branch: "main" (if 2026-01 doesn't exist on origin yet)

### GitHub

1. Run `gh issue view <number> --json title,body,state,labels,assignees,milestone,comments`
2. If 404, try `gh pr view <number> --json ...`
3. Extract fields:
   - `title` → Title
   - `body` → Description
   - `state` → Status
   - `labels[].name` → Labels
   - `assignees[].login` → Assignees
   - `comments[].body` → Discussion

### File

1. Read file content
2. Parse frontmatter if present (YAML between `---`)
3. Use content as-is or extract structured data

## Output Format

All sources output a normalized markdown document:

```markdown
---
source: youtrack|github|file
ticket_id: PROJ-123
fetched_at: 2024-01-15T10:30:00Z
url: https://...
---

# [Ticket Title]

## Metadata

| Field | Value |
|-------|-------|
| Status | Open |
| Type | Feature |
| Priority | High |
| Assignee | @username |
| Labels | label1, label2 |

## Description

[Original ticket description]

## Comments

### Comment by @author (2024-01-14)

[Comment content]

---

### Comment by @author2 (2024-01-15)

[Comment content]
```

## Error Handling

### YouTrack Errors
- **MCP unavailable**: Return error with message "YouTrack MCP server not available. Ensure it's configured in Claude settings."
- **Issue not found**: Return error with message "Issue {id} not found in YouTrack"
- **Permission denied**: Return error with message "Access denied to issue {id}"

### GitHub Errors
- **gh not authenticated**: Return error with message "GitHub CLI not authenticated. Run: gh auth login"
- **Issue/PR not found**: Return error with message "Issue/PR #{number} not found in repository"
- **Repository not specified**: Return error with message "GitHub repository not specified. Use format owner/repo#123 or configure in ticket-config.json"

### File Errors
- **File not found**: Return error with message "Ticket file not found: {path}"
- **Invalid format**: Return error with message "Could not parse ticket file: {path}"

## Usage in Workflow

This skill is typically invoked by:
1. `/resolve` command - as first step
2. `/fetch-ticket` standalone command
3. Other skills needing ticket data

## Configuration Integration

Reads from project's `.claude/ticket-config.json`:
- `default_source`: Preferred source when ambiguous
- `youtrack.project_prefix`: Default prefix for short IDs
- `github.repo`: Default repository for GitHub issues

## Implementation Steps

When invoked:

1. **Parse input** to determine ticket ID and potential source
2. **Load config** from `.claude/ticket-config.json` if exists
3. **Detect source** using patterns above
4. **Fetch data** using appropriate method
5. **Normalize output** to standard markdown format
6. **Return** the formatted ticket document

## Language

Output ticket content in its original language. Metadata labels in English for consistency.
