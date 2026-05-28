---
name: obsidian-markdown-vault-writer
description: Use this skill for efficient management and uploading of Markdown documents within an Obsidian vault, leveraging LSP features for search, backlink exploration, and document organization.
---

# Obsidian Markdown Vault Writer Skill

This skill facilitates the management and uploading of Markdown documents in an Obsidian vault, utilizing the markdown-oxide LSP for enhanced functionality.

## Core Features

### 1. LSP-Based Search (markdown-oxide)

When connected to the markdown-oxide MCP server, the following features are available:

- **Find References**: Locate all backlinks referencing a specific note.
- **Go to Definition**: Navigate to the actual file from `[[link]]`.
- **Tag Search**: Search all instances of `#tag`.
- **Completion**: Utilize auto-completion for links, tags, and headings.
- **Diagnostics**: Detect broken links and non-existent notes.

### 2. Vault Structure Understanding

Before performing tasks, always assess the vault structure:

```bash
# Check directory structure
ls -la

# Find MOC (Map of Content) notes
find . -name "*MOC*" -o -name "*Index*" -o -name "*목차*"

# Check recently modified notes
find . -name "*.md" -mtime -7
```

### 3. Document Uploading

Upload documents to the Obsidian vault based on the current project context:

- Automatically detect the project name from the current directory.
- Save documents in `workspace/{project}/context/` by default.
- Support for custom path mapping via `~/.agents/OBSIDIAN.md`.

### 4. Token Optimization Strategy

When processing documents, adhere to the following principles:

1. Process no more than 10 files at a time.
2. Ignore `.obsidian/` and `archive/` folders.
3. Read MOC notes first and selectively load related notes.
4. Execute `/compact` or `/clear` after 20 iterations.

## Workflow

### Document Upload Steps

1. **Project Detection**: Automatically detect the project name from the current working directory.
2. **Upload Document**: Use the following command to upload a document:

```bash
./scripts/obsidian-write.py \
  --title "Document Title" \
  --content "Markdown content"
```

### Example Usage

#### Uploading a Document

```
User: Upload this API design document to Obsidian.

Claude: Preparing to upload to Obsidian.

## Upload Information

- **Project**: agent-skills (auto-detected)
- **Save Path**: workspace/agent-skills/context/api-design.md

### Document Preview
---
created: 2025-01-15T14:30:00
project: agent-skills
tags: [claude, api, design]
---

# API Design Document

[Document content...]

Shall I upload this? (Y/n)
```

#### Tag-Based Analysis

```
User: Find notes with the #project/active tag.

Claude: Searching for notes with the specified tag using LSP.
```

## Best Practices

**DO:**
- Set the vault path as an absolute path.
- Manage metadata with frontmatter.
- Maintain a consistent folder structure.
- Review content before saving.

**DON'T:**
- Store sensitive information (API keys, passwords).
- Overwrite existing files without confirmation.
- Modify Obsidian lock files (.obsidian).

## Troubleshooting

### Common Issues

1. **Vault Path Not Found**: Ensure the path is correctly set in `~/.agents/OBSIDIAN.md`.
2. **Permission Denied**: Check write permissions for the vault folder.
3. **File Already Exists**: Confirm overwriting or use the `--suffix` option to append a number.

## Related Files

- `scripts/obsidian-write.py`: Document creation script.
- `~/.agents/OBSIDIAN.md`: User settings for vault configuration.

## Integration with Other Skills

| Skill | Integration Method |
|-------|--------------------|
| static-index | Retrieve OBSIDIAN.md file path |
| security-auditor | Check for sensitive information before saving |
| mindcontext | Integrate with project-specific context |