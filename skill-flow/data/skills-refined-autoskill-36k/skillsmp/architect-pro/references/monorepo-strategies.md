# Monorepo Strategies & Large Codebase Indexing (2026 Edition)

In 2026, managing enterprise-scale codebases requires specialized tooling for **performance**, **context awareness**, and **search efficiency**. This guide focuses on **Bun/pnpm monorepos** and **Repomix context packing**.

## 🏗️ Monorepo Architecture with Bun & pnpm
**Bun** is the preferred runtime and package manager for 2026 monorepos due to its extreme speed and native workspace support.

### Workspace Configuration
```hcl
// bunfig.toml
[install]
lockfile = true

[install.workspaces]
include = ["apps/*", "packages/*"]
```

### Dependency Management
- **Shared Packages**: Use the `workspace:*` protocol to ensure internal dependencies always point to the local version.
- **Strict Typing**: Use `tsconfig` paths to map packages during development.

## 📦 Context Packing with Repomix
AI agents need compressed, relevant context. **Repomix** is the standard tool for packing an entire repository (or parts of it) into a single, LLM-friendly file.

### Optimized Repomix Usage
```bash
# pack the core logic for AI analysis
npx repomix --include "src/domain/**/*.ts,src/application/**/*.ts" --output context-core.md --compress
```

### Why use Repomix?
- **Token Efficiency**: Removes noise (comments, empty lines) and focuses on logic.
- **Structural Integrity**: Maintains the directory tree structure so the AI understands file relationships.

## 🔍 Large Codebase Indexing (Archive Search)
Searching millions of lines of code requires more than just standard grep.

### 1. Advanced Grep Patterns
Use `--file` to search for multiple patterns at once, or `git grep` for speed within a repository.

```bash
# Fast search across the whole project ignoring ignored files
git grep -n "pattern_name"

# Search for multiple patterns defined in a file
grep -f search_patterns.txt -r . --exclude-dir=node_modules
```

### 2. Large Scale Indexing
For projects exceeding 1GB of source code, use specialized indexing tools like **Archive Searcher** patterns.
- **Frequency Analysis**: Identify most modified files to prioritize context.
- **Cross-Reference Mapping**: Use `ls-files` and `ctags` to build a symbol map.

## 🚫 Common Pitfalls
1. **Phantoms Dependencies**: Relying on dependencies from other packages without explicitly declaring them. Always use `pnpm` or `bun` workspace checks.
2. **Circular Package Imports**: `Package A -> Package B -> Package A`. Break these cycles by extracting shared logic into a `Package C`.
3. **Monolithic Builds**: Ensure your CI/CD can perform **affected builds** (only building what changed) to save time and resources.

*Updated: January 22, 2026 - 15:20*
