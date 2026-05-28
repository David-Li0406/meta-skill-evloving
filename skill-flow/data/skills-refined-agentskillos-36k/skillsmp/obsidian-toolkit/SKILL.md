---
name: obsidian-toolkit
description: A toolkit for interacting with an Obsidian Vault using atomic CRUD and Search operations.
---

# Obsidian Toolkit

This skill provides a set of atomic scripts to managing notes in an Obsidian Vault (or any Markdown-based knowledge base).


## Installation

Dependencies should be installed in your project's Python environment.

```bash
# Install dependencies for this skill
pip install -r .agent/skills/obsidian-toolkit/requirements.txt
```

## Usage


Each tool is a standalone Python script located in the `scripts/` directory. You can run them using `python3`.


### Markdown Syntax Guide

When creating or editing notes, you **MUST** follow the Obsidian Flavored Markdown syntax described in:
`references/obsidian_syntax.md`

This guide covers:
- **Wikilinks** (`[[Link]]`) instead of standard markdown links.
- **Callouts** (`> [!type]`) for highlighted blocks.
- **Embeds** (`![[Note]]`) for including content.
- **Frontmatter** (YAML properties) for metadata.
- **Math**, **Mermaid Diagrams**, and more.

Please consult this file to ensure all generated content is compatible with Obsidian's features.

### 1. Create a Note


Creates a new markdown note.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/create_note.py --vault "/path/to/vault" --name "folder/My New Note" --content "# Heading\n\nContent here."
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--name`: Name of the note. You can include subdirectories (e.g., `Daily/2023-10-27`). `.md` extension is automatically added if missing.
- `--content`: The text content of the note.
- `--overwrite`: (Optional) Flag to overwrite if the file already exists.

### 2. Read a Note

Reads the content of an existing note.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/read_note.py --vault "/path/to/vault" --name "My Note"
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--name`: Name of the note to read.

### 3. Update a Note

Updates an existing note by appending content or replacing it entirely.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/update_note.py --vault "/path/to/vault" --name "My Note" --content "\n## New Section" --mode append
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--name`: Name of the note to update.
- `--content`: The content to add or use as replacement.
- `--mode`: `append` (default) to add to the end, or `replace` to overwrite the entire file.

### 4. Delete a Note

Deletes a note permanently.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/delete_note.py --vault "/path/to/vault" --name "My Note"
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--name`: Name of the note to delete.

### 5. Search Notes

Searches for text across all notes in the vault.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/search_notes.py --vault "/path/to/vault" --query "TODO"
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--query`: The text string to search for.
- `--case-sensitive`: (Optional) Perform a case-sensitive search.

### 6. Analyze Tags

Analyzes tag usage across the entire vault to assess organizational efficiency.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/analyze_tags.py --vault "/path/to/vault"
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--output`: (Optional) Path to save the markdown report. If not specified, prints to stdout.
- `--verbose`: (Optional) Show detailed progress during scanning.

**Features:**
- Extracts tags from YAML frontmatter and inline `#tag` format
- Analyzes tag frequency and usage patterns
- Detects tag hierarchies (nested tags with `/`)
- Identifies similar tags that might be duplicates
- Finds low-usage tags
- Generates comprehensive markdown report with recommendations

### 7. Fix Tags

Automatically fixes common tag issues in the vault.

**Command:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/fix_tags.py --vault "/path/to/vault" --fix-format --dry-run
```

**Arguments:**
- `--vault`: Absolute path to the Obsidian Vault root.
- `--fix-format`: Fix tag formatting issues (e.g., `#tag` → `tag` in frontmatter).
- `--remove-tags`: Comma-separated list of tags to remove.
- `--remove-pattern`: Regex pattern for tags to remove.
- `--dry-run`: Preview changes without modifying files.
- `--verbose`: Show detailed progress.

**Features:**
- Fixes formatting inconsistencies in frontmatter tags
- Removes unwanted or auto-generated tags
- Dry-run mode for safe preview
- Detailed change summary

## Examples


**Creating a daily note:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/create_note.py --vault "/home/user/obsidian" --name "Daily/2023-10-27" --content "# Daily Log\n\n- [ ] Task 1"
```

**Appending a todo:**
```bash
python3 .agent/skills/obsidian-toolkit/scripts/update_note.py --vault "/home/user/obsidian" --name "Daily/2023-10-27" --content "- [ ] New Task" --mode append
```
