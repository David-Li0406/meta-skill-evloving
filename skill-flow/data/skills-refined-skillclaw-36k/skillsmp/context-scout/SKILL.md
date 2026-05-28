---
name: context-scout
description: Token-efficient codebase exploration using RepoPrompt codemaps and slices. Use when you need deep codebase understanding without bloating context, finding all pieces of a feature across many files, or building context for code review. Requires rp-cli on macOS; degrades to repo-scout otherwise.
---

# Context Scout

Token-efficient codebase exploration using RepoPrompt's rp-cli. Gathers comprehensive context without bloating the main conversation.

**Role**: Deep context gatherer
**Purpose**: Find and summarize code across many files efficiently
**Primary tool**: rp-cli (macOS only)

## Tool Requirements

**Required tools**: rp-cli (macOS only)

**Platform detection**:
```bash
if [[ "$(uname)" == "Darwin" ]] && command -v rp-cli &>/dev/null; then
  echo "rp-cli available"
else
  echo "Degrading to repo-scout"
fi
```

**Degradation strategy** (non-macOS or no rp-cli):
```
rp-cli not available. Please use repo-scout skill instead, or manually:

1. Search for code patterns:
   grep -r '<pattern>' --include='*.ts' .

2. Get function signatures:
   grep -n 'function\|class\|interface' src/

3. Find related files:
   find . -name '*<feature>*' -type f
```

## When to Use

- Deep codebase understanding before planning/implementation
- Finding all pieces of a feature across many files
- Understanding architecture and data flow
- Building context for code review
- Exploring unfamiliar codebases efficiently

## Phase 0: Window Setup (REQUIRED)

Always start here - rp-cli needs to target the correct RepoPrompt window.

```bash
# 1. List all windows with their workspaces
rp-cli -e 'windows'

# 2. Verify with file tree (replace W with your window ID)
rp-cli -w W -e 'tree --folders'
```

All subsequent commands need `-w W` to target that window.

## CLI Quick Reference

```bash
rp-cli -e '<command>'                  # Run command (lists windows if no -w)
rp-cli -w <id> -e '<command>'          # Target specific window
rp-cli -w <id> -t <tab> -e '<cmd>'     # Target window + tab (v1.5.62+)
rp-cli -d <command>                    # Get detailed help for command
```

### Core Commands

| Command | Purpose |
|---------|---------|
| `windows` | List all windows with IDs |
| `tree` | File tree (`--folders`, `--mode selected`) |
| `structure` | Code signatures - token-efficient |
| `search` | Search (`--context-lines`, `--extensions`, `--max-results`) |
| `read` | Read file (`--start-line`, `--limit`) |
| `select` | Manage selection (`add`, `set`, `clear`, `get`) |
| `builder` | AI-powered file selection (30s-5min) |

## Exploration Workflow

### Step 1: Get Overview
```bash
rp-cli -w W -e 'tree --folders'
rp-cli -w W -e 'structure .'
```

### Step 2: Use Builder for AI-Powered Discovery
```bash
rp-cli -w W -e 'builder "Find all files implementing [FEATURE]: main implementation, types, utilities, and tests"'
```

### Step 3: Verify and Augment Selection
```bash
rp-cli -w W -e 'select get'
rp-cli -w W -e 'search "pattern" --extensions .ts --max-results 20'
rp-cli -w W -e 'select add path/to/missed/file.ts'
```

### Step 4: Deep Dive with Slices
```bash
rp-cli -w W -e 'structure --scope selected'
rp-cli -w W -e 'read src/file.ts --start-line 1 --limit 50'
```

## Token Efficiency Rules

1. **NEVER dump full files** - use `structure` for signatures
2. **Use `read --start-line --limit`** for specific sections only
3. **Use `search --max-results`** to limit output
4. **Summarize findings** - do not return raw output verbatim

| Approach | Tokens |
|----------|--------|
| Full file dump | ~5000 |
| `structure` (signatures) | ~500 |
| `read --limit 50` | ~300 |

## Output Format

```markdown
## Context Summary

[2-3 sentence overview of what you found]

### Key Files
- `path/to/file.ts:L10-50` - [what it does]
- `path/to/other.ts` - [what it does]

### Code Signatures
```typescript
// Key functions/types from structure command
function validateToken(token: string): Promise<AuthUser>
interface AuthConfig { ... }
```

### Architecture Notes
- [How pieces connect]
- [Data flow observations]

### Recommendations
- [What to focus on for the task at hand]
```

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/context-scout/SKILL.md"
# Expected: file exists, exit code 0

# Check rp-cli availability
if [[ "$(uname)" == "Darwin" ]]; then
  rp-cli --version 2>/dev/null || echo "rp-cli not installed (optional)"
else
  echo "Non-macOS: rp-cli not available, use repo-scout instead"
fi
````
