---
name: development-workflow
description: This skill should be used when the user asks about "development workflow", "quality workflow", "symbol-based editing", "LSP navigation", "find references", "go to definition", "replace symbol body", "rename across codebase", "before making changes", "after making changes", or needs language-agnostic code editing and quality patterns. Covers built-in LSP tools and MCP symbol modification tools.
---

# Development Workflow Standards

## Symbol-Based Editing

When working with LSP-supported languages (TypeScript, JavaScript, Python, Go, Rust, Java, C++, etc.), prefer symbol-based editing using built-in LSP tools for navigation and MCP tools for modification.

### Built-in LSP Tools (Navigation)

Use the `LSP` tool for semantic code navigation. All operations require:
- `filePath` - Path to the file
- `line` - Line number (1-based, as shown in editors)
- `character` - Character offset (1-based, as shown in editors)

**Available Operations:**

| Operation | Description |
|-----------|-------------|
| `goToDefinition` | Find where a symbol is defined |
| `findReferences` | Find all references to a symbol |
| `hover` | Get documentation and type information |
| `documentSymbol` | List all symbols in a file (functions, classes, variables) |
| `workspaceSymbol` | Search for symbols across the entire workspace |
| `goToImplementation` | Find implementations of an interface or abstract method |
| `incomingCalls` | Find all functions/methods that call the function at position |
| `outgoingCalls` | Find all functions/methods called by the function at position |

**Why Prefer LSP Over Grep/Glob:**
- **Semantic understanding** - LSP understands code structure, not just text patterns
- **Accurate references** - Finds actual symbol references, not string matches
- **Scope awareness** - Distinguishes between local variables with the same name
- **Import tracking** - Understands module imports and re-exports
- **Type hierarchy** - Navigates inheritance and interface implementations

### MCP Tools (Modification)

Use MCP tools for symbol-based code modification:

- `insert_before_symbol` - Insert code before a symbol definition
- `insert_after_symbol` - Insert code after a symbol definition
- `replace_symbol_body` - Replace entire symbol body
- `rename_symbol` - Rename symbol across codebase

*Note: These are MCP tool calls - invoke them through your MCP client.*

### Example Workflow

When modifying a function in a file:

```
1. LSP documentSymbol     → See file structure (functions, classes, etc.)
2. LSP goToDefinition     → Navigate to the function you want to modify
3. LSP findReferences     → Understand all usages before changing
4. MCP replace_symbol_body → Update the function implementation
5. LSP findReferences     → Verify changes didn't break callers
```

**When to use symbol-based editing:**
- Adding new functions, classes, methods
- Modifying existing function bodies
- Refactoring with confidence about impact
- Want to preserve file organization

**When to use Edit tool instead:**
- Files without LSP support (JSON, markdown, config files)
- Complex multi-line string replacements
- Precise line-by-line edits needed

## Quality Workflow

### Before Making Changes
1. Read and understand existing code patterns
2. Use `LSP documentSymbol` to understand file structure
3. Use `LSP findReferences` to understand symbol usage
4. Run the project's lint commands to verify current state
5. If the project requires compilation (Go, Rust, C++, Java, etc.), run the build command

### After Making Changes
1. Run appropriate linting tools for the language
2. Run the project's test suite
3. Verify no new errors introduced
4. Follow project's code style conventions

## Research Tools

Use documentation tools to understand libraries:
- `resolve-library-id` - Find library documentation IDs
- `query-docs` - Get documentation for a library

## Language-Specific Standards

This skill provides generic workflow patterns. For language-specific commands and conventions, load the appropriate language skill (e.g., bun-runtime for JavaScript/TypeScript).
