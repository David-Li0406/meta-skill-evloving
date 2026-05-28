---
name: ast-grep
description: Use this skill for structural code search, refactoring, and security scanning across multiple programming languages using AST-based analysis.
---

# AST-Grep (sg) - Structural Code Search and Refactoring

AST-Grep is a syntax-aware code search and refactoring tool that understands code structure and semantics, making it superior to regex-based searches for code analysis.

## Quick Start

### Basic Commands

```bash
# Find function calls
sg -p 'functionName($$)' -l javascript .

# Find class definitions
sg -p 'class $NAME { $$ }' -l typescript .

# Find imports
sg -p 'import { $$ } from "$MODULE"' -l javascript .

# Interactive rewrite
sg -p '$OLD_PATTERN' --rewrite '$NEW_PATTERN' -l python --interactive .
```

### When to Use AST-Grep

Use `sg` (AST-Grep) when:

- Searching for **structural code patterns** (e.g., function calls, class definitions)
- Performing **language-aware refactoring** (e.g., renaming variables, updating function signatures)
- Conducting **security scans** for vulnerabilities (e.g., SQL injection, XSS)
- Handling **API migrations** and deprecations
- Enforcing **code style rules** at the syntax level

## Pattern Syntax Basics

- **`$VAR`** — matches any single node and captures it
- **`$$`** — matches zero or more nodes (wildcard)
- **`$$$`** — matches one or more nodes
- **Literal code** — matches exactly as written
- **Indentation insensitive** — matches regardless of whitespace/formatting

## Supported Languages

AST-Grep supports 40+ languages including:

- **Web**: JavaScript, TypeScript, HTML, CSS
- **Backend**: Python, Ruby, Go, Rust, Java, C, C++
- **Others**: PHP, Scala, Elixir, Lua, and more

## Implementation Guide

### Installation

For macOS, use:
```bash
brew install ast-grep
```
For cross-platform via npm, use:
```bash
npm install -g @ast-grep/cli
```
For Rust via Cargo, use:
```bash
cargo install ast-grep
```

### Basic Pattern Matching

#### Simple Pattern Search

To find all console.log calls:
```bash
sg -p 'console.log($MSG)' -l javascript
```

To find all Python function definitions:
```bash
sg -p 'def $FUNC($$$ARGS): $$$BODY' -l python
```

### Code Transformation

#### Simple Rewrite

To rename a function:
```bash
sg -p 'oldFunc($ARGS)' --rewrite 'newFunc($ARGS)' -l python
```

To update an API call:
```bash
sg -p 'axios.get($URL)' --rewrite 'fetch($URL)' -l typescript
```

### Rule-Based Scanning

Create an `sgconfig.yml` file to define rules for scanning and transformation. For example, to detect SQL injection risks, define a rule that matches vulnerable patterns and suggests fixes.

## Advanced Usage

### Complex Patterns

Create complex rules using logical operators to combine multiple conditions. For example, to find async functions without await:
```bash
sg -p 'async function $NAME($$$PARAMS)' -l javascript --not 'await $EXPR'
```

### Performance Benefits

AST-Grep provides significant performance improvements for codebase exploration compared to text-based search, reducing false positives and unnecessary scans.

## Reference

For additional information, consult the [AST-Grep Official Documentation](https://ast-grep.github.io), the [AST-Grep GitHub Repository](https://github.com/ast-grep/ast-grep), and the [Pattern Playground](https://ast-grep.github.io/playground.html).