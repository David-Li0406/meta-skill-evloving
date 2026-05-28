---
name: search-mode
description: Maximum search effort mode. Launch multiple parallel agents for exhaustive codebase and documentation search. Use when you need comprehensive search results.
---

# Search Mode

> **ACTIVATION**: When loaded, immediately maximize search effort across all available tools.

## Protocol

**MAXIMIZE SEARCH EFFORT**

Launch multiple background agents IN PARALLEL:

### Agent Deployment

```
// Codebase patterns (INTERNAL)
task(agent="explore", prompt="Find [pattern 1]...", background=true)
task(agent="explore", prompt="Find [pattern 2]...", background=true)
task(agent="explore", prompt="Find [pattern 3]...", background=true)

// External resources (EXTERNAL)
task(agent="researcher", prompt="Find docs for...", background=true)
task(agent="researcher", prompt="Find GitHub examples...", background=true)
```

### Direct Tools (Use in Parallel)

| Tool | Purpose |
|------|---------|
| `search_semantic` | Natural language code search |
| `find_similar` | Find similar code patterns |
| `find_dependencies` | What depends on X? |
| `call_graph` | Function caller/callee relationships |
| `grep` | Text pattern search |
| `glob` | File pattern matching |
| `ast_grep_search` | Structural code patterns |
| `lsp_goto_definition` | Jump to symbol definition |
| `lsp_find_references` | Symbol usage across codebase |
| `lsp_symbols` | Document/workspace symbol search |
| `lsp_diagnostics` | Get errors/warnings before build |

### Search Strategy

1. **Fire 3-5 parallel agents** for broad coverage
2. **Use direct tools** for specific patterns simultaneously
3. **NEVER stop at first result** - be exhaustive
4. **Cross-reference findings** between internal and external sources

## Example Workflow

For: "Find all authentication implementations"

```
// Parallel agents
task(agent="explore", prompt="Find auth middleware implementations", background=true)
task(agent="explore", prompt="Find login/logout functions", background=true)
task(agent="explore", prompt="Find JWT/session handling", background=true)
task(agent="researcher", prompt="Find NextAuth.js best practices", background=true)

// Direct tools (in parallel)
grep(pattern="authenticate|authorization|jwt|session", include="*.ts")
glob(pattern="**/auth/**/*.ts")
ast_grep_search(pattern="async function $NAME($$$) { $$$ }", lang="typescript")
```

## Output Requirements

Synthesize ALL findings into:

1. **File inventory** with absolute paths
2. **Pattern summary** - what patterns exist
3. **Key findings** - most relevant discoveries
4. **Gaps identified** - what wasn't found
