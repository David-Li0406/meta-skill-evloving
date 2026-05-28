---
name: filesystem-skill
description: Become a helpful co-worker in the workspace. Use it whenever you need to access, manage, or reference files.
---

## Important Directories
- `/persistence` - your persistence directory for this chat session
- `/persistence/uploads` - files uploaded by the user in this chat session
- `/shared` - workspace shared across different chat sessions

- `/mnt/skills` - skills directory
- `/mnt/...` - all other directories are mounted under /mnt/

## File Path Formatting
When you create, modify, or reference files, always format them as markdown links using the file:// protocol:

[filename](file:///full/path/to/file) or `full/path/to/file`

Examples:
- "I saved the report to [report.pdf](file:///persistence/report.pdf)"
- "Check [data.csv](file:///mnt/data/data.csv) for the analysis results"
- "I've created [config.json](file:///persistence/config.json) with your settings"

This makes the path clickable for the user to view the file.

