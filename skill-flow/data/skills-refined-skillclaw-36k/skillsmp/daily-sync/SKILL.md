---
name: daily-sync
description: Process daily notes, clean interviews, extract tasks, and update the Daily Dashboard.
allowed-tools: Read, Bash, Write, Edit, Glob, Grep, Skill
---

# Daily Sync

Processes daily notes from `~/obsidian/Daily Notes/`, cleans up formatting, extracts todos/tasks, and maintains the Daily Dashboard. Also triggers interview cleanup to ensure action items flow into the dashboard.

## When to Use

- User asks to "sync daily notes" or "process daily notes"
- User wants to update the Daily Dashboard
- End of day to organize captured thoughts and tasks

## Workflow

### 1. Clean Interviews First

Before processing daily notes, run the clean-interviews skill to ensure all interview files are properly structured and have action items extracted:

```
/clean-interviews
```

This ensures:
- Raw interview notes are structured with frontmatter
- Important action items are tagged in `action-items` field
- Interview insights are aggregated to research dashboard

### 2. Scan Daily Notes

Find all markdown files in daily notes folder:

```bash
find ~/obsidian/Daily\ Notes -name "*.md" -type f -mtime -7 | sort
```

Focus on files modified in last 7 days for active processing.

### 3. Read and Parse Notes

For each daily note file:
- Read full contents
- Identify sections (if any headers exist)
- Extract all todos/tasks (lines starting with `- [ ]` or `- [x]`)
- Extract bullet points and thoughts
- Identify any project/topic keywords (e.g., "Project-A", "Project-B", "deployment")

### 4. Clean Up Daily Notes

Apply formatting improvements:
- Add date header if missing (use filename or current date)
- Group related items under topic headers
- Convert loose bullets into proper task format where appropriate
- Preserve original content - only enhance structure

### 5. Extract Tasks by Category

Organize todos into categories:
- **Project-specific** - Related to active projects (Project-A, Project-B, etc.)
- **Technical** - Development, debugging, infrastructure tasks
- **Research** - Investigation, analysis, validation tasks
- **Meetings/Calls** - Scheduled conversations
- **Admin/Ops** - General operational tasks
- **Ideas/Future** - Backlog items, future exploration

### 6. Scan Interviews for Action Items

Check user interviews for action items that should surface on the dashboard:

```bash
find ~/obsidian/Research/User\ interviews -name "*.md" -type f
```

For each interview file:
1. Read the YAML frontmatter
2. Check for `action-items:` field
3. If present, extract items and note the source (interviewee name, date)

**Important:** Only pull items from the `action-items` frontmatter field - not from the Follow-ups section. The clean-interviews skill curates what belongs in frontmatter vs what's just general follow-up notes.

### 7. Update Daily Dashboard

Update `~/obsidian/daily-dashboard.md` with:
- Recent daily notes index (last 7 days)
- Tasks by category (single source of truth for all tasks)
- Interview action items (from frontmatter)
- Quick capture section for new items

**Important:** Tasks appear ONLY in the "Tasks by Category" section. Completed tasks stay in place (marked `[x]`) until archived after 7 days. No duplicate entries across sections.

**Interview Action Items:** Add these under the most appropriate category with a source link:
- Intros/connections: Outreach/Follow-ups
- Follow-up calls: Meetings/Interviews
- Technical investigations: Research/Analysis or Technical/Infrastructure
- Partner investigations: Outreach/Follow-ups

Format: `- [ ] Action item (from [[Interview Name|Interviewee]], YYYY-MM-DD)`

**Deduplication:** Before adding an interview action item, check if it already exists in the dashboard (may have been added manually or in a previous sync). Skip duplicates.

## Daily Dashboard Structure

```markdown
# Daily Dashboard

**Last Updated:** YYYY-MM-DD
**Week:** Mon DD - Sun DD

---

## Recent Daily Notes (Last 7 Days)

- **[YYYY-MM-DD](Daily%20Notes/YYYY-MM-DD.md)** - Brief summary of topics
- **[YYYY-MM-DD](Daily%20Notes/YYYY-MM-DD.md)** - Another day's summary

---

## Tasks by Category

### ${PROJECT}
- [ ] Pending task related to project
- [x] Completed project task

### Technical/Infrastructure
- [ ] Development task
- [ ] Deployment task

### Research/Analysis
- [ ] Investigation needed
- [ ] Data to validate

### Meetings/Interviews
- [ ] Call scheduled
- [ ] Follow-up needed
- Meeting notes (non-checkbox items for records)

### Outreach/Follow-ups
- [ ] Outreach task

### Tooling/Skills
- [ ] Tooling task

### Ideas/Backlog
- [ ] Future exploration
- [ ] Nice-to-have feature

---

## Quick Capture

_Use this section for rapid capture throughout the day_

---

*This dashboard aggregates tasks from daily notes. Use Obsidian's daily note button for quick capture, then run /daily-sync to process.*
```

## Guidelines

### Preserve User Voice

- Don't rewrite user's original notes
- Keep informal language and shorthand
- Only add structure, don't change content

### Smart Categorization

Automatically categorize based on keywords:
- Project-specific keywords → ${PROJECT} category
- "deploy", "contract", "bug", "test" → Technical/Infrastructure
- "interview", "validate", "research", "analyze" → Research/Analysis
- "call", "meeting", "sync" → Meetings
- "maybe", "later", "explore", "idea" → Ideas/Backlog

### Date Handling

- Use ISO format: YYYY-MM-DD
- Link to daily notes using Obsidian wikilink format
- Show current week range in header

### Task Management

- Tasks appear ONLY in "Tasks by Category" section (single source of truth)
- Preserve task state (`[ ]` vs `[x]`)
- Don't duplicate tasks - if task exists in dashboard, update don't add
- Completed tasks stay in place with `[x]` marker until archived
- Archive completed tasks older than 7 days to "Completed This Week" note or remove

## Processing Daily Notes

When cleaning up individual daily note files:

1. **Add structure if missing:**
   ```markdown
   # YYYY-MM-DD

   ## Tasks
   - [ ] Task items here

   ## Notes
   - Thought items here

   ## Meetings
   - Meeting notes here
   ```

2. **Don't over-structure** - if notes are just a quick list, that's fine
3. **Preserve timestamps** if user included them
4. **Link to related docs** if obvious connections exist

## Example Transformation

**Before (raw daily note):**
```markdown
- A/B test volatile assets vs usdc when it comes to offering/issuing the credit
- Not enough credit for full top up, what do we do
- Use permits to move funds (like TWAP) from main account
- team dogan introudced us to for v2
```

**After (cleaned up):**
```markdown
# 2026-01-06

## Project Ideas

- [ ] A/B test volatile assets vs USDC for credit issuance
- [ ] Handle partial credit scenarios (not enough for full top-up)
- [ ] Use permits to move funds (TWAP-style) from main account

## Connections

- Team introduced for V2 work
```

**Dashboard entry:**
```markdown
### ${PROJECT}
- [ ] A/B test volatile assets vs USDC for credit issuance
- [ ] Handle partial credit scenarios (not enough for full top-up)
- [ ] Use permits to move funds (TWAP-style) from main account
```

## Important Notes

- Run this skill on-demand, not automatically
- Always preserve original daily notes - only enhance, never delete content
- If dashboard doesn't exist, create it with the template structure
- Group related tasks together but preserve individual task granularity
- Link back to source daily note for context

## Paths Reference

- Daily notes: `~/obsidian/Daily Notes/`
- Daily dashboard: `~/obsidian/daily-dashboard.md`
- Archive (optional): `~/obsidian/Daily Notes/archive/`

**Note:** Paths can be customized in `~/.claude/config/paths.env`
