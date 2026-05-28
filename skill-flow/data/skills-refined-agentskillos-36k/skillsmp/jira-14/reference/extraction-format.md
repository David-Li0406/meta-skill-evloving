# Issue Extraction Format

## Overview

This document defines the standard format for extracting and presenting Jira issue data in PRISM workflows.

## Standard Issue Summary Format

When fetching any Jira issue, use this consistent format:

```markdown
## [{ISSUE-KEY}] {Summary}

**🔗 Link**: [View in Jira](https://resolvesys.atlassian.net/browse/{ISSUE-KEY})

### Details
- **Type**: {Epic|Story|Bug|Task|Subtask}
- **Status**: {Status Name}
- **Priority**: {Priority Level}
- **Assignee**: {Assignee Name or "Unassigned"}
- **Reporter**: {Reporter Name}

### Description
{Description text formatted as markdown}

### Acceptance Criteria
{Extracted AC from description or custom field, formatted as checklist}
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Estimation
- **Story Points**: {Points or "Not estimated"}
- **Original Estimate**: {Hours or "Not set"}
- **Remaining**: {Hours or "Not set"}

### Linked Issues
- **Blocks**: [{KEY}] {Summary}
- **Is Blocked By**: [{KEY}] {Summary}
- **Relates To**: [{KEY}] {Summary}
- **Duplicates**: [{KEY}] {Summary}

### Components & Labels
- **Components**: {Component list or "None"}
- **Labels**: {Label list or "None"}
- **Fix Versions**: {Version list or "None"}

### Recent Comments (Last 3)
1. **{Author}** ({Date}):
   {Comment text}

2. **{Author}** ({Date}):
   {Comment text}

3. **{Author}** ({Date}):
   {Comment text}
```

## Epic-Specific Format

When fetching an Epic, include additional hierarchy information:

```markdown
## [EPIC-KEY] {Epic Name}

**🔗 Link**: [View in Jira](https://resolvesys.atlassian.net/browse/EPIC-KEY)

### Epic Overview
- **Type**: Epic
- **Status**: {Status}
- **Epic Name**: {Epic custom field name}
- **Total Child Stories**: {Count}
- **Total Story Points**: {Sum of child story points}

### Epic Goal
{Epic description/goal}

### Acceptance Criteria
{Epic-level acceptance criteria}

### Child Stories
1. [[STORY-1]] {Summary} - {Status} - {Story Points} SP
2. [[STORY-2]] {Summary} - {Status} - {Story Points} SP
3. [[STORY-3]] {Summary} - {Status} - {Story Points} SP

**Progress**:
- ✅ Done: {count} ({percentage}%)
- 🔄 In Progress: {count}
- 📋 To Do: {count}

### Epic Dependencies
{Linked issues that block or are blocked by this epic}

### Components & Scope
- **Components**: {List}
- **Fix Version**: {Target release}
```

## Story-Specific Format

When fetching a Story:

```markdown
## [STORY-KEY] {Story Title}

**🔗 Link**: [View in Jira](https://resolvesys.atlassian.net/browse/STORY-KEY)

### Story Details
- **Type**: Story
- **Epic**: [[EPIC-KEY]] {Epic Name}
- **Status**: {Status}
- **Priority**: {Priority}
- **Assignee**: {Assignee}
- **Story Points**: {Points} SP

### User Story
{As a [user], I want [feature] so that [benefit]}

### Acceptance Criteria
- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

### Technical Notes
{Extracted from description or comments}

### Subtasks
- [[SUBTASK-1]] {Summary} - {Status}
- [[SUBTASK-2]] {Summary} - {Status}

### Implementation Dependencies
- **Blocks**: {List}
- **Is Blocked By**: {List}
- **Related Stories**: {List}

### Development Context
{Any relevant technical comments, implementation notes, or decisions}
```

## Bug-Specific Format

When fetching a Bug:

```markdown
## [BUG-KEY] {Bug Summary}

**🔗 Link**: [View in Jira](https://resolvesys.atlassian.net/browse/BUG-KEY)

### Bug Details
- **Type**: Bug
- **Severity**: {Priority}
- **Status**: {Status}
- **Assignee**: {Assignee}
- **Reporter**: {Reporter}
- **Environment**: {Affected environment}

### Description
{Bug description}

### Steps to Reproduce
1. {Step 1}
2. {Step 2}
3. {Step 3}

### Expected Behavior
{What should happen}

### Actual Behavior
{What actually happens}

### Screenshots/Logs
{Reference to attachments or inline log snippets}

### Related Issues
- **Duplicates**: {Similar bugs}
- **Related Bugs**: {Potentially related issues}

### Customer Impact
{Extracted from comments or description}

### Investigation Notes
{Recent comments from developers}
```

## Extraction Prompt Templates

### General Issue Extraction

```
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

Format as a clear, structured markdown summary for development context.
```

### Epic with Children Extraction

```
Extract and format this Epic with all child stories:

**Epic Details**:
- Key, Name, Status
- Description and Goal
- Acceptance Criteria

**Child Stories**:
- List all child issues with key, summary, status, story points
- Calculate total story points
- Show completion progress (Done/In Progress/To Do)

**Dependencies**:
- Linked issues that affect this epic

Format as structured markdown with progress metrics.
```

### Story for Development Extraction

```
Extract and format this Story for implementation:

**Story Overview**:
- Key, Title, Epic Link
- Status, Priority, Assignee

**Requirements**:
- User story (As a... I want... So that...)
- Acceptance Criteria (as checklist)

**Technical Context**:
- Technical notes from description
- Implementation comments
- Blocked by / Blocking issues

**Subtasks**:
- List all subtasks with status

Format clearly for developer to start implementation.
```

### Bug Investigation Extraction

```
Extract and format this Bug for investigation:

**Bug Summary**:
- Key, Title, Severity, Status

**Reproduction**:
- Steps to reproduce
- Expected vs Actual behavior

**Customer Impact**:
- Who reported it
- How many affected
- Business impact

**Investigation**:
- Recent comments from team
- Related bugs or patterns

**Environment**:
- Where it occurs
- Version information

Format for support/developer to investigate.
```

## Field Mapping

### Standard Jira Fields to Display Names

| Jira API Field | Display Name |
|----------------|--------------|
| `fields.issuetype.name` | Type |
| `fields.status.name` | Status |
| `fields.priority.name` | Priority |
| `fields.assignee.displayName` | Assignee |
| `fields.reporter.displayName` | Reporter |
| `fields.summary` | Title/Summary |
| `fields.description` | Description |
| `fields.parent.key` | Parent Issue |
| `fields.comment.comments` | Comments |
| `fields.issuelinks` | Linked Issues |
| `fields.labels` | Labels |
| `fields.components` | Components |
| `fields.fixVersions` | Fix Versions |
| `fields.timetracking.originalEstimate` | Original Estimate |
| `fields.timetracking.remainingEstimate` | Remaining Estimate |

### Custom Fields (Instance-Specific)

| Custom Field | Typical ID | Display Name |
|--------------|------------|--------------|
| Epic Link | `customfield_10014` | Epic |
| Story Points | `customfield_10016` | Story Points |
| Sprint | `customfield_10020` | Sprint |
| Epic Name | `customfield_10011` | Epic Name |
| Acceptance Criteria | `customfield_xxxxx` | Acceptance Criteria |

**Note**: Custom field IDs vary by Jira instance. Use AI extraction to find relevant fields generically.

## Acceptance Criteria Extraction

Acceptance Criteria can appear in multiple places:

### From Description

Look for markers in description text:
- "Acceptance Criteria:"
- "AC:"
- "Success Criteria:"
- Lists that follow these markers

### From Custom Field

Some instances have dedicated AC custom field:
- `customfield_xxxxx` (varies by instance)
- Usually contains structured list

### Extraction Strategy

```
1. Check for dedicated AC custom field first
2. If not found, scan description for AC markers
3. Extract list items following markers
4. Format as checklist:
   - [ ] Criterion 1
   - [ ] Criterion 2
5. If no explicit AC found, note: "No explicit acceptance criteria defined"
```

## Handling Missing Data

Not all issues have all fields. Handle gracefully:

```markdown
### Field Display Rules

- **Missing Assignee**: Display "Unassigned"
- **No Story Points**: Display "Not estimated"
- **No Epic Link**: Omit Epic section entirely
- **No Comments**: Display "No comments"
- **No Linked Issues**: Display "No linked issues"
- **No Labels**: Display "None"
- **No Description**: Display "No description provided"
- **No Acceptance Criteria**: Display "No explicit acceptance criteria defined"
```

## Clickable Links

Always include clickable Jira links:

```markdown
**🔗 Link**: [View in Jira](https://resolvesys.atlassian.net/browse/PLAT-123)

**Epic**: [[PLAT-789]](https://resolvesys.atlassian.net/browse/PLAT-789) Authentication System

**Blocked By**: [[PLAT-456]](https://resolvesys.atlassian.net/browse/PLAT-456) Database schema update
```

## Session Caching

When an issue is fetched, cache it for the conversation session:

```markdown
## Cached Issue Data

Store in memory for current conversation:
- Issue key → Full issue data
- Last fetched timestamp
- TTL: End of conversation session

Reuse cached data when:
- Same issue referenced again in conversation
- Reduces API calls
- Ensures consistency during session

Refetch when:
- User explicitly requests refresh
- Cached data is from previous session
- User mentions issue status changed
```

## Formatting Best Practices

### Markdown Elements

✅ **Use**:
- Headers (`##`, `###`) for sections
- Bullet lists for non-sequential items
- Numbered lists for sequential items (steps)
- Checkboxes (`- [ ]`) for acceptance criteria
- Bold (`**text**`) for field names
- Links (`[text](url)`) for Jira references
- Code blocks (` ``` `) for logs or JSON

❌ **Avoid**:
- Excessive nested lists (max 2 levels)
- Tables for small data (use lists instead)
- All-caps text
- Emojis (except standard status icons: ✅ 🔄 📋 🔗)

### Readability

- Keep line length reasonable (~80-100 chars)
- Use blank lines to separate sections
- Indent nested content consistently
- Format dates consistently (YYYY-MM-DD or relative "3 days ago")
- Truncate very long descriptions (show first ~500 chars + "...")

### Context Awareness

Adjust verbosity based on use case:

**For Story Master (Epic Decomposition)**:
- Emphasize epic goal and scope
- Show all child stories
- Highlight gaps or missing stories

**For Developer (Implementation)**:
- Emphasize acceptance criteria
- Show technical notes prominently
- Include blocking issues

**For Support (Bug Investigation)**:
- Emphasize reproduction steps
- Show customer comments
- Highlight related bugs

**For QA (Test Planning)**:
- Emphasize acceptance criteria
- Show expected behavior
- List related test issues

## Examples

See the main [Jira SKILL.md](../SKILL.md) for complete real-world extraction examples.
