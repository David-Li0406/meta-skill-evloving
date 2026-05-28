---
name: file-organizer
description: Use this skill when you need to intelligently organize your files and folders across your computer, reducing clutter and improving your digital workspace without manual effort.
---

# File Organizer

This skill acts as your personal organization assistant, helping you maintain a clean, logical file structure across your computer without the mental overhead of constant manual organization.

## When to Use This Skill

- Your Downloads folder is a chaotic mess
- You can't find files because they're scattered everywhere
- You have duplicate files taking up space
- Your folder structure doesn't make sense anymore
- You want to establish better organization habits
- You're starting a new project and need a good structure
- You're cleaning up before archiving old projects

## What This Skill Does

1. **Analyzes Current Structure**: Reviews your folders and files to understand what you have.
2. **Finds Duplicates**: Identifies duplicate files across your system.
3. **Suggests Organization**: Proposes logical folder structures based on your content.
4. **Automates Cleanup**: Moves, renames, and organizes files with your approval.
5. **Maintains Context**: Makes smart decisions based on file types, dates, and content.
6. **Reduces Clutter**: Identifies old files you probably don't need anymore.

## How to Use

### From Your Home Directory

```bash
cd ~
```

Then run Claude Code and ask for help:

```bash
Help me organize my Downloads folder
```

```bash
Find duplicate files in my Documents folder
```

```bash
Review my project directories and suggest improvements
```

### Specific Organization Tasks

```bash
Organize these downloads into proper folders based on what they are
```

```bash
Find duplicate files and help me decide which to keep
```

```bash
Clean up old files I haven't touched in 6+ months
```

```bash
Create a better folder structure for my [work/projects/photos/etc]
```

## Instructions

When a user requests file organization help:

1. **Understand the Scope**

   Ask clarifying questions:
   - Which directory needs organization? (Downloads, Documents, entire home folder?)
   - What's the main problem? (Can't find things, duplicates, too messy, no structure?)
   - Any files or folders to avoid? (Current projects, sensitive data?)
   - How aggressively to organize? (Conservative vs. comprehensive cleanup)

2. **Analyze Current State**

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

3. **Identify Organization Patterns**

   Based on the files, determine logical groupings:
   - By Type (Documents, Images, Videos, Archives, Code/Projects)
   - By Date (Last modified, Created)
   - By Project or Category