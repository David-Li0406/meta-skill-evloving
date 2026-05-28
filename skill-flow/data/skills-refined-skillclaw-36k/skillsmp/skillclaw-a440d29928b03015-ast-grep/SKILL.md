---
name: ast-grep
description: Use this skill when you need to perform structural code searches, refactoring, or security scanning across multiple programming languages using AST analysis.
---

# AST-Grep (sg) - Structural Code Search and Refactoring

AST-Grep is a syntax-aware code search and refactoring tool that leverages Abstract Syntax Tree (AST) analysis. It is designed to understand code structure and semantics, making it more effective than regex-based searches for code analysis.

## When to Use AST-Grep

Use `sg` (ast-grep) when:

- You need to find structural code patterns (e.g., functions, classes, imports) that regex cannot capture.
- You require language-aware refactoring across multiple files.
- You are performing security scans for vulnerability patterns (e.g., SQL injection, XSS).
- You need to handle API migrations and deprecations.
- You want to enforce code style rules at the syntax level.

## Quick Start

### Basic Search Pattern
```bash
sg -p '$PATTERN' -l $LANGUAGE $PATH
```

### Search with Context
```bash
sg -p '$PATTERN' -l $LANGUAGE -C 3 $PATH  # Show 3 lines of context
sg -p '$PATTERN' -l $LANGUAGE -A 5 $PATH  # Show 5 lines after
sg -p '$PATTERN' -l $LANGUAGE -B 5 $PATH  # Show 5 lines before
```

### Interactive Rewrite
```bash
sg -p '$OLD_PATTERN' --rewrite '$NEW_PATTERN' -l $LANGUAGE --interactive $PATH
```

### Security Scan
```bash
sg scan --config sgconfig.yml
```

### JSON Output for Processing
```bash
sg -p '$PATTERN' -l $LANGUAGE --json $PATH
```

## Pattern Syntax Reference

- **`$VAR`** — matches any single node and captures it.
- **`$$`** — matches zero or more nodes (wildcard).
- **`$$$`** — matches one or more nodes.
- **Literal code** — matches exactly as written.
- **Indentation insensitive** — matches regardless of whitespace/formatting.

## Supported Languages

AST-Grep supports a wide range of programming languages, including but not limited to:

- Python
- JavaScript
- TypeScript
- Go
- Rust
- Java
- Kotlin
- C
- C++
- Ruby
- Swift
- C#

Use AST-Grep for efficient and effective code analysis and transformation tasks across these languages.