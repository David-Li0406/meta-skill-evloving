---
tags: 30_Resources
---
# Obsidian Frontmatter Explorer Skill

Search and manage Obsidian note frontmatter metadata.

## Installation

This skill requires Python 3.7+ and PyYAML:

```bash
pip install pyyaml
```

## Quick Start

### Search for notes
```bash
python scripts/frontmatter_search.py "d:\00_MyData\obsidianKMS" --property tags --contains "30_Resources"
```

### List property values
```bash
python scripts/frontmatter_list.py "d:\00_MyData\obsidianKMS" --property tags
```

### Modify frontmatter (preview)
```bash
python scripts/frontmatter_modify.py "note.md" --create "reviewed:true"
```

### Apply changes
```bash
python scripts/frontmatter_modify.py "note.md" --create "reviewed:true" --apply
```

## Documentation

See [SKILL.md](SKILL.md) for complete documentation.

## Files

- `SKILL.md` - Main skill documentation
- `scripts/utils.py` - Utility functions for frontmatter operations
- `scripts/frontmatter_search.py` - Search notes by properties
- `scripts/frontmatter_list.py` - List property values
- `scripts/frontmatter_modify.py` - Create/update/delete properties
