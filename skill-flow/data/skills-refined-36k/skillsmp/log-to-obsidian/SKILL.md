---
name: log-to-obsidian
description: Review a session or the git history for today and summarize this for our daily reporting
license: Apache-2.0
compatibility: opencode
---

## Vault Configuration
Obsidian vault path: "~/Documents/nls"
Daily notes location: "00 Journals/Daily/YYYY-MM-DD.md"

## Quick Start

1. Determine today's date
2. Determine which Area we are working on (Upsun, Side Projects, Personal)
3. Find or create daily note at `{vault}/00 Journals/Daily/YYYY-MM-DD.md`
4. Summarize session activity
5. Append task to the right Area
6. Create a short summary of the changes in the Notes section

## Base Daily Template

```markdown
---
Mood:
Productivity:
Physical:
Food:
---
# Activities
## Upsun
- [ ] 
## Side projects
- [ ] 
## Personal
- [ ] 

---
# Notes

# Retrospection
```

## Process

**Step 1: Locate the daily note**
- Get current date from system
- Build path: `{vault}/00 Journals/Daily/YYYY-MM-DD.md`
- If file doesn't exist, create with frontmatter

**Step 2: Analyze session for loggable content**

Identify:
- Decisions made
- Tasks completed or created
- Project progressed
- Strategic insights
- Next steps identified

**Step 3: Structure the update**
- Add a new task (short text) in the task list in the related Area: Upsun, Side Projects or Personal. The user will specify this.
- Add new sections for distinct topics in the Notes section. Add a paragraph with a summary of the changes and actions.
- Update existing sections if adding to prior content

**Step 4: Append to daily note**
- Preserve all existing content
- Add new sections in logical order
- Use consistent markdown formatting

## Formatting Guidelines

**Section headers:** Use `### Section Name` for main topics


## Success Criteria

- [ ] Daily note exists at correct path
- [ ] All significant session activity captured
- [ ] Content organized into logical sections