# DEVONthink Skill

An agent skill for automating [DEVONthink](https://www.devontechnologies.com/apps/devonthink) on macOS via JXA (JavaScript for Automation) and Python.

## Features

- **Record Management**: Create, search, move, duplicate, replicate, delete records
- **Content Operations**: Read/update record content, rename, convert formats
- **Organization**: Tags, labels, ratings, flags, custom metadata
- **Navigation**: Browse databases, groups, selected records
- **Web Import**: Create records from URLs (Markdown, PDF, HTML, web archive)
- **AI Features**: Classification, similarity search, chat/summarization
- **Bibliography Integration**: Look up bibliography citation keys and find matching DEVONthink records

## Installation

### Claude Code

```bash
git clone https://github.com/TomBener/devonthink-skill.git ~/.claude/skills/devonthink
```

### Codex

```bash
git clone https://github.com/TomBener/devonthink-skill.git ~/.codex/skills/devonthink
```

## Requirements

- macOS with DEVONthink installed
- Python 3 (for bibliography lookup)
- Zotero JSON export (for bibliography features)

## Usage Examples

### JXA Operations

Ask Claude Code to:

- "Search DEVONthink for PDFs created this week"
- "Create a new markdown note in DEVONthink"
- "Move all tagged 'inbox' records to the Archive group"
- "Find similar documents to the selected record"

### Bibliography Lookup

```bash
# Get citation key from file path
python3 devonthink/scripts/bib_lookup.py --path "/path/to/document.pdf"

# Get metadata by citation key
python3 devonthink/scripts/bib_lookup.py --citation-key "smith2024"

# Find DEVONthink records by citation key
python3 devonthink/scripts/bib_lookup.py --citation-key "smith2024" --find-devonthink
```

> **Note:** Requires `BIBLIOGRAPHY_JSON` environment variable or `--bib-json` flag. See [Configuration](#configuration).

## Skill Structure

```
devonthink/
├── SKILL.md                 # Main skill instructions
├── scripts/
│   └── bib_lookup.py        # Bibliography lookup script
└── references/
    └── jxa-api.md           # Complete JXA API reference
```

## Configuration

### Bibliography Path

The bibliography lookup script requires a Zotero JSON export. Configure it once via environment variable:

```bash
# Add to ~/.zshrc or ~/.bashrc:
export BIBLIOGRAPHY_JSON="~/Library/CloudStorage/Dropbox/pkm/bibliography.json"

# Reload shell:
source ~/.zshrc
```

**Export from Zotero:**

1. Select items or library
2. File → Export Library → CSL JSON
3. Save to a convenient location

**Or override per-command:**

```bash
python3 bib_lookup.py --citation-key "smith2024" --bib-json "~/other/bibliography.json"
```

## Related Projects

- [devonthink-mcp](https://github.com/TomBener/devonthink-mcp) - MCP server for DEVONthink (this skill is based on its functionality)

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please open an issue or PR.
