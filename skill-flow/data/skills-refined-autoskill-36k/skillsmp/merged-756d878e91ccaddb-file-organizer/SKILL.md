---
name: file-organizer
description: Intelligently organize files and folders by understanding context, finding duplicates, and suggesting better structures. Use this skill to clean up directories, organize downloads, remove duplicates, or restructure projects.
---

# File Organizer

Your personal organization assistant for maintaining clean, logical file structures without mental overhead.

## When to Use

- Your Downloads folder is chaotic
- You can't find files because they're scattered everywhere
- You have duplicate files taking up space
- Your folder structure doesn't make sense anymore
- You want to establish better organization habits
- You're starting a new project and need a good structure
- You're cleaning up before archiving old projects

## Core Capabilities

1. **Analyze Structure**: Review folders and understand content
2. **Find Duplicates**: Identify duplicate files across the system
3. **Suggest Organization**: Propose logical folder structures
4. **Automate Cleanup**: Move, rename, and organize files with approval
5. **Context-Aware**: Make smart decisions based on file types, dates, and content
6. **Reduce Clutter**: Identify old files you probably don't need anymore

## Instructions

When a user requests file organization help:

### 1. Understand Scope

Ask clarifying questions:
- Which directory needs organization? (Downloads, Documents, entire home folder?)
- What's the main problem? (Can't find things, duplicates, too messy, no structure?)
- Any files or folders to avoid? (Current projects, sensitive data?)
- How aggressively to organize? (Conservative vs. comprehensive cleanup)

### 2. Analyze Current State

Review the target directory:

```bash
# Get overview of current structure
ls -la [target_directory]

# Check file types and sizes
find [target_directory] -type f -exec file {} \; | head -20

# Identify largest files
du -sh [target_directory]/* | sort -rh | head -20

# Count file types
find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

Summarize findings:
- Total files and folders
- File type breakdown
- Size distribution
- Date ranges
- Obvious organization issues

### 3. Identify Patterns

Based on the files, determine logical groupings:

**By Type:**
- Documents (PDFs, DOCX, TXT)
- Images (JPG, PNG, SVG)
- Videos (MP4, MOV)
- Archives (ZIP, TAR, DMG)
- Code/Projects (directories with code)
- Spreadsheets (XLSX, CSV)
- Presentations (PPTX, KEY)

**By Purpose:**
- Work vs. Personal
- Active vs. Archive
- Project-specific
- Reference materials
- Temporary/scratch files

**By Date:**
- Current year/month
- Previous years
- Very old (archive candidates)

### 4. Find Duplicates

When requested, search for duplicates:

```bash
# Find exact duplicates by hash
find [directory] -type f -exec md5sum {} \; | sort | uniq -d

# Find files with same name
find [directory] -type f -printf '%f\n' | sort | uniq -d

# Find similar-sized files
find [directory] -type f -printf '%s %p\n' | sort -n
```

For each set of duplicates:
- Show all file paths
- Display sizes and modification dates
- Recommend which to keep (usually newest or best-named)
- **Important**: Always ask for confirmation before deleting

### 5. Propose Organization Plan

Present a clear plan before making changes:

```markdown
# Organization Plan for [Directory]

## Current State
- X files across Y folders
- [Size] total
- File types: [breakdown]
- Issues: [list problems]

## Proposed Structure
[Directory]/
├── Work/
│   ├── Projects/
│   ├── Documents/
│   └── Archive/
├── Personal/
│   ├── Photos/
│   ├── Documents/
│   └── Media/
└── Downloads/
    ├── To-Sort/
    └── Archive/

## Changes I'll Make
1. **Create new folders**: [list]
2. **Move files**:
   - X PDFs → Work/Documents/
   - Y images → Personal/Photos/
   - Z old files → Archive/
3. **Rename files**: [any renaming patterns]
4. **Delete**: [duplicates or trash files]

## Files Needing Your Decision
- [List any files you're unsure about]

Ready to proceed? (yes/no/modify)
```

### 6. Execute Organization

After approval, organize systematically:

```bash
# Create folder structure
mkdir -p "path/to/new/folders"

# Move files with clear logging
mv "old/path/file.pdf" "new/path/file.pdf"

# Rename files with consistent patterns
# Example: "YYYY-MM-DD - Description.ext"
```

**Important Rules:**
- Always confirm before deleting anything
- Log all moves for potential undo
- Preserve original modification dates
- Handle filename conflicts gracefully
- Stop and ask if you encounter unexpected situations

### 7. Provide Summary and Maintenance Tips

After organizing:

```markdown
# Organization Complete! ✨

## What Changed
- Created [X] new folders
- Organized [Y] files
- Freed [Z] GB by removing duplicates
- Archived [W] old files

## New Structure
[Show the new folder tree]

## Maintenance Tips
To keep this organized:
1. **Weekly**: Sort new downloads
2. **Monthly**: Review and archive completed projects
3. **Quarterly**: Check for new duplicates
4. **Yearly**: Archive old files

## Quick Commands for You
# Find files modified this week
find . -type f -mtime -7

# Sort downloads by type
[custom command for their setup]

# Find duplicates
[custom command]
```

## Best Practices

### Folder Naming
- Use clear, descriptive names
- Avoid spaces (use hyphens or underscores)
- Be specific: "client-proposals" not "docs"
- Use prefixes for ordering: "01-current", "02-archive"

### File Naming
- Include dates: "2024-10-17-meeting-notes.md"
- Be descriptive: "q3-financial-report.xlsx"
- Avoid version numbers in names (use version control instead)
- Remove download artifacts: "document-final-v2 (1).pdf" → "document.pdf"

### When to Archive
- Projects not touched in 6+ months
- Completed work that might be referenced later
- Old versions after migration to new systems
- Files you're hesitant to delete (archive first)

## Pro Tips
1. Start small (one folder at a time)
2. Run weekly cleanup on Downloads
3. Use consistent naming: "YYYY-MM-DD - Description"
4. Archive aggressively (don't delete)
5. Keep active work separate from archives
6. Trust the process: let the system handle the cognitive load of where things go