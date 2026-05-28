---
name: org-roam-knowledge-mgmt
description: Use when working with Jeff's org-roam notes, daily journals, agenda system, or capture workflows for personal knowledge management
---

# Org-roam Knowledge Management System

## Overview

**Personal Knowledge Management**: Jeff uses org-roam for bidirectional linking, daily journals, and agenda/task management.

**Core principle**: Atomic notes + bidirectional links + daily journals + agenda integration = knowledge system

## When to Use

Use this skill when:
- Creating/modifying org-roam notes
- Working with daily journal entries
- Setting up capture templates
- Debugging agenda file issues
- Understanding directory structure

## Quick Reference

### Key Functions

| Task | Function | Keybinding |
|------|----------|------------|
| Find/open note | `org-roam-node-find` | `C-c n f` |
| Insert link | `org-roam-node-insert` | `C-c n i` |
| Create note | `org-roam-capture` | `C-c n c` |
| Today's journal | `org-roam-dailies-goto-today` | `C-c n d` |
| Refresh agenda | `jf/refresh-org-agenda-files` | `C-c r` |
| Open agenda | `org-agenda` | `C-c a` |
| Show backlinks | `org-roam-buffer-toggle` | (manual) |

### Directory Structure

```
~/org/
├── roam/                      # org-roam-directory
│   ├── dailies/{hostname}/    # Machine-specific journals (YYYY-MM-DD.org)
│   └── *.org                  # Knowledge notes (timestamp-slug.org)
└── agenda/                    # Other org files
```

**Agenda scans**: `~/org/` and `~/src/dotfiles/emacs/` recursively

## Core Workflows

### Daily Journal
- `C-c n d` opens today's journal
- Location: `~/org/roam/dailies/{hostname}/YYYY-MM-DD.org`
- Template: Meetings, Worklog, Tasks sections
- Machine-specific (work/home separation)

### Knowledge Notes
- `C-c n c` creates note with timestamp + slug filename
- `C-c n i` links to existing note (creates if missing)
- `C-c n f` finds and opens notes
- Backlinks via `org-roam-buffer-toggle`

### Capture Templates

**Standard** (`org-roam-capture-templates`):
- "d" default: Basic note
- "f" foo: Structured template from file

**Web** (`org-roam-capture-ref-templates`):
- "r" ref: General web reference
- "b" browser-history: Browser integration with URL refs

Template structure:
```elisp
'(("key" "description" plain "%?"
   :if-new (file+head "path/${slug}.org" "#+title: ${title}\n")
   :unnarrowed t))
```

## Configuration

### Key Variables
- `org-roam-directory`: `~/org/roam/`
- `org-roam-dailies-directory`: `dailies/{hostname}/`
- `find-file-visit-truename`: Follow symlinks
- `org-roam-completion-everywhere`: Enable in all org files

### Agenda System
- Auto-refresh on agenda mode entry
- Manual refresh: `C-c r`
- Scans directories recursively
- Priority-based views available

## Node Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `#+title:` | Note title | `#+title: Emacs Configuration` |
| `ROAM_REFS` | External URLs | `:ROAM_REFS: https://example.com` |
| Tags | Categorization | `#+filetags: :emacs:config:` |

## Org-roam Protocol (Web Capture)

**Setup**: Requires `(server-start)` in config
**Usage**: Browser bookmarklet → captures page with URL as ROAM_REFS
**Integration**: Works with browser-hist for history analysis

## Common Mistakes

| Mistake | Why Bad | Fix |
|---------|---------|-----|
| Agenda files stale | Missing TODOs | Run `C-c r` to refresh |
| Wrong dailies directory | Can't find journals | Check `org-roam-dailies-directory` matches hostname |
| No backlinks | Isolation, no connections | Use `C-c n i` to create links |
| Server not running | Protocol won't work | Add `(server-start)` to config |
| Absolute paths in templates | Breaks portability | Use relative paths or variables |
| Not using machine-specific dailies | Work/personal mixing | Use `{hostname}` in dailies path |

## Best Practices

- **Atomic notes**: One concept per note
- **Link liberally**: Use `C-c n i` frequently
- **Daily capture**: Use journals for temporal entries
- **Regular review**: Check agenda for tasks
- **Web integration**: Capture URLs with context
- **Backlink review**: Discover connections via org-roam buffer
