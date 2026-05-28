## md2xmind Skill

Use this skill to convert Markdown files with hierarchical bullet lists to XMind (`.xmind`) format. Creates mind map files that can be opened in XMind applications.

## Requirements

- Python 3

If Python 3 is not available, install it before using this skill.

## Usage

Basic conversion:

```bash
python ~/.claude/skills/md2xmind/references/md2xmind input.md output.xmind
```

## Options

- `--title TEXT`: Set the title for the mind map (default: "Mind Map")

## Input Format

The markdown file should use hierarchical bullet lists with `-` markers:

```markdown
- Main Topic
  - Subtopic 1
    - Detail A
    - Detail B
  - Subtopic 2
    - Detail C
- Another Main Topic
  - More content
```

## Examples

Convert with custom title:

```bash
python ~/.claude/skills/md2xmind/references/md2xmind --title "Project Plan" plan.md project.xmind
```

## Features

- Supports multiple root topics
- Handles space-based (2 spaces per level) and tab-based indentation  
- Removes hierarchical numbering automatically
- Creates XMind-compatible files
- Preserves topic hierarchy and relationships