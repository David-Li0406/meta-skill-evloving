---
name: agent-journal
description: "Search past AI agent sessions, stored knowledge, and indexed content. Use for finding previous work, recalling conventions, storing learnings, and indexing documentation."
---

# Agent Journal - Session Search, Knowledge Bank & Content Indexing

Search and retrieve past AI agent sessions, stored knowledge, and indexed content.

## When to Use

- User asks "have I done this before?" or "find previous work on X"
- User wants context from past sessions about a topic
- User needs to find how a problem was solved previously
- User wants to export or reference a past conversation
- Agent learns a convention or best practice that should be remembered
- User wants to recall project-specific knowledge
- User wants to index and search documentation or specs

## Commands

### Search Sessions

```bash
# Hybrid search (combines keyword + semantic, best quality)
agent-journal search "<query>" --mode hybrid --max 10

# Semantic search (best for concepts and "how to" queries)
agent-journal search "<query>" --mode semantic --max 10

# Lexical search (fast keyword search)
agent-journal search "<query>" --mode lexical --max 10

# Get context around matches (N messages before/after)
agent-journal search "<query>" --context 5

# Filter by project
agent-journal search "<query>" --project <project-name>

# Filter by agent
agent-journal search "<query>" --agent claude-code
agent-journal search "<query>" --agent copilot-cli

# JSON output for parsing
agent-journal search "<query>" --robot
```

### Index Sessions

```bash
# Rebuild index (run after new sessions)
agent-journal index --rebuild

# Quick incremental index
agent-journal index

# Watch mode (continuous indexing)
agent-journal index --watch
```

### Export Session

```bash
# Export to markdown
agent-journal export <session-id> --format md

# Export to HTML
agent-journal export <session-id> --format html

# Output to stdout
agent-journal export <session-id> --stdout
```

### Check Status

```bash
# Show configuration and paths
agent-journal config show

# List embedding models
agent-journal models list
```

## Search Mode Selection

| Query Type | Recommended Mode |
|------------|------------------|
| Exact error messages, file names | `lexical` |
| Concepts, "how to", similar approaches | `semantic` |
| General queries, best recall | `hybrid` |

---

## Knowledge Bank Commands

### Remember - Store Knowledge

```bash
# Store a fact or convention
agent-journal remember "Use ESLint Airbnb config for TypeScript" --tags "code-style,linting"

# Store project-specific knowledge
agent-journal remember "API uses JWT with 24h expiry" --project my-api --tags "auth,security"

# Include source reference
agent-journal remember "Pattern from auth refactoring" --source "session:abc123"
```

### Recall - Search Knowledge

```bash
# Search knowledge bank
agent-journal recall "authentication" --mode hybrid

# Filter by tags
agent-journal recall "code style" --tags "linting"

# Filter by project
agent-journal recall "conventions" --project my-api

# JSON output
agent-journal recall "security" --robot
```

### Reinforce - Keep Knowledge Fresh

```bash
# Reset decay timer when knowledge was useful
agent-journal reinforce <id>

# Reinforce multiple entries
agent-journal reinforce abc123 def456
```

### Forget - Remove Knowledge

```bash
# Remove by ID
agent-journal forget abc123
```

---

## Content Indexing Commands

Index and search markdown files, specs, and documentation.

### Index Content from Directory

```bash
# Index all markdown files in a directory
agent-journal content index ./docs --project my-project

# Index with custom filter
agent-journal content index ./specs --filter "*.md" --project api-specs

# Non-recursive indexing
agent-journal content index ./docs --recursive false

# Rebuild content index
agent-journal content index ./docs --rebuild
```

### Add Content Directly

```bash
# Add content with source identifier (for later lookup)
agent-journal content add --source "design/auth-flow" --title "Auth Flow Design" --content "..."

# Add with project and tags
agent-journal content add --source "notes/api-v2" --title "API v2 Notes" \
  --project my-api --tags "api,design"

# Pipe content from file
cat design.md | agent-journal content add --source "design/main" --title "Design Doc"
```

### Search Content

```bash
# Search indexed content
agent-journal content search "authentication flow"

# Filter by project
agent-journal content search "api design" --project my-api

# Filter by source prefix (directory/location)
agent-journal content search "endpoints" --source-prefix "docs/api/"

# Filter by tags
agent-journal content search "security" --tags "auth,security"

# Limit results
agent-journal content search "database" --max 5

# JSON output
agent-journal content search "config" --robot
```

### List Content

```bash
# List all indexed content
agent-journal content list

# Filter by project
agent-journal content list --project my-api

# Filter by source prefix
agent-journal content list --source-prefix "specs/"

# Show only expired content
agent-journal content list --expired

# JSON output
agent-journal content list --robot
```

### Remove Content

```bash
# Remove by exact source
agent-journal content remove --source "docs/old-spec.md"

# Remove by source prefix (all under directory)
agent-journal content remove --source-prefix "docs/deprecated/"

# Remove by project
agent-journal content remove --project old-project

# Remove by ID
agent-journal content remove --id abc123

# Force (skip confirmation)
agent-journal content remove --project old-project --force
```

### Reinforce Content

```bash
# Reset decay timer for important content
agent-journal content reinforce --source "docs/api-spec.md"
```

---

## Knowledge Decay System

All knowledge and content entries decay over time with a 90-day half-life:
- **Fresh (>75%)**: Recently added or reinforced
- **Good (50-75%)**: Still relevant
- **Aging (25-50%)**: Consider reinforcing
- **Decaying (<25%)**: Will expire soon ⚠️

Reinforce entries when they're useful to keep them fresh.

---

## MCP Server Mode

```bash
# Start MCP server for AI agent integration
agent-journal mcp
```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `SearchSessions` | Search sessions with context window |
| `GetSession` | Get full session details |
| `ListRecentSessions` | List recent sessions |
| `Remember` | Store knowledge |
| `Recall` | Search knowledge |
| `Reinforce` | Reset knowledge decay |
| `Forget` | Remove knowledge |
| `IndexContent` | Index markdown files |
| `AddContent` | Add content directly |
| `SearchContent` | Search indexed content |
| `ListContent` | List indexed content |
| `RemoveContent` | Remove content |
| `ReinforceContent` | Reset content decay |
| `Search` | Unified search (sessions + knowledge) |

---

## Example Workflows

### Find previous solution
```bash
agent-journal search "fix authentication error" --mode semantic --context 3 --max 5
```

### Index project documentation
```bash
agent-journal content index ./docs --project my-project
agent-journal content search "api endpoints" --project my-project
```

### Store and recall conventions
```bash
agent-journal remember "Use snake_case for database columns" --project my-api --tags "conventions,db"
agent-journal recall "database conventions" --project my-api
```

### Export for documentation
```bash
agent-journal search "implemented feature X" --mode semantic --max 1
agent-journal export <session-id> --format md
```
