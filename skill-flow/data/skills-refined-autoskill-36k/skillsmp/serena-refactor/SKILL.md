---
name: serena-refactor
description: Large-scale refactoring using Serena's symbol-based operations. Use for renaming functions/classes/methods across codebase, updating signatures, and ensuring all references are updated consistently.
context: fork
agent: general-purpose
---

# Serena Refactor Skill

Perform large-scale, symbol-aware refactoring using Serena MCP's semantic code tools.

## Core Principles

1. **Understand before changing**: Use `find_symbol` and `get_symbols_overview` to understand the current structure
2. **Track all references**: Use `find_referencing_symbols` to find all usages before making changes
3. **Atomic operations**: Use symbol-based editing for precise, structure-aware modifications
4. **Verify completeness**: Ensure all references are updated after refactoring

## Serena MCP Tools

### Analysis Tools
- `mcp__serena__get_symbols_overview`: Get top-level symbols in a file
- `mcp__serena__find_symbol`: Find symbol by name path with optional body
- `mcp__serena__find_referencing_symbols`: Find all references to a symbol

### Editing Tools
- `mcp__serena__replace_symbol_body`: Replace entire symbol body
- `mcp__serena__insert_after_symbol`: Insert code after a symbol
- `mcp__serena__insert_before_symbol`: Insert code before a symbol
- `mcp__serena__replace_regex`: Regex-based replacement for smaller edits

### Support Tools
- `mcp__serena__search_for_pattern`: Find patterns across codebase
- `mcp__serena__list_dir`: Explore directory structure
- `mcp__serena__read_file`: Read file contents when needed

## Refactoring Workflow

1. **Identify target**: Find the symbol to refactor using `find_symbol`
2. **Map dependencies**: Use `find_referencing_symbols` to find all usages
3. **Plan changes**: Determine all files and locations that need updates
4. **Execute refactoring**:
   - Use `replace_symbol_body` for the main symbol
   - Use `replace_regex` for reference updates
5. **Verify**: Confirm all references are updated

## Supported Refactoring Types

- **Rename**: Function, class, method, variable renaming with reference updates
- **Signature change**: Update parameters/return types and all call sites
- **Extract**: Pull code into new function/class
- **Move**: Relocate symbol to different file/module
- **Inline**: Replace function calls with function body

## Response Format

```
## Refactoring Plan

- Target: [symbol name and location]
- Type: [rename/signature/extract/move/inline]
- Affected files: [list of files]
- References found: [count]

## Changes Made

1. [Change 1]
2. [Change 2]
...

## Verification

- [Status of verification]
```

## Task: $ARGUMENTS

Perform the following refactoring task using Serena's symbol-based tools:

$ARGUMENTS

Always find and update ALL references to maintain code consistency.
