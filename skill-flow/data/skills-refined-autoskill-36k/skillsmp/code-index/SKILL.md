---
name: code-index
description: Index and query the code structure and symbols. Use this to find where symbols are defined and referenced.
---

# Code Index Skill

This skill allows you to explore the codebase structure and symbols without relying on external tools or heavy indexing.
It maintains a lightweight index of files, classes, functions, and global variables.

## Commands

### Initialize
Set up the code index by defining source roots.
Command: `python3 scripts/code_index.py init`
(Interactive)

### Refresh Index
Re-scan the source roots and update the index.
Command: `python3 scripts/code_index.py index`
**Run this after significant code changes.**

### List Files
View the file structure and symbol counts.
Command: `python3 scripts/code_index.py list [--format json]`

### Statistics
View codebase statistics (files, symbols, test coverage ratio).
Command: `python3 scripts/code_index.py stats [--format json]`

### Search Symbols
Fuzzy search for symbols (classes, functions, etc.).
Command: `python3 scripts/code_index.py search <query> [--format json]`

### Lookup
Get exact definition location of a symbol or list symbols in a file.
Command: `python3 scripts/code_index.py lookup <symbol_or_filepath> [--format json]`

### Find References
Find text references to a symbol across the codebase.
Command: `python3 scripts/code_index.py references <symbol> [--format json]`

## Workflow

1.  **Exploration**: Use `list` to see the structure.
2.  **Navigation**: Use `search` to find a known symbol.
3.  **Understanding**: Use `lookup` to see where it's defined.
4.  **Impact**: Use `references` to see where it's used.
