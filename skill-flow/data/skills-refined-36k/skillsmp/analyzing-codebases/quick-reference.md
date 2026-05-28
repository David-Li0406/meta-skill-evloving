# Quick Reference - LLM Context Tools

## Commands Cheat Sheet

### Analysis
```bash
node analyze.js              # Auto-detect full/incremental
node analyze.js --force      # Force full re-analysis
node change-detector.js      # Preview changes
```

### Queries
```bash
node query.js stats          # Statistics
node query.js entry-points   # Find entry points
node query.js side-effects   # Functions with side effects
node query.js find-function <name>    # Find by name
node query.js calls-to <name>         # Who calls this?
node query.js called-by <name>        # What does this call?
node query.js trace <name>            # Call tree
```

## File Structure

```
.llm-context/
├── graph.jsonl           # Function call graph (read this!)
├── manifest.json         # Change tracking metadata
└── summaries/
    ├── L0-system.md     # Start here: 200 tokens
    ├── L1-domains.json  # Then here: domain details
    └── L2-modules.json  # Finally: module details
```

## Reading Strategy

1. **L0** (200 tokens) → Architecture overview
2. **L1** (50-100 tokens/domain) → Subsystem boundaries
3. **L2** (20-50 tokens/module) → File details
4. **Graph** (variable) → Function specifics
5. **Source** (as needed) → Targeted reading

## Common Workflows

### Understanding New Codebase
```bash
node analyze.js
cat .llm-context/summaries/L0-system.md
node query.js entry-points
node query.js stats
```

### After Code Changes
```bash
node analyze.js  # Auto-detects changes, runs incrementally
```

### Debugging
```bash
node query.js find-function <buggy-function>
node query.js calls-to <buggy-function>
node query.js side-effects | grep <keyword>
```

### Architecture Review
```bash
node query.js stats
node query.js entry-points
cat .llm-context/summaries/L1-domains.json | jq
```

## Graph Format

Each line in `graph.jsonl`:

```json
{
  "id": "functionName",
  "file": "path/to/file.js",
  "line": 42,
  "sig": "(param1, param2)",
  "async": false,
  "calls": ["foo", "bar.baz"],
  "effects": ["database", "network"],
  "scipDoc": ""
}
```

## Side Effect Types

- `file_io` - Reads/writes files
- `network` - HTTP requests, fetch, axios
- `database` - DB queries, ORM operations
- `logging` - console.log, logger calls
- `dom` - Browser DOM manipulation

## Performance

| Codebase | Initial | Incremental | Savings |
|----------|---------|-------------|---------|
| 100 files | 2-5s | 50-200ms | 90% |
| 1,000 files | 30-60s | 200-500ms | 99% |
| 10,000 files | 5-15min | 500ms-2s | 99.7% |

## Token Efficiency

Traditional approach:
- Read 10 files = 10,000 tokens

LLM-context approach:
- L0 + L1 + Graph = 500 tokens
- **95% savings**
