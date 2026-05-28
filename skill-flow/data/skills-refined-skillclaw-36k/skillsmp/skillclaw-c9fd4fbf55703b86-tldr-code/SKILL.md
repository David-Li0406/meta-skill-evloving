---
name: tldr-code
description: Use this skill for token-efficient code analysis utilizing a 5-layer stack (AST, Call Graph, CFG, DFG, PDG) to achieve 95% token savings compared to raw file reads.
---

# TLDR-Code: Complete Reference

Token-efficient code analysis. **95% savings** vs raw file reads.

## Quick Reference

| Task | Command |
|------|---------|
| File tree | `tldr tree src/` |
| Code structure | `tldr structure . --lang python` |
| Search code | `tldr search "pattern" .` |
| Call graph | `tldr calls src/` |
| Who calls X? | `tldr impact func_name .` |
| Control flow | `tldr cfg file.py func` |
| Data flow | `tldr dfg file.py func` |
| Program slice | `tldr slice file.py func 42` |
| Dead code | `tldr dead src/` |
| Architecture | `tldr arch src/` |
| Imports | `tldr imports file.py` |
| Who imports X? | `tldr importers module_name .` |
| Affected tests | `tldr change-impact --git` |
| Type check | `tldr diagnostics file.py` |
| Semantic search | `tldr semantic search "auth flow"` |

---

## The 5-Layer Stack

```
Layer 1: AST         ~500 tokens   Function signatures, imports
Layer 2: Call Graph  +440 tokens   What calls what (cross-file)
Layer 3: CFG         +110 tokens   Complexity, branches, loops
Layer 4: DFG         +130 tokens   Variable definitions/uses
Layer 5: PDG         +150 tokens   Dependencies, slicing
───────────────────────────────────────────────────────────────
Total:              ~1,200 tokens  vs 23,000 raw = 95% savings
```

---

## CLI Commands

### Navigation

```bash
# File tree
tldr tree [path]
tldr tree src/ --ext .py .ts        # Filter extensions
tldr tree . --show-hidden           # Include hidden files

# Code structure (codemaps)
tldr structure [path] --lang python
tldr structure src/ --max 100       # Max files to analyze
```

### Search

```bash
# Text search
tldr search <pattern> [path]
tldr search "def process" src/
tldr search "class.*Error" . --ext .py
tldr search "TODO" . -C 3           # 3 lines context
tldr search "func" . --max 50       # Limit results

# Semantic search (natural language)
tldr semantic search "authentication flow"
tldr semantic search "error handling" --k 10
tldr semantic search "database queries" --expand  # Include call graph
```

### File Analysis

```bash
# Full file info
tldr extract <file>
tldr extract src/api.py
tldr extract src/api.py --class UserService
```