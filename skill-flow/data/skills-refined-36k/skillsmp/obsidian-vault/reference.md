# Obsidian Vault Quick Reference

This is a condensed reference for quick lookups when working with Kevin's Obsidian vault.

## Directory Quick Map

| What I Need | Directory Path | File Format |
|------------|----------------|-------------|
| Meeting notes | `/Meetings/` | `YYYY-MM-DD - [Name].md` |
| Daily notes | `/Daily Notes/` | `YYYY-MM-DD.md` |
| Person profiles | `/People/` | `[Last], [First].md` |
| SIC project docs | `/SIC/` | Various |
| Templates | `/Templates/` | Various templates |

## Common Search Patterns

### Find Last Meeting with Person
```bash
grep -ri "[person]" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md" | grep -o "^[^:]*" | sort | tail -1
```

### Find Topic Discussion
```bash
grep -ri "[topic]" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"
```

### Find Decisions About Topic
```bash
grep -ri "decide.*[topic]\|[topic].*decide" /Users/kevin/Documents/Obsidian/HPE/Meetings/ --include="*.md"
```

## Todoist Syntax (Updated)
```todoist
name: Task List Name
filter: "#HPE & (today | overdue)"
groupBy: date
sorting:
- date
- priority
```

## File Creation Formats

### Meeting Note
```yaml
---
when: YYYY-MM-DD
tags:
  - meeting
---
# Notable Attendees
- [[Last, First]]

# Subject
- 

# Notes
- 

# Take Aways
- 

# Actions
- 
```

### Person Profile
```yaml
---
aliases:
  - First Last
---

## Overview
- [Role/Title]
```

## Common Teams
- **Green Team**: Daily standups, planning
- **Magenta Team**: Daily standups
- **SIC Team**: Sustainability Insight Center

## Common Meeting Types
- Green Standup
- Magenta Standup
- Aruba Weekly Sync
- SIC Istanbul Sync
- Storage Interlock
- COM Interlock
- 1-1 meetings

## Wiki Link Patterns
- People: `[[Last, First]]` or `[[First Last]]` (via alias)
- Projects: `[[SIC/Sustainability Insight Center]]`
- Notes: `[[Note Name]]`

## Tags
- `#meeting` - Meeting notes
- `#note` - General notes
- `#HPE` - Work-related tasks (Todoist)

## Key Locations
- Vault root: `/Users/kevin/Documents/Obsidian/HPE/`
- Daily template: `/Templates/Daily Template.md`
- Meeting template: `/Templates/Meeting Notes.md`

## Installed Plugins
- calendar
- dataview
- templater-obsidian
- todoist-sync-plugin
- buttons
- periodic-notes
- nldates-obsidian
- obsidian-jira-issue
- obsidian-omnivore
- obsidian-outliner
- editing-toolbar

---

**Pro Tip**: Always search in specific directories (`/Meetings/`, `/People/`, `/SIC/`) rather than broad searches across the entire vault.
