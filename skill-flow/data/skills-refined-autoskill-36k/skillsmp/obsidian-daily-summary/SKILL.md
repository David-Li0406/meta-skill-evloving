---
name: obsidian-daily-summary
description: Generate daily summaries for Obsidian daily notes. **Use when** user asks to "create a daily summary", "summarize today", "generate daily summary", or "summarize this day". Aggregates content from meetings, notes, and conversations associated with a specific day to create a comprehensive summary in the daily note.
---

# Obsidian Daily Summary Generator

Generate comprehensive daily summaries by aggregating meetings, notes, and conversations from a specific day.

## Quick Start

**"Create a daily summary"** or **"Summarize today"** = Generate daily summary:
1. Find today's daily note (YYYY-MM-DD.md format)
2. Extract meetings linked to this day (via Dataview query in daily note)
3. Extract notes linked to this day (via Dataview query in daily note)
4. Read "Short Conversations and Notes" section content
5. Generate comprehensive summary of the day
6. Insert summary under `## Daily Summary` header (create if missing)

## Daily Note Structure

Daily notes are located at: `/Users/kevin/Documents/Obsidian/HPE/Daily Notes/YYYY-MM-DD.md`

### Key Sections

- **This Week's Tasks**: Todoist query showing weekly tasks
- **Short Conversations and Notes**: Brief notes and conversation snippets
- **☎️ Meetings**: Dataview query listing meetings where `when=date(this.file.name)`
- **📝 Notes**: Dataview query listing notes where `when=date(this.file.name)`

### Summary Placement

1. **If `## Daily Summary` exists**: Replace/update the content under this header
2. **If `## Daily Summary` does NOT exist**: Insert it directly after the "This Week's Tasks" todoist block (before `## Short Conversations and Notes`)

## Workflow

### Step 1: Identify Target Daily Note

Determine which date to summarize:
- Default: Today's date (current date)
- User can specify: "summarize yesterday", "summarize 2026-01-15", etc.

### Step 2: Read Daily Note Content

Read the daily note file to extract:
- Short conversations and notes section content
- Dataview queries to identify linked meetings and notes

### Step 3: Gather Linked Content

Execute Dataview logic to find associated files:
- **Meetings**: Files in `/Meetings/` with `when=<date>` and `tags: meeting`
- **Notes**: Files in `/Notes/` with `when=<date>` and `tags: note`

Read each linked meeting and note file to understand content.

### Step 4: Generate Summary

Analyze all gathered content and create a summary highlighting:
- Key decisions and outcomes from meetings
- Important discussions and topics
- Action items and follow-ups
- Notable events or conversations from "Short Conversations and Notes"
- Overall themes and priorities for the day

**Format as bulleted lists** organized by topic/meeting, NOT narrative paragraphs. Use clear section headers and concise bullet points.

### Step 5: Insert Summary

Insert or update the `## Daily Summary` section in the daily note:
- If section exists: Update content
- If section doesn't exist: Insert after "This Week's Tasks" block

## Example Summary Format

```markdown
## Daily Summary

### Key Decisions
- Decided to [decision] based on [context]
- Cancelled [meeting/activity] due to [reason]
- Approved [action/plan] with [conditions]

### Project Updates
- **[Project/Team Name]**: [Brief status update]
  - Completed: [specific accomplishments]
  - Blocked: [blockers if any]
  - Next steps: [planned actions]

### Technical Work
- [Person] completed [work item] achieving [outcome]
- [Technical update or milestone]
- [Infrastructure or environment changes]

### Action Items & Follow-ups
- [Person] to [action] by [date/timeframe]
- [Team] needs to [action]
- Outstanding: [pending items]

### Strategic Discussions
- Discussed [topic] with [people]
- Options considered: [brief list]
- Direction: [outcome or preference]
```

## Tips

- **Use bulleted lists** - NOT narrative paragraphs
- Organize by topic/theme with clear section headers (### heading level)
- Focus on outcomes and decisions, not just activities
- Link to people using `[[Last, First|First Last]]` format
- Highlight actionable items with clear ownership
- Keep bullets concise and scannable
- Include context that would be valuable when reviewing this day later
