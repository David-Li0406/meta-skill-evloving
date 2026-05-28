---
name: sync-dashboard
description: Update the Obsidian research dashboard after creating new research documents or when project status changes. Use when user asks to sync dashboard, update research tracking, or after completing significant research work.
allowed-tools: Read, Bash, Edit, Glob, Grep
---

# Sync Dashboard

Updates `~/obsidian/research-dashboard.md` with recent research documents, status changes, and task updates.

## When to Use

- After creating significant research documents
- When project status or decisions change
- When user explicitly asks to sync or update dashboard
- Weekly task refresh

## Workflow

### 1. Archive Current Dashboard

**When to archive (before updating):**
- Major status changes (phase transitions)
- New research with changed conclusions
- Weekly review (7+ days since last archive)
- NOT required for minor content additions

Run the archive script to capture current state:

```bash
bash ~/.claude/scripts/archive-dashboard.sh
```

This creates timestamped snapshot and diff before making changes.

### 2. Scan Recent Research

Find documents created/modified in the last 7 days:

```bash
find ~/obsidian/Research -name "*.md" -type f -mtime -7 -exec ls -lt {} + | head -20
```

Read each recent document to understand:
- What it covers
- Key findings or decisions
- Numbers or projections (confirmed vs modeled)
- What needs validation

### 3. Read Current Dashboard

```bash
cat ~/obsidian/research-dashboard.md
```

Note current state:
- Active project and stage
- This week's tasks (what's checked/unchecked)
- Latest documents section
- Key numbers and decisions

### 4. Identify Changes

Compare recent documents to dashboard:
- New research documents not yet linked
- Changed status (validation phase → implementation, etc.)
- Completed tasks that should be checked off
- New numbers that replace old assumptions
- Decisions made that update "Key Decisions Needed"
- New critical questions answered

### 5. Apply Updates

Use Edit tool to update dashboard sections:
- Latest Research Documents: Add new links chronologically
- Current Status: Update phase/stage
- This Week's Critical Tasks: Check off completed, add new
- Key Decisions Needed: Update or remove resolved decisions
- What We Actually Know: Move items from "Need Validation" to "Confirmed"
- Key Numbers: Update with new data, note if still modeled

### 6. Verify

Read the updated dashboard to confirm:
- All new documents linked
- Status accurate
- Tasks reflect reality
- Numbers current
- No broken links

## Guidelines

### Maintain Existing Structure

Do NOT redesign the dashboard. Preserve:
- Section order and headers
- Formatting style (markdown lists, bold, etc.)
- Tone and language
- Date format (YYYY-MM-DD)

### Chronological Organization

Latest Research Documents section:
- **This Week** section first (current week's docs)
- **Previous Week** section below
- Move docs from "This Week" to "Previous Week" when they age
- Within each section: newest first

### Link Format

Use Obsidian wikilink format with display text:
```
- **[Document Title](Research/Subfolder/2026-01-08-filename.md)** - Brief description
```

### Facts vs Assumptions

When updating numbers:
- Mark clearly if "Confirmed" or "Modeled"
- In "What We Actually Know" section, only move to Confirmed if there's actual validation
- Keep modeling assumptions visible

### Task Hygiene

- Check off completed tasks: `- [x] Task name`
- Remove tasks that are no longer relevant (don't leave them unchecked)
- Add new tasks discovered during research
- Keep list focused: 3-5 critical tasks

### Date Management

Update "Last Updated" field at top:
```
**Last Updated:** YYYY-MM-DD
```

Use current date when syncing.

## Example Updates

### Adding New Document

Before:
```markdown
### This Week (Jan 6-8)
- **[User Interview Quick Start](Research/Project-A/2026-01-08-user-interview-quick-start.md)** - 10 critical questions
```

After:
```markdown
### This Week (Jan 6-8)
- **[Risk Analysis Framework](Research/Project-A/2026-01-09-risk-analysis.md)** - Default rates and liquidity risks
- **[User Interview Quick Start](Research/Project-A/2026-01-08-user-interview-quick-start.md)** - 10 critical questions
```

### Completing Tasks

Before:
```markdown
- [ ] **User Interviews:** 8-10 target users (Wed-Fri)
```

After:
```markdown
- [x] **User Interviews:** 8-10 target users (completed 10 interviews)
```

### Updating Status

Before:
```markdown
## Current Status: Validation Phase
**Stage:** Active validation - user interviews happening this week
```

After:
```markdown
## Current Status: Decision Phase
**Stage:** Validation complete - analyzing results, making GO/NO-GO decision
```

## Important Notes

- Always archive before updating (captures history)
- Preserve user's voice and formatting
- Focus on factual updates, not editorializing
- Keep dashboard scannable: concise bullets, clear structure
- Link to actual files (verify paths exist)

## Paths Reference

- Dashboard: `~/obsidian/research-dashboard.md`
- Archive script: `~/.claude/scripts/archive-dashboard.sh`
- Research root: `~/obsidian/Research/`
- Active project folder: Check dashboard for current project path

**Note:** Paths can be customized in `~/.claude/config/paths.env`
