---
name: file-organizer
description: Organize files and folders intelligently with duplicate detection
license: MIT
compatibility: opencode
metadata:
  audience: users
  workflow: productivity
---

# File Organizer

Intelligently organize files and folders by understanding context, finding duplicates, and suggesting better structures.

## When to Use

- Downloads folder is a mess
- Need to consolidate scattered files
- Looking for duplicate files to clean up
- Reorganizing a project structure
- Archiving old files systematically

## How to Use

### Analyze Current State

```
Analyze the structure of ~/Downloads and suggest organization
```

```
Find duplicate files in ~/Documents
```

### Organize Files

```
Organize ~/Downloads by file type
```

```
Sort these files by date and move to archive
```

### Project Cleanup

```
Reorganize this project following standard conventions
```

## Organization Strategies

### By Type (Default)

```
organized/
├── documents/     # .pdf, .doc, .txt, .md
├── images/        # .jpg, .png, .gif, .svg
├── videos/        # .mp4, .mov, .avi
├── audio/         # .mp3, .wav, .flac
├── code/          # .py, .js, .ts, .go
├── archives/      # .zip, .tar, .gz
├── data/          # .csv, .json, .xml
└── other/         # everything else
```

### By Date

```
organized/
├── 2025/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2024/
└── older/
```

### By Project

```
organized/
├── project-alpha/
│   ├── docs/
│   ├── assets/
│   └── exports/
├── project-beta/
└── unsorted/
```

## Duplicate Detection

### Find Duplicates

```bash
# By content hash (exact duplicates)
find . -type f -exec md5sum {} + | sort | uniq -d -w32

# By name (potential duplicates)
find . -type f -name "*copy*" -o -name "*(1)*"
```

### Handle Duplicates

| Strategy | When to Use |
|----------|-------------|
| Keep newest | Active files, latest version matters |
| Keep oldest | Original documents, provenance matters |
| Keep largest | Photos/videos (higher quality) |
| Keep in preferred location | Organized > Downloads |

## Process

### 1. Analyze
- List all files with sizes and dates
- Identify file types and categories
- Detect potential duplicates
- Note naming patterns

### 2. Plan
- Propose folder structure
- Show what moves where
- Highlight duplicates for decision
- Estimate space savings

### 3. Execute (with confirmation)
- Create directory structure
- Move files to destinations
- Handle duplicates per user choice
- Generate summary report

### 4. Verify
- Confirm all files accessible
- No broken links or references
- Summary of changes made

## Safety Rules

1. **Never delete without asking** - always confirm before removing
2. **Preserve originals** - copy first, delete after verification
3. **Handle conflicts** - ask when destination exists
4. **Skip system files** - ignore .DS_Store, Thumbs.db, etc.
5. **Respect .gitignore** - don't move tracked files unexpectedly

## Example Session

**User**: "Organize my Downloads folder"

**Response**:
```
## Analysis of ~/Downloads

📊 Found 847 files (12.3 GB)

### By Type
- Documents: 234 files (890 MB)
- Images: 412 files (3.2 GB)  
- Videos: 45 files (6.1 GB)
- Archives: 89 files (1.8 GB)
- Other: 67 files (340 MB)

### Duplicates Found
- 23 exact duplicates (could save 1.2 GB)
- 45 similar names (need review)

### Proposed Structure
Downloads/
├── organized/
│   ├── documents/
│   ├── images/
│   ├── videos/
│   ├── archives/
│   └── other/
├── duplicates/  # For review
└── to-sort/     # Ambiguous files

Proceed with organization? [y/n]
```
