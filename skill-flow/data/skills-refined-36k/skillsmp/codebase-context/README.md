# Codebase Context Skill

A Claude Code skill that generates comprehensive context documents for AI agents working on your codebase, with automatic staleness detection.

## What It Does

This skill creates pre-built context files that help AI agents understand your codebase immediately, without spending tokens on exploration:

| File | Purpose | Format |
|------|---------|--------|
| `codebase-context.md` | Human-readable project overview | Markdown |
| `code-index.json` | Fast lookups for concepts, exports, types | JSON |
| `deps.mermaid` | Dependency graph for tracing imports | Mermaid |

### codebase-context.md
- Project structure and architecture
- Key files organized by feature
- Naming conventions and code style
- Database schema and domain concepts
- Common commands and gotchas

### code-index.json (NEW)
- **concepts** → file locations (e.g., "authentication" → `src/auth/*.ts`)
- **entry_points** → API routes/handlers (e.g., `POST /api/login` → `src/routes/auth.ts:15`)
- **exports** → module public APIs (e.g., `src/utils.ts` → `["formatDate", "debounce"]`)
- **types** → type definitions (e.g., `User` → `src/types/user.ts:5`)

### deps.mermaid (NEW)
- Visual dependency graph in Mermaid format
- Shows which files import which
- Renders in GitHub, VSCode, and most markdown viewers

## Staleness Detection

The skill includes automatic freshness checking:

```bash
# Check if context needs regeneration
.claude/check-context-freshness.sh
```

The check detects:
- **Directory structure changes** - New folders, reorganization
- **Config file changes** - package.json, tsconfig.json, etc.
- **Age > 7 days** - Recommends weekly regeneration

## Installation

### Option 1: Clone to skills directory

```bash
git clone https://github.com/airowe/codebase-context-skill ~/.claude/skills/codebase-context
```

### Option 2: Symlink from your preferred location

```bash
git clone https://github.com/airowe/codebase-context-skill ~/path/to/skills/codebase-context
ln -s ~/path/to/skills/codebase-context ~/.claude/skills/codebase-context
```

## Usage

### Option 1: Use the extraction scripts (recommended)

Run the extraction scripts to generate machine-readable context files:

```bash
# Generate all context files at once
~/.claude/skills/codebase-context/scripts/generate-all.sh .

# Or run individually:
~/.claude/skills/codebase-context/scripts/generate-code-index.sh .
~/.claude/skills/codebase-context/scripts/generate-deps.sh . mermaid
~/.claude/skills/codebase-context/scripts/generate-deps.sh . json
```

### Option 2: Use the Claude Code skill

The skill triggers automatically when you ask Claude to:
- "Generate codebase context"
- "Create a context file for this project"
- "Document this codebase for AI agents"

Or reference it directly:
```
/skill codebase-context
```

### Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `generate-all.sh` | Run all generators | All files below |
| `generate-code-index.sh` | Extract concepts, exports, types, API routes | `code-index.json` |
| `generate-deps.sh` | Build dependency graph | `deps.mermaid`, `deps.json`, or `deps.dot` |

**Supported languages:**
- TypeScript / JavaScript (Next.js, Express, Node)
- Python (FastAPI, Flask)
- Go (partial)

For best results with TypeScript/JavaScript, install [madge](https://github.com/pahen/madge):
```bash
npm install -g madge
```

## Generated Files

After running the skill, your project will have:

```
.claude/
├── codebase-context.md           # Human-readable context
├── code-index.json               # Machine-optimized lookups
├── deps.mermaid                  # Dependency graph (Mermaid)
├── codebase-context.snapshot     # Freshness snapshot
└── check-context-freshness.sh    # Freshness check script
```

## Example Output

- [examples/codebase-context.md](examples/codebase-context.md) - Human-readable context
- [examples/code-index.json](examples/code-index.json) - Machine-optimized index
- [examples/deps.mermaid](examples/deps.mermaid) - Dependency graph (Mermaid)
- [examples/deps.dot](examples/deps.dot) - Dependency graph (GraphViz DOT)

## Why Use This?

**Before:** Every Claude Code session starts with the agent exploring your codebase, using tokens to understand structure, patterns, and conventions.

**After:** Agents read the pre-built context file and immediately understand your project, saving tokens and providing more accurate assistance.

## Best Practices

1. **Check freshness first** - Run the check script before trusting the context
2. **Regenerate after major changes** - The staleness check will remind you
3. **Reference in CLAUDE.md** - Tell agents to read it first
4. **Be specific** - Include actual file paths, not generic descriptions
5. **Commit all files** - Version control the context, snapshot, and check script

## Companion Tools

The codebase-context file provides static, high-level understanding. For deeper dynamic exploration, consider:

### [grepai](https://github.com/yoanbernabeu/grepai) - Semantic Code Search

Search code by meaning, not just text patterns. Query "user authentication flow" instead of grepping for function names.

```bash
# Install & setup
curl -sSL https://raw.githubusercontent.com/yoanbernabeu/grepai/main/install.sh | sh
cd your-project && grepai init && grepai watch

# Search by meaning
grepai search "error handling in API routes"

# Trace call graphs
grepai trace callers myFunction
```

- 100% local (uses Ollama)
- MCP server for Claude Code integration
- Real-time indexing

### Recommended Workflow

| Step | Tool | Purpose |
|------|------|---------|
| 1 | codebase-context.md | Understand project structure |
| 2 | code-index.json | Fast lookups (concepts, exports, types) |
| 3 | deps.mermaid | Trace dependencies |
| 4 | grepai | Find code by semantic meaning |
| 5 | Glob/Grep | Exact pattern matching |

### Dependency Graph Tools

For JavaScript/TypeScript projects, you can generate dependency graphs with existing tools:

```bash
# madge - simple, reliable
npx madge --json src > .claude/deps.json

# dependency-cruiser - more powerful
npx depcruise --output-type dot src > .claude/deps.dot
```

For Python:
```bash
pydeps mypackage --no-show --output .claude/deps.svg
```

## Contributing

PRs welcome! Please follow the existing format and include examples.

## License

MIT
