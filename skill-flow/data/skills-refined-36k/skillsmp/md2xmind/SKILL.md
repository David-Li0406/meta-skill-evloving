---
name: md2xmind
description: Use md2xmind to convert markdown tree structures to XMind mind map files. Converts hierarchical markdown bullet lists into .xmind format for use in mind mapping applications.
---

# Markdown to XMind Converter Skill

## Instructions

Use this skill when users need to convert markdown files with hierarchical bullet lists into XMind (.xmind) files.

### Steps:

1. **Check if Python 3 is available:**
   ```bash
   python --version
   ```
   
   If Python 3 is not installed, kindly inform the user:
   "This skill requires Python 3 to be installed on your system. Please install Python 3 and try again."

2. **Run the included md2xmind script to convert markdown to XMind:**
   ```bash
   python ~/.claude/skills/md2xmind/references/md2xmind input.md output.xmind
   ```
   
   The command creates an XMind file from the markdown bullet structure.

   Available options:
   - `--title TEXT`: Set the title for the mind map (default: "Mind Map")

### Input Format

The markdown file should contain hierarchical bullet lists using `-` markers:

```markdown
- Root Topic
  - Subtopic 1
    - Detail 1
    - Detail 2
  - Subtopic 2
- Another Root Topic
  - More content
```

### Features

- Supports multiple root topics (creates wrapper if needed)
- Handles both space-based (2 spaces per level) and tab-based indentation
- Automatically removes hierarchical numbering (e.g., "1.2.3 Title" becomes "Title")
- Creates valid XMind files compatible with XMind applications
- Generates unique IDs for all topics