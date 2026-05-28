# AI-PRO Reference: Architecture and Large Codebase Intelligence

## Modern Codebase Orchestration
As codebases scale to millions of lines, the strategy for **Context Management** and **Search Efficiency** becomes paramount. This reference covers Repomix and high-performance search patterns.

## 1. Context Packing with Repomix
Repomix is the successor to traditional `llm-tldr` approaches, specifically designed for "packing" entire repositories into a single, structured file for LLM ingestion.

### Standard Configuration (`repomix.config.json`)
```json
{
  "output": "repomix-output.txt",
  "ignore": {
    "customPatterns": ["node_modules", ".next", "dist", "public/assets"],
    "useGitignore": true
  },
  "security": {
    "enableSecretDetection": true
  },
  "tokenLimit": 100000
}
```

### Usage Workflow
```bash
# Pack the current directory for analysis
bun x repomix --style xml

# Pack a specific module with dependencies
bun x repomix src/modules/auth --include "src/shared/**"
```

## 2. Monorepo Management (Bun & pnpm)
The combination of Bun for speed and pnpm for strict dependency isolation is the 2026 standard for Monorepos.

### Key Benefits:
- **Shared Workspace**: One `node_modules` at the root using hard links.
- **Fast Execution**: Bun's native workspace support is 5x faster than yarn.
- **Parallel Builds**: Native support for running tasks across all packages.

### Monorepo Structure
```text
root/
├── package.json (workspace config)
├── bun.lockb
├── packages/
│   ├── ui-core/ (Shared Components)
│   ├── api/ (Backend)
│   └── web/ (Frontend)
└── apps/
    └── docs/
```

## 3. Advanced Codebase Search (Archive Intelligence)
Navigating large archives requires moving beyond standard `grep`.

### High-Performance Grep Patterns
```bash
# Search for patterns across multiple files listed in a text file
grep --file=patterns.txt -r .

# Git Grep (Faster than standard grep in git repos)
git grep -E "AUTH_.*_SECRET" -- ':!node_modules'

# Searching with Rippgrep (Recommended)
rg -i "TODO:.*security" --type ts --glob "!**/tests/**"
```

### Codebase Indexing
For massive codebases (>10k files), use indexing tools to pre-calculate embeddings or tags.
- **Symbol Indexing**: Use `ctags` or `lsif` to generate a symbol map.
- **Semantic Search**: Use local vector databases (like ChromaDB or LanceDB) to index function signatures.

## Best Practices
1. **Context Slicing**: Only provide the relevant "slice" of the monorepo to the LLM.
2. **Deterministic Search**: Use fixed strings (`-F`) for faster searches when regex is not needed.
3. **Secret Hygiene**: Always use `repomix --check-secrets` before sharing a pack with an external LLM.

## The "Do Not" List
- **Do NOT** pipe the output of `grep -r` directly into an LLM without filtering.
- **Do NOT** use `yarn` or `npm` in a Bun-pnpm monorepo; it will break the lockfile parity.
- **Do NOT** include large binary files or build artifacts in your context packs.
- **Do NOT** ignore the power of `git log -S` (Pickaxe) to find when specific code strings were introduced.

## Performance Benchmarks
| Operation | Traditional (v4) | Modern (v5/2026) | Gain |
| :--- | :--- | :--- | :--- |
| Workspace Install | 45s | 8s | 82% |
| Full Repo Search | 12s | 1.5s | 87% |
| Context Packing | 30s | 4s | 86% |

*Updated: January 22, 2026 - 15:20*
