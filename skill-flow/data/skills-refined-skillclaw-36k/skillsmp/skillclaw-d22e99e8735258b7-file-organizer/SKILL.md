---
name: file-organizer
description: Use this skill when you need to intelligently organize files and folders, find duplicates, and suggest better structures for a cleaner digital workspace.
---

# File Organizer

Your personal organization assistant for maintaining clean, logical file structures without mental overhead.

## When to Use

- Downloads folder is chaotic
- Can't find files (scattered everywhere)
- Duplicate files taking up space
- Folder structure doesn't make sense
- Need better organization habits
- Starting new project structure
- Cleaning up before archiving

## Core Capabilities

1. **Analyze Structure**: Review folders and understand content.
2. **Find Duplicates**: Identify duplicate files across the system.
3. **Suggest Organization**: Propose logical folder structures.
4. **Automate Cleanup**: Move, rename, and organize files with user approval.
5. **Context-Aware**: Make smart decisions based on file type, date, and content.
6. **Reduce Clutter**: Identify old and unused files.

## Quick Commands

### Downloads Cleanup
```
Organize Downloads folder - move documents to Documents, images to Pictures, archive files older than 3 months.
```

### Find Duplicates
```
Find duplicate files in Documents and help me decide which to keep.
```

### Project Organization
```
Review Projects folder and separate active from archived projects.
```

### Desktop Cleanup
```
Desktop is covered in files - organize into Documents properly.
```

### Photo Organization
```
Organize photos by date (year/month) based on EXIF data.
```

### Work/Personal Separation
```
Separate work files from personal files in Documents.
```

## Organization Workflow

### 1. Understand Scope

Ask clarifying questions:
- Which directory? (Downloads, Documents, home?)
- Main problem? (Can't find, duplicates, messy, no structure?)
- Files to avoid? (Current projects, sensitive data?)
- How aggressive? (Conservative vs. comprehensive?)

### 2. Analyze Current State

```bash
# Overview
ls -la [target]

# File types and sizes
find [target] -type f -exec file {} \; | head -20

# Largest files
du -sh [target]/* | sort -rh | head -20

# File type distribution
find [target] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

Summarize:
- Total files/folders
- File type breakdown
- Size distribution
- Date ranges
- Organization issues

### 3. Identify Patterns

**By Type:**
- Documents (PDF, DOCX, TXT)
- Images (JPG, PNG, SVG)
- Videos (MP4, MOV)
- Archives (ZIP, TAR)
- Code/Projects
- Spreadsheets (XLSX, CSV)

**By Purpose:**
- Work vs. Personal
- Active vs. Archived