---
name: xmind2md
description: Use xmind2md to read and process XMind mind map files by converting them to markdown format, enabling analysis and manipulation of hierarchical mind map content. Use it for all files that end with `.xmind` extension.
---

# XMind File Reader Skill

## Instructions

Use this skill when users need to read or process XMind (.xmind) files.

### Steps:

1. **Check if Python 3 is available:**
   ```bash
   python --version
   ```
   
   If Python 3 is not installed, kindly inform the user:
   "This skill requires Python 3 to be installed on your system. Please install Python 3 and try again."

2. **Run the included xmind2md script to read XMind file and output as text:**
   ```bash
   python ~/.claude/skills/xmind-file-reader/references/xmind2md /path/to/file.xmind
   ```
   
   The command outputs the mind map structure in markdown format to stdout.

   Available options:
   - `--numbers`: Prefix bullets with hierarchical numbers (1.2.3)
   - `--max-depth N`: Limit depth (1 = root only)
   - `--sheet-sep TEXT`: Separator between sheets (default: blank line)
