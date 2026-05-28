# Architectural Context & Large Codebase Archiving (2026)

Strategies for managing high-context applications using Repomix, Bun/pnpm Monorepos, and advanced search techniques.

## Repomix Context Packing

Repomix is the gold standard for "packing" your codebase into a single, LLM-readable context file.

### Configuration (`repomix.config.json`)
```json
{
  "output": {
    "filePath": "codebase-context.md",
    "style": "markdown"
  },
  "include": ["src/**/*", "lib/**/*"],
  "exclude": ["node_modules", ".next", "dist", "*.log"],
  "security": {
    "enableSecretDetection": true
  }
}
```

### Usage for AI Agents
Agents should run `bun x repomix` before starting a complex refactor to ensure they have the latest architectural map.

## Monorepo Excellence: Bun & pnpm

In 2026, Bun has surpassed Node.js for developer velocity, while pnpm remains the standard for strict dependency management in large monorepos.

### Bun Workspace Layout
```yaml
# package.json
{
  "name": "my-monorepo",
  "workspaces": [
    "apps/*",
    "packages/*",
    "skills/*"
  ]
}
```

### pnpm Recursive Execution
`pnpm -r exec <command>` is essential for running migrations or builds across all packages simultaneously.

## Large Codebase Indexing & Search

When the context is too large for a single prompt, use high-speed indexing tools.

### 1. Grep --file for Pattern Matching
Use a file containing hundreds of patterns to scan for specific vulnerabilities or deprecated APIs.
`grep -f patterns.txt -r ./src`

### 2. Git Grep for Speed
Leverage the git index for searches that are 10x faster than standard grep.
`git grep "AUTH_SECRET" -- src/`

### 3. Archive Indexing (2026)
Maintain a `CODEBASE_INDEX.json` that maps every function and class to its file path, allowing agents to perform "Lookups" rather than "Full Scans".

## Modern Project Structure
- **Core Logic**: `packages/core` (Framework agnostic)
- **API Clients**: `packages/api` (Shared between frontend and backend)
- **Agents**: `apps/agents` (Autonomous GPT-5 orchestrators)

*Updated: January 22, 2026 - 15:18
