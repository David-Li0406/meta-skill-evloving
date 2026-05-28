# CodeCompanion Memory Skill

Search through previous CodeCompanion chat conversations using semantic search.
This is basically the "skill" equivalent of the `@memory` tool from
[codecompanion-history](https://github.com/ravitemer/codecompanion-history.nvim).


## Why does this exist?

The fantastic
[codecompanion-history](https://github.com/ravitemer/codecompanion-history.nvim)
neovim plugin is capable of summarizing and vectorizing conversations with
CodeCompanion. Once a conversation is summarized and vectorized, you can use
the `@memory` tool to search through past conversations. Under the hood, it
uses `vectorcode` to fetch relevant "memories" from the vector database. Your
next conversations will be enhanced by relevant context from past chats.

This works really well with vanilla CodeCompanion, but it doesn't work at all
when using ACP adapters (necessary to use Claude Code). This skill fills that
gap by wrapping `vectorcode` in a bash script that can be invoked as a Claude
Code skill. Ultimately, it allows you to get the same memory search functionality
when using Claude Code as you would with vanilla CodeCompanion.

## Quick Start

```bash
# Test the skill
./query.sh --query "your search query" --count 5

# Verbose mode (show full document)
./query.sh --query "authentication" --verbose

# Help
./query.sh --help
```

## Installation for Claude Code

```bash
mkdir -p ~/.claude/skills/codecompanion-memory
cp SKILL.md query.sh ~/.claude/skills/codecompanion-memory/
chmod +x ~/.claude/skills/codecompanion-memory/query.sh

# Update paths in SKILL.md
sed -i 's|~/informatique/go/codecompanion-memory/|~/.claude/skills/codecompanion-memory/|g' \
  ~/.claude/skills/codecompanion-memory/SKILL.md
```

## How It Works

```
User Query → Bash Script → VectorCode CLI → ChromaDB → Results
```

The skill wraps VectorCode to search through conversation summaries stored in ChromaDB.

## Requirements

- `bash`
- `python3` (for JSON parsing)
- `vectorcode` CLI (install with: `pipx install vectorcode`)

## Files

- `query.sh` - The skill script (3KB)
- `SKILL.md` - Claude Code skill definition
- `README.md` - This file

Total size: ~28KB

## Usage Examples

```bash
# Find past solutions
./query.sh --query "Docker networking" --count 3

# Architectural decisions
./query.sh --query "database choice" --verbose

# Code patterns
./query.sh --query "error handling Go" --count 5
```

## Output

Results are sorted by relevance (semantic similarity):

```
--- Result 1 ---
Path: 1759511459.md
Preview: ## Code Context
**Files Modified**: ardoise.ino ...
```

Full conversation summaries are in: `~/codecompanion-history/summaries/`

## Troubleshooting

**"vectorcode command not found"**
```bash
pipx install vectorcode
```

**"No results found"**
- Try broader queries
- Check summaries exist: `ls ~/codecompanion-history/summaries/`

## Performance

- First query: ~3s (cold start)
- Subsequent: ~1-2s
- Memory: ~150MB

## Documentation

See `SKILL.md` for complete documentation and Claude Code integration details.

---

**Status**: ✅ Production ready  
**Total size**: 28KB (just the essentials)
