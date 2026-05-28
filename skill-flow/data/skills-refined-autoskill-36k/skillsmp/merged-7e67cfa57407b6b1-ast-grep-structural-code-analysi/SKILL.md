---
name: ast-grep-structural-code-analysis
description: Use this skill for structural code search, refactoring, and security scanning across multiple programming languages using ast-grep.
---

# AST-Grep - Structural Code Search and Refactoring

AST-Grep (sg) is a powerful tool for syntax-aware code search and transformation, leveraging Abstract Syntax Tree (AST) analysis to provide accurate results that surpass traditional regex-based methods.

## Quick Start

### Installation

For macOS:
```bash
brew install ast-grep
```

For cross-platform via npm:
```bash
npm install -g @ast-grep/cli
```

For Rust via Cargo:
```bash
cargo install ast-grep
```

### Basic Usage

#### Search Patterns
To find specific code patterns, use:
```bash
sg -p '$PATTERN' -l $LANGUAGE $PATH
```

#### Example Searches
- Find function calls in JavaScript:
  ```bash
  sg -p 'functionName($$)' -l javascript .
  ```
- Find class definitions in TypeScript:
  ```bash
  sg -p 'class $NAME { $$ }' -l typescript .
  ```
- Find imports in Python:
  ```bash
  sg -p 'from $MODULE import $$' -l python .
  ```

### Code Transformation

#### Rewrite Patterns
To perform code transformations, use:
```bash
sg -p '$OLD_PATTERN' --rewrite '$NEW_PATTERN' -l $LANGUAGE --interactive $PATH
```

#### Example Rewrites
- Rename a function:
  ```bash
  sg -p 'oldFunc($ARGS)' --rewrite 'newFunc($ARGS)' -l python
  ```
- Update an API call:
  ```bash
  sg -p 'axios.get($URL)' --rewrite 'fetch($URL)' -l typescript
  ```

## Pattern Syntax

- **`$VAR`** — matches any single node and captures it.
- **`$$`** — matches zero or more nodes (wildcard).
- **`$$$`** — matches one or more nodes.
- **Literal code** — matches exactly as written.
- **Indentation insensitive** — matches regardless of whitespace/formatting.

## Supported Languages

AST-Grep supports over 40 languages, including:
- **Web**: JavaScript, TypeScript, HTML, CSS
- **Backend**: Python, Ruby, Go, Rust, Java, C, C++
- **Config**: YAML, JSON, TOML
- **And many more** - see [full list](https://ast-grep.github.io/reference/languages.html)

## Security Scanning

AST-Grep can also be used for security scanning to identify vulnerabilities such as SQL injection and XSS. Create a configuration file (`sgconfig.yml`) to define rules for scanning.

### Example Security Rule
```yaml
id: sql-injection-risk
language: python
severity: error
rule:
  pattern: 'cursor.execute($SQL)'
fix: 'Use parameterized queries instead'
```

## Advanced Usage

### Complex Patterns
You can create complex rules using logical operators to combine multiple conditions. For example:
```yaml
id: complex-migration
rule:
  any:
    - pattern: 'pattern1($A)'
    - pattern: 'pattern2($B)'
  not:
    pattern: 'exception($C)'
```

### Integration with CI/CD
For continuous integration, you can run scans and output results in JSON format suitable for CI/CD pipelines:
```bash
sg scan --config sgconfig.yml --json > results.json
```

## When to Use AST-Grep

Use AST-Grep when:
- You need to search for structural code patterns that regex cannot capture.
- You require language-aware refactoring across multiple files.
- You are performing security scans for vulnerability patterns.
- You need to enforce code style rules at the syntax level.

## Conclusion

AST-Grep is an essential tool for developers looking to enhance their code analysis, refactoring, and security scanning capabilities. Its ability to understand code structure and semantics makes it a superior choice for modern software development.

For more information, consult the [AST-Grep Official Documentation](https://ast-grep.github.io).