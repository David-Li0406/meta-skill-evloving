---
name: repoprompt
description: Use RepoPrompt CLI for token-efficient codebase exploration.
---

# Skill body

## When to Use

- **Explore codebase structure** (tree, codemaps)
- **Search code** with context lines
- **Get code signatures** without full file content (token-efficient)
- **Read file slices** (specific line ranges)
- **Build context** for tasks

## Token Optimization

RepoPrompt is **more token-efficient** than raw file reads:
- `structure` → signatures only (not full content)
- `read --start-line --limit` → slices instead of full files
- `search --context-lines` → relevant matches with context

## CLI Usage

```bash
# If installed to PATH (Settings → MCP Server → Install CLI to PATH)
rp-cli -e 'command'

# Or use the alias (configure in your shell)
repoprompt_cli -e 'command'
```

## Commands Reference

### File Tree
```bash
# Full tree
rp-cli -e 'tree'

# Folders only
rp-cli -e 'tree --mode folders'

# Selected files only
rp-cli -e 'tree --mode selected'
```

### Code Structure (Codemaps) - TOKEN EFFICIENT
```bash
# Structure of specific paths
rp-cli -e 'structure src/auth/'

# Structure of selected files
rp-cli -e 'structure --scope selected'

# Limit results
rp-cli -e 'structure src/ --max-results 10'
```

### Search
```bash
# Basic search
rp-cli -e 'search "pattern"'

# With context lines
rp-cli -e 'search "error" --context-lines 3'

# Filter by extension
rp-cli -e 'search "TODO" --extensions .ts,.tsx'

# Limit results
rp-cli -e 'search "function" --max-results 20'
```

### Read Files - TOKEN EFFICIENT
```bash
# Full file
rp-cli -e 'read path/to/file.ts'

# Line range (slice)
rp-cli -e 'read path/to/file.ts --start-line 50 --limit 30'

# Last N lines (tail)
rp-cli -e 'read path/to/file.ts --start-line -20'
```

### Selection Management
```bash
# Add files to selection
rp-cli -e 'select add src/auth/'

# Set selection (replace)
rp-cli -e 'select set src/api/ src/types/'

# Clear selection
rp-cli -e 'select clear'

# View current selection
rp-cli -e 'select get'
```

### Workspace Context
```bash
# Get full context
rp-cli -e 'context'

# Specific includes
rp-cli -e 'context --include prompt,selection,tree'
```

### Chain Commands
```bash
# Multiple operations
rp-cli -e 'select set src/auth/ && structure --scope selected && context'
```

### Workspaces
```bash
# List workspaces
rp-cli -e 'workspace list'

# List tabs
rp-cli -e 'workspace tabs'

# Switch workspace
rp-cli -e 'workspace switch "ProjectName"'
```