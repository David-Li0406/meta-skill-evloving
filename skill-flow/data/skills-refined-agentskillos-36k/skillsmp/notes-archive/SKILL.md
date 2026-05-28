---
name: notes-archive
description: Work with personal notes archive stored in date-based directory structure with Markdown files. Navigate notes by date, ID, or slug. Search content and tags.
---

# Notes Archive Skill

## Archive Structure

**Location**: `$NOTES_PATH` (defaults to `~/Dropbox/Notes` if not set, also accessible via `~/Library/CloudStorage/Dropbox/Notes`)

**Directory Hierarchy**:
```
YYYY/MM/YYYYMMDD_ID[_slug].md
```

**Examples**:
- `2026/01/20260106_8823.md` - no slug
- `2026/01/20260102_8814_todo.md` - with slug
- `2024/12/20241203_6973_disable-letter_opener.md` - descriptive slug

**ID Tracking**: `id.json` contains `{"last_id": 8849}`

**UID (Unique Identifier)**: `YYYYMMDD_ID` - the date+ID prefix uniquely identifies each note

## File Format

**Naming Pattern**: `YYYYMMDD_ID[_slug].md`
- `YYYYMMDD` - Date in ISO-8601 basic format
- `ID` - Sequential number from id.json (zero-padded in old notes 2013-2014, plain integers in modern notes)
- `slug` - Optional suffix: category (`todo`, `backlog`, `weekly`) or descriptive text

**YAML Frontmatter (Optional)**:
```yaml
---
title: Note title
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
slug: short-name
published: true  # For publication to notes.musayev.com
description: Brief description
---
```

**Published Notes**: Notes with `published: true` are included when running `publish-notes` script (generates HTML → pushes to GitHub Pages).

**Content**: Standard Markdown. Mixed English/Russian.

**Task Syntax** (in `*_todo.md` notes):
- `[+]` - Completed
- `[>]` - In progress
- `[ ]` - Pending

## Existing Tooling

**User has established scripts and plugins - DO NOT recreate these.**

**Shell Scripts** (`~/bin/`):
- `new-note` - Creates note with auto-incremented ID, updates id.json, opens in editor
- `latest-note`, `latest-todo`, `latest-backlog`, `latest-weekly` - Opens most recent (skips `99999999_*` pinned notes)
- `commit-notes` - Commits with message "Autocomit"

**Sublime Text Plugins** (`~/.dotfiles/config/sublimetext/`):
- `file_autorename` - Renames file based on frontmatter `slug` field
- `notes_browser` - Browse notes by tags (shows ALL/UNTAGGED + tag list)
- `open_note_reference` - Opens note by UID under cursor

**Pinned Notes**: Files starting with `99999999_*` are skipped by `latest-*` scripts.

## Common Search Patterns

**Find by ID**:
```bash
find . -name "*_8823*.md"
```

**Find by slug**:
```bash
find . -name "*_todo.md"
find . -name "*_backlog.md"
```

**Find by date**:
```bash
ls 2026/01/
ls 2026/01/20260106_*.md
```

**Search content**:
```bash
grep -r "search-term" 2026/
grep -r "^tags:" --include="*.md"
```

**Recent notes**:
```bash
find . -type f -name "*.md" -exec stat -f "%m %N" {} \; | sort -rn | head -20
```

**Active tasks**:
```bash
grep -r "^\[>\]" --include="*_todo.md"
```

**Tag frequency**:
```bash
grep -rh "^tags:" --include="*.md" | sed 's/tags: \[\(.*\)\]/\1/' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn
```

**Archive stats**:
```bash
# Total notes
find . -name "*.md" | wc -l

# By year
for year in [0-9][0-9][0-9][0-9]; do
  count=$(find "$year" -name "*.md" 2>/dev/null | wc -l)
  [ $count -gt 0 ] && echo "$year: $count"
done

# Common slugs
find . -name "*_*.md" | sed 's/.*_\([^.]*\)\.md/\1/' | grep -vE '^\d+$' | sort | uniq -c | sort -rn | head -10
```

## Key Concepts

**Note References**: Notes reference each other using UIDs (`YYYYMMDD_ID` or `YYYYMMDD_ID_slug`). The `open_note_reference` plugin navigates these.

**Tag Organization**: Frontmatter tags used for categorization. `notes_browser` plugin provides tag-based navigation.

**Slug Flexibility**: Can be category markers (`todo`, `weekly`), descriptive (`postgres-debugging`), or absent.

**Archive Evolution**: 17+ years (2009-present), ~8849 notes, git-tracked.

## Usage Guidelines

- Focus on search, analysis, and content-level operations
- Use existing scripts for creation/navigation
- Use `$NOTES_PATH` env var or fallback to `~/Dropbox/Notes`
- Archive is git-tracked - use `commit-notes` to commit
- Preserve frontmatter structure when editing
- UIDs are unique and stable - use for references
