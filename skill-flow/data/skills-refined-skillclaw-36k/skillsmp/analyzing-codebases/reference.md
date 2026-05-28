# Command Reference

## Analysis Commands

### `llm-context analyze`

Run analysis (auto-detects full vs incremental mode)

**Behavior:**
- First run: Full analysis of all files
- Subsequent runs: Only analyzes changed files
- Creates/updates `.llm-context/` directory

**Output:**
- `graph.jsonl` - Function call graph
- `manifest.json` - Change tracking
- `summaries/L0-system.md` - System overview
- `summaries/L1-domains.json` - Domain summaries
- `summaries/L2-modules.json` - Module summaries

**Example:**
```bash
llm-context analyze
# Output: "Files re-analyzed: 3, Files skipped: 45"
```

---

### `llm-context analyze:full`

Force full re-analysis (ignore cached data)

**When to use:**
- Manifest is corrupted
- Want fresh analysis from scratch
- Debugging the tool itself

**Example:**
```bash
llm-context analyze:full
```

---

### `llm-context check-changes`

Preview what files changed without analyzing

**Output shows:**
- Added files
- Modified files (with hash changes)
- Deleted files
- Unchanged files

**Example:**
```bash
llm-context check-changes
# Output: "Changes: 2 added, 1 modified, 0 deleted"
```

---

## Query Commands

### `llm-context stats`

Show codebase statistics

**Output:**
```json
{
  "totalFunctions": 156,
  "filesAnalyzed": 47,
  "totalCalls": 423,
  "withSideEffects": 89,
  "effectTypes": ["database", "network", "file_io", "logging"]
}
```

---

### `llm-context entry-points`

Find entry point functions

**Heuristics:**
- Functions not called by others
- Functions named `main`, `init`, `start`

**Output:**
```
Found 12 results:
  1. main (src/index.js:8)
  2. handleRequest (src/server.js:23)
  ...
```

---

### `llm-context side-effects`

Find functions with side effects

**Output:**
```
Found 89 results:
  1. saveUser (src/users.js:34)
     Calls: db.query, logger.info
     Effects: database, logging
  ...
```

---

### `llm-context query <command> [args]`

Run custom queries on the graph

**Commands:**

#### `find-function <name>`
```bash
llm-context query find-function authenticateUser
```

#### `calls-to <name>`
Who calls this function?
```bash
llm-context query calls-to updateUser
# Output: handleUpdate, adminUpdate, syncData
```

#### `called-by <name>`
What does this function call?
```bash
llm-context query called-by login
# Output: validateCredentials, createSession
```

#### `trace <name>`
Show complete call tree
```bash
llm-context query trace processPayment
# Output: JSON tree showing all calls recursively
```

---

## Utility Commands

### `llm-context init`

Initialize tool in current project

**Steps:**
1. Creates `package.json` if needed
2. Installs dependencies
3. Runs initial analysis

---

### `llm-context version`

Show installed version

```bash
llm-context version
# Output: llm-context v0.2.0
```

---

### `llm-context help`

Show help message with all commands

---

## Working with Generated Files

### Read L0 Summary
```bash
cat .llm-context/summaries/L0-system.md
```

### Query Graph Directly
```bash
# Find all async functions
cat .llm-context/graph.jsonl | jq 'select(.async == true)'

# Functions with network effects
cat .llm-context/graph.jsonl | jq 'select(.effects | contains(["network"]))'
```

### Check Manifest Age
```bash
cat .llm-context/manifest.json | jq '.generated'
```

### List All Functions
```bash
cat .llm-context/graph.jsonl | jq -r '.id'
```

---

## Performance Flags

Currently all analysis is optimized automatically. Future versions may add:

```bash
# Planned features
llm-context analyze --watch    # Watch mode
llm-context analyze --parallel  # Parallel processing
```

---

## Exit Codes

- `0` - Success
- `1` - General error (file not found, parse error, etc)
- Other codes reserved for future use
