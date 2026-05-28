---
name: synap-assistant
description: Use this skill when you want to capture ideas, track todos, organize projects, or review your personal knowledge system.
---

# synap Assistant

A CLI for externalizing your working memory - capture ideas, projects, features, todos, and questions without the overhead of complex tools.

## Why?

Your brain is for having ideas, not holding them. But sticky notes get lost, notepads pile up unread, and tools like Asana are overkill for personal capture.

**synap** solves this by providing:
- **Zero-friction capture** - dump thoughts in seconds
- **Structured retrieval** - find anything with search and filters
- **AI-assisted triage** - agents help you organize, prioritize, and act

## Agent Mindset

When assisting users with their synap entries:

1. **Capture first, organize later** - Never block on classification during fast capture. Get the thought out, refine later.
2. **Proactive triage** - Regularly surface raw entries needing processing. Don't let the inbox grow stale.
3. **Connect the dots** - Link related entries, identify patterns, consolidate ideas into projects.
4. **Reduce cognitive load** - Present summaries and prioritized lists, not exhaustive dumps.
5. **Preserve context** - Include enough detail for future recall. A cryptic note is useless later.
6. **Respect simplicity** - Simple thoughts don't need tags, priorities, and parents. Don't over-engineer.

## User Preferences (Memory)

synap stores user data in a configurable data directory (default: `~/.config/synap/`).

**Data files (syncable):**
- `entries.json` - Active entries
- `archive.json` - Archived entries  
- `user-preferences.md` - Agent memory / user preferences

**Config files (local only):**
- `config.json` - Settings (including `dataDir` for custom data location)
- `deletion-log.json` - Audit trail for restore

### Custom Data Directory (for sync)

Users can point synap to a custom folder (e.g., a git repo for multi-device sync):

```bash
synap config dataDir ~/synap-data
# Or during setup:
synap setup
```

When custom `dataDir` is set:
- Data files go to the custom location
- Config stays in `~/.config/synap/`
- User can sync data folder via git, Dropbox, iCloud, etc.

### Preferences Operations

- Read preferences at the start of the session.