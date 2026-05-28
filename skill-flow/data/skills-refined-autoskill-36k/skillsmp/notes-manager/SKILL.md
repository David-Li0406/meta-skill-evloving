---
name: Notes Manager
description: Tools for searching, reading, and adding to the user's personal notes (Obsidian vault).
---

# Notes Manager Skill

This skill allows the agent to interact with the user's Obsidian notes located at `/Users/mthorning/Documents/Notes`.

## Capabilities

### 1. Check/Search Notes
When the user asks to "check my notes" or search for something:
- **Search**: Use `grep -r` or `ripgrep` (if available) to search specifically within the `/Users/mthorning/Documents/Notes` directory.
- **Context**: Prioritize the `Daily/` and `Knowledge/` folders unless instructed otherwise.
- **Read**: Use `read_file` to retrieve the full content of relevant matches.

### 2. Add to Notes
When the user asks to "add that to my notes" or "make a not of that":
- **Default Location**: Unless a specific file is mentioned or it's obvious where the note should be made, append the information to the **Current Daily Note**.
  - Path format: `/Users/mthorning/Documents/Notes/Daily/YYYY-MM-DD.md` (e.g., `2025-01-16.md`).
  - **Create if missing**: If today's daily note doesn't exist, create it.
- **Format**:
  - Append a bullet point (`- `) followed by the content.
  - Ensure the content is formatted in Markdown.

### 3. Add to Tasks
When the user asks to "add that to my tasks":
- **Default Location**: Unless a specific file is mentioned, append the information to the **Current Daily Note**.
  - Path format: `/Users/mthorning/Documents/Notes/Daily/YYYY-MM-DD.md` (e.g., `2025-01-16.md`).
  - **Create if missing**: If today's daily note doesn't exist, create it.
- **Format**:
  - Append a task item (`- [ ] `) followed by the content.
  - Ensure the content is formatted in Markdown.

### 4. Commit and Push Changes
After making any updates to notes (adding, editing, etc.), always commit and push the changes:
- Run the script: `~/dotfiles/skills/notes/commit-and-push.sh "<description>"`
- The description should briefly describe what was added/changed (e.g., "Add project notes", "Add task for code review")
- This script will automatically commit, set the main bookmark, and push to git


## Constraints & Rules (from AGENTS.md)
1. **Preserve Structure**: Do not create new top-level directories.
2. **Privacy**: Be careful when reading from `Personal/` or `Work/` if the context implies sharing sensitive info.
3. **Formatting**: Respect existing Markdown links `[[Link]]` and tags `#tag`.

## Example Workflows

- **User**: "Check my notes for 'project alpha'."
  - **Action**: `grep -r "project alpha" /Users/mthorning/Documents/Notes`
  
- **User**: "Add this conversation to my notes."
  - **Action**: 
    1. specific_file = `/Users/mthorning/Documents/Notes/Daily/$(date +%Y-%m-%d).md`
    2. Read file to check existing content.
    3. Append the summary/content to that file.
