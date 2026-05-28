---
name: voice-note-taker
description: Save and structure a voice idea to the knowledge base with automatic GitHub merge
---

# Voice Note Taker Skill

Structure the idea from this conversation and save it to the knowledge base with full automatic GitHub workflow.

## Steps

### 1. Structure the Idea

Based on the conversation, create a structured markdown file:

```markdown
# [Descriptive Title]

## Summary
[2-3 sentences capturing the core idea]

## Key Insights
- [Key point 1]
- [Key point 2]
- [Add more as needed]

## Action Items
- [ ] [Task 1]
- [ ] [Task 2]
- [Add more or remove section if none]

## Connections
- Related to: [topics]
- Source: [if applicable]
```

### 2. Choose the Folder

| Folder | Use When |
|--------|----------|
| `knowledge-base/ideas/` | Raw thoughts, brainstorms, "what if" |
| `knowledge-base/insights/` | Learnings, wisdom, mental models |
| `knowledge-base/actions/` | Tasks, plans, goals, decisions |

### 3. Create Filename

Format: `YYYY-MM-DD-descriptive-slug.md`

Example: `2026-01-22-morning-routine-focus.md`

### 4. Git Workflow (Fully Automatic)

Execute these commands in sequence:

```bash
# Ensure on main and up to date
git checkout main
git pull origin main

# Create branch for this idea
git checkout -b idea/[slug]

# Create the file in the appropriate folder
# (write file content)

# Stage and commit
git add knowledge-base/[folder]/[filename]
git commit -m "Add: [brief topic description]"

# Push the branch
git push -u origin idea/[slug]

# Create PR, merge, and cleanup (automatic!)
gh pr create --title "Add: [brief topic]" --body "Auto-captured idea" --base main
gh pr merge --merge --delete-branch

# Return to main
git checkout main
git pull origin main
```

### 5. Confirm to User

After completing, confirm:
- File saved: `knowledge-base/[folder]/[filename]`
- Automatically merged to main branch
- Ready to capture next idea

## Example

**User says:** "Morning routines reduce decision fatigue because you don't have to think about what to do first thing"

**Result:**
- File: `knowledge-base/insights/2026-01-22-morning-routines-decision-fatigue.md`
- Branch created, PR merged, cleanup complete
- Idea now in main branch
