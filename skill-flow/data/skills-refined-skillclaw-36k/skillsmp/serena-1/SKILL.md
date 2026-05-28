---
name: serena
description: Serena provides IDE-like semantic code retrieval and editing tools for coding agents, enabling efficient symbol-level code operations
license: MIT
compatibility: opencode
metadata:
    related_mcp_servers: For MCP server integration patterns, use skill `mcp-servers`
    related_coding_principles: For code quality and best practices, use skill `coding-principles`
---

# Serena

## What I Do

Serena transforms LLMs into powerful coding agents that work directly on your codebase. Unlike basic tools that read entire files or perform string-based searches, Serena provides semantic code understanding at the symbol level, making code operations more efficient and accurate.

## Key Capabilities

### Symbol-Level Code Operations

| Tool Category | Tools | Purpose |
| --- | --- | --- |
| **Symbol Discovery** | `find_symbol`, `get_symbols_overview`, `find_referencing_symbols` | Find and understand code entities |
| **Symbol Editing** | `insert_after_symbol`, `insert_before_symbol`, `replace_symbol_body`, `rename_symbol` | Modify code at symbol level |
| **File Operations** | `read_file`, `create_text_file`, `replace_content`, `replace_lines`, `delete_lines` | Standard file manipulation |
| **Project Management** | `activate_project`, `remove_project`, `onboarding`, `check_onboarding_performed` | Project setup and management |
| **Memory** | `write_memory`, `read_memory`, `list_memories`, `delete_memory` | Project-specific knowledge storage |
| **Analysis** | `search_for_pattern`, `list_dir`, `find_file` | Codebase exploration |

### Project Workflow

```text
1. Project Creation: Configure project settings (language detection, indexing)
2. Project Activation: Make Serena aware of your project
3. Onboarding: Serena learns project structure and creates memories
4. Coding Tasks: Use semantic tools for efficient code operations
```

## When to Use Me

Use this skill when:

- Working with structured codebases that benefit from symbol-level operations
- Need IDE-like capabilities (find references, rename symbols, navigate structure)
- Want to avoid reading entire files for small changes
- Need project-specific memories for context preservation
- Working with multi-file refactoring tasks

## Universal Examples

### Finding and Understanding Code

```python
# Find all symbols matching a pattern
symbols = find_symbol(
    name_path_pattern="function_name",
    relative_path="src/",
    include_kinds=[12]  # Function kind
)

# Get overview of file structure
overview = get_symbols_overview(
    relative_path="src/main.py",
    depth=1  # Include methods/fields
)

# Find all references to a symbol
references = find_referencing_symbols(
    name_path="ClassName/method_name",
    relative_path="src/file.py"
)
```

### Editing Code at Symbol Level

```python
# Insert after a symbol definition
insert_after_symbol(
    body="\n    def new_method(self):\n        pass",
    name_path="ClassName/existing_method",
    relative_path="src/file.py"
)

# Rename symbol throughout codebase
rename_symbol(
    name_path="OldClassName",
    new_name="NewClassName",
    relative_path="src/"
)

# Replace entire symbol body
replace_symbol_body(
    body="def updated_function(param: Type) -> ReturnType:\n    new implementation",
    name_path="function_name",
    relative_path="src/file.py"
)
```

### Project Memory Management

```python
# Store project knowledge
write_memory(
    memory_file_name="architecture",
    content="""# Project Architecture
This project uses a layered architecture with:
- Data layer for persistence
- Service layer for business logic
- Presentation layer for UI
Key patterns: Repository, Service, Factory"""
)

# Recall project knowledge
memories = list_memories()
architecture = read_memory(memory_file_name="architecture")
```

### File Operations

```python
# Read specific file
content = read_file(relative_path="src/module.py")

# Create or update file
create_text_file(
    relative_path="new_file.py",
    content="# New module\n\ndef main(): pass"
)

# Replace content with pattern matching
replace_content(
    needle="old_function\(\)",
    repl="new_function()",
    mode="regex",
    relative_path="src/file.py"
)
```

## Best Practices

1. **Use Symbol Tools First**: Always prefer `find_symbol` and symbol-based edits over file reading and string replacement
1. **Create Memories**: Store project context, architecture decisions, and important patterns in Serena memories
1. **Onboarding**: Let Serena perform onboarding for new projects to build initial context
1. **Type Annotations**: For dynamically typed languages, use type annotations to improve symbol detection
1. **Modular Code**: Serena works best with well-structured, modular codebases

## Integration with Other Skills

- Combine with `mcp-servers` for MCP integration patterns
- Use with `coding-principles` for code quality during edits
- Leverage `knowledge-management` for cross-project knowledge sharing
